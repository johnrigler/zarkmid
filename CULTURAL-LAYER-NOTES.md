# ZarkMid / Lantern Cultural Layer Notes

## Lantern should stay thin

Lantern is the execution layer for interactive fiction. Its job is to make games such as Zork playable through a clean browser interface, preserve deterministic session state, and expose a small set of useful controls such as movement, LOOK, INVENTORY, save, and load.

Lantern should not gradually become a giant fan site, archive, encyclopedia, or editorial publication. Those things can surround Lantern without being fused into the game client.

## Handmade maps

For games with established cultural weight, especially Zork, a handmade map is preferable to building an elaborate live automapper.

The topology of Zork is not reliably Euclidean. NORTH does not guarantee SOUTH is the inverse path, one-way passages exist, and maze geometry can be intentionally deceptive. A hand-authored map can represent those oddities directly instead of pretending that the world is a simple Cartesian grid.

Maps can be:
- published as separate artifacts;
- included in a periodical such as Dark Star;
- linked from ledger-addressable entries;
- incomplete, stylized, annotated, or issue-specific;
- treated as human interpretation rather than generated telemetry.

Lantern can still expose the player's current room and ordered moves, but it does not need to solve mapping automatically.

## Zork as an addressable cultural node

The broader goal is not merely "Zork in a browser." A Zork entry can become a durable cultural node that points outward to the ecosystem around the game:

- Lantern launch point
- handmade maps
- walkthroughs
- Infocom history
- manuals and packaging where distribution rights permit
- interpreters and preservation tools
- interactive-fiction mapping projects
- fan scholarship and essays
- related games and artifacts

The surrounding ledger/index layer should point to the authentic object and then to the culture that accumulated around it.

## Populate Web3 with authentic artifacts

One objective is to give Web3 address space things worth visiting that are not primarily financial instruments or algorithmic commentary.

Older games, music videos, early-web artifacts, Vine-era material, zines, maps, manuals, and other culturally dense objects are useful because they already have history and meaning. The system does not need to manufacture importance for them. It can provide durable identity, discovery, provenance, and linkage.

This suggests a separation of responsibilities:

- **Lantern** — execution and interaction
- **Chisel** — identity, signing, publication, ledger writing
- **Mogwai** — discovery and presentation
- **Dark Star** — editorial and cultural framing
- **Ledger** — durable address space

## Chisel boundary

A Lantern session can be exported as a deterministic artifact containing the game, story hash, seed, ordered moves, and relevant metadata. Chisel can then sign or publish that artifact when the user explicitly chooses to do so.

Server-side signing may exist later as a separate Node.js service for workflows requiring a server identity or attestation. Normal Lantern gameplay should not require a blockchain private key on the game server.
