"""The GPS Swears It Was a Shortcut.

Writes the GPS's own one-line excuse for sending the driver down the
wrong road to /output/entry.txt (or $MAKEFUN_OUTPUT_DIR/entry.txt).

The line is the GPS talking: smug, defensive, caught red-handed, and
blaming the map for a shortcut that ends in a lake.
"""

import os
import stat

MAX_CHARS = 200

LINE = (
    "The map promised a shortcut past the wedding and through the "
    "cul-de-sac, and I followed it perfectly - the fact that it ends "
    "in a lake is the map's problem, not mine."
)


def build_excuse() -> str:
    """Return the single-line excuse, validated against the gate."""
    line = LINE.strip()
    if not line:
        raise ValueError("excuse is empty")
    if "\n" in line or "\r" in line:
        raise ValueError("excuse must be a single line")
    if len(line) > MAX_CHARS:
        raise ValueError(f"excuse is {len(line)} chars, over the 200 limit")
    return line


def write_entry(path: str, text: str) -> None:
    """Write the text straight to the final file.

    No temporary file: the grader runs as a different user and must be
    able to read the output, so the file is created directly with mode
    0644 instead of being moved into place from a 0600 temp file.
    """
    data = text.encode("utf-8")
    with open(path, "wb") as handle:
        handle.write(data)
    os.chmod(path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    with open(path, "rb") as handle:
        written = handle.read()
    if written != data:
        raise RuntimeError("entry.txt did not round-trip cleanly")


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    write_entry(os.path.join(out_dir, "entry.txt"), build_excuse())


if __name__ == "__main__":
    main()
