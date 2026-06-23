# POB2 Import/Export Format — Reverse-Engineered

## Source

Reverse-engineered from `PathOfBuildingCommunity/PathOfBuilding-PoE2/src/Modules/Build.lua` (SaveDB function at line 2426) and saver modules.

## Export Format

```
base64.encode(Deflate(SaveDB("code"))):gsub("+","-"):gsub("/","_")
```

**Pipeline**: XML text → zlib deflate → base64 encode → replace `+` with `-`, `/` with `_`.

**Python encode**:
```python
import zlib, base64
compressed = zlib.compress(xml.encode(), 9)
code = base64.b64encode(compressed).decode()
code = code.replace('+', '-').replace('/', '_')
```

**Python decode**:
```python
code = code.replace('-', '+').replace('_', '/') + '=='
decoded = base64.b64decode(code)
text = zlib.decompress(decoded).decode()
```

## XML Structure

```xml
<?xml version="1.0" encoding="UTF-8"?>
<PathOfBuilding2>
    <Build targetVersion="0_5" viewMode="TREE" level="90"
           className="Monk" ascendClassName="Martial Artist"
           mainSocketGroup="1" characterLevelAutoMode="false">
        <PlayerStat stat="Life" value="2500" />
        <PlayerStat stat="EnergyShield" value="1800" />
    </Build>
    <Config ... />
    <Notes>...</Notes>
    <Party />
    <Tree activeSpec="1">
        <Spec title="..." treeVersion="0_5"
              classInternalId="Monk" ascendancyInternalId="Monk1"
              secondaryAscendClassId="0">
            <SpecNode id="27176" /> <!-- passive node allocation -->
            <SpecNode id="65204" />
        </Spec>
    </Tree>
    <TreeView panX="0" panY="0" zoomX="1" zoomY="1" showHeatMap="false" />
    <Items activeItemSet="1" showStatDifferences="false" itemSetType="Standard">
        <ItemSet id="1" title="Main" />
    </Items>
    <Skills activeSkillSet="1" defaultGemLevel="20" defaultGemQuality="20" sortGemsByDPS="true">
        <SkillSet id="1" title="Build Name">
            <Skill enabled="true" includeInFullDPS="true"
                   mainActiveSkill="true" mainActiveSkillCalcs="true"
                   label="Skill Name" slot="Body Armour" source="Item">
                <Gem skillId="FlickerStrikePlayer" nameSpec="Flicker Strike"
                     level="20" quality="20" enabled="true" />
                <Gem skillId="SupportCloseCombatPlayerTwo"
                     nameSpec="Close Combat II" level="20" quality="20" enabled="true" />
            </Skill>
        </SkillSet>
    </Skills>
    <Calcs />
    <Import />
</PathOfBuilding2>
```

## Saver Modules (from Build.lua:524)

| Section | Saver | Source |
|---------|-------|--------|
| Config | self.configTab | ConfigTab.lua |
| Notes | self.notesTab | NotesTab.lua |
| Party | self.partyTab | PartyTab.lua |
| Tree | self.treeTab | TreeTab.lua |
| TreeView | self.treeTab.viewer | TreeTab.lua |
| Items | self.itemsTab | ItemsTab.lua |
| Skills | self.skillsTab | SkillsTab.lua |
| Calcs | self.calcsTab | CalcsTab.lua |
| Import | self.importTab | ImportTab.lua |

## Spec XML Attributes (from PassiveSpec.lua:226)

```
classInternalId = "Monk"          -- NEW format (string ID)
ascendancyInternalId = "Monk1"   -- NEW format (string ID)
classId = "N"                     -- LEGACY (integer)
ascendClassId = "N"               -- LEGACY (integer)
secondaryAscendClassId = "0"     -- 0 = none
treeVersion = "0_5"
title = "Spec Name"
```

## Ascendancy Internal IDs (from tree.json)

| Class | Ascendancy | internalId |
|-------|-----------|------------|
| Monk | Martial Artist | Monk1 |
| Monk | Invoker | Monk2 |
| Monk | Acolyte of Chayula | Monk3 |
| Warrior | Titan | Warrior1 |
| Warrior | Warbringer | Warrior2 |
| Warrior | Smith of Kitava | Warrior3 |
| Huntress | Amazon | Huntress1 |
| Huntress | Spirit Walker | Huntress2 |
| Huntress | Ritualist | Huntress3 |

## Verified Skill Keys (from Skills/ .lua files)

All skillId values are the Lua table keys in `skills["..."]` — use these for XML `<Gem skillId="...">`.

### Active Skills (act_int.lua, act_dex.lua, act_str.lua)

| Display Name | skillId |
|-------------|---------|
| Flicker Strike | `FlickerStrikePlayer` |
| Siphoning Strike | `SiphoningStrikePlayer` |
| Killing Palm | `KillingPalmPlayer` |
| Storm Wave | `StormWavePlayer` |
| Tempest Bell | `TempestBellPlayer` |
| Herald of Thunder | `HeraldOfThunderPlayer` |
| Ghost Dance | `GhostDancePlayer` |

### Support Gems

**Dexterity supports (sup_dex.lua):**
| Name | skillId |
|------|---------|
| Close Combat I | `SupportCloseCombatPlayer` |
| Close Combat II | `SupportCloseCombatPlayerTwo` |
| Lightning Penetration | `SupportLightningPenetrationPlayer` |
| Culling Strike | `SupportCullingStrikePlayer` |

**Strength supports (sup_str.lua):**
| Name | skillId |
|------|---------|
| Heft | `SupportHeftPlayer` |
| Elemental Armament I | `SupportElementalArmamentPlayer` |
| Elemental Armament II | `SupportElementalArmamentPlayerTwo` |
| Efficiency I | `SupportEfficiencyPlayer` |
| Stun I | `SupportStunPlayer` |

**Intelligence supports (sup_int.lua):**
| Name | skillId |
|------|---------|
| Elemental Focus | `SupportElementalFocusPlayer` |
| Concentrated Area | `SupportConcentratedAreaPlayer` |
| Magnified Effect | `SupportMagnifiedAreaPlayer` |
| Mana Leech | `SupportManaLeechPlayer` |

## Why POB Codes Can't Be Hand-Crafted

1. **Passive tree requires connected nodes** — POB validates that every SpecNode ID is reachable from the class start via allocated path nodes. Allocating a distant node without allocating the path to it results in an import error.
2. **Items require exact affix/mod IDs** — POB doesn't parse plain-text mods. Each mod must reference an internal modifier ID from the game data.
3. **Skills require valid links** — Support gems must be compatible with the active skill's types (check `requireSkillTypes` in the support definition).
4. **No dry-run validation** — The only way to verify an import code works is to actually import it into a running POB instance.

**Best practice**: Instead of trying to hand-craft import codes, give users a setup checklist with:
- Exact passive node IDs to allocate manually
- Gem names and support order
- Ascendancy node pick order
- Gear stat priorities per slot

This is faster and avoids import failures from missing path nodes or incompatible supports.
