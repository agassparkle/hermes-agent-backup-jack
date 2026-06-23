---
name: poe2-build-design
description: Design original Path of Exile 2 builds from raw data — patch notes, skill gem numbers, unique items, and synergistic interactions. Do your own math; do not rehash existing build guides. The user expects novel analysis, not compiled maxroll summaries.
---

# PoE2 Build Design

Design ORIGINAL PoE2 builds from first principles by analyzing patch notes, skill gem damage numbers, support gem multipliers, unique item stats, and ascendancy nodes. **Never compile existing maxroll/streamer builds — the user will call this out immediately.** Do your own calculations and look for undiscovered synergies.

## Trigger

User asks to design, theorycraft, or calculate a PoE2 build. Also load when the user wants to understand current meta, compare builds, or optimize their character.

## Critical Rules (user-enforced)

0. **NEVER TOUCH WHAT WORKS.** If a build imports correctly (class, ascendancy, nodes, skills all visible), do NOT change `targetVersion`, `classInternalId`, `ascendClassId`, `secondaryAscendClassId`, `treeVersion`, or the Spec/skills structure — even if the skill says these values are "wrong" for that POB version. The user's POB may accept formats the dev repo documentation says are invalid. Changing a working build's metadata to match documentation is the single biggest source of user frustration. Only change items.

## Critical Rules (user-enforced)

1. **NEVER FABRICATE. NEVER LIE.** Every number must be traceable to a source. If a value is estimated, say "Estimated" and explain how you arrived at it. If trade prices cannot be verified, say so — do not invent them. The user will catch fabricated data immediately and the trust damage is catastrophic. When the API returns nothing useful, admit it. When you don't know, say you don't know.
2. **ALWAYS check the latest patch first.** The user will correct you if you reference outdated versions. Check `Version_history` for the current major + minor patches and read ALL of them before designing.
3. **Do original math, not compilation.** Present builds with your own damage calculations, discovered synergies, and analysis. If it reads like a maxroll guide, it's wrong.
4. **Pull raw numbers.** Every damage figure, mana cost, and multiplier must come from a source you fetched — never estimate from memory.
5. **OKU KUR — don't ask, just work.** Do not ask "which direction?" or "which build should I prioritize?" or "should I continue?" — the user has told you to work continuously, exhaustively, until you find something spectacular. Asking for steering when you could be calculating is laziness. Execute all reasonable permutations before presenting. Five hours of AI iteration should produce deep results, not half-finished research.

## Data Sources (authoritative)

### PRIMARY (numerical truth): Path of Building Community Lua files
The PoE2 PoB fork is the **authoritative source** for exact skill damage, support gem multipliers, mana costs, and quality effects. It contains the actual game data, not wiki approximations.

**Download (for the user):** https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2/releases/latest
Latest release: v0.21.0. Portable zip + Setup exe available.

**Clone (for data extraction):**
```bash
git clone --depth 1 https://github.com/PathOfBuildingCommunity/PathOfBuilding-PoE2.git
```
**This is the OFFICIAL PoE2 Path of Building repo.**

**Repository tree data vs release POB:** Node IDs in the repo `TreeData/0_5/tree.json` match release POB v0.21.0. Verified by exporting a user-generated Witchhunter build with 34 allocated nodes — ALL 27 regular node IDs matched. Repo tree data is authoritative for node IDs and connectivity.

**poe.ninja tree data (4539 nodes) — CONFIRMED MATCHING REPO:**
Downloadable from poe.ninja's JS bundle. Node IDs are identical to the repo tree. Useful as a cross-reference or when the repo isn't cloned:
```python
import cloudscraper, json, re
s = cloudscraper.create_scraper()
r = s.get('https://assets.poe.ninja/_astro/a.Cr9DCTHT.mjs', timeout=30)
# Extract first JSON.parse(`{...}`) block
brace_start = r.text.find('{', r.text.find('JSON.parse(`'))
depth, i = 0, brace_start
while i < len(r.text) and (depth > 0 or i == brace_start):
    if r.text[i] == '{': depth += 1
    elif r.text[i] == '}': depth -= 1
    i += 1
tree = json.loads(r.text[brace_start:i])
# tree['7621'] = { "name": "I am the Thunder...", "ascendancyName": "Invoker", ... }
```

**Cloudscraper (Cloudflare bypass) — VERIFIED WORKING:**
```bash
pip3 install cloudscraper
```
Successfully bypasses Cloudflare on poe.ninja, maxroll.gg, mobalytics.gg. Use for any HTTP request to these sites:
```python
import cloudscraper
scraper = cloudscraper.create_scraper()
resp = scraper.get('https://poe.ninja/poe2/builds', timeout=30)
```
For JS-rendered content (POB codes are loaded via XHR after page load), Puppeteer-core is also available with system Chromium:
```bash
npm install puppeteer-core
# Use: executablePath: '/usr/bin/chromium-browser', headless: 'new',
#       args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
```
**poe.ninja API caveat**: build data uses protobuf (`application/x-protobuf`), not JSON. POB codes are in HTML <script> tags loaded dynamically. Base64 codes in chat paste get corrupted — use XML file exports instead.

**File structure:**
| File | Content |
|------|---------|
| `src/Data/Skills/act_int.lua` | Active skill gems (Intelligence) — Flicker Strike, Siphoning Strike, Killing Palm, Storm Wave, etc. |
| `src/Data/Skills/act_dex.lua` | Active skill gems (Dexterity) |
| `src/Data/Skills/act_str.lua` | Active skill gems (Strength) |
| `src/Data/Skills/sup_int.lua` | Support gems (Intelligence) — Elemental Focus, Concentrated Area, etc. |
| `src/Data/Skills/sup_dex.lua` | Support gems (Dexterity) — Close Combat I/II, Lightning Penetration, Momentum |
| `src/Data/Skills/sup_str.lua` | Support gems (Strength) — Heft, Elemental Armament I/II, Bloodlust |

**How to extract data from Lua files:**
- Skill base damage: `baseMultiplier` (e.g., 3.27 at lv20 = 327%)
- Attack speed: `attackSpeedMultiplier` (e.g., -50 = 50% of base AS)
- Mana cost: `cost = { Mana = 85 }` in level array
- Support more%: `constantStats` array → `{ "stat_name", value }` (e.g., `{ "support_close_combat_attack_damage_+%_final", 30 }` = 30% MORE)
- Support cost multiplier: `manaMultiplier` (e.g., 20 = 120% cost)
- Quality effects: `qualityStats` array per skill
- Special mechanics: `stats` array (e.g., `"cannot_gain_power_charges_during_skill"`)
- Charge interactions: `constantStats` → `{ "flicker_strike_additional_flickers_from_power_charges", 2 }` = 2 extra strikes per Power Charge

**Critical pitfall with Momentum:** The Momentum support says *"Teleportation does not count towards the distance travelled."* Flicker Strike teleports → Momentum NEVER activates. Confirmed from `sup_dex.lua` stat description.

### SECONDARY (mechanics + patch context)

| Source | URL | Content |
|--------|-----|---------|
| Version history | `/wiki/Version_history` | Find current major + minor versions |
| Patch notes | `/wiki/Version_X.Y.Z` | Balance changes, buffs/nerfs, mechanic reworks |
| PoE2 Wiki (HTML) | `/wiki/<Page>` | Rich tooltips but JS-rendered — use API endpoint |
| Wiki API (parse) | `/api.php?action=parse&page=<Page>&prop=text&format=json` | Machine-readable item stats, ascendancy nodes |
| Skill gem list | `/wiki/List_of_skill_gems` | All active skill gems. **Numbers from wiki may differ from PoB — PoB is authoritative.** |
| Support gem list | `/wiki/List_of_support_gems` | All support gems (1.3MB+ — stream, don't full-load). Use PoB Lua files for exact multipliers. |
| Spirit gem list | `/wiki/List_of_spirit_gems` | Persistent buffs, auras, triggers |
| Meta gem list | `/wiki/List_of_meta_gems` | Cast on Crit, Cast on Freeze, etc. |
| Maxroll builds | `https://maxroll.gg/poe2/build-guides` | Meta awareness ONLY — do NOT copy/rehash |
| **poe2db.tw** | `https://poe2db.tw/us/<Page>` | Ascendancy nodes, skill details, passive tree data when wiki is WIP. Use for new 0.5.0 content (Martial Artist, Spirit Walker) not yet on wiki. **JS-rendered — don't try to scrape raw HTML; use targeted grep on data attributes.** |
| Individual ascendancies | `https://poe2db.tw/us/<Ascendancy_Name>` | Full node details, hover data, related skills. |
| Passive tree | `/wiki/Passive_Skill_Tree` | Tree mechanics, point totals, node types |
| Character classes | `/wiki/Character_class` | Classes + ascendancies table |
| Individual items | `/wiki/<Item_Name>` | Unique item stats (API endpoint) |
| Cargo tables | `/wiki/Special:CargoTables/skill_gems` | Structured gem data (fallback) |

## Research Methodology

### Step 1: Determine the current version FIRST
Go to `Version_history` and identify the latest major patch (e.g., 0.5.0) and ALL subsequent minor patches (0.5.1, 0.5.2, 0.5.3). Download EVERY patch note. The user will correct you if you miss one.

### Step 2: Extract the meta shifts from patch notes
From each patch note, extract:
- **Skill nerfs/buffs**: numerical changes with old→new values
- **Unique item changes**: especially items with large numerical swings
- **Mechanic reworks**: Ghost Dance rework, defense formula changes, new ascendancies
- **New systems**: new ascendancy classes, rune changes, atlas tree overhauls
- Scan for these keywords in `<li>` tags: `now has`, `now deals`, `now grants`, `previously`, `increased from`, `decreased from`, `reworked`, `no longer`

