# Passive Tree Node Data (PoE2 0.5)

Extracted from `PathOfBuildingCommunity/PathOfBuilding-PoE2/src/TreeData/0_5/tree.json` on 2026-06-21.

## Extraction Method

```python
import json
with open('src/TreeData/0_5/tree.json') as f:
    tree = json.load(f)
nodes = tree['nodes']  # 4914 nodes
groups = tree['groups']  # 1623 groups (position containers)
# nodes[nodeId]['group'] indexes into groups[] for x,y coordinates
```

## Power Charge Nodes

Maximum Power Charges reachable from Monk start: **+3** (base 3 → 6 minimum, 7 with helm corrupt).

### +Maximum Power Charges

| Node ID | Name | Position | Effect |
|---------|------|----------|--------|
| 27176 | The Power Within | (3599, 2962) | +1 Max Power Charges, 20% inc Crit Damage if gained PC recently |
| 65204 | Overflowing Power | (9400, 4450) | +2 Max Power Charges |
| 1104 | Lust for Power | (-5885, -2365) | +1 Max Power Charges (too far left for Monk) |

### Power Charge Utility

| Node ID | Name | Position | Effect |
|---------|------|----------|--------|
| 9444 | One with the Storm | (10699, -1058) | Quarterstaff Skills consuming PC count as consuming 1 additional |
| 13228 | Gain Max PC on Gaining | (-7861, 2932) | 2% chance to gain max PC instead (×3 copies in same cluster) |
| 54289 | Gift of the Plains | (-7861, 2932) | 2% chance to gain max PC |
| 24812 | Power Charge Duration | (3599, 2962) | 20% inc PC Duration (×3 copies) |
| 25890 | Recover Mana on PC consume | (-6535, -4056) | Recover 2% max Mana when consuming a PC (×3 copies) |
| 58198 | Well of Power | (-6535, -4056) | 20% inc Crit Damage if consumed PC recently, recover 2% max Mana |
| 13777 | PC Duration and ES | (-8162, -1195) | 10% PC Duration, 10% inc max ES if consumed PC recently |
| 38532 | Thirst for Power | (-8162, -1195) | 25% chance to gain additional PC on PC gain |
| 36643 | Additional PC Chance | (16364, 950) | 10% chance to gain additional PC on PC gain |
| 25520 | Resonance | (5979, -1522) | Gain Power Charges instead of Frenzy Charges |
| 2516 | Price of Power | (6105, 8403) | Spells consume PC to deal 40% more Damage |

## Combo Nodes (Monk Area)

| Node ID | Name | Position | Effect |
|---------|------|----------|--------|
| 16364(asc) | Martial Adept | (16364, 950) | +1 Combo on gain, -0.2s ES delay per Combo spent |
| 16364(asc) | Martial Master | (16364, 950) | Combo from ALL Attack Hits, retained across weapons |
| — | Chakra of Impact | (10113, -1238) | 20% inc Attack Damage, 8% inc Damage per Combo consumed (up to 40%) |
| — | Chakra of Rhythm | (10113, -1238) | 6% inc Attack Speed, 20% chance extra Combo |
| — | Combo Gain | (10113, -1238) | 10% chance extra Combo (×2 copies = 20% total) |
| — | Attack Damage and Combo | (10113, -1238) | 5% inc Attack Damage, 5% chance extra Combo |
| — | Chakra of Elements | (5250, -6000) | 8% phys as extra Cold vs Shocked, 8% phys as extra Lightning vs Chilled |
| — | Chakra of Thought | (6171, -6135) | 8% MoM, 15% inc Attack Speed while not on Low Mana |
| — | Chakra of Breathing | (4872, -4974) | 20% faster ES recharge, 20% inc Evasion while have ES |

## Mace / Stun / Boneshatter Nodes (Warrior Area)

### MORE Multipliers (multiplicative with support gems)

| Node | Position | Effect |
|------|----------|--------|
| Skullcrusher | (-10198, 3732) | **20% MORE Damage** vs Heavy Stunned with Maces |
| Crushing Impacts | (-11101, 11172) | **25% MORE Damage** vs Heavy Stunned + Crushing Blows |

### Stun Buildup Nodes

| Node | Position | Effect |
|------|----------|--------|
| Crushing Verdict | (-7460, 372) | 30% inc Stun Buildup, 50% inc Attack Damage, 5% reduced AS |
| Hulking Smash | (-7729, 1935) | 30% inc Stun Buildup, +15 Str |
| Cranial Impact | (-5165, 833) | 30% inc Stun Buildup, Endurance Charge on Heavy Stun Rare/Unique |
| Impact Force | (-6849, -7456) | 20% inc Stun Buildup, 25% inc Attack Area Damage |
| Heavy Weaponry | (1485, -2827) | 15% inc Melee Damage, 15% inc Stun Buildup with 2H |
| Forcewave | (8325, -131) | 20% inc Stun Buildup, 20% inc Knockback Distance |

### Warcry Nodes

| Node | Position | Effect |
|------|----------|--------|
| Admonisher | (-5983, 3453) | 25% inc Warcry Speed, 25% inc Warcry CDR |
| Bolstering Yell | (-5983, 3453) | Empowered Attacks deal 30% inc Damage |
| Warcry Power Counted | (-5983, 3453) | 10% inc total Power counted by Warcries (×2 copies) |

### Defense/Armour Nodes

| Node | Position | Effect |
|------|----------|--------|
| Conall the Hunted | (-5722, 6103) | +15% Armour applies to Elemental Damage |
| Imploding Impacts | (-15032, 6079) | Broken Armour increases all Damage Taken from Hits, can break below 0 |

## Monk Area — Utility Nodes

| Node | Position | Effect |
|------|----------|--------|
| Electric Amplification | (1403, 958) | 18% Lightning Pen, 6% ES gained as Lightning |
| Essence of the Storm | (2727, 2025) | 5% phys as extra Lightning, 30% inc Shock effect |
| Mindful Awareness | (2940, -2768) | 24% inc Evasion, 24% inc max ES (notable) |
| Deflection | (274, 2491) | Gain Deflection = 5% of Armour |
| Hollow Palm Technique | (7274, -2313) | Can Attack as Quarterstaff while unarmed |
| One with the River | (10699, -1058) | 10% Daze on Hit, 30% inc Armour/Evasion |
| Finishing Blows | (1574, 1709) | 60% inc Damage vs Low Life enemies |

## Class Starting Positions

| Class | Approximate Area |
|-------|-----------------|
| Monk | Center-right (x: 0–12000, y: -3000–5000) |
| Warrior | Bottom-left (x: -8000–0, y: 0–8000) |
| Ranger | Top-right (x: 0–12000, y: -10000–-3000) |
| Witch/Sorceress | Far left (x: -12000–-4000, y: -5000–2000) |
| Huntress | Far top (x: 5000–18000, y: -18000–-10000) |
| Druid | Center (x: 0–8000, y: -8000–-3000) |
| Mercenary | Bottom-right (x: 4000–14000, y: 2000–7000) |
