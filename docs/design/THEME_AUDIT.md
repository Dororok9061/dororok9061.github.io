# Theme and Reference Audit

Audit date: 2026-07-30.

No reviewed theme code, CSS, JavaScript, font, icon, or personal content was
copied into the final site. The final implementation is an independent static
design.

## 1. jekyll-theme-simplex

- Registry: https://rubygems.org/gems/jekyll-theme-simplex
- Source: https://github.com/andreondra/jekyll-theme-simplex
- Registry version reviewed: `0.9.8.15`
- Source commit reviewed: `25b620ad4b1ecf649307b12669e164070d3fc7da`
- Gem SHA-256 reported by RubyGems:
  `850ab718db1bd59d34612c8ed348577f8684e1aafd1bdccaa7f08ae3a17023a9`
- Declared license: MIT
- Runtime dependency: Jekyll `~> 4.0`
- Bundled assets observed: Roboto family files, jQuery slim 3.4.1, Lity, Ionicons-derived arrows

Applicable ideas:

- responsive content width
- dark/light color system
- image-forward project reading
- Open Graph and readable typography

Excluded:

- theme code and layouts
- jQuery and Lity
- bundled fonts and icons
- Jekyll plugin surface

Reason: the portfolio can satisfy the same UX with native HTML/CSS and one
small Vanilla JavaScript file, avoiding package and theme supply-chain surface.

## 2. pRoJEct-NeGYa

- Requested legacy URL redirects to canonical repository:
  https://github.com/gmkzwwg/pRoJEct-NeGYa
- Source commit reviewed: `079be07341345a1139875ddd2bd525ff93c5605e`
- License: MIT, copyright Lob.com (2017)

Applicable ideas:

- strong portfolio navigation
- category composition
- image-led gallery rhythm

Excluded:

- source code, CSS, images, collection content, names, and copy

Reason: only visual hierarchy was needed. Independent implementation avoids
copying personal content and legacy theme assumptions.

## 3. keemtj/portfolio

- Source: https://github.com/keemtj/portfolio
- Commit reviewed: `681b3468fe93ff2f9c75f405c52cfdff36c4837d`
- Repository license: none detected
- Stack observed: React 17, Firebase 9, styled-components, carousel, router,
  EmailJS, SweetAlert2

Applicable ideas:

- concise hero
- responsive section navigation
- project-card hierarchy
- language and theme controls

Excluded:

- all source code, CSS, JavaScript, images, personal copy, and Firebase config
- React, Firebase, EmailJS, carousel and modal dependencies

Reason: absence of an explicit license blocks code reuse. The dependency set
also exceeds the needs of a public static portfolio.

## 4. GitHub Pages workflow article

- Reference: https://raccoonjy.tistory.com/33
- Use: conceptual workflow reference only
- Copied content: none

GitHub's current Pages and Actions documentation takes precedence over the
older article for deployment and security settings.

