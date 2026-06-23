# Flicker Strike Power Charge Engine — Verified Math

All numbers verified from `PathOfBuildingCommunity/PathOfBuilding-PoE2/src/Data/Skills/` on 2026-06-21.

## Core Mechanic

```
Flicker Strike (Tier 13, Quarterstaff, lv20: 327% base, 85 mana)
├── Teleports to enemy and Strikes
├── Consumes ALL Power Charges
├── 2 additional teleport Strikes per Power Charge consumed
├── 285% more Attack Speed during the sequence
├── +1% crit chance per quality (20% at 20Q)
└── CANNOT gain Power Charges while using this skill
```

## Verified Skill Data

| Skill | lv20 base | Mana | AS | Key Mechanic |
|---|---|---|---|---|
| Flicker Strike | 327% | 85 | 50% base | 2 strikes/charge, no charge gain during |
| Killing Palm | 281% | 42 | 75% base | Culling Strike, 1/2/3 charges per kill, 4% mana on cull at 20Q |
| Siphoning Strike Dash | 234% | 47 | — | Dash + melee strike |
| Siphoning Strike Shockwave | 624% | — | — | Consumes Shock, grants 1 Power Charge |
| Storm Wave | 343% | 54 | 75% base | 8m line, 100% more Shock chance |
| Tempest Bell Impact | 408% | 98 | 120% base | 0.5s CD, requires 4 Combo |
| Tempest Bell Shockwave | 119% | — | — | Triggers when Bell is Hit |

## Verified Support Gem Multipliers (6-Link Flicker Strike)

| Support | % | Type | Applies To |
|---|---|---|---|
| Close Combat II | 30% MORE | Generic damage | ALL damage (10-35 unit ramp) |
| Concentrated Area | 30% MORE | Area damage | ALL area damage (-50% AoE) |
| Heft | 30% MORE | Max phys | Physical portion only (40% of hit) |
| Elemental Armament II | 25% MORE | Elem attack | Lightning portion only (60% of hit) |
| Elemental Focus | 25% MORE | Elemental | Lightning portion only (cannot inflict ailments) |
| Lightning Penetration | 30% pen | — | Enemy lightning res -30% |

## Damage Calculation (6 Power Charges)

```
Strikes per Flicker: 1 + 6 × 2 = 13

Supports weighted multiplier:
  Phys portion (40%): 1.30 × 1.30 × 1.30 = 2.197
  Light portion (60%): 1.30 × 1.30 × 1.25 × 1.25 = 2.641
  Weighted: 0.40 × 2.197 + 0.60 × 2.641 = 2.464

With Mountain's Teachings: 2.464 × 1.15 = 2.834

Lightning pen vs 75% res: (100-45)/(100-75) = 2.20× on lightning
  Effective: 0.40 + 0.60 × 2.20 = 1.72

FINAL multiplier: 2.834 × 1.72 = 4.87×

Per-strike effective: 327% × 4.87 = 1,592%
Full Flicker (13 strikes): 1,592% × 13 = 20,696%
```

## Charge Breakpoints

| Charges | Strikes | Effective % |
|---|---|---|
| 3 (base) | 7 | 11,144% |
| 4 | 9 | 14,328% |
| 5 | 11 | 17,512% |
| 6 | 13 | 20,696% |
| 7 | 15 | 23,880% |
| 8 | 17 | 27,064% |

## Rotation

```
1. Storm Wave     → shock pack (8m line, 100% more shock chance built-in)
2. Killing Palm   → cull 2-3 enemies → 3-7 Power Charges
3. Siphoning ×1   → consume remaining shock → 624% shockwave + 1 Charge
4. Flicker Strike  → 13 strikes at 1,592% each → 20,696% total
5. Tempest Bell   → drop from 26 accumulated Combo (Martial Adept + Master)
6. Repeat
```

## Martial Artist Synergies

- **Martial Master**: All 13 Flicker hits generate Combo → 13 base
- **Martial Adept**: +1 per gain → 26 total Combo per Flicker
- **Tempest Bell cost**: 4 Combo → can drop Bell 6 times per Flicker
- **Way of the Mountain**: 15% more damage always active, 40% less chip damage
- **Runic Meridians**: 5 free rune sockets for stats/defense

## Mana Sustain

```
Flicker total cost: 85 × 13 = 1,105 mana
Killing Palm recovery (2 kills): 4% × 2000 × 2 = 160 over 4s
Mana on kill (rings, 10 kills): ~150
Leech (Mind Rune 4% phys): ~60 per Flicker
Mana Flask (Enduring): covers the gap (~700 deficit)
```

## Pitfalls

- **Momentum DOES NOT WORK**: "Teleportation does not count towards distance travelled." Replace with Elemental Armament II.
- **Cannot gain charges during Flicker**: Must build 5-6 charges BEFORE pressing Flicker. Killing Palm and Siphoning Strike are the charge builders.
- **Bosses without adds**: Use Conductivity curse + Siphoning Strike for guaranteed Shock → charge generation. Slower on pure single-target.
- **Heft + Elemental Armament only affect their respective damage portions**: Weighted average formula is critical for accurate DPS.

## What Still Needs Verification

- Overcharge passive exact location and +charges on tree
- Tempest Bell + Flicker Strike hit detection (does Flicker hit the Bell? needs gameplay)
- Hollow Form/Resonance/Focus full descriptions
