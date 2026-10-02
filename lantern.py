#!/usr/bin/env python3
"""
Lantern prototype server for Z-machine games.

No third-party Python packages are required.

Endpoints:
  GET  /health
  POST /api/session
  GET  /api/session/<session_id>
  POST /api/session/<session_id>/move
  POST /api/replay

The server never accepts an arbitrary executable path from the client.
Games are selected from GAME_FILES below and are executed through dfrotz.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlparse


BASE_DIR = Path(__file__).resolve().parent
GAME_DIR = Path(os.environ.get("LANTERN_GAME_DIR", BASE_DIR / "games")).resolve()
DATA_DIR = Path(os.environ.get("LANTERN_DATA_DIR", BASE_DIR / "lantern-data")).resolve()
SESSION_DIR = DATA_DIR / "sessions"
DFROTZ = os.environ.get("LANTERN_DFROTZ", "dfrotz")

GAME_FILES = {
    "zork1": "zork1-r119-s880429.z3",
    "zork2": "zork2-r63-s860811.z3",
    "zork3": "zork3-r25-s860811.z3",
}

MAX_COMMAND_LENGTH = 200
MAX_MOVES = 5000
DEFAULT_SEED = 1
RUN_TIMEOUT_SECONDS = 20


class LanternError(Exception):
    pass


def now_iso() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def story_path(game: str) -> Path:
    filename = GAME_FILES.get(game)
    if not filename:
        raise LanternError(f"Unknown game: {game}")

    path = (GAME_DIR / filename).resolve()

    if path.parent != GAME_DIR:
        raise LanternError("Invalid game path.")

    if not path.is_file():
        raise LanternError(f"Game file not found: {path}")

    return path


def story_sha256(game: str) -> str:
    h = hashlib.sha256()
    with story_path(game).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def dfrotz_path() -> str:
    resolved = shutil.which(DFROTZ)
    if not resolved:
        raise LanternError(
            f"dfrotz not found. Set LANTERN_DFROTZ or install frotz. Requested: {DFROTZ}"
        )
    return resolved


def clean_moves(moves: list[Any]) -> list[str]:
    if len(moves) > MAX_MOVES:
        raise LanternError(f"Too many moves; maximum is {MAX_MOVES}.")

    cleaned: list[str] = []
    for raw in moves:
        if not isinstance(raw, str):
            raise LanternError("Every move must be a string.")

        move = raw.strip()
        if not move:
            continue
        if len(move) > MAX_COMMAND_LENGTH:
            raise LanternError(
                f"Command is too long; maximum is {MAX_COMMAND_LENGTH} characters."
            )

        cleaned.append(move)

    return cleaned


def run_game(game: str, moves: list[str], seed: int = DEFAULT_SEED) -> dict[str, Any]:
    path = story_path(game)
    cleaned = clean_moves(moves)

    # This deliberately preserves the core behavior of the original Zarkmid PHP:
    # replay the complete command stream through dfrotz from the beginning.
    command_stream = "\n".join(cleaned)
    if command_stream:
        command_stream += "\n"

    started = time.monotonic()
    result = subprocess.run(
        [dfrotz_path(), "-s", str(int(seed)), str(path)],
        input=command_stream,
        text=True,
        capture_output=True,
        timeout=RUN_TIMEOUT_SECONDS,
        cwd=str(GAME_DIR),
        check=False,
    )
    elapsed_ms = round((time.monotonic() - started) * 1000)

    return {
        "game": game,
        "storyFile": path.name,
        "storySha256": story_sha256(game),
        "seed": int(seed),
        "moves": cleaned,
        "moveCount": len(cleaned),
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returnCode": result.returncode,
        "elapsedMs": elapsed_ms,
    }


def session_file(session_id: str) -> Path:
    try:
        parsed = uuid.UUID(session_id)
    except ValueError as exc:
        raise LanternError("Invalid session id.") from exc

    return SESSION_DIR / f"{parsed}.json"


def save_session(session: dict[str, Any]) -> None:
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    path = session_file(session["id"])
    temp = path.with_suffix(".json.tmp")
    temp.write_text(json.dumps(session, indent=2) + "\n", encoding="utf-8")
    temp.replace(path)


def load_session(session_id: str) -> dict[str, Any]:
    path = session_file(session_id)
    if not path.is_file():
        raise LanternError("Session not found.")
    return json.loads(path.read_text(encoding="utf-8"))


def create_session(game: str, seed: int = DEFAULT_SEED) -> dict[str, Any]:
    path = story_path(game)

    session = {
        "version": "lantern.session.v1",
        "id": str(uuid.uuid4()),
        "game": game,
        "storyFile": path.name,
        "storySha256": story_sha256(game),
        "seed": int(seed),
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
        "moves": [],
    }
    save_session(session)
    return session


def add_move(session_id: str, command: str) -> tuple[dict[str, Any], dict[str, Any]]:
    session = load_session(session_id)

    cleaned = clean_moves([command])
    if not cleaned:
        raise LanternError("Command is empty.")

    session["moves"].append(cleaned[0])
    if len(session["moves"]) > MAX_MOVES:
        raise LanternError(f"Too many moves; maximum is {MAX_MOVES}.")

    session["updatedAt"] = now_iso()
    save_session(session)

    result = run_game(session["game"], session["moves"], session["seed"])
    return session, result


class LanternHandler(BaseHTTPRequestHandler):
    server_version = "Lantern/0.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        print(f"[{self.log_date_time_string()}] {fmt % args}")

    def send_cors(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def send_json(self, status: int, data: Any) -> None:
        encoded = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_cors()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_html(self, status: int, html: str) -> None:
        encoded = html.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}

        raw = self.rfile.read(length)
        try:
            value = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LanternError("Request body must be JSON.") from exc

        if not isinstance(value, dict):
            raise LanternError("JSON request body must be an object.")
        return value

    def do_OPTIONS(self) -> None:
        self.send_response(204)
        self.send_cors()
        self.end_headers()

    def do_GET(self) -> None:
        try:
            path = urlparse(self.path).path

            if path == "/":
                if not FRONTEND_FILE.is_file():
                    raise LanternError(f"Frontend file not found: {FRONTEND_FILE}")
                self.send_html(200, FRONTEND_FILE.read_text(encoding="utf-8"))
                return

            if path == "/health":
                games = {}
                for game, filename in GAME_FILES.items():
                    candidate = GAME_DIR / filename
                    games[game] = {
                        "file": filename,
                        "present": candidate.is_file(),
                    }

                self.send_json(
                    200,
                    {
                        "ok": True,
                        "service": "lantern",
                        "dfrotz": shutil.which(DFROTZ),
                        "gameDir": str(GAME_DIR),
                        "games": games,
                    },
                )
                return

            prefix = "/api/session/"
            if path.startswith(prefix):
                session_id = path[len(prefix):]
                session = load_session(session_id)
                self.send_json(200, session)
                return

            self.send_json(404, {"error": "Not found."})
        except LanternError as exc:
            self.send_json(400, {"error": str(exc)})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})

    def do_POST(self) -> None:
        try:
            path = urlparse(self.path).path
            body = self.read_json()

            if path == "/api/session":
                game = str(body.get("game", "zork1"))
                seed = int(body.get("seed", DEFAULT_SEED))
                session = create_session(game, seed)
                initial = run_game(game, [], seed)
                self.send_json(201, {"session": session, "result": initial})
                return

            if path == "/api/replay":
                game = str(body.get("game", "zork1"))
                seed = int(body.get("seed", DEFAULT_SEED))
                moves = body.get("moves", [])
                if not isinstance(moves, list):
                    raise LanternError("moves must be an array.")
                self.send_json(200, run_game(game, moves, seed))
                return

            prefix = "/api/session/"
            suffix = "/move"
            if path.startswith(prefix) and path.endswith(suffix):
                session_id = path[len(prefix):-len(suffix)]
                command = body.get("command", "")
                if not isinstance(command, str):
                    raise LanternError("command must be a string.")

                session, result = add_move(session_id, command)
                self.send_json(200, {"session": session, "result": result})
                return

            self.send_json(404, {"error": "Not found."})
        except LanternError as exc:
            self.send_json(400, {"error": str(exc)})
        except subprocess.TimeoutExpired:
            self.send_json(504, {"error": "dfrotz timed out."})
        except Exception as exc:
            self.send_json(500, {"error": str(exc)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Lantern Z-machine HTTP bridge")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=7788)
    parser.add_argument(
        "--walkthrough",
        help="Replay a newline-delimited walkthrough file and print the dfrotz transcript.",
    )
    parser.add_argument("--game", default="zork1", choices=sorted(GAME_FILES))
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    args = parser.parse_args()

    if args.walkthrough:
        moves = Path(args.walkthrough).read_text(encoding="utf-8").splitlines()
        moves = [
            line.strip()
            for line in moves
            if line.strip() and not line.lstrip().startswith("#")
        ]
        result = run_game(args.game, moves, args.seed)
        print(result["stdout"], end="")
        if result["stderr"]:
            print(result["stderr"], end="", file=os.sys.stderr)
        raise SystemExit(result["returnCode"])

    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((args.host, args.port), LanternHandler)
    print(f"Lantern listening on http://{args.host}:{args.port}")
    print(f"Game directory: {GAME_DIR}")
    print(f"dfrotz: {dfrotz_path()}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Lantern.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
