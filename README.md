# GULF WATCH 2.0

**Real-time MENA security intelligence deck.** OSINT aggregator watching the Gulf
theatre: 70+ public RSS sources — tier-1 wire services (Reuters, BBC, Guardian,
Al Jazeera) and official government accounts (MOI/MOD/civil defence across UAE,
KSA, Qatar, Kuwait, Bahrain, Oman, Israel) — classified, geolocated, scored.

Live: **https://nkoxxx.github.io/gulf-watch-2.0/** (Pages, rebuilt on every hourly feed refresh)

```
┌────────────┐   hourly GH Action   ┌──────────┐   Pages   ┌──────────────┐
│ 70+ RSS    │──▶ scripts/fetch_* ─▶│ public/*.json ─▶ index.html deck │
└────────────┘   23 * * * * UTC     └──────────┘           └──────────────┘
```

## Architecture (deliberately boring where it matters)

- **Zero runtime dependencies.** One self-contained `index.html`. No frameworks,
  no CDNs, no trackers, no supply chain. CSP locked to `'self'` + inline styles.
- **Static pipeline.** Python fetchers commit `public/incidents.json` +
  `public/markets.json` hourly via GitHub Actions; Pages serves the deck
  directly from repo state. No servers to sleep, no DBs to expire, no cold starts.
- **Feed fallback.** If the committed feed is unreachable, the deck falls back to
  the previous-generation live mirror (`gulf-watch-v2.vercel.app`), then degrades
  visibly (degraded banner) rather than lying.
- **XSS-safe by construction.** Every feed-derived string is rendered via
  `textContent`/`createElement` — never `innerHTML`.

## Layout

- `index.html` — the deck (map, stream, situation rail, ticker)
- `scripts/fetch_rss.py` — RSS ingestion + classification + geolocation (ported from the proven v2 fetcher; pure RSS, zero API keys)
- `scripts/fetch_markets.py` — Brent/TTF/gold/BTC quotes (Yahoo public endpoints)
- `scripts/coordinate_extractor.py` — gazetteer-based coordinate extraction (ported)
- `.github/workflows/update-feed.yml` — hourly refresh + auto-commit
- `.github/workflows/ci.yml` — gitleaks + lint gates
- `SECURITY_BASELINE.md` — 18-point control matrix with evidence

## Local run

```bash
python3 -m http.server 8790
open http://127.0.0.1:8790          # deck reads public/ directly
```

Regenerate data locally: `pip install feedparser && python scripts/fetch_rss.py && python scripts/fetch_markets.py`

## Honest limits

- Aggregated **public RSS only** — this is OSINT, not verified intelligence.
  Every item carries source + credibility score; government/official sources are
  badged `OFFICIAL`. Item `status` reflects confirmation level from the feed.
- Map is a stylized operational graphic (equirectangular projection), not a
  boundary-accurate cartographic product.
- Markets panel is indicative reference data, delayed.
- Not affiliated with any government or defence entity.
