from mockrelay._06 import _01, _04, _05, _06
from mockrelay._09 import _03 as _match, _05 as _best


def test_01():
    m = _01(method="GET", path="/x", query_subset={"a": ["1"]})
    fx = _06(id="1", upstream="u", match=m,
             request=_04(method="GET", path="/x"),
             response=_05(status=200))
    assert _match(fx, "GET", "/x", {"a": ["1"]}, None)
    assert not _match(fx, "GET", "/x", {"a": ["2"]}, None)


def test_02():
    fixtures = [
        _06(id="a", upstream="u",
            match=_01(method="GET", path="/x"),
            request=_04(method="GET", path="/x"),
            response=_05(status=200)),
        _06(id="b", upstream="u",
            match=_01(method="GET", path="/x", body_contains={"a": 1}),
            request=_04(method="GET", path="/x"),
            response=_05(status=201)),
    ]
    best = _best(fixtures, "GET", "/x", {}, {"a": 1, "b": 2})
    assert best.id == "b"
