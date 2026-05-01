**PRODUCT SPECIFICATION**

**EM Risk Intelligence Dashboard**

Extending the Financial Fragility Clock for institutional clients

| Built on | Financial Fragility Clock — MSc FinTech, University of Birmingham |
| :---- | :---- |
| **Target client** | EM-exposed asset managers, risk advisory practices (e.g. KPMG FS Risk) |
| **Core methodology** | Minsky regime classification \+ country-specific ML fragility scoring |
| **Delivery** | Standalone web page (em-risk.html) linked from existing dashboard |
| **Status** | **Draft spec — not yet built** |

# **1\. Context & Motivation**

The core project (Financial Fragility Clock) demonstrates that a global-only model systematically underreads stress during country-specific crises. The November 2021 Turkey episode is the canonical example: Model A scored 33.5 (Hedge) while Model B scored 53.0 (Speculative) — a 19.4-point gap — because global markets were calm while Turkey's domestic institutional architecture was collapsing.

The EM Risk Dashboard extends this into a client-facing product. The insight is not Turkey-specific — it is generalizable to any emerging market where domestic stress can decouple from global indices. The product answers the question a risk manager at KPMG or a fund with EM exposure actually asks:

*"My portfolio is 40% Turkey, 30% Brazil, 30% Egypt. What does the fragility signal say about my current exposure, and how would each position have performed through past crises?"*

No existing tool answers this through a Minsky regime lens with country-specific ML scoring. That is the gap.

# **2\. The Three Core Features**

The page has three distinct interactive tools. Each is self-contained but they share a common output: a Minsky regime reading with portfolio implications.

## **Feature A — Portfolio Stress-Tester**

The user inputs their EM portfolio allocation (%) across supported countries. The tool runs the fragility score against each country's data and simulates what a theoretically matched portfolio would have experienced during each of the four historical crisis windows.

### **User inputs**

* Country selector — dropdown with supported EM markets (Turkey, Brazil, Egypt, South Africa, Indonesia — see §4 for rollout)

* Allocation per country — percentage slider, must sum to 100%

* Asset class toggle — Equity / FX / Fixed Income (affects which fragility component is weighted most)

* Time horizon — 1Y, 3Y, 5Y lookback for the stress simulation

### **Outputs**

* Portfolio-weighted fragility score — composite of individual country scores, weighted by allocation

* Regime badge — current Minsky regime for the whole portfolio (Hedge / Speculative / Ponzi)

* Crisis simulation table — for each of the 4 crisis windows, shows: individual country score at peak stress, portfolio-weighted score, estimated drawdown (based on historical ISE/EM returns during that window)

* Heat intensity chart — a 2D grid, countries on Y-axis, crisis windows on X-axis, coloured by fragility score at peak (green → red)

* Worst-case flag — if any position is currently in Speculative or Ponzi territory, shows a prominent alert with the country name and current score

### **Key design constraint**

This tool does **not** produce return predictions. It produces regime signals. The copy on the page must be explicit: this is a risk indicator, not investment advice. The drawdown estimates are historical, not forward-looking.

## **Feature B — Country Comparison**

A side-by-side fragility comparison across all supported EM countries, using the same pipeline and methodology as the Turkey model but with country-specific feature sets.

### **User inputs**

* Select up to 4 countries from the supported list

* Select a date range (scrubber or calendar input)

* Optional: overlay a global event (GFC, COVID, etc.) as a reference band on the chart

### **Outputs**

* Multi-line fragility timeline — one line per country, colour-coded, with Minsky threshold bands (40 and 70\) as horizontal rules

* Current regime table — snapshot of today's score and regime for each selected country

* Divergence stat — for each pair of countries, the correlation of their fragility scores over the selected period (low correlation \= good diversification, high correlation \= contagion risk)

* Top driver comparison — for each country, the top 2 SHAP features driving the current score, shown as a small bar chart

### **Why this matters for a client**

An asset manager holding both Turkey and Brazil might assume they're diversified because the assets are in different geographies. If the fragility correlation between the two countries is 0.87, they're not. This feature surfaces that.

## **Feature C — Forward-Looking Scenario Tool**

Given the current fragility score and Minsky regime, what are the implications for position sizing? This is the most opinionated feature — it translates the score into a suggested risk posture.

### **User inputs**

* Select a country (or use the portfolio from Feature A)

* Input current position size (% of portfolio or absolute £/$)

