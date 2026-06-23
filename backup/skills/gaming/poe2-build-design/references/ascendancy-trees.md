# PoE2 Ascendancy Trees — Complete Verified Data

Extracted from tree.json `connections` + tree.lua ascendancy definitions. Node IDs verified against POB Community PoE2 v0.21.0 release (repo `TreeData/0_5/`).

## Point Costs

- **All ascendancy nodes cost 2 points** (both small passives and notables).
- Total ascendancy points available: 8 (4 trials × 2 points each).
- **Max nodes allocatable: 4** (8 ÷ 2).
- Typical allocation: 2 notables with their connecting small passives (2+2+2+2 = 8).

---

## Invoker (Monk, ascendClassId=2, ascendancyInternalId="Monk2")

**Start node: 9994** (small, 2 pts, orbit=0, "Invoker")

### Tree Structure (BFS layers from start)

```
Layer 0: 9994 (START)
Layer 1: 23415(sm), 44357(sm), 13065(sm), 27686(sm), 25434(sm), 17268(sm)
Layer 2: 8143(★), 63713(★), 63236(★), 12876(★),  -  , 7621(★)
Layer 3: 16100(sm), 57181(sm),  -  ,  -  ,  -  , 55611(sm)
Layer 4: 65173(★), 52448(★),  -  ,  -  ,  -  , 64031(★)
```

### Notable Descriptions

| ID | Name | Path | Effect Summary |
|----|------|------|----------------|
| 7621 | I am the Thunder... | 9994→17268→7621 | 10% phys→extra Lightning, 25% Shocked Ground on Shock |
| 8143 | Lead me through Grace... | 9994→23415→8143 | Evasion+ES grants Spirit |
| 12876 | Faith is a Choice | 9994→27686→12876 | Grants Skill: Meditate |
| 23587 | I am the Blizzard... | 9994→25434→23587 | 10% phys→extra Cold, Chilled Ground on Freeze |
| 52448 | ...and Scatter Them to the Winds | 9994→44357→63713→57181→52448 | Elemental Expression on Melee Crit |
| 63236 | The Soul Springs Eternal | 9994→13065→63236 | Energy/ES recovery |
| 63713 | Sunder my Enemies... | 9994→44357→63713 | Crits ignore resists |
| 64031 | ...and I Shall Rage | 9994→17268→7621→55611→64031 | Rage/Unbound Avatar |
| 65173 | ...and Protect me from Harm | 9994→23415→8143→16100→65173 | PDR from Armour+Evasion, 35% less Evasion |

### Small Passives

| ID | Name | Connects To |
|----|------|-------------|
| 17268 | Shock Effect | 8143 |
| 23415 | Evasion and Energy Shield | 8143 |
| 27686 | Energy Shield Recharge Rate | 12876 |
| 25434 | Chill Effect | 23587 |
| 13065 | Triggered Spell Damage | 63236 |
| 44357 | Critical Chance | 63713 |
| 16100 | Evasion | 65173 |
| 55611 | Elemental Damage | 64031 |
| 57181 | Critical Chance | 52448 |
| 29133 | Elemental Damage | (leaf) |

### Optimal Auto-Bomber Allocation (8 pts)
- Branch A: 9994 → 17268(sm, 2) → 7621(★, 2) = 4 pts
- Branch B: 9994 → 23415(sm, 2) → 8143(★, 2) = 4 pts
- **Result**: 10% extra Lightning + Shocked Ground + Spirit from Evasion/ES for Herald chains.

---

## Witchhunter (Mercenary, ascendClassId=2, ascendancyInternalId="Mercenary2")

**Start node: 7120** (small, 2 pts, orbit=0, "Witchhunter")

### Tree Structure (BFS layers from start)

```
Layer 0: 7120 (START)
Layer 1: 43131(sm), 20830(sm), 61897(sm), 51737(sm), 25172(sm)
Layer 2: 61973(★), 37078(★), 38601(★), 8272(★), 3704(★)
Layer 3: 40719(sm),  -  , 34501(sm),  -  , 32559(sm)
Layer 4: 17646(★),  -  , 6935(★),  -  , 46535(★)
```

### Notable Descriptions

