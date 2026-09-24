from mockrelay._06 import _01, _03, _04, _06
from mockrelay._09 import _03 as _match, _05 as _best


def _01():
    m = _01(method="GET", path="/x", query_subset={"a": ["1"]})
    fx = _06(id="1", upstream="u", match=m,
             request=_03(method="GET", path="/x"),
             response=_04(status=200))
    assert _match(fx, "GET", "/x", {"a": ["1"]}, None)
    assert not _match(fx, "GET", "/x", {"a": ["2"]}, None)


def _02():
    fixtures = [
        _06(id="a", upstream="u",
            match=_01(method="GET", path="/x"),
            request=_03(method="GET", path="/x"),
            response=_04(status=200)),
        _06(id="b", upstream="u",
            match=_01(method="GET", path="/x", body_contains={"a": 1}),
            request=_03(method="GET", path="/x"),
            response=_04(status=201)),
    ]
    best = _best(fixtures, "GET", "/x", {}, {"a": 1, "b": 2})
    assert best.id == "b"
