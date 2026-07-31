# Notion publication inventory

Audit date: 2026-08-01.

The connected workspace contains the integrated engineering portfolio and
related project/coursework pages. The previously recorded `app.notion.com`
addresses are authenticated workspace links, not verified public publishing
URLs, and were removed from the website and repository documentation.

## Publication status

- Known integrated portfolio page ID: `3ab518ac-7a59-8121-b666-e4c7cce8324c`.
- Verified public URL:
  `https://fierce-rodent-308.notion.site/Engineering-Portfolio-FPGA-Radar-Embedded-Systems-Biomedical-AI-3ab518ac7a598121b666e4c7cce8324c`.
- Anonymous `getPublicPageData` verification returned `requireLogin: false`,
  `publicAccessRole: reader`, the expected page ID, and the published domain
  `fierce-rodent-308`.
- Anonymous page-content loading returned the expected Engineering Portfolio
  title and content. The public URL also returned HTTP 200.
- Website link status: **VERIFIED_PUBLIC_2026-08-01**.
- Authenticated `app.notion.com` workspace links remain excluded from public
  site data.

## Verification repeated for this release

1. Open the proposed URL in a signed-out browser.
2. Confirm that no Notion account or workspace membership is required.
3. Review the rendered page for private pages, student IDs, phone/address data,
   license files, and raw research data.
4. Add only the verified `notion.site` URL to `src/_data/profile.yml`.

This verification confirms anonymous read access at the stated time. It does
not replace future privacy review when Notion content or sharing settings
change.
