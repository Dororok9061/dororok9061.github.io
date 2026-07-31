# Series management guide

Series definitions live in `src/_data/blog_series.yml`. Every published item needs a real KO/EN URL, unique order, source material, category, and status. Planned items have no URL. A post points back with `series` and `series_order`; those values must match the data file.

Change status only with evidence: `planned` → `studying` → `draft` → `published` → `verified`. Do not calculate a percentage that implies planned work is complete. Series pages report absolute published and planned counts.
