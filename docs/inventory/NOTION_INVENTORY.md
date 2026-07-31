# Notion publication inventory

Audit date: 2026-07-31.

The connected workspace contains the integrated engineering portfolio and
related project/coursework pages. The previously recorded `app.notion.com`
addresses are authenticated workspace links, not verified public publishing
URLs, and were removed from the website and repository documentation.

## Publication status

- Known integrated portfolio page: public access check returned `none`.
- Verified `notion.site` publishing URL: not available.
- Website link status: **BLOCKED** until the owner republishes the page or
  supplies a verified public URL.
- Internal workspace pages remain unchanged in Notion; no private URL is copied
  into public site data.

## Required verification before re-enabling

1. Open the proposed URL in a signed-out browser.
2. Confirm that no Notion account or workspace membership is required.
3. Review the rendered page for private pages, student IDs, phone/address data,
   license files, and raw research data.
4. Add only the canonical public URL to `src/_data/profile.yml`.

This BLOCKED state is a publication/access boundary, not a failure of the local
Notion content update.
