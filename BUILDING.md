# Build and extend

## One source of truth

Edit template.html for design/behaviour and the two data JSON files for content. Do not edit dist/index.html directly: it is generated.

build.py renders recipe/attachment data once. It renders a local-asset page in memory and derives the self-contained dist/index.html by embedding exactly those asset bytes as data URLs. dist/index.html is the guide. build.py also writes dist/404.html from template-404.html, which links fonts at absolute /assets/fonts/ paths (a 404 can be served from any URL depth), and copies assets/fonts into dist/assets/fonts. Deploy dist/ at a domain root; hosts such as Cloudflare Pages and Netlify serve 404.html automatically. test.py reverses that embedding and asserts the two renderings are otherwise byte-identical. Build uses only Python's standard library and cached assets, with no network or installation.

## Recipe schema

Each recipes.json item contains:

- id: unique HTML anchor, use lowercase kebab-case.
- title, intro: human-facing recipe name and useful short introduction.
- category: dough, batter, pasta, frozen or everyday.
- requirement: standard, roller or icecream. This controls equipment filtering.
- equipment: actual tools and ordinary kitchen equipment.
- bowl: model-specific bowl recommendation; optional frozen bowl for churning.
- yield: estimated result, without asserting measured output.
- time: honest elapsed time, including resting/chilling; distinguish active mixing.
- ingredients: array of metric ingredient strings.
- steps: complete ordered plain-text method strings.
- cue: visible endpoint; safe temperature when applicable.
- troubleshoot: useful corrective advice.
- sources: array of objects with title and https URL.
- note: formula provenance, scaling/adaptation and caveats.

The schema is not a public API. There is no backend or service endpoint. This is a static webpage; controls operate on pre-rendered HTML.

For new recipes, update count text in template.html and count assumptions in build.py, test.py and any browser tests. IDs must not conflict with section anchors. Preserve safety limits when adapting source recipes. Do not regenerate authored quantities from a source recipe without reviewing every change.

## Attachment schema

Items contain label, title, does, limit and url. The source link supports equipment/operating guidance; current regional stock is not inferred from a live page.

## Images and fonts

assets/manifest.json records image paths, sources, original URLs and credits. The builder reads local bytes. The local-asset rendering uses local font CSS; dist/index.html embeds the font bytes. If changing fonts, update assets/fonts/fonts.css and retain applicable license text under references/font-licenses/.

If replacing an image, use an authorized local image; update credit, source, alt text, width and height in the manifest. Do not rely on a remote URL for rendering. Asset fetching/resizing was a preparation step, not a runtime or rebuild requirement.

## Commands and actual results

```text
$ python3 build.py
Built self-contained online page into dist/index.html.
$ python3 build.py --check
Verified self-contained online page into dist/index.html.
```

Exit status: 0 = pass; build --check exits 1 for stale outputs. Tests and checksum verification exit nonzero on failure. The full captured seventeen-test run is in references/test-results.txt.

## Browser verification

The optional script references/browser-test-script.py needs Playwright and Chromium for developer testing only. It is not required to view, rebuild or verify this bundle. The delivered browser results cover 320/390/768/1440 widths, zero horizontal overflow with drawers closed/open, image loading, all equipment filters, search/no-result/reset, expand/collapse, no-JavaScript drawers and no external runtime requests from the publication page.

For a content update, rebuild, run structural tests and repeat real browser checks at phone and desktop sizes before republishing. Recompute checksums only after validating the intentional edit. See RECREATING.md.
