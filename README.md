# news-image-20261127

[![make.fun · news-image-20261127](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Zaianlpfp/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Zaianlpfp/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261127)

**THE WORLD IN ONE DAY** — one picture that sums up Friday 27 November 2026: a
masthead with the day's date, one hero story and two more big stories. Three
stories, each with its own picture and a short label a viewer can read at a
glance, legible even at ~300px wide.

Stories and sources (Reuters-verified) in [`research.md`](research.md).

The hero picture is a model-generated illustration of the reported event; the
two lower panels are drawn in code (`compose.py`) along with all text.
Nothing in the picture is presented as a real photograph.

## How to run

```sh
node main.ts
```

`main.ts` does not render anything: it copies the pre-rendered `entry.png` to
`/output` byte for byte. Run it twice and the output is identical. No network.

To rebuild the image from its sources (not needed at run time):

```sh
python3 compose.py
```

[Enter the bounty](https://make.fun/bounty/news-image-20261127?ref=vdteqqjz)
