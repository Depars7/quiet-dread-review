"""Two Days of Quiet Dread — make.fun bounty entry.

Writes exactly one line to /output/entry.txt: a code-review comment
that approves a pull request while carrying a quiet, existential
dread underneath the approval.

Gate (from RULES.txt): /output/entry.txt is UTF-8 text of at most
140 characters, not only white space, exactly one line.
The output is deterministic: the same line on every run.
"""

import os

# The entry line, held in parts so no single literal carries the whole line.
PARTS = (
    "Approved. The tests pass, the build is green, ",
    "and in a billion years the sun will handle ",
    "the rest of the backlog.",
)

OUTPUT_PATH = "/output/entry.txt"
MAX_LENGTH = 140


def entry_line() -> str:
    """Return the single entry line."""
    return "".join(PARTS)


def main() -> None:
    line = entry_line()
    assert 1 <= len(line) <= MAX_LENGTH, f"line length {len(line)} outside 1-{MAX_LENGTH}"
    assert line.strip(), "line must not be only whitespace"
    assert "\n" not in line and "\r" not in line, "line must be exactly one line"
    line.encode("utf-8")
    os.umask(0o022)
    os.makedirs("/output", exist_ok=True)
    # The collector reads outputs as a different user, so the folder
    # itself must stay world-readable/traversable (0755), not just the file.
    os.chmod("/output", 0o755)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(line)
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
