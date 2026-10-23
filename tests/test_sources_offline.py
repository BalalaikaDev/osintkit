"""Behavioral tests that exercise real source code without any network call.

Each case hits a guard clause that returns before the source makes an HTTP
request (private IP, malformed input, empty query), so these are deterministic
regardless of which API keys happen to be set in the environment.
"""
import osintkit


async def test_ipinfo_private_ip_is_skipped():
    res = await osintkit.get("ipinfo").fetch("10.0.0.1")
    assert res.ok is False
    assert res.source == "ipinfo"
    assert res.indicator == "10.0.0.1"
    # the underlying dict is preserved unchanged
    assert res.data.get("found") is False


async def test_etherscan_rejects_non_address():
    res = await osintkit.get("etherscan").fetch("definitely-not-an-eth-address")
    assert res.ok is False
    assert "reason" in res.data


async def test_wigle_rejects_empty_query():
    res = await osintkit.get("wigle").fetch("")
    assert res.ok is False
    assert res.data.get("found") is False


async def test_fetch_returns_source_result_shape():
    res = await osintkit.get("ipinfo").fetch("127.0.0.1")
    d = res.to_dict()
    assert set(d) == {"source", "indicator", "found", "error", "data"}
    assert d["source"] == "ipinfo"
