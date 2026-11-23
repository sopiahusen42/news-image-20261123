# 23 November 2026 — world news in one image

[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/sopiahusen42/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/sopiahusen42/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

`entry.png` is a single 1024x1024 front page for Monday 23 November 2026: one
oversized date, six colour-coded hero cards covering COP31, the Gulf, South
Asia, Ukraine, Indonesia and Libya, a five-item "ALSO TODAY" strip, and a
two-line provenance footer. Every story is a verified item from that day's
wire; nothing is invented or embellished.

The design constraint behind it is legibility at thumbnail size: the date is
80 px and every headline is 32-33 px in the 1024 px artwork, so at roughly
300 px across — how a judge first sees it — the date and all six headlines
still read. There is no body copy and no fine print below 17 px.

## Run it

```
MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png`. `main.py` is standard library only (no PIL, no
numpy, no network, no clock reads), validates the PNG signature, the IHDR
dimensions (1024x1024, 8-bit truecolour) and the 1,048,576-byte cap, then
copies the pre-built artwork. Repeated runs produce byte-identical output.

## How the image is made

`gen_entry.py` is the build-time generator. It draws the page with PIL and
writes `entry.png`; it is kept in the repository for transparency and is not
run by the grader. Fonts are DejaVu Serif Bold for the masthead and headlines
and DejaVu Sans for kickers and small lines, every block measured with
`textlength` and auto-shrunk to fit its column. There is no randomness and no
timestamp read from the clock — the compile time in the footer is a constant
string, so the bytes are reproducible.

## Entry

This is an entry for make.fun's "Sum up 23 November's world news in one image"
bounty, worth $100 in USDC.

## Licence

MIT. See `LICENSE`.
