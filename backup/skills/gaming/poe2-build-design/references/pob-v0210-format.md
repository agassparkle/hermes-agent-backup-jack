# POB v0.21.0 Verified Import Format

Reverse-engineered from actual user exports on 2026-06-22. The repo source code alone was insufficient — many silent failures only surfaced against the live release.

## Class Start Nodes (BFS Entry Points)

| Class | Node ID | Name | Connects To |
|:---|:---|:---|:---|
| Monk | **44683** | SIX | 9994 (Invoker start), 5162, 45406, 50198, 52980, 74, 11495 |
| Mercenary | **50986** | DUELIST | 7120 (Witchhunter start), 39383, 10889, 62386, 36252, 55536, 59915 |

These are the regular-tree nodes that bridge to their respective ascendancy start nodes. All BFS pathfinding for these classes MUST begin here.

## Spec Element — Complete Attribute List

```xml
<Spec classId="10" nodes="9994,17268,7621" ascendClassId="2" treeVersion="0_5"
      masteryEffects="" classInternalId="10" secondaryAscendClassId="nil"
      ascendancyInternalId="Monk2">
    <URL>https://www.pathofexile.com/passive-skill-tree/...</URL>
    <Sockets/>
    <Overrides>
        <AttributeOverride strNodes="" dexNodes="" intNodes=""/>
    </Overrides>
</Spec>
```

### Attribute Details

| Attribute | Monk/Invoker | Mercenary/Witchhunter | Notes |
|:---|:---|:---|:---|
| `classId` | `"10"` | `"9"` | Old format. Include BOTH classId and classInternalId |
| `classInternalId` | `"10"` | `"9"` | New format. Same as tree.lua integerId |
| `ascendClassId` | `"2"` | `"2"` | **POSITION INDEX** — both are 2nd ascendancy |
| `ascendancyInternalId` | `"Monk2"` | `"Mercenary2"` | String ID |
| `secondaryAscendClassId` | `"nil"` | `"nil"` | Literal string "nil" |
| `treeVersion` | `"0_5"` | `"0_5"` | Matches user's POB tree data |
| `nodes` | `"9994,17268,..."` | `"7120,20830,..."` | Comma-separated, NO SpecNode children |
| `masteryEffects` | `""` | `""` | Empty string |

## Gem Elements — Full Format

```xml
<!-- Active skill gem -->
<Gem skillId="GalvanicShardsPlayer" 
     gemId="Metadata/Items/Gem/SkillGemGalvanicShards"
     variantId="GalvanicShards"
     count="1" enabled="true" enableGlobal1="true" enableGlobal2="true"
     corrupted="false" corruptLevel="0"
     statSetIndex="nil" statSetIndexCalcs="nil"
     nameSpec="Galvanic Shards" quality="20" level="20"/>

<!-- Support gem -->
<Gem skillId="SupportEonyrsThunderPlayer"
     gemId="Metadata/Items/Gems/SupportGemEonyrsThunder"
     variantId="EonyrsThunderSupport"
     count="1" enabled="true" enableGlobal1="true" enableGlobal2="true"
     corrupted="false" corruptLevel="0"
     statSetIndex="nil" statSetIndexCalcs="nil"
     nameSpec="Eonyr's Thunder" quality="20" level="20"/>
```

### gemId Path Rules

- **Skills**: singular `"Metadata/Items/Gem/SkillGem<name>"`
- **Supports**: plural `"Metadata/Items/Gems/SupportGem<name>"`
- **Heralds**: plural `"Metadata/Items/Gems/SkillGemHeraldOfThunder"`

### variantId vs skillId

| skillId | variantId |
|:---|:---|
| `SupportEonyrsThunderPlayer` | `EonyrsThunderSupport` |
| `SupportFieryDeathPlayer` | `FieryDeathSupport` |
| `SupportShockConductionPlayer` | `ShockConductionSupport` |
| `SupportDeadlyCurrentPlayer` | `DeadlyCurrentSupport` |
| `SupportStaticShocksPlayer` | `StaticShocksSupport` |
| `SupportLightningPenetrationPlayer` | `LightningPenetrationSupport` |
| `GalvanicShardsPlayer` | `GalvanicShards` |
| `TempestFlurryPlayer` | `TempestFlurry` |
| `HeraldOfThunderPlayer` | `HeraldOfThunder` |

