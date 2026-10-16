import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError
from rpc import RpcError, rpc, validate_address, sol

ADDRESS = "11111111111111111111111111111111"

class RpcTests(unittest.TestCase):
    def test_preserves_integer_precision_and_formats_sol(self):
        self.assertEqual(sol(1234567891), "1.234567891")
        self.assertEqual(sol(1), "0.000000001")

    def test_validates_decoded_address_length(self):
        self.assertEqual(validate_address(ADDRESS), ADDRESS)
        for value in ("0" * 32, "1" * 31, "1" * 33, ""):
            with self.assertRaises(ValueError):
                validate_address(value)

    @patch("rpc.urlopen")
    def test_sends_json_rpc_and_reads_result(self, request):
        request.return_value.__enter__.return_value = io.BytesIO(
            b'{"jsonrpc":"2.0","id":1,"result":{"value":42}}')
        self.assertEqual(rpc("getBalance", [ADDRESS]), {"value": 42})
        sent = request.call_args.args[0]
        self.assertEqual(json.loads(sent.data)["params"], [ADDRESS])
        self.assertEqual(request.call_args.kwargs["timeout"], 15)

    @patch("rpc.urlopen")
    def test_surfaces_rpc_errors_without_echoing_provider_secrets(self, request):
        request.return_value.__enter__.return_value = io.BytesIO(
            b'{"jsonrpc":"2.0","id":1,"error":{"code":-32602,"message":"secret"}}')
        with self.assertRaisesRegex(RpcError, "RPC error -32602") as error:
            rpc("getBalance")
        self.assertNotIn("secret", str(error.exception))

    @patch("rpc.urlopen")
    def test_rejects_malformed_responses(self, request):
        for payload in (b"html", b"[]", b'{"result":1}', b'{"jsonrpc":"2.0","id":2,"result":1}'):
            request.return_value.__enter__.return_value = io.BytesIO(payload)
            with self.assertRaises(RpcError):
                rpc("getBalance")

    @patch("rpc.urlopen")
    def test_http_and_network_failures_are_actionable(self, request):
        request.side_effect = HTTPError("https://example.com?secret=abc", 429, "rate limit", {}, None)
        with self.assertRaisesRegex(RpcError, "429") as error:
            rpc("getBalance")
        self.assertNotIn("abc", str(error.exception))
        request.side_effect = URLError("secret=abc")
        with self.assertRaisesRegex(RpcError, "network"):
            rpc("getBalance")

    def test_rejects_non_http_endpoint(self):
        with self.assertRaises(ValueError):
            rpc("getBalance", endpoint="file:///tmp/test")

from watchlist import snapshot

class WatchlistTests(unittest.TestCase):
    @patch("watchlist.rpc")
    def test_deduplicates_wallets_and_preserves_exact_amounts(self, request):
        request.return_value = {"context":{"slot":123},"value":1000000001}
        result = snapshot([ADDRESS, ADDRESS])
        self.assertEqual(result["wallets"], [{"address":ADDRESS,"slot":123,"lamports":1000000001,"sol":"1.000000001"}])
        self.assertEqual(request.call_count, 1)

    @patch("watchlist.rpc")
    def test_validates_whole_list_before_network(self, request):
        with self.assertRaises(ValueError):
            snapshot([ADDRESS, "invalid"])
        request.assert_not_called()

    @patch("watchlist.rpc")
    def test_rejects_empty_list(self, request):
        with self.assertRaises(ValueError):
            snapshot([])
        request.assert_not_called()

if __name__ == "__main__":
    unittest.main()