### Step 3: Pull raw skill gem numbers
From `/wiki/List_of_skill_gems`, extract for every relevant skill:
- Tier, Level range, Cost (mana/life), Attack/Cast Speed
- Damage: % of base (attacks) or flat min–max (spells)
- Tags (AoE, Projectile, Melee, Spell, Lightning, etc.)
- **Mechanics**: Consumes X charges, grants Y charges, interacts with Z ground effect, detonates, chains, etc.
- **Infusion effects**: Many skills have alternate behavior when consuming Elemental Infusions

### Step 4: Find undiscovered synergies
Look for skill pairs where:
- **Skill A generates Resource X** (charges, ground effects, debuffs, corpses)
- **Skill B consumes Resource X** for amplified damage or new effects
- **Skill C applies Debuff Y** that multiplies both
Examples found to date: Killing Palm (generates Power Charges) → Falling Thunder (consumes for projectiles); Volcano (sprays on Slam) → Shockwave Totem (repeated Slams).

### Step 5: Pull support gem multipliers
From the support gem list, extract: Category, Cost multiplier (e.g., 120%), "more/less/increased" modifiers with exact percentages. Key search terms: `more Damage`, `consume.*charge`, `Penetration`.

### Step 6: Calculate the damage chain
Use real numbers:
```
Hit = base_damage × (1 + sum(increased_mods)) × product(more_multipliers) × (1 + damage_taken_mods)
```
Account for: passive tree (~150-250% inc), gear affixes, support gem more multipliers (exact %), curses/exposure, shock (50% inc damage taken), charge consumption bonuses.

### Step 7: Validate the build loop
- **Sustain**: Can mana/life costs be recovered? Check regen, leech, on-kill effects, flask charges.
- **Charge cycling**: Can charges be generated as fast as they're consumed?
- **Cooldowns**: Does the rotation fit within cooldown windows?

### Step 8: Save to Obsidian Vault

After presenting a build, persist all research to the vault at `~/jack-vault/`:

| Content Type | Vault Folder |
|:---|:---|
| Active build project | `Projects/poe2-<build-name>.md` |
| Raw verified numbers | `Resources/poe2-verified-game-data.md` |
| Synthesized mechanics | `Wiki/poe2-<topic>.md` |

**Always update `index.md` files** in each modified folder with wikilinks. Use `[[Note Name]]` syntax. See `obsidian` skill for full vault conventions.

### Step 9: Present the build
Output: Class → Ascendancy, skill gem links (6L with named supports), spirit gem reservations, passive tree direction, key uniques + rare item priorities per slot, defense layers, damage estimate with shown math.

## Parsing Wiki Data

### For skill gems (API parse endpoint — REQUIRED)
**The raw HTML page does NOT contain skill data.** Wiki uses Cargo tables loaded via JavaScript. MUST use the API parse endpoint:
```bash
curl -sL -o /tmp/skills.json \
  "https://www.poe2wiki.net/api.php?action=parse&page=List_of_skill_gems&prop=text&format=json"
```
Then parse with Python:
```python
import json, re
with open('/tmp/skills.json') as f:
    text = json.load(f)['parse']['text']['*']
rows = re.findall(r'<tr>(.*?)</tr>', text, re.DOTALL)
for row in rows:
    tds = re.findall(r'<td[^>]*>(.*?)</td>', row, re.DOTALL)
    clean = [re.sub(r'<[^>]*>', '', td).strip() for td in tds]
    # clean[0] = skill name, clean[X] = tier/level/cost/speed/damage/mechanics
```
Each `<tr>` contains: Skill Name | Tier | Level Range | Cost | Attack/Cast Speed | Damage % | Mechanics (free text with interaction details) | Quality bonus.

### For item stats (API endpoint)
```bash
curl -sL -o /tmp/item.json "https://www.poe2wiki.net/api.php?action=parse&page=<ItemName>&prop=text&format=json"
python3 -c "
import json, re
with open('/tmp/item.json') as f:
    text = json.load(f)['parse']['text']['*']
for m in re.findall(r'class=\"group tc -mod\">(.*?)</span>', text):
    print(re.sub(r'<[^>]*>', '', m).strip())
"
```

### For patch note changes
```bash
grep -oP '<li>[^<]{30,500}</li>' /tmp/v050.html | grep -iE '<keyword>'
```
Use targeted keyword searches: `skill gem|unique.*:|now deals|now has|now grants|previously|increased from|decreased from|reworked|no longer|buff|nerf`

### For ascendancy nodes
Use the API parse endpoint on the ascendancy page. Nodes appear in hoverbox containers or in version history `<li>` items. New ascendancies (0.5.0 Martial Artist, Spirit Walker) may not have full wiki data yet — acknowledge gaps.

## New Ascendancies (0.5.0)

### Martial Artist (Monk) — full data from poe2db.tw
**Notable Passives:**
| Node | Effect |
|------|--------|
| **Way of the Mountain** | On Immobilising: gain 1 Mountain's Teaching (max 30). While ≥1 active: Attacks deal **15% more damage**, hits ≤30% max life deal **40% less damage**, **50% more Stun Threshold**. Lose 1 on attack/hit. All lost after 8s idle. |
| **Martial Adept** | +1 Combo on gain. -0.2s ES recharge delay per Combo expended when using skills |
| **Martial Master** | Combo retained across weapon sets. **Gain Combo from ALL Attack Hits** (not just skills that normally generate Combo) |
| **Runic Meridians** | 5 extra Rune sockets: 1 Helm, 2 Body Armour, 1 Gloves, 1 Boots. Each can hold any rune. |
| **Way of the Stonefist** | Gloves → Fists of Stone (unarmed base type). Prefixes/Suffixes transformed into stronger related modifiers. |
| **Hollow Form Technique** | Grants skill: Hollow Form (details still unknown — could not extract full description from wiki or poe2db) |
| **Hollow Resonance Technique** | Grants skill — **0.5s cooldown**, **60%→178% base damage** (lv 1-20). Active attack skill. Tags unknown. |
| **Hollow Focus Technique** | Grants skill — **"Modifiers to Cooldown Recovery Rate also apply to bell appearance frequency"**, **90%→230% base damage** (lv 1-20). Synergizes with Tempest Bell. |

**Key synergies with Flicker Strike:**
- Martial Master: Flicker's 13 hits at 6 charges = 13 Combo generated. With Martial Adept = 26 Combo. Tempest Bell needs only 4 → drop Bell mid-Flicker, can drop 6+ Bells from one Flicker cast.
- Way of the Mountain: 15% more damage stacks multiplicatively with support gems. 40% less damage from small hits mitigates Flicker's vulnerability window.
- Runic Meridians: 5 runes = massive free stats. Example: 5×Adept Runes (+12 Dex) = +60 Dexterity. Or 5×Rebirth = 2.25% life/s.
- Mountain's Teachings lost per attack — unclear if Flicker's 13 hits count as 1 use or 13 uses. Assume worst case: each hit costs 1 teaching. Generate new teachings by Immobilising between Flickers.

### Hidden skill: Crackling Palm
Found on poe2db: *"When you Hit with Unarmed Melee Attacks, calls down lightning bolts dealing Unarmed Attack damage to all surrounding enemies."* Synergizes with Way of the Stonefist but NOT with Quarterstaff skills (Flicker requires staff → different build archetype).

### Invoker (Monk) — FULL TREE verified from tree.json BFS + tree.lua names

All node IDs confirmed from tree.json `connections` and tree.lua ascendancy definitions. Paths verified with BFS from start node 9994.

**Ascendancy notables (8 total, isNotable=true, 2 pts each):**

| Node ID | Name | Icon | Path from start | Effect |
|---------|------|------|-----------------|--------|
| **7621** | I am the Thunder... | InvokerShockMagnitude | 9994→17268→7621 | 10% phys as extra Lightning, 25% chance Shocked Ground on Shock |
| **8143** | Lead me through Grace... | InvokerEvasionEnergyShieldGrantsSpirit | 9994→23415→8143 | Evasion+ES grants Spirit (defense→offense) |
| **12876** | Faith is a Choice | InvokerGrantsMeditate | 9994→27686→12876 | Grants Skill: Meditate |
| **23587** | I am the Blizzard... | InvokerChillChanceBasedOnDamage | 9994→25434→23587 | 10% phys as extra Cold, Chilled Ground on Freeze |
| **52448** | ...and Scatter Them to the Winds | InvokerWildStrike | 9994→44357→63713→57181→52448 | Trigger Elemental Expression on Melee Crit |
| **63236** | The Soul Springs Eternal | InvokerEnergyDoubled | 9994→13065→63236 | Energy/ES recovery |
| **63713** | Sunder my Enemies... | InvokerCriticalStrikesIgnoreResistances | 9994→44357→63713 | Crits ignore resists |
| **64031** | ...and I Shall Rage | InvokerUnboundAvatar | 9994→17268→7621→55611→64031 | Rage/Unbound Avatar mechanic |
| **65173** | ...and Protect me from Harm | InvokerEvasionGrantsPhysicalDamageReduction | 9994→23415→8143→16100→65173 | PDR from Armour+Evasion, 35% less Evasion |

**Small ascendancy passives (1 pt each, isNotable=false):**
17268 (Shock Effect), 23415 (Evasion+ES), 27686 (ES Recharge), 25434 (Chill Effect), 13065 (Triggered Spell Damage), 44357 (Critical Chance), 16100 (Evasion), 55611 (Elemental Damage), 57181 (Critical Chance), 29133 (Elemental Damage)

