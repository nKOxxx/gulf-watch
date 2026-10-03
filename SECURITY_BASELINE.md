# Gulf Watch 2.0 — Security Baseline

Static-site edition of the 18-point baseline (skill: security-baseline).
Scope: zero-backend public dashboard. Threat model: feed poisoning, XSS via
feed content, supply chain, secret leakage through Actions.

| # | Control | Status | Evidence |
|---|---------|--------|----------|
| 1 | No secrets in repo/code | ✅ | Fetchers are pure RSS + public Yahoo endpoints; zero API keys by design. Gitleaks CI gate (ci.yml). |
| 2 | CI secret scanning (full history) | ✅ | `ci.yml` runs gitleaks on every push/PR. |
| 3 | CSP locked | ✅ | `index.html` meta CSP: `default-src 'self'`; connect-src limited to self + legacy mirror. |
| 4 | XSS: no innerHTML on external data | ✅ | All feed-derived strings rendered via textContent/createElement (index.html renderFeed/renderTicker). |
| 5 | Deny-by-default fetch chain | ✅ | Deck loads committed repo feed first; cross-origin fallback allowlisted to one host; hard failure visible in UI. |
| 6 | Supply chain: zero runtime deps | ✅ | No package.json, no CDN scripts, no frameworks. CI grep gate asserts no external script/style origins. |
| 7 | Actions least privilege | ✅ | update-feed.yml: `contents: write` only, pinned majors (actions/checkout@v4, setup-python@v5), concurrency lock. |
| 8 | Feed poisoning containment | ✅ | Feed data rendered as data (never executed); links `rel="noopener noreferrer"`; titles truncated in UI contexts; credibility + source shown per item. |
| 9 | No PII collected | ✅ | No cookies, no analytics, no forms, no storage writes. |
| 10 | Transport | ✅ | Pages enforces HTTPS; no mixed content (all asset refs relative or self). |
| 11 | Dependency audit (python) | ✅ | Single runtime dep (feedparser) pinned by Actions install; gitleaks + pip-audit style check via ci.yml job. |
| 12 | Generic failure mode | ✅ | Feed failure → visible DEGRADED banner; no stack traces, no partial trust render. |
| 13 | Referrer/privacy | ✅ | No outbound beacons; outbound links are plain anchors to publisher sites. |
| 14 | Clickjacking | ✅ (n/a for Pages) | Pages serves framing headers platform-side; deck has no sensitive actions to protect. |
| 15 | No client-side trust decisions | ✅ | Pure presentation layer; no auth, no privileged ops. |
| 16 | Repo branch protection | ⚠️ platform | Single-maintainer repo; feedbot commits to main by design (data-only). Recommend protecting main for human PRs if repo gains collaborators. |
| 17 | Data classification | ✅ | Public OSINT only; sources credited; no proprietary/gov-derived data. |
| 18 | Verification log | ✅ | This file; CI run URL recorded on first green run. |

## Escalation triggers reviewed
No payments, no health data, no infrastructure control. Geopolitical incident
data is public-aggregator class; mis/disinformation risk mitigated by per-item
source + credibility display and OFFICIAL badging.

## Verification log
- CI run 37040986177 (2026-10-02): gitleaks clean, supply-chain gate pass, deck parse pass, feed schema pass. Pages deploy run 37040985757 green. Prod verified: nkoxxx.github.io/gulf-watch-2.0 200, 68 items, 0 JS errors.
