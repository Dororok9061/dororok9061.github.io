#!/usr/bin/env python3
import argparse
import re
import time
from pathlib import Path
from urllib.request import Request, urlopen

root = Path(__file__).resolve().parents[2]
text = (root / "src/_data/rfdh_source_index.yml").read_text(encoding="utf-8")
urls = sorted(set(re.findall(r"https://rfdh\.com/[^\"\s]+", text)))
denied = ("/admin", "/member", "/login", "/market", "/qna", "/board", "/bbs")
errors = [url for url in urls if any(part in url.lower() for part in denied)]
parser = argparse.ArgumentParser()
parser.add_argument("--live", action="store_true")
args = parser.parse_args()
if args.live:
    for index, url in enumerate(urls):
        if index:
            time.sleep(1.5)
        try:
            with urlopen(Request(url, headers={"User-Agent": "Dororok9061-RF-link-check/1.0"}), timeout=25) as response:
                if response.status != 200:
                    errors.append(f"{url}: HTTP {response.status}")
        except Exception as exc:
            errors.append(f"{url}: {exc}")
if errors:
    raise SystemExit("\n".join(errors))
print(f"RFDH source links: PASS ({len(urls)} unique HTTPS URLs{' live' if args.live else ' structural'})")