* Risk tolerance — Conservative / Moderate / Aggressive (affects the suggested drawdown tolerance)

### **Outputs**

* Scenario cards (3) — one per Minsky regime, showing: what would have happened historically if the market had moved from its current regime to each of the three, estimated drawdown per £100k of exposure, suggested hedge ratios from academic literature (Brock et al. 2005, Kahneman framework)

* Regime transition probability — based on the historical transition matrix from the Turkey model, shows the empirical probability of staying in the current regime vs. escalating to the next one over a 3-month horizon

* Position sizing indicator — a simple traffic light: Green (current regime Hedge, hold), Amber (Speculative, consider reducing or hedging), Red (Ponzi, flag for risk committee)

### **Disclaimer block (mandatory)**

*This scenario analysis is based on historical regime transitions and is provided for informational purposes only. It does not constitute investment advice. Past fragility patterns do not guarantee future outcomes.*

# **3\. Data Architecture**

## **3.1 What exists today**

The Turkey model pipeline already produces all required data structures:

* fragility\_output.json — monthly scores 2003–2026 for both Model A and B

* Walk-forward R² by crisis window (4 events × 4 algorithms)

* SHAP values per feature per model

* Regime transition matrix (3×3 Markov)

## **3.2 What needs to be built for new countries**

Each new country requires running the same pipeline with a modified feature set. The heavy lifting is identifying the 3–5 country-specific features that play the role TRY velocity and CBRT dummy play for Turkey.

| Country | Currency | Exchange | Country-specific features | Data source |
| :---- | :---- | :---- | :---- | :---- |
| **Turkey ✓** | TRY | ISE | TRY velocity, CBRT dummy, VIX lags | yfinance (done) |
| **Brazil** | BRL | Bovespa | BRL velocity, Selic rate changes, commodity index (BCOM) | yfinance \+ BCB API |
| **Egypt** | EGP | EGX 30 | EGP depreciation velocity, IMF programme dummy, USOIL | yfinance \+ IMF data API |
| **South Africa** | ZAR | JSE Top 40 | ZAR velocity, load-shedding index, gold/platinum prices | yfinance \+ Eskom API |
| **Indonesia** | IDR | IDX Composite | IDR velocity, BI rate changes, palm oil / coal prices | yfinance \+ BI API |

Each country pipeline takes approximately 2–3 days of notebook work once the feature set is agreed. Turkey is the template — the code is already parameterised.

## **3.3 JSON schema for multi-country support**

The existing fragility\_output.json needs a new top-level key per country. The Turkey data becomes:

{ "countries": { "TR": { "scores": \[...\], "shap": {...}, "transitions": {...} }, "BR": {...} } }

All three features on the new page fetch from this structure. No new backend needed — it's a static JSON file regenerated by the notebooks.

# **4\. Page Structure & UI**

## **4.1 Navigation**

The existing dashboard nav adds a single link:

Dashboard  ·  Presentation  ·  Reports  ·  Guide  ·  \[ EM Risk ← new \]

URL: fragility-clock.vercel.app/em-risk.html

## **4.2 Page layout (single scroll)**

| Section | Content |
| :---- | :---- |
| Header | Page title, one-line description, link back to main dashboard |
| Context strip | 3 stat cards: current Turkey score, highest current EM score across supported countries, number of countries in Speculative+ regime right now |
| Feature A | Portfolio Stress-Tester — full width, input panel left, outputs right |
| Feature B | Country Comparison — full-width timeline chart, regime table below |
| Feature C | Scenario Tool — 3 scenario cards side by side, transition matrix below |
| Footer | Methodology note, disclaimer, link to full reports page |

## **4.3 Design system**

* Reuse all CSS variables and colour tokens from dashboard.html — no new design language

* Purple \#534AB7 as primary action colour (matches existing)

* Regime colours consistent across all pages: green \#3ECF8E (Hedge), amber \#F5A623 (Speculative), red \#E05252 (Ponzi)

* All charts use the same charting approach as the existing dashboard (vanilla JS / D3, no new libraries)

* Mobile responsive — the three feature sections stack vertically below 768px

# **5\. Build Plan**

**Phase gates — instruction for the AI agent:** After completing every task within a phase, check whether all tasks for that phase are done. When the phase is complete, stop executing, do not begin the next phase, and tell the user: which phase just finished, what was built, and approximately how long the next phase will take relative to the one just completed (e.g. "Phase 2 will take roughly twice as long as what we just did" — no clock times, just a relative comparison). Then wait for the user to say they want to continue before starting anything else.

