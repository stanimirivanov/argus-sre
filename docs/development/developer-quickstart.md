# Developer quickstart

## TL;DR

- Use Python 3.12 and GNU Make for the documentation foundation.
- Run `make bootstrap` for a new checkout, `make verify` during development,
  and `make validate` before handoff.
- Validation is offline and uses only the Python standard library.
- Runtime dependencies will be added only after the M01 technology decision.

## Current requirements

- Git
- Python 3.12, selected by `.python-version`
- GNU Make 4.3 or newer

On Windows, use a GNU Make distribution that preserves tabbed recipes. CI uses
the same root targets on Windows Server and Ubuntu.

## Verify the checkout

```sh
make bootstrap
make verify
make validate
```

`make bootstrap` reports the toolchain and confirms that the scaffold has no
external packages to install. `make fmt` normalizes supported repository text
files; review its diff before running `make validate` again. `make verify` and
`make validate` are currently equivalent and offline. The distinction preserves
a stable inner-loop/acceptance surface for the selected runtime to extend.

## Constrained environments

If Make is unavailable, the exact underlying checks are:

```sh
python scripts/validate_docs.py
python -m unittest discover -s scripts -p "test_*.py" -v
```

Report the aggregate Make target as not run rather than pretending the direct
commands prove Make compatibility. The CI matrix remains authoritative for the
supported operating systems.

## Runtime evolution

When M01 selects runtime and contract tooling, this guide must document pinned
versions, installation, offline/cache behavior, platform support, configuration,
and troubleshooting. The root `make validate` target remains the aggregate
non-mutating acceptance surface.
