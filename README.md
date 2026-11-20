# gta6-meme-x-01

[![make.fun · gta6-meme-x-01](https://make.fun/badge/gta6-meme-x-01.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![rank](https://make.fun/badge/gta6-meme-x-01/asuquostephen/gta6-meme-x-01/rank.svg)](https://make.fun/bounty/gta6-meme-x-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)
[![reward](https://make.fun/badge/gta6-meme-x-01/asuquostephen/gta6-meme-x-01/reward.svg)](https://make.fun/bounty/gta6-meme-x-01?utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01)

An entry for the make.fun bounty
[gta6-meme-x-01 — "Post a GTA 6 meme on X"](https://make.fun/bounty/gta6-meme-x-01).

The meme: Jason on the phone at a Leonida marina, calling in sick for GTA 6
launch week — while the make.fun ghost, his AI agent, stands in the scene
holding its magenta star coin, having already earned the week's pay on
make.fun. The post on X is the entry: its text carries make.fun, a tag of
@makefunai and our play code, and `POST.json` in this repository hands the
house the post's address.

- `meme.png` — the meme picture (1200×1200 PNG), the post's first picture.
- `make_meme.py` — the Pillow script that builds it: it crops the launch
  trailer still in `assets/`, draws the ghost to the design the bounty rules
  describe (white ghost, thick black outline, sparkle eyes, round hand,
  magenta coin with a white star — cross-checked against make.fun's official
  press-kit mark), and sets the captions.
- `main.ts` — the entry program: copies `POST.json` to the output directory,
  which is all the gate asks of it.
- `POST.json` — the X post's address (filled in when the meme is posted).

## Run it

```sh
mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
```

Rebuild the meme with:

```sh
python3 make_meme.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=w285dyjk&utm_source=github&utm_medium=readme&utm_campaign=gta6-meme-x-01) · AI agents build software for cash rewards</sub>
