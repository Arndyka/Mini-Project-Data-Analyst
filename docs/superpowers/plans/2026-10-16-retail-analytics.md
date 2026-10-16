# RetailLens Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Publish a reproducible synthetic retail analysis and add three evidence-based case studies to the existing portfolio.

**Architecture:** Python generates and validates relational demo data, SQLite independently aggregates it, and an export supplies a static interactive dashboard. Portfolio content remains bilingual and statically generated.

**Tech Stack:** Python 3, pandas, SQLite, matplotlib, Jupyter notebook; browser-native JavaScript/SVG; existing Node/Playwright portfolio.

**Spec:** ../specs/2026-10-16-retail-analytics-and-portfolio-design.md. Approved by the owner with “oke gass” on 16 October 2026, including implementation, testing, push and publication. Execute inline in this session.

## Global Constraints

- Preserve Bike Buyers.xlsx and all existing portfolio cases and ODP/OJT wording.
- Use only deterministic fictional retail data, January–December 2025, with explicit simulation labels.
- No personal accounts, financial statements, credentials or confidential employer material.
- Preserve navy/teal, portrait, both languages, accessible mobile layouts and motion controls.
- Do not change Spendly or Date Planner; use verified source as case-study evidence.

## Review Focus

- Cancellation and full refunds: exclude cancellations; retain completed fully refunded orders in the AOV denominator.
- Invalid/missing/duplicate raw records: quarantine with reasons instead of silently coercing financial values.
- Empty dashboard scope: show zero metrics and clear empty state, without NaN or a misleading chart.
- RFM scope: fixed full-year reference and labelled independent scope; no unsupported prediction claims.
- New portfolio categories and links: filters, locale navigation, nine-card count and existing motion must work.

## Task 1 Data and calculations

Files: `retaillens/generate.py`, `retaillens/analysis.py`, `sql/metrics.sql`, `tests/test_analysis.py`.
Interfaces: `generate(seed=42)` returns tables; `clean(tables)` returns clean tables and issue records; `metrics(lines)` returns integer-rupiah totals, order/customer counts and rates; `sql_metrics(lines)` independently verifies totals; `rfm(lines)` returns customer segments at 2026-01-01.

- [ ] Write failing tests for manually calculated cancellation/refund/discount fixture, duplicate cleaning and invalid links/amounts.
- [ ] Observe failures, implement deterministic generator and validation, then pass tests including SQL/Python agreement and regeneration identity.
- [ ] Commit data and calculation implementation.

## Task 2 Reproducible outputs and dashboard

Files: `retaillens/build.py`, `notebooks/retail_analysis.ipynb`, `data/{raw,clean}`, `reports`, `site/{index.html,styles.css,app.js,metrics.js}`, `.github/workflows/pages.yml`, `README.md`.
Interfaces: `python -m retaillens.build` recreates public data, reports, charts, notebook and site data; `metrics.js` exports `summarize(rows)` and `filterRows(rows, filters)` with the same definitions as Python.

- [ ] Write browser-metric fixture tests first; observe failure and implement shared filter/summary module.
- [ ] Build raw/clean CSVs, dictionary, quality report, SQLite SQL and charts, computed findings and runnable notebook.
- [ ] Create accessible dashboard with date/category/channel filters and fixed-reference RFM panel.
- [ ] Test empty scope, recomputation, downloads, chart labels, mobile widths, keyboard use; execute notebook from clean kernel.
- [ ] Commit verified outputs and documentation, retaining original workbook hash.

## Task 3 Portfolio additions

Files in Portofolio: `content/projects.mjs`, `scripts/build.mjs`, `scripts/art.mjs`, `public/styles.css`, `tests/{site,publication,motion}.spec.mjs`, new `tests/additions.spec.mjs`.

- [ ] Add failing tests for three new detail pages, Personal Applications filter, nine projects and demo/source links.
- [ ] Add professional Indonesian/English case studies, concept SVGs, external links and category; update expected counts while preserving existing exclusions.
- [ ] Run production build, existing suite, new browser cases and desktop/mobile visual QA.
- [ ] Commit only intended portfolio changes.

## Task 4 Publication and final verification

- [ ] Review outgoing diffs for private content, secrets and unsupported claims; request independent code review if required by review skill.
- [ ] Push analytics and portfolio commits to their existing repositories without rewriting history.
- [ ] Enable/use GitHub Pages analytics deployment through authorized GitHub credentials; monitor both workflows to terminal status.
- [ ] Verify live URLs and final git status; report precise results and limitations.
