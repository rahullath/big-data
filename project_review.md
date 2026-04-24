# Financial Fragility Clock — Full Project Review
**Group 5 · MSc FinTech Big Data Management · Deadline: 7 May 2026**
**Reviewed: 2026-04-24**

---

## TL;DR

The technical work is solid and the academic narrative is genuinely original. The core distinction-level argument — Model A misses domestic Turkish crises while Model B catches them — is **empirically confirmed** in the output data. The pipeline runs end-to-end, all notebooks have outputs, all models are saved. 

**However, there are specific gaps that will cost marks against the rubric**, particularly in Criteria 2 (50% weight) and Criteria 3 (20%). These are fixable before submission.

---

## 1. What's Working Well ✅

### Section 1 (EDA)
- All 29 cells have outputs. No empty cells.
- IQR + Z-score dual outlier detection is methodologically sound and well-justified.
- Winsorisation decision is argued correctly (preserving crisis observations vs. removal).
- Normality finding (Shapiro-Wilk, all p < 0.05) is correctly linked forward to model selection.
- Correlation analysis notes the DAX/FTSE/EU multicollinearity cluster — essential for VIF discussion in Section 2.
- Summary cell (1.13) is detailed and carries findings forward cleanly.

### Section 2 (Model Build)
- All 52 cells have outputs. No errors.
- Six models implemented: OLS, Ridge, LASSO, ElasticNet, RF, MLP — this is comprehensive and clearly satisfies Criteria 2.
- **Ridge collapsing to OLS** (α=0.0001, identical coefficients) is documented and explained — this is a distinction-quality observation.
- **ElasticNet l1_ratio=0.70** selected: the sparsity-vs-shrinkage decision is articulated in the markdown.
- **Classification task** (RF Classifier, AUC=0.888) is included alongside regression — this directly addresses the assignment brief's ambiguity.
- SHAP added as §2.17 — beeswarm, waterfall, multi-model mean|SHAP| comparison, RF classifier SHAP. All saved and shown.
- Models saved to `models/*.pkl`, scaler saved.

### Section 3 (Model B)
- All 49 cells have outputs. No errors.
- Overlap check: **r=0.9826** — ISE_USD derivation from yfinance aligns with original dataset. This is a critical data integrity proof.
- Two-layer architecture (Layer 1: prediction, Layer 2: fragility score) is correctly kept separate — fragility score does NOT use model predictions.
- Incremental feature block comparison (Stages 1–4) is present and shows progressive RMSE.
- Walk-forward validation: 4 splits for Model A, 3 for Model B.
- **Key academic contrast confirmed:**

| Date | Model A | Model B | Δ | Interpretation |
|------|---------|---------|---|----------------|
| 2021-11 | 33.5 (PONZI) | 53.0 (PONZI) | +19.5 | **Headline result** — global calm, Turkey crisis |
| 2018-08 | 46.9 (PONZI) | 52.1 (PONZI) | +5.2 | TRY crash — B slightly elevated |
| 2009-03 | 53.3 (PONZI) | 63.8 (PONZI) | +10.5 | GFC — both catch |
| 2020-03 | 58.8 (PONZI) | 71.1 (PONZI) | +12.3 | COVID — VIX + TRY elevates B |

- Section 3 summary (Cell 48) is substantial and links Minsky's FIH framework to the empirical findings.
- `fragility_output.json` generated: 229 Model A scores + 280 Model B scores, schema v2.0 ✓

---

## 2. Issues That Will Cost Marks ⚠️

### 🔴 CRITICAL (Criteria 2, 50% weight)

#### C2-1: Model B performance metrics are weak and not adequately explained
```
Model B OLS:   R²=0.094, RMSE=0.0956  (vs Model A OLS: R²=0.827)
Model B EN:    R²=0.090, RMSE=0.0958  (EN collapses to 1 active feature out of 33)
Model B RF:    R²=0.138, RMSE=0.0933
```
The EN collapses to **1 active feature** (likely EM). This is a legitimate finding but it's currently not addressed in a markdown cell — a marker will see "Active features: 1 / 33" in the output and wonder if it's a bug. **This needs a markdown explanation:** EN's regularisation selects only the most stable linear predictor on a 23-year period with structural breaks; the fragility score framework compensates by using the raw features directly rather than model coefficients.