| Phase | Task | Detail | Who / When |
| ----- | :---- | :---- | :---- |
| **1** | **JSON schema update** | Restructure fragility\_output.json to support multi-country keys. Migrate Turkey data to { countries: { TR: {...} } }. Validate existing dashboard still works. | Notebook work — 2–3 hrs |
| **1** | **Static mock data (scaffold only)** | Add Brazil and Egypt with placeholder scores (Turkey data scaled ±10%) so the UI can be built and tested before real pipelines run. **This data must be fully replaced by real pipeline output before Phase 4 is complete. Mock data must not appear in the final deployed page — see §8.** | 1–2 hrs |
| **2** | **em-risk.html skeleton** | Build the page structure, nav link, header, context strip stat cards, footer. No feature logic yet — just layout and CSS. | 3–4 hrs |
| **2** | **Feature A UI** | Build portfolio input panel (country selector, allocation sliders), crisis simulation table, heat intensity chart. Wire to mock JSON. | 6–8 hrs |
| **3** | **Feature B UI** | Multi-country timeline chart, regime snapshot table, divergence correlation stat, top-driver mini bar charts. Wire to mock JSON. | 5–6 hrs |
| **3** | **Feature C UI** | 3 scenario cards, transition probability display, traffic light position indicator. Wire to mock JSON. | 4–5 hrs |
| **4** | **Real country pipelines** | Run the notebook pipeline for Brazil (BRL velocity \+ Selic dummy) and Egypt (EGP velocity \+ IMF dummy). Replace mock JSON with real scores. | 3–4 days per country |
| **4** | **Vercel deploy** | Deploy em-risk.html to existing Vercel project. Update nav on all 4 existing pages to include EM Risk link. | 30 mins |

# **6\. What This Adds to the Presentation**

The professor's feedback was that the project needs a stronger business narrative. The EM Risk Dashboard addresses this directly:

| What was missing | What this adds |
| :---- | :---- |
| Single-market scope (Turkey only) | Generalizable pipeline — same methodology, any EM market. Brazil and Egypt add immediately. |
| Academic output only | Client-facing tool with a clear use case: EM portfolio risk assessment through a Minsky lens |
| No actionable output | Scenario tool translates score → position sizing implication → risk committee flag |
| "Why would KPMG care?" | Portfolio stress simulation against 4 real crisis windows, country correlation matrix, regime transition probabilities — these are things a risk advisory practice charges for |

The one-sentence pitch for the presentation: *"We built an academic fragility model. We also built what it becomes when you hand it to a client."*

# **7\. What This Is Not**

Being explicit about scope prevents scope creep and deflects overclaiming in the presentation.

* Not a trading signal — the fragility score is a risk indicator. It says nothing about whether to buy or sell specific securities.

* Not a Bloomberg replacement — coverage is limited to supported countries with 20+ years of yfinance data. This is a proof-of-concept product, not a data terminal.

* Not a real-time system — scores update monthly when the notebook pipeline is rerun. There is no live data feed.

* Not investment advice — every client-facing output must carry the disclaimer in §2 Feature C.

* Not a complete KPMG product — it demonstrates the methodology and the client interface. Productionising it for a real advisory engagement would require regulatory compliance work, data licensing, and proper backtesting standards. This is the academic prototype.

# **8\. Implementation Guide for the AI Agent**

This section exists because the person running this build may not have a programming background, and the gap between "it runs without errors" and "it actually works" is wide enough to waste days. Read this before writing a single line of code.

## **8.1 The non-negotiable output requirement**

**The final deployed page must serve real data. No exceptions.**

Mock data (see §5, Phase 1) is a build scaffold — it exists only so the UI can be developed and visually verified before the notebook pipelines produce real country scores. Mock data is not a deliverable. The build is not complete until:

* `fragility_output.json` contains real computed scores for every country that appears in the UI
* Every chart, table, and stat card on `em-risk.html` is reading from that real JSON
* There are no hardcoded numbers, placeholder arrays, or `Math.random()` calls anywhere in the production code

If the real pipeline for a country (e.g. Egypt) is not ready in time, the correct response is to **remove that country from the UI entirely** — not to ship placeholder scores labelled as real. A country either has real data behind it or it does not appear on the page.

