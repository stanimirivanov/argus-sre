# Developer quickstart

## TL;DR

- Use Python 3.12 and GNU Make for the documentation foundation.
- Run `make doctor`, then `make validate` from the repository root.
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
make doctor
make validate
```

`make fmt` normalizes supported repository text files. Review its diff before
running `make validate` again. No command downloads dependencies or contacts an
external service at this stage.

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
