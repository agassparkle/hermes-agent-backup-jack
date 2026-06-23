# POB Import Code — Complete Corrections (Session 2026-06-22)

## The 4 Critical Bugs Found

All four must be fixed for a POB import code to work. This session discovered each one through iterative debugging against the user's POB Community PoE2 install (v0.21.0).

### Bug 1: `classInternalId` Must Be Numeric

**Wrong:**
```xml
<Spec classInternalId="Monk" ...>
```

**Right:**
```xml
<Spec classInternalId="10" ...>  <!-- Monk = 10 -->
<Spec classInternalId="9" ...>   <!-- Mercenary = 9 -->
```

**Why:** `PassiveSpec:Load` does `tonumber(xml.attrib.classInternalId)`. String `"Monk"` returns `nil`, triggering: *"'Spec' element missing 'classId' / 'classInternalId' attribute"* error.

**How to find numeric IDs:**
```bash
grep -B5 'name="Monk"' TreeData/0_1/tree.lua | grep integerId
# Output: integerId=10

grep -B5 'name="Mercenary"' TreeData/0_1/tree.lua | grep integerId
# Output: integerId=9
```

Complete mapping for 0_1 tree:
| Class | integerId |
|:---|:---|
| Monk | 10 |
| Mercenary | 9 |
| Ranger | 2 |
| Warrior | 6 |
| Witch | 1 |
| Sorceress | 7 |

### Bug 2: Use `nodes="id1,id2,..."` Attribute, NOT `<SpecNode/>` Children

**Wrong:**
```xml
<Spec ...>
    <SpecNode id="7621" />
    <SpecNode id="23587" />
</Spec>
```

**Right:**
```xml
<Spec ... nodes="7621,23587,52448,65173,27176">
```

**Why:** `PassiveSpec:Load` iterates children looking for `URL`, `Sockets`, `WeaponSet`, and `Overrides` — but NEVER processes `SpecNode` elements. Child `SpecNode` elements are silently ignored, causing empty tree on import.

**Evidence:** Searched entire `PassiveSpec.lua` — zero references to `SpecNode` string. The old format `nodes=""` attribute is the only way.

### Bug 3: `targetVersion` and `treeVersion` Are Separate Concepts

- `targetVersion` on `<Build>` — controls the "Game Version" dialog. Must match `liveTargetVersion` from user's `GameVersions.lua`.
- `treeVersion` on `<Spec>` — controls which passive tree data directory is loaded (`TreeData/<version>/`).

**They CAN differ.** Example that worked:
```xml
<Build targetVersion="0_1" ...>
  ...
  <Spec treeVersion="0_5" ... nodes="...">
```

The user's POB had `liveTargetVersion="0_1"` (from `GameVersions.lua`) but tree data for `0_5` (from `TreeData/0_5/`). Using `targetVersion="0_5"` triggered the version dialog; using `targetVersion="0_1"` imported clean.

### Bug 4: The "Convert" Button Is Broken for Unsaved Imports

When the "Game Version" dialog appears and the user clicks "Convert to X", POB calls:
```lua
Init(self.dbFileName, self.buildName, nil, true)
```

`buildXML=nil` → skips XML loading → tries `LoadDBFile()` which fails because the import was never saved to a DB file → `CloseBuild()` → dialog reappears.

**The Convert button achieves nothing for clipboard imports.** You must match `targetVersion` exactly on first import.

## Version Testing Protocol

1. Create a minimal test XML: 1 ascendancy node, 0 skills, just class+ascendancy+Spec
2. Generate 3 POB codes with `targetVersion="0_5"`, `targetVersion="0_1"`, and no `targetVersion`
3. User imports each — whichever imports without dialog is correct
4. Use that `targetVersion` for the full build

## Compression Format (Final Answer)

POB's `ImportBuild` decodes with:
```lua
Inflate(common.base64.decode(importLink:gsub("-", "+"):gsub("_", "/")))
```

`Inflate` is raw deflate — BUT zlib-compressed codes work because the zlib wrapper bytes (0x78 0x9C) are tolerated by the inflater.

**Working code:**
```python
import zlib, base64
code = base64.b64encode(zlib.compress(xml.encode('utf-8'), 9)).decode().replace('+', '-').replace('/', '_').rstrip('=')
```

Raw deflate (`compressobj(..., -15)`) produces "Invalid input" — don't use it.

## XML Format Checklist

