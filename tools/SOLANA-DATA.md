# Solana token data collector

Run with Python 3 (standard library, no pip dependencies):

```bash
python3 tools/solana_token_dump.py
python3 tools/solana_token_dump.py --pages 5
python3 tools/solana_token_dump.py --token get-money --pages 0
SOLANA_RPC_URL=https://YOUR_RPC_ENDPOINT python3 tools/solana_token_dump.py --pages 20
```

The tool reads the public Solana RPC and DEX Screener API and writes local JSON snapshots under `solana-data/<token>/`. Repeated runs accumulate timestamped `snapshots/`. `latest.json` contains the latest snapshot. Mint-account signature pagination writes `mint_signatures.jsonl` and stores a resume cursor. The `--restart` option clears just those signature files for the selected token, not the market snapshots.

Initial comparison targets:

* Get Money: `7Y8shnrkN9sKySNmUFCVG8FwQk9829ncozJ2AjaEnREV` (confirmed in the user's Solscan image).
* Purple Squirrel: `6z9oBZ84zSx2uPvPofyaAABmBaWUk1BmDkMQryiYorzk` (mint quoted in prior research; reverify before formal analysis).

**Scope:** `getTokenSupply`, `getTokenLargestAccounts` (top 20 *accounts*, not holders), mint account details, DEX Screener current pair snapshots and paid orders, plus signatures referencing the mint account. **It does not collect all swaps, token transfers, historical liquidity, unique wallet holders, or full indexed mint history.** For that, one needs token-account/pool discovery and archival/indexed data sources. Public RPC may rate-limit or prune history. A mint address is not a list of every token transaction. DEX Screener values are observations taken at collection time, not backfilled history.

Do not commit the downloaded data or private RPC API URLs. Add `solana-data/` to local `.gitignore`.

Sources: [Solana RPC](https://solana.com/docs/rpc/http/getsignaturesforaddress), [DEX Screener API](https://docs.dexscreener.com/api/reference).
