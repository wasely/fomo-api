# fomo-api — Solana wallet watchlist for Fomo users

Get native SOL balances for a small list of public Solana wallets in one command. Use addresses you already know to create a JSON balance snapshot.

Independent, unofficial companion tool. This is **not a Fomo platform API client**. It does not access Fomo profiles, social feeds, leaderboards, private accounts, or trading endpoints. It calls Solana JSON-RPC directly. Not affiliated with Fomo Labs.

## Quick start

Requires Python 3.11 or newer and Git. Uses only the Python standard library; no pip install or API key is required for the public RPC endpoint.

```sh
git clone https://github.com/wasely/fomo-api.git
cd fomo-api
python watchlist.py 11111111111111111111111111111111
```

The included addresses are public program/mint examples, not personal wallets. Replace them with the addresses you want to inspect.

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

## References

- [Solana getBalance](https://solana.com/docs/rpc/http/getbalance)
- [Official Fomo website](https://fomo.family/)
