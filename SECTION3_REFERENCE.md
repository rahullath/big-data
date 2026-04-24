# Section 3 Reference — Model B Technical Spec
## Financial Fragility Clock · Group 5 · MSc FinTech Big Data Management

> This file exists to survive context compaction. All critical technical decisions are here.
> Never delete. Update in-place when design changes.

---

## 1. Architecture: Two-Layer Pipeline

```
LAYER 1 (Prediction)   →  OLS + ElasticNet + LASSO + RF predict ISE_USD monthly return
LAYER 2 (Fragility)    →  6-component fixed-weight score from raw features (independent of Layer 1)
```

The fragility score is NOT the model prediction. It is a structured signal built from raw features.
Regime labels are derived FROM the fragility score + hard-coded crisis anchors, not from model output.

---

## 2. Model Stack

| Role | Model | Key decision |
|---|---|---|
| Regression baseline | OLS (10-feature restricted set) | Transparent, comparable to Model A |
| Primary model | Elastic Net (l1_ratio=0.70 from section2 finding) | Best Model A performer; handles correlated Turkey+global features |
| Feature pruner | LASSO | Shows which Turkey features stop mattering; narrative value |
| Non-linear challenger | Random Forest | Crisis threshold effects; importance plots |
| Primary classifier | Logistic Elastic Net | Interpretable regime/crisis classifier |
| Secondary classifier | RF Classifier | Continuity with section2 AUC=0.888 result |
| **EXCLUDED** | Ridge | Collapsed to OLS in section2 (α=0.0001 → L2 not needed) |
| **EXCLUDED** | ANN/MLP | CV_RMSE=0.037 on 428 rows; too unstable for headline model |

---

## 3. Data Sources

```python
TICKERS = {
    'BIST100': 'XU100.IS',    'USDTRY': 'USDTRY=X',
    'SP500':   '^GSPC',       'DAX':    '^GDAXI',
    'FTSE':    '^FTSE',       'NIKKEI': '^N225',
    'BOVESPA': '^BVSP',       'EU':     '^STOXX50E',   # Euro Stoxx 50 proxy
    'EM':      'EEM',         'VIX':    '^VIX',
    'DXY':     'DX-Y.NYB',   'BRENT':  'BZ=F',
}
# Date range: 2003-01-01 to 2026-04-30
```

**ISE_USD daily** = `log(BIST100 / USDTRY).diff()` (i.e., `log(BIST100).diff() - log(USDTRY).diff()`)
**ISE_USD monthly** = sum of daily log-returns per month (log-returns are additive)

**Overlap verification (required §2):** correlate yfinance ISE_USD monthly (2009-2011) vs `ise2` column
from `group5_clean_data.csv`. Target: r > 0.90. If below, document the discrepancy.

---

## 4. Feature Engineering

### 4a. Monthly feature matrix (all monthly resampled from daily)

**Return features** (sum of daily log-returns per month):
- `SP500`, `DAX`, `FTSE`, `NIKKEI`, `BOVESPA`, `EU`, `EM` — 7 global index returns

**Level features** (monthly mean of daily levels):
- `VIX` — raw level (not return); monthly mean
- `DXY` — raw level; monthly mean
- `BRENT` — raw level; monthly mean
- `USDTRY` — raw level; monthly mean

**Rolling features** (computed on daily data, then resampled to month-end using `.resample('ME').last()`):
- `mean_corr` — mean of abs(upper triangle) of 60d rolling NxN Pearson matrix (8 indices including ISE_USD)
- `eigenvalue_ratio` — λ_max / Σλ from the 60d NxN matrix
- `pe` — permutation entropy on ISE_USD daily returns (m=3, delay=1, window=30), normalised to [0,1]
- `usdtry_vol` — `log(USDTRY).diff().rolling(30).std() * sqrt(252)` (annualised)
- `rolling_vol` — `ISE_USD_daily.rolling(30).std()` — ISE-specific volatility

### 4b. Derived features (after normalization)

