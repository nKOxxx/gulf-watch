#!/usr/bin/env python3
"""Adapt v2's Yahoo Finance quotes into the 2.0 deck's markets.json shape."""
import json
import urllib.request
from datetime import datetime, timezone

def fetch_yahoo(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d"
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode('utf-8'))
            result = (data.get('chart') or {}).get('result') or []
            if result:
                meta = result[0].get('meta') or {}
                current = meta.get('regularMarketPrice')
                prev = meta.get('chartPreviousClose')
                if current and prev:
                    return {
                        'price': round(float(current), 2),
                        'chg': round(((float(current) - float(prev)) / float(prev)) * 100, 2),
                    }
    except Exception as e:
        print(f"  ! {symbol}: {e}")
    return None

SYMBOLS = [
    ('BRENT', 'BZ=F'),
    ('TTF GAS', 'NG=F'),
    ('GOLD', 'GC=F'),
    ('BTC', 'BTC-USD'),
]

def main():
    rows = []
    for label, sym in SYMBOLS:
        d = fetch_yahoo(sym)
        if d:
            rows.append({'sym': label, 'price': d['price'], 'chg': d['chg']})
            print(f"  ok {label}: {d['price']} ({d['chg']:+.2f}%)")
        else:
            print(f"  miss {label}")
    out = {
        'generated_at': datetime.now(timezone.utc).isoformat(),
        'rows': rows,
    }
    with open('public/markets.json', 'w') as f:
        json.dump(out, f, indent=2)
    print(f"saved public/markets.json ({len(rows)} rows)")

if __name__ == '__main__':
    main()
