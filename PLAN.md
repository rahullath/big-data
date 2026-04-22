# PLAN.md — ISE Return Prediction Project
## Group 5 | LM Big Data Management in Finance (36320) | Birmingham Business School

> **Accountability document — updated as tasks are completed. Never delete a row; mark ✅ when done.**

---

## Project Context

| Item | Detail |
|---|---|
| **Dataset** | `Group_5.csv` / `.xlsx` — 536 daily observations, Jan 2009–Feb 2011 |
| **Target** | `ISE_USD` — USD-based Istanbul Stock Exchange daily returns |
| **Features** | SP, DAX, FTSE, NIKKEI, BOVESPA, EU, EM (7 global indices) |
| **Hard Deadline** | 7 May 2026, 12:00 PM BST |
| **Presentation** | 29 April 2026 (in-person) |
| **Video Deadline** | 26 April 2026 (send to Jasneek) |
| **Module** | Dr Animesh Acharjee (Acharjee, 2026) |

---

## Rahul's Scope (Section 2: Model Build)

Co-owned with Vansh (methods write-up) and Sahar (critical evaluation).

---

## Model Checklist

| # | Model | Type | Status | Result |
|---|---|---|---|---|
| 1 | OLS Linear Regression | Regression baseline | ✅ Run | RMSE=0.005188, R²=0.8265 |
| 2 | Ridge Regression (L2) | Regularised | ✅ Run | RMSE=0.005188, R²=0.8265 — α=0.0001 (≡ OLS; finding: L2 not needed) |
| 3 | LASSO Regression (L1) | Feature selection | ✅ Run | RMSE=0.005175, R²=0.8274 — zeroed SP, DAX, EU |
| 4 | Elastic Net (L1+L2) | Combined | ✅ Run | RMSE=0.005170, R²=0.8277 — **best model**, l1_ratio=0.70 |
| 5 | Random Forest | Non-linear ensemble | ✅ Run | RMSE=0.005358, R²=0.8149 — ise2 dominant (66% MDI) |
| 6 | ANN / MLP | Deep learning | ✅ Run | RMSE=0.006244, R²=0.7486 — CV_RMSE=0.037 (overfitting on small sample) |
| 7 | RF Classifier (direction) | Classification bonus | ✅ Run | AUC=0.888, Accuracy=82% |

---

## Figure Checklist

| Figure | Description | Status | Saved as |
|---|---|---|---|
| fig_01_ise_timeseries.png | ISE_USD daily returns time series | ✅ | `plots/s2_timeseries.png` |
| fig_02_ise_distribution.png | Return distribution + Q-Q plot | — | (in Section 1 EDA) |
| fig_03_correlation_heatmap.png | Pearson correlation matrix (all 8 vars) | ✅ | `plots/s2_correlation.png` |
| fig_04_scatter_matrix.png | Each feature vs ISE_USD scatter + trendline | — | (in Section 1 EDA) |
| fig_05_vif.png | VIF bar chart (multicollinearity diagnostic) | ✅ | `plots/s2_vif.png` |
| fig_06_rf_feature_importance.png | RF Gini importance | ✅ | embedded in `s2_feature_importance.png` |
| fig_07_ann_loss_curve.png | ANN training/validation loss curve | ✅ | `plots/fig_07_ann_loss_curve.png` |
| fig_08_model_comparison.png | RMSE / MAE / R² bar charts all 6 models | ✅ | `plots/s2_model_comparison.png` |
| fig_09_pred_vs_actual.png | Best model predicted vs actual + residuals | ✅ | `plots/s2_actual_vs_predicted.png` |
| fig_10_classification_results.png | Confusion matrix + ROC curve | ✅ | `plots/s2_classification.png` |
| fig_11_feature_importance_all.png | Normalised feature importance all models | ✅ | `plots/s2_feature_importance.png` |

---

## Notebook Sections