## Ascendancy Node IDs (Verified)

### Invoker (Monk)
9994=start, 17268=Shock Effect, 7621=Thunder, 25434=Chill Effect, 23587=Blizzard,
44357=Crit→63713=Sunder→57181=Crit→52448=Scatter, 23415=Ev/ES→8143=Grace→16100=Evasion→65173=Protect

### Witchhunter (Mercenary)
7120=start, 20830=Area of Effect→37078=Zealous Inquisition,
46535=No Mercy, 61973=Pitiless Killer, 17646=Judge Jury Executioner,
3704=Witchbane, 6935=Ceremonial Ablution, 8272=Weapon Master,
38601=Obsessive Rituals, 25172/32559/51737=Cooldown passives,
34501/61897=Armour/Evasion, 40719/43131=Damage vs Low Life

## Items Tab — Slot Elements

```xml
<Items useSecondWeaponSet="false" activeItemSet="1" showStatDifferences="true">
    <ItemSet id="1" useSecondWeaponSet="false" title="Default">
        <Slot name="Weapon 1" itemPbURL="" itemId="0"/>
        <Slot name="Body Armour" itemPbURL="" itemId="0"/>
        <!-- ... all 20+ slot types ... -->
    </ItemSet>
</Items>
```

## The #1 Silent Failure: ascendClassId

Both Invoker and Witchhunter use `ascendClassId="2"` because each is the SECOND ascendancy of their class. Using `ascendClassId="1"` produces **zero error but zero nodes** — the wrong ascendancy tree loads, so none of your node IDs exist. The UI displays the correct class/ascendancy (from the Build element), but internally the tree data belongs to the first ascendancy (Acolyte of Chayula / Gemling Legionnaire).

## Node ID Stability

Confirmed: ALL 34 nodes from a user-generated Witchhunter export (7 ascendancy + 27 regular) exist in the repo's `TreeData/0_5/tree.json`. Repo tree.json is authoritative for node IDs in POB v0.21.0.

## ADDING ITEMS TO A WORKING BUILD (step-by-step)

This is the ONLY reliable method. Do NOT hand-craft builds from scratch. Do NOT use SpecNode children. Always template from a verified working build.

### Prerequisites
- A **working POB code** that imports correctly (class, ascendancy, nodes, skills all show)
- Base types must be real PoE2 items (check wiki or use known types)
- Every item needs a unique `Unique ID` (SHA256 hash of any unique string)

### Step 1: Decode the working build
```python
import zlib, base64, re
with open('working-build.txt') as f:
    code = f.read().strip()
# Fix URL-safe encoding and padding
code = code.replace('-', '+').replace('_', '/')
padding = 4 - len(code) % 4
if padding != 4:
    code += '=' * padding
xml = zlib.decompress(base64.b64decode(code)).decode('utf-8')
```

### Step 2: Find the item to replace by its ID
Items are identified by `<Item id="N">`. Find the slot reference to get the itemId:
```xml
<Slot name="Body Armour" itemPbURL="" itemId="12"/>
```
Then find the matching `<Item id="12">...</Item>` element.

### Step 3: Create the new item XML
Copy the exact format from the existing item. Change ONLY:
- Item name (first line after `Rarity: RARE`)
- Base type (second line)
- Armour/Evasion/ES values
- `Unique ID` — generate fresh: `hashlib.sha256(b"unique-string").hexdigest()[:64]`
- Stat lines — keep the exact format (no tags = regular mod, `{crafted}` = crafted mod)
- Adjust `ModRange` count to match number of stat lines

