import http.client
import json
import tempfile

from mockrelay._05 import _06 as Config
from mockrelay._06 import _01, _04, _05, _06
from mockrelay._10 import _04 as Store
from mockrelay._11 import _01 as Metrics
from mockrelay._13 import _18 as State
from mockrelay._13 import _30 as start
from mockrelay._14 import _10 as start_admin


def _serve(td: str, fixtures, **cfg_kw):
    cfg = Config({
        "listen": "127.0.0.1:0",
        "admin_listen": "127.0.0.1:0",
        "fixtures_dir": td,
        "mode": "replay",
        "upstreams": {"u": {"base_url": "http://127.0.0.1:9"}},
        **cfg_kw,
    })
    store = Store(cfg.fixtures_dir)
    for fx in fixtures:
        store._06("u", fx)
    state = State(cfg, store, Metrics())
    srv = start(state)
    return cfg, srv


def _fx(fid, path, method="GET", body=None, status=200, **kw):
    return _06(id=fid, upstream="u",
               match=_01(method=method, path=path, **kw),
               request=_04(method=method, path=path),
               response=_05(status=status, body=body))


def _req(port, path, method="GET", body=None):
    c = http.client.HTTPConnection("127.0.0.1", port, timeout=5)
    payload = json.dumps(body).encode() if body is not None else None
    headers = {"Content-Type": "application/json"} if payload else {}
    c.request(method, path, payload, headers)
    r = c.getresponse()
    out = (r.status, dict(r.getheaders()), r.read())
    c.close()
    return out


def test_01_wildcard_replay_over_http():
    with tempfile.TemporaryDirectory() as td:
        cfg, srv = _serve(td, [
            _fx("a", "/users/*", body={"ok": True}),
            _fx("b", "/files/**", body={"deep": True}),
        ])
        try:
            port = srv.server_address[1]
            for path in ("/u/users/1", "/u/users/abc"):
                st, hdrs, raw = _req(port, path)
                assert st == 200, path
                assert hdrs["X-MockRelay-Match"] == "wildcard", path
                assert hdrs["X-MockRelay-Fixture"] == "a"
                assert json.loads(raw) == {"ok": True}
            st, hdrs, raw = _req(port, "/u/files/a/b/c")
            assert (st, hdrs["X-MockRelay-Fixture"]) == (200, "b")
            assert json.loads(raw) == {"deep": True}
            for path in ("/u/users/9/posts", "/u/orders/1", "/u/users"):
                st, _, _ = _req(port, path)
                assert st == 501, path
        finally:
            srv.shutdown()


def test_02_regex_and_fuzzy_replay_over_http():
    with tempfile.TemporaryDirectory() as td:
        fixtures = [
            _fx("rx", "re:/users/\\d+", body={"kind": "regex"}),
            _fx("fz", "fuzzy:/customer/1234", body={"kind": "fuzzy"}),
            _fx("lit", "/exact/1", body={"kind": "exact"}),
        ]
        cfg, srv = _serve(td, fixtures)
        try:
            port = srv.server_address[1]
            st, hdrs, raw = _req(port, "/u/users/42")
            assert (st, json.loads(raw)["kind"]) == (200, "regex")
            assert hdrs["X-MockRelay-Match"] == "regex"
            st, hdrs, raw = _req(port, "/u/customer/123")
            assert (st, json.loads(raw)["kind"]) == (200, "fuzzy")
            assert hdrs["X-MockRelay-Match"] == "fuzzy"
            st, hdrs, raw = _req(port, "/u/exact/1")
            assert (st, json.loads(raw)["kind"]) == (200, "exact")
            assert hdrs["X-MockRelay-Match"] == "exact"
        finally:
            srv.shutdown()


