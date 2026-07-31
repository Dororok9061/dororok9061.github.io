# Privacy audit

Excluded fields include certificate issue numbers and QR codes, phone numbers, meeting credentials, private Drive/Colab links, Classroom class identifiers, grades, feedback, student names, local account paths, transcript images, raw biosignals, and participant identifiers.

The source Notion page contains instructor contact and meeting data; none is copied. The mmWave screenshot set contains academic-record information; it is classified PERSONAL_DATA and excluded. Classroom and Kaggle identifiers supplied for access are not stored in site data or rendered pages.

The P2 notebook contains a plaintext Google generative-AI API key in an unexecuted cell. Its value is excluded from all derived data and public pages. A new secret-free rerun and sanitized notebook were created without copying the key. Required owner action remains: revoke and replace the exposed credential.

Default visibility remains private for grades, feedback, raw certificates, raw notebooks, datasets, feature caches, fitted models, and submission CSV files. Public pages show verified metadata, compact result JSON, sanitized notebooks, historical execution summaries, and explicit blocked states.
