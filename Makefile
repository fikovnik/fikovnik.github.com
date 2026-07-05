# Run Zola through Docker so no local install is needed.
ZOLA_VERSION ?= 0.22.1
ZOLA_IMAGE   := ghcr.io/getzola/zola:v$(ZOLA_VERSION)
DOCKER       := docker run --rm -v "$(CURDIR):/app" -w /app

.PHONY: serve build check clean publications

## publications: regenerate content/publications/_index.md from publications.bib
publications:
	uv run scripts/bib2md.py static/publications/publications.bib content/publications/_index.md

## serve: live preview at http://localhost:1111
serve: publications
	$(DOCKER) -p 1111:1111 $(ZOLA_IMAGE) serve --interface 0.0.0.0 --port 1111 --base-url localhost

## build: build the site into ./public
build: publications
	$(DOCKER) $(ZOLA_IMAGE) build

## check: validate content and links
check:
	$(DOCKER) $(ZOLA_IMAGE) check

## clean: remove build output
clean:
	rm -rf public
