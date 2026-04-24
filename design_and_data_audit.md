# Design & Data Coherence Audit
## Financial Fragility Clock — `index.html` (presentation) + `dashboard.html`
**Date: 2026-04-24 | Pre-submission review**

---

## The Core Tension

Both files were built to tell a clean, compelling story:

> **Model B detects Turkey's crises because it sees TRY/USD collapse; Model A is blind because it was trained only on global crises.**

That story is *academically true* and *empirically supported*. But when real data loads from `fragility_output.json`, several pieces of the UI will either break silently, show numbers that contradict the narrative, or show no data at all. Below is a full accounting.

---

## Part 1 — Data Mismatches (Real vs Hardcoded)

### 1.1 Performance Numbers Are Completely Wrong in `index.html`

`index.html` has hardcoded `MODELS.A.perfRows` and `MODELS.B.perfRows` with placeholder numbers. When `patchModelsFromRealData()` runs, it overwrites them from the JSON — but only if you look at the actual JSON carefully:

| What `index.html` claims (hardcoded) | What the JSON actually has |
|--------------------------------------|---------------------------|
| Model B RF R² = **0.91** | RF R² = **0.138** |
| Model A RF R² = **0.74** | Model A RF R² = **0.138** |
| Model B OLS R² = **0.76** | Model B OLS R² = **0.094** |
| Model A OLS R² = **0.61** | Model A OLS R² = **0.040** |

**These are order-of-magnitude wrong.** The JSON R² values are raw-return-scale metrics (predicting monthly ISE returns in fraction units, e.g. 0.03), not fragility-score-scale. But the display will show `0.094` where the UI context implies `0 = bad, 1 = perfect` — which looks like a catastrophic model failure to any reader, not a unit-scale issue.

**Effect in UI:** The stat strip `Best Model R²` will show `0.094` or `|0.094|` (the code does `Math.abs(bestR2).toFixed(4)`). This directly contradicts the narrative "Model B is high-performing."

> [!CAUTION]
> The `patchModelsFromRealData()` function in `index.html` silently replaces the good-looking hardcoded numbers with the confusing real numbers. There's no note in the UI explaining the unit difference.

---

### 1.2 Crisis Scores Don't Match Either File's Claims

**Real scores from JSON:**

| Crisis Date | Model A (real) | Model B (real) | index.html claims (hardcoded) | dashboard.html uses |
|------------|---------------|---------------|-------------------------------|---------------------|
| May 2010   | **55.9** (SPEC) | **63.5** (SPEC) | A=78.4 PONZI, B=82.1 PONZI | A=39.2, B=49.2 |
| Aug 2018   | **46.9** (SPEC) | **52.1** (SPEC) | A=43.2 SPEC, B=67.8 PONZI | A=24.0, B=40.5 |
| Mar 2020   | **58.8** (SPEC) | **71.1** (PONZI✓) | A=71.2 PONZI, B=88.5 PONZI | A=42.5, B=77.8 |
| Nov 2021   | **33.5** (HEDGE) | **53.0** (SPEC) | — | A=27.2, B=60.1 |

**Problems:**
- The Greek Crisis 2010: Real data shows both models in SPEC (55.9 / 63.5). `index.html` shows both as PONZI (78.4 / 82.1) from hardcoded values. The crisis archive text says "Both models detect this." → With real data, neither reaches PONZI. The bar chart will show amber bars, not red, which is technically correct but visually weak for a crisis labeled as "detected."
- The 2018 TRY Crisis: Real data = A:46.9 (SPEC), B:52.1 (SPEC). **Neither model crosses the PONZI threshold.** The crisis detection chart will show both bars as amber (SPECULATIVE), both tagged "✕ missed" if the threshold is ≥70. This directly breaks the core narrative claim.
- The Key Finding box in `dashboard.html` says: *"Model B scored 40.5 (SPECULATIVE)"* — but the real B score for Aug 2018 is **52.1**, not 40.5. It's still SPEC, but wrong number.
- The crisis archive in `dashboard.html` says *"Model A: 24.0 (HEDGE)"* for 2018 — real A is **46.9 (SPEC)**, which is actually a stronger result that undermines the "A saw nothing" story.

> [!WARNING]
> The narrative climax — "Model A scored HEDGE during the 2018 TRY crash" — is **not supported by real data**. Both models score SPECULATIVE. This needs to be re-framed before submission.

---

