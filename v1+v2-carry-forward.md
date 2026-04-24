# V1 + V2 Carry-Forward: Best Parts of Both Previous Attempts

## What this document is and is not

Three repos exist. Understanding which is which prevents confusion:

| Repo | Location | Description | Status |
|---|---|---|---|
| **V1** | `~/dev/fragility-clock/` | React + Python pipeline. Full visualisations, wrong modelling. | Abandoned |
| **V2** | `~/dev/big-data-challenge/` | HTML dashboard + Turkey-specific Python pipeline. Good design and Turkey focus, no Model A grounding. | Abandoned |
| **Active** | `~/dev/model-a/` | Clean slate. Section1 + Section2 ipynb done. Section3 + dashboard next. | **Working here** |

**What's already in the active repo (not "carry-forward"):** `section1_eda.ipynb`, `section2_model_build.ipynb`, `models/*.pkl`, `plots/`, `group5_clean_data.csv`, `Financial Fragility Clock v2.html`, `learnings.txt`, `plan-1.txt`. These were copy-pasted into this directory (`fragility-clock/`) as reference context only — they live in the active repo and don't need to move.

**What this document covers:** two sources of inspiration for the section3 notebook and the v2.html dashboard:
- **From V1** (fragility-clock React/Python): visualisation patterns and analytical ideas from `src/components/` and `python/`
- **From V2** (big-data-challenge Python): correct feature engineering, fragility formula, walk-forward splits, crisis validation logic from `python/model_b/`

Nothing here requires moving files. Everything is a pattern to reproduce.

---

## Part 1: Visualisation Inventory (Port to HTML Dashboard)

The v2.html has a solid design shell. Below is every visualisation from the V1 React app worth adding or upgrading, with exact implementation notes for vanilla SVG/JS.

---

### 1.1 Full Correlation Matrix (NxN, not just ISE row)

**What V1 did:**  
`CorrelationHeatmap.tsx` rendered a full NxN SVG grid of 60-day rolling Pearson correlations across all indices. It showed every pairwise relationship — not just ISE vs others. On hover, it showed the exact value AND a 30-day delta (whether the correlation had risen or fallen).

**Why it matters:**  
The v2.html currently only shows one row: ISE vs each other market (`heatmapCorr` function returns 7 values for a single row). This misses the whole point of correlation-as-fragility. The academic argument is that *contagion spreads when ALL markets move together*, which is only visible in the full matrix. The eigenvalue concentration story (a single dominant eigenvalue = systemic lockup) only makes sense when you can see the full matrix going red.

**How to port:**  
Replace the current `.hmap` single-row display with a proper NxN grid. The colour scale should be RdBu diverging (red = strong positive correlation, blue = negative/zero). Key additions over v2.html's current heatmap:

```javascript
// Full NxN grid — replace updateHeatmap() in v2.html
function buildFullHeatmap(monthIdx) {
  const row = DATA.models[currentModel].monthly_scores[monthIdx];
  const pc = row.pairwise_correlations; // { "SP500_DAX": 0.74, "SP500_FTSE": 0.81, ... }
  const indices = ['SP500','DAX','FTSE','NIKKEI','BOVESPA','EU','EM','ISE_USD'];
  const n = indices.length;

  // Build NxN matrix from flat pairwise dict
  const matrix = Array.from({length: n}, (_, i) =>
    Array.from({length: n}, (__, j) => {
      if (i === j) return 1;
      const k1 = `${indices[i]}_${indices[j]}`;
      const k2 = `${indices[j]}_${indices[i]}`;
      return pc[k1] ?? pc[k2] ?? null;
    })
  );

  // Hover: show value + 30-day delta vs prevMonthIdx
  // Use CSS transition: fill 300ms ease on each rect
}
```

**Hover tooltip** must show: `INDEX_A × INDEX_B | r = 0.74 | Δ30d = +0.12↑`. The delta colouring should be red for rising correlation (increasing contagion risk) and green for falling.

**section3 JSON must export:** `pairwise_correlations` as a flat dict per monthly score row, with keys like `"SP500_DAX"`. This is the single most important structured data field for the dashboard.

---

### 1.2 Regime-Coloured Timeline Gradient

**What V1 did:**  
`RegimeTimeline.tsx` rendered the fragility score area chart with the fill gradient coloured by regime — green fill during HEDGE periods, amber during SPECULATIVE, red during PONZI. It was computed by sampling regime at every ~1% of the data range and building a horizontal `linearGradient` with stops. It also drew:
- Dashed reference lines at y=33 (HEDGE/SPEC boundary) and y=67 (SPEC/PONZI boundary)
- A vertical cursor line at the selected date
- Labelled vertical crisis annotation lines for each known event

