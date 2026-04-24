# Financial Fragility Clock

**MSc FinTech · Group 5 · University of Birmingham**

A Minsky-framework fragility monitor for the Istanbul Stock Exchange (ISE/BIST), scoring market stress 0–100 across a 2003–2026 window using regularised regression and tree-based models.

---

## What it does

Maps monthly ISE returns onto three Minsky financing regimes:

| Score | Regime | Interpretation |
|-------|--------|----------------|
| < 40 | Hedge | Debt serviced from income |
| 40–70 | Speculative | Debt serviced from rollovers, not income |
| ≥ 70 | Ponzi | New borrowing required just to pay interest |

A Doomsday Clock metaphor maps score 70 → midnight. Hands reaching 12 signals a Ponzi threshold crossing.

---

## Models

| | Model A | Model B |
|---|---|---|
| Training window | 2009–2011 (GFC recovery) | 2003–2026 (full history) |
| Features | 7 global indices | 33 features incl. USDTRY vol, VIX lags, DXY lags |

Algorithms compared: OLS · Elastic Net (primary) · Lasso · Random Forest  
Validation: Walk-forward splits at 2018 TRY crisis, COVID-19 2020, 2021–24 Turkey stress

---

## Pages

- **`dashboard.html`** — interactive fragility clock with timeline scrubber, SHAP charts, correlation heatmap, walk-forward R² heatmap
- **`presentation.html`** — 8-slide deck (light/dark toggle)
- **`reports.html`** — full research report with SVG + PNG export and 24-reference Harvard bibliography

---

## Structure

```
├── data/fragility_output.json     # model scores, SHAP, walk-forward, correlations
├── plots/                         # 18 static PNG figures (§2 and §3)
├── section1_eda.ipynb
├── section2_model_build.ipynb
├── section3_model_b.ipynb
├── dashboard.html
├── presentation.html
└── reports.html
```

---

## Running locally

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Data is fetched from `data/fragility_output.json` at runtime — no build step, no mock data on a proper server.

---

## Key findings

- **COVID-19 (Mar–Apr 2020):** Model B crosses Ponzi threshold (71.1 → 74.3); Model A reaches only 55.6
- **November 2021:** Largest divergence — B reads 53.0, A reads 33.5 (+19.4 gap) during Turkey-specific stress with calm global markets
- **Current (April 2026):** Model B = 38.2 · Model A = 34.2 · Hedge regime

---

## References

Theoretical foundation: Minsky (1992). Full 24-reference Harvard list in `reports.html §11`.
