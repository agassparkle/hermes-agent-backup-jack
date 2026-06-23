# Auto-Bomber Mechanics — Complete Reference

## Living Lightning Swarm (NEW — discovered 2026-06-22)

### Core Support Gem
`SupportLivingLightningPlayer` / `SupportLivingLightningPlayerTwo` (sup_int.lua)
- **Tier 1**: 0.2s CD, 5 stored uses. Creates Living Lightning minion when dealing lightning damage with attacks.
- **Tier 2**: 0.2s CD, 8 stored uses. Same mechanic, higher burst capacity.
- Requirements: Attack + Damage (any weapon type, not Crossbow-restricted)
- gemFamily: `"LivingLightning"` — unique category, no conflicts with any other support

### Minion Stats (from Minions.lua, line 694)
```
damage = 0.35          → 35% of weapon base damage per Zap
attackTime = 1.0       → Base attack time (overridden by Zap skill)
attackRange = 20       → Long range
critChance = 5         → 5% base crit
baseMovementSpeed = 97 → Very fast
limit = "ActiveLivingLightningLimit"
```

Minion is UNDAMAGEABLE (`DamageTaken MORE -100`), immune to stun/knockback/curses, phases through objects, untargetable by monsters. Cannot die — only expires by duration.

### Zap Skill (from minion.lua)
`LivingLightningZap` — the minion's auto-attack:
- 0.25s cooldown, 1 stored use per minion
- 9% crit chance
- Teleports to target, chains lightning (melee attack with Chain tag)
- **MORE damage per additional hit** — key scaling mechanic:
  - statMap: `living_lightning_damage_+%_final_per_additional_hit`
  - div=3/2 means MORE is averaged over 3 hits
  - After 3 hits: effective ~30% MORE (if per-hit=20%), cumulative MORE over more hits

### Sustain Calculation
- Typical APS: Tempest Flurry 1.96 APS × 1.5 hits/attack = 2.94 hits/sec → ~3 spawns/sec
- Spawn rate: capped by 0.2s CD = 5/sec max. Hit rate is below cap.
- Minion limit: Unknown (ActiveLivingLightningLimit). Estimated 10-15 base.
- With 3 spawns/sec and 8s duration: 24 minions generated, capped at min(limit, 24)
- At 15 active: 15 × 4 zaps/sec × 0.35 weapon damage = 21× weapon DPS from minions alone
- Each zap chains (hits multiple enemies) — real DPS much higher

### Optimal Delivery Skills
- **Tempest Flurry** (Quarterstaff, 140% AS, 4-hit combo, Lightning tag) — BEST
- **Charged Staff** (buff: adds flat lightning + shockwave to all QS attacks) — compound enabler
- Any fast-hitting lightning attack qualifies. Key: deal lightning damage per hit to trigger support.

### Synergies
- **Herald of Thunder** (30 Spirit): Shocked-kill bolts add AoE cleanup
- **Herald of Ice** (30 Spirit): Shatter explosions from minion cold damage (needs flat cold from gear)
- **Charged Staff**: Consume Power Charges → all attacks gain lightning → guarantees LL trigger
- **Killing Palm**: Cull + Power Charge generation → fuel Charged Staff

---

## Crossbow Quintuple Auto-Bomber — Pandemonium Engine (NEW — discovered 2026-06-22)

### The Discovery
Five distinct support categories can stack on ONE Crossbow Ammo skill. All verified different `gemFamily` fields from Lua files. No conflicts.

### Verified Support Categories

| Support | gemFamily | File | Effect |
|:---|:---|:---|:---|
| **Eonyr's Thunder** | Electrocute | sup_dex.lua | Lightning→Electrocute, slain Electrocuted enemies trigger Voltaic Fulmination |
| **Fiery Death** | FieryDeath | sup_int.lua | 60% chance: ignited enemies explode on death (10% corpse life fire) |
| **Shock Conduction** | ShockConduction | sup_int.lua | 50% chance shock spreads to nearby (2.5m radius) |
| **Coursing Current** | DeadlyCurrent | sup_int.lua | 0.2s CD, 6 stored: chain lightning to Drenched on shock |
| **Lightning Penetration** | LightningPenetration | sup_dex.lua | 30% lightning penetration |

All require `CrossbowAmmoSkill` type. All different categories → all can fit on one 6L.

### Additional Mechanics (non-ammo support slots)

| Support | gemFamily | File | Slot |
|:---|:---|:---|:---|
| **Static Shocks** | GroundingShocks | sup_int.lua | Firing skill (CrossbowSkill, not Ammo) |
| **Zealous Inquisition** | Ascendancy | tree.json:37078 | Passive — 10% chance 100% max life Phys explode (20% vs Undead) |
| **Culling Strike** | Ascendancy | tree.json:61973 | Passive — guaranteed first kill |
| **Decimating Strike** | Ascendancy | tree.json:17646 | Passive — first hit removes 5-30% life |
| **No Mercy** | Ascendancy | tree.json:46535 | Passive — up to 40% MORE vs broken Concentration |

**7 total chain/explosion mechanics** per attack. Zero mana (Galvanic Shards costs 0).

