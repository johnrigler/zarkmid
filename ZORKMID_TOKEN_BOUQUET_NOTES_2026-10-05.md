# Zorkmid Token / Multi-Chain Bouquet Notes
Date: 2026-10-05

## Intent

Create a real Zorkmid economic object, most likely starting with Solana, while preserving the option for a multi-chain "bouquet" rather than pretending that one chain must become canonical for every function.

This is intentionally separate from the Dark Star story. Dark Star may point to it, advertise it, or contextualize why it exists, but the story must not depend on the token.

## First candidate: Solana Zorkmid token

A Solana token is attractive as the first implementation because it gives Zorkmid a recognizable, liquid, low-friction monetary object without requiring the game itself to be rebuilt around Solana.

The game and identity layers should remain separable from the token.

Possible roles:

- optional in-world or cross-world currency;
- rewards or trophies for published game activity;
- payment for artifacts, printed material, services, or events;
- an object referenced by QR codes in Dark Star or Passport;
- a bridge from a player identity into broader crypto use;
- a deliberately small-value teaching asset for learning wallet operations.

Do not force possession of the token in order to play Lantern/Zorkmid.

## Multi-chain bouquet

A bouquet is preferable to a naive "same token everywhere" model.

The bouquet can treat different chains as different media with different strengths rather than pretending they are interchangeable.

Example conceptual bouquet:

- Solana: fungible Zorkmid token and fast inexpensive transfers;
- Polygon/EVM: contract-readable references, Chisel inscriptions, or persistent structured artifacts;
- DigiByte/Litecoin/Ravencoin/eCash: UTXO-side messages, burns, identities, or collectible evidence depending on the chain;
- IPFS: content;
- Chisel/Mogwai: discovery, interpretation, signing, and traversal between these objects.

The bouquet can be represented as one higher-level identity or named object whose constituent chain artifacts are independently verifiable.

## Design constraint

Do not create fake scarcity just because a token exists.

Do not let tokenomics become the purpose of Zorkmid.

A useful rule is:

> Game first. Identity second. Publication third. Money when money actually does something.

The token is valuable to the project only if it makes an existing activity easier, more legible, more portable, or more interesting.

## Open implementation questions

- Is ZORKMID the asset name, ticker, or only the project name?
- Is supply fixed, mintable, burnable, or deliberately trivial?
- Does the token represent money, reputation, access, trophies, or none of those?
- Should published scores or achievements refer to token transfers, or stay ledger-neutral?
- Does a bouquet have one canonical Chisel descriptor that lists its chain components?
- Can a user create their own bouquet under a self-sovereign identity rather than depending on a single project-controlled registry?
- Should testnet/devnet usage be the default educational path before any real-value token is introduced?

No implementation decision is implied by this note.
