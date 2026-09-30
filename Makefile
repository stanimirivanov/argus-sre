PYTHON ?= python

.PHONY: help bootstrap doctor fmt fmt-check docs-check check test verify validate

help:
	@echo Argus SRE foundation command surface
	@echo   make bootstrap  Confirm the dependency-free scaffold toolchain
	@echo   make doctor     Report the local scaffold toolchain
	@echo   make fmt        Normalize supported text files
	@echo   make fmt-check  Verify canonical repository text
	@echo   make docs-check Verify documentation and repository policy
	@echo   make check      Run all static repository checks
	@echo   make test       Run validator unit tests
	@echo   make verify     Run the fast offline development feedback loop
	@echo   make validate   Run the complete non-mutating acceptance suite

bootstrap: doctor
	@echo No external scaffold dependencies require installation.

doctor:
	@git --version
	@$(PYTHON) --version
	@$(MAKE) --version

fmt:
	$(PYTHON) scripts/validate_docs.py --fix

fmt-check:
	$(PYTHON) scripts/validate_docs.py

docs-check: fmt-check

check: docs-check

test:
	$(PYTHON) -m unittest discover -s scripts -p "test_*.py" -v

verify: check test

validate: verify
