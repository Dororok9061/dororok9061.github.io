# PaperBanana Academic Figure Workflow

## Current execution status

The workflow and source-controlled prompts are implemented, but **no image in the
public site is currently claimed as a PaperBanana model output**. The present
`start-here-domain-map.svg` and `start-here-methodology.svg` files are original,
source-faithful vector redraws committed so that the portfolio has visible
figures before a generation model is configured.

Running the PaperBanana Visualizer requires a locally configured image-generation
provider and credential. Those credentials are not stored in this repository.
A future generated PNG/WebP may replace a vector redraw only after the candidate,
critic notes, source comparison, and metadata scan have been retained.

This portfolio uses a two-stage visual strategy:

1. **Immediate web visual** — source-faithful HTML/CSS flow, SVG figures, and concept diagrams generated from the structured Jekyll data. These render without an external model and never invent measurements.
2. **Publication-style replacement** — high-resolution figures generated with PaperBanana from the prompts in `docs/paperbanana_figures.yml`, then reviewed against the source before publication.

Reference implementation: <https://github.com/dwzhu-pku/PaperBanana>

## Why PaperBanana is used here

PaperBanana is designed for academic illustration generation using a Retriever → Planner → Stylist → Visualizer → Critic pipeline. Its interactive workflows accept method text and a figure caption, which maps well to the structured `problem`, `architecture`, `methods`, `results`, and course/topic data already used by this Jekyll portfolio.

## Safety and source rule

A generated figure may reorganize or redraw supported information, but it must not create:

- measurements that do not exist in the source;
- model accuracy, timing, RF performance, PPA, or clinical claims not present in the source;
- hardware that was not used;
- fabricated experiment screenshots;
- CES Innovation Awards results or product certifications that have not been publicly announced.

Every generated figure is compared with the page source before it replaces the built-in vector summary.

## Local setup

Follow the upstream PaperBanana README. A typical local setup is:

```powershell
git clone https://github.com/dwzhu-pku/PaperBanana.git D:\Tools\PaperBanana
Set-Location D:\Tools\PaperBanana
uv venv
.\.venv\Scripts\Activate.ps1
uv python install 3.12
uv pip install -r requirements.txt
```

Copy the upstream configuration template to the ignored runtime configuration file, or use environment variables. **Never commit API keys or `model_config.yaml`.**

## Generation input

For each item in `docs/paperbanana_figures.yml`:

1. Read `source` and the linked public/source page.
2. Copy the manifest `prompt` into PaperBanana's method-content input.
3. Use `caption_ko` or `caption_en` as the figure caption/communicative intent.
4. Generate several candidates with the full or planner+critic pipeline.
5. Retain candidate identifiers and critic feedback.
6. Compare labels, arrows, stages, component names, and every number with the source.
7. Refine only the candidate that remains source-faithful.
8. Export the final PNG to the exact `output` path from the manifest.
9. Add a WebP derivative and update the related page/gallery metadata.
10. Record the model/provider, generation date, source hash, candidate, and review decision.

## Recommended visual hierarchy

- **Architecture / methodology diagrams:** 16:9 or 4:3, 2K minimum.
- **Compact paper figures:** 4:3 or square where appropriate.
- **Website hero/case-study figures:** 16:9.
- **Do not rasterize text-heavy diagrams at low resolution.**

## Review checklist

Before publishing a PaperBanana output:

- [ ] Every node and label exists in the source material.
- [ ] Every numeric value matches a cited/linked source.
- [ ] No new hardware, sensor, dataset, participant, or result was invented.
- [ ] Arrows preserve the actual data/control flow.
- [ ] Korean/English terminology is consistent with the page.
- [ ] Text is readable at 390 px mobile width.
- [ ] PNG/WebP contain no private metadata.
- [ ] Candidate and critic records are retained.
- [ ] The generated image is labeled as an explanatory/redrawn figure when it is not a direct experiment capture.

## Current backlog

The source-controlled backlog lives in:

`docs/paperbanana_figures.yml`

It currently covers representative figures for FMCW radar cardiac timing, PPG-HRV, FPGA delay verification, drowsiness monitoring, RF/Smith-chart study, STM32, PADS, and motor control. More items should be added only after the related source has been mapped.
