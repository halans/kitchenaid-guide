# Re-create the artifacts offline

The source, recipe/attachment data, prebuilt outputs, local images/fonts and key upstream operating snapshots are included. Rebuilding does not need any external source to be available again.

## Fresh extraction

Extract the zip into a new directory. Use Python 3.9+:

```sh
cd kitchenaid-guide
python3 verify.py
```

This checks every recorded file hash, compares generated output to both existing HTML pages, and runs all seventeen standard-library tests.

## Rebuild after intentional edits

```sh
python3 build.py
python3 test.py
```

Review both HTML outputs in modern desktop and phone browsers. Then refresh the manifest using the included script:

```sh
python3 package.py --manifest-only
python3 verify.py
```

The old checksums deliberately fail after a content edit until regenerated. Never refresh them just to conceal an unexplained discrepancy.

## Re-create the zip

```sh
python3 package.py
```

Writes beyond-the-bowl-offline.zip in the parent folder. The zip includes the kitchenaid-guide top-level folder. package.py excludes bytecode, its own checksum manifest from manifest entries, cache folders and existing zip files. It recomputes checksums before packaging. Identical file content and metadata choices produce deterministic zip bytes; changes require a new checksum manifest.

## Publication

Upload page-online.html to a static HTML host or publish it as a webpage artifact. It contains its own fonts and photos, with no external rendering dependencies. index.html must be served alongside its assets. Both files render the same guide and are compared by test.py.

## What cannot be regenerated from upstream

Recipe adaptation decisions, ingredients, descriptions, troubleshooting, category assignment and the HTML design are authored project data. Preserve the JSON and template files. Upstream pages do not contain a ready-to-download version of this guide.

references/upstream/ caches nine primary operating/model references with URL, retrieval date and hashes. Research markdown records the wider recipe sources and critical differences; it is not a full mirror of every linked recipe website. Source links are references, not runtime inputs.
