"""Registry-level tests — fully offline, no network or API keys required."""
import osintkit
from osintkit.core import Source, SourceResult


def test_sources_registered():
    names = {s.name for s in osintkit.all_sources()}
    # a representative spread across indicator kinds
    for expected in ("ipinfo", "hunter", "sanctions", "etherscan", "wikidata", "wigle"):
        assert expected in names
    assert len(names) == 21


def test_every_source_has_metadata():
    for s in osintkit.all_sources():
        assert isinstance(s, Source)
        assert s.name and isinstance(s.name, str)
        assert s.kind in osintkit.kinds()
        assert s.description
        # a keyless source declares no keys; a keyed one declares at least one
        assert s.keyless == (len(s.env_keys) == 0)


def test_get_and_by_kind():
    assert osintkit.get("ipinfo").kind == "ip"
    domain_sources = {s.name for s in osintkit.by_kind("domain")}
    assert {"hunter", "whois_history"} <= domain_sources


def test_keyless_sources_are_configured():
    # sanctions needs no key, so it is always considered configured
    assert osintkit.get("sanctions").configured is True


def test_unknown_source_raises():
    try:
        osintkit.get("does-not-exist")
    except KeyError:
        return
    raise AssertionError("expected KeyError for unknown source")


def test_describe_lists_all():
    text = osintkit.describe()
    for s in osintkit.all_sources():
        assert s.name in text


def test_result_ok_semantics():
    assert SourceResult("x", "i", found=True).ok is True
    assert SourceResult("x", "i", found=False).ok is False
    assert SourceResult("x", "i", found=True, error="boom").ok is False
