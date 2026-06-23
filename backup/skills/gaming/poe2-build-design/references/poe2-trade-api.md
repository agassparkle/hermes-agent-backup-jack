# PoE2 Trade API Reference

**How to query live item prices from the official PoE2 trade site.**

---

## Authentication

Requires a `POESESSID` cookie from a logged-in pathofexile.com session:
1. Log into pathofexile.com in browser
2. F12 → Application → Cookies → `pathofexile.com` → `POESESSID`
3. Copy the 32-char hex value
4. Pass as `-b "POESESSID=<value>"` in curl

Cookie expires when browser session ends. Can be rotated anytime.

## League

Current softcore league (as of June 2026): **Runes of Aldur**
- Use URL-encoded: `Runes%20of%20Aldur`
- NOT `Standard` (that's PoE1)
- HC variant: `HC%20Runes%20of%20Aldur`

Find current leagues: `GET /api/trade2/data/leagues`

## Rate Limiting

**USER-ENFORCED:** The user explicitly demanded slow, human-paced searches.
- **Minimum 12 seconds** between queries
- **15 seconds** recommended safe pace
- If search times out (20s+), wait 30s before retry
- Never fire rapid searches — Cloudflare will rate-limit
- Search results expire quickly (seconds to minutes) — fetch immediately after search

## Search (POST)

```
POST https://www.pathofexile.com/api/trade2/search/<League>
Content-Type: application/json
Cookie: POESESSID=<cookie>

{
  "query": {
    "status": {"option": "online"},
    "type": "Gothic Quarterstaff",
    "stats": [{
      "type": "and",
      "filters": [
        {"id": "explicit.stat_1509134228"},
        {"id": "explicit.stat_210067635"}
      ],
      "disabled": false
    }],
    "filters": {
      "type_filters": {
        "filters": {
          "ilvl": {"min": 75}
        }
      }
    }
  },
  "sort": {"price": "asc"}
}
```

**Response:**
```json
{
  "id": "Wl9yVpbSm",
  "total": 1311,
  "result": ["a4ff6ff5...", "510e2718...", ...]
}
```

### Key Fields

| Field | Description |
|:---|:---|
| `query.status.option` | `"online"` — only online sellers recommended |
| `query.type` | Base item name, e.g. `"Gothic Quarterstaff"`, `"Wyrm Quarterstaff"`, `"Gold Ring"`. Use names from `/api/trade2/data/items` |
| `query.stats` | Array of stat groups. Each group: `"type":"and"` + `"filters"` array |
| `query.filters` | Structural filters. `type_filters.filters.ilvl` — non-functional for PoE2 (always returns 0). Skip ilvl filtering |
| `sort.price` | `"asc"` for cheapest first |
| Response `id` | Search session ID — **must pass to fetch** |
| Response `result` | Array of up to 100 item IDs (64-char hex) |

### Stat ID Format

Use `explicit.stat_XXXXXXXXX` (10-digit numeric suffix):

| Stat | ID |
|:---|:---|
| Flat Lightning Damage to Attacks | `explicit.stat_1754445556` |
| Flat Physical Damage to Attacks | `explicit.stat_3032590688` |
| % increased Physical Damage | `explicit.stat_1509134228` |
| % increased Attack Speed | `explicit.stat_681332047` |
| % increased Attack Speed (Local) | `explicit.stat_210067635` |
| + to Level of all Melee Skills | `explicit.stat_9187492` |
| + to Level of all Elemental Skills | `explicit.stat_2901213448` |
| % increased Elemental Damage with Attacks | `explicit.stat_387439868` |
| % increased Critical Strike Chance | `explicit.stat_518292764` |
| % increased Elemental Damage | `explicit.stat_3141070085` |
| Trigger skills refund Energy | `explicit.stat_599320227` |

Find all stat IDs: `GET /api/trade2/data/stats`

### Structural Filter Reference

| Filter | Path | Notes |
|:---|:---|:---|
| Item category | `filters.type_filters.filters.category.option` | `"weapon"`, `"armour"`, `"accessory"` |
| Ilvl | `filters.type_filters.filters.ilvl` | **NON-FUNCTIONAL in PoE2** — always returns 0. Skip |
| Weapon class | `filters.type_filters.filters.weapon_class.option` | `"Staves"` — but `type` filter is more reliable |

## Fetch (GET)

```
GET https://www.pathofexile.com/api/trade2/fetch/<id1>,<id2>,<id3>?query=<search_id>
Cookie: POESESSID=<cookie>
```

**CRITICAL:** The `?query=<search_id>` parameter is **MANDATORY**. Without it, all results are `[null, null, null]`. The search session expires quickly — fetch within seconds of searching.

**Response:**
```json
{
  "result": [{
    "item": {
      "name": "The Sentry",
      "typeLine": "Gothic Quarterstaff",
      "ilvl": 76,
      "explicitMods": [{
        "hash": "stat.explicit.stat_1509134228",
        "description": "64% increased [Physical] Damage"
      }],
      "properties": [...],
      "requirements": [...]
    },
    "listing": {
      "price": {"amount": 1, "currency": "regal"},
      "account": {"name": "..."},
      "whisper": "..."
    }
  }]
}
```

### Extracting Data

- `item.typeLine` — base item type
- `item.ilvl` — item level
- `item.explicitMods[].hash` — `"stat.explicit.stat_XXXXXXXXX"` (hash format differs from search format — search omits the `stat.` prefix)
- `item.explicitMods[].description` — human-readable mod text (contains `[Tag]` wiki formatting)
- `listing.price.amount` + `listing.price.currency` — price (e.g., `1`, `"exalted"`)
- `listing.account.name` — seller account

### Common Currency Names

`aug`, `transmute`, `alteration`, `alch`, `regal`, `exalted`, `divine`, `chaos`, `vaal`, `exalt`, `annul`, `blessing`

## Complete Query Script

```bash
#!/bin/bash
POESESSID="your_cookie_here"
LEAGUE="Runes%20of%20Aldur"

# Search
SEARCH=$(curl -s -b "POESESSID=$POESESSID" \
  -X POST --max-time 12 \
  -H "Content-Type: application/json" \
  -d '{"query":{"status":{"option":"online"},"type":"Gothic Quarterstaff","stats":[{"type":"and","filters":[{"id":"explicit.stat_1509134228"}],"disabled":false}]},"sort":{"price":"asc"}}' \
  "https://www.pathofexile.com/api/trade2/search/$LEAGUE")

QID=$(echo "$SEARCH" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
IDS=$(echo "$SEARCH" | python3 -c "import json,sys; print(','.join(json.load(sys.stdin)['result'][:3]))")

sleep 2

# Fetch immediately (query param MANDATORY)
curl -s -b "POESESSID=$POESESSID" --max-time 12 \
  "https://www.pathofexile.com/api/trade2/fetch/${IDS}?query=${QID}" | \
  python3 -c "
import json,sys
d=json.load(sys.stdin)
for r in d['result']:
    if r is None: print('null'); continue
    item = r['item']; p = r['listing']['price']
    print(f'{p[\"amount\"]} {p[\"currency\"]}  ilvl:{item[\"ilvl\"]}  {item[\"typeLine\"]}')
    for m in item.get('explicitMods',[]):
        print(f'    {m[\"description\"][:80]}')
"
```

## Pitfalls

- **PRICE FILTER IS COMPLETELY BROKEN (2026-06-22 confirmed)**: All currency/price filters in `trade_filters` are silently ignored. Queries return items at ALL price levels regardless of `\"max\":50,\"min\":5,\"option\":\"divine\"`. The only way to price items: fetch them and read `listing.price.amount`. Do NOT trust search result counts as filtered.
- **SORT BY PRICE DESC = TROLL LISTINGS**: Top results when sorting by price descending are absurdly overpriced garbage (e.g., ilvl11 55 PDPS white Quarterstaff at 600 divine, 900 divine Crossbows at 69 PDPS). Sample from positions 30-70 for real items.
- **CROSSBOW TYPE IS \"Bombard Crossbow\"**: All other names (\"Crossbow\", \"Advanced Crossbow\", \"Votive Crossbow\", \"Siege Crossbow\", \"Arbalest\", \"Repeating Crossbow\") return \"Unknown item base type\". Only \"Bombard Crossbow\" works.
- **RARITY FILTER REQUIRED**: Without `\"type_filters\":{\"filters\":{\"rarity\":{\"option\":\"rare\"}}}`, white/normal base items flood results. White Quarterstaff base PDPS = 35 (confirmed from API fetch).

- **Wrong league name**: PoE2 uses `Runes of Aldur`, not `Standard` (PoE1). Check `/api/trade2/data/leagues` if uncertain.
- **Missing `?query=` on fetch**: Results will be all `null`. The query parameter links items to the search session. Search sessions expire fast.
- **Ilvl filter doesn't work**: `type_filters.filters.ilvl` always returns 0 results. PoE2 trade API doesn't support ilvl filtering this way.
- **Wrong stat ID format**: Items use `stat.explicit.stat_XXXXXXXXX` in their hash field, but the search API omits the `stat.` prefix — search uses `explicit.stat_XXXXXXXXX`.
- **Stat filter nesting**: Stat filters go in `query.stats[]`, NOT in `query.filters.stat_filters`.
- **Base type names**: `"Quarterstaff"` alone doesn't work. Must use full name: `"Gothic Quarterstaff"`, `"Wyrm Quarterstaff"`, `"Long Quarterstaff"`, etc. Find all via `/api/trade2/data/items`.
- **Search expiration**: If fetch returns `[null]`, the search session expired. Re-search and fetch immediately.
- **Request format security**: Don't pipe curl to python in one command (`curl | python3`). Use files or heredocs.
