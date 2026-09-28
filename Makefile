PYTHON ?= python

.PHONY: help doctor fmt fmt-check check test validate

help:
	@echo Argus SRE foundation command surface
	@echo   make doctor     Report the local scaffold toolchain
	@echo   make fmt        Normalize supported text files
	@echo   make fmt-check  Verify repository documentation and policy
	@echo   make check      Run all static repository checks
	@echo   make test       Run validator unit tests
	@echo   make validate   Run the complete non-mutating acceptance suite

doctor:
	@git --version
	@$(PYTHON) --version
	@$(MAKE) --version

fmt:
	$(PYTHON) scripts/validate_docs.py --fix

fmt-check:
	$(PYTHON) scripts/validate_docs.py

check: fmt-check

test:
	$(PYTHON) -m unittest discover -s scripts -p "test_*.py" -v

validate: check test