| Cell Group | Content | Status |
|---|---|---|
| §0 | Imports, style setup | ✅ |
| §1 | Data load + validation (NIKKEI 0-fill + bfill for row-0 holiday) | ✅ |
| §2 | EDA — timeseries, distribution, correlation, scatter, VIF | ✅ |
| §3 | Train/test split (80/20, time-ordered), scaling | ✅ |
| §4.1 | OLS + CV score | ✅ |
| §4.2 | Ridge + optimal λ (α=0.0001 → finding: L2 not needed) | ✅ |
| §4.3 | LASSO + feature selection (zeroed SP, DAX, EU) | ✅ |
| §4.4 | Elastic Net + l1_ratio=0.70 (sparsity preferred) | ✅ |
| §4.5 | Random Forest + GridSearchCV | ✅ |
| §4.6 | ANN/MLP + GridSearchCV + loss curve | ✅ |
| §5 | Comparison table + bar charts | ✅ |
| §6 | Classification framing (RF + AUC-ROC=0.888) | ✅ |
| §7 | Unified feature importance across all models | ✅ |
| §8 | Save all models (.pkl) + scaler | ✅ |
| §9 | Business interpretation + module connections | ✅ |

---

## Dependencies

```
pip install pandas numpy matplotlib seaborn scikit-learn statsmodels scipy joblib
```

No TensorFlow/Keras needed — sklearn MLPRegressor covers ANN requirement from module.
If you want Keras: `pip install tensorflow` and replace §4.6 with a Keras Sequential model.

---

## Key Technical Decisions (justified)

| Decision | Rationale |
|---|---|
| Time-ordered train/test split (no shuffle) | Financial returns are temporally dependent; shuffling would leak future info |
| StandardScaler on train only | Prevents data leakage; required for Ridge/LASSO/EN/ANN |
| KFold(shuffle=False) for CV | Preserves temporal order in cross-validation folds |
| 10-fold CV for λ selection | Module lecture recommendation; reduces overfitting of penalty parameter |
| NIKKEI 0 → forward-fill | 34 zero values are Japanese market holidays, not actual zero returns |
| Dual framing (reg + clf) | Earns Criteria 4 marks; actionable for practitioners |
| Elastic Net l1_ratio grid search | Module-taught; handles correlated European features better than pure LASSO |

---

## Write-up Section Mapping (for Vansh)

| Write-up requirement | Where answered in notebook |
|---|---|
| Supervised vs unsupervised | §3 (train/test split, labelled target) + §9 |
| Univariate vs multivariate | §2 EDA correlation + §9 |
| Variable contribution ("churn") | §7 unified feature importance |
| Regularisation justification | §4.2–4.4 + §5 VIF discussion |
| Advantages/disadvantages | §9 business interpretation |
| Deep learning coverage | §4.6 ANN |

---

## Assignment Criteria Mapping

| Criterion | Weight | How covered |
|---|---|---|
| C1: Understanding (LO1) | 20% | §9 module connections, ANN coverage |
| C2: Technical (LO2) | 50% | All 6 models + dual framing |
| C3: Communication (LO3) | 15% | 11 figures, structured notebook, PLAN.md |
| C4: Critical (LO4) | 15% | Classification framing, VIF analysis, business hook |

---

## File Inventory

| File | Purpose |
|---|---|
| `section2_model_build.ipynb` | Main notebook (this repo) |
| `group5_clean_data.csv` | Dataset (already in repo — use as DATA_PATH) |
| `PLAN.md` | This accountability document |
| `models/` | Saved model .pkl files (created on run) |
| `fig_01` – `fig_11` | All output figures (created on run) |

---

## Timeline

| Date | Task |
|---|---|
| **22–24 Apr** | ✅ Notebook written → run on local venv, freeze all outputs |
| **24 Apr** | Record 4-min video segment covering model build section |
| **26 Apr** | Send MP4 to Jasneek |
| **25–28 Apr** | Vansh drafts Section 2 write-up using outputs; Sahar critical eval |
| **29 Apr** | In-person presentation |
| **4–6 May** | Final proofread + merge |
| **7 May 12pm** | HARD SUBMIT DEADLINE |

---

*Last updated: 23 April 2026 | Rahul Lath — notebook fully executed, all outputs frozen, markdown interpretations verified against actual results*
