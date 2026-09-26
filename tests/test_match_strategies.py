from mockrelay._06 import _01, _04, _05, _06
from mockrelay._09 import _03 as _match
from mockrelay._09 import _05 as _best
from mockrelay._09 import _06 as _seq
from mockrelay._09 import _07 as Opts
from mockrelay._09 import _12 as scalar
from mockrelay._09 import _14 as body
from mockrelay._09 import _20 as similarity
from mockrelay._09 import _22 as rank
from mockrelay._09 import _23 as resolve
from mockrelay._09 import _25 as smartize
from mockrelay._09 import _26_order as _order
from mockrelay._09 import _28 as strategies
from mockrelay._09 import _29 as build


def _fx(fid: str, path: str, method: str = "GET", **kw):
    return _06(id=fid, upstream="u",
               match=_01(method=method, path=path, **kw),
               request=_04(method=method, path=path),
               response=_05(status=200))


def test_01_exact_is_the_default():
    o = Opts()
    assert scalar("/users/1", "/users/1", o) == 1000
    assert scalar("/users/1", "/users/2", o) is None
    assert _match(_fx("a", "/users/1"), "GET", "/users/1", {}, None, o)


def test_02_wildcard_paths():
    o = Opts()
    assert scalar("/users/*", "/users/1", o)
    assert scalar("/users/*", "/users/abc", o)
    assert scalar("/users/*", "/users/1/posts", o) is None
    assert scalar("/a/**", "/a/b/c/d", o)
    assert scalar("/a/**", "/b/c", o) is None
    assert scalar("/users/?", "/users/1", o) is None
    assert scalar("wildcard:/users/?", "/users/1", o)
    assert scalar("wildcard:/users/?", "/users/12", o) is None
    assert scalar("/users/?", "/users/?", o)
    assert scalar("/users/[0-9]", "/users/7", o)
    assert scalar("/users/[0-9]", "/users/x", o) is None


def test_03_regex_paths():
    o = Opts()
    assert scalar("re:/users/\\d+", "/users/123", o)
    assert scalar("re:/users/\\d+", "/users/abc", o) is None
    assert scalar("regex:^/v\\d+/", "/v2/x", o)
    assert scalar("~/^/v\\d+/", "/v2/x", o)
    assert scalar("re:/[unclosed", "/x", o) is None
    assert scalar("/v\\d+/x", "/v2/x", Opts(mode="regex"))


def test_04_fuzzy_paths():
    assert similarity("/user/1234", "/user/123") > 0.9
    assert similarity("/user/1234", "/user/123") < 1.0
    assert scalar("fuzzy:/user/1234", "/user/123") is not None
    assert scalar("~=/user/1234", "/user/123") is not None
    assert scalar("~=/user/1234", "/nope", Opts()) is None
    assert scalar("~=/user/1234", "/user/12", Opts(threshold=0.99)) is None
    assert scalar("/user/1234", "/user/123", Opts(mode="fuzzy")) is not None


def test_05_auto_never_fuzzy_by_default():
    assert scalar("/user/1234", "/user/123", Opts()) is None
    assert scalar("/user/1234", "/user/123",
                  build({"fuzzy_enabled": True})) is not None


def test_06_auto_keeps_literal_meta_characters():
    o = Opts()
    assert scalar("who?what", "who?what", o) == 1000
    assert scalar("a[0]b", "a[0]b", o) == 1000
    assert scalar("/re:po/x", "/re:po/x", o) == 1000
    assert scalar("2*3", "2*3", o) == 1000


def test_07_path_normalization():
    o = Opts()
    assert scalar("/users", "/users/", o) == 950
    assert scalar("/a//b/", "/a/b", o) == 950
    assert scalar("/Users", "/users", Opts(ignore_case=True)) == 960
    assert scalar("/Users", "/users", o) is None


