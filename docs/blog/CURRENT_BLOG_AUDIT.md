# Current blog audit

Audit date: 2026-08-01
Baseline: `bae518de56340934e82ae9140af8c468fa84c661`

## Before the change

- 12 Markdown files represented six Korean/English post pairs.
- The blog layout hard-coded six category slugs; no parent-child taxonomy existed.
- All posts were short policy summaries published on one date.
- No series order, roadmap, start page, archive, tag index, or client-side search existed.
- The post layout exposed only category, date, author, description, and body.
- No table of contents, source list, evidence field, tool list, series navigation, or related-project block existed.
- Legacy category pages used a flat `site.categories` lookup and did not explain planned work.
- Existing project images were available but absent from blog posts.

## Implemented architecture

Taxonomy, series, roadmaps, learning programs, and competitions now live in `_data`. A small Jekyll generator creates bilingual category and roadmap routes from those records. The site keeps the Simplex Gem theme, static HTML/CSS, and one vanilla JavaScript search module.

The 10 requested engineering categories are retained, with `external-learning` added as an independent 11th category because completion, assignment, competition, and score evidence has a different disclosure boundary. Methodology remains last in display order and is excluded from the main latest-post list.

## Preserved URLs

The six original Korean URLs and six English URLs retain their original permalinks and dates. `updated` and `revision_history` record the rewrite. Old flat category routes remain in the repository as compatibility pages.

## Honest limits

Planned series entries have no post URL. PADS and mmWave source folders support inventory and roadmap placement, but vendor documents, installers, local paths, transcript images, and third-party paper/manual captures are excluded from publication.
