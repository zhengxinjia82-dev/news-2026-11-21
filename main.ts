import { copyFileSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const src = join(root, "entry 2.png");
const dest = join("/output", "entry.png");

mkdirSync("/output", { recursive: true });
copyFileSync(src, dest);

// Verify the copy landed intact: same byte size as the source image.
const srcBytes = statSync(src).size;
const destBytes = statSync(dest).size;
if (srcBytes !== destBytes) {
  throw new Error(`copy size mismatch: ${srcBytes} vs ${destBytes}`);
}
console.log(`entry 2.png copied to /output/entry.png (${destBytes} bytes)`);