Minimum required elements:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<PathOfBuilding2>
    <Build targetVersion="0_1" viewMode="TREE" level="90" 
           className="Monk" ascendClassName="Invoker" 
           mainSocketGroup="1" characterLevelAutoMode="false" />
    <Config />
    <Tree activeSpec="1">
        <Spec title="Build Name" treeVersion="0_5" 
              classInternalId="10" ascendancyInternalId="Monk2" 
              secondaryAscendClassId="0" 
              nodes="7621,23587,52448,65173" />
    </Tree>
    <TreeView />
    <Items activeItemSet="1" showStatDifferences="false" itemSetType="Standard">
        <ItemSet id="1" title="Gear" />
    </Items>
    <Skills activeSkillSet="1" defaultGemLevel="20" defaultGemQuality="20">
        <SkillSet id="1" title="Skills">
            <Skill enabled="true" includeInFullDPS="true" 
                   mainActiveSkill="true" mainActiveSkillCalcs="true"
                   label="Skill Name" slot="Body Armour" source="Item">
                <Gem skillId="TempestFlurryPlayer" nameSpec="Tempest Flurry" 
                     level="20" quality="20" enabled="true" />
            </Skill>
        </SkillSet>
    </Skills>
    <Calcs />
    <Import />
</PathOfBuilding2>
```

## Ascendancy Internal ID Reference

From `TreeData/0_1/tree.lua`:
| Class | Ascendancy | internalId |
|:---|:---|:---|
| Monk | Invoker | Monk2 |
| Monk | Acolyte of Chayula | Monk3 |
| Mercenary | Witchhunter | Mercenary2 |
| Mercenary | Gemling Legionnaire | Mercenary3 |

The `ascendancyInternalId` is used directly as a string — no numeric conversion needed (`tostring()` is called on it).

## Bug 5: Two Distinct Version Dialogs — Don't Confuse Them

POB has TWO separate version mismatch warnings with completely different behavior:

| Warning | Trigger | Appearance | Convert Works? | Build Loaded? |
|:---|:---|:---|:---|:---|
| **Game Version popup** | `targetVersion ≠ liveTargetVersion` | Modal popup with title bar, Info+Warning text, Convert/Cancel buttons | **BROKEN** (see Bug 4) | Only class/ascendancy |
| **Older tree version banner** | `treeVersion ≠ latestTreeVersion` but IS recognized | Inline bar at top of tree tab: "This is an older tree version..." with "Convert to X" / "Convert all" buttons | **WORKS** | Fully loaded (nodes, skills present) |

**Key insight:** The tree version warning is BENIGN — the build has already loaded correctly. Clicking "Convert to 0_5" works because the build was fully parsed and saved before the tree comparison. This is the opposite of the game version popup where Convert is broken because the build was never saved.

**If user sees the older tree banner:** The build IS working. The nodes and skills loaded. Tell the user to click Convert — it will remap the passive tree to the current version. The build is functional either way.

## Bug 6: Skill IDs May Not Match Between Repo and Release

The repo (`PathOfBuilding-PoE2`) is a development snapshot. The user's installed POB release (e.g., v0.21.0) may have different internal skill IDs than what `grep` finds in the Lua source.

**Symptom:** Build imports with class/ascendancy visible. Ascendancy passives appear as skills (e.g., "On kill monster explosion" from Zealous Inquisition). But manual gem skills (Tempest Flurry, Galvanic Shards, etc.) show as EMPTY.

**Root cause:** `data.skills[child.attrib.skillId]` returns nil — the skill ID from the repo doesn't exist in the release's data.

**Fix:** Ask the user to export ANY working build from their POB, decompress the code, and extract the exact `skillId` values their version uses. Use those IDs in generated builds.

**Discovery method (2026-06-22 session):** User exported a build from their POB. The code started with `eNq` (zlib magic) but NEITHER zlib nor raw deflate decompression succeeded in Python:
- `zlib.decompress(data)`: `Error -3: invalid distance too far back`
- `zlib.decompress(data, -15)`: `Error -3: invalid stored block lengths`

This means the POB engine's `Deflate` function produces data that is incompatible with Python's zlib module. The import `Inflate` function (C++ engine code, not Lua) handles this non-standard format. We cannot decode user-exported POB codes in Python. To get the correct skill IDs, the user must export in a plain-text or readable format — or we must cross-reference against the installed POB's data directory (not the repo).

## Bug 7: Old `classId` Format as Fallback

If `classInternalId` (numeric string like `"10"`) fails to map through `classIntegerIdMap`, the old PoE1-style `classId` format might work:

```xml
<Spec classId="6" ascendClassId="1" ... nodes="...">
```

These are the position indices of the class (1-based) and ascendancy (1-based) in the tree.lua definition. Monk is the 6th class, Invoker is the 1st ascendancy of Monk.

**Use as last resort** when `classInternalId="10"` produces empty tree. The user's POB release might have a different `classIntegerIdMap` than the dev repo.

## Delivery Protocol

**On Telegram, use MEDIA:/path for .txt files — the user clicks to download.** Do NOT paste 1800+ char POB codes inline — the Telegram input box and POB's import field both truncate to ~50 visible characters, causing "Invalid input" errors.

User behavior observed:
- "give the files here so i can download" → MEDIA delivery works
- "no post here in the chat" → inline paste → truncated to 50 chars → fails
- "make them txt and post here" → MEDIA delivery preferred
