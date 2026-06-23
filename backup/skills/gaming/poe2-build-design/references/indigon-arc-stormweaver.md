# Indigon Mana Stacker Arc Stormweaver (v0.4.0 — OUTDATED)

> **⚠️ This build was designed for 0.4.0. ES defense has been gutted in 0.5.0.**
> The Indigon + Cloak of Defiance core is still valid, but the ES-recharge-based defense layer documented here no longer works. See `references/v0.5.0-changes.md` for the defense meta shift.
> The Indigon CALCULATION METHOD (damage per mana spent, mana sustain math) remains useful as a template.

Designed June 2026. Full build with damage calculations.

## Core Items

### Indigon (Magus Tiara) — Survived 0.5.0 unchanged
- ES: 180-216
- Requires Level 65, 91 Int
- (100-140)% increased Energy Shield
- +(80-120) to maximum Mana
- **(10-15)% increased Spell damage for each 200 total Mana Spent Recently**
- (5-10)% increased Cost of Skills for each 200 total Mana Spent Recently
- Mana Recovery other than Regeneration cannot Recover Mana

### Cloak of Defiance — Survived 0.5.0 unchanged
- 50% of Damage is taken from Mana before Life (MoM)

## Class: Sorceress → Stormweaver

Ascendancy nodes (4 notables):
1. **Force of Will**: 20% MoM, +20% Arcane Surge magnitude per 10% missing mana
2. **Refracted Infusion**: 50% chance double Elemental Infusion
3. **Multiplying Squalls**: +2 Elemental Skill limit
4. **Tempest Caller**: Elemental Storm skill (3s CD)
5. **Storm's Recollection**: Remnants reappear after 3s
Minor nodes: 4x +12% Mana Regen Rate = +48% total

## Skill: Arc (6-Link)

Level 20 stats: 781–3869 Lightning Damage (including damage effectiveness), 90 mana, chains 9 times

Support gems:
1. Controlled Destruction — more spell damage
2. Arcane Surge — more spell damage after mana threshold
3. Lightning Penetration — penetration
4. Unleash — Seals for repeated casts (150% cost multiplier)
5. Zenith I — more damage above 90% ES
6. Rapid Casting I — 15% inc cast speed

## Defense (0.4.0 — OUTDATED for 0.5.x)

- 70% MoM (50% Cloak + 20% Force of Will)
- ES + Mana hybrid pool — **ES recharge values gutted in 0.5.0, replace with Ghost Dance + Evasion**
- Convalescence spirit gem (30 Spirit): instant ES recharge
- Arctic Armour spirit gem (30 Spirit): melee barrier

## Damage Estimate (calculation method still valid)

Arc base avg hit: ~2325 (from 781–3869)
- Indigon (4000 mana spent): +200–300% increased
- Passive tree (lightning/spell): +150–200% increased
- Support more multipliers: ~2.6x
- Shock: ~1.4x
**Estimated avg hit: ~42,000 lightning damage**

## Mana Sustain

- Base regen: 1.8% max mana/sec
- With +300% inc regen (0.4.0 values; runes buffed in 0.5.0): 7.2%/sec
- 5000 mana → 360 mana/sec
- Arc cost at max Indigon stacks: 180–270 mana
- Sustained: 1.3–2.0 casts/sec

## Gear Priorities

| Slot | Priority |
|------|----------|
| Helmet | Indigon (mandatory) |
| Body | Cloak of Defiance (mandatory) |
| Weapon | Wand: +lightning, cast speed, spell dmg |
| Off-hand | Focus/Shield: ES, mana, spell dmg |
| Rings | Max mana, mana regen, lightning dmg, resists |
| Amulet | +lightning gems, max mana, mana regen |
| Belt | Mana, ES, resists |
| Boots | Movespeed, mana, ES, resists — consider evasion base for Ghost Dance |
| Gloves | Cast speed, mana, ES |

## Passive Tree

Quadrants: Int (top), Int/Dex hybrid (southeast for lightning)
Key clusters: mana, mana regen, ES, lightning damage, spell damage, cast speed
Keystone: Mind Over Matter (if separate stacking source)
