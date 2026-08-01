# Full Study Source Coverage

Snapshot date: 2026-08-01
Scope: internal QA for the full engineering study rebuild

## Purpose and boundaries

This report records only confirmed inventory results supplied for the current
rebuild. It does not infer unpublished course topics, execution results,
ownership, or redistribution rights from a filename or extension.

The OneDrive university root was compared with its D-drive migration staging
copy through file metadata only. No placeholder was hydrated and no source file
was moved, deleted, rewritten, or published. Inventory views below may overlap
and therefore must not be added together.

Status meanings:

- **PASS**: the stated count, byte total, or parser result was verified for its
  stated snapshot and scope.
- **BLOCKED**: a required comparison or coverage claim cannot be completed
  within the current access boundary.
- **PLATFORM LIMITATION**: the connected service exposes metadata or page text
  but not the binary material required for file-level verification.

## Confirmed inventory

### Coursework mirror

The D-drive coursework mirror contains **571 files** and **988,776,752 bytes**.
Major confirmed formats are:

| Format | Files |
|---|---:|
| PNG | 378 |
| PDF | 76 |
| ZIP | 7 |
| PPTX | 4 |
| VHDL | 4 |
| XLSX | 3 |
| EXE | 3 |
| DOCX | 2 |
| HWPX | 2 |
| MP4 | 1 |

Other formats exist but are not enumerated in this public-safe QA summary.
The **76 PDF files contain 4,306 pages**. Parser verification found **0
encrypted PDFs** and **0 parsing failures**.

Folder-level inventory found **15 course folders**: **10 nonempty** and **5
empty**. An STM course folder was not present in this snapshot. The folder
inventory itself is verified, but full course coverage remains **BLOCKED**
until empty folders and the absent STM source are resolved from an authorized
non-OneDrive source.

### OUTTA archive

The OUTTA parent archive contains **65 entries** with **785,961,658 bytes** of
uncompressed content. Recursive inspection of nested material produced a
separate view of **5,739 items** and **805,124,280 bytes**. These are parent and
nested views of related material, not independent totals.

Confirmed material classes are **16 PDFs**, **34 notebook-like files**, and **3
nested ZIP files**. Inventory and format classification are **PASS**. Complete
PDF-page and notebook-cell mapping to public topic pages is not established by
these counts alone and remains **BLOCKED**.

### Private preservation ledger

The current Private Master ledger records **6,380 items** and
**3,137,214,983 bytes**. It includes the three separately preserved Kaggle
notebooks and the pre-update Notion page backup. JSON and CSV ledgers contain
the same 6,380 relative paths and byte total.

The current D-drive-only snapshot is **PASS**. Its SHA-256 values are
`6B6FD14AB0E80AC1338DE9877F1214BAA9676248CC31671BBFC445AEEC5B89A0`
for JSON and
`C5AE963078220925EA7FEB30DF23E2A5F289CABC7A23AB4C73B9CAF1709669D9`
for CSV. Superseded snapshots remain preserved separately.

## Source-to-use mapping

| Source group | Topic mapping | Public derived use | Private preservation | Verification method | Status |
|---|---|---|---|---|---|
| D coursework mirror | University coursework; per-course chapter mapping still required | Privacy-reviewed, user-authored code, figures, calculations, and summaries only | Keep source mirror unchanged | Recursive file count and logical-byte total | PASS |
| Coursework PDFs | Course chapters, equations, figures, examples, and references | Page citations, rewritten explanations, and rights-reviewed crops | Keep original PDFs private | PDF page parser: 76 files, 4,306 pages, no encryption or parse failures | PASS |
| Coursework course folders | Course-level hubs and topic plans | Derivatives from the 10 nonempty folders after file-level review | Preserve all 15 folders, including empty folders | Folder existence and nonempty check | BLOCKED |
| OUTTA parent archive | Deep-learning bootcamp and P-1/P-2/P-3 projects | Rewritten study notes and sanitized user-derived outputs | Keep original archive private | Archive central-directory inventory | PASS |
| OUTTA nested material | Lecture topics, notebooks, exercises, and project material | Topic summaries, sanitized notebooks, and derived figures after rights review | Keep nested review copy private | Recursive nested item and byte count | PASS |
| OUTTA PDFs and notebooks | Day/topic pages and project execution records | Page-level notes and cell/output-level derivatives | Keep instructor material and original notebooks private | Format classification only; page/cell mapping not yet verified | BLOCKED |
| Three Kaggle files | Kaggle P-1/P-2/P-3 | Sanitized code and verified derived results only | Preserve originals outside public repositories | Included in current D-drive ledger with file hashes | PASS |
| Private Master ledger snapshot | All private source groups represented at snapshot time | Classification metadata only | Retain immutable source and ledger copies | Matching JSON/CSV item paths, byte totals, and SHA-256 | PASS |
| OneDrive freshness comparison | Source freshness and duplicate detection | Metadata only; no source content is published | OneDrive placeholders remain untouched | Relative path, size, timestamp, and file attributes compared read-only | PARTIAL |
| Notion binary attachments | External-course source material | Connector-visible text and metadata; no binary-derived claim | Original attachments remain in their source service | Connector cannot retrieve and hash all binaries | PLATFORM LIMITATION |

## Publication boundary

Public repositories, the website, and public Notion pages may use only:

- user-authored code that passes secret and privacy review;
- sanitized user-modified notebooks with source attribution;
- user-generated outputs whose execution context is documented;
- rewritten explanations, original diagrams, and rights-reviewed figure crops;
- citations and metadata that do not expose private paths or identifiers.

Raw course archives, instructor binaries, datasets with restricted terms,
installers, executable tools, license files, credentials, tokens, private links,
and personal data remain private. A file being inventoried is not permission to
publish it.

## Required next verification

1. Keep the sanitized source-ID map aligned with every D-drive Private Master record.
2. Produce page-level mappings for 4,306 PDF pages and cell-level mappings for
   authorized notebooks without reopening prohibited sources.
3. Resolve the five empty course folders and absent STM source from an
   authorized non-OneDrive copy.
4. The read-only metadata comparison observed 143,288 OneDrive entries
   (140,791,485,603 logical bytes), all represented as offline/reparse entries.
   The D-drive staging copy contains 5,791 matching relative paths
   (11,613,055,300 bytes), with no size or newer-source mismatch among those
   matches; 137,497 entries are not present in staging. Content hashes remain
   unverified because no placeholder was hydrated.
5. Keep Notion binary verification marked **PLATFORM LIMITATION** until a
   connector can retrieve the binaries for hashing and content review.
