# Verification record

Date: 16 October 2026, Asia/Jakarta.

## Local checks

- Six Python tests pass: independently calculated totals, cancellations/full refunds, empty results, deterministic generation, invalid records/links, fixed-reference RFM, and null/numeric date quarantine.
- Two Node tests pass for dashboard metrics and combined filters with empty results.
- Six Playwright/Edge cases pass: SQL/Python export agreement with dashboard totals, filters/reset, empty scopes, date warnings, downloads, keyboard skip link, phone/tablet/desktop layout and automated accessibility, and preventing split currency digits in small KPI cards.
- The notebook executes from a fresh kernel with zero error outputs. It independently reconciles pandas net totals and the SQL/Python metric contract.
- Full regeneration produces byte-identical raw/clean CSVs and summary/dashboard data (13 files).
- Desktop and phone screenshots were visually inspected. KPI overflow found during that inspection was reproduced in a failing regression, fixed with compact values and exact-value supporting text, and passed afterward.
- Original `Bike Buyers.xlsx` Git blob remains `4eb964c33247ee8edc5b34daea035dfcf54e7922`.

## Independent review

A separate reviewer found null/non-string dates could abort the validator. A regression failed before the fix and passed after order/refund date handling was corrected. A missing verification-document link was resolved by this record. Stray external-link glyphs in the separate portfolio integration were also corrected.

## Limits

Automated accessibility checks are limited to the rules and states exercised; they are not accessibility certification. All browser data is synthetic. The tests establish arithmetic and interface behavior for this simulated case study, not business effectiveness or predictive validity. Hosted status must be checked separately after publishing.
