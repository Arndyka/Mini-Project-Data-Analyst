# Retail analytics project and portfolio additions

Status: approved by the owner on 16 October 2026; implemented and verified locally before publication.

## Purpose and agreed direction

The owner wants a demonstrable data analyst project in Arndyka/Mini-Project-Data-Analyst and wants the existing personal portfolio updated with this project, Spendly, and Date Planner. The owner selected retail sales and customer behaviour as the analytics theme on 16 October 2026.

The intended reader is a recruiter or technical reviewer. They should be able to see the business questions, inspect the data and SQL, reproduce the results, and open a working dashboard. Personal applications should be presented through implemented features and engineering decisions, with professional bilingual wording.

## Approach considered

1. Recommended: a complete retail case study using deliberately synthetic data, SQL and Python analysis, a reproducible report, and an interactive static dashboard. This demonstrates a broader analysis workflow and can be published without a paid backend.
2. Extend only the existing Bike Buyers Excel workbook. This is smaller and preserves the existing exercise, but demonstrates less of the SQL and reproducibility workflow.
3. Publish notebooks and charts without a dashboard. This provides analytical evidence with less UI work, but reviewers must navigate the files to inspect the results.

The recommended scope retains the existing Bike Buyers.xlsx unchanged and adds RetailLens as a separate case study. It does not turn the workbook into an invented history of real retail work.

## RetailLens scope

Use a deterministic synthetic dataset covering January through December 2025: approximately 1,000 customers, 60 products and 12,000 orders, with order items and returns. IDs are fictional; no real names, contact information, bank statements, employer data, API credentials or private account records are included. The README, dashboard and portfolio explicitly identify the case study as simulated.

Business questions:

- How do net sales, order volume and average order value change over time?
- Which product categories and channels contribute to sales?
- How do returning customers and customer segments differ?
- How do returns and data-quality issues affect the interpretation?

Deliverables include raw and cleaned CSVs, a data dictionary, a documented cleaning pipeline, SQLite queries, a runnable analysis notebook, generated charts, an Indonesian business summary with concise English project documentation, and a responsive dashboard with date, category and channel filters. Include an explicit data-quality report rather than silently dropping invalid records.

Metrics have shared definitions. Completed orders exclude cancelled orders. Gross sales uses fulfilled item quantities and prices. Net sales subtracts item discounts and validated refunds; no unverified profit or margin metric is presented. AOV uses net sales divided by completed orders in the selected scope, including orders subsequently refunded. Repeat-purchase rate uses customers with at least two completed orders divided by customers with completed orders. RFM uses documented rules and a fixed reference date after the dataset window; segments are descriptive, not a trained prediction model. Refunds are attributed to their original order for this case study, and that accounting convention is disclosed.

## Architecture and data flow

Separate data generation, validation/cleaning, SQL analysis and report/dashboard export. A documented command regenerates the public synthetic outputs from a fixed seed. Keep metric rules centralized and verify SQL results against the analysis outputs. The static dashboard reads generated public demo data, recomputes metrics consistently for its filters, and never requests private files or services. The RFM section clearly states its fixed reference window rather than implying that global segments are recomputed for every dashboard filter.

Provide empty-state handling, clear labels and units, keyboard-operable filters, readable mobile charts and reduced-motion support. Avoid unnecessary authentication, databases exposed to the internet, AI APIs and paid services. Generated results and written findings must agree; recommendations are hypotheses based on the simulation, not measured business outcomes.

## Portfolio changes

Preserve the navy/teal design, supplied profile photograph, professional wording, bilingual Indonesian/English routes, accessible typography and existing motion controls. Add three case studies, bringing the collection from six to nine:

- RetailLens: synthetic retail sales and customer behaviour analysis, linked to the repository and working dashboard when published.
- Spendly: personal finance application with ledger-based transaction records, budgets, wallets, goals, statement parsing/local OCR and a separate demo. Describe the current local scanner; do not claim the retired external AI backend is active. Use only fictional/demo visuals and links.
- Date Planner / Our Little Date: a personal collaborative planning application covering plans and activities, budgets, calendar export, wishlist, shared rooms and synchronization. Describe React/TypeScript and Supabase access controls without publishing credentials, private room data, personal invitations or screenshots of real accounts.

Add a Personal Applications category and explicit demo/source links on case-study pages. Provide original concept illustrations consistent with the current visual system, rather than screenshots of private accounts. Summaries distinguish the owner's work, implemented deliverables and limitations. Keep the formal ODP IT role and OJT context unchanged. Confidential workplace material, unrelated coursework and previously excluded personal folders remain out of scope. The explicitly requested Spendly application is in scope.

## Verification and publication

Test metric definitions with small independently calculated fixtures, duplicate/missing/invalid records, cancellation and refund cases, and SQL/Python agreement. Check deterministic regeneration and reconciliation totals. Execute the notebook from a clean state. Test dashboard filters, empty results, responsive layouts, keyboard use and chart labels. Review the dashboard and portfolio on desktop and mobile using synthetic/demo data only.

Update portfolio tests that currently assert six projects, and retain coverage for all previous case studies, both languages, category filtering, links, reduced motion, no-JavaScript content and accessibility. Run the appropriate existing build and test commands. Scan outgoing commits for secrets and private data, preserve the existing workbook's hash, and push only the intended repositories. Publish the analytics dashboard through GitHub Pages if the repository's Pages configuration is available; publish portfolio changes through its existing GitHub Pages Actions workflow. Verify actual deployment status and URLs before reporting them as live.

## Boundaries

Do not modify the Spendly or Date Planner applications, their production account data, or confidential OJT repositories. Their source and documentation are evidence for portfolio descriptions only. Do not claim production adoption, revenue improvements, ML accuracy, certification or quantified personal impact without evidence. If deployment access is unavailable, deliver the complete tested repository content and explain the precise remaining hosting step.
