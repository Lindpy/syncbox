.PHONY: install-uv
install-uv:
	@which uv > /dev/null 2>&1 || (echo "Installing uv..." && curl -LsSf https://astral.sh/uv/0.6.5/install.sh | sh)
	uv pip install --config-settings="--global-option=build_ext" \
	             --config-settings="--global-option=-IC:/Program Files/Graphviz/include/" \
	             --config-settings="--global-option=-LC:/Program Files/Graphviz/lib/" \
	             pygraphviz==1.9
	uv sync --all-extras --python 3.10
	uv run pre-commit install -t pre-push

.PHONY: fastpush
fastpush:
	@git add -A
	@git commit -m "$(m)"
	@git push

.PHONY: format
format:
	ruff format
	
.PHONY: lint
lint:
	ruff check 
	ruff format --check 

.PHONY: mypy
mypy:
	mypy 

.PHONY: test
test:
	pytest

.PHONY: all
all: lint mypy test


.PHONY: clean
clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]'`
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*~'`
	rm -f `find . -type f -name '.*~'`
	rm -f `find . -type f -name '.*DS_Store'`
	find . -type d -name ".benchmarks" -exec rm -rf {} +
	rm -rf .cache
	rm -rf .*_cache
	rm -rf *.egg-info
	rm -rf .eggs
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf public
	rm -rf .plots
	rm -rf .hypothesis
	rm -rf .profiling
	rm -rf .ropeproject