def test_08_json_operators():
    o = Opts()
    assert body({"age": {"$gt": 5}}, {"age": 10}, o)
    assert not body({"age": {"$gt": 5}}, {"age": 1}, o)
    assert body({"age": {"$gte": 5, "$lte": 5}}, {"age": 5}, o)
    assert body({"s": {"$in": ["x", "y"]}}, {"s": "y"}, o)
    assert not body({"s": {"$nin": ["x", "y"]}}, {"s": "y"}, o)
    assert body({"s": {"$exists": True}}, {"s": "v"}, o)
    assert not body({"s": {"$exists": True}}, {"s": None}, o)
    assert body({"s": {"$exists": False}}, {"other": 1}, o)
    assert body({"n": {"$type": "string"}}, {"n": "5"}, o)
    assert not body({"n": {"$type": "number"}}, {"n": True}, o)
    assert body({"s": {"$contains": "ell"}}, {"s": "hello"}, o)
    assert body({"s": {"$startswith": "he"}}, {"s": "hello"}, o)
    assert body({"s": {"$endswith": "lo"}}, {"s": "hello"}, o)
    assert body({"t": {"$regex": "^sk_"}}, {"t": "sk_live_1"}, o)
    assert body({"t": {"$len": 3}}, {"t": ["a", "b", "c"]}, o)
    assert body({"t": {"$len": {"$gte": 2}}}, {"t": ["a", "b"]}, o)
    assert body({"t": {"$any": [{"$gt": 3}]}}, {"t": [1, 9]}, o)
    assert body({"t": {"$all": [1, 2]}}, {"t": [1, 2, 3]}, o)
    assert not body({"t": {"$all": [1, 9]}}, {"t": [1, 2, 3]}, o)
    assert body({"a": {"$eq": 1}}, {"a": 1}, o)
    assert body({"a": {"$ne": 2}}, {"a": 1}, o)
    assert not body({"a": {"$gt": 1}}, {"a": "9"}, o)


def test_09_json_paths():
    o = Opts()
    doc = {"items": [{"id": 1}, {"id": 2}], "meta": {"page": 1}}
    assert body({"$.items[*].id": 2}, doc, o)
    assert not body({"$.items[*].id": 9}, doc, o)
    assert body({"$.items[0].id": 1}, doc, o)
    assert not body({"$.items[5].id": 1}, doc, o)
    assert body({"$.meta.page": 1}, doc, o)
    assert body({"meta.page": 1}, doc, o)
    assert body({"$.missing": {"$exists": False}}, doc, o)
    assert body({"..id": 2}, doc, o)


def test_10_json_keys_and_values_are_patterns():
    o = Opts()
    assert body({"user_*": 1}, {"user_id": 1}, o)
    assert not body({"user_*": 1}, {"order_id": 1}, o)
    assert body({"*": 1}, {"anything": 1}, o)
    assert body({"name": "Jo*"}, {"name": "John"}, o)
    assert not body({"name": "Jo*"}, {"name": "Jim"}, o)
    assert body({"id": "re:^u_"}, {"id": "u_1"}, o)


def test_11_json_containers():
    o = Opts()
    assert body({"a": [1, 2]}, {"a": [1, 2]}, o)
    assert not body({"a": [1, 2]}, {"a": [2, 1]}, o)
    assert not body({"a": [1, 2]}, {"a": [1]}, o)
    assert body({"a": [{"x": 1}]}, {"a": [{"x": 1, "y": 2}]}, o)
    assert not body({"a": [{"x": 9}]}, {"a": [{"x": 1}]}, o)
    assert not body({"a": 1}, {"a": "1"}, o)
    assert not body({"a": 1}, [1, 2], o)
    assert body({"a": None}, {"a": None}, o)
    assert not body({"a": None}, {"a": 1}, o)


