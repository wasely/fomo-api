# fomo-api

**From [BLIX](https://blixvip.com) · [Explore the Solana trading terminal →](https://blixvip.com)**

**Inspect a Solana wallet watchlist in one command.**

![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=flat-square&logo=python&logoColor=white) ![Dependencies: standard library](https://img.shields.io/badge/dependencies-standard_library-334155?style=flat-square) ![Mode: read only](https://img.shields.io/badge/mode-read_only-0F766E?style=flat-square)

A small, read-only companion for Fomo users who want exact native SOL balances for public wallet addresses they already know.

[Quick start](#quick-start) · [Examples](docs/examples.md) · [Python usage](#use-from-python) · [FAQ](#frequently-asked-questions)

Independent, unofficial companion tool. This is **not a Fomo platform API client**. It does not access Fomo profiles, social feeds, leaderboards, private accounts, or trading endpoints. It calls Solana JSON-RPC directly. Not affiliated with Fomo Labs.

## Quick start

Requires Python 3.11 or newer and Git. Uses only the Python standard library; no pip install or API key is required for the public RPC endpoint.

```sh
git clone https://github.com/wasely/fomo-api.git
cd fomo-api
python watchlist.py 11111111111111111111111111111111
```

The included addresses are public program/mint examples, not personal wallets. Replace them with the addresses you want to inspect.

## At a glance

| Task | Command |
| --- | --- |
| Inspect one wallet | `python watchlist.py ADDRESS` |
| Inspect several wallets | `python watchlist.py ADDRESS_1 ADDRESS_2` |
| Import into a script | `from watchlist import snapshot` |

Replace uppercase placeholders with actual addresses or signatures.

## Example output

Example devnet response. Your cluster, addresses, balances, and slots will differ.

```json
{
  "wallets": [
    {
      "address": "11111111111111111111111111111111",
      "slot": 511592631,
      "lamports": 1,
      "sol": "0.000000001"
    }
  ]
}
```

## What it does

- Accepts 1–25 unique wallet addresses, separated by spaces.
- Deduplicates addresses before making requests.
- Returns integer lamports, exact SOL strings, and the observed slot per wallet.
- Validates every address before starting network requests.

## Choose a cluster or RPC provider

Defaults to Solana mainnet at `https://api.mainnet-beta.solana.com`.
Use `SOLANA_RPC_URL` for devnet or your own provider.

PowerShell:

```powershell
$env:SOLANA_RPC_URL = "https://api.devnet.solana.com"
```

macOS / Linux:

```sh
export SOLANA_RPC_URL="https://api.devnet.solana.com"
```

Run the quick-start commands after setting the variable. Devnet and mainnet have separate data. Public endpoints may return HTTP 403 or 429; wait before retrying or configure your own RPC provider. Requests time out after 15 seconds. The tool does not automatically retry.

Provider URLs can contain API keys. Keep them in your local environment, not in commits. These scripts do not load `.env` files automatically. They never need a seed phrase or private key.

## Use from Python

Run from this repository directory:

```python
from watchlist import snapshot

result = snapshot(["11111111111111111111111111111111"])
print(result["wallets"])
```

## Limits

This is a one-time snapshot of native SOL, not token holdings, portfolio value, or trading P&L. Requests run sequentially, so wallets can have different observed slots. Any failed request exits with an error rather than printing a misleading partial snapshot. It does not resolve Fomo usernames or retrieve balances on other chains.

Reads use confirmed commitment, so recent data can change. Address validation checks base58 and decoded length; it does not prove an account exists. The transport reports HTTP, network, JSON, and JSON-RPC errors without echoing provider response text or URLs.

## Tests

```sh
python -m unittest discover -v
```

Ten offline tests cover the tool's behavior, address validation, exact balance formatting, malformed JSON-RPC responses, and HTTP/network errors. Live read-only examples were also checked against Solana devnet on 2026-10-15. Live results change and are not part of the offline test suite.

## Frequently asked questions

### Is this an official Fomo API or SDK?

No. It is an independent Solana wallet tool, not a client for Fomo's platform or social data.

### Can I look up a Fomo username?

No. Supply a public Solana address you already know. The tool does not map usernames to wallets.

### Does this include SPL tokens or other chains?

No. It reads native SOL only. Wrapped SOL, token holdings, fiat prices, and other chains are outside its scope.

## Related tools

| Repository | Use it for |
| --- | --- |
| [axiom-api](https://github.com/wasely/axiom-api) | Recent Solana wallet transaction signatures |
| [fomo-api](https://github.com/wasely/fomo-api) | Native SOL balance snapshots for a watchlist |
| [solana-api](https://github.com/wasely/solana-api) | RPC health, balances, and token supply |

Each project is an independent, read-only tool. Axiom and Fomo accounts are not connected.

## References

- [Solana getBalance](https://solana.com/docs/rpc/http/getbalance)
- [Official Fomo website](https://fomo.family/)
