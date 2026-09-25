import hashlib
import json
import tempfile
from pathlib import Path

from mockrelay._06 import _01, _04, _05, _06
from mockrelay._10 import _03 as _id
from mockrelay._10 import _04 as _store


def test_01_id_is_unchanged_for_plain_matches():
    match = _01(method="GET", path="/x", query_subset={"a": ["1"]})
    legacy = hashlib.sha1(json.dumps({
        "u": "u",
        "m": "GET",
        "p": "/x",
        "q": {"a": ["1"]},
        "b": None,
    }, sort_keys=True, default=str).encode()).hexdigest()[:12]
    assert _id("u", match) == legacy


def test_02_id_separates_match_modes():
    plain = _01(method="GET", path="/x")
    fuzzy = _01(method="GET", path="/x", match_mode="fuzzy")
    assert _id("u", plain) != _id("u", fuzzy)


def test_03_spec_round_trip():
    with tempfile.TemporaryDirectory() as d:
        s = _store(Path(d))
        match = _01(method="POST", path="/users/*",
                    query_subset={"p": ["1"]},
                    body_contains={"a": {"$gt": 1}},
                    match_mode="fuzzy", fuzzy_threshold=0.9,
                    ignore_case=True)
        s._06("u", _06(id="f1", upstream="u", match=match,
                       request=_04(method="POST", path="/users/1"),
                       response=_05(status=200)))
        raw = json.loads((Path(d) / "u" / "f1.json").read_text())
        assert raw["match"]["match_mode"] == "fuzzy"
        assert raw["match"]["fuzzy_threshold"] == 0.9
        assert raw["match"]["ignore_case"] is True
        assert "body_contains" in raw["match"]
        back = list(s._07("u"))[0]
        assert back.match.match_mode == "fuzzy"
        assert back.match.fuzzy_threshold == 0.9
        assert back.match.ignore_case is True
        assert back.match.body_contains == {"a": {"$gt": 1}}


def test_04_legacy_fixtures_still_load():
    legacy = {
        "id": "old",
        "upstream": "u",
        "match": {"method": "GET", "path": "/x",
                  "query_subset": {}, "body_contains": None},
        "request": {"method": "GET", "path": "/x", "query": {}, "headers": {}},
        "response": {"status": 200, "headers": {}, "body": None},
    }
    fx = _06._08(legacy)
    assert fx.match.match_mode is None
    assert fx.match.fuzzy_threshold is None
    assert fx._07()["match"] == {"method": "GET", "path": "/x",
                                 "query_subset": {}}
