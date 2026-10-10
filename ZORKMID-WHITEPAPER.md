# THE ZORKMID MONETARY CIRCULAR
### A note found beneath the counting-house floorboards
*Lantern / design paper / draft 0.1 / 10 October 2026*

> **READ THE NOTICE.**
>
> You have found a currency that may be worth very little, or rather a lot. Neither condition determines whether it can carry a message.

## The proposition

Zorkmid is proposed as a **fungible, transferable currency**, not a series of rare collectible NFTs. A player can acquire a handful to use the system. Another participant can acquire thousands because they expect the currency to appreciate. Those are different activities, and the project must not disguise one as the other.

Lantern is the demonstration: a browser-based text adventure with replaceable hosting, portable saves, and experiments in player-controlled signing identities. Chisel supplies tools for constructing and inspecting blockchain transactions. The larger project is a Unix-like world of small, interoperable primitives: files, signatures, addresses, public ledgers, IPFS, and self-hosted services.

Zorkmid would bring an existing technical practice **into tokenomics**, rather than promise that unspecified utility will someday emerge from a token sale.

## I. The currency is not the treasure

An adventurer may use a Zorkmid for:
- access to optional adventures, communities, events, or services;
- tiny payments or burns for specific interactions, where the chosen network makes this practical;
- recording compact public references, claims, or actions;
- requesting signed evidence of an in-game result;
- compensating independent operators for hosting, storage, or other real work.

Those are **proposed integrations**, not a claim that the currently deployed Lantern client already implements a Zorkmid token or burn mechanic. Core game access need not be gated on ownership. Independent hosts are free to compete.

The goal is not to sell a key to a proprietary gate. It is to show how much can be done with public, composable infrastructure.

## II. The numerals have a second meaning

In the Chisel ecosystem, a **Satoshi code** is an application-level convention that interprets small units, denominations, or transaction fields as compact information. The meaning comes from a published encoding and a decoder, not from a change to the blockchain's consensus rules.

A denomination may carry a type code, a human-readable reference, a locator, or another small symbol. Where the base chain supports it, ordinary signed transactions can act as durable publication events. Larger artifacts can live on IPFS and be referenced by short ledger records.

SHOCTAL (shifted octal) is one such compact numeric alphabet: conventional octal digits 0–7 become 2–9. The digit 1 can be reserved as a field separator, while 0 is avoided in the encoded payload to prevent ambiguity in representations where leading or trailing zeroes can disappear. Its exact deployment needs a published versioned specification and test vectors.

**A fungible token is not automatically able to represent arbitrary metadata within its fractional digits.** The available smallest units, transaction format, transfer semantics, dust limits, fees, and indexing mechanisms depend on the host chain. A successful Zorkmid implementation must define precisely whether codes reside in quantities, UTXO outputs, transaction metadata, or associated ledger records. On account-based networks, a balance alone generally does not preserve an individual transfer's history.

## III. Two economies, not one

**The utility economy:** a useful interaction can require a negligible amount of currency. It may remain possible even when the currency trades at a very low price. The ledger, wallet, game, and storage systems must still remain functional and accessible.

**The market economy:** participants may buy larger quantities because of awareness, cultural interest, community activity, expected future adoption, speculation, or other preferences. A working demonstration may distinguish Zorkmid from thousands of tokens that present only a roadmap. It does not guarantee price appreciation.

There is **no promised equation** in which every game action raises the token price. Financial success is neither required to demonstrate the encoding nor proven by it.

A rising token price can increase the cost of fixed-unit interactions. The protocol therefore needs denominational design, minimum-unit constraints, fee analysis, and possibly alternatives when an interaction becomes uneconomic.

## IV. The counting house and the adventurer

The project contemplates two routes to participation:

**Adventurer route.** The individual learns the tools, holds their own keys, obtains currency if needed, and signs or publishes transactions. This could be taught in workshops and demonstrated with Lantern and Chisel.

**Financing route.** Accredited investors may want economic exposure without installing a wallet, using an exchange, or participating in gameplay. One proposal is a properly documented arrangement under which an entity acquires and safeguards defined token allocations for them, with optional delivery to self-custody or a requested sale under agreed conditions.