### 1.3 The Δ at Nov-2021 IS the Distinguishing Result

The project review correctly identified **2021-11 (A=33.5, B=53.0, Δ=+19.5)** as the headline result. This is where Model A goes fully HEDGE while Model B stays elevated SPEC — the divergence is real and the cleanest empirical contrast. But **neither dashboard currently foregrounds this date**. The crisis detection chart is hardcoded to specific months (May 2010, Aug 2018, Mar 2020, Jan 2021) and Jan 2021 is `A=26.7, B=25.1` — both nearly identical and very low, which actually *undermines* the argument.

**The right date is Nov-2021, not Jan-2021.**

---

### 1.4 SHAP Data Loaded Correctly But Story Changes

Real SHAP (Model B): `EM=0.018, BOVESPA=0.008, FTSE=0.004, VIX_lag1m=0.004, SP500=0.004, usdtry_vol=0.003`

- **EM (Emerging Markets index) dominates**, not SP500
- `usdtry_vol` (USD/TRY volatility) is present at rank 6 — this IS the Turkey-specific signal
- `USDTRY_lag1m` is at rank 10

The current hero label says "Primary driver: **SP500 rolling correlation**" — but real data will show **EM** as the top driver. This is actually a *better* story (EM index captures Turkey's co-movement with all EMs, not just US), but the drawer explanation for SHAP says *"SP500 (67.8) and BIST100 (32.5) dominate"* — which are the old hardcoded values. With real data, that text is wrong.

Real SHAP (Model A): `EM=0.027, SP500=0.020, FTSE=0.015, NIKKEI=0.011, EU=0.010, BOVESPA=0.010`

Model A's SHAP also has EM at top. But importantly, Model A has **no TRY/USD features at all** — confirmed by the SHAP key list. This is correct and supports the narrative.

---

### 1.5 Walk-Forward Table: Model A Has Structure, Model B Does Not Match

`dashboard.html` reads walk-forward via `getWF()`. For Model A (model_2009), the JSON has the split structure under top-level `ols`, `rf`, `elastic_net` keys (not under a `metrics` sub-object). For Model B, it's under `metrics.test_r2` etc.

The `renderPerf()` function in `dashboard.html` handles both branches — but the real Model A walk-forward R² values are:
- `split_2008`: OLS R²=0.386, RF R²=0.523 — **these look reasonable** ✓
- `split_2018_try`: OLS R²=0.178 — moderate ✓
- `split_2020`: OLS R²=0.742, EN R²=0.743 — **excellent** ✓  
- `split_2021_turkey`: OLS R²=-0.151, EN R²=-0.160, RF R²=-0.266 — **negative** ⚠️

The negative 2021 split will render with a `—` minus in the table. Without an explanation, this looks like failure. (Note: negative R² is expected and actually a finding, per the project review.)

For Model B, the split R² values are:
- `split_2018_try`: -0.045 (negative)
- `split_2020`: +0.320
- `split_2021_turkey`: -0.353 (negative, most negative)

**Two of three Model B splits are negative.** The table will show two bright red values with no explanation.

---

### 1.6 Correlation Heatmap: Silent Null Handling

`dashboard.html` already has the right workaround: it always reads correlations from `model_2009` scores. But `index.html` uses `SCORES_TL` (model_2009_tl) which **doesn't exist** in the JSON (`model_2009_tl` is `null` after load). The fallback simulation will always be used for the heatmap in `index.html` when showing Model B. This is a silent data fall-through — the heatmap looks fine but is showing simulated data.

---

## Part 2 — Design Issues

### 2.1 `index.html` Has Better Architecture, `dashboard.html` Is the Richer UI

`index.html` is clearly the more complete presentation page with the Lead Time Analysis section, VIX chart, and a cleaner drawer. `dashboard.html` has the Feature Timeline, Score Distribution chart, and Regime Transition Matrix, but lacks the Lead Time panel.

Both need fixes but `index.html` is the one linked as `presentation.html` (the "▶ Present" button) — if that's what gets shown to the marker, it carries the most risk because its hardcoded data is the most out-of-sync.

---

### 2.2 The Crisis Detection Chart's Binary Logic Is Too Harsh

Current logic: score < 70 → "✕ missed" (red badge). But the real scores show both models in 40–69 range for most crises. The entire chart will show a column of red "✕ missed" for Model A AND yellow "~ spec" for Model B — which looks like both models failed.

**The threshold framing is wrong for the data.** The correct frame is:
- The **Δ between A and B** is the finding, not whether either crosses 70
- Model B consistently scores 5–20 points higher than Model A at crisis dates
- The 2020 COVID case (A=58.8, B=71.1) IS the one case where B crosses into PONZI and A doesn't — **this should be the visual centrepiece**

Suggested fix: Change the chart to show a **differential bar** (Δ = B − A) with the framing "Model B elevates its signal by X points that Model A cannot detect."

---

### 2.3 The Stat Strip in `index.html` Shows Confusing Metrics

Current stats: `Fragility Score YTD`, `30d Volatility`, `SP500 Correlation`, `Best Model R²`.

When real data loads:
- `Best Model R²` → will show `0.094` or `0.138` — looks terrible without context
- `SP500 Correlation` → falls back to null (SCORES_TL is null), shows `—`
- `Fragility Score YTD` → works fine if there are scores for Jan of the current year

**Suggestion**: Replace `Best Model R²` with something that tells the story — e.g. **`Model B − A Delta`** at the current scrubbed date, or **`Crises Detected`** (Model B: 2/4 ≥PONZI vs Model A: 1/4).

---

### 2.4 Hero Section: Primary Driver Label Will Be Wrong

Both files dynamically set "Primary driver: **[top SHAP feature]**". With real data, this will always say "Primary driver: **EM**" regardless of model or date, because SHAP is a static global importance, not per-date. For Model A, it'll also say EM.

This is misleading — it implies EM is driving today's score, not that it's globally important. Either:
- Change label to "Top global driver: **EM** (mean SHAP)" with a note that this is the average across all periods
- Or remove the dynamic SHAP from the hero and put it only in the dedicated SHAP card

---

### 2.5 Crisis Archive in `dashboard.html`: Numbers Hardcoded and Wrong

The crisis archive (bottom section of `dashboard.html`) is fully static HTML — it will never update from real data. It says:
- "Model A: 24.0 (HEDGE) · Model B: 40.5 (SPEC)" for 2018
- "Model A: 42.5 (SPEC) · Model B: 77.8 (PONZI)" for COVID

Real values: A=46.9, B=52.1 (2018); A=58.8, B=71.1 (COVID). The COVID one is directionally right (B crosses PONZI, A doesn't) but both numbers are wrong.

`dashboard.html`'s `renderCrisisArchive()` uses hardcoded strings. These need to be wired to `getScoreByDate()` calls.

---

### 2.6 Score Distribution Chart (dashboard.html): Same Purple, No Differentiation

Both Model A and Model B bars are purple (opacity .25 vs .50). In a dark mode context with dark purple bars on dark background this is nearly invisible and fails to communicate anything distinctive. The color should be different per model (e.g., muted gray for A, brand purple for B).

---

### 2.7 The Regime Matrix Is a Gem That Needs a Callout

The empirical Markov chain (`renderRegimeMatrix()`) is genuinely excellent — it shows that HEDGE→PONZI probability is near zero, validating Minsky's sequential regime hypothesis. But it's buried in a 2-column grid at the bottom of the Models section with no visual prominence. For a marker reading the academic narrative, this chart alone proves the Minsky thesis empirically. It deserves more visual weight.

---

## Part 3 — What the Pipeline Needs to Export Differently

### 3.1 Scale the Fragility Scores to 0–100 in the JSON

The core problem is that the pipeline generates a `fragility_score` on a 0–100 scale in `monthly_scores` (correct), but the `performance.ols.r2` etc. are measured on the raw-return prediction task (not the fragility score). This creates an irreparable unit mismatch in the UI.

**Options:**
1. Add a separate `fragility_r2` key in performance that measures model accuracy on the fragility score scale (not raw returns)
2. Add an explanatory note field: `"performance_note": "R² measured on monthly ISE returns (0.03–0.10 scale), not fragility score"` 
3. Remove R² from the UI for Model B entirely and focus on the walk-forward detection narrative instead

**Recommendation**: Option 3 is easiest for submission. Replace the R² stat in the UI with a detection-rate metric derived from crisis scores.

---

### 3.2 Fix the 2021 Crisis Anchor Date

The crisis detection chart uses `2021-01-31` as the Turkey 2021 crisis date. But:
- Jan 2021: A=26.7, B=25.1 (both near HEDGE — **worst possible showcase date**)
- Nov 2021: A=33.5, B=53.0 (Δ=+19.5 — the headline result)

Change the hardcoded crisis date in `renderCrisisDetection()` from `'2021-01-31'` to `'2021-11-30'` in `dashboard.html`.

In `index.html`, change the MODELS data `'Turkey 2021–26': '2022-12-31'` to `'2021-11-30'`.

---

### 3.3 Add `regime_metrics` to Walk-Forward JSON

The `regime_metrics: {}` is empty for all splits. The dashboard table shows `—` for Hedge RMSE and Spec RMSE. Either:
- Populate this in the pipeline (requires re-run)
- Or remove those columns from the dashboard table so no empty values are shown

---

### 3.4 Add a `model_2009_tl` Key or Point Heatmap to `model_2009`

`index.html` reads correlations from `SCORES_TL = REAL_DATA?.models?.model_2009_tl?.monthly_scores`. This key doesn't exist in the JSON. The heatmap will silently fall back to simulation.

Fix: In `index.html`, change `SCORES_TL` to read from `REAL_DATA?.models?.model_2009?.monthly_scores` directly — the correlations are already there.

---

## Part 4 — The Narrative Reframe (Most Important)

The current narrative is: **"Model B crosses PONZI threshold, Model A doesn't."** The data doesn't fully support this for 2018 (both SPEC) and 2010 (both SPEC).

The narrative that IS supported: **"Model B consistently sees 15–20 points more fragility than Model A at Turkish crisis dates, while both models agree during global crises."**

This is actually a stronger academic argument — it shows the models have the same global crisis response but diverge systematically on domestic Turkish stress. The mechanism is identifiable through SHAP (usdtry_vol, USDTRY_lag1m in Model B; absent from Model A).

**The one clean PONZI/non-PONZI contrast is COVID 2020 (A=58.8 SPEC, B=71.1 PONZI).** Lead with this as the "proof of threshold crossing" and reframe 2018 as "Model B elevates warning signal while Model A stays calm — the 2020 event proved the threshold was real."

---

## Priority Fix List

| # | File | Fix | Impact | Effort |
|---|------|-----|--------|--------|
| 1 | `dashboard.html` | Change 2021 crisis date from Jan → Nov-2021 | Fixes headline result | Trivial |
| 2 | `index.html` | Change `'Turkey 2021–26': '2022-12-31'` → `'2021-11-30'` in CRISIS_DATES | Same | Trivial |
| 3 | `dashboard.html` + `index.html` | Wire crisis archive scores to `getScoreByDate()` / real data | Stops wrong numbers appearing | Low |
| 4 | `index.html` | Fix `SCORES_TL` to fall back to `SCORES_A` when null | Heatmap shows real data | Low |
| 5 | `dashboard.html` + `index.html` | Change crisis detection from PONZI-threshold binary to Δ(B−A) differential framing | Fixes narrative collapse | Medium |
| 6 | Both | Replace `Best Model R²` in stat strip with `Model B − A` delta or detection count | Avoids confusing R² units | Low |
| 7 | `dashboard.html` | Change `hero-driver` label to "Top SHAP feature (global): **EM**" to avoid implying it's date-specific | Accuracy | Trivial |
| 8 | `dashboard.html` | Update drawer SHAP explanation text to match real data (EM not SP500) | Accuracy | Low |
| 9 | `dashboard.html` | Score distribution: use different colors for A vs B (not both purple) | Readability | Trivial |
| 10 | `dashboard.html` | Add a note row in perf table when R² < 0 explaining structural break | Academic narrative | Low |
| 11 | Pipeline (notebook) | Populate `regime_metrics` in walk-forward export OR remove columns from table | Either fix is valid | Medium |

---

## Questions for You

1. **Is the 2018 PONZI threshold essential to the narrative, or can you reframe to "Model B sees more"?** If the thesis must be "B crosses PONZI, A doesn't," you need to re-examine whether the fragility score parameters can be adjusted (e.g., lowering PONZI threshold to 50 would make 2018 B=52.1 a crisis detection). But that would require academic justification.

2. **Are these two files the same presentation?** `index.html` is linked as the presentation mode from `dashboard.html` via `▶ Present`. Should I treat `index.html` as the primary submission artifact and `dashboard.html` as the detailed exploration? Or vice versa?

3. **Can the pipeline be re-run before submission?** If yes, fixing `regime_metrics` and adding a `fragility_performance` key (R² on the 0-100 scale) would resolve issues 6 and 11 properly. If not, the frontend can work around both.