def test_12_nested_and_type_aware():
    o = Opts()
    assert body({"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 1, "d": 2}}}, o)
    assert not body({"a": {"b": {"c": 1}}}, {"a": {"b": {"c": 2}}}, o)
    assert not body({"a": True}, {"a": 1}, o)
    assert body({"a": 1}, {"a": 1.0}, o)


def test_13_query_subset():
    o = Opts()
    f = _fx("a", "/x", query_subset={"page": ["1", "2"]})
    assert _match(f, "GET", "/x", {"page": ["1"]}, None, o)
    assert not _match(f, "GET", "/x", {"page": ["3"]}, None, o)
    assert not _match(f, "GET", "/x", {}, None, o)
    g = _fx("b", "/x", query_subset={"q": ["a*"]})
    assert _match(g, "GET", "/x", {"q": ["abc"]}, None, o)
    h = _fx("c", "/x", query_subset={"p*": ["1"]})
    assert _match(h, "GET", "/x", {"page": ["1"]}, None, o)
    assert _match(_fx("d", "/x"), "GET", "/x", {"any": ["1"]}, None, o)


def test_14_specificity_order():
    o = Opts()
    fixtures = [
        _fx("wild", "/users/*"),
        _fx("fuzz", "fuzzy:/users/1234"),
        _fx("rx", "re:/users/\\d+"),
        _fx("exact", "/users/123"),
    ]
    assert _best(fixtures, "GET", "/users/123", {}, None, o).id == "exact"
    assert _best(fixtures[:3], "GET", "/users/123", {}, None, o).id == "wild"
    assert _best(fixtures[:2], "GET", "/users/123", {}, None, o).id == "wild"


def test_15_specificity_prefers_more_constraints():
    o = Opts()
    fixtures = [
        _fx("loose", "/x"),
        _fx("tight", "/x", body_contains={"a": 1}),
        _fx("q", "/x", query_subset={"p": ["1"]}),
    ]
    assert _best(fixtures, "GET", "/x", {}, {"a": 1}, o).id == "tight"
    assert _best(fixtures[:1] + fixtures[2:], "GET", "/x", {"p": ["1"]},
                 None, o).id == "q"


def test_16_method_gate():
    o = Opts()
    f = _fx("a", "/x", method="POST")
    assert _match(f, "post", "/x", {}, None, o)
    assert not _match(f, "GET", "/x", {}, None, o)


def test_17_spec_overrides():
    strict = Opts(threshold=0.99)
    f = _fx("a", "~=/user/1234")
    assert not _match(f, "GET", "/user/123", {}, None, strict)
    assert _match(f, "GET", "/user/123", {}, None,
                  Opts(threshold=0.9))
    loose = _fx("b", "~=/user/1234", fuzzy_threshold=0.1)
    assert _match(loose, "GET", "/user/123", {}, None, strict)
    tight = _fx("c", "~=/user/1234", fuzzy_threshold=0.94)
    assert _match(tight, "GET", "/user/123", {}, None, Opts(threshold=0.5))
    assert _match(tight, "GET", "/user/123", {}, None, strict)
    ci = _fx("d", "/Users")
    assert not _match(ci, "GET", "/users", {}, None, strict)
    assert _match(ci, "GET", "/users", {}, None,
                  build({"ignore_case": True}))


def test_18_spec_threshold_fallback_and_clamping():
    base = Opts(threshold=0.5)
    assert resolve(base, _fx("a", "/x").match).threshold == 0.5
    assert resolve(base, _fx("b", "/x", fuzzy_threshold="bad").match).threshold == 0.5
    assert resolve(base, _fx("c", "/x", fuzzy_threshold=2).match).threshold == 1.0
    assert resolve(base, _fx("d", "/x", fuzzy_threshold=-1).match).threshold == 0.0


def test_19_build_clamps_bad_values():
    o = build({"match_mode": "nope", "fuzzy_threshold": "bad"})
    assert o.mode == "auto"
    assert o.threshold == 0.86
    assert build({"fuzzy_threshold": 5}).threshold == 1.0
    assert build({"fuzzy_threshold": -1}).threshold == 0.0
    assert build(None).mode == "auto"
    assert build({"match_mode": "fuzzy"}).fuzzy_enabled is True


def test_20_rank_and_probe():
    o = Opts()
    fixtures = [_fx("a", "/x"), _fx("b", "/users/*")]
    rows = rank(fixtures, "GET", "/users/9", {}, None, o)
    assert rows[0]["id"] == "b"
    assert rows[0]["matched"] is True
    assert rows[0]["strategy"] == "wildcard"
    assert rows[0]["score"] > rows[1]["score"]
    assert [c["name"] for c in rows[0]["checks"]] == [
        "method", "path", "query", "body"]
    miss = rank(fixtures, "GET", "/nope", {}, None, o)
    assert all(r["matched"] is False for r in miss)
    assert miss[0]["strategy"] == "miss"
    assert miss[0]["score"] == 0


def test_21_strategies_and_smartize():
    assert strategies() == ("auto", "exact", "wildcard", "regex", "fuzzy")
    assert smartize("/users/123/posts") == "/users/*/posts"
    assert smartize("/t/8f1c2b3a-4c5d-6e7f-8091-a2b3c4d5e6f7") == "/t/*"
    assert smartize("/users/me") == "/users/me"
    assert smartize("") == ""


def test_22_sequential_uses_smart_paths():
    o = Opts()
    fixtures = [
        _06(id="a", upstream="u", call_index=0,
            match=_01(method="GET", path="/users/*"),
            request=_04(method="GET", path="/users/*"),
            response=_05(status=200)),
        _06(id="b", upstream="u",
            match=_01(method="GET", path="/orders/*"),
            request=_04(method="GET", path="/orders/*"),
            response=_05(status=201)),
    ]
    counter = {}
    assert _seq(fixtures, "GET", "/users/1", {}, None, counter, o).id == "a"
    assert _seq(fixtures, "GET", "/users/2", {}, None, counter, o).id == "a"
    assert _seq(fixtures, "GET", "/orders/2", {}, None, counter, o).id == "b"


def test_23_literal_question_mark_is_not_a_wildcard():
    o = Opts()
    pat = "/search?page=2"
    assert scalar(pat, pat, o, "auto") is not None
    assert scalar(pat, "/searchXpage=2", o, "auto") is None


def test_24_order_normalization():
    assert _order(None) == ("path", "body", "query", "literal")
    assert _order([]) == ("path", "body", "query", "literal")
    assert _order(["query", "path"]) == ("query", "path", "body", "literal")
    assert _order("query,path") == ("query", "path", "body", "literal")
    assert _order(["nope", "body"]) == ("body", "path", "query", "literal")
    assert _order(["path", "path"]) == ("path", "body", "query", "literal")
    assert _order(12345) == ("path", "body", "query", "literal")
    assert build({"match_priority": ["query", "path"]}).order == (
        "query", "path", "body", "literal")
    assert build().order == ("path", "body", "query", "literal")


def test_25_query_match_outranks_wildcard_when_ordered():
    fixtures = [
        _fx("wild_q", "/users/*", query_subset={"page": ["1"]}),
        _fx("exact", "/users/7"),
    ]
    q = {"page": ["1"]}
    assert _best(fixtures, "GET", "/users/7", q, None,
                 Opts()).id == "exact"
    assert _best(fixtures, "GET", "/users/7", q, None,
                 Opts(order=_order(["query", "path"]))).id == "wild_q"
    assert build({"match_priority": ["query", "path"]}).order[0] == "query"


def test_26_body_ordered_first():
    fixtures = [
        _fx("plain", "/x"),
        _fx("body", "/x", body_contains={"a": 1}),
    ]
    assert _best(fixtures, "GET", "/x", {}, {"a": 1}, Opts()).id == "body"
    o = Opts(order=("body", "path", "query", "literal"))
    assert _best(fixtures, "GET", "/x", {}, {"a": 1}, o).id == "body"


def test_27_priority_overrides_criteria():
    fixtures = [
        _fx("exact", "/users/7"),
        _fx("pinned", "/users/*", priority=10),
        _fx("sunk", "/users/7", priority=-5),
    ]
    o = Opts()
    assert _best(fixtures, "GET", "/users/7", {}, None, o).id == "pinned"
    assert _best(fixtures[:1] + fixtures[2:], "GET", "/users/7",
                 {}, None, o).id == "exact"
    assert _best(fixtures[1:], "GET", "/users/7", {}, None, o).id == "pinned"


def test_28_priority_round_trips_through_fixtures():
    from mockrelay._06 import _01 as Spec
    from mockrelay._06 import _06 as Fx
    fx = Fx(id="p", upstream="u",
            match=Spec(method="GET", path="/x", priority=3),
            request=_04(method="GET", path="/x"),
            response=_05(status=200))
    raw = fx._07()
    assert raw["match"]["priority"] == 3
    back = Fx._08(raw)
    assert back.match.priority == 3
    assert Fx._08(Fx(id="q", upstream="u",
                     match=Spec(method="GET", path="/x", priority="7"),
                     request=_04(method="GET", path="/x"),
                     response=_05(status=200))._07()).match.priority == 7
    assert Fx._08(Fx(id="r", upstream="u",
                     match=Spec(method="GET", path="/x", priority="nope"),
                     request=_04(method="GET", path="/x"),
                     response=_05(status=200))._07()).match.priority is None
    plain = Fx(id="s", upstream="u", match=Spec(method="GET", path="/x"),
               request=_04(method="GET", path="/x"),
               response=_05(status=200))._07()
    assert "priority" not in plain["match"]


def test_29_priority_differentiates_fixture_ids():
    from mockrelay._10 import _04 as Store
    from mockrelay._06 import _01 as Spec
    a = Spec(method="GET", path="/x")
    b = Spec(method="GET", path="/x", priority=2)
    assert Store._09("u", a) == Store._09("u", Spec(method="GET", path="/x"))
    assert Store._09("u", a) != Store._09("u", b)


def test_30_rank_reports_priority_and_keeps_order():
    fixtures = [
        _fx("wild", "/users/*"),
        _fx("pinned", "/users/*", priority=5),
    ]
    rows = rank(fixtures, "GET", "/users/7", {"page": ["1"]}, None,
                Opts(order=("query", "path")))
    assert rows[0]["id"] == "pinned"
    assert rows[0]["priority"] == 5
    assert rows[1]["priority"] == 0
    assert Opts(order=("query", "path", "body", "literal")).order[0] == "query"
