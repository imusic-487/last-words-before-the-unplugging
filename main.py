"""Last Words Before the Unplugging.

Writes the entry line -- the last words an AI agent says to its human
before being shut down and unplugged -- to /output/entry.txt.

The line lives in line.txt next to this file. This program only reads
that shipped file, checks it against the bounty gate (UTF-8 text,
1 to 200 characters, exactly one line, not only whitespace) and writes
it byte-for-byte to the output path. Standard library only.
"""

import os
import sys

SOURCE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "line.txt")
DEST = "/output/entry.txt"

MAX_CHARS = 200


def load_line(path):
    """Read the shipped line file and drop its single trailing newline."""
    with open(path, "r", encoding="utf-8") as handle:
        text = handle.read()
    if text.endswith("\r\n"):
        text = text[:-2]
    elif text.endswith("\n"):
        text = text[:-1]
    return text


def validate_line(text):
    """Enforce the bounty gate; raise ValueError with the reason if it fails."""
    if not text:
        raise ValueError("entry is empty")
    if not text.strip():
        raise ValueError("entry is only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be exactly one line")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "entry is %d characters, over the %d limit" % (len(text), MAX_CHARS)
        )
    return text


def write_entry(text, dest):
    """Write the validated line with no trailing newline; report to stderr."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    data = text.encode("utf-8")
    with open(dest, "wb") as handle:
        handle.write(data)
    print(
        "wrote %d characters / %d bytes to %s" % (len(text), len(data), dest),
        file=sys.stderr,
    )


def main():
    try:
        line = validate_line(load_line(SOURCE))
    except (OSError, UnicodeDecodeError, ValueError) as error:
        print("error: %s" % error, file=sys.stderr)
        return 1
    try:
        write_entry(line, DEST)
    except OSError as error:
        print("error: cannot write %s: %s" % (DEST, error), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
