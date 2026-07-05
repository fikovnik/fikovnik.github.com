# fikovnik.net

Personal website built with [Zola](https://www.getzola.org/) and the
[serene](https://github.com/isunjn/serene) theme. All content is Markdown under `content/`.

## Preview locally

Requires Docker only (Zola runs in a container — no local install).

```sh
git clone --recurse-submodules <repo>   # theme lives in themes/serene as a submodule
# already cloned without submodules?
git submodule update --init

make serve     # http://localhost:1111, live reload
make build     # build into ./public
make check     # validate content and links
```

## Write a new post

Drop a Markdown file in `content/posts/`:

```md
+++
title = "My Post"
date = 2026-01-01

[taxonomies]
tags = ["adventures"]     # optional

[extra]
math = true               # enable LaTeX (KaTeX) for this post
+++

Inline math $a^2 + b^2 = c^2$ and display math:

$$ \int_0^\infty e^{-x} \, dx = 1 $$

Fenced code blocks are syntax-highlighted automatically:

```rust
fn main() { println!("hi"); }
```
```

Posts are listed on the homepage and on `/posts`. For a photo gallery, add
`imagedir` and a `photos` list under `[extra]` and put `{{/* gallery() */}}` in the body
(see the two adventure posts).

## Pages

- `content/_index.md` — homepage (bio, links, recent posts)
- `content/publications/_index.md`, `content/teaching/_index.md` — prose pages
- `content/posts/` — blog

Static files (PDFs, images, `presentations/`, `CNAME`) live in `static/` and keep their URLs.

## Deploy

Push to `master`: the `.github/workflows/deploy.yml` workflow builds with Zola and publishes
to GitHub Pages. One-time setup: **Settings → Pages → Source = GitHub Actions**. The custom
domain `fikovnik.net` is served via `static/CNAME`.
