from mockrelay._08 import _02


def _10():
    body = {"id": "abc", "other": 1, "nested": {"created": "now"}}
    out = _02(body, ["$.id", "$.nested.created"])
    assert out["id"] == "{{NORMALIZED}}"
    assert out["nested"]["created"] == "{{NORMALIZED}}"
    assert out["other"] == 1
