# Extracting Working POB Codes from poe.ninja

## The Problem

POB import codes pasted in chat get **base64 corruption in transit**. The string looks complete, starts with correct `eN` zlib magic bytes, but decompression fails with "invalid distance too far back" or "invalid stored block lengths." This happens even with codes the user received from a working source (poe.ninja, pastebin, etc.).

The corruption is typically in the second half of the compressed stream — standard `zlib.decompress()` chokes at the first corrupt byte and throws an error with zero output beyond that point.

## The Solution: Byte-by-Byte Decompression

Use `zlib.decompressobj()` and feed the decoded data ONE BYTE AT A TIME. When it hits a corrupt byte, it stops but you keep ALL the decompressed data it produced before the failure:

```python
import zlib, base64

with open('code.txt') as f:
    code = f.read().strip()

padding = 4 - (len(code) % 4)
if padding != 4:
    code += '=' * padding
decoded = base64.b64decode(code.replace('-', '+').replace('_', '/'))

decomp = zlib.decompressobj(15)
xml = b''
for i in range(0, len(decoded)):
    try:
        xml += decomp.decompress(decoded[i:i+1])
    except:
        break

try:
    xml += decomp.flush()
except:
    pass

xml_str = xml.decode()
print(f"Recovered {len(xml_str)} chars")
```

This recovered 51,017 chars from a 10,284-char poe.ninja code — complete XML including closing `</PathOfBuilding2>`.

**Performance**: ~30 seconds for 10K chars. Worth it — gives you the exact XML structure POB expects.

## Re-encoding: Byte-Identical Comparison

After decompressing the original poe.ninja code byte-by-byte and re-compressing with Python zlib level 9:

```python
# Verify byte-identical re-compression
recompressed = zlib.compress(xml, 9)
assert recompressed == original_compressed  # TRUE — 0 byte differences in 9,461 bytes
```

Python's `zlib.compress(data, 9)` produces **byte-identical** output to Lua's deflate used by poe.ninja. Level 6 and 1 produce DIFFERENT output. Always use level 9 for POB codes.

## Gem Element Format (verified from working POB v0.21.0 import)

```xml
<Gem statSetIndex="nil" enableGlobal2="true" quality="20" level="20" enableGlobal1="true" 
     variantId="TempestFlurry" skillId="TempestFlurryPlayer" corruptLevel="0" corrupted="false" 
     gemId="Metadata/Items/Gem/SkillGemTempestFlurry" nameSpec="Tempest Flurry" enabled="true" 
     count="1" statSetIndexCalcs="nil"/>
```

ALL attributes required. **`statSetIndex="nil"` and `statSetIndexCalcs="nil"` must be present** — build imports silently empty without them.

### variantId vs skillId

Support gems: `skillId="SupportCloseCombatPlayerTwo"` → `variantId="CloseCombatSupportTwo"`
Heralds: `skillId="HeraldOfIcePlayer"` → `variantId="HeraldOfIce"`
Active gems: `skillId="TempestFlurryPlayer"` → `variantId="TempestFlurry"`

### gemId paths

- **Active skill gems**: `Metadata/Items/Gem/SkillGem<Name>` (singular "Gem")
- **Support gems**: `Metadata/Items/Gems/SupportGem<Name>` (plural "Gems")
- **Heralds/spirit gems**: `Metadata/Items/Gems/SkillGem<Name>` (plural "Gems", even though active)

## Ascendancy ID Mappings (Confirmed)

| Ascendancy | Class | internalId | ascendClassId | classInternalId |
|:---|:---|:---|---:|:---|
| **Martial Artist** | Monk | `Monk1` | 1 | 10 |
| **Invoker** | Monk | `Monk2` | 2 | 10 |
| Acolyte of Chayula | Monk | `Monk3` | 3 | 10 |
| **Witchhunter** | Mercenary | `Mercenary2` | 2 | 9 |
| Gemling Legionnaire | Mercenary | `Mercenary3` | 3 | 9 |
| Tactician | Mercenary | `Mercenary1` | 1 | 9 |

**CRITICAL**: `ascendClassId` is the ascendancy's POSITION INDEX (1=first, 2=second). Invoker is Monks's SECOND ascendancy → ascendClassId="2". Martial Artist is Monk's FIRST → ascendClassId="1". Verified from a working poe.ninja Martial Artist build: `<Spec ascendancyInternalId="Monk1" ascendClassId="1" classInternalId="10" .../>`

The poe.ninja format uses ONLY `classInternalId` (no `classId` attribute). POB v0.21.0 user exports include both — both work.

## Ascendancy Skills

Martial Artist ascendancy skills use the pattern:
- `skillId="HollowFocusPlayer"` → `gemId="Metadata/Items/Gem/SkillGemAscendancyHollowFocus"`
- Appear twice in the Skills section (once per allocated ascendancy node granting the skill)

## Template Modification Workflow

1. Decompress working poe.ninja code byte-by-byte
2. String-replace class/ascendancy IDs in the XML
3. String-replace the nodes attribute with your BFS-verified node list
4. Replace the entire `<Skills>...</Skills>` block with your gem setup
5. Remove `<Items>...</Items>` block (replace with `<Items/>`)
6. Set `level="90"` (or desired)
7. Re-compress with `zlib.compress(xml, 9)` + base64
8. **Always round-trip verify**: decompress the generated code and assert equality

This template-based approach succeeded where 40+ hand-crafted XML attempts with identically correct content failed. The difference is the Calcs/Config/Import sections from the original template that POB expects.
