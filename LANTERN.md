# Lantern prototype

Lantern is the successor experiment to the original Zarkmid PHP wrapper.

The first version deliberately keeps the old Zarkmid execution model: the server stores an ordered move list and replays the complete list through `dfrotz` with a fixed random seed. This keeps the game run reproducible and gives later signing/attestation work a simple object to hash.

## Expected game files

Put the compiled story files in `games/`:

```
games/
  zork1-r119-s880429.z3
  zork2-r63-s860811.z3
  zork3-r25-s860811.z3
```

Frotz must provide `dfrotz` on the server path.

## Egg walkthrough smoke test

The included test walks from the opening of Zork I to the tree, retrieves the jewel-encrusted egg, returns through the kitchen window, reaches the Living Room, and puts the egg in the trophy case.

Run:

```bash
python3 test_lantern.py
```

Or print the raw replay directly:

```bash
python3 lantern.py --game zork1 --seed 1 --walkthrough walkthroughs/zork1-egg.txt
```

## Start the API

```bash
python3 lantern.py
```

Default address:

```
http://127.0.0.1:7788
```

Browser client:

```
http://127.0.0.1:7788/
```

With Apache reverse-proxying `/lantern/` to `127.0.0.1:7788/`:

```
https://rigler.org/lantern/
```

Health check:

```bash
curl http://127.0.0.1:7788/health
```

Create a session:

```bash
curl -X POST http://127.0.0.1:7788/api/session \
  -H 'Content-Type: application/json' \
  -d '{"game":"zork1","seed":1}'
```

Submit a move, replacing SESSION_ID with the returned id:

```bash
curl -X POST http://127.0.0.1:7788/api/session/SESSION_ID/move \
  -H 'Content-Type: application/json' \
  -d '{"command":"north"}'
```

Sessions are stored under:

```
lantern-data/sessions/
```

Each session records the game identifier, exact story filename, SHA-256 of the story file, seed, timestamps, and ordered move list.

## Why replay instead of a persistent dfrotz process?

It matches the original Zarkmid prototype and makes the first Lantern record straightforward:

```
story hash + seed + ordered moves
```

That is enough to reproduce the run with the same game image and interpreter behavior. A later version can add player signatures, hash-chained moves, server attestations, milestones, and token claims without changing the basic record.
