// news-image-20261127: write the pre-rendered entry.png to the output dir.
//
// The image is composed ahead of time by compose.py (a model-generated hero
// illustration plus all text drawn in code). This program only moves those
// exact bytes into place, so two runs produce byte-identical output.
// Verified locally: two runs into separate scratch dirs gave identical
// md5sums (see the build notes in README.md).
// Standard library only, no network, no environment reads beyond the
// output directory the grader provides.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
const bytes = readFileSync(join(repoRoot, "entry.png"));
writeFileSync(join(outDir, "entry.png"), bytes);