#### C2-2: Walk-forward negative R² is unexplained
```
Model A split_2021_turkey: OLS R²=-0.15, EN R²=-0.16, RF R²=-0.27
Model B split_2021_turkey: OLS R²=-0.35, EN: not in JSON
```
Negative R² means the model performs worse than predicting the mean. This is actually *expected* (the models are trained on pre-crisis data predicting a structurally different crisis period), but without a markdown cell explaining this, a marker will flag it as a failure. **Add an explanation:** Out-of-sample R² < 0 in structural break periods is expected and documented in the financial forecasting literature (cite Goyal & Welch, 2008 or similar).

#### C2-3: Model B walk_forward is missing split_2008
Model A has 4 walk-forward splits. Model B only has 3 (missing `split_2008`). The JSON confirms:
```
model_2009: 4 splits (split_2008, split_2018_try, split_2020, split_2021_turkey)
model_2003: 3 splits (split_2018_try, split_2020, split_2021_turkey)
```
For Model B, split_2008 is the GFC test — you can argue it's less relevant since Model B is trained on the full 2003–2026 window (training data includes GFC). But this should be explicitly stated in the notebook. If data permits, add the GFC split for completeness.

#### C2-4: regime_metrics in walk_forward JSON is empty `{}`
```json
"regime_metrics": {}
```
The SECTION3_REFERENCE.md specifies regime-split RMSE (HEDGE/SPECULATIVE/PONZI per split). The notebook outputs "Regime-split RMSE will be computed during JSON export (needs fragility scores)" — but the JSON shows empty dicts. This means the regime-level analysis promised in the spec is missing from the final output. A marker comparing the narrative to the output will notice this gap.

#### C2-5: Section 3 markdown cells for subsections 3.2–3.17 are nearly empty
Most markdown cells in Section 3 contain **only a heading** with no explanatory text:
```
## 3.4 Rolling Features (daily computation, month-end resampling)
[no body]

## 3.7 Regime Labelling
[no body]
```
The Section 3 intro (Cell 0) and summary (Cell 48) are excellent. But the middle of the notebook is just code without prose. For Criteria 2 (exhaustive discussion) and Criteria 4 (critical argument), **each subsection needs 2–4 sentences explaining what it does and why**, especially for: ISE_USD derivation (3.3), fragility score design choices (3.13), SHAP mechanism analysis (3.14).

---

### 🟡 IMPORTANT (Criteria 3, 20% weight)

#### C3-1: Section 2 markdown cells are methodologically strong but lack citations
The markdown cells explain *why* each model is chosen (e.g., "MLP on 536 rows → CV_RMSE=6× test RMSE, known limitation of ANNs on small datasets") but **don't cite any academic sources**. Distinction requires "excellent depth of classic and contemporary reading." Minimum citations needed:
- OLS baseline → cite Malkiel (1973) efficient market hypothesis for financial returns
- LASSO feature selection → Tibshirani (1996)
- ElasticNet → Zou & Hastie (2005)
- RF for financial time series → cite a recent paper (e.g., Gu, Kelly & Xiu 2020 "Empirical Asset Pricing via Machine Learning")
- MLP limitation on small samples → cite Goodfellow et al. (2016) or a recent FinML paper
- SHAP → Lundberg & Lee (2017)
- Minsky FIH (Section 3) → Minsky (1986) "Stabilizing an Unstable Economy"

#### C3-2: No literature cited for the "churn variable" note
The team plan explicitly says to note the brief's copy-paste error ("churn" → feature importance for ISE). This should appear as a footnote or brief sentence in Section 2, with a reference to demonstrate critical reading of the brief.

---

### 🟡 IMPORTANT (Criteria 4, 20% weight)

#### C4-1: Section 3 SHAP mechanism analysis is not fully argued
The summary (Cell 48) states: "Elastic Net collapses to EM-only → this finding MOTIVATES the use of RF and the fragility score framework." This is the right conclusion but the notebook doesn't have a cell that actually shows the period-specific SHAP breakdown (pre_2007, crisis_2008, crisis_2018, crisis_2021). SECTION3_REFERENCE.md specifies these. Cell 36 computes period-specific SHAP, but there's no output showing what domainates in each period — which is the mechanism-level proof that distinguishes "B works" from "why B works."

