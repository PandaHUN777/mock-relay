from mockrelay._06 import _01, _04, _05, _06
from mockrelay._09 import _06 as _seq


def _10():
    fixtures = [
        _06(id="a", upstream="u", call_index=0,
            match=_01(method="GET", path="/x"),
            request=_04(method="GET", path="/x"),
            response=_05(status=200)),
        _06(id="b", upstream="u", call_index=1,
            match=_01(method="GET", path="/x"),
            request=_04(method="GET", path="/x"),
            response=_05(status=201)),
    ]
    counter = {}
    r1 = _seq(fixtures, "GET", "/x", {}, None, counter)
    r2 = _seq(fixtures, "GET", "/x", {}, None, counter)
    r3 = _seq(fixtures, "GET", "/x", {}, None, counter)
    assert r1.id == "a"
    assert r2.id == "b"
    assert r3.id == "a"
