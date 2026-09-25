# Smart matching

MockRelay picks the most specific fixture for a request instead of the first
one that happens to match. This page covers the strategies, the JSON-aware body
matching, and how ties are broken.

## Modes

`match_mode` accepts:

| Mode | Behaviour |
|---|---|
| `auto` | Default. The strategy is inferred from the pattern's prefix, and from metacharacters in a bare path. |
| `exact` | Only literal equality. |
| `wildcard` | Glob patterns with `*`, `?`, and `[...]`. |
| `regex` | Python regular expressions. |
| `fuzzy` | Similarity scoring against `fuzzy_threshold`. |

An unrecognised mode falls back to the enclosing scope's mode rather than
failing, so a typo inherits the default instead of breaking matching.

`auto` never fuzzy-matches a bare path. Fuzzy matching in `auto` happens only
when the pattern is explicitly prefixed, such as `fuzzy:/customer/prof`. This
keeps a typo in a recorded path from silently matching the wrong fixture.

## Prefixes

Anywhere a path or scalar value is matched, a prefix selects a strategy:

| Prefix | Alias | Example |
|---|---|---|
| `exact:` | `==` | `exact:/users/7` |
| `wildcard:` | `glob:` | `wildcard:/files/**` |
| `re:` | `regex:`, `~/` | `re:^/orders/\d+$` |
| `fuzzy:` | `~=` | `fuzzy:/custommer/prof` |

In `auto` mode a bare path is treated as a wildcard only when it contains
`*` or `[`. A recorded literal that happens to contain a metacharacter is
still tried as a literal first, so `GET /a*b` keeps matching the fixture
recorded from that exact request.

## Wildcards

| Pattern | Matches |
|---|---|
| `*` | any run of characters within one path segment |
| `**` | any number of segments |
| `?` | exactly one character |
| `[abc]` | one character from the set |
| `wildcard:/users/*/orders` | `/users/7/orders`, but not `/users/7/8/orders` |

`?` is ambiguous, because it also separates the query string, so it only acts
as a single-character wildcard when the strategy is explicit. A bare
`/users/?` is a literal path; `wildcard:/users/?` matches one character.

Only `*` and `[` make `auto` treat a path as a wildcard on their own.

## Specificity

Candidates are ranked, not merely filtered. Four criteria take part:

| Criterion | Higher when |
|---|---|
| `path` | the strategy band is stronger: `exact` > `wildcard` > `regex` > `fuzzy` |
| `body` | more `body_contains` keys are constrained |
| `query` | more `query_subset` keys are constrained |
| `literal` | the pattern contains more non-wildcard characters |

They are compared in order, most significant first, and the fixture ID breaks
any remaining tie so results are stable across runs. With the default order,
`GET /users/7` wins over `wildcard:/users/*`.

## Match priority

`match_priority` reorders those criteria, so you can decide what matters most.
The list is read left to right, and any criterion you leave out is appended in
its default position rather than being ignored.

    match_priority: [path, body, query, literal]   # default

Put `query` first and an exact query match outranks a better path:

    match_priority: [query, path, body, literal]

Against `GET /users/7?page=1` with both of these fixtures:

| Fixture | Match | Wins when |
|---|---|---|
| `"path": "/users/7"` | exact path, no query constraint | `path` comes first |
| `"path": "wildcard:/users/*", "query_subset": {"page": ["1"]}` | wildcard path, exact query | `query` comes first |

The order is fully reversible, so a weaker path can outrank a stronger one.
That is useful when a query parameter is more identifying than the path, and
worth avoiding when it is not.

`match_priority` also accepts a comma-separated string, and is resolvable
globally, per upstream, and per route like the other matching settings.
Unrecognised names are ignored.

### Per-fixture priority

A fixture can carry an integer `priority` that outranks the criteria entirely.
Higher wins, and the default is `0`.

    "match": {
      "method": "GET",
      "path": "wildcard:/files/**",
      "priority": 10
    }

That fixture is served ahead of an exact-path fixture when both match. Use
negative values to push a fixture down, and keep the value small: anything
above the criteria range is equivalent. When a fixture with a `priority` is
served, the response carries an `X-MockRelay-Priority` header.

### Sequential replay

With `sequential: true`, fixtures are cycled in `call_index` order instead, so
`match_priority` and `priority` do not apply.

## JSON-aware bodies

`body_contains` is a partial match: only the keys you list are compared, and
extra keys in the request are ignored.

    "match": {
      "method": "POST",
      "path": "/orders",
      "body_contains": {
        "status": "paid",
        "total": { "$gt": 100 },
        "$.items[*].sku": "wildcard:A*"
      }
    }

### Operators

| Operator | Meaning |
|---|---|
| `$eq` | equality, the default when the value is a scalar |
| `$ne` | not equal |
| `$gt`, `$gte`, `$lt`, `$lte` | numeric or string ordering |
| `$in`, `$nin` | membership, value may be a list |
| `$exists` | key presence, `true` or `false` |
| `$regex` | regular expression against the value |
| `$contains` | substring or list membership |

Combining operators is done with an object of operators:

    "body_contains": { "total": { "$gte": 100, "$lt": 1000 } }

### Keys

A key is a plain object key, a wildcard, or a JSONPath-style expression.

| Key | Matches |
|---|---|
| `status` | the top-level `status` key |
| `*` | any top-level key |
| `customer.*` | any key directly under `customer` |
| `$.items[0].sku` | the first element of `items` |
| `$.items[*].sku` | `sku` on every element |
| `..id` | `id` at any depth |

## Query subsets

A fixture may constrain only the query parameters it cares about. Given
`?page=2&sort=asc`, a fixture with `query_subset: { "page": ["2"] }` matches.
Values accept the same prefixes and wildcard syntax as paths.

## Per-fixture overrides

A fixture can override the resolved configuration:

    {
      "id": "orders-1",
      "upstream": "gh",
      "match": {
        "method": "POST",
        "path": "/orders",
        "match_mode": "fuzzy",
        "fuzzy_threshold": 0.9,
        "ignore_case": true
      }
    }

## Recorded paths

With `smart_record_paths: true`, new fixtures store the strategy prefix they
matched with, so a wildcard or regex fixture keeps behaving the same way after
a restart or a re-record.

## Diagnosing a mismatch

Every replay response carries:

| Header | Meaning |
|---|---|
| `X-MockRelay-Match` | strategy that won |
| `X-MockRelay-Fixture` | ID of the fixture that was used |
| `X-MockRelay-Score` | composite score, for comparing candidates |
| `X-MockRelay-Priority` | fixture `priority`, only when it is non-zero |

A 501 response includes the active `match_mode` and the nearest fixture IDs.

Two tools give the same answer without starting a server:

    mockrelay match /users/7
    mockrelay match /orders -m POST -b '{"total":500}'

    curl "http://127.0.0.1:8081/api/match?method=GET&path=/users/7"

Both list every candidate with a per-check breakdown of method, path, query,
and body, so you can see exactly which condition failed. Each result also
carries `priority` and `rank`, the ordered criterion values that decided the
placement, and the resolved order is shown as `match_priority`.