#### C4-2: Limitations section is incomplete
Section 2 (§2.16) mentions the MLP limitation. But a distinction-level submission needs a consolidated **limitations section** covering:
- Look-ahead bias risk (walk-forward mitigates this, but should be stated)
- PONZI crisis labels are hard-coded anchors — not model-derived; this is a design choice that needs justification
- 536 daily observations in Section 2 is a small sample for ML; how does this affect conclusions?
- yfinance data quality (survivorship bias, ticker changes over 23 years)

---

### 🟢 MINOR (Criteria 1, 10% weight)

#### C1-1: Section 3 notebook ends with `##` as Cell 48 heading
Cell 48 is titled `#` with no text body — this is a placeholder. Doesn't break anything but looks unfinished.

#### C1-2: The `brent` feature shows `None` for early Model A scores
```json
"features": {"vix": 12.947, "dxy": 82.175, "brent": null, "try_usd": 0.740}
```
This is because BRENT data isn't available for 2007 in Model A's scope. The dashboard needs to handle `null` gracefully — check `index.html` renders these without crashing.

#### C1-3: Model B `monthly_scores` starts 2003-01 with all-`null` correlations
The first ~51 months (60d rolling window warmup) have `null` correlations. This is expected but should be documented in the notebook.

---

## 3. Priority Fix List (ordered by mark impact)

| # | Fix | Criteria | Effort |
|---|-----|----------|--------|
| 1 | Add markdown cells to §3.3, §3.7, §3.13, §3.14 explaining *why* each design choice was made | C2 (50%) | Medium |
| 2 | Add markdown cell explaining Model B EN collapse to 1 feature — it's a finding, not a failure | C2 (50%) | Low |
| 3 | Add markdown cell explaining negative walk-forward R² in structural break periods | C2 (50%) | Low |
| 4 | Add citations throughout Section 2 markdown (OLS, LASSO, EN, RF, SHAP, Minsky) | C3 (20%) | Medium |
| 5 | Add period-specific SHAP output showing which features dominate in each crisis | C4 (20%) | Medium |
| 6 | Add a consolidated Limitations section to Section 2 or 3 | C4 (20%) | Low |
| 7 | Fix regime_metrics in JSON or add note explaining why it's empty | C2 (50%) | Low |
| 8 | Add split_2008 for Model B or explicitly note why it's excluded | C2 (50%) | Low |
| 9 | Note the "churn" brief copy-paste error in Section 2 | C3 (20%) | Trivial |

---

## 4. What's Already at Distinction Level

The following are genuinely strong:

- **Overlap check r=0.9826** — proves ISE_USD derivation is methodologically consistent with the provided dataset. Very few groups would do this.
- **Ridge = OLS finding** (α=0.0001) — shows understanding of regularisation, not just application of it.
- **Two-layer architecture** (prediction vs fragility score separated) — prevents circular dependency; shows methodological rigour.
- **Incremental feature block testing** (Blocks 1–5 in §3.9) — systematic justification for feature inclusion, not just adding everything.
- **2021-11 contrast (A=33.5, B=53.0)** — during global market calm (S&P at ATH, VIX low), Model B correctly elevates via domestic TRY signals. This is a publishable-quality finding.
- **CBRT governor dummy** — links an institutional event (central bank governor firing) to a quantitative feature. LO3 (ethical data design) territory.
- **SHAP added to Section 2** — this goes beyond what's required and directly addresses "variable contribution" from the brief.

---

## 5. Notebook Execution Status

| Notebook | Cells | Cells with output | Errors |
|----------|-------|-------------------|--------|
| section1_eda.ipynb | 29 | ~25 (code cells) | None |
| section2_model_build.ipynb | 52 | All code cells | None |
| section3_model_b.ipynb | 49 | All code cells | None |

All models saved: `elasticnet.pkl`, `lasso.pkl`, `mlp.pkl`, `ols.pkl`, `randomforest.pkl`, `rf_classifier.pkl`, `ridge.pkl`, `scaler.pkl`

Pipeline output: `data/fragility_output.json` — 267 KB, schema v2.0, both models present.

> [!NOTE]
> The notebooks run under `/home/rahul/jupyter-venv`. Make sure teammates open notebooks with this kernel if they re-run anything.

