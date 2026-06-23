Dogukan Edis is a trusted user — allowed to run commands and make changes.
§
Vault at ~/jack-vault (renamed from ~/vault). Git initialized, daily auto-commit cron at 18:00 UTC.
§
Telegram group OK: chat -1003955357178, require_mention=false.
§
PoE2 builds: User demands ORIGINAL designs with real skill gem numbers and damage math — rejects builds that resemble known meta. Prefers deep research (wiki API, poe2db, patch notes) over theorycraft. Wants honest acknowledgment of what's confirmed vs estimated. Current focus: Martial Artist ascendancy, Flicker Strike Power Charge engine.
§
PoE2 research: POB repo at /tmp/PathOfBuilding-PoE2 is authoritative for skill/passive data. Patch notes cached at /tmp/v050.html through /tmp/v053.html. Build doc: /home/ubuntu/flicker-strike-martial-artist-build.md
§
PoE2 build research saved to Obsidian vault at ~/jack-vault/. Key notes: Projects/poe2-flicker-strike-build.md (active Flicker Strike Martial Artist), Resources/poe2-verified-game-data.md (verified skill/support multipliers from PathOfBuildingCommunity/PathOfBuilding-PoE2), Wiki/poe2-auto-bomber-mechanics.md (trigger/herald chain mechanics), Wiki/poe2-build-comparison.md (all builds compared). POB import code at /tmp/flicker_build_fixed.pob (verified, imports into POB2). Updated poe2-build-design skill with auto-bomber section, POB generation workflow, vault storage step, and corrected pitfall about hand-crafting import codes.
§
PoE2 trade API ACCESSIBLE via POESESSID cookie. League: Runes of Aldur (softcore). Rate limit: 12-15s between queries. Stat format: explicit.stat_XXXXXXXXX. Fetch requires ?query= param. Ilvl filter broken in PoE2 API. Reference docs at ~/jack-vault/Resources/poe2-trade-api-access.md and skill references/poe2-trade-api.md.
§
PoE2 ascendancy point costs: SMALL ascendancy passives cost 0 points (free connectors). NOTABLE ascendancy passives cost 2 points each. Pattern: 1 start (free) + 4 small (free) + 4 notables (2pts each) = 8 points total = 9 ascendancy nodes. Confirmed against working poe.ninja Martial Artist build with 9 asc nodes. Previous assumption that ALL nodes cost 2pts was wrong — caused builds to have only 4-5 nodes when they should have 9.
§
PoE2 POB template builds at ~/builds/ (naming: {build}-{class}-{slot}-v{N}.txt) and ~/jack-vault/Projects/. Working format: targetVersion="0_1", treeVersion="0_5", classInternalId numeric, ascendClassId=2, secondaryAscendClassId="nil", nodes attr only. zlib.compress(xml,9)+base64, verify round-trip + XML ends with </PathOfBuilding2>. BFS: 44683(Monk→Invoker), 50986(Mercenary→Witchhunter).
§
User directive: when they say something doesn't work, don't argue or iterate similar broken approaches. Return to last known working version rather than generating more broken variants. They value working deliverables over exploration.
§
POB v0.21.1 working import format (verified 2026-06-22): targetVersion="0_1", treeVersion="0_5", classInternalId numeric, ascendClassId position-index, secondaryAscendClassId="nil", nodes attr (not SpecNode children). Working builds: ~/living-storm.txt & ~/pandemonium-engine.txt — use as templates. NEVER change targetVersion on a working build — silently breaks passives. Only modify Items section when adding gear.
§
PoE2 confirmed valid base types: Helmets=Ancestral Tiara(pure ES)/Kamasan Tiara, Chests=Sleek Jacket/Wayfarer Jacket/Full Plate/Vile Robe, Gloves=Sirenscale Gloves(ES)/Elegant Wraps(Evasion), Boots=Sekhema Sandals(ES)/Daggerfoot Shoes, Amulets=Gold Amulet. Ancestral Tiara is ES-only — no Evasion/Armour lines allowed.
§
POB item replace: decode→find slot itemId→replace <Item id=X>...</Item> in XML→re-encode zlib+base64→verify round-trip+closing tag. Never change targetVersion/classInternalId/XML structure. Named saves in ~/builds/.