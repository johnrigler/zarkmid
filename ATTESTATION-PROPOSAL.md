# Proposal: Portable Chisel Attestations

Status: design suggestion / not yet implemented

## Summary

Lantern should not create or own a separate user identity system. A user should bring an existing Chisel-compatible identity into Lantern, prove control of that identity, and then receive signed attestations from Lantern/rigler.org about verifiable events.

The player can then choose whether to publish those attestations, and can pay the transaction cost themselves on whichever supported ledger they prefer.

This separates four concerns:

1. **Identity** — controlled by the user.
2. **Verification** — performed by Lantern or another attestor.
3. **Attestation** — a portable signed claim.
4. **Publication** — optionally performed by the user through Chisel.

The result is not fundamentally a blockchain game feature. Lantern is a useful deterministic test harness for a more general attestation protocol.

## Trust Model

A useful claim has several distinct cryptographic roles.

### Subject signature

The user proves control of a Chisel identity by signing a challenge.

Example semantic statement:

> I control identity X and am registering it with Lantern for this session.

This should not be treated as proof of an achievement. A user cannot self-attest that they won, completed, verified, or otherwise satisfied an externally meaningful condition.

### Issuer signature

Lantern/rigler.org evaluates the session and signs a claim about the user's identity.

Example semantic statement:

> rigler.org attests that identity X completed Zork I under the conditions described by this attestation.

The attestation key should be a dedicated signing key, separate from payment keys. It may intentionally hold no funds. Compromise of the key would still permit forged attestations, so it remains security-sensitive, but it would not expose treasury funds.

### Ledger signature

The user may then publish the attestation using their own funds.

This transaction proves that the publishing key authorized the ledger transaction. It does **not** make the claim true by itself.

The meaningful verification question remains:

> Does this object contain a valid signature from an issuer I trust?

## Proposed Flow

```text
Chisel identity
      |
      | sign Lantern challenge
      v
verified Lantern registration
      |
      | deterministic session
      v
Lantern result
      |
      | signed by rigler.org attestation key
      v
portable attestation
      |
      +--> keep locally
      +--> store evidence on IPFS
      +--> publish through Chisel
             |
             +--> Digibyte
             +--> Litecoin
             +--> Ravencoin
             +--> Dogecoin
             +--> eCash
             +--> Polygon
             +--> other supported ledgers
```

## Generic Attestation Envelope

Lantern-specific claims should fit inside a reusable Chisel attestation object rather than define an isolated game-only format.

Example:

```json
{
  "type": "chisel.attestation.v1",
  "subject": "subject-identity",
  "issuer": "rigler.org",
  "issuedAt": "2026-10-02T00:00:00Z",

  "claim": {
    "type": "lantern.game-result",
    "game": "zork1",
    "result": "completed",
    "score": 350,
    "moveCount": 287
  },

  "evidence": {
    "storySha256": "...",
    "movesSha256": "...",
    "seed": 1,
    "uri": "ipfs://..."
  },

  "issuerKeyId": "rigler-lantern-2026-01",
  "signature": "..."
}
```

The exact canonical serialization and signature format still need to be chosen.

## Canonical Attestation ID

The attestation should have a ledger-independent identifier derived from its canonical signed representation.

Conceptually:

```text
attestationId = SHA256(canonical signed attestation)
```

The same attestation can then be published on multiple chains without becoming multiple achievements.

```text
               +--> Litecoin
attestation ---+--> Digibyte
               +--> Ravencoin
               +--> Polygon
```

All of those ledger entries point to the same underlying signed claim.

## Evidence and Replay

Lantern is particularly useful as the first attestor because Z-machine sessions are replayable.

A Lantern game attestation can include:

- subject identity
- game identifier
- story file hash
- deterministic seed
- ordered move-list hash
- move count
- final score
- final location
- completion/result state
- evidence CID or URI
- issuer identity
- issuer key ID
- issuer signature

The full move list does not need to be written directly to a blockchain.

A better model is:

