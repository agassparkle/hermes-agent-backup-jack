# Verified Support Gem Multipliers

> **VERIFICATION STATUS**: All multipliers below were cross-verified against BOTH the inyfinn fork AND the official `PathOfBuildingCommunity/PathOfBuilding-PoE2` repository. Every value is identical — the fork and official repo share the same game data.

> **WHEN NUMBERS CONFLICT**: PoB Lua files are authoritative over wiki. Example — Tempest Bell: wiki says Impact 490% / Shockwave 132% at lv20. PoB Lua (`act_int.lua` statSets) says Impact **408%** / Shockwave **119%**. PoB extracts directly from game data; wiki values lag behind patches.

Extracted from `PathOfBuildingCommunity/PathOfBuilding-PoE2/src/Data/Skills/sup_{str,dex,int}.lua` on 2026-06-21 (PoE2 0.5.x era).

## Verified 6-Link for Flicker Strike (Martial Artist)

| Support Gem | File | Stat | Value | Cost |
|---|---|---|---|---|
| **Close Combat II** | sup_dex.lua | `support_close_combat_attack_damage_+%_final_from_distance` | **30% MORE** | 120% |
| **Concentrated Area** | sup_int.lua | `support_area_concentrate_area_damage_+%_final` | **30% MORE area** (-50% AoE) | 100% |
| **Heft** | sup_str.lua | `support_heft_maximum_physical_damage_+%_final` | **30% MORE max phys** | 120% |
| **Elemental Armament II** | sup_str.lua | `support_attack_skills_elemental_damage_+%_final` | **25% MORE elem attack** | 120% |
| **Elemental Focus** | sup_int.lua | `support_gem_elemental_damage_+%_final` | **25% MORE elemental** | 120% |
| **Lightning Penetration** | sup_dex.lua | `base_reduce_enemy_lightning_resistance_%` | **30% penetration** | 120% |

## Verified Damage Formula (mixed phys/lightning conversion)

Flicker Strike converts 60% Physical → Lightning.

```
Physical portion (40%):
  Close Combat (1.30) × Concentrated (1.30) × Heft (1.30) = 2.197×

Lightning portion (60%):
  Close Combat (1.30) × Concentrated (1.30) × Elem Armament (1.25) × Elem Focus (1.25) = 2.641×

Weighted total: 0.40 × 2.197 + 0.60 × 2.641 = 2.464×

With Mountain's Teachings (1.15×): 2.464 × 1.15 = 2.834×

Lightning Penetration effect vs 75% res enemy:
  75% - 30% pen = 45% effective res
  Lightning damage taken: 55% / 25% = 2.20× more
  Applied to 60% lightning portion: 0.40 + 0.60 × 2.20 = 1.72×

FINAL multiplier: 2.834 × 1.72 = 4.87×
```

## Pitfall: Momentum Does NOT Work with Flicker Strike

**Verified from `sup_dex.lua`:**
```
name = "Momentum",
description = "...causing it to deal more damage if you move a sufficient distance
while using the skill. Teleportation does not count towards the distance travelled."
```
```
constantStats = {
    { "support_momentum_distance_travelled_to_gain_momentum", 20 },
    { "support_momnetum_damage_+%_final_with_momentum", 40 },  -- 40% MORE when triggered
},
```

Flicker Strike teleports → Momentum NEVER triggers. Replace with Elemental Armament II (25% MORE elemental attack).

## Verified Skill Base Damage (lv20)

| Skill | baseMultiplier | Mana | Other |
|---|---|---|---|
| **Flicker Strike** | 3.27 (327%) | 85 | 2 strikes/charge, 50% base AS, +1% crit/quality |
| **Siphoning Strike Dash** | 2.34 (234%) | 47 | - |
| **Siphoning Strike Shockwave** | 6.24 (624%) | — | Consumes Shock, grants Power Charge |
| **Killing Palm** | 2.81 (281%) | 42 | 75% base AS, Culling Strike, 0.2%/quality mana recovery |
| **Storm Wave** | 3.43 (343%) | 54 | 75% base AS, 100% more Shock chance |
| **Tempest Bell Impact** | 4.08 (408%) | 98 | 0.5s CD, 120% base AS |
| **Tempest Bell Shockwave** | 1.19 (119%) | — | Triggers on Bell hit |

**Note:** Tempest Bell numbers from PoB (408%/119%) differ from wiki (490%/132%). PoB is authoritative — wiki may have pre-0.5.0 values.

## Additional Support Gems (not used in this build)

| Support Gem | File | Stat | Value | Cost |
|---|---|---|---|---|
| Close Combat I | sup_dex.lua | `support_close_combat_attack_damage_+%_final_from_distance` | 20% MORE | 120% |
| Elemental Armament I | sup_str.lua | `support_attack_skills_elemental_damage_+%_final` | 20% MORE | 120% |
| Bloodlust | sup_str.lua | (vs Bleeding) | 30% MORE Melee Phys | — |
| Ferocity | sup_dex.lua | (consuming Frenzy) | 40% MORE Skill Speed | — |
| Dauntless | sup_str.lua | (stationary 1.5s) | 3%/0.25s up to 45% MORE | — |
| **Efficiency I** | sup_str.lua | `support_inspiration_cost_+%_final` | **-30% cost** (30% REDUCED) | 100% |
| **Stun I** | sup_str.lua | Stun Buildup | More Stun Buildup | — |
| **Mana Leech** | sup_int.lua | Mana Leech | Leeches mana from hits | — |
| **Culling Strike** | sup_dex.lua | Culling Strike | Execute enemies at low life | — |

**Important renaming note**: PoE1 "Inspiration" → PoE2 **"Efficiency"** (`SupportEfficiencyPlayer`). PoE1 "Overpower" → PoE2 **"Stun"** (`SupportStunPlayer`, which adds Stun Buildup — NOT more damage). Grep the PoB Lua files for the actual gem name before recommending a support. "Magnified Effect" in wiki = `SupportMagnifiedAreaPlayer` in PoB data.

## Key Extraction Commands

```bash
# Clone official PoB
git clone --depth 1 https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2.git

# Find a specific support gem
grep -A30 'name = "Support Name"' src/Data/Skills/sup_{str,dex,int}.lua | grep "constantStats" -A1

# Extract skill base damage at lv20
sed -n '/"SkillNamePlayer"/,/^}/p' src/Data/Skills/act_int.lua | grep "\[20\]"

# Extract charge mechanics
sed -n '/"SkillNamePlayer"/,/^}/p' src/Data/Skills/act_int.lua | grep -E "constantStats|PowerCharge|FrenzyCharge|cannot_gain"
```
