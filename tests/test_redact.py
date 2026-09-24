from mockrelay._07 import _05, _06


def test_01():
    h = {"Authorization": "Bearer abc", "X-Trace": "keep"}
    out = _05(h, ["authorization"])
    assert out["Authorization"] == "{{SECRET}}"
    assert out["X-Trace"] == "keep"


def test_02():
    assert "sk_{{SECRET}}" in _06("key=sk_test_ABC123")
    assert "ghp_{{SECRET}}" in _06("token=ghp_aaaaaaaaaaaaaaaaaaaa")
