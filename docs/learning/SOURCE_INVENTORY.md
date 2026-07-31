# External learning source inventory

Audit date: 2026-08-01. Source folders were read-only; originals were not modified.

| Source group | Observed content | Public use | Status |
|---|---|---|---|
| OUTTA supplied archive | 65 entries; notebooks, PDFs, nested data archives | metadata summary only | INSTRUCTOR_MATERIAL / KAGGLE_RESTRICTED |
| OUTTA P-1 notebook | 27 cells; 16/17 code cells carry execution counts; 13 output objects; SHA-256 `A5034371F3509ADBDABEBE004FEF224F93AC30A55E1D416F375105446B450852` | execution summary only | USER_MODIFIED / COURSE_STARTER_CODE |
| OUTTA P-2 notebook | 80 cells; 37/49 code cells carry execution counts; 30 output objects; training stopped at 14%; SHA-256 `633FFF0D55AA7AF4606ADDD2A45749C6DE4C8FF890280F61E59D2B44A23FD0D7` | summary only; raw file blocked | SECRET_DETECTED |
| OUTTA P-3 notebook | 31 cells; 17/17 code cells carry execution counts; 29 output objects; SHA-256 `215831AA10FCE59DB524713A693F9D1230C513FBECF1A69163C01A4435938345` | execution summary only | USER_MODIFIED / COURSE_STARTER_CODE |
| OUTTA P-1 dataset | 27,455 labelled 28×28 rows; 7,172 test rows; 24 labels | read-only local rerun; not redistributed | KAGGLE_RESTRICTED |
| OUTTA P-2 dataset | 12,516 labelled rows; 5,364 test rows; positive rate 4.75% | read-only local rerun; not redistributed | KAGGLE_RESTRICTED |
| OUTTA P-3 dataset | 914 labelled and 300 test WAV files; 10 genres | read-only local rerun; not redistributed | KAGGLE_RESTRICTED |
| Sanitized P-1/P-2/P-3 reruns | clean scripts, compact JSON reports, and three executed review notebooks | publish with split protocol and limitations | USER_CREATED_DERIVATIVE |
| OUTTA certificate | one-page completion certificate | metadata only; raw QR withheld | PERSONAL_DATA |
| KAIST 2024 winter certificate | two-page PDF; 20-hour course metadata | metadata only | PERSONAL_DATA |
| KAIST 2025 summer certificate | one-page PDF; 20-hour course metadata | metadata only | PERSONAL_DATA |
| Defense practice certificate | one-page PDF; dates and completion verified | metadata only | PERSONAL_DATA |
| Generative-model course Notion | 38 headings; child pages Diffusion Models and Pix2Pix; 26 attachments (11 PPTX, 13 PDF, 2 notebooks); 14 Colab links | paraphrased curriculum only | INSTRUCTOR_MATERIAL / ATTACHMENT_EXPORT_BLOCKED |
| Google Classroom | browser initialization failed before authentication | none | BLOCKED_AUTHENTICATION |
| Kaggle | CLI and credential absent | no title, metric, score, rank, or submission claim | BLOCKED_KAGGLE_AUTHENTICATION |
| PADS archive | 192 items, about 7.96 GB; designs, screenshots, installers, vendor references | roadmap; user-created artifacts require per-file review | MIXED |
| mmWave archive | 142 items, about 24.0 MB; papers, presentation, screenshots | roadmap and public summary only | MIXED |

PADS installers and third-party packages are excluded. The mmWave screenshots include transcript/personal data and captures from third-party papers or manuals; none are copied into the public site. The P2 notebook contains a plaintext Google API key; the value is not copied into this repository or Notion and the raw notebook remains excluded. All source notebooks and datasets were read-only; improved outputs were written only to the isolated workspace.