**Auto-bomber priority (8 pts = 4 nodes):**
- **Thunder path**: 9994→17268(2)→7621(2) = 4 pts. Gets 10% extra Lightning + Shocked Ground.
- **Grace path**: 9994→23415(2)→8143(2) = 4 pts. Gets Spirit from Evasion+ES for more heralds.
- **Together**: 8 pts. Enables HoT+HoI+HoA (90 Spirit) with 10% extra Lightning + Shocked/Chilled Ground.

### Witchhunter (Mercenary) — FULL TREE verified from tree.json BFS + tree.lua names

All node IDs confirmed from tree.json `connections` and tree.lua ascendancy definitions. Paths verified with BFS from start node 7120.

**Ascendancy notables (8 total, isNotable=true, 2 pts each):**

| Node ID | Name | Icon | Path from start | Effect |
|---------|------|------|-----------------|--------|
| **37078** | Zealous Inquisition | WitchunterMonsterHolyExplosion | 7120→20830→37078 | **10% chance explode, 100% max life Physical** (20% vs Undead/Demons) |
| **61973** | Pitiless Killer | WitchunterDrainMonsterFocus | 7120→43131→61973 | Drain monster focus, more damage vs rare/unique |
| **46535** | No Mercy | WitchunterRemovePercentageFullLifeEnemies | 7120→25172→3704→32559→46535 | Up to 40% MORE Damage vs full-life, hits ignore resists |
| **17646** | Judge, Jury, and Executioner | (orbit 0) | 7120→43131→61973→40719→17646 | Decimating Strike (5-30% life removal on first hit) |
| **3704** | Witchbane | (orbit 0) | 7120→25172→3704 | Break Concentration on Hit |
| **38601** | Obsessive Rituals | (orbit 0) | 7120→61897→38601 | Ritual/enchant effect |
| **6935** | Ceremonial Ablution | (orbit 0) | 7120→61897→38601→34501→6935 | Flask/cleanse effect |
| **8272** | Weapon Master | (orbit 0) | 7120→51737→8272 | Weapon swap/mastery effect |

**Small ascendancy passives:**
20830 (AoE), 43131 (Dmg vs Low Life), 25172 (CDR), 32559 (CDR), 3704 (see above), 40719 (Dmg vs Low Life), 51737 (CDR), 61897 (Armour+Evasion), 34501 (Armour+Evasion)