### The Chain
1. Galvanic Shards (7 proj, chains lightning, 0 mana) → Electrocute + Ignite + Shock full screen
2. Culling Strike kills first enemy
3. **Triple explosion**: Eonyr (Lightning) + Fiery Death (Fire, 10% corpse life) + Zealous (Physical, 100% max life)
4. Shock Conduction spreads shocks 2.5m → more Electrocuted+Ignited enemies
5. Coursing Current chains lightning through Drenched survivors
6. Static Shocks turns shocked enemies into lightning pulse beacons
7. More enemies die → triple explosion → infinite chain

### Key Build Details
- **Class**: Mercenary → Witchhunter (Mercenary2)
- **Spirit**: 30 (Herald of Thunder only — chain carries itself)
- **Ammo type**: Bombard Crossbow (correct API type name)
- **6L Ammo**: Galvanic Shards + Eonyr + Fiery Death + Shock Conduction + Coursing Current + Lightning Pen
- **2L Firing**: Galvanic Shards (Fire) + Static Shocks
- **Boss swap**: Shockburst Rounds for single target

---

## Herald Chains (verified)

### Triple Herald (HoT + HoI + HoA — 90 Spirit)
```
Herald of Thunder (30) + Herald of Ice (30) + Herald of Ash (30)
  Kill shocked → HoT lightning bolt
  HoT bolt shatters frozen → HoI cold explosion
  HoI explosion shocks → HoT again
  Overkill damage → HoA ignite spread → more kills
```

Requires lightning + cold + fire damage on same skill. Invoker ascendancy (10% extra cold + lightning, Shocked/Chilled Ground) provides consistency without gear.

### Existing Builds (verified POB codes)

**Storm Cascade** (Invoker Triple Herald): Storm Wave + HoT/HoI/HoA + 90 Spirit. POB code at `/home/ubuntu/storm-cascade-build.pob`

**Voltaic Fulmination** (Witchhunter Double Detonate): Galvanic Shards + Eonyr's Thunder + Zealous Inquisition. POB code at `/home/ubuntu/voltaic-fulmination-build.pob`

**Living Storm** (Invoker Living Lightning Swarm): Tempest Flurry + Living Lightning II + Charged Staff + HoT/HoI. POB code at `/home/ubuntu/living-storm-build.pob`

**Pandemonium Engine** (Witchhunter 7-Mechanic): Galvanic Shards + 5 supports + Static Shocks + Zealous + Culling. POB code at `/home/ubuntu/pandemonium-engine-build.pob`

---

## Other Trigger/Explosion Mechanics (verified from Lua)

### Fiery Death
- gemFamily: `"FieryDeath"`, Crossbow Ammo only
- 60% chance on ignited enemy death → 10% corpse life as fire explosion (2m radius)
- 15% less damage with supported skills (cost multiplier)

### Coursing Current (Deadly Current)
- gemFamily: `"DeadlyCurrent"`, Crossbow Ammo only
- 0.2s CD, 6 stored uses
- Shocking an enemy → chains lightning to Drenched enemies
- 10% crit, Lightning Spell type

### Shock Conduction
- gemFamily: `"ShockConduction"`, Crossbow Ammo only
- 50% chance to shock nearby enemies (2.5m) when you shock
- Tier II: Always shocks Drenched enemies (Legacy)

### Static Shocks
- gemFamily: `"GroundingShocks"`, CrossbowSkill (firing skill, not Ammo)
- Shocking an enemy → that enemy becomes lightning pulse source → pulses damage nearby

### Catalyzing Discharge
- Triggered by Elemental Ground Surface boost → matching element discharge
- 1s cooldown, spell, area

### Elemental Discharge
- Consume Freeze/Ignite/Shock on hit → trigger explosion matching consumed ailment type
- Damage scales with Intelligence (% of Int as base damage per ailment)
- 1s CD, 10% crit

### Corrupting Cry
- Warcries trigger Corrupted Blood (Physical DoT) on enemies
- Spreads on death

### Profane Ritual
- Corpse → Chaos DoT area → generates Power Charge
- Triggerable (can be socketed in Cast on X gems)

---

## Ascendancy Auto-Bomber Synergies

### Invoker (Monk)
| Node | ID | Effect |
|:---|:---|:---|
| I am the Thunder | 7621 | 10% extra lightning + 25% Shocked Ground on Shock |
| I am the Blizzard | 23587 | 10% extra cold + Chilled Ground on Freeze |
| Scatter Them to the Winds | 52448 | Trigger Elemental Expression on Melee Crit |
| Protect Me from Harm | 65173 | Armour+Evasion hybrid PDR |

### Witchhunter (Mercenary)
| Node | ID | Effect |
|:---|:---|:---|
| Zealous Inquisition | 37078 | 10% chance: 100% max life Physical explode (20% vs Undead) |
| Judge, Jury, Executioner | 17646 | Decimating Strike (first hit removes 5-30% life) |
| Pitiless Killer | 61973 | Culling Strike |
| Witchbane | 3704 | Break Concentration on Hit |
| No Mercy | 46535 | Up to 40% MORE vs broken Concentration |
| Cull the Hordes | 36341 | 40% increased Cull threshold vs Rare/Unique |