**Why it matters:**  
The v2.html timeline (`drawTimeline`) already draws the score line and crisis pins, but the fill is a flat purple gradient. The regime-coloured fill makes the Minsky narrative *visible at a glance* — you see the whole 2003–2026 arc as a colour story: green GFC recovery, amber drift, red 2008, long amber, red again 2020, amber/red 2021+.

**How to port:**  
In `drawTimeline()`, replace the static fill gradient with a regime-derived one:

```javascript
function buildRegimeGradient(scores) {
  const total = scores.length;
  return scores
    .filter((_, i) => i % Math.max(1, Math.floor(total / 120)) === 0)
    .map((s, i, arr) => ({
      offset: (i / Math.max(arr.length - 1, 1) * 100).toFixed(1) + '%',
      color: s.regime === 'PONZI' ? '#dc2626'
           : s.regime === 'SPECULATIVE' ? '#d97706'
           : '#22c55e'
    }));
}
```

Also add threshold lines at the 33 and 67 score levels as dashed horizontals on the timeline SVG — the v2.html version doesn't have these and without them the HEDGE/SPEC/PONZI zones are invisible.

---

### 1.3 Clickable Timeline → Scrubber Sync

**What V1 did:**  
Clicking anywhere on the `RegimeTimeline` area chart updated `DateContext.selectedDate`, which drove every other component to re-render for that date. Click on 2008-10 → clock hand moves, heatmap updates, SHAP updates, stats update.

**Why it matters:**  
The v2.html has a slider scrubber but clicking the timeline SVG directly doesn't move the scrubber. This is a significant UX gap — for a presentation the click-to-navigate behaviour makes the dashboard feel like a live instrument rather than a static chart.

**How to port:**  

```javascript
svg.addEventListener('click', function(e) {
  const rect = svg.getBoundingClientRect();
  const x = e.clientX - rect.left - PAD.l;
  const idx = Math.round((x / chartWidth) * (DATA.models[currentModel].monthly_scores.length - 1));
  if (idx >= 0) {
    currentMonthIdx = idx;
    updateAll(); // re-render clock, stats, heatmap, SHAP, VIX
  }
});
```

---

### 1.4 Feature Importance Over Time (Rolling SHAP)

**What V1 did:**  
`FeatureImportanceTimeSeries.tsx` showed how each feature's SHAP contribution changed month by month as a multi-line chart. It had:
- Toggle-able legend (click feature name to hide/show its line)
- "Significant change" badge (!) when a feature's importance range exceeded 50% of its mean
- Features sorted by average importance, top N shown

**Why it matters:**  
This chart is analytically essential for the model comparison story. For Model A, you'd see `ise2` dominating with flat low contributions from global indices. For Model B, you'd see `USDTRY` and `VIX` spike around 2018 and 2021 while staying flat in 2009. This is the proof that Model B is capturing what Model A couldn't.

**How to port:**  
Add as a new chart section in v2.html. The data lives in `fragility_output.json` under `models[m].feature_importance_timeseries`:

```javascript
function drawFeatureImportanceTimeline() {
  const fits = DATA.models[currentModel].feature_importance_timeseries;
  const features = Object.keys(fits[0].feature_importance);
  const colors = ['#3b82f6','#ef4444','#10b981','#f59e0b','#8b5cf6','#ec4899','#14b8a6'];
  // Draw one SVG path per feature, same PAD/scale approach as updateVixChart
  // Annotate with vertical lines at 2018-08 and 2021-03
}
```

**section3 must export:** `feature_importance_timeseries` array with monthly granularity for the full 2003–2026 range.

---

### 1.5 Regime Transition Matrix

**What V1 did:**  
`RegimeTransitionMatrix.tsx` showed a 3×3 heatmap of Minsky regime transition probabilities (HEDGE→HEDGE, HEDGE→SPEC, etc.), computed empirically from the historical regime sequence. Used YlOrRd scale. Current regime row highlighted. Hover: exact transition name and probability.

