# Path of Building Import Code Format

## Format

POB2 import/export codes use:

```
base64(deflate(XML)) with + → - and / → _
```

Extracted from `src/Modules/Build.lua` line 1911:
```lua
controls.similarBuildList:SetImportCode(
    common.base64.encode(Deflate(self:SaveDB("code")))
    :gsub("+","-")
    :gsub("/","_")
)
```

## Can You Hand-Craft One?

**Yes — with caveats.** The Skills and Tree sections import correctly when using verified IDs. Items cannot be hand-crafted (require exact mod IDs from POB runtime).

### What works:
- **Skills section**: `<Gem skillId="FlickerStrikePlayer" ... />` — uses Lua keys from PoB repo, verified to import
- **Tree section**: `<SpecNode id="27176" />` — uses node IDs from `tree.json`, verified
- **Config section**: Standard settings (enemy level, main skill, boss toggle)
- **Notes section**: CDATA with build guide text

### What doesn't work:
- **Items section**: Each item requires `variantId`, exact affix `modId` values, `implicitModId`, etc. These are internal POB representations that are only generated when POB creates an item from the game data. Omit items from hand-crafted XML.

### XML structure (verified from source):
```xml
<PathOfBuilding2>
    <Build targetVersion="0_5" viewMode="TREE" level="90" className="Monk" ascendClassName="Martial Artist" mainSocketGroup="1" />
    <Config mainSkill="Flicker Strike" enemyLevel="84" enemyIsBoss="false" partySkill1="" partySkill2="" />
    <Notes><![CDATA[build guide text]]></Notes>
    <Tree activeSpec="1">
        <Spec title="Build Name" treeVersion="0_5" classInternalId="Monk" ascendancyInternalId="Monk1">
            <SpecNode id="27176" />
            <SpecNode id="65204" />
        </Spec>
    </Tree>
    <Items activeItemSet="1" showStatDifferences="false" itemSetType="Standard">
        <ItemSet id="1" title="Main" />
    </Items>
    <Skills activeSkillSet="1" defaultGemLevel="20" defaultGemQuality="20" sortGemsByDPS="true">
        <SkillSet id="1" title="Build">
            <Skill enabled="true" includeInFullDPS="true" mainActiveSkill="true" label="Name" slot="Body Armour" source="Item">
                <Gem skillId="FlickerStrikePlayer" nameSpec="Flicker Strike" level="20" quality="20" enabled="true" />
                <Gem skillId="SupportCloseCombatPlayerTwo" nameSpec="Close Combat II" level="20" quality="20" enabled="true" />
            </Skill>
        </SkillSet>
    </Skills>
    <TreeView panX="0" panY="0" zoomX="1" zoomY="1" showHeatMap="false" />
    <Calcs />
    <Import />
</PathOfBuilding2>
```

### Key rules for skill IDs:
- Use `skillId` attribute (Lua key), NOT `gemId` (ignored by importer)
- Support gem format: `Support<Name>Player` (e.g., `SupportCloseCombatPlayerTwo`)
- Active gem format: `<Name>Player` (e.g., `FlickerStrikePlayer`, `StormWavePlayer`)
- Efficiency replaces PoE1's Inspiration: `SupportEfficiencyPlayer`
- Stun replaces PoE1's Overpower: `SupportStunPlayer`

## Generation Script

Use `scripts/generate-pob-code.py` to compress XML → POB import code.

```python
import zlib, base64
with open('build.xml', 'rb') as f:
    xml = f.read()
compressed = zlib.compress(xml, 9)
code = base64.b64encode(compressed).decode('ascii')
code = code.replace('+', '-').replace('/', '_')
```

## Decoding an Import Code (for inspection)

```python
import base64, zlib
code = code.replace('-','+').replace('_','/')
code += '=' * (4 - len(code) % 4)  # fix padding
decoded = base64.b64decode(code)
xml = zlib.decompress(decoded).decode('utf-8')
```

Note: If the code is truncated (common in chat copy-paste), decompression will fail with "invalid distance" or "missing end-of-block." The XML will be garbled.
