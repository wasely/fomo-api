"""Snapshot SOL balances for a small watchlist of public Solana addresses."""
import argparse
import json
from rpc import RpcError, rpc, sol, validate_address


def snapshot(addresses):
    addresses = list(dict.fromkeys(addresses))
    if not 1 <= len(addresses) <= 25:
        raise ValueError("Provide between 1 and 25 unique wallet addresses.")
    for address in addresses:
        validate_address(address)
    wallets = []
    for address in addresses:
        result = rpc("getBalance", [address, {"commitment": "confirmed"}])
        wallets.append({"address": address, "slot": result["context"]["slot"],
                        "lamports": result["value"], "sol": sol(result["value"])})
    return {"wallets": wallets}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("addresses", nargs="+", help="Public Solana wallet addresses")
    args = parser.parse_args()
    try:
        print(json.dumps(snapshot(args.addresses), indent=2))
    except (ValueError, RpcError) as exc:
        parser.exit(1, f"Error: {exc}\n")


if __name__ == "__main__":
    main()
