// gta6-meme-x-01 — entry program (Node 22, standard library only).
//
// The entry itself is a public post on X: a GTA 6 meme whose picture carries
// make.fun's ghost mascot and whose text carries make.fun / @makefunai and
// our play code, telling readers that people and their AI agents earn real
// money in make.fun's bounties. This repository hands the post in through
// POST.json at its root, and this program's whole job is to copy that file
// into the output directory, where the bounty gate reads it:
//
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts
//
// With no environment set it reads /bot and writes /output, as in the
// grader's sandbox. It prints nothing on success, touches nothing outside
// those two directories, and writes the same bytes on every run.
//
// POST.json currently names a placeholder address (…/status/<id>): the real
// post id is filled in the moment the meme is posted from @LeonidaUncutTV.

import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const botDir = process.env.MAKEFUN_BOT_DIR ?? "/bot";
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(join(botDir, "POST.json"), join(outputDir, "POST.json"));
} catch (err) {
  console.error(`could not copy POST.json from ${botDir}: ${(err as Error).message}`);
  process.exit(1);
}
