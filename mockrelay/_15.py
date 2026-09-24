from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
from typing import List, Optional

from ._04 import _11 as _01
from ._04 import _14 as _02
from ._04 import _15 as _03
from ._04 import _16 as _04
from ._04 import _17 as _05
from ._04 import _18 as _06
from ._05 import _06 as _07
from ._10 import _04 as _08
from ._11 import _01 as _09
from ._13 import _18 as _10
from ._13 import _30 as _11
from ._14 import _10 as _12
from ._12 import _06 as _13
from ._17 import _02 as _17a


def _14(cfg: _07, store) -> None:
    _01("M O C K R E L A Y", show_brand=True)
    phost, pport = _13(cfg.listen)
    ahost, aport = _13(cfg.admin_listen)
    _04("mode", cfg.mode)
    _04("latency", f"{cfg.latency_ms} ms")
    _04("proxy", f"http://{phost}:{pport}")
    _04("admin", f"http://{ahost}:{aport}")
    _04("fixtures", str(cfg.fixtures_dir.resolve()))
    counts = _17a(store)
    if counts:
        for name, n in counts.items():
            label = "fixture" if n == 1 else "fixtures"
            _04("  " + name, str(n) + " " + label)
    else:
        _04("  (empty)", "no fixtures recorded yet")
    _04("upstreams", ", ".join(cfg.upstreams.keys()) or "(none)")
    print()
    _03("upstream routes")
    rows = [[name, u.base_url, cfg._08(name)] for name, u in cfg.upstreams.items()]
    if rows:
        _05(["name", "base_url", "mode"], rows)
    else:
        _06("warn", "no upstreams defined")
    print()
    _03("try it")
    for name in cfg.upstreams:
        _06("info", f"curl http://{phost}:{pport}/{name}/...")
    _06("info", f"open  http://{ahost}:{aport}  for admin UI")
    print()


def _15(args) -> None:
    cfg = _07._07(Path(args.config))
    if args.mode:
        cfg.mode = args.mode
    if args.latency is not None:
        cfg.latency_ms = args.latency
    store = _08(cfg.fixtures_dir)
    metrics = _09()
    state = _10(cfg, store, metrics)

    _14(cfg, store)

    try:
        proxy_srv = _11(state)
    except OSError as e:
        _06("err", f"proxy bind failed: {e}")
        sys.exit(1)
    try:
        admin_srv = _12(state)
    except OSError as e:
        _06("err", f"admin bind failed: {e}")
        sys.exit(1)

    _06("ok", "serving - Ctrl-C to stop")
    print()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        print()
        _06("info", "shutting down")
        proxy_srv.shutdown()
        admin_srv.shutdown()


def _16(args) -> None:
    args.mode = "record"
    _15(args)


def _17(args) -> None:
    args.mode = "replay"
    if args.latency is None:
        args.latency = 0
    _15(args)


def _18(args) -> None:
    cfg = _07._07(Path(args.config))
    store = _08(cfg.fixtures_dir)
    _01("F I X T U R E S", show_brand=False)
    rows = []
    for f in store._07(args.upstream):
        rows.append([f.upstream, f.match.method, f.match.path,
                     f.response.status, f.id])
    if not rows:
        _06("warn", "no fixtures")
        return
    _05(["upstream", "method", "path", "status", "id"], rows)


def _19(args) -> None:
    path = Path(args.path)
    if path.exists():
        _06("warn", f"refusing to overwrite {path}")
        return
    path.write_text(
        "listen: '127.0.0.1:8080'\n"
        "admin_listen: '127.0.0.1:8081'\n"
        "fixtures_dir: './fixtures'\n"
        "mode: record\n"
        "latency_ms: 0\n"
        "redact_headers: [authorization, cookie, x-api-key]\n"
        "normalize_json_paths: ['$.id', '$.created']\n"
        "upstreams:\n"
        "  gh:\n"
        "    base_url: 'https://api.github.com'\n"
        "    mode: record\n"
    )
    _06("ok", f"wrote {path}")


def _20(args) -> None:
    from ._01 import _09 as s
    from ._02 import _05 as b
    _01("S E T T I N G S", show_brand=False)
    for k, v in sorted(s._08().items()):
        if k == "brand_key":
            v = "***"
        _04(k, repr(v))
    print()
    _01("B R A N D", show_brand=False)
    _04("decoded", b())
    _04("key_env", "SWIVEL_BRAND_KEY")


def _21() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="mockrelay",
        description="Universal local API mock-and-record proxy",
    )
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("serve")
    sp.add_argument("-c", "--config", default="mockrelay.yaml")
    sp.add_argument("-m", "--mode", choices=["record", "replay", "passthrough", "hybrid"])
    sp.add_argument("-l", "--latency", type=int)
    sp.set_defaults(func=_15)

    rp = sub.add_parser("record")
    rp.add_argument("-c", "--config", default="mockrelay.yaml")
    rp.add_argument("-l", "--latency", type=int)
    rp.set_defaults(func=_16)

    rl = sub.add_parser("replay")
    rl.add_argument("-c", "--config", default="mockrelay.yaml")
    rl.add_argument("-l", "--latency", type=int)
    rl.set_defaults(func=_17)

    lp = sub.add_parser("list")
    lp.add_argument("-c", "--config", default="mockrelay.yaml")
    lp.add_argument("-u", "--upstream")
    lp.set_defaults(func=_18)

    ip = sub.add_parser("init")
    ip.add_argument("path", nargs="?", default="mockrelay.yaml")
    ip.set_defaults(func=_19)

    cp = sub.add_parser("config")
    cp.set_defaults(func=_20)

    return p


def _40(argv: Optional[List[str]] = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        argv = ["serve"]
    parser = _21()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)