```python
def _norm(series):
    lo, hi = series.quantile(0.02), series.quantile(0.98)
    return (series.clip(lo, hi) - lo) / (hi - lo + 1e-8)

# IMPORTANT: Use VELOCITY (log diff) not LEVEL for try_weakness.
# Level fails because USDTRY 98th pct = 42 (2024 extreme), so 2018's 4.7 maps to only 0.09.
# Velocity captures RATE of depreciation: 2018 crash +44% and 2021-22 collapse both score high.
usdtry_log_chg = np.log(fm['USDTRY']).diff()
try_weakness   = _norm(usdtry_log_chg)        # HIGH when lira depreciating fast → HIGH fragility
corr_n         = _norm(mean_corr)
pe_inv         = 1 - _norm(pe)                # HIGH when PE falls (markets "orderly" pre-crisis)
vol_n          = _norm(rolling_vol)
eig_n          = _norm(eigenvalue_ratio)
vix_n          = _norm(VIX_monthly)
```

### 4c. Lag features

```python
LAG_FEATS  = ['DXY', 'USDTRY', 'BRENT', 'VIX']
LAG_MONTHS = [1, 3, 6, 12]
# Naming: DXY_lag1m, DXY_lag3m, etc.
# All lag features go into Elastic Net full set. LASSO prunes unhelpful ones.
```

### 4d. CBRT Governor Dummy

```python
CBRT_SHOCK_MONTHS = ['2019-03', '2019-07', '2020-11', '2021-03']
# Binary: 1 on months of Central Bank of Turkey governor dismissals
```

### 4e. ISE pairwise correlations (for dashboard heatmap)

Per month: rolling 60d Pearson of ISE_USD vs each of [SP500, DAX, FTSE, NIKKEI, BOVESPA, EU, EM].
Stored in JSON as lowercase keys: `{sp500: X, dax: X, ftse: X, nikkei: X, bovespa: X, eu: X, em: X}`

---

## 5. Feature Sets Per Model

```python
OLS_B_FEATURES = ['SP500','DAX','FTSE','NIKKEI','BOVESPA','EU','EM','VIX','DXY','mean_corr']
# OLS restricted to 10 features for interpretability

LASSO_EN_FEATURES = [
    # Market block
    'SP500','DAX','FTSE','NIKKEI','BOVESPA','EU','EM',
    # FX/Vol/Oil block
    'VIX','DXY','BRENT','USDTRY',
    # Turkey macro block
    'usdtry_vol','CBRT_dummy',
    # Regime mechanics block
    'mean_corr','pe','eigenvalue_ratio','rolling_vol',
    # Lag features
    'DXY_lag1m','DXY_lag3m','DXY_lag6m','DXY_lag12m',
    'USDTRY_lag1m','USDTRY_lag3m','USDTRY_lag6m','USDTRY_lag12m',
    'BRENT_lag1m','BRENT_lag3m','BRENT_lag6m',
    'VIX_lag1m','VIX_lag3m','VIX_lag6m',
]
# NEVER include: try_weakness, corr_n, pe_inv, vol_n, eig_n, vix_n
# (these are fragility score components derived from the raw features above)
# NEVER include: regime labels (circular dependency)
# NEVER include: fragility_score (output, not input)
```

---

## 6. Fragility Score Formulas

### Model A (4-component)

```python
fragility_a = (
    0.40 * corr_n  +
    0.30 * pe_inv  +
    0.20 * vol_n   +
    0.10 * rf_err_n    # normalised absolute RF prediction error
) * 100
```

### Model B (6-component, V2 formula — KEY: try_weakness at 0.30 NOT DXY at 0.10)

```python
fragility_b = (
    0.20 * corr_n       +    # 60d rolling mean abs pairwise correlation
    0.15 * pe_inv       +    # 1 - normalised permutation entropy
    0.10 * vol_n        +    # ISE_USD rolling_vol normalised
    0.10 * eig_n        +    # λ_max / Σλ normalised
    0.15 * vix_n        +    # VIX level normalised
    0.30 * try_weakness      # ← CORE TURKEY SIGNAL — this is what makes 2018 visible
) * 100
```

**Normalisation**: 2nd–98th percentile clipping via `_norm()`. NOT min-max.
**No dynamic weight redistribution.** Fixed weights always.

---

## 7. Regime Classification

### Hard-coded crisis PONZI anchors

```python
CRISIS_PERIODS = [
    ('2008-09-01', '2009-03-31', 'PONZI'),   # GFC
    ('2018-05-01', '2018-11-30', 'PONZI'),   # 2018 TRY Crisis ← V1 was missing this
    ('2020-03-01', '2020-04-30', 'PONZI'),   # COVID-19
    ('2021-03-01', '2022-01-31', 'PONZI'),   # 2021-22 TRY Collapse ← V1 was missing this
]
```

