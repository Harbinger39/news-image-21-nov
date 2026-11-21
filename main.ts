// Entry program for the make.fun news-image-20261121 bounty.
// It ships the finished front page (entry.png, drawn by compose21.py)
// and copies it to the output directory the grader provides.
// Node 22, standard library only; no network, no randomness, so every
// run writes exactly the same bytes.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
