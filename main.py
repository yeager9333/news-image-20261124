"""Copy entry.png to the grader's output directory.

Standard library only, no network. Outside the grader's container,
MAKEFUN_OUTPUT_DIR stands in for /output. The copy is checked first: the
source must be a whole PNG or JPEG (the gate reads only those), and the
destination is verified byte for byte after the copy.
"""

import os
import shutil
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"

src = Path(__file__).resolve().parent / "entry.png"
out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
out_dir.mkdir(parents=True, exist_ok=True)
head = src.read_bytes()[:8]
if not (head.startswith(PNG_MAGIC) or head.startswith(JPEG_MAGIC)):
    raise SystemExit("entry.png is neither a PNG nor a JPEG")
dest = out_dir / "entry.png"
shutil.copyfile(src, dest)
if dest.read_bytes() != src.read_bytes():
    raise SystemExit("copy mismatch: destination differs from entry.png")
