# Beyond the Bowl

An independent KitchenAid Artisan KSM195 field guide: 25 metric recipe cards, five cooking chapters, four KSM195 bowl tools, nine optional-attachment guides, operating cautions and source notes. Companion to the Ninety Seconds pizza guide.

## Open it

Extract the whole folder, then open dist/index.html in a modern browser. No install, server, account, internet connection or runtime library is needed. Keep dist/assets beside dist/index.html. Alternatively, dist/page-online.html is one self-contained file with embedded fonts and photos; it can be moved on its own.

Search matches recipe names, descriptions, equipment and ingredients. Equipment filters show 17 standard-tool recipes, two roller-required recipes or six ice-cream-bowl recipes. Egg-free semolina hand shapes do not require a roller. Native recipe drawers still work when JavaScript is disabled. Print / save as PDF opens all recipes for printing and restores the previous view afterward. External reference links naturally require internet; the guide itself does not.

## Recipe chapters

- Dough/pastry: pizza, white tin loaf, focaccia, overnight brioche and shortcrust.
- Batter/baking: cookies, butter cake, pancakes, crêpes, buttercream and baked meringues.
- Pasta: egg sheets/tagliatelle, egg-free semolina hand shapes, ricotta ravioli.
- Frozen: quick four-ingredient churn-and-eat vanilla, three-ingredient no-churn vanilla (no special attachment), vanilla custard, egg-free chocolate, strawberry sorbet, lemon sorbet and pistachio gelato-style ice cream.
- Everyday: whipped cream, butter, mashed potatoes and shredded fully cooked chicken.

These are source-informed recipes and editorial metric adaptations, **not kitchen-tested by this project**. Exact changes are disclosed inside recipe source drawers and research files. Yields and timings are estimates. Do not advertise the formulations as official KitchenAid recipes or as tested without real kitchen validation. The tray pizza is deliberately not the lean, hot-oven Neapolitan dough from Ninety Seconds.

## Safety and compatibility

- Knead yeast dough at speed 2; never faster.
- Model manuals override general guidance. AU heavy-load guidance says 5–6 minutes running, then 20 minutes rest; recipes use at most five minutes per heavy run, including initial mixing. Dough stiffness still matters in a small batch.
- Plan at least 24 hours freezing the ice-cream bowl, chill base to 4°C or below and start the dasher on Stir before adding it. 1.9 L finished capacity is not starting-liquid capacity: official guidance limits starting base to 1.4 L.
- Pasta roller speed and roller thickness dial are different. The documented KSMPRA family uses roller speed 2, fettuccine cutter 5 and spaghetti cutter 7; other models require their own manuals.
- Do not taste raw flour/dough/batter. The mixer does not cook chicken, freeze a warm base, sterilize meat, preserve juice or replace required kitchen appliances.
- This revision is tailored to the Australian Artisan KSM195. Optional-attachment ownership and purchase generation have not been specified. Confirm actual tools, attachment SKU and manual before operating.

## Verify and rebuild

Python 3.9 or newer is needed only for development/verification, not viewing. No Python packages are required.

```sh
python3 verify.py
python3 build.py
python3 build.py --check
python3 test.py
```

Actual captured test output and browser test results are in references/. See BUILDING.md and RECREATING.md for editing and packaging details.

## Files

- template.html: design, layout and client-side controls.
- data/recipes.json: authoritative authored recipe data.
- data/attachments.json: authoritative attachment summaries.
- assets/: cached local images, fonts, font CSS and image provenance.
- build.py: one deterministic builder for both HTML surfaces.
- dist/index.html: offline local-asset output (with dist/assets copied beside it).
- dist/page-online.html: equivalent fully embedded publication output.
- test.py / verify.py / checksums.json: offline structural, equivalence, freshness and byte verification.
- references/: research, primary operating-source snapshots, font licenses and captured tests.

No branding affiliation or endorsement is implied. Images and referenced source text retain their original rights; attribution does not grant a new redistribution/commercial-use license. See SOURCES.md before republishing. The guide is designed and browser-tested at 320, 390, 768 and 1440 px wide.

## KSM195 revision

Tool recommendations and bowl choices are tailored to the Australian Artisan KSM195. Use the supplied pastry beater for shortcrust, mash and cooked chicken, and flex-edge beater for normal creaming/batter work. The model manual excludes Stir/speed 1 for mixing yeast dough: initial mixing and kneading both use speed 2. Hand-wash the supplied whisk. Ingredient formulas remain unchanged and not kitchen-tested. See references/ksm195-revision.md for evidence and changes that supersede the initial generic research.