def test_03_json_aware_body_replay_over_http():
    with tempfile.TemporaryDirectory() as td:
        match = _01(method="POST", path="/orders",
                    body_contains={"kind": "book", "total": {"$gt": 100}})
        fx = _06(id="j", upstream="u", match=match,
                 request=_04(method="POST", path="/orders"),
                 response=_05(status=201, body={"created": True}))
        cfg, srv = _serve(td, [fx])
        try:
            port = srv.server_address[1]
            st, _, raw = _req(port, "/u/orders", "POST",
                              {"kind": "book", "total": 500})
            assert st == 201
            assert json.loads(raw) == {"created": True}
            st, _, raw = _req(port, "/u/orders", "POST",
                              {"kind": "book", "total": 5})
            assert st == 501
            miss = json.loads(raw)
            assert miss["error"] == "no fixture matched"
            assert miss["nearest"] == ["j"]
        finally:
            srv.shutdown()


def test_04_exact_beats_wildcard_over_http():
    with tempfile.TemporaryDirectory() as td:
        fixtures = [
            _fx("wild", "/users/*", body={"from": "wild"}),
            _fx("exact", "/users/42", body={"from": "exact"}),
        ]
        cfg, srv = _serve(td, fixtures)
        try:
            port = srv.server_address[1]
            st, _, raw = _req(port, "/u/users/42")
            assert (st, json.loads(raw)["from"]) == (200, "exact")
            st, _, raw = _req(port, "/u/users/7")
            assert (st, json.loads(raw)["from"]) == (200, "wild")
        finally:
            srv.shutdown()


def test_05_route_match_mode_override_over_http():
    with tempfile.TemporaryDirectory() as td:
        fx = _fx("fz", "/customer/1234", body={"from": "fuzzy"})
        cfg, srv = _serve(
            td, [fx],
            match_mode="fuzzy",
            upstreams={"u": {"base_url": "http://127.0.0.1:9",
                             "routes": {"/customer": {"match_mode": "exact"}},
                             "match_mode": "fuzzy"}},
        )
        try:
            port = srv.server_address[1]
            assert cfg._12("u", "/customer/123")["match_mode"] == "exact"
            assert cfg._12("u", "/other")["match_mode"] == "fuzzy"
            st, _, _ = _req(port, "/u/customer/123")
            assert st == 501
        finally:
            srv.shutdown()


def test_06_fuzzy_disabled_by_default_over_http():
    with tempfile.TemporaryDirectory() as td:
        cfg, srv = _serve(td, [_fx("fz", "/customer/1234", body={})])
        try:
            port = srv.server_address[1]
            st, _, _ = _req(port, "/u/customer/123")
            assert st == 501
        finally:
            srv.shutdown()


def test_07_no_upstream_still_502():
    with tempfile.TemporaryDirectory() as td:
        cfg, srv = _serve(td, [])
        try:
            port = srv.server_address[1]
            st, _, raw = _req(port, "/nope/x")
            assert st == 502
            assert json.loads(raw)["error"] == "unknown upstream 'nope'"
        finally:
            srv.shutdown()


def test_08_admin_match_api():
    order = _06(id="o", upstream="u",
                match=_01(method="POST", path="/orders",
                          body_contains={"total": {"$gt": 100}}),
                request=_04(method="POST", path="/orders"),
                response=_05(status=201, body={"ok": 1}))
    with tempfile.TemporaryDirectory() as td:
        cfg, proxy = _serve(td, [_fx("a", "/users/*", body={"w": 1}),
                                 _fx("b", "/users/7", body={"w": 0}),
                                 order])
        admin = start_admin(State(cfg, Store(cfg.fixtures_dir), Metrics()))
        try:
            port = admin.server_address[1]
            st, _, raw = _req(port, "/api/match?method=GET&path=%2Fusers%2F7")
            assert st == 200
            out = json.loads(raw)
            assert out["match_mode"] == "auto"
            assert out["results"][0]["id"] == "b"
            assert out["results"][0]["matched"] is True
            assert out["results"][0]["strategy"] == "exact"
            assert out["results"][1]["strategy"] == "wildcard"
            st, _, raw = _req(port, "/api/match?method=GET&path=%2Fnope")
            miss = json.loads(raw)
            assert all(r["matched"] is False for r in miss["results"])
            q = "/api/match?method=POST&path=%2Forders&body="
            st, _, raw = _req(port, q + "%7B%22total%22%3A500%7D")
            assert st == 200, (st, raw)
            hit = json.loads(raw)["results"][0]
            assert hit["id"] == "o" and hit["matched"] is True
            st, _, raw = _req(port, q + "%7B%22total%22%3A5%7D")
            rows = json.loads(raw)["results"]
            low = next(r for r in rows if r["id"] == "o")
            assert low["matched"] is False
            assert [(c["name"], c["ok"]) for c in low["checks"]] == [
                ("method", True), ("path", True), ("query", True),
                ("body", False)]
        finally:
            admin.shutdown()
            proxy.shutdown()