### Fixed thresholds (for non-crisis periods)

```
HEDGE        < 40
SPECULATIVE  40 – 67
PONZI        ≥ 67 (or override by crisis anchor)
```

---

## 8. Walk-Forward Splits (4 Turkey-specific)

```python
WF_SPLITS = [
    {'name': 'split_2008',       'desc': 'GFC 2008',
     'train': ('2003-01','2007-12'), 'test': ('2008-01','2008-12'),
     'narrative': 'Global crisis — both models should catch'},
    {'name': 'split_2018_try',   'desc': '2018 TRY Crisis',
     'train': ('2003-01','2017-12'), 'test': ('2018-01','2018-12'),
     'narrative': 'Turkey-specific — Model A trained on GFC should MISS this'},
    {'name': 'split_2020',       'desc': 'COVID-19 2020',
     'train': ('2003-01','2019-12'), 'test': ('2020-01','2020-12'),
     'narrative': 'Global shock — both models expected to catch'},
    {'name': 'split_2021_turkey','desc': '2021–24 Turkey Crisis',
     'train': ('2003-01','2020-12'), 'test': ('2021-01','2024-12'),
     'narrative': 'Prolonged Turkey crisis — long OOS test for Model B'},
]
# Report RMSE per split per model. split_2018_try and split_2021_turkey are the KEY ones.
```

---

## 9. Period-Specific SHAP

```python
SHAP_PERIODS = {
    'pre_2007':    'df.index < 2008-01-01',
    'crisis_2008': '2008-09-01 to 2009-03-31',
    'crisis_2018': '2018-05-01 to 2018-11-30',
    'crisis_2020': '2020-03-01 to 2020-04-30',
    'crisis_2021': '2021-03-01 to 2022-01-31',
}
# Model A in crisis_2008: EM and EU dominate
# Model B in crisis_2018: DXY_lag3m and USDTRY dominate, EM flat
# This is the MECHANISM-LEVEL proof, not just performance-level
```

SHAP implementations:
- Linear models → `shap.LinearExplainer`
- RF → `shap.TreeExplainer`
- MLP (section2 only) → `shap.KernelExplainer` with sample(X_train, 50)

---

## 10. JSON Export Schema (dashboard.html contract)

```json
{
  "version": "2.0",
  "generated_at": "...",
  "models": {
    "model_2009": {
      "meta": {
        "id": "model_2009",
        "label": "2009–2011 Original"
      },
      "performance": {
        "ols":           {"r2": X, "rmse": X, "mae": X},
        "random_forest": {"r2": X, "rmse": X, "mae": X},
        "elastic_net":   {"r2": X, "rmse": X, "mae": X}
      },
      "shap_values": {"SP500": X, "DAX": X, ...},
      "walk_forward": [
        {
          "split": "split_2008", "description": "GFC 2008",
          "ols":  {"r2": X, "rmse": X, "mae": X, "hedge_rmse": X, "spec_rmse": X},
          "rf":   {"r2": X, "rmse": X, "mae": X, "hedge_rmse": X, "spec_rmse": X},
          "elastic_net": {"r2": X, "rmse": X, "mae": X, "hedge_rmse": X, "spec_rmse": X}
        }
      ],
      "monthly_scores": [
        {
          "date": "2009-01",
          "fragility_score": 71.2,
          "regime": "PONZI",
          "correlations": {"sp500": 0.74, "dax": 0.65, "ftse": 0.71,
                           "nikkei": 0.34, "bovespa": 0.62, "eu": 0.68, "em": 0.70},
          "features": {
            "vix": 28.5,          
            "dxy": 82.3,          
            "brent": 45.2,        
            "try_usd": 0.00143    
          }
        }
      ]
    },
    "model_2003": {
      "walk_forward": [
        {
          "split": "split_2018_try", "description": "2018 TRY Crisis",
          "metrics": {"test_r2": X, "test_rmse": X, "test_mae": X},
          "regime_metrics": {
            "HEDGE":       {"rmse": X, "n": X},
            "SPECULATIVE": {"rmse": X, "n": X},
            "PONZI":       {"rmse": X, "n": X}
          }
        }
      ]
    }
  }
}
```

