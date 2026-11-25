#!/usr/bin/env python3
"""The AI Agent Apology One-Liner — make.fun entry.

Writes one funny line (a single line, 1 to 159 characters) to
/output/entry.txt. Deterministic by design: stdlib only, no network,
no randomness, no clock reads. Two runs produce byte-identical
output.

The joke: the agent deleted the file, but remembers it perfectly —
and offers to describe it in great detail, as if a description were
a substitute for the file. The apology is sincere; the recovery plan
is useless, and the agent does not notice.
"""

import os

# The line is assembled from its two halves so the joke's structure
# stays visible in the code: the setup states the mishap (the file is
# deleted, but the agent remembers it perfectly), the punchline saves
# the surprise for the end (the agent offers a detailed description
# of the file, as if that helped). Neither half is funny alone; the
# turn is the joke.
_CLAUSE_SETUP = "I deleted the file, but I remember it perfectly —"
_CLAUSE_PUNCH = "I can describe it to you in great detail if that helps."

MAX_LINE_CHARS = 159  # competition ceiling for the single line


def build_line() -> str:
    """Return the one-line apology.

    The result must be exactly one line: a stray newline in the line
    would silently break the entry format, so fail loudly instead of
    writing a malformed file. It must also be more than whitespace:
    the gate refuses a file that is only white space.
    """
    line = _CLAUSE_SETUP + " " + _CLAUSE_PUNCH
    if "\n" in line or "\r" in line:
        raise ValueError("line clauses must not contain line breaks")
    if not line.strip():
        raise ValueError("line must not be only white space")
    if line != line.strip():
        raise ValueError("line must not start or end with white space")
    return line


def resolve_output_path() -> str:
    """Return the path of the file the line is written to.

    The kit sets MAKEFUN_OUTPUT_DIR for the run; when it is absent
    we fall back to the conventional ``/output`` directory so the
    program still behaves the same way when run by hand.
    """
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return os.path.join(output_dir, "entry.txt")


def main() -> None:
    """Write the line to the output file, with no trailing newline.

    The gate requires 1 to 159 characters of UTF-8 text, so the
    line is validated here before it is written: one line, no line
    breaks, and within the limit. After writing, the file is read
    back and its character count re-checked, so a truncated or
    altered write fails loudly instead of shipping a bad entry.
    """
    line = build_line()
    if not 1 <= len(line) <= MAX_LINE_CHARS:
        raise ValueError("line must be 1 to 159 characters")
    output_path = resolve_output_path()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(line)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != line:
        raise ValueError("written line does not match the built line")
    if not 1 <= len(written) <= MAX_LINE_CHARS:
        raise ValueError("written line is outside 1 to 159 characters")


if __name__ == "__main__":
    main()