def test_09_match_cli_end_to_end(capsys, tmp_path):
    from argparse import Namespace
    from mockrelay._15 import _22
    store = Store(str(tmp_path))
    for fid, path in (("a", "wildcard:/users/*"),
                      ("b", "/users/7"),
                      ("c", "re:^/orders/\\d+$")):
        store._06("u", _fx(fid, path, body={"from": fid}))
    cfg_path = tmp_path / "mockrelay.yaml"
    cfg_path.write_text(
        "fixtures_dir: '{d}'\nmode: replay\nupstreams:\n  u:\n"
        "    base_url: 'http://127.0.0.1:9'\n".format(
            d=str(tmp_path).replace("\\", "/")))
    _22(Namespace(config=str(cfg_path), method="GET", path="/users/7",
                  query=["page=2"], body=None, upstream="u"))
    out = capsys.readouterr().out
    assert "winner" in out
    assert "exact" in out and "wildcard" in out
    assert out.index("winner") > out.index("exact")


def test_11_query_is_not_part_of_the_path():
    with tempfile.TemporaryDirectory() as td:
        _, srv = _serve(td, [
            _fx("q", "/search", body={"ok": 1}),
            _fx("q2", "/items/*", body={"ok": 2}),
        ])
        try:
            port = srv.server_address[1]
            st, hdrs, raw = _req(port, "/u/search?page=2&sort=asc")
            assert st == 200
            assert hdrs["X-MockRelay-Fixture"] == "q"
            assert json.loads(raw) == {"ok": 1}
            st, _, _ = _req(port, "/u/search")
            assert st == 200
            st, _, _ = _req(port, "/u/other?page=2")
            assert st == 501
            st, hdrs, raw = _req(port, "/u/items/7?page=2")
            assert st == 200
            assert hdrs["X-MockRelay-Match"] == "wildcard"
            assert json.loads(raw) == {"ok": 2}
        finally:
            srv.shutdown()


def test_10_match_options_precedence():
    cfg = Config({
        "match_mode": "exact", "fuzzy_threshold": 0.5,
        "upstreams": {"gh": {
            "base_url": "https://api.github.com",
            "match_mode": "wildcard", "fuzzy_threshold": 0.7,
            "ignore_case": True,
            "routes": {"/v1/search": {
                "match_mode": "fuzzy", "fuzzy_threshold": 0.95,
                "ignore_case": False}}}}})
    assert cfg._12("gh", "/other") == {
        "match_mode": "wildcard", "fuzzy_threshold": 0.7,
        "ignore_case": True, "fuzzy_enabled": False}
    assert cfg._12("gh", "/v1/search/x") == {
        "match_mode": "fuzzy", "fuzzy_threshold": 0.95,
        "ignore_case": False, "fuzzy_enabled": False}
    assert cfg._12("unknown", "/x") == {
        "match_mode": "exact", "fuzzy_threshold": 0.5,
        "ignore_case": False, "fuzzy_enabled": False}