## **8.2 Environment setup — what you need before you start**

The AI agent must not assume any tools are installed. Before running any command, verify the following are present and install them if not.

**Required for UI development:**

```bash
# Check Node is installed
node --version        # needs v18 or higher
npm --version

# If not installed: https://nodejs.org/en/download
# On Mac with Homebrew: brew install node
```

**Required for the Python notebook pipeline (generating real JSON):**

```bash
# Check Python is installed
python3 --version     # needs 3.9 or higher

# Install notebook dependencies (run from the project root)
pip install -r requirements.txt

# If requirements.txt doesn't exist yet, the minimum set is:
pip install yfinance pandas numpy scikit-learn shap jupyter
```

**Required for Git and GitHub:**

```bash
git --version         # must be installed to submit a PR
# If not: https://git-scm.com/downloads
```

## **8.3 Why you cannot just open em-risk.html directly in a browser**

Opening an HTML file by double-clicking it (the `file://` protocol) will silently block the `fetch()` calls that load `fragility_output.json`. The charts will appear to render — they may even show data if the page falls back to mock values — but the real JSON will not have loaded. **This is the most common way to incorrectly believe the page is working when it is not.**

To view the page with real data loading correctly, you must serve it over HTTP. The simplest way:

```bash
# From the project root directory (the folder containing em-risk.html and the data/ folder)
python3 -m http.server 8000

# Then open in browser:
# http://localhost:8000/em-risk.html
```

Leave this terminal running while you work. Every time you refresh the browser, it will re-fetch the JSON. If you see the data update after regenerating the JSON, the pipeline is wired correctly.

## **8.4 How to verify the page is using real data (not mock)**

Before marking any phase complete, run through this checklist in the browser with the HTTP server running:

1. Open `http://localhost:8000/em-risk.html`
2. Open the browser developer console (right-click → Inspect → Console tab)
3. Look for any log line that says "mock", "placeholder", "fallback", or similar — if you see one, the real JSON did not load
4. In the Network tab, filter by `fragility_output.json` and confirm the request returned status 200 (not from cache, not a 404)
5. Click into the response — verify the JSON contains `countries.TR`, `countries.BR` etc. with real score arrays (not identical or near-identical values, which would indicate copy-paste scaling)
6. Change the portfolio allocation in Feature A and confirm the portfolio-weighted score updates to a different number — if it stays the same, the inputs are not wired to the data

If all six checks pass, the page is reading real data. Do not skip this.

## **8.5 Submitting the work — pull request workflow**

All work must be submitted as a pull request to the main repository. Do not push directly to `main`. The steps:

```bash
# 1. Make sure you're starting from a clean, up-to-date main
git checkout main
git pull origin main

# 2. Create a new branch for this feature
git checkout -b feature/em-risk-dashboard

# 3. Do your work — build the page, run the pipelines, update the JSON
# ... (all your changes) ...

# 4. Stage everything
git add em-risk.html data/fragility_output.json
# Also add any new notebook files, updated nav on existing pages, etc.
git add .

# 5. Commit with a clear message
git commit -m "Add EM Risk Dashboard (em-risk.html) with real country data for TR, BR, EG"

# 6. Push to GitHub
git push origin feature/em-risk-dashboard

# 7. Open GitHub in the browser and create the pull request
# Go to: https://github.com/[repo-owner]/[repo-name]/pulls
# Click "New pull request" → base: main ← compare: feature/em-risk-dashboard
# Title: "EM Risk Dashboard — initial build"
# Description: list which countries have real pipeline data, which charts are live, and confirm the §8.4 checklist was run
```

Once the pull request is merged to `main`, Vercel will automatically detect the change and deploy — no manual deploy step needed. The live URL (`fragility-clock.vercel.app/em-risk.html`) will be live within 1–2 minutes of the merge.

## **8.6 What a completed build looks like**

The build is done when:

* `em-risk.html` exists at the project root and is accessible at `fragility-clock.vercel.app/em-risk.html` after deploy
* The nav on all existing pages (`dashboard.html`, `presentation.html`, `reports.html`, `guide.html`) includes the EM Risk link
* All three features (A, B, C) render with real country data — no mock fallbacks in production
* The §8.4 checklist passes in the deployed Vercel URL (not just localhost)
* A pull request exists on GitHub with the changes, and has been reviewed before merging to main