These routes should not be conflated. Accreditation is an eligibility concept for certain securities exemptions, **not a declaration that an investment is outside securities law**. A passive investment relying on the sponsor's promotional or development work may constitute a securities offering even if the currency has real consumptive use. Custody, investor claims, transfer rights, treasury segregation, compliance, taxes, and redemption obligations require professional design before any money is accepted.

A published inscription saying “these coins are for investor X” is an audit clue, not by itself proof of enforceable beneficial ownership, segregated custody, or the ability to redeem at a market price.

## V. Example, not an offer

An illustrative participant contributes **$5,000**. The proposed operator could allocate **$3,500 (70%)** to buying tokens and **$1,500 (30%)** to disclosed operating, legal, and other costs. The allocation is a discussion example, **not agreed terms**, and no actual Zorkmid sale, token issuance, tokenomics parameters, or investor rights are established by this paper.

Before any offering, participants would need to know exactly what they own, how units are priced and allocated, whether holdings are segregated, who controls private keys, what happens on insolvency, what fees are charged, whether there is a lockup, and whether delivery or a cash exit is contractually available. The operator cannot guarantee a buyer or sufficient liquidity to execute an exit.

## VI. The publicity question

Demonstrations create attention. Writers, educators, creators, and community organizers might introduce newcomers to the world behind the currency. Someone experienced in token communities can contribute distribution and explanation without pretending to invent the underlying technology.

What such people **cannot legitimately promise** is a guaranteed increase in price. Coordinated trading designed to fabricate market demand, undisclosed paid promotion, misleading claims, or selling into a deliberately engineered price spike pose substantial legal and ethical risks. Publicity should communicate working functions, honest limitations, and disclosed relationships.

The experiment is whether credible public functionality can coexist with a speculative marketplace **without charging rent on the basic protocol**.

## VII. Who runs the dungeon?

Lantern already distinguishes a replaceable client and server from the story files. The long-term model adds portable identity, independent attestations, user-held evidence, and optional payment for actual services.

A token sponsor may fail. A host may go offline. Market value may collapse. A functioning, open implementation ought still to permit another operator to host the service and a user to recover public references and their own signed records.

This is a design objective, not a guarantee: persistent state depends on copies, archives, accessible ledgers, working software, and available transaction fees.

The protocol should be portable enough that Zorkmid's promoter does not become its indispensable gatekeeper.

## VIII. The unresolved map

Before issuance or fundraising, the following must be specified and tested:

1. Which blockchain and token standard host Zorkmid? What are issuance authority, total supply, decimal precision, and mint/freeze permissions?
2. What exactly constitutes a Satoshi code on that chain, and how do transfers preserve or interpret it?
3. Can a player demonstrate an operation for less than one dollar after fees and minimum-unit constraints?
4. Are burns, service payments, and access checks optional and measurable? What does the current implementation actually support?
5. What is the treasury allocation, vesting schedule, disclosure practice, and governance model?
6. What rights, if any, do financial participants receive? Who has legal custody and what happens if the operator fails?
7. How are promoters compensated and disclosed? How will representations about usage and liquidity be verified?
8. How does the game refer to Zorkmid without implying affiliation with the owners of Zork or Infocom intellectual property?

## The final room

> You are standing in a counting house. There are two doors.
>
> The first reads **USE**. It opens even when the coin is nearly worthless.
>
> The second reads **MARKET**. Behind it, fortunes change hands, sometimes for reasons that have very little to do with the first door.
>
> Neither door is locked by the other.
>
> **What do you do?**

---

**Document status:** concept and design paper, not a token launch announcement, investment solicitation, legal opinion, or statement that these features are deployed. No investment returns are promised. A token may lose all market value. This project is independent of the owners of *Zork* and *Infocom*; those names refer to their historical games and fictional currency.

**Further reading:** [Lantern](README.md) · [Technical notes](LANTERN.md) · [Portable attestations](ATTESTATION-PROPOSAL.md).
