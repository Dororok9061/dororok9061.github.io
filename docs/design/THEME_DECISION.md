# Theme Decision

Decision date: 2026-07-31.

## Decision

Use the MIT-licensed `jekyll-theme-simplex` Gem as the actual Jekyll theme:

```ruby
gem "jekyll-theme-simplex", "= 0.9.8.15"
```

`src/_config.yml` declares `theme: jekyll-theme-simplex`; the theme's SCSS,
color variables, typography, and WOFF2 fonts are resolved from the installed
Gem during every build. Accessible repository-owned layouts and includes
override the stock theme layouts without replacing the Gem dependency.

## Information architecture

- independent Korean and English routes
- project index plus six independent project case-study pages in each language
- publications, coursework, defense systems, lab, role-oriented, about, and
  security pages
- real Jekyll posts, blog indexes, Atom feed, sitemap, and category pages
- public GitHub, GitHub Pages, and Notion evidence links

The previous custom single-page source remains only as the non-deployed
`site/` recovery snapshot.

## Minimal implementation boundary

The site needs build-time content generation, not a runtime web application.
It therefore uses:

- Jekyll and Simplex at build time
- static HTML/CSS at runtime
- one small Vanilla JavaScript file for the accessible mobile menu
- no React, Next.js, Vue, Firebase, database, API, authentication, upload,
  analytics, external form, chat, Service Worker, Blockchain, or Web3 surface

The stock Simplex jQuery, Lity, helper script, legacy WOFF/TTF fallbacks, and
unused icons are not copied into `_site`. This preserves the actual Gem Theme
while publishing only assets required by the overridden layouts.

## Performance and maintenance

- exact Gem versions and transitive dependencies in `Gemfile.lock`
- GitHub Actions and local builds use `src/` → `_site`
- public build remains below the 3 MB budget
- local WebP with JPEG fallback, explicit dimensions, and lazy loading
- CSP-compatible external CSS/JS only; no source maps
- KO/EN canonical and `hreflang`, sitemap, feed, robots, and Open Graph image

## Accessibility

- skip link and semantic landmarks
- visible keyboard focus and reduced-motion support
- keyboard-operable mobile menu with `aria-expanded` and Escape close
- no hover-only content
- language metadata and paired alternate routes
- descriptive image alternative text and explicit dimensions

## Profile photograph

The supplied formal photograph is now approved for Hero and About use. The
OneDrive original was not modified. Processing used a read-only backup copy,
removed metadata, resized/cropped only, and did not generate or alter facial,
skin, eye, clothing, or background content. See `docs/PROFILE_ASSET_STATUS.md`.