**Why it matters:**  
Empirical Markov transitions from the 2003–2026 regime sequence give a genuinely interesting result: PONZI→PONZI has high persistence (crises last); HEDGE→PONZI is near-zero (no sudden collapses without an intermediate SPECULATIVE phase — Minsky's point exactly). This validates the model's theoretical grounding in one 3×3 table.

**How to port:**  

```javascript
function computeTransitionMatrix(scores) {
  const regimes = ['HEDGE','SPECULATIVE','PONZI'];
  const counts = Object.fromEntries(regimes.map(r => [r, Object.fromEntries(regimes.map(t => [t, 0]))]));
  for (let i = 1; i < scores.length; i++) {
    const from = scores[i-1].regime, to = scores[i].regime;
    if (counts[from] && counts[from][to] !== undefined) counts[from][to]++;
  }
  return regimes.map(from => {
    const rowTotal = regimes.reduce((s, t) => s + counts[from][t], 0);
    return regimes.map(to => rowTotal > 0 ? counts[from][to] / rowTotal : 0);
  });
}
```

Render as a 3×3 coloured grid. Current regime row gets a border highlight.

---

### 1.6 Network MST (Minimum Spanning Tree of Market Correlations)

**What V1 did:**  
`NetworkMST.tsx` built a force-directed D3 graph using Mantegna distances (`sqrt(2(1-corr))`), then ran Kruskal's MST. Node size ∝ betweenness centrality. Node colour ∝ rolling volatility.

**Why it matters:**  
In normal markets, ISE_USD sits as a peripheral leaf node. During 2018 TRY crisis and 2021 Turkey crisis, ISE_USD's edge to DXY/USDTRY becomes the shortest edge in the tree — it becomes a central node. Direct visual proof that Turkey's fragility mechanism is different from global EM contagion.

**How to port:**  
Use a circular layout fallback (no force simulation needed) — nodes on a circle, edges drawn with Mantegna distance controlling opacity and thickness. Achievable in ~80 lines of pure SVG. **section3 must export** `pairwise_correlations` per monthly score (same dict needed for heatmap — no extra export required).

---

### 1.7 Volatility Clustering Chart

**What V1 did:**  
`VolatilityClusteringChart.tsx` plotted rolling volatility over time with shaded `<ReferenceArea>` rectangles for contiguous high-vol clusters (>1.5× historical mean). Shade opacity ∝ cluster intensity. Historical average as dashed line.

**Why it matters:**  
The v2.html VIX overlay shows VIX vs fragility score but not ISE-specific volatility clustering. The 2018 and 2021 Turkey crises produce ISE volatility clusters when VIX is calm — core evidence for Model B's superiority.

**How to port:**  

```javascript
function findVolatilityClusters(scores, threshold = 1.5) {
  const vols = scores.map(s => s.components.rolling_vol);
  const avgVol = vols.reduce((s,v) => s+v, 0) / vols.length;
  const clusters = [];
  let inCluster = false, start = 0;
  vols.forEach((v, i) => {
    if (v > avgVol * threshold && !inCluster) { inCluster = true; start = i; }
    else if (v <= avgVol * threshold && inCluster) {
      inCluster = false;
      clusters.push({start, end: i-1, intensity: vols.slice(start,i).reduce((s,x)=>s+x,0)/(i-start)/avgVol});
    }
  });
  return clusters;
}
```

---

### 1.8 Lead Time Analysis

**What V1 did:**  
`LeadTimeAnalysis.tsx` computed how many days in advance the model's fragility score crossed the PONZI threshold before each known crisis. It showed a histogram of lead time distribution (10-day bins), a scatter of crisis date vs lead time, a Model A vs B comparison box plot, and summary stats.

**Why it matters:**  
This directly answers "is this model actually useful?" If Model B crosses the PONZI threshold an average of 45 days before each Turkey crisis and Model A misses 2018/2021 entirely, the lead time comparison is the killer evidence slide. The v2.html has fake hardcoded `renderLeadTime()` bars that need replacing.

**section3 must export:** `crisis_lead_times` array with `{crisis_name, crisis_date, model_a_first_warning, model_b_first_warning, model_a_lead_days, model_b_lead_days}`.

---

### 1.9 Model Performance Table with Regime-Split RMSE

**What V1 did:**  
`ModelPerformanceTable.tsx` showed the performance table broken out by regime — separate RMSE columns for HEDGE, SPECULATIVE, PONZI rows. Auto-highlights when RF outperforms OLS specifically in the PONZI regime.

**Why it matters:**  
A model with good overall RMSE might still fail precisely during PONZI crises. For Model B the story is: overall metrics modestly improve vs Model A, but PONZI-regime RMSE drops substantially. That's the academic result.

**How to port:**  
Add HEDGE RMSE, SPEC RMSE, PONZI RMSE columns to the existing `renderPerf()` table:

```python
# In section3 notebook
for regime in ['HEDGE','SPECULATIVE','PONZI']:
    mask = [r == regime for r in regime_labels_test]
    regime_rmse[regime] = np.sqrt(mean_squared_error(y_test[mask], y_pred[mask]))
```

---

## Part 2: Feature Engineering Gold (From V1 Python)

These computations from V1's `python/model_b/feature_engineering_b.py` were implemented correctly and should be reproduced in section3.

---

### 2.1 60-Day Rolling Pairwise Correlations (Full Matrix)

`compute_rolling_correlation()` correctly builds the full NxN Pearson matrix per day using `window_data.corr()`, extracts the upper triangle, computes `mean_corr = np.mean(np.abs(upper_triangle))` and `corr_concentration = np.var(upper_triangle)`, and stores all pairwise correlations as flat columns `INDEX_A_INDEX_B`.

**Carry forward as-is.** Only change: use 8 indices (SP500, DAX, FTSE, NIKKEI, BOVESPA, EU, EM, ISE_USD) not the 13 Istanbul-irrelevant ones from V1.

**Critical:** run rolling correlation on daily data and resample result to month-end. Do not compute correlation on monthly returns — with N=1 observation per pair per period there's no variance.

---

### 2.2 Permutation Entropy

`compute_permutation_entropy()` with `m=3, delay=1, window=30`. Non-parametric complexity measure that falls before crises (markets become more "orderly" as panic behaviour synchronises). Normalisation: `entropy / log(factorial(m))` maps to [0,1]. Invert as `1 - PE` in the fragility formula.

**Carry forward verbatim.** Compute on ISE_USD daily returns then resample to monthly mean.

---

### 2.3 Eigenvalue Concentration Ratio

`eigenvalue_ratio = max_eigenvalue / sum(eigenvalues)` from the NxN correlation matrix. When high, all markets move together. Directly related to PCA: ratio → 1/N means fully decorrelated, ratio → 1.0 means single dominant factor = systemic lockup.

Keep the `try/except` around `np.linalg.eigvalsh` with `np.isfinite` guard — monthly data with short windows can produce singular matrices.

---

### 2.4 Volatility Synchrony

`volatility_synchrony = window_data.std().mean()` — mean of per-market standard deviations in the rolling window. Use as a secondary diagnostic component at 0.10–0.15 weight.

---

### 2.5 Fixed Fragility Score Weights (Corrected from V1 — TRY_weakness is primary)

**The V1 formula was wrong.** The V2 big-data-challenge pipeline (`feature_engineering_b.py`) has the correct formula. The key difference: `TRY_weakness` carries 30% weight, not DXY at 10%.

```python
# Correct V2 formula (from big-data-challenge/python/model_b/feature_engineering_b.py)
fragility_score = (
    0.20 * corr_n        +   # mean_abs_pairwise_corr (60d)
    0.15 * pe_inv        +   # 1 - permutation_entropy (30d on ISE_USD)
    0.10 * vol_n         +   # ISE_USD.rolling(30).std()
    0.10 * eig_n         +   # λ_max / Σλ from NxN matrix
    0.15 * vix_n         +   # normalised VIX level
    0.30 * try_weakness  +   # 1 - norm(TRY_USD): the core Turkey signal
) * 100.0
```

| Component | Weight | Rationale |
|---|---|---|
| rolling_corr | 0.20 | Contagion synchronisation |
| pe_inv | 0.15 | Complexity collapse before crises |
| rolling_vol | 0.10 | Direct volatility elevation |
| eigenvalue_ratio | 0.10 | PCA concentration = systemic lock-up |
| vix | 0.15 | Global risk aversion signal |
| **try_weakness** | **0.30** | **Core Turkey signal: 1 - norm(TRY_USD)** |

**Normalisation:** use 2nd–98th percentile clipping (`quantile(0.02)` and `quantile(0.98)`) instead of min-max. This prevents outlier crises from compressing all other variation to zero.

```python
def _norm(series):
    lo, hi = series.quantile(0.02), series.quantile(0.98)
    return (series.clip(lo, hi) - lo) / (hi - lo + 1e-8)
```

**TRY_weakness derivation:** `try_weakness = 1 - _norm(TRY_USD_series)`. A strong dollar-vs-lira = high fragility (1 - normalised value inverts direction). This single component explains why 2018-08 scores ~68 (PONZI) in Model B while Model A misses it entirely.

**Do not use dynamic weight redistribution** when components are missing. Fixed weights; accept NaN for unavailable months.

---

### 2.6 Regime Classification (Corrected Crisis Dates — Turkey Crises Added)

The V1 crisis anchor list only covered 2008 and 2020. The V2 `regime_labeling_b.py` has the correct Istanbul-specific list:

```python
CRISIS_PERIODS = [
    ('2008-09-01', '2009-03-31', 'PONZI', '2008 Global Financial Crisis'),
    ('2018-05-01', '2018-11-30', 'PONZI', '2018 Turkish Currency Crisis'),   # ← V1 missing
    ('2020-03-01', '2020-04-30', 'PONZI', 'COVID-19 Market Crash'),
    ('2021-03-01', '2022-01-31', 'PONZI', '2021-22 Turkish Lira Collapse'),  # ← V1 missing
]
```

**The two Turkey-specific crises (2018 and 2021) are the academic core of Model B.** Without them, the hard-coded PONZI anchors cover only global crises and the classifier is identical to something trained purely on international data.

Additional regime logic to carry forward from V2:
- **Adaptive thresholds**: `rolling(252, min_periods=60).quantile(0.75)` for HEDGE/SPEC boundary; `.quantile(0.90)` for SPEC/PONZI boundary in non-crisis periods
- **Confidence score**: count how many components individually indicate PONZI range → export as `regime_confidence` (0–1) per monthly row
- **Signal availability audit**: track how many non-NaN fragility components were available for each observation — important for 2003–2009 when VIX data may be sparse

---

### 2.7 ISE_USD Construction

`ISE_USD = log_return(BIST100 / USDTRY)` — the fundamental Turkey-specific signal. Monthly: sum daily log-returns (log-returns are additive — do NOT average or use last-day level).

**Overlap verification in section3 §2:** cross-check 2009-01 to 2011-08 of the yfinance-derived ISE_USD against the `ise2` column in `group5_clean_data.csv`. Correlation should be >0.90 to confirm you're measuring the same thing.

---

## Part 3: V2 Pipeline Patterns (New — From big-data-challenge)

These patterns were implemented correctly in V2 and are not in V1 or the current active repo at all. They should be reproduced in section3.

---

### 3.1 Lag Features for Leading Indicators

V2's `feature_engineering_b.py` adds lagged versions of the main macro variables:

```python
LAG_FEATURES = ['DXY', 'TRY_USD', 'US_10Y_YIELD', 'BRENT', 'VIX']
LAG_MONTHS   = [1, 3, 6, 12]

def add_lag_features(df):
    for feat in LAG_FEATURES:
        for lag in LAG_MONTHS:
            df[f'{feat}_lag{lag}m'] = df[feat].shift(lag)
    return df
```

This is analytically important: lagged DXY and TRY_USD at 3m and 6m horizon let the model learn that dollar strength and lira weakness *precede* Istanbul fragility, not just correlate with it contemporaneously. The 6m and 12m lags capture slow-building macro stress.

**Use in section3.** All lag features should be in the Elastic Net feature set; LASSO will prune the unhelpful ones.

---

### 3.2 Four Turkey-Specific Walk-Forward Splits

V1 used generic train/test splits. V2's `models_b.py` defines four walk-forward splits with Turkey-specific rationale:

```python
walk_forward_splits = {
    'split_2008': {
        'train': ('2003-01-01', '2007-12-31'),
        'test':  ('2008-01-01', '2008-12-31'),
        'rationale': 'GFC — global crisis, both models should catch'
    },
    'split_2018_try': {
        'train': ('2003-01-01', '2017-12-31'),
        'test':  ('2018-01-01', '2018-12-31'),
        'rationale': 'TRY crash — Turkey-specific, Model A trained on 2009 should miss this'
    },
    'split_2020': {
        'train': ('2003-01-01', '2019-12-31'),
        'test':  ('2020-01-01', '2020-12-31'),
        'rationale': 'COVID — global shock, both models expected to catch'
    },
    'split_2021_turkey': {
        'train': ('2003-01-01', '2020-12-31'),
        'test':  ('2021-01-01', '2024-12-31'),
        'rationale': 'Prolonged Turkey crisis — long out-of-sample test for Model B'
    }
}
```

**The split_2018_try and split_2021_turkey are the key ones.** They test exactly the thesis: Model A misses Turkish-specific crises because it was trained on a global-crisis window. Report walk-forward RMSE for each split separately, not just one aggregate test metric.

---

### 3.3 USDTRY Volatility as a Separate Feature

V2's `fetch_turkish_macro.py` derives:

```python
USDTRY_ret    = np.log(df['USDTRY']).diff()
USDTRY_vol30  = USDTRY_ret.rolling(30).std() * np.sqrt(252)  # annualised
```

This is *different* from TRY_weakness (which is the level/direction of USDTRY). USDTRY_vol30 is the *speed of lira deterioration*. In 2018-08, TRY_weakness was high AND USDTRY_vol30 spiked — both were active. In gradual devaluations, TRY_weakness is high but vol30 is moderate. Include both as features in the Elastic Net feature set; they capture different aspects of lira stress.

---

### 3.4 TURKISH_CRISIS_EVENTS Annotation List

V2 has a precise list of 7 annotated Turkey events that should be the `crisis_annotations` in the dashboard and the ground truth for crisis detection evaluation:

```python
TURKISH_CRISIS_EVENTS = [
    {'date': '2018-05-23', 'event': 'TRY pressure begins', 'type': 'currency'},
    {'date': '2018-08-10', 'event': 'TRY freefall',        'type': 'currency'},
    {'date': '2021-03-20', 'event': 'CBRT governor sacked','type': 'governance'},
    {'date': '2021-11-23', 'event': 'Lira collapse',       'type': 'currency'},
    {'date': '2022-10-01', 'event': 'CPI peaks at 85%',    'type': 'macro'},
    {'date': '2023-06-22', 'event': 'Policy normalisation begins', 'type': 'macro'},
    {'date': '2024-03-21', 'event': 'Rate raised to 50%',  'type': 'macro'},
]
```

Use these dates as vertical annotation lines in the dashboard timeline. The governance shock (CBRT governor) and normalisation events are as important as the currency crashes — they show that Turkey's financial fragility is driven by institutional/policy shocks, not just market dynamics.

**For section3:** these dates define the `CBRT_GOVERNOR_DUMMY` column (shock dates: 2019-03, 2019-07, 2020-11, 2021-03). Include as a binary feature in the extended feature set.

---

### 3.5 Crisis Prediction Validation (3–6 Month Lead Test)

V2's `models_b.py` implements a formal crisis prediction validation that V1 completely lacks:

```python
def validate_crisis_prediction(scores_df, crisis_dates, lead_min=3, lead_max=6):
    """
    Check if fragility score peaks in the [lead_min, lead_max] months
    window BEFORE each crisis date. Report:
      - baseline_elevation: mean score in pre-crisis window vs full-period mean
      - actionable_lead_pct: % of crises where peak was within actionable window
      - false_positive_rate: % of non-crisis months with score > PONZI threshold
    """
```

This is the core evidence table for the submission. Run it for both Model A and Model B. Expected result: Model B has baseline_elevation > Model A for 2018 and 2021 crises, with an actionable lead of 2–4 months. Model A may show leads only for 2008.

**Export in section3:** `crisis_prediction_validation` block per model with these three metrics per crisis event.

---

### 3.6 SHAP Per Crisis Period (Not Just Global Feature Importance)

V2's `models_b.py` computes SHAP values broken out by regime/crisis period:

```python
shap_periods = {
    'pre_2007':     (df.index < '2008-01-01'),
    'crisis_2008':  (df.index >= '2008-09-01') & (df.index <= '2009-03-31'),
    'pre_2019':     (df.index >= '2018-01-01') & (df.index < '2018-08-01'),
    'crisis_2020':  (df.index >= '2020-03-01') & (df.index <= '2020-04-30'),
}
```

This gives SHAP values *per crisis episode*, not just the global average. The key narrative: for Model A in crisis_2008, EM and EU dominate. For Model B in crisis_2018 (TRY crash), DXY_lag3m and TRY_USD dominate while EM stays flat. This is the proof of Model B's different mechanism. Without period-specific SHAP, you can only show "Model B uses TRY features globally" — with it you can show "TRY features activate specifically during Turkish crises."

**Export in section3:** `shap_by_period` object per model with keys matching the crisis period names.

---

### 3.7 OLS Parsimonious Feature Set

V2 defines an explicit minimal feature set for OLS (to keep it interpretable):

```python
OLS_FEATURES = ['SP500','DAX','FTSE','NIKKEI','BOVESPA','EU','EM','VIX','DXY','mean_corr']
```

This is the right approach: OLS with all lag features + Turkey dummies overfits and loses interpretability. Keep OLS restricted to ~10 core features. Elastic Net gets the full expanded set (it will prune automatically via L1).

---

### 3.8 regime_encoded Exclusion Rationale

V2's `models_b.py` has an explicit comment explaining why the regime label is excluded as a feature:

```python
# Explicitly exclude regime_encoded from features to avoid data leakage.
# The regime is derived from the fragility score which uses model outputs —
# including it as a predictor creates a circular dependency.
feature_cols = [c for c in df.columns if c not in ['ISE_USD_return', 'regime', 'regime_encoded']]
```

Document this in the section3 notebook as a methodological note. The regime label is a *downstream output* of the prediction layer, not a predictor.

---

## Part 4: Analytical Ideas Worth Preserving (From V1)

---

### 4.1 ISE_TL vs ISE_USD Divergence as Core Evidence

During the 2018 TRY crash, ISE_TL (BIST100 in TL) *looks calm* while ISE_USD *crashes* — a collapsing lira inflates nominal stock prices in TL terms. A model trained on TL-denominated returns is tracking inflation, not fragility.

**In section3:** include a dual-axis chart of ISE_TL vs ISE_USD for 2016–2022, annotated at Aug 2018. The divergence is the paper's core empirical evidence for why you need the USD-denominated target. This belongs as an explicit subplot in §2 before the feature engineering.

---

### 4.2 Model A Failure Mode: Confusion Matrix Per Crisis

Section3 §4 applies saved Model A to 2012–2026. Report not just higher RMSE but which crises Model A *labels wrong*. Build a binary "crisis month" confusion matrix (TP/FP/TN/FN) for both models across the four known crises. Model A expected to have high FN for 2018 and 2021. That's the quantitative case for Model B.

**section3 must export:** `crisis_detection_confusion` per model: `{TP, FP, TN, FN, precision, recall}`.

---

### 4.3 DTW Similarity: "This Looks Like Aug 2018"

V1's `compute_dtw_similarity.py` computed Dynamic Time Warping distances between the current 90-day fragility score window and all historical windows. Top-5 most similar historical periods are surfaced for navigation.

Run post-modelling on exported fragility scores. Use z-score normalisation before DTW (compare shape, not level). Replace `features.json` paths with new `fragility_output.json`. Surface as a "Most Similar Past Periods" card in the dashboard.

---

### 4.4 Permutation Entropy Precursor Pattern

PE falls (markets become more "orderly") ~1–3 months before major regime transitions. Plot PE alongside the fragility score in section3 and annotate pre-crisis PE drops at 2008-08, 2018-07, 2021-02. This motivates PE's inclusion in the fragility formula even if it's not a strong standalone predictor.

---

### 4.5 The Two-Layer Architecture

The `learnings.txt` separation of the pipeline into Prediction Layer and Fragility Layer is architecturally correct:
- **Layer 1** models predict `ISE_USD monthly return` (supervised task, same as section2)
- **Layer 2** converts model residuals + raw features into the 6-component fragility score
- The fragility score is NOT the model's prediction; it's a separate structured signal
- The regime label is NOT derived from score thresholds alone; hard-coded crisis anchors + adaptive thresholds

This separation lets section3 discuss model performance (R², RMSE) and fragility score quality independently.

---

## Part 5: Section3 JSON Export Schema

The exact shape `fragility_output.json` must have. All dashboard wiring from plan-1.txt §2.2 and all visualisations above depend on this schema.

```json
{
  "generated_at": "2026-04-23T...",
  "models": {
    "model_2009": {
      "label": "Model A · 2009–2011",
      "desc": "7 global indices · trained on GFC recovery window",
      "training_window": "2009-01 to 2011-08",
      "performance": {
        "r2": 0.8277,
        "rmse": 0.00517,
        "mae": 0.00414,
        "regime_rmse": { "HEDGE": 0.0041, "SPECULATIVE": 0.0055, "PONZI": 0.0078 }
      },
      "shap_values": [
        {"lbl": "ise2", "val": 0.014},
        {"lbl": "em",   "val": 0.008}
      ],
      "shap_by_period": {
        "pre_2007":    {"ise2": 0.66, "eu": 0.11},
        "crisis_2008": {"ise2": 0.45, "em": 0.21, "eu": 0.18}
      },
      "crisis_prediction_validation": {
        "GFC_2008":      {"baseline_elevation": 1.42, "lead_months": 4, "actionable": true},
        "TRY_2018":      {"baseline_elevation": 0.91, "lead_months": 0, "actionable": false},
        "COVID_2020":    {"baseline_elevation": 1.38, "lead_months": 2, "actionable": false},
        "Turkey_2021":   {"baseline_elevation": 0.88, "lead_months": 0, "actionable": false}
      },
      "crisis_detection_confusion": {"TP": 6, "FP": 2, "TN": 241, "FN": 8},
      "monthly_scores": [
        {
          "date": "2009-01",
          "fragility_score": 71.2,
          "regime": "PONZI",
          "regime_confidence": 0.83,
          "components": {
            "rolling_corr":    0.74,
            "pe_inv":          0.81,
            "rolling_vol":     0.69,
            "eigenvalue_ratio":0.71,
            "vix":             0.88,
            "try_weakness":    0.61
          },
          "pairwise_correlations": {
            "SP500_DAX": 0.81, "SP500_FTSE": 0.79, "SP500_NIKKEI": 0.34,
            "SP500_BOVESPA": 0.62, "SP500_EU": 0.83, "SP500_EM": 0.71,
            "SP500_ISE_USD": 0.54,
            "DAX_FTSE": 0.87, "DAX_EU": 0.94, "DAX_EM": 0.66, "DAX_ISE_USD": 0.63,
            "FTSE_EU": 0.95, "FTSE_EM": 0.63, "FTSE_ISE_USD": 0.60,
            "EU_EM": 0.66, "EU_ISE_USD": 0.69,
            "EM_ISE_USD": 0.70
          },
          "ise_usd_return": -0.0847,
          "ise_usd_predicted": -0.0791
        }
      ],
      "feature_importance_timeseries": [
        { "date": "2009-01", "feature_importance": {"ise2": 0.66, "eu": 0.11, "em": 0.06} }
      ],
      "crisis_lead_times": [
        {
          "crisis": "GFC 2008",
          "crisis_date": "2008-09",
          "first_ponzi_warning": "2008-08",
          "lead_days": 31
        }
      ]
    },
    "model_2003": {
      "label": "Model B · 2003–2026",
      "desc": "12 features incl. TRY_weakness, VIX, DXY, lag features · Turkey-aware",
      "training_window": "2003-01 to 2026-04",
      "performance": { "...": "same shape as model_2009" },
      "shap_by_period": { "...": "same shape, now includes crisis_2018 and crisis_2021 periods" },
      "crisis_prediction_validation": {
        "TRY_2018":    {"baseline_elevation": 1.61, "lead_months": 4, "actionable": true},
        "Turkey_2021": {"baseline_elevation": 1.44, "lead_months": 3, "actionable": true}
      },
      "monthly_scores": [ "...same shape..." ],
      "crisis_lead_times": [ "...now includes 2018 and 2021 entries..." ]
    }
  },
  "regime_transition_matrix": {
    "model_2009": [[0.91,0.08,0.01],[0.14,0.79,0.07],[0.03,0.12,0.85]],
    "model_2003": [[0.89,0.10,0.01],[0.12,0.81,0.07],[0.02,0.09,0.89]]
  },
  "crisis_annotations": [
    {"date": "2018-05-23", "label": "TRY pressure", "type": "currency"},
    {"date": "2018-08-10", "label": "TRY freefall",  "type": "currency"},
    {"date": "2021-03-20", "label": "CBRT governor sacked", "type": "governance"},
    {"date": "2021-11-23", "label": "Lira collapse", "type": "currency"}
  ],
  "dtw_similarity": {
    "window_size": 90,
    "feature_used": "fragility_score",
    "periods": [
      { "date": "2018-05", "score": 0.91, "label": "Pre-TRY crash" }
    ]
  },
  "volatility_clusters": [
    { "id": 1, "start": "2008-09", "end": "2009-03", "intensity": 0.82, "duration_months": 7 }
  ]
}
```

---

## Part 6: Dashboard Sections to Add in v2.html

| Priority | Section to Add | Data Dependency | Effort |
|---|---|---|---|
| 1 | Full NxN correlation heatmap (replace single row) | `pairwise_correlations` per month | 2h SVG |
| 2 | Regime-coloured timeline gradient + threshold lines | `regime` per month | 1h (modify existing) |
| 3 | Feature importance timeline (Model A vs B) | `feature_importance_timeseries` | 3h SVG |
| 4 | Clickable timeline → scrubber sync | No new data | 30min JS |
| 5 | Regime transition matrix (3×3) | Compute client-side from monthly_scores | 2h SVG |
| 6 | Volatility clustering overlay on ISE timeline | `components.rolling_vol` | 2h SVG |
| 7 | Real lead time table (replace fake bars) | `crisis_lead_times` | 1h (modify existing) |
| 8 | Regime-split RMSE in performance table | `performance.regime_rmse` | 30min (modify existing) |
| 9 | MST network (circular layout) | `pairwise_correlations` | 3h SVG |
| 10 | Crisis prediction validation summary | `crisis_prediction_validation` | 1h |
| 11 | DTW similar periods card | `dtw_similarity` | 2h |

---

## Part 7: Things That Looked Good But Are NOT Worth Porting

- **DTWSimilarityHeatmap** grid layout: replace with a simple top-5 list. The scrollable bar grid was confusing.
- **CorrelationNetworkEvolution**: animated MST transitions over time — too heavy for a submission dashboard.
- **LaymanOverlay** drawer-in-drawer: v2.html already has the drawer (`openDrawer()`). Don't replicate the per-component floating overlay.
- **TutorialOverlay**: not needed.
- **React app's multi-file architecture**: the entire reason v2 switched to single HTML is correct.
- **V2's dynamic weight redistribution**: explicitly do not carry this forward — it makes the fragility score non-comparable across time.
- **Ridge as a headline model**: V1 used it, learnings.txt says drop it. Ridge = OLS in this setup.
- **ANN/MLP as a main model**: V1 used it, overfit on the sample size. Excluded from section3 mainline.

---

## Summary

**Five things that would most prevent section3/dashboard from feeling analytically weaker than the previous attempts:**

1. **TRY_weakness at 0.30 weight** (V2 formula, not V1's DXY at 0.10) — this is the single change that makes Model B see 2018 and 2021
2. **Full NxN correlation heatmap** with 30-day delta on hover — the core analytical chart from V1
3. **Regime-coloured timeline gradient** — makes the Minsky narrative visible immediately (V1)
4. **Four Turkey-specific walk-forward splits** — the correct academic validation structure (V2)
5. **Period-specific SHAP** (pre_2007 vs crisis_2008 vs crisis_2018 vs crisis_2021) — proves *why* Model B wins at the mechanism level (V2)

Everything else is polish. These five are the analytical substance.
