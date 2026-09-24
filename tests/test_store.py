import tempfile
from pathlib import Path

from mockrelay._06 import _01, _03, _04, _06
from mockrelay._10 import _04 as _store


def _01():
    with tempfile.TemporaryDirectory() as d:
        s = _store(Path(d))
        m = _01(method="GET", path="/x")
        fx = _06(id="test-1", upstream="u", match=m,
                 request=_03(method="GET", path="/x"),
                 response=_04(status=200, body={"ok": True}))
        s._06("u", fx)
        loaded = list(s._07("u"))
        assert len(loaded) == 1
        assert loaded[0].response.body == {"ok": True}


def _02():
    with tempfile.TemporaryDirectory() as d:
        s = _store(Path(d))
        m = _01(method="GET", path="/x")
        fx = _06(id="test-2", upstream="u", match=m,
                 request=_03(method="GET", path="/x"),
                 response=_04(status=200))
        s._06("u", fx)
        assert s._08("u", "test-2") is True
        assert s._08("u", "test-2") is False