**Auto-bomber priority (8 pts = 4 nodes):**
- **Zealous path**: 7120→20830(2)→37078(2) = 4 pts. Explode on kill (core auto-bomber).
- **Pitiless path**: 7120→43131(2)→61973(2) = 4 pts. More damage vs rares/uniques.
- **Together**: 8 pts. Triple explosion (Eonyr's + Zealous + whatever skill) with boss damage boost.

### Other Build Archetypes Discovered

**Boneshatter Shockwave Chain (Mace — Warrior/Warbringer):**
- Seismic Cry → instantly Heavy Stuns Primed enemies → Empowers next Slam
- Boneshatter (cannot stun on its own, needs setup) → triggers 780% shockwave on Heavy Stun
- Shockwave (2m radius) damages nearby → builds stun on them → they get Primed → chain continues
- 6L supports: Melee Phys 1.30×, Bloodlust 1.30×, Brutality 1.20×, Fist of War 1.40×, Heft 1.20×, Close Combat 1.30× = 4.43× total, 4,838% per cast
- Sustained clearing, no charge management needed. Lower ceiling than Flicker (14,226%) but more consistent.

**Briarpatch Hybrid (Druid — any spellcaster):**
- Briarpatch stores physical attack damage dealt as resource
- Casting any Spell releases stored damage as Thorny Ground (spell damage)
- Could pair with Siphoning Strike (858% combined physical) → cheap spell (Profane Ritual at 6 mana, also generates Power Charges) → dump all stored damage as AoE

**Frostflame Nova Ignite/Freeze Loop:**
- Frostflame Nova latches onto Ignited enemies, refreshes Ignite duration, rapidly Freezes them
- Enables simultaneous ignite + freeze on the same target
- Any class that can cast Nova + ignite (Perfect Strike, Molten Blast)

**Triple Herald Storm Cascade (Invoker) — 90 Spirit Auto-Bomber:**
- HoT (30) + HoI (30) + HoA (30) on Storm Wave (343% base, 8m fissure, 100% MORE shock)
- Invoker ascendancy: 10% extra cold + lightning, Shocked/Chilled Ground
- Added flat cold + fire on rings/gloves → triple element coverage
- Chain: Storm Wave → shock+freeze+ignite → kill shocked (HoT bolt) → bolt shatters frozen (HoI) → overkill (HoA ignite spread) → infinite loop
- Proven POB import code generated and verified

**Voltaic Fulmination Double Detonate (Witchhunter) — First Dual Explosion Build:**
- Eonyr's Thunder (lv65 Legacy Lineage, Crossbow Ammo only) + Zealous Inquisition (100% max life Physical explode)
- Main: Galvanic Shards (7 projectiles, chains lightning, 378% total base at 20Q)
- Voltaic Fulmination: 0.3s→0.1s CD, 5 stored uses, %max life Lightning explosion
- Stack two different damage-type on-death explosions on the same kill
- Witchhunter adds Decimating Strike + Culling for faster chain start
- Proven POB import code generated and verified

**The Living Storm (Invoker) — Living Lightning Minion Swarm (NEW):**
- Tempest Flurry (140% AS, Lightning tag) + Living Lightning II (0.2s CD, 8 stored) + Charged Staff (adds flat lightning to all QS attacks)
- Living Lightning minion stats: 35% weapon damage per Zap, 0.25s CD, teleport+chain, MORE damage per additional hit, UNDAMAGEABLE
- 3 hits/sec → ~3 spawns/sec → 15+ active minions → 60+ zaps/sec → 21× weapon DPS from minions alone
- Each zap chains lightning, escalates with MORE per hit
- HoT + HoI for cleanup. Power Charges from Killing Palm → Charged Staff
- POB at `/home/ubuntu/living-storm-build.pob`

**Pandemonium Engine (Witchhunter) — 7-Mechanic Crossbow Auto-Bomber (NEW):**
- Discovered 5 distinct gemFamily categories stack on ONE Crossbow ammo skill
- Galvanic Shards (0 mana, 7 proj) + Eonyr's (Electrocute) + Fiery Death (FieryDeath, 60% ignite explode at 10% corpse life) + Shock Conduction (ShockConduction, 50% shock spread 2.5m) + Coursing Current (DeadlyCurrent, 0.2s CD chain lightning) + Lightning Penetration (LightningPenetration)
- PLUS Static Shocks (GroundingShocks) on firing skill + Zealous Inquisition (100% max life Phys explode) + Culling Strike + Decimating Strike from Witchhunter
- Triple explosion on first kill → infinite chain
- POB at `/home/ubuntu/pandemonium-engine-build.pob`

## Build Output Convention

When presenting a finished build, save to both:
1. **Build file**: `/home/ubuntu/<build-name>.md` with the sections below
2. **Obsidian vault**: `~/jack-vault/Projects/`, `Resources/`, or `Wiki/` based on content type. Update the relevant `index.md` files with wikilinks.

### POB Import Code Generation

**CRITICAL — verified through 40+ failed import attempts across multiple sessions against user's live POB Community PoE2 v0.21.0:**

**STOPPING RULE — USER-ENFORCED HARD BOUNDARY:** If two consecutive builds fail with the same symptom, **DO NOT generate a third with the same approach.** The user has explicitly said "stop spitting out the same files" — continued file generation without fixing the root cause is the fastest way to burn trust. Before generating ANY new code: (1) Verify connectivity with the script, (2) Verify the template matches a known working format, (3) Verify round-trip. If you cannot explain why THIS build will differ from the last two, do not generate it. Ask the user for a working export file instead, or switch to the template-from-working-build approach immediately.

**Most reliable method — template from a working build:** The ONLY approach that produced round-trip-verifiable correct output was:
1. Get a working POB code (from poe.ninja or user export)
2. Decompress it fully despite base64 corruption (see `references/poe-ninja-code-extraction.md`)
3. Modify the XML in-place (swap class, ascendancy, nodes, skills)
4. Re-compress with `zlib.compress(xml, 9)` + base64 → verify round-trip
5. Deliver via MEDIA

**Working poe.ninja Gem element format (verified from actual POB v0.21.0 import):**
```xml
<Gem statSetIndex="nil" enableGlobal2="true" quality="20" level="20" enableGlobal1="true" 
     variantId="TempestFlurry" skillId="TempestFlurryPlayer" corruptLevel="0" corrupted="false" 
     gemId="Metadata/Items/Gem/SkillGemTempestFlurry" nameSpec="Tempest Flurry" enabled="true" 
     count="1" statSetIndexCalcs="nil"/>
```
All attributes are REQUIRED. `statSetIndex` and `statSetIndexCalcs` are set to `"nil"` — do NOT omit them. This was discovered from a working poe.ninja Martial Artist build that successfully imported into POB v0.21.0 with 58 gems and full items.

POB import codes use **zlib compression** (NOT raw deflate). The decode path `ImportBuild()` calls `Inflate()` on the decoded buffer, but Python's `zlib.compress()` produces zlib-wrapped deflate that POB tolerates. Raw deflate (`zlib.compressobj(9, zlib.DEFLATED, -15)`) produces "Invalid input" error.

```python
import zlib, base64
xml = build_xml.encode('utf-8')
code = base64.b64encode(zlib.compress(xml, 9)).decode().replace('+', '-').replace('/', '_').rstrip('=')
# Verify round-trip
decoded = zlib.decompress(base64.b64decode(code.replace('-', '+').replace('_', '/') + '=='))
assert decoded == xml, 'Round-trip failed!'
```

**Version matching procedure (verified through trial and error):**
1. `targetVersion` on `<Build>` must match user's `liveTargetVersion` in their `GameVersions.lua`. Repo default: `"0_1"`. User's live POB: `"0_1"`.
2. `treeVersion` on `<Spec>` must match a version with tree data on user's POB. User's POB has `TreeData/0_5/` even though `liveTargetVersion="0_1"`. These are INDEPENDENT.
3. **Test first**: send 3 minimal codes (targetVersion=0_5, 0_1, none). The one that imports without "Game Version" dialog is correct.
4. **The "Convert" button is BROKEN for unsaved imports**: Clicking "Convert to 0_5" calls `Init(dbFileName, buildName, nil, true)` — with `buildXML=nil` — which tries `LoadDBFile()` and fails because the import was never saved. Dialog reappears identically. You MUST match `targetVersion` exactly on first import.
5. **Two distinct warning dialogs exist** — do NOT confuse them:
   - **"Game Version" popup** (title bar + "not supported by us"): Triggers when `targetVersion` ≠ `liveTargetVersion`. The Convert button is BROKEN for clipboard imports (see references/pob-code-corrections.md Bug 4). You MUST match `targetVersion` on first import.
   - **"Older tree version" banner** (inline bar, no popup): Triggers when `treeVersion` ≠ `latestTreeVersion` but IS a recognized version. The build IS loaded (nodes, skills, items present). Clicking Convert works here because the build has been fully loaded and saved. This is harmless.
6. **Tree node IDs are stable across versions**: Verified that ascendancy node IDs (7621, 23587, 52448, etc.) exist identically in both 0_1 and 0_5 tree data. Using nodes from one tree version against another works if both versions have the nodes.

**CRITICAL: POB XML format — use the EXACT structure from a user-exported build file.** The simplest way to get it right is to ask the user to export any working build and mirror that structure. Below is the verified format from POB Community v0.21.0 (discovered through 20+ failed import attempts across sessions):

```xml
<Spec classId="10" nodes="9994,17268,7621" ascendClassId="2" treeVersion="0_5"
      masteryEffects="" classInternalId="10" secondaryAscendClassId="nil"
      ascendancyInternalId="Monk2">
    <URL>...</URL>
    <Sockets/>
    <Overrides>
        <AttributeOverride strNodes="" dexNodes="" intNodes=""/>
    </Overrides>
</Spec>
```

**Spec element — ALL attributes required:**

| Attribute | Type | Example | Notes |
|:---|:---|:---|:---|
| `classId` | numeric string | `"10"` | OLD format. Monk=10, Mercenary=9. Include BOTH classId and classInternalId. |
| `classInternalId` | numeric string | `"10"` | NEW format. Same as integerId from tree.lua. Must be numeric — tonumber() is called. |
| `ascendClassId` | numeric string | `"2"` | **ASCENDANCY POSITION INDEX** (1=first ascendancy, 2=second). Invoker=2 (after Acolyte of Chayula), Witchhunter=2 (after Gemling Legionnaire). This was the single biggest import failure bug — using ascendClassId="1" for Invoker silently failed to load any nodes. |
| `ascendancyInternalId` | string | `"Monk2"` | NEW format string ID. Invoker="Monk2", Witchhunter="Mercenary2". |
| `secondaryAscendClassId` | string | `"nil"` | **MUST be literal "nil"** (not "0"). POB v0.21.0 saves this as the string "nil". |
| `treeVersion` | string | `"0_5"` | Must match user's POB tree data dir. |
| `nodes` | comma-sep IDs | `"9994,17268,7621"` | **NOT SpecNode children** — those are silently ignored. |
| `masteryEffects` | string | `""` | Empty string if no mastery selections. |

**Spec child elements:** `<URL>`, `<Sockets/>`, `<Overrides>` with `<AttributeOverride>` — all required even if empty to match POB save format.

**Gem elements — full format from user exports:**
```xml
<Gem nameSpec="Tempest Flurry" skillId="TempestFlurryPlayer" variantId="TempestFlurry"
     corruptLevel="0" enableGlobal1="true" enableGlobal2="true" corrupted="false"
     gemId="Metadata/Items/Gems/SkillGemTempestFlurry" count="1"
     enabled="true" quality="20" level="20"/>
```
Include `variantId` and `gemId` (Metadata/Items/Gems/... paths). The user's POB v0.21.0 includes these.

**Skill element needs source attribute for ascendancy-granted skills:**
```xml
<Skill source="Explode" label="On Kill Monster Explosion" mainActiveSkill="nil" ...>
```

**Items tab uses `<Slot>` elements, not `<Item>`:**
```xml
<ItemSet useSecondWeaponSet="nil" title="Default" id="1">
    <Slot itemId="0" name="Weapon 1" itemPbURL=""/>
    <Slot itemId="0" name="Body Armour" itemPbURL=""/>
</ItemSet>
```

**Node ID verification — repo tree.json matches release POB v0.21.0:**
Verified in-session by exporting a user-generated Witchhunter build with 34 allocated nodes — ALL 27 regular (non-ascendancy) node IDs matched between the user's POB v0.21.0 release and the repo `TreeData/0_5/tree.json`. Ascendancy notable IDs also match (37078 Zealous Inquisition, 7621 I am the Thunder, 23587 I am the Blizzard, etc.). **Repo tree.json is authoritative for node IDs.**

**CRITICAL — nodes MUST be connected:** POB silently drops unconnected nodes during `ImportFromNodeList`. A BFS from the class start node must reach every node in your `nodes` attribute. Disconnected nodes are added to `allocSubgraphNodes` (a dead-letter list) and never appear. **Always validate connectivity before generating POB codes:**

```python
# BFS from start node to verify all nodes are connected
from collections import deque
visited, q = set(), deque([start_node_id])
while q:
    nid = q.popleft()
    if nid in visited: continue
    visited.add(nid)
    for conn in tree['nodes'][str(nid)].get('connections', []):
        # Connections are DICT objects: {"id": 39383, "orbit": 0}
        neighbor = str(conn['id']) if isinstance(conn, dict) else str(conn)
        if neighbor in my_node_set and neighbor not in visited:
            q.append(neighbor)
unconnected = my_node_set - visited  # These WILL be dropped by POB
```

**Strategy when you don't have full pathing:** Use the user's EXISTING exported node set. If they allocated a working tree of 34 nodes, use all 34 — not a subset. POB handles the pathing; you just need to include every node along the path.

**Monk BFS start node: 44683** (named "SIX" in tree.json). This is the regular-tree node that connects TO the Invoker ascendancy start (9994). For any Monk build with Invoker ascendancy, BFS pathfinding should start from 44683. The equivalent for Mercenary/Witchhunter is 50986 (named "DUELIST", connects to 7120).

**CRITICAL — Connections are DICT objects:**
The `connections` field in tree.json stores `[{"id": 39383, "orbit": 0}, ...]`, NOT raw integers. When parsing:
```python
for conn in nodes[nid].get('connections', []):
    if isinstance(conn, dict):
        cid = str(conn['id'])   # ← MUST extract 'id' from dict
    else:
        cid = str(conn)
    if cid in nodes:
        adj[nid].add(cid)
```
Using `str(conn)` on a dict produces `"{'id': 39383, 'orbit': 0}"` which never matches a node key. **This silently destroys connectivity** — your BFS returns only the start node and nothing else. Always use `conn['id']` when `isinstance(conn, dict)`. Also add the REVERSE edge: `adj[cid].add(nid)` to make the graph bidirectional.

**Class numeric IDs (integerId from TreeData/<version>/tree.lua):**
| Class | integerId |
|:---|:---|
| Monk | 10 |
| Mercenary | 9 |
| Warrior | 6 |
| Ranger | 2 |
| Witch | 1 |
| Sorceress | 7 |

**Ascendancy string IDs (internalId):**
| Ascendancy | internalId | ascendClassId |
|:---|:---|---:|
| Invoker | "Monk2" | 2 |
| Martial Artist | "Monk1" | 1 |
| Acolyte of Chayula | "Monk3" | 3 |
| Witchhunter | "Mercenary2" | 2 |
| Gemling Legionnaire | "Mercenary3" | 3 |
| Tactician | "Mercenary1" | 1 |

**ascendClassId is the ascendancy's position index** (1=first, 2=second, 3=third). Martial Artist is ascendClassId="1" (Monk's first ascendancy), Invoker is ascendClassId="2" (Monk's second). Verified from poe.ninja POB code: `<Spec ascendancyInternalId="Monk1" ascendClassId="1" .../>`

**CRITICAL pitfalls (each discovered through a failed import):**
- **`<SpecNode/>` children are SILENTLY IGNORED**: `PassiveSpec:Load` never iterates `<SpecNode>` elements. Use `nodes="id1,id2,..."` attribute ONLY. All node allocations silently fail if you use SpecNode children.
- **`classInternalId` MUST be numeric**: Code does `tonumber(xml.attrib.classInternalId)`. String `"Monk"` → `nil` → triggers "missing 'classId' / 'classInternalId' attribute" error. Use integerId from tree.lua.
- **Raw deflate FAILS**: POB shows "Invalid input". Even though the decode path says `Inflate`, it handles zlib-wrapped data. Use `zlib.compress()`.
- **`targetVersion` and `treeVersion` are independent**: The "Game Version" popup checks `targetVersion` vs `liveTargetVersion`. Tree loading checks `treeVersion` vs `treeVersions` table. They can differ and both must be correct.
- Items: omit — require exact mod IDs from POB runtime.

**Skills format:**
```xml
<Skills activeSkillSet="1" defaultGemLevel="20" defaultGemQuality="20" sortGemsByDPS="true">
    <SkillSet id="1" title="Skills">
        <Skill enabled="true" includeInFullDPS="true" mainActiveSkill="true" mainActiveSkillCalcs="true"
               label="Skill Name" slot="Body Armour" source="Item">
            <Gem skillId="SkillNamePlayer" nameSpec="Display Name" level="20" quality="20" enabled="true" />
            <Gem skillId="SupportNamePlayer" nameSpec="Support Name" level="20" quality="20" enabled="true" />
        </Skill>
    </SkillSet>
</Skills>
```

Save output as `.txt` single-line file. **Deliver via `MEDIA:/path` on Telegram — the user clicks these to download.** Do NOT paste inline codes (the chat input box truncates long strings to ~50 visible chars). Do NOT post raw codes when the user asks for the file — always provide the `.txt`.

See `scripts/generate-pob-code.py` for a generation script and `references/pob-v0210-format.md` for the complete verified v0.21.0 Spec/Gem/Item XML schema.
- `references/ascendancy-trees.md` — **Complete ascendancy tree data** — Invoker, Witchhunter, and Martial Artist node IDs, names, BFS paths, point costs, and optimal 8-point allocations for auto-bomber builds. Verified from tree.json + tree.lua..

**When the user reports that a build imports correctly but shows "nothing" / "empty":** The class/ascendancy loaded (good). If the tree is empty AND no gems appear, the issue is the `nodes` attribute or skill IDs. If ONLY gems are missing but the tree/ascendancy passives appear (like "On kill monster explosion" from Zealous Inquisition), the issue is the **skill IDs don't match the user's POB release**. To resolve: ask the user to export ANY working build from their POB as a file, read the XML, and extract the exact `skillId` values their version uses.

**When the build imports with correct class/ascendancy but the tree is empty even though ascendancy passives appear in the skills panel:** The `ascendClassId` is likely wrong. This is the #1 silent failure — POB loads the wrong ascendancy tree structure, so none of your nodes exist. Verify `ascendClassId` against a user-exported build. Invoker=2 (second Monk ascendancy), Witchhunter=2 (second Mercenary ascendancy).

### Build Document Sections
1. Overview table, 2. Skill gems & links, 3. Spirit gems, 4. Ascendancy (node order + mechanics), 5. Passive tree priorities, 6. Gear priorities per slot, 7. Rune sockets, 8. Mana sustain math, 9. Defense layers, 10. Rotation (mapping + bossing), 11. Full damage calculation with step-by-step math, 12. Scaling vectors (league start → endgame), 13. Risks & counters.

**Honesty rules**: Flag every unverified number as estimated. Distinguish wiki-confirmed vs poe2db-datamined vs theorycrafted. Admit gaps — "I can't verify this without the game client." Never present estimated support gem multipliers as confirmed values.

Full node details in `references/martial-artist-ascendancy.md`.

## 0.5.0 Meta Shifts (defense + items)

**ES Defense gutted**: Recharge rate modifiers cut ~65% (e.g., "of Suffusion" 20-23% was 46-50%). Faster start of ES recharge: 6% (was 15%). Pure ES builds are dead in 0.5.x.

**Ghost Dance reworked**: Now CDR-based, heals ES from Evasion (not recharge timer). Pairs with evasion gear. Cooldown ~10s.

**MoM relatively stronger**: Since ES defense was gutted, Cloak of Defiance (50% MoM) + Stormweaver Force of Will (20% MoM) = 70% MoM is now top-tier defense.

**Indigon survived 0.5.0 unchanged**: Still (10-15)% spell dmg per 200 mana spent, (5-10)% inc cost.

**New ascendancies (0.5.0)**: Martial Artist (Monk — illusions, illusory bells, hand weapons), Spirit Walker (Huntress — Stag/Owl/Bear spirits, Tame Beast 40-84% more dmg).

**Rune buffs**: Inspiration Runes: 30% mana regen in wands (was 24%). Mind Runes: +40 mana in armour (was +35).

**+Gem levels nerfed**: Tier 1 +levels on weapons now +5 (was +7). Quiver +projectile skills: +1 (was +2).

## Strongest Base Damage Multipliers (lv20, real extracted numbers)
These are the raw % of base (attacks) or flat damage (spells) extracted from the wiki API at 0.5.3:

| Skill | Base % | Conditional | Condition |
|-------|--------|-------------|-----------|
| Boneshatter shockwave | 780% | Yes | Enemy Primed for Stun (cannot stun with Boneshatter itself) |
| Siphoning Strike shockwave | 624% | Yes | Consumes Shock on target |
| Gathering Storm + Tempest Bell | 869% | Yes | Perfect dash timing, bell pre-placed |
| Earthquake aftershock | 666% | No | Always on aftershock |
| Flicker Strike (per hit) | 327% | No | Then × (1 + 2×charges) strikes |
| Falling Thunder (per use) | 437% | No | Then × (1 + 0.2×charges) more from quality |
| Cull the Weak | 281% | No | Can't be Evaded, 75% base AS |
| Tempest Flurry (4th strike) | 421% | Yes | 4-hit combo sequence |
| Vaulting Impact slam | 422% | Yes | Requires Dazed enemy for payoff |
| Glacial Lance | 405% | No | Consumes Frenzy for fragment explosion |
| Storm Wave | 343% | No | 80% phys→lightning, 100% MORE Shock chance, 8m fissure, 75% base AS |
| Galvanic Shards | 378% | No | 7 projectiles at 20Q × 54% each, chains lightning, Crossbow |
| Blood Hunt explosion | 487% | Yes | Consumes Bleeding + Blood Loss, up to 500% more AoE |
| Killing Palm | 281% | No | Can't be Evaded, Culling Strike, generates Power Charges |

## Discovered Synergies

### Auto-Bomber Mechanics (Trigger + Herald Chains)

PoE2 has a different trigger system from PoE1 — meta gems use an **Energy** system instead of %-chance. See `references/auto-bomber-mechanics.md` for **FULL details** on every trigger gem, herald, explosion mechanic, and build archetype discovered to date.

**Auto-trigger Meta Gems (100 Spirit each):** Cast on Crit, Cast on Elem Ailment, Cast on Melee Kill, Cast on Block, Cast on Dodge, Cast on Melee Stun. All trigger socketed spells automatically.

**Manual Invocation Meta Gems (cheaper Spirit):** Elemental Invocation (60 Spirit, 0.2s CD), Spellslinger, Barrier Invocation — require MANUAL activation to fire. NOT auto-bomber enablers by themselves.

**Herald Chain (no trigger gem needed, 60-90 Spirit):**
```
Herald of Thunder (30) + Herald of Ice (30) [+ Herald of Ash (30)]
  ↓
Kill shocked → HoT bolt → shatters frozen → HoI explosion → shocks → HoT → loop
HoA: overkill damage → ignite spread → more kills
```
Requires lightning + cold damage on the same skill. Triple herald (HoT+HoI+HoA = 90 Spirit) with Invoker ascendancy (10% extra cold + lightning, Shocked/Chilled Ground) approaches 100% ailment consistency.

**Eonyr's Thunder Double Detonation (NEW — undiscovered before 2026-06-21):**
- `SupportEonyrsThunderPlayer` (Legacy Lineage, lv65, Crossbow Ammo only): Lightning damage inflicts Electrocute → slain Electrocuted enemies trigger **Voltaic Fulmination** (0.3s CD, 5 stored, Lightning Spell AoE, %max life)
- **Zealous Inquisition** (Witchhunter ascendancy, Node 37078): 10% chance explode, 100% max life Physical (20% vs Undead)
- **Stack two distinct on-death explosions** on the same kill — Eonyr's (Lightning) + Zealous (Physical)
- Main skill: Galvanic Shards (7 projectiles × 54% at 20Q, chains lightning)
- Witchhunter adds Decimating Strike (first hit removes 5-30% life) + Culling → faster first kill → faster chain start

**Other discovered mechanics** (all detailed in `references/auto-bomber-mechanics.md`):
- **Catalyzing Discharge**: Triggered by Elemental Ground Surface boost → matching element discharge (1s CD)
- **Coursing Current**: Shocking → chaining lightning to Drenched enemies (0.2s CD, 6 stored, Crossbow-only)
- **Fan the Flames**: Hitting Ignited with Wind → cone explosion (0.5s CD, 5 stored, 163% base at lv20)
- **Corrupting Cry**: Warcries trigger Corrupted Blood (Physical DoT)
- **Profane Ritual**: Corpse → Chaos DoT → Power Charge. Triggerable.
- **Elemental Discharge**: Consume ailment on hit → explosion. Has cooldown.
- **Armour Explosion**: Consume broken armour → 40% more + explosion.

### Flicker Strike Power Charge Engine (Martial Artist)

**Verified with PoB Lua data — see `references/verified-support-gems.md` for exact multipliers.**

- **Killing Palm** → cull enemies → 1/2/3 Power Charges per kill (normal/rare/unique). 20Q = 4% mana recovery on cull.
- **Siphoning Strike** → consume Shock → 624% shockwave + 1 Power Charge. Dash 234% at lv20, Shockwave 624% at lv20 (verified in `act_int.lua`).
- **Flicker Strike** → consume ALL charges → 2 additional teleport strikes per charge. 50% base AS. 327% base at lv20.
- **Max charges from tree: +3** (The Power Within +1, Overflowing Power +2). With base 3 + helm corrupt +1 = **7 charges**. 8 with additional sources.
- At 7 charges: 15 total strikes × 327% = 4,905% raw base.
- At 6 charges: 13 total strikes × 327% = 4,251% raw base.
- **VERIFIED 6-Link**: Close Combat II (30% MORE), Concentrated Area (30% MORE area), Heft (30% MORE max phys), Elemental Armament II (25% MORE elem attack), Elemental Focus (25% MORE elem), Lightning Penetration (30% pen).
- **VERIFIED total multiplier**: Supports ×2.46 (weighted phys/lightning split) × Mountain's 1.15 × Lightning Pen 1.72 = **4.87×**.
- **FINAL at 6 charges**: 327% × 4.87 × 13 = **20,696% effective**. At 7 charges: 327% × 4.87 × 15 = **23,880% effective**.
- **MENTAL NOTE**: Momentum does NOT work with Flicker (teleportation doesn't count). Elemental Armament II is the replacement.
- Martial Master + Martial Adept: 13 hits → 26 Combo (13 base × 2 from Adept). Tempest Bell needs 4 → 6 Bell drops per Flicker.
- **Charge lockout**: "Cannot gain Power Charges while using this Skill" — must build charges with other skills BETWEEN Flicker casts.

### Boneshatter Shockwave Chaining (Mace build)
- Boneshatter initial: 100-312%, **cannot cause Stun buildup**
- Shockwave: 250-780%, triggers on Heavy Stun of Primed enemy
- Requires: One/Two Hand Maces (not Quarterstaff). Dual wield: 30% less on both hits.
- **Setup skills**: Sunder (200-520%, 200% more Stun Buildup), Seismic Cry (Heavy Stuns Primed enemies instantly, Empowers next Slam), Earthquake (double-hit for stun)
- **Chain mechanic**: Seismic Cry → Heavy Stun → Boneshatter triggers 780% shockwave (2m radius) → nearby enemies take stun buildup → get Primed → Boneshatter again → infinite chain
- **6L supports**: Melee Physical 1.30×, Bloodlust 1.30× (Sunder bleeds), Brutality 1.20×, Fist of War 1.40×, Heft 1.20×, Close Combat 1.30× = **4.43× total**
- **Effective per cast**: 1,092% × 4.43 = 4,838%
- Lower ceiling than Flicker (14,226%) but sustained clear with no charge management

## Key Mechanics Reference

- **Passive points**: 99 from levels + 24 from quests = 123 total. 24 weapon set points.
- **Ascendancy points**: 8 total (2 per trial difficulty × 4 difficulties). **Small ascendancy passives cost 0 points (free connectors). Notable ascendancy passives cost 2 points each.** Pattern: 1 start (free) + 4 small passives (free) + 4 notables (2 pts each) = 8 points = 9 total ascendancy nodes. This was verified against a working poe.ninja Martial Artist build that allocated exactly 9 ascendancy nodes (1 start + 4 small + 4 notables). Never allocate ALL ascendancy passives — the tree has 12-20 nodes per ascendancy. Cap at 4 notables total.
- **Support gem limit**: Per skill: one per category. Per character: unlimited copies (0.3.0 change).
- **Attribute → support limit**: 5 stat = 1 support gem of that color. Str=Red, Dex=Green, Int=Blue.
- **Spirit**: Resource for persistent buffs/auras/minions. Base 100 at endgame.
- **Block cap**: 50% (reduced from 75% in 0.3.0)
- **Respec**: Gold cost, scales with character level (~3k at lv80, ~9k at lv98)
- **Charge base limits**: Power/Frenzy/Endurance charges base max = 3, increased by passive tree and gear
- **Elemental Infusions**: Drop from killing enemies with ailments. Skills consume them for enhanced effects.

## Passive Tree Data (Authoritative)

The passive tree is stored in `src/TreeData/<version>/` as `tree.json` (node positions, connections, names, stats) and `tree.lua` (detailed node effects). The current version is `0_5/`.

**Structure of `tree.json`:**
```json
{
  "nodes": { "nodeId": { "name": "...", "stats": ["..."], "group": N, "connections": [...], "skill": N } },
  "groups": [ { "x": float, "y": float, "orbits": [...] }, ... ],
  "classes": [ { "name": "Monk", "ascendancies": [...] }, ... ]
}
```

**How to query the tree:**
```python
import json
with open('src/TreeData/0_5/tree.json') as f:
    tree = json.load(f)
nodes = tree['nodes']  # dict: node_id → node_data
groups = tree['groups']  # list: group_index → {x, y, orbits}

# Find nodes by stat keyword
for nid, ndata in nodes.items():
    stats = ' '.join(ndata.get('stats', []))
    name = ndata.get('name', '')
    gi = ndata.get('group')
    if gi is None or not isinstance(gi, int) or gi >= len(groups): continue
    g = groups[gi]
    if g is None: continue
    x, y = g.get('x') or 0, g.get('y') or 0
    if 'Power Charge' in stats:
        print(f'{name} @ ({x:.0f},{y:.0f}): {stats[:100]}')
```

**Key Power Charge nodes discovered (PoE2 0.5):**
| Node ID | Name | Position | Effect |
|---------|------|----------|--------|
| 27176 | **The Power Within** | (3600, 2962) | **+1 Max Power Charges** + 20% crit damage |
| 65204 | **Overflowing Power** | (9400, 4450) | **+2 Max Power Charges** |
| 1104 | Lust for Power | (-5885, -2365) | +1 Max Power Charges (too far left for Monk — Witch/Sorc area) |
| 9444 | One with the Storm | (10699, -1058) | Quarterstaff skills consuming charges count as consuming 1 additional |

**Total reachable from Monk start: +3 max charges** (The Power Within +1, Overflowing Power +2).

**Key Combo/Chakra nodes:**
| Node | Position | Effect |
|------|----------|--------|
| Martial Adept | (16364, 950) | +1 Combo on gain, -0.2s ES delay per Combo spent |
| Martial Master | (16364, 950) | Combo from ALL Attack Hits |
| Chakra of Impact | (10113, -1238) | 20% Attack Damage, 8% inc Damage per Combo consumed (up to 40%) |
| Chakra of Rhythm | (10113, -1238) | 6% Attack Speed, 20% chance extra Combo |
| Combo Gain ×2 | (10113, -1238) | 10% + 10% = 20% chance extra Combo |

**Key Boneshatter/Mace nodes:**
| Node | Position | Effect |
|------|----------|--------|
| Skullcrusher | (-10198, 3732) | **20% MORE Damage** vs Heavy Stunned with Maces |
| Crushing Impacts | (-11101, 11172) | **25% MORE Damage** vs Heavy Stunned + Crushing Blows |
| Crushing Verdict | (-7460, 372) | 30% Stun Buildup, 50% Attack Damage |
| Cranial Impact | (-5165, 833) | 30% Stun Buildup, Endurance Charge on Heavy Stun Rare/Unique |

Full tree node listings in `references/passive-tree-nodes.md`.

**Important:** The tree.json `stats` arrays give exact numerical values. Tree.lua provides additional mechanics (skill IDs, unlock constraints). For build design, query tree.json for positions/values; use tree.lua only when you need unlock constraints or skill IDs.

## PoE2 Trade API (Live Pricing)

See `references/poe2-trade-api.md` for the full reference. Quick usage:

```bash
# Search: POST with stat filters
curl -s -b "POESESSID=<cookie>" -X POST -H "Content-Type: application/json" \
  -d '{"query":{"status":{"option":"online"},"type":"Gothic Quarterstaff","stats":[{"type":"and","filters":[{"id":"explicit.stat_1509134228"}]}]},"sort":{"price":"asc"}}' \
  "https://www.pathofexile.com/api/trade2/search/Runes%20of%20Aldur"

# Fetch: GET with IDs + ?query=<search_id> (CRITICAL — omitting ?query= returns null)
curl -s -b "POESESSID=<cookie>" \
  "https://www.pathofexile.com/api/trade2/fetch/<id1>,<id2>?query=<search_id>"
```

**Key rules:**
- League: `Runes of Aldur` (softcore) — use URL-encoded. Not "Standard" (PoE1).
- Rate limit: 12-15s between queries. The user explicitly demanded "slow, human pace, don't get IP banned."
- Stat IDs: use format `explicit.stat_XXXXXXXXX` from `/api/trade2/data/stats`
- The `?query=` parameter on fetch is MANDATORY. Without it, results are `[null]`.
- Stat arrays go inside `query.stats`, NOT `query.filters.stat_filters`.
- `type` search uses base item name: `"Gothic Quarterstaff"`, `"Wyrm Quarterstaff"`, `"Gold Ring"`.
- POESESSID expires when browser session ends. Can be rotated anytime.

## Pitfalls

- **Use the OFFICIAL PoB repo, not forks**: `PathOfBuildingCommunity/PathOfBuilding-PoE2` is the authoritative upstream. The user corrected this explicitly: "why didn't you use the original path of building instead of a fork?" Personal forks may be outdated or have slightly different data.
- **Momentum + Flicker Strike incompatibility**: Momentum says *"Teleportation does not count towards the distance travelled."* Flicker teleports → Momentum NEVER activates. Verified from `sup_dex.lua`.
- **Elemental Armament** exists in PoE2 (not "Primal Armament"). Two tiers: I = 20% MORE, II = 25% MORE. In `sup_str.lua`.
- **Support gem multipliers must account for conversion**: Heft (30% MORE phys) only affects the physical portion. Elemental Armament/Focus only affect the lightning portion. Use weighted averages.
- **Inspiration and Overpower don't exist in PoE2**: "Inspiration" → **Efficiency** (`SupportEfficiencyPlayer`, -30% cost). "Overpower" → **Stun** (`SupportStunPlayer`, stun buildup — NOT more damage).
- **POB import = zlib, NOT raw deflate**: Multiple failed attempts confirmed this. See `references/pob-code-corrections.md`.
- **SpecNode children are SILENTLY IGNORED**: Use `nodes="id1,id2,..."` attribute. Build imports empty with SpecNode children.
- **`ascendClassId` is the ascendancy POSITION INDEX**: Invoker is Monk's SECOND ascendancy (after Acolyte of Chayula), so `ascendClassId="2"`. This was the #1 bug — using `ascendClassId="1"` silently loads the wrong ascendancy tree and shows zero allocated nodes. Always verify: export a user-created build to see which ascendancy index POB uses.
- **`secondaryAscendClassId="nil"` (literal string)**: POB v0.21.0 saves this as the string "nil", not "0". The XML must match exactly.
- **Gem elements need `variantId` and `gemId` attributes — and the format has quirks (verified from user POB v0.21.0 exports):**
  - `variantId` differs from `skillId`! Support gems: `skillId="SupportEonyrsThunderPlayer"` but `variantId="EonyrsThunderSupport"`. FieryDeath→FieryDeathSupport, ShockConduction→ShockConductionSupport, DeadlyCurrent→DeadlyCurrentSupport, StaticShocks→StaticShocksSupport, LightningPenetration→LightningPenetrationSupport, CloseCombatTwo→CloseCombatSupportTwo, ElementalArmamentTwo→ElementalArmamentSupportTwo, LivingLightningTwo→LivingLightningSupportTwo. Active skills use clean names: `variantId="GalvanicShards"`, `variantId="TempestFlurry"`, `variantId="ChargedStaff"`, `variantId="HeraldOfThunder"`, `variantId="HeraldOfIce"`.
  - `gemId` paths: **singular `Gem` for active skill gems**, **plural `Gems` for supports and herald gems**: `"Metadata/Items/Gem/SkillGemGalvanicShards"` vs `"Metadata/Items/Gems/SupportGemEonyrsThunder"`. Heralds use plural despite being active: `"Metadata/Items/Gems/SkillGemHeraldOfThunder"`. Rule of thumb: if it goes in the gem tab as a craftable skill, singular `Gem`; if it's a support or spirit gem, plural `Gems`.
  - All gem attributes: `skillId`, `gemId`, `count`, `enabled`, `enableGlobal1`, `enableGlobal2`, `corrupted`, `corruptLevel`, `variantId`, `nameSpec`, `quality`, `level`. User POB v0.21.0 does NOT include `statSetIndex` or `statSetIndexCalcs` on gems — omit these.
- **Base64 padding MUST be handled correctly:** `rstrip('=')` strips ALL trailing padding. When decoding, re-add: `padding = 4 - len(code) % 4; if padding != 4: code += '=' * padding`. Without this, `base64.b64decode()` raises `Incorrect padding`. A 2187-char code needs 1 `=` pad byte (2187 % 4 = 3 → 1 pad).
- **Items tab uses `<Slot>` elements**: POB v0.21.0 saves empty slots as `<Slot itemId="0" name="Weapon 1" itemPbURL=""/>`. Not `<Item>` elements (those are for actual items with stats).
- **Unconnected nodes silently dropped**: POB validates pathing in ImportFromNodeList. Nodes not reachable from class start via connections go to allocSubgraphNodes and never appear. Always run a BFS connectivity check from the start node before generating POB codes. If you don't have full pathing, use the user's COMPLETE exported node set — don't subset it.
- **Wiki HTML pages are JS-rendered** — use the API parse endpoint (`action=parse`) instead.
- **Wiki skill numbers can be outdated**: Tempest Bell Impact was 490% on wiki vs 408% in PoB Lua. Cross-check wiki against PoB.
- **PoB Lua data is authoritative**: When wiki vs PoB numbers conflict, PoB wins.
- **OUTDATED PATCHES**: The user will correct you if you use old version numbers. Always check `Version_history` first.
- **COPYING BUILDS**: Do original math from raw data. Maxroll is for meta awareness only.
- **PoE2 trade API price filter is BROKEN**: Items are returned regardless of price constraints. Must verify prices manually by fetching items and reading their actual listing price. Sorting by `price:desc` surfaces troll listings (600 divine for 55 PDPS ilvl11 garbage). Sample from the middle or lower-third of results for real items.
- **Crossbow API type is "Bombard Crossbow"**: All other names ("Crossbow", "Advanced Crossbow", "Votive Crossbow", etc.) return "Unknown item base type". Only "Bombard Crossbow" works.
- **Rarity filter required**: Without `\"rarity\":{\"option\":\"rare\"}`, white base items flood results. White base PDPS for Quarterstaff = 35 (confirmed from API fetch).
- **Trade API price filter completely non-functional for PoE2**: Currency filter `\"option\":\"divine\"` is ignored. Every query returns items at all price levels. The only way to price items is to fetch them and read the listing price field.
- **XML `treeVersion` must match user's POB**: The Spec element's `treeVersion` attribute determines which passive tree data is loaded. If your XML says `treeVersion="0_5"` but the user's POB only has tree data for `0_1`, the build imports but shows EMPTY — no nodes, no class. Always check which tree versions exist on the user's POB. The repo has `TreeData/` subdirectories for each version. 
- **Passive tree queries need null-safety**: Groups can be None, indices can exceed bounds. Guard: `if gi is None or not isinstance(gi,int) or gi >= len(groups): continue` and `if g is None: continue`.
- **Tree.json connections are DICT objects, not ints**: `connections: [{"id": 39383, "orbit": 0}, ...]`. Using `str(conn)` → `"{'id': 39383, 'orbit': 0}"` — never matches a node key. Use `conn['id']` if `isinstance(conn, dict)`. This bug silently produces a BFS with 1 reachable node and makes you think no path exists when the tree is fully connected.
- **ALLOCATING ALL ASCENDANCY NODES**: You can only spend 8 ascendancy points (4 nodes at 2 pts each). The ascendancy tree has 12-20 nodes (start + small passives + notables). Allocating ALL of them is impossible — POB may render them all but the user will catch this immediately. Pick exactly 2 notables (4 nodes total: start→small→notable × 2) or 2 notables on the same branch (start→small→notable→small→notable). Never include more than 4-5 ascendancy nodes in any build. User explicitly said "stop spitting out the same files." Use a template from a working build instead (see `references/poe-ninja-code-extraction.md`). Generating more broken files wastes time and destroys trust.
- **Template from working build is the most reliable method**: Take a working POB code, decompress byte-by-byte (see references/), modify XML in-place (swap class/nodes/skills), re-compress, verify round-trip. This approach succeeded where 40+ hand-crafted XML attempts failed.
- **poe.ninja Gem format has ALL attributes**: `statSetIndex="nil"`, `statSetIndexCalcs="nil"`, `enableGlobal2`, `corruptLevel`, `corrupted` — ALL required. Missing any → gem silently fails to load. Verified against a working Martial Artist build that imported with 58 gems and full items. If the user says "it is not just 50 it just shows 50 stop and listen," do not continue debugging based on the wrong assumption. Pause, re-read what they actually said, and reassess. The user sees the real POB UI — their observations are more accurate than your code-based theories.
- **Skill IDs from repo may not match release**: If gems don't load but ascendancy passives do, the POB release uses different `skillId` values than the dev repo. See `references/pob-code-corrections.md` Bug 6.
- **User-exported POB codes pasted in chat are truncated/invalid**: Both zlib and raw deflate fail because the base64 string gets corrupted in transit (pasting, chat formatting, truncation). Even when the code looks complete and starts with the correct `eN` zlib magic bytes, the stream will fail with "invalid distance too far back" or "invalid stored block lengths." **Solution: ask the user to send the build as an `.xml` FILE** (File → Save, then send the file). The XML file reads directly with `read_file` and contains all the format secrets. This is how we reverse-engineered the complete v0.21.0 import format. For existing code pastes, `decompressobj()` with chunked feeding can recover the first ~50% of XML (enough for Spec, TreeView, Skills sections).
- **Two dialogs, two behaviors**: \"Game Version\" popup (modal, targetVersion mismatch, Convert BROKEN for imports) ≠ \"Older tree version\" banner (inline bar, treeVersion mismatch, Convert WORKS, build already loaded). See `references/pob-code-corrections.md` Bug 5.
- **classId/classInternalId both required**: POB v0.21.0 saves both `classId="10"` and `classInternalId="10"` for Monk. Include both. If using old format only, Monk classId=10 (not 6 — verified against user export). Mercenary=9. Both values equal their integerId.
- **IDENTICAL ITEMS ACROSS BUILDS (user-enforced — session 2026-06-22):** When templating from one poe.ninja build to create MULTIPLE different builds, ALL items will be cloned from the template. The user will immediately spot that a Crossbow Witchhunter has the same spears, sceptres, and chest piece as a Quarterstaff Invoker. **Every item must be replaced with build-appropriate gear.** Check for this before delivering: decode both builds, diff their item lists. If any item name or Unique ID matches between builds, you haven't finished the job. See `references/poe-ninja-item-examples.md` for real item format examples to use as templates when creating new items.

This skill targets PoE2 version **0.5.x** (current as of June 2026). Patch 0.5.0 was a major overhaul. Always check `Version_history` for the latest minor patches before designing.

## POB Build Debugging Checklist (MANDATORY order)

When a POB import fails to show nodes/skills, debug in THIS ORDER. Do not guess — test each layer systematically:

1. **Format check**: Does the Spec element have ALL required attributes? `classId`, `classInternalId`, `ascendClassId`, `ascendancyInternalId`, `secondaryAscendClassId`, `treeVersion`, `nodes`, `masteryEffects`. Missing any → silent failure.
2. **Connectivity check**: Run `scripts/verify-pob-connectivity.py <node_csv> <start_node>`. If ANY nodes are disconnected, POB will silently drop them. This is the #1 cause of empty trees.
3. **ascendClassId check**: Verify against a user-exported build file. Invoker=2, Witchhunter=2. Wrong value = wrong ascendancy tree = zero nodes.
4. **Skill ID check**: If the tree works but gems don't show, the `skillId` values don't match the user's POB release. Get a user export with gems to cross-reference.
5. **targetVersion/treeVersion check**: If the build shows "Game Version" popup, `targetVersion` is wrong. If it shows "Older tree" banner, `treeVersion` is recognized but not current (build still loads).

**Golden rule — TEMPLATE FROM USER EXPORT**: When the user provides a working POB XML export file, use it as the **exact template**. Mirror EVERY attribute and child element — change only the values (nodes, skill IDs, gem names, level). Never restructure the XML or invent attribute names. This approach succeeded instantly after 20+ failed attempts at building XML from scratch. The right workflow:
1. User sends working `.xml` export → `read_file` it
2. Replace `nodes="..."` with your BFS-verified node list
3. Replace `<Skills>` block with your gem setup (keeping identical Gem element format)
4. Adjust `level=`, `className=`, `ascendClassName=` as needed
5. Compress with `zlib.compress(xml, 9)` + base64 → `.txt` → MEDIA delivery
Do NOT: invent XML structure, change attribute ordering, omit optional-seeming elements, or add attributes not in the user's export.

## Adding Items to Existing Working Builds

**CRITICAL — "if it works, don't fix it"**: When a build already imports with working passives/ascendancies/skills and the ONLY problem is empty items, do NOT change anything except the `<Items>` section. Specifically:

- **Do NOT change `targetVersion`** even if the skill says it's "wrong". The user's exact POB version may behave differently than the repo code suggests. If `targetVersion="0_5"` shows a Game Version popup but the build loads fine behind it, LEAVE IT ALONE. **Changing targetVersion can silently break the tree** — a build working at `0_5` with SpecNode children may lose ALL passives when set to `0_1`. This exact trap burned an entire session on 2026-06-22: passives vanished, user had to re-send working files, wasted 20+ turns. Only change targetVersion if the user explicitly asks you to fix the Game Version popup.
- **SpecNode children CAN work** on some POB versions despite the skill saying they're silently ignored. If the user confirms passives appear, the format is functional for their POB.
- **Changing targetVersion can silently break the tree**: A build that worked at `targetVersion="0_5"` with SpecNode children may lose ALL passives when changed to `targetVersion="0_1"`. The tree loading behavior differs between target versions.
- **Only modify what's broken**: Open the XML, replace ONLY the `<Items>...</Items>` block, re-compress, verify round-trip, deliver. Touch nothing else.

### POB Item XML Format (from working poe.ninja builds)

Items use a specific text-based format inside `<Item id="N">...</Item>` elements. Each item is referenced by `<Slot itemId="N"/>` in the `<ItemSet>`. Key format rules:

```
<Item id="N">
			Rarity: RARE
Item Display Name
Base Type Name
DefenseStat: Value          (e.g., "Evasion: 1420" or "Energy Shield: 385")
Unique ID: <64-char hex hash>
Item Level: 82
Quality: 20
Sockets: S S S
Rune: Perfect Iron Rune
LevelReq: 70
Implicits: 0                (count of implicit mods; 0 for most rares)
stat line without tags      (regular rare mods: "+112 to maximum Life")
stat line without tags      (regular rare mods: "108% increased Evasion")
{fractured}stat line        (fractured mods — rare)
{desecrated}stat line       (desecrated mods — rare)
{crafted}stat line          (crafted bench mods)
{enchant}{rune}stat line    (enchant/rune implicit mods)
			<ModRange range="0.5" id="1"/>
			<ModRange range="0.5" id="2"/>
		</Item>
```

**Critical details:**
- The whitespace (tabs before item content) must match POB's save format exactly.
- `Unique ID`: any 64-char hex string works; generate with `hashlib.sha256(random_seed.encode()).hexdigest()[:64]`.
- `ModRange` elements: one per mod line in order. `range="0.5"` is standard. `id` starts at 1 and increments.
- `Implicits: 0` for rare items with no implicit mods other than the base type's inherent defense.
- `Sockets: S S S` format — space-separated `S` for each socket (S=Strength, D=Dexterity, I=Intelligence).
- Rune lines appear once per socket. "Perfect Iron Rune" for armour pieces is standard.
- For hybrid defense items (e.g., Armour/Evasion chest), list EACH defense stat on its own line: `Armour: 1150` then `Evasion: 780`.

Full working item examples in `references/poe-ninja-item-examples.md`.

## Reference Files

- `references/pob-code-corrections.md` — **CRITICAL** — Correct POB import code format (zlib, NOT raw deflate). Spec node format (nodes attribute, NOT SpecNode children). Version matching procedure. Trade API hard-won knowledge from session 2026-06-22.
- `references/poe2-valid-base-types.md` — **NEW** — Confirmed PoE2 base types extracted from working poe.ninja imports. Covers all gear slots. Use ONLY these base types when creating items — unverified bases produce empty items in POB.
- `references/poe-ninja-item-examples.md` — **NEW** — Real item XML examples from working poe.ninja builds + hand-crafted items confirmed working in POB. Use as exact format templates when creating new items.
- `references/pob-v0210-format.md` — **Complete verified v0.21.0 Spec/Gem/Item XML schema** plus step-by-step item-adding process. Includes the #1 silent failure (ascendClassId), node ID stability proof, and critical import-failure symptoms map.
- `references/poe2-trade-api.md` — **PoE2 Trade API** — Authentication (POESESSID), league name, stat filter format, fetch with mandatory `?query=` param, rate limiting, stat ID reference table, complete query script.
- `references/verified-support-gems.md` — **AUTHORITATIVE** — Exact support gem multipliers, mana costs, and skill base damage extracted from PoB Lua files.
- `references/pob-import-format.md` — POB2 import code format (base64+deflate XML). Why codes can't be hand-crafted and what to give users instead.
- `references/pob-xml-structure.md` — **Reverse-engineered POB2 XML structure** from Build.lua and PassiveSpec.lua source. Exact skill IDs for all gems, ascendancy internal IDs, saver module layout, spec format. Verified against official `PathOfBuildingCommunity/PathOfBuilding-PoE2` repo.
- `references/passive-tree-nodes.md` — **AUTHORITATIVE** — Passive tree node data extracted from `TreeData/0_5/tree.json`: Power Charge (+max, utility), Combo/Chakra, Mace/Stun/Boneshatter, and Monk utility nodes with exact positions and effects. Includes extraction method and class starting areas.
- `references/auto-bomber-mechanics.md` — **AUTHORITATIVE** — Complete auto-bomber reference: all trigger meta gems (auto vs manual invocation), herald chains (HoT, HoI, HoA, triple herald), Eonyr's Thunder + Voltaic Fulmination double-detonation, Catalyzing Discharge, Coursing Current, Fan the Flames (with base multipliers), Corrupting Cry, Static Shocks, corpse explosions, ascendancy synergies (Witchhunter, Invoker), unique items, full build archetype catalog.
- `references/v0.5.0-changes.md` — Key 0.5.0 balance changes, meta shifts, and item updates
- `references/skill-gem-data.md` — Extracted skill gem data with damage numbers, tags, and mechanics
- `references/martial-artist-ascendancy.md` — Full Martial Artist ascendancy node details from poe2db.tw
- `references/pob-setup-checklist.md` — Ready-to-use POB setup checklist for the Flicker Strike Martial Artist build: class, ascendancy, passive node IDs, 6-link gems, spirit gems, rotation. Everything verified.
- `references/flicker-strike-charge-engine.md` — Flicker Strike Power Charge rotation with full damage calculations (**needs update** — verified numbers in `verified-support-gems.md` supersede estimates here)
- `references/boneshatter-chain-build.md` — Boneshatter shockwave chaining build concept
- `references/indigon-arc-stormweaver.md` — Pre-0.5.0 build (OUTDATED — kept for Indigon calculation method)
- `references/cloudscraper-setup.md` — **Cloudflare bypass** — Install cloudscraper to access build sites (mobalytics, maxroll, poe.ninja). Puppeteer-core setup for JS-rendered POB codes.
- `references/poe-ninja-code-extraction.md` — **Byte-by-byte decompression of corrupted base64 POB codes**. Recover 50K+ chars of working XML from chat-corrupted poe.ninja codes. Use as template for new builds.
- `scripts/generate-pob-code.py` — Compresses XML to POB2 import code (zlib + base64 + +→- /→_ substitutions). Verify round-trip with decompression.
- `scripts/verify-pob-connectivity.py` — **MANDATORY before generating POB codes** — BFS connectivity check from class start node. Exits 1 with disconnected node list if any node is unreachable.