**Item format rules:**
```
Rarity: RARE
Item Name
Base Type
Armour: 1150          ← only if armour base
Evasion: 780          ← only if evasion base
Energy Shield: 385    ← only if ES base
Unique ID: <64-char hex>
Item Level: 82
Quality: 20
Sockets: S S
Rune: Greater Iron Rune  ← one per socket
LevelReq: 70
Implicits: 0           ← number of implicit mods (0 for most rare items)
+126 to maximum Life   ← plain = regular mod, no tag
95% increased Armour and Evasion
{crafted}28% to Chaos Resistance  ← {crafted} = crafted mod
            <ModRange range="0.5" id="1"/>   ← one per mod line
            <ModRange range="0.5" id="2"/>
```

### Step 4: Replace in XML and re-encode
```python
old_item = re.search(r'<Item id="12">.*?</Item>', xml, re.DOTALL).group()
xml = xml.replace(old_item, new_item_xml)

# Re-encode with zlib (NOT raw deflate!)
encoded = base64.b64encode(zlib.compress(xml.encode('utf-8'), 9)).decode()
encoded = encoded.replace('+', '-').replace('/', '_').rstrip('=')

# CRITICAL: Verify round-trip
verify = encoded.replace('-', '+').replace('_', '/')
pad = 4 - len(verify) % 4
if pad != 4:
    verify += '=' * pad
decoded = zlib.decompress(base64.b64decode(verify)).decode('utf-8')
assert decoded == xml, "Round-trip failed!"
assert decoded.strip().endswith('</PathOfBuilding2>'), "XML truncated!"
```

### Step 5: Deliver as .txt via MEDIA
Save to `.txt` file and use `MEDIA:/path/to/file.txt` to deliver. Never paste codes inline.

### Pitfalls
- **Do NOT change any XML structure** — only replace item text content
- **Do NOT add/remove XML elements** — keep `<ModRange>`, `<Item>`, all attributes identical
- **Do NOT change `targetVersion`** — if the build works, don't touch it
- **USE ONLY VALID PoE2 BASE TYPES** — items with invalid base types silently fail to appear. See `references/poe2-valid-base-types.md` for confirmed PoE2 bases
- **Match base type to defense line** — an ES-only base (e.g. Ancestral Tiara) cannot have `Evasion:` or `Armour:` lines. Hybrid bases (e.g. Sleek Jacket) can have both
- **`secondaryAscendClassId` must be literal `"nil"`** — not `"0"`, not `""`
- **`classInternalId` must be numeric** — `"10"` not `"Monk"`, `"9"` not `"Mercenary"`
- **Use ONLY `nodes="..."` attribute** — `<SpecNode/>` children are silently ignored
- **Items must have valid base types** — POB validates these against its item database

## Critical Import-Failure Symptoms Map

| Symptom | Root Cause | Fix |
|:---|:---|:---|
| "Error parsing... 'Spec' element missing 'classId' / 'classInternalId'" | `classInternalId` is non-numeric (string like "Monk") | Use numeric integerId: 10 (Monk), 9 (Mercenary) |
| "Invalid input" popup | Raw deflate used instead of zlib | Use `zlib.compress()` not raw deflate |
| "Game Version" popup with Convert button (broken) | `targetVersion` ≠ `liveTargetVersion` | Set `targetVersion="0_1"` on `<Build>` |
| "Older tree version" banner (inline, Convert works) | `treeVersion` ≠ `latestTreeVersion` but IS valid | Harmless — nodes load. Or set `treeVersion="0_5"` |
| Build imports, class/ascendancy show, tree EMPTY | `ascendClassId` wrong OR nodes unconnected | Verify ascendClassId=2 for Invoker/Witchhunter. BFS-test connectivity |
| Build imports, ascendancy passives appear, tree empty, NO gems | `skillId` values don't match user's POB release | Export a working build, extract exact skillIds |
| Build imports, SOME gems show (ascendancy passives), NO tree | `ascendClassId` is correct but nodes are disconnected | BFS from class start node, use FULL connected path |
| Base64 decode fails ("Incorrect padding") | `rstrip('=')` removed padding needed for decode | Re-add: `padding = 4 - len(code) % 4; if padding != 4: code += '=' * padding` |
