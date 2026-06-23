# Cloudscraper — Cloudflare Bypass

cloudscraper bypasses Cloudflare anti-bot challenges on PoE build sites.

## Install
```bash
pip3 install cloudscraper
```

## Usage
```python
import cloudscraper
scraper = cloudscraper.create_scraper()
resp = scraper.get('https://poe.ninja/poe2/builds', timeout=30)
```

## Verified working on
- poe.ninja (200, returns full page HTML with 90KB+)
- maxroll.gg (200, returns full page HTML with 500KB+)
- mobalytics.gg (200)

## Limitations
- POB codes on these sites are loaded via JavaScript XHR after page load — cloudscraper gets the HTML shell but not the dynamically loaded data
- poe.ninja build data API uses **protobuf** (`application/x-protobuf`), not JSON. Cannot decode without the .proto schema
- For JS-rendered data, Puppeteer-core + Chromium is the next step (installed and available)

## Puppeteer Setup
```bash
npm install puppeteer-core
```
```javascript
const puppeteer = require('puppeteer-core');
const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
});
```

## poe.ninja Passive Tree Download
poe.ninja bundles the full passive tree as a JSON literal in its JavaScript. Download with:
```python
import cloudscraper, json, re
s = cloudscraper.create_scraper()
r = s.get('https://assets.poe.ninja/_astro/a.Cr9DCTHT.mjs', timeout=30)
brace_start = r.text.find('{', r.text.find('JSON.parse(`'))
depth, i = 0, brace_start
while i < len(r.text) and (depth > 0 or i == brace_start):
    if r.text[i] == '{': depth += 1
    elif r.text[i] == '}': depth -= 1
    i += 1
tree = json.loads(r.text[brace_start:i])
# 4539 nodes, IDs match repo TreeData/0_5/tree.json
```
