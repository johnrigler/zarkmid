#!/usr/bin/env python3
"""Smoke test for the first Lantern/Zork I walkthrough."""

from pathlib import Path

import lantern


BASE_DIR = Path(__file__).resolve().parent
WALKTHROUGH = BASE_DIR / "walkthroughs" / "zork1-egg.txt"


def load_moves():
    return [
        line.strip()
        for line in WALKTHROUGH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]


def main():
    moves = load_moves()
    result = lantern.run_game("zork1", moves, seed=1)
    transcript = result["stdout"].lower()

    assert result["returnCode"] == 0, (
        f"dfrotz returned {result['returnCode']}\n{result['stderr']}"
    )
    assert "zork i" in transcript, "Zork I title was not found in transcript."
    assert "living room" in transcript, "Walkthrough did not reach the Living Room."
    assert "trophy case" in transcript, "Trophy case was not found in transcript."

    print("PASS: Lantern replayed the Zork I egg walkthrough.")
    print(f"Story SHA-256: {result['storySha256']}")
    print(f"Seed: {result['seed']}")
    print(f"Moves: {result['moveCount']}")
    print(f"Runtime: {result['elapsedMs']} ms")
    print()
    print(result["stdout"])


if __name__ == "__main__":
    main()
