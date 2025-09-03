PROJECT ?= all

.PHONY: install install-viewer install-creator lint lint-viewer lint-creator test test-viewer test-creator build build-viewer build-creator sync-assets dev dev-viewer

install:
ifeq ($(PROJECT),viewer)
	$(MAKE) install-viewer
else ifeq ($(PROJECT),creator)
	$(MAKE) install-creator
else
	$(MAKE) install-viewer
	$(MAKE) install-creator
endif

install-viewer:
	cd viewer/world-viewer && npm ci

install-creator:
	cd creator && uv sync

lint:
ifeq ($(PROJECT),viewer)
	$(MAKE) lint-viewer
else ifeq ($(PROJECT),creator)
	$(MAKE) lint-creator
else
	$(MAKE) lint-viewer
	$(MAKE) lint-creator
endif

lint-viewer:
	cd viewer/world-viewer && npm run lint

lint-creator:
	cd creator && uvx ruff check src/worldbuilder src/tests

test:
ifeq ($(PROJECT),viewer)
	$(MAKE) test-viewer
else ifeq ($(PROJECT),creator)
	$(MAKE) test-creator
else
	$(MAKE) test-viewer
	$(MAKE) test-creator
endif

test-viewer:
	cd viewer/world-viewer && npm test

test-creator:
	cd creator && uvx --with pyyaml --with jinja2 pytest src/tests

build:
ifeq ($(PROJECT),viewer)
	$(MAKE) build-viewer
else ifeq ($(PROJECT),creator)
	$(MAKE) build-creator
else
	$(MAKE) build-creator
	$(MAKE) sync-assets
	$(MAKE) build-viewer
endif

build-viewer:
	cd viewer/world-viewer && npm run build

build-creator:
	cd creator && bash run.sh

sync-assets:
        rm -rf viewer/world-viewer/public/worlds
        mkdir -p viewer/world-viewer/public
        cp -r creator/output/worlds viewer/world-viewer/public/worlds

dev:
ifeq ($(PROJECT),viewer)
	$(MAKE) dev-viewer
else
	$(MAKE) dev-viewer
endif

dev-viewer:
	cd viewer/world-viewer && npm run dev
