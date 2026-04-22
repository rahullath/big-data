# Financial Fragility Clock v2 — Project Status

**Date:** 2026-04-21  
**Branch:** `turkey`

---

## Goal

Replace the over-engineered React/Vite app (`src/`) with a **single-file HTML dashboard** that matches the design in `Financial Fragility Clock v2.html`, wired to real pipeline output from `data/fragility_output.json`.

The academic punchline: **Model A** (2009–2011 trained) misses the 2018 TRY crisis and 2021–26 Turkey crisis. **Model B** (2003–2026 extended) catches both. This contrast is the core LO1/LO2/LO3 demonstration.

---

## File Map

| File / Dir | Role |
|---|---|
| `Financial Fragility Clock v2.html` | **Design reference + current submission target** (still on simulated data) |
| `data/fragility_output.json` | Pipeline output — real data, both models present |
| `pipeline-schema.html` | Exact JSON schema the dashboard expects |
| `pipeline-execution-plan.html` | Step-by-step plan for all pipeline changes |
| `python/model_b/` | Model B pipeline (2003–2026, Turkish macro + global indices) |
| `python/model_a/` | Model A pipeline (2009–2011, pure index data) |
| `python/export_unified.py` | Unified JSON exporter → `data/fragility_output.json` |
| `python/run_pipeline.py` | Orchestrator — runs both models + exporter |
| `context-dump/converted/Group_5.csv` | Raw input for Model A (8 indices, daily log returns) |
| `src/` | Legacy React app — **ignore, do not touch** |

---

## Current Status vs Expected

### Dashboard (`Financial Fragility Clock v2.html`)

| Item | Current | Expected |
|---|---|---|
| Data source | **Simulated** (`monthToScoreA`, `monthToScoreB` hardcoded functions, ~line 608–625) | Real data fetched from `data/fragility_output.json` |
| Model toggle A/B | Works (UI only, both use fake data) | Drives real scores, SHAP, performance from JSON |
| SHAP section | Hardcoded values in JS (~line 572–593) | Read from `fragility_output.json → models.model_2009/model_2003.shap_values` |
| Crisis events | Hardcoded | Derived from monthly scores (regime transitions) |
| Correlation heatmap | Simulated `heatmapCorr` function | Read from `monthly_scores[i].correlations` |

**Single remaining task:** Replace all simulated data functions in `v2.html` with a `fetch('data/fragility_output.json')` call and rewire all rendering functions to consume the real JSON schema.

---

### `data/fragility_output.json` (pipeline output)

| Item | Current | Expected |
|---|---|---|
| Schema version | `2.0` ✓ | `2.0` |
| `model_2009` scores | **276 monthly scores**, 2003-05 to 2026-04 ✓ | Full range with correct fragility scores |
| `model_2003` scores | **277 monthly scores**, 2003-04 to 2026-04 ✓ | Full range |
| Performance keys | `random_forest`, `ols`, `var` ✓ | Same |
| `model_2009` SHAP keys | `mean_corr`, `pe_inv`, `rolling_volatility`, `rf_prediction_error` ✓ | 4-component fixed weights |
| `model_2003` SHAP keys | `FTSE`, `SP500`, `BOVESPA`, `DAX`, `BIST100` ✓ | Global index drivers |
| Academic contrast visible | **Unverified** — need to check 2018 and 2021–26 fragility scores | Model A ~43 in 2018 (SPECULATIVE), ~39 in 2021–26 (HEDGE); Model B ~68 in 2018, ~61 in 2021–26 |

---

### Model B (`python/model_b/`)

| File | Status | Notes |
|---|---|---|
| `fetch_market_data.py` | Exists, 290 lines | Verify DXY, BRENT, EUR_USD, TRY_USD (USDTRY inverted) are included |
| `fetch_macro_data.py` | Exists, 297 lines | Verify US_10Y_YIELD (FRED: DGS10) is included |
| `fetch_turkish_macro.py` | Exists, 117 lines | Derives ISE_USD = BIST100 / USDTRY |
| `preprocessing_b.py` | Exists, 446 lines | Verify CBRT governor dummy (Mar2019, Jul2019, Nov2020, Mar2021) + monthly resampling |
| `feature_engineering_b.py` | Exists, 548 lines | Verify 6-component fixed weights: corr(0.25), pe_inv(0.20), vol(0.15), eigenvalue(0.15), vix(0.15), dxy(0.10); no dynamic redistribution |
| `models_b.py` | Exists, 1018 lines | Verify 2018 TRY crisis split + 2021–2024 Turkey crisis split; OLS and VAR present |
| `regime_labeling_b.py` | Exists, 548 lines | HEDGE(<40), SPECULATIVE(40–70), PONZI(≥70) |

---

### Model A (`python/model_a/`)

| File | Status | Notes |
|---|---|---|
| `preprocessing.py` | Exists, 81 lines | Loads `Group_5.csv`, targets ISE_USD — appears functional |
| `feature_engineering.py` | Exists, 155 lines | 4-component fixed formula: corr(0.40), pe_inv(0.30), vol(0.20), rf_err(0.10) |
| `models.py` | Exists, 253 lines | RF + OLS + VAR; walk-forward splits: 2018 TRY, 2020 COVID, 2021–2024 Turkey |

---

### Exporter + Orchestrator

| File | Status | Notes |
|---|---|---|
| `python/export_unified.py` | Exists, 180 lines | Writes `data/fragility_output.json` — verify output matches `pipeline-schema.html` |
| `python/run_pipeline.py` | Exists, 278 lines | Orchestrates Model A → Model B → export |

---

## Immediate Next Steps (priority order)

1. **Wire `v2.html` to real data** — replace `monthToScoreA`/`monthToScoreB`/`heatmapCorr` simulation functions with a `fetch('data/fragility_output.json')` call; rewire all chart/SHAP/correlation renderers to the real JSON schema.
2. **Verify academic contrast** — spot-check `data/fragility_output.json` scores at 2018-08 and 2022-01 for both models to confirm the narrative holds.
3. **Verify Model B features** — confirm DXY, BRENT, CBRT governor dummies, and 6-component fixed weights are all present in the current pipeline files.
4. **End-to-end run** — run `python/run_pipeline.py` to regenerate `data/fragility_output.json` from scratch and confirm no errors.

---

## JSON Schema Quick Reference

```json
{
  "version": "2.0",
  "generated_at": "...",
  "models": {
    "model_2009": {
      "meta": {},
      "performance": { "random_forest": {}, "ols": {}, "var": {} },
      "shap_values": { "feature_name": value },
      "monthly_scores": [
        {
          "date": "YYYY-MM-DD",
          "fragility_score": 0.0,
          "regime": "HEDGE|SPECULATIVE|PONZI",
          "components": {},
          "correlations": {},
          "features": {}
        }
      ]
    },
    "model_2003": { "...same shape..." }
  }
}
```

Regime thresholds: HEDGE < 40 · SPECULATIVE 40–70 · PONZI ≥ 70
