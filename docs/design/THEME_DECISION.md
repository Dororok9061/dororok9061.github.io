# Theme Decision

## Decision

Build an independent static site with:

- semantic HTML
- one shared CSS file
- one small Vanilla JavaScript file for theme preference
- separate Korean and English HTML routes
- GitHub Actions Pages deployment

## Reviewed references

| Reference | License | Used | Excluded |
|---|---|---|---|
| jekyll-theme-simplex 0.9.8.15 | MIT | dark/light idea, responsive reading rhythm | code, Jekyll, fonts, jQuery, Lity |
| pRoJEct-NeGYa | MIT | category/gallery composition idea | code, CSS, images, personal content |
| keemtj/portfolio | No license detected | hero/card/navigation idea only | all source and assets, React, Firebase |
| GitHub Pages workflow article | Article copyright | general workflow context | text, screenshots, code |

## Why React is not used

The site has no application state, authentication, database, uploads, API, or
dynamic CMS. React would add a build toolchain, runtime bundle, dependency
updates, and supply-chain surface without improving the required navigation.

## Why Jekyll is not used

The root portfolio has two hand-authored routes and a small fixed project set.
Jekyll would introduce Ruby and gem dependencies for content that can be served
directly. Existing project Pages can keep their own structures.

## Performance and maintenance

- no runtime framework or third-party script
- system font stack
- local compressed WebP with JPEG fallback
- public site under 3 MB
- explicit image dimensions and lazy loading below the fold
- CSP-compatible external CSS/JS only
- separate source/docs and public `site/` deployment boundaries

## Accessibility

- skip link and semantic landmarks
- visible keyboard focus
- no hover-only content
- language metadata and alternate routes
- high-contrast tokens for dark and light modes
- reduced-motion support
- descriptive project-image alternative text

## Deferred item

The supplied formal profile photograph remains `BLOCKED` because the protected
OneDrive original was not accessed. The live design uses a truthful HR monogram
instead of a wrong or generated face. A copied, user-approved source outside
OneDrive can be processed later without changing the layout.

