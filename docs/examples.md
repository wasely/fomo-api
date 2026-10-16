# Create a Solana wallet balance snapshot

## Read one wallet

```sh
python watchlist.py 11111111111111111111111111111111
```

The address above is the Solana System Program, used as a public example. Replace it with a wallet's public address.

## Read a watchlist

```sh
python watchlist.py ADDRESS_1 ADDRESS_2 ADDRESS_3
```

Replace each placeholder with a public Solana address. You can supply up to 25 unique addresses. Duplicates are removed while preserving first-seen order. All addresses are validated before any request starts.

## Save JSON for another tool

```sh
python watchlist.py ADDRESS_1 ADDRESS_2 > balances.local.json
```

`*.local.json` files are ignored by Git. Check the command's exit code before consuming the file: a failed request exits nonzero and produces no successful JSON snapshot.

## Read the values

| Field | Meaning |
| --- | --- |
| `address` | Public Solana address queried |
| `slot` | Slot at which the RPC observed that balance |
| `lamports` | Exact integer native balance; 1 SOL = 1,000,000,000 lamports |
| `sol` | Exact decimal string, avoiding floating-point rounding |

Requests are sequential. This is not an atomic snapshot across all wallets. A change in native balance alone is not evidence of profit or a trade.

[Back to README](../README.md)
