# Boneshatter Shockwave Chain — Mace Build Analysis

## Discovery Date
2026-06-21 (Patch 0.5.3)

## Core Mechanic

**Boneshatter cannot prime its own stun.** The skill explicitly says "Cannot cause Stun buildup" — you need a separate setup skill to put enemies into Primed for Stun state. Once Primed, Boneshatter's first hit triggers Heavy Stun → the 780% shockwave fires.

## Skill Data

### Boneshatter (Tier 1, Mace)

```
Requires: One Hand Mace or Two Hand Mace
Attack Speed: 60% of base
Initial Strike: 100-312% base, +2 Melee Strike Range
Shockwave: 250-780% base, 2m radius
Cannot cause Stun buildup
Dual Wield: 30% less damage on both hits
Quality: (0-20)% increased Attack Speed
Mana cost: 9-60
```

### Setup Skills

| Skill | Tier | Base % | Stun Utility |
|:---|:---:|:---:|:---|
| **Sunder** | 5 | 200-520% | 200% more Stun Buildup, consumes Broken Armour for Sundered Armour (extra phys damage taken) |
| **Seismic Cry** (Warcry) | N/A | AoE damage | Heavy Stuns Primed enemies INSTANTLY, Empowers next Slam with extra Aftershock. Bypasses cooldown by expending Endurance Charges. |
| **Earthquake** | 1 | 40-125% + 130-405% | Double hit = double stun buildup applied. Aftershock is always-on. |
| **Rolling Slam** | 1 | 150-468% | Second slam at 50% more damage. Knockback adds utility. |
| **Supercharged Slam** | ? | Channel | Massive single hit — best for single-target Priming |

## The Chain Mechanic

```
1. Seismic Cry → AoE damage + Heavy Stun all Primed enemies → Empowers next Slam
   (bypass cooldown with Endurance Charges for repeated uses)
   ↓
2. Boneshatter → 312% strike + 780% shockwave on Heavy Stunned target
   ↓
3. Shockwave (2m radius) → hits ALL nearby enemies → applies stun buildup to them
   ↓
4. Nearby enemies get Primed for Stun from the shockwave damage
   ↓
5. Boneshatter again on another Primed enemy → another shockwave
   ↓
6. Chain continues across entire pack — **infinite sustain as long as enemies exist**
```

## Support Setup (Mace 6-Link Boneshatter)

| Support | Category | Multiplier | Notes |
|:---|:---|:---:|:---|
| Melee Physical Damage | Melee Physical | 1.30× | More phys damage |
| Bloodlust | Bloodlust | 1.30× | More vs Bleeding. Sunder applies Bleeding. |
| Brutality | Brutality | 1.20× | More phys. Cannot deal non-phys (irrelevant). |
| Fist of War | Fist of War | 1.40× | More damage with Ancestral Boost. Empowered by Seismic Cry. |
| Heft | Heft | 1.20× | More phys attack damage |
| Close Combat | Close Combat | 1.30× | More to nearby enemies (Boneshatter is melee range) |

**Total: 1.30 × 1.30 × 1.20 × 1.40 × 1.20 × 1.30 = 4.43×**

All multipliers estimated — game client needed for exact PoE2 values.

## Damage Calculation (single Boneshatter cast)

```
Combined base: 312% + 780% = 1,092% of base
× 4.43 supports = 4,838% effective
× 290 avg weapon (2H mace: ~400 base, but reduced by 60% AS penalty)
  → let's say 350 avg with 2H mace
350 × 48.38 = 16,933 damage per cast

With Sundered Armour (Sunder debuff, ~20% inc damage taken):
  16,933 × 1.20 = 20,320

With 50% shock from alternate source (if Lightning-infused):
  20,320 × 1.50 = 30,480

Per-cast DPS ceiling: much lower than Flicker (14,226% × 290 = 41,256 BEFORE shock/crit/pen),
but Boneshatter has SUSTAINED damage with no charge management downtime.
```

## Build Comparison: Boneshatter vs Flicker Strike

| Metric | Boneshatter Chain | Flicker Strike (6 charges) |
|:---|:---:|:---:|
| Effective % per cast | 4,838% | 14,226% |
| DPS style | **Sustained chaining** | Burst → stall → burst |
| AoE | 2m shockwave, chainable | Teleport-cleave |
| Charge management | None (Endurance for Seismic Cry only) | Heavy (must build 6 charges between Flickers) |
| Defense | Warbringer (Totems, Warcries, Block) | Martial Artist (Mountain's, Evasion/ES) |
| Mana cost | 60 per cast | 85 × 13 per Flicker |
| Clear speed | Slower, more methodical | Faster, more explosive |
| Boss damage | Lower (~20k/cast) | Higher (~172k/rotation) |
| Complexity | Low (2-button: Cry → Boneshatter) | High (4-button rotation) |
| League start | **Strong** — 2H mace, no uniques needed | Medium — requires charge pathing |

## Optimal Ascendancy: Warbringer (Warrior)

- **Ancestral Bond**: +1 totem, totem buffs
- **Warcry nodes**: Empowered Warcries for bigger Seismic Cry chains
- **Jade Heritage**: Defensive layers via Endurance Charges
- Seismic Cry bypasses cooldown with Endurance Charges → Warbringer generates them efficiently

## Gear Priorities

| Slot | Priority |
|:---|:---|
| Weapon | 2H Mace: high phys DPS, +5 melee skills, attack speed |
| Body | Armour/Life — pure phys build, needs phys mitigation |
| Rings | Added phys, life, resists |
| Amulet | +1 melee skills, phys damage, life |
| Runes | Stone Runes (40% stun buildup per) in weapon, Desert/Glacial for resists in armour |
