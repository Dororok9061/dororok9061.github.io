# Publication matrix

| Item | Classification | Public representation |
|---|---|---|
| Course title, provider, dates, hours verified by certificate | USER_CREATED_PUBLIC summary | publish metadata |
| Raw certificate image/PDF | PERSONAL_DATA | EXCLUDED |
| Instructor curriculum | INSTRUCTOR_MATERIAL | PUBLIC_SUMMARY_ONLY |
| OUTTA user-modified notebook | USER_MODIFIED / COURSE_STARTER_CODE | publish evidence summary; do not claim fully user-original code |
| P2 raw notebook with plaintext API key | SECRET_DETECTED | EXCLUDED until key rotation and sanitization |
| P1/P2/P3 clean rerun scripts, compact result JSON, sanitized notebooks | USER_CREATED_DERIVATIVE | publish with local-validation protocol and limitations |
| P1/P3 stored output | HISTORICAL_NOTEBOOK_OUTPUT | retain separately from the current rerun |
| Generated submission CSV, feature cache, fitted model | KAGGLE_RESTRICTED / BULK_ARTIFACT | keep local; publish only row count and SHA-256 |
| Kaggle submission, score, rank | KAGGLE_RESTRICTED | publish only after authenticated verification |
| PADS user schematic/BOM/Gerber | USER_CREATED_PRIVATE pending review | planned; per-file review required |
| PADS installers/vendor docs | THIRD_PARTY_COPYRIGHTED | EXCLUDED |
| mmWave papers/manual captures | THIRD_PARTY_COPYRIGHTED | citation or own summary only |
| mmWave transcript screenshot | PERSONAL_DATA | EXCLUDED |