**Critical JSON notes:**
- `date` format: "YYYY-MM" (not "YYYY-MM-DD") — dashboard uses `s.date.startsWith('2018-08')`
- `correlations` keys: **lowercase** `sp500`, `dax`, `ftse`, `nikkei`, `bovespa`, `eu`, `em`
- `features.try_usd` = `1/USDTRY` (value of 1 TRY in USD). Dashboard multiplies by 100 for display.
- `shap_values` = mean |SHAP| per feature (positive floats, sorted descending for bar chart)
- Model A walk_forward: keys `ols`, `rf`, `elastic_net` at the split level (no `metrics` wrapper)
- Model B walk_forward: key `metrics` wrapper with `test_r2`, `test_rmse`, `test_mae`
- `performance` is the fallback if `walk_forward` is empty

---

## 11. Academic Narrative Checkpoints

These 4 data points validate the entire Model B thesis. Must verify after export:

| Date | Model A score | Model B score | Δ | Note |
|---|---|---|---|---|
| 2018-08 | 46.9 (PONZI) | 52.1 (PONZI) | +5.2 | B elevated via try_weakness velocity |
| 2021-11 | 33.5 (PONZI) | 53.0 (PONZI) | +19.4 | KEY — domestic Turkey crisis, global calm |
| 2009-03 | 53.3 (PONZI) | 63.8 (PONZI) | +10.5 | Both catch GFC, B higher (extra components) |
| 2020-03 | 58.8 (PONZI) | 71.1 (PONZI) | +12.3 | B elevated by VIX + TRY velocity |

**CONFIRMED** (2026-04-24): Overlap check r=0.9826. All crisis periods PONZI via hard-coded anchors.
The 2021-11 (+19.4) is the headline academic result: global-index Model A scores 33.5 while Turkey-aware
Model B scores 53.0 for the domestic TRY collapse. No global market stress — pure Turkey signal.

---

## 12. Section 3 Notebook Structure

```
§0  Context & motivation (markdown)
§1  Imports + constants
§2  Data fetch (yfinance 2003-2026)
§3  ISE_USD derivation + overlap check vs group5_clean_data.csv
§4  Rolling features (daily computation, monthly resampling)
§5  Monthly feature matrix (all features combined)
§6  CBRT dummy + lag features
§7  Fragility score components (_norm, try_weakness, pe_inv, etc.)
§8  Regime labelling (crisis anchors + fixed thresholds)
§9  Model A Extended (retrain OLS+EN on 2009-2011, apply 2003-2026)
§10 Model B — incremental feature blocks (Stage 1–4, EN RMSE comparison)
§11 Model B — final training (OLS, EN, LASSO, RF on full feature set)
§12 Walk-forward validation (4 splits, regime-split RMSE)
§13 Regime classifiers (Logistic EN + RF Classifier)
§14 Fragility scores (Model A 4-component, Model B 6-component)
§15 SHAP analysis (global + period-specific)
§16 Crisis prediction validation
§17 Key figures (ISE_TL vs ISE_USD divergence, contrast timeline)
§18 JSON export → data/fragility_output.json
```

---

## 13. Section 2 SHAP Additions (§2.17)

Added after §2.16 in section2_model_build.ipynb.

SHAP explainers:
- `shap.LinearExplainer(en, X_train)` → ElasticNet SHAP (best model)
- `shap.LinearExplainer(ols, X_train)` → OLS SHAP (baseline comparison)
- `shap.TreeExplainer(rf_best)` → RF regressor SHAP
- `shap.TreeExplainer(rf_clf)` → RF classifier SHAP
- `shap.KernelExplainer(mlp_best.predict, shap.sample(X_train, 50))` → MLP SHAP (small sample)

Key insight to verify: `ise2` dominates all linear models AND RF (66% MDI). This motivates Model B:
the 2009-2011 dataset has ise2 as the dominant predictor because both ISE measures track the same
underlying market. Once we extend to 2003-2026 and target ISE_USD (without ise2 as feature),
the global indices and Turkey-specific features must carry the prediction.

---

## 14. Files

```
section2_model_build.ipynb  ← exists, SHAP cells added as §2.17
section3_model_b.ipynb      ← new, full Model B pipeline
data/fragility_output.json  ← generated by §18 of section3
SECTION3_REFERENCE.md       ← this file
models/*.pkl                ← section2 models (ols, en, rf, mlp, classifier, scaler)
```
