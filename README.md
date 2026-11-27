# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Zaianlpfp/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Zaianlpfp/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

**THE WORLD IN ONE DAY** — one picture that sums up Friday 27 November 2026: a
masthead with the day's date, one hero story and two more big stories. Three
stories, each with its own picture and a short label a viewer can read at a
glance, legible even at ~300px wide.

Stories and sources (Reuters-verified) in [`research.md`](research.md).

**1. New Zealand — COALITION ONE SEAT SHORT (hero).** Final results of the
7 November election, released Friday 27 Nov, leave the ruling centre-right
coalition with 65 of 130 seats — one short of a majority. PM Christopher
Luxon now needs the centrist Opportunity Party to stay in power.
[Reuters](https://www.reuters.com/world/asia-pacific/new-zealands-ruling-coalition-falls-just-short-majority-final-election-count-2026-11-27/)

**2. Australia — SANCTIONS FOR IRAN.** Canberra places counterterrorism
financing sanctions on two people it says carried out antisemitic attacks
for Iran's Revolutionary Guard.
[Reuters](https://www.reuters.com/world/asia-pacific/australia-sanctions-two-people-over-antisemitic-attacks-that-it-blames-iran-2026-11-27/)

**3. Asia — SHARES FIND FOOTING.** Asian stocks steady after a bruising
month: Nikkei +0.7%, Kospi +2%. Tokyo core inflation hits a 16-month high;
the dollar eyes a third monthly gain.
[Reuters](https://www.reuters.com/world/china/global-markets-global-markets-2026-11-27/)

The hero picture is a model-generated illustration of the reported event; the
two lower panels are drawn in code (`compose.py`) along with all text.
Nothing in the picture is presented as a real photograph.

## How to run

```sh
node main.ts
```

`main.ts` does not render anything: it copies the pre-rendered `entry.png` to
`/output` byte for byte. Run it twice and the output is identical. No network.

Verified 27 Nov 2026: two runs into separate scratch dirs both produced
md5 `33fa394d878cbeffdce36a97d7405733`, identical to `entry.png`
(1024×1024 PNG, 521,276 bytes, under the 1 MiB gate). Legibility checked at
full size and at ~300px wide.

To rebuild the image from its sources (not needed at run time):

```sh
python3 compose.py
```

[Enter the bounty](https://make.fun/bounty/news-image-20261127?ref=vdteqqjz)
