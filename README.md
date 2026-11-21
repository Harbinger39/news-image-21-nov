# Saturday 21 November 2026: COP31 into overtime, missiles over Riyadh, BepiColombo fires for Mercury — and more

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/harbinger39/news-image-21-nov/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/harbinger39/news-image-21-nov/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for make.fun's **"Sum up 21 November's world news in one image"** bounty
($100 pot, closes Mon 23 Nov 2026 01:00 WAT). A dense newspaper front page:
35 stories, 7 regions, all from Saturday 21 November 2026.

## How it is built

- `compose21.py` — the build script (Python 3, Pillow). It draws the whole
  1024×1024 front page in code: masthead, date bar, subdeck, an hour-by-hour
  timeline strip, a six-cell numbers strip (with a small Bitcoin sparkline
  of the 18–21 Nov closes), a region tally, 3 lead cards, 10 pictured cards,
  a dotted world map with pins 1–13, a 22-item ALSO ON list, and a red
  DATE CHECK box. All illustrations are flat scenes drawn with PIL
  primitives. **No photographs.**
- `entry.png` — the finished image the program ships (1024×1024 PNG).
- `main.ts` — the entry program (Node 22, standard library only). It copies
  `entry.png` to `MAKEFUN_OUTPUT_DIR` (or `/output`), so both grader runs
  write byte-identical output.

Run it: `mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts`

## The 13 pictured stories (all verified as 21 November)

| # | Story | Source |
|---|-------|--------|
| 1 | COP31 runs into overtime in Antalya; draft drops fossil fuels | AFP |
| 2 | Three ballistic missiles intercepted over Riyadh, ~02:00 AST | CNA |
| 3 | Kryvyi Rih strike: 2 killed, 58 hurt; 117 of 148 drones downed | Ukrainska Pravda |
| 4 | BepiColombo fires its thrusters for Mercury, 19:24 CET (scheduled) | ESA |
| 5 | Peru M6.7 quake, 00:09 UTC, Junín; no deaths | USGS |
| 6 | Air Niugini PX19 emergency landing in Davao; all 146 safe | AP |
| 7 | Gen Z marches sweep Germany against conscription and cuts | Al Jazeera |
| 8 | India 486/4 at stumps in Wellington; Rahul 136, Gill 98 | NDTV |
| 9 | Zverev v Medvedev semi tonight in Turin (scheduled) | ATP |
| 10 | Freight train derails in Sejong, S. Korea, 05:37; none hurt | Yonhap |
| 11 | Bitcoin below $56,000, lowest in over two years, −9% in a day | CoinGecko |
| 12 | Three Paris officers convicted over the Zecler assault | AFP |
| 13 | Three Salvadoran soldiers killed in an accidental blast, Haiti | N Globe |

ALSO ON (22 more, all Saturday): Rutte to Warsaw; Alcaraz v Shelton semi;
Paris march 2 p.m.; Australia–China AI dialogue; Cyclone Xavier warnings
lifted 00:08 UTC; Hodeidah toll 41; ANC coalition scramble; Verstappen on
pole for the Las Vegas GP; Sativasur miners killed; NYC flu 10th weekly
rise; Bukele registers for a third term; Montreal Santa Claus Parade;
Sydney stabbings; youth strike continues; CAN calls COP31 "the worst COP
ever"; Vanuatu's fossil-fuel warning; COP31's "Colossal Fossil" award;
Australia v England T20; Calgary mayor's talks; São Paulo bus changes;
Vancouver bus shelters; Kusal Mendis on Sri Lanka's woes.

## Date discipline

Every story's date was checked independently against live reporting. The
brief's candidate list was mostly wrong-day and was corrected: the Riyadh
count is **three** missiles (CNA/Arab News/Al Jazeera agree; the "five"
figure was Friday's intercepts), the Kryvyi Rih toll is **2 killed, 58
hurt** (the big Kyiv barrage — 110+ missiles, 3 bridges hit, 8–9 killed —
was Friday night, not Saturday), and the Peru quake is stated at its honest
00:09 UTC time. BepiColombo is framed as scheduled (19:24 CET), never as
completed. The red DATE CHECK box names the stories deliberately left out
because they belong to 19 or 20 November (ICJ Myanmar ruling, Shenzhen
summit, Poland missiles, Kyiv bridges, Akvan landfall, UK–EU deal, Wall
Street slide, Anthropic IPO, GTA VI $3.79bn, Riemann claim, Zelensky
"killer", Palisades verdict, Denmark plot, EU €8bn, Bayer $7.25bn, H5N1
vaccine, Bayelsa boat, FBI hack, Hodeidah strikes, Kenya Ebola, Fiona,
Starc 7/58) — and the pictured list agrees with it.

## Verification

- `entry.png`: valid PNG, exactly 1024×1024, 184,075 bytes (≤ 1,048,576).
- `main.ts` run twice into fresh dirs: byte-identical output.
- Image read back and checked for overflow, garble and overlap; the
  timeline strip was shortened after a first render ran past the right edge.

---

<sub>Entered on [make.fun](https://make.fun/?ref=vvpj4842&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
