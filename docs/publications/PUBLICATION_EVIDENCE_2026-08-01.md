# Publication evidence verification — 2026-08-01

This record separates supplied images, source PDFs, database records, and
public URLs. A successful check in one category does not imply success in the
others.

## KIEE 2026 FMCW paper

### Supplied first-page image

- Original image SHA-256:
  `82BED7ED21CFFF2EC4D94A95587CEEAC4E70F297D8FFF4E50A0947568EE0E502`
- Original dimensions: 570 × 782 pixels.
- Public derivatives:
  - `kiee2026_fmcw_first_page.jpg` —
    `AE566B627644DD0C05501C7F9A20AEF115536E03C03725F8BE8675B0257BBF5B`
  - `kiee2026_fmcw_first_page.webp` —
    `35D3B07A4D4B3A1CF9312CA5385116DF47F74B51A0B39F99A2491DCC533F4FE2`
- Both derivatives were rebuilt without EXIF metadata and visually checked
  against the supplied image.

### Proceedings page range

- Source PDF SHA-256:
  `F82789853FD10CA777FA4E1F0B15F40AE42F051481F333D129709AD6A441BFAE`
- PDF properties: 2 pages, A4, unencrypted, no JavaScript.
- Rendered page 1 contains the paper title and printed page `2413`.
- Rendered page 2 continues the same paper through its conclusion and
  references and contains printed page `2414`.
- Verified range: **pp. 2413–2414**.
- The local source PDF is verification evidence only. No public PDF link is
  asserted because an independently verified public PDF URL was not found.

### DBpia status

- Exact-title search on 2026-08-01 returned zero records.
- Record existence: `NOT_FOUND_BY_EXACT_TITLE_SEARCH`.
- Exact URL: `NOT_VERIFIED`.
- This is a dated search result, not a claim that no future record can exist.

## CICS 2025 CNN–HRV paper

### First-page preview optimization

- The preview was regenerated from the public two-page paper PDF rather than
  from a second-generation screenshot.
- Public dimensions: 700 × 990 pixels.
- Public derivative hashes:
  - JPG: `6BDB94E2F2160991B8D86B95F44198FB4B751EC6B94E757F3CF5BE677D2BA009`
  - WebP: `D0DB499DB8A49FE721CB6E669CC2B3CEE18F9B1B3EEC68E1A4672E945FAC1F1B`
- The original 1132 × 1600 site derivatives remain recoverable from the
  pre-change Git bundle and the dated local backup.

### DBpia record and URL

- Exact-title search returned one record: `NODE12564300`.
- The API result matched the title, authors 류형록·강우석·김경호, publication
  month 2025.10, and pp. 291–292.
- Exact record URL:
  `https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE12564300`.
- The record page returned HTTP 200 and exposed the matching title, first
  author, and page range.
- Record existence: `VERIFIED_PRESENT`.
- Exact URL: `VERIFIED_EXACT`.

### Metric scope note

The supplied paper PDF reports average AUC 0.85 and F1-score 0.82 in its
abstract and conclusion. Its body also reports a Fold 5 F1 value of 0.992,
while the DBpia record abstract reports AUC 0.99 and F1 0.992. The portfolio
keeps the abstract/conclusion averages as its headline paper metrics and
records the other values as a source-scope difference rather than combining
them.
