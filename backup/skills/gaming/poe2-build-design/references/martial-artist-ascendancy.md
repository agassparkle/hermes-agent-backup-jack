# Martial Artist Ascendancy (Monk) — 0.5.0

Source: poe2db.tw (wiki does NOT have this data yet as of June 2026).

## Notable Passives

### Way of the Mountain
- **Trigger**: 100% chance per enemy Power to gain Mountain's Teachings on Immobilising an enemy
- **Max stacks**: 30
- **Lose 1 stack**: When you are Hit, or when you use/Sustain an Attack that benefits from Mountain's Teachings
- **Lose all stacks**: After 8 seconds without gaining any
- **While active** (any amount of teachings):
  - Attacks you use and Attacks granted by this Ascendancy deal **15% more damage**
  - Enemy hits ≤30% of your max life (after Armour/Resists, before other damage modifiers) deal **40% less damage**
  - **50% more Stun Threshold**

### Martial Adept
- When you gain Combo, gain an additional Combo (+1 per Combo gain event)
- -0.2 seconds to current Energy Shield Recharge delay per Combo expended when using skills

### Martial Master
- Skills can build and retain Combo regardless of Weapon Set
- **Gain Combo from ALL Attack Hits** (extends Combo generation to skills that normally don't generate Combo)

### Runic Meridians
- Can tattoo Runes onto your body, gaining additional Rune-only sockets:
  - 1 Helmet socket
  - 2 Body Armour sockets
  - 1 Gloves socket
  - 1 Boots socket

### Way of the Stonefist
- Gloves you equip have their Base Type transformed to Fists of Stone while equipped
- Prefixes and Suffixes are transformed into more powerful related Modifiers
- This enables UNARMED combat with the gloves as weapons

### Hollow Form Technique
- Grants Skill: Hollow Form
- (Full mechanics unknown — poe2db has scaling data at 100% across all levels)

### Hollow Resonance Technique
- Grants Skill: Hollow Resonance
- Cooldown: 500ms (0.5 seconds)
- Damage scaling: 60% → 178% base (levels 1-20)
- Active attack skill with very short cooldown

### Hollow Focus Technique
- Grants Skill: Hollow Focus
- "Modifiers to Cooldown Recovery Rate also apply to bell appearance frequency"
- Damage scaling: 90% → 230% base (levels 1-20)
- Buffs Tempest Bell generation rate via CDR

## Hidden Skill: Crackling Palm
- Source: poe2db.tw skill database
- "When you Hit with Unarmed Melee Attacks, calls down lightning bolts which deal Unarmed Attack damage to all surrounding enemies."
- Synergizes with Way of the Stonefist (unarmed) but NOT with Quarterstaff attacks like Flicker Strike

## Combo Mechanics Impact

Baseline Combo generation: only from skills with explicit "Build Combo" text (e.g., Tempest Bell says "Build Combo by successfully Striking Enemies with other skills").

With **Martial Master**: ALL attack hits generate Combo, not just designated skills. This means:
- Flicker Strike (13 hits at 6 charges) → 13 Combo from hits
- With **Martial Adept** (+1 per gain) → 26 Combo total
- Tempest Bell requires 4 Combo to use
- Can drop Bell after 2-4 hits of Flicker Strike

## Rune Socket Value Analysis

5 sockets with max-tier runes (0.5.0 buffed values):

| Rune Type | Per Socket | ×5 Total | Effect |
|-----------|-----------|----------|--------|
| Adept Rune | +12 Dex | **+60 Dexterity** | Attribute requirements, evasion |
| Robust Rune | +12 Str | **+60 Strength** | Life, melee damage |
| Resolve Rune | +12 Int | **+60 Intelligence** | Mana, ES, spell support reqs |
| Rebirth Rune | 0.45% life/s | **2.25% life/sec** | Sustain |
| Inspiration Rune | +30 mana/kill | **150 mana/kill** | Mapping sustain |
| Stone Rune | 40% stun buildup | **200% stun buildup** | Stun consistency |
| Storm Rune | 18% light res | **90% lightning res** | Gearing flexibility |

Mix and match for attribute requirements, defense, or sustain as needed.