| ID | Name | Path | Effect Summary |
|----|------|------|----------------|
| 37078 | Zealous Inquisition | 7120→20830→37078 | 10% explode on kill, 100% max life Physical |
| 61973 | Pitiless Killer | 7120→43131→61973 | Drain monster focus, more dmg vs rare/unique |
| 46535 | No Mercy | 7120→25172→3704→32559→46535 | Up to 40% MORE vs full-life, hits ignore resists |
| 17646 | Judge, Jury, and Executioner | 7120→43131→61973→40719→17646 | Decimating Strike (5-30% life removal) |
| 3704 | Witchbane | 7120→25172→3704 | Break Concentration on Hit |
| 38601 | Obsessive Rituals | 7120→61897→38601 | Ritual/enchant boost |
| 6935 | Ceremonial Ablution | 7120→61897→38601→34501→6935 | Flask/cleanse effect |
| 8272 | Weapon Master | 7120→51737→8272 | Weapon swap mastery |

### Small Passives

| ID | Name | Connects To |
|----|------|-------------|
| 20830 | Area of Effect | 37078 |
| 43131 | Damage vs Low Life Enemies | 61973 |
| 25172 | Cooldown Recovery Rate | 3704 |
| 51737 | Cooldown Recovery Rate | 8272 |
| 61897 | Armour and Evasion | 38601 |
| 34501 | Armour and Evasion | 6935 |
| 32559 | Cooldown Recovery Rate | 46535 |
| 40719 | Damage vs Low Life Enemies | 17646 |

### Optimal Auto-Bomber Allocation (8 pts)
- Branch A: 7120 → 20830(sm, 2) → 37078(★, 2) = 4 pts
- Branch B: 7120 → 43131(sm, 2) → 61973(★, 2) = 4 pts
- **Result**: Explode on kill (Zealous) + boss damage (Pitiless). Eonyr's Thunder stacks with Zealous for double-detonation.

**Alternative**: Swap Pitiless for No Mercy (better bossing, worse pathing). No Mercy path: 7120→25172→3704→32559→46535 = 10 pts (5 nodes) — **cannot fit within 8 pts without dropping Zealous.** Not recommended; Zealous is non-negotiable for auto-bomber.

---

## Martial Artist (Monk, ascendClassId=1, ascendancyInternalId="Monk1")

**Start node identified but tree structure not fully mapped in this session.** Verified from poe.ninja working build that Martial Artist uses these ascendancy nodes: 11495, 51546, 52295, 19370, 20437, 39552, 39595, 34081, 37604 (9 total — includes small passives and notables).

### Known Notables (from tree.lua, names confirmed)

| ID | Name | Icon | Effect (from poe2db.tw) |
|----|------|------|--------------------------|
| ? | Martial Master | ? | Combo retained across weapons, gain Combo from ALL Attack Hits |
| ? | Martial Adept | ? | +1 Combo on gain, -0.2s ES recharge per Combo spent |
| ? | Way of the Mountain | ? | On Immobilising: gain Mountain's Teaching. 15% MORE dmg, 40% less from small hits |
| ? | Runic Meridians | ? | 5 extra Rune sockets (Helm, 2×Body, Gloves, Boots) |
| ? | Hollow Form Technique | ? | Grants skill: Hollow Form |
| ? | Hollow Resonance Technique | ? | Grants skill, 0.5s CD, 60-178% base (lv1-20) |
| ? | Hollow Focus Technique | ? | CDR applies to bell frequency, 90-230% base (lv1-20) |
| ? | Way of the Stonefist | ? | Gloves→Fists of Stone, transformed affixes |

**Note**: Node ID mapping incomplete. Need user export with Martial Artist ascendancy to confirm. IDs above are from poe.ninja POB code but not individually named.

---

## URL-Safe Base64 Encoding (POB Codes)

POB import codes from poe.ninja use **URL-safe base64**: `-` replaces `+`, `_` replaces `/`, `=` padding stripped.

**Decode:**
```python
b64_std = code.replace('-', '+').replace('_', '/')
padding = 4 - len(b64_std) % 4
if padding != 4:
    b64_std += '=' * padding
raw = base64.b64decode(b64_std)
xml = zlib.decompress(raw)  # wbits=0 (default)
```

**Encode:**
```python
b64 = base64.b64encode(zlib.compress(xml.encode(), 9)).decode()
code = b64.replace('+', '-').replace('/', '_').rstrip('=')
```