```text
IPFS:
  full transcript
  move list
  supporting evidence

Chisel / ledger:
  compact attestation reference
  attestation hash
  subject
  issuer
  claim type
  evidence CID
```

This keeps blockchain publication compact while preserving independently replayable evidence.

## Reputation

Do not collapse attestations into one universal reputation score.

An identity should accumulate signed claims from different issuers.

Example:

```text
Identity X

rigler.org
  - completed Zork I
  - completed Zork II
  - solved Dark Star puzzle

Nerd Coffee
  - document verified in person

Other issuer
  - completed training exercise
```

A viewer decides which issuers matter.

Reputation therefore becomes closer to:

```text
claim + issuer + evidence + history
```

rather than:

```text
user = 87 reputation points
```

Chisel should preserve and index claims, not declare which issuers are trustworthy.

## Issuer Key Management

The attestation signing key should:

- be dedicated to attestations
- not be reused as a payment wallet
- preferably hold no funds
- have a stable public identifier
- support rotation
- include an `issuerKeyId` in every attestation

Example:

```text
issuer: rigler.org
issuerKeyId: rigler-lantern-2026-01
```

If the key is later retired, old attestations remain verifiable against the historical public key.

A separate durable record should map issuer key IDs to public keys and their validity periods.

## Suggested Lantern API Direction

Possible future endpoints:

```text
POST /api/identity/challenge
POST /api/identity/register

GET  /api/session/<id>/attestation
POST /api/session/<id>/attestation
```

Possible flow:

1. Client requests a registration challenge.
2. User signs challenge with Chisel-compatible identity.
3. Lantern verifies signature.
4. Lantern binds verified identity to a session.
5. Session proceeds normally.
6. Lantern evaluates a qualifying event.
7. Lantern creates canonical attestation payload.
8. Lantern signs payload with its issuer key.
9. Client receives signed attestation.
10. User chooses whether and where to publish it.

Actual Chisel publication should remain a separate user action.

## Important Boundary

Being on-chain does not imply truth.

Anyone can publish arbitrary data to a public ledger.

Verification should always distinguish:

- who published the transaction
- who is the subject of the claim
- who issued the attestation
- whether the issuer signature is valid
- whether the verifier trusts that issuer
- whether the evidence can be independently checked

This separation should remain explicit in the UI and data format.

## Generalization Beyond Lantern

Lantern should be treated as the first attestor implementation, not the definition of the protocol.

Possible future attestors include:

- Lantern game results
- Dark Star puzzles or interaction paths
- Nerd Coffee in-person verification
- training/course completion
- document review
- witnessed events
- CertLedger factual-record attestations
- organizational credentials
- device or software attestations

The same envelope should work for all of these.

## Implementation Phases

### Phase 1: Identity proof

Add a Chisel identity connection flow and challenge/response signature verification.

### Phase 2: Session binding

Bind verified subject identity to Lantern sessions.

### Phase 3: Portable signed attestation

Define canonical serialization, issuer key handling, and a signed Lantern result object.

### Phase 4: Evidence packaging

Create deterministic evidence bundles and optionally place large evidence objects on IPFS.

### Phase 5: Chisel publication

Allow the user to take the signed attestation and publish it, at their own expense, to any supported ledger.

### Phase 6: Discovery and reputation

Teach Chisel/Mogwai/Lantern to discover attestations associated with an identity and display them grouped by issuer and claim type.

## Open Questions

- Which signature scheme should be canonical across UTXO and EVM identities?
- Should subject identity be one address, a Chisel identity object, or an address set?
- What exact serialization format should be hashed and signed?
- Should the issuer sign the evidence hash only, the full envelope, or both?
- How should issuer public-key rotation and revocation be represented?
- Which claims merit an attestation automatically versus requiring explicit issuer approval?
- How should privacy-sensitive attestations be handled?
- What minimal subset should be placed directly on-chain versus referenced by CID/hash?

## Design Principle

The identity belongs to the user.

The attestor does not create or own that identity. It only makes a signed statement about it.

The ledger does not make the statement true. It makes the signed statement durable, portable, and discoverable.
