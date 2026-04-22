"""
Patch markdown cells in section2_model_build.ipynb
to reflect actual results instead of pre-run assumptions.
"""
import json

NB_PATH = "section2_model_build.ipynb"

with open(NB_PATH, "r") as f:
    nb = json.load(f)

PATCHES = {
    # --- §2.7 Ridge ---
    # Old: claimed VIF > 5 for eu AND em. em VIF is actually 3.77.
    # Also Ridge alpha=0.0001 means virtually no shrinkage vs OLS.
    "Particularly useful here given the moderate-to-high inter-index correlations (VIF > 5 for `eu`, `em`). `RidgeCV` performs efficient leave-one-out CV over a log-spaced alpha grid.":
    "Particularly useful given the severe multicollinearity found in §2.3: `eu` (VIF=22.8), `ftse` (9.6), and `dax` (9.2) all exceed the VIF=10 threshold. `RidgeCV` selects α via cross-validation over a log-spaced grid; in this dataset the optimal α=0.0001 is negligibly small, meaning Ridge converges to OLS — a sign that the training signal is strong enough that aggressive shrinkage would hurt.",

    # --- §2.10 RF ---
    # Old: implies RF will likely outperform linear models.
    # Actual: RF came 5th out of 6 (worse than all linear models).
    "Feature importances (mean decrease in impurity) are extracted post-fit to compare with LASSO's coefficient-based selection.":
    "Feature importances (mean decrease in impurity) are extracted post-fit to compare with LASSO's coefficient-based selection. Note: RF did not outperform the regularised linear models on this dataset (RMSE 0.005358 vs ElasticNet 0.005170), suggesting that ISE USD returns are driven by linear co-movements with global indices rather than non-linear interactions.",

    # --- §2.11 MLP ---
    # Old: implies MLP GridSearch will find useful non-linearity.
    # Actual: MLP was worst (RMSE 0.006244, CV_RMSE 0.037 — severe overfitting).
    "`early_stopping=True` prevents overfitting on the training set. Inputs are already standardised from Section 2.4, which is critical for MLP convergence.":
    "`early_stopping=True` prevents overfitting on the training set. Inputs are already standardised from Section 2.4, which is critical for MLP convergence. Note: MLP produced the weakest test performance (RMSE 0.006244, R²=0.749) and a very high CV RMSE (0.037), indicating the neural network overfits despite early stopping — likely because 428 training rows is insufficient for a (64,64,32) architecture to generalise.",

    # --- §2.16 Business interpretation – non-linearity paragraph ---
    # Old: "If RF or MLP substantially outperform..." (conditional)
    # Actual: they did NOT — conclusion should be stated, not conditional.
    "**Non-linearity:** If Random Forest or MLP substantially outperform the linear models on RMSE and R², this suggests non-linear relationships between global index returns and ISE USD returns — relevant for systemic risk modelling in Section 3.":
    "**Non-linearity:** Random Forest and MLP did *not* substantially outperform the linear models (RF RMSE=0.005358, MLP RMSE=0.006244 vs ElasticNet 0.005170). This suggests that ISE USD returns are predominantly driven by *linear* co-movements with global indices. Non-linear and interaction effects exist (RF's EU importance of 11.4% vs LASSO zeroing EU entirely) but are not the dominant predictive signal.",

    # --- §2.16 – classification AUC paragraph ---
    # Old: "AUC > 0.55 indicates some directional predictive power" — sets a very low bar.
    # Actual: AUC = 0.888, accuracy = 82% — this is strong, not marginal.
    "**Classification (direction prediction):** An AUC > 0.55 indicates the model has some directional predictive power beyond a coin flip, which has practical trading and risk management implications.":
    "**Classification (direction prediction):** The RF Classifier achieved AUC=0.888 and 82% accuracy on the held-out test set — well above chance. Precision and recall are balanced (≈0.82–0.87) across both classes, indicating the model reliably identifies up-days and down-days. This strong directional signal has practical risk management implications: it can flag high-probability negative days for hedging or position reduction.",

    # --- §2.16 – Elastic Net paragraph ---
    # Old: frames l1_ratio result as still unknown ("reveals whether...")
    # Actual: l1_ratio=0.70 — sparsity is preferred, should state the finding.
    "**Elastic Net vs Ridge vs LASSO:** The optimal `l1_ratio` from `ElasticNetCV` reveals whether sparsity (→ 1.0, LASSO-like) or coefficient shrinkage (→ 0.0, Ridge-like) is more appropriate for this dataset.":
    "**Elastic Net vs Ridge vs LASSO:** `ElasticNetCV` selected `l1_ratio=0.70` — confirming that *sparsity is more appropriate than pure shrinkage* for this dataset. The EN zeroed SP, DAX, and EU (same as LASSO), while retaining ise2, FTSE, NIKKEI, BOVESPA, and EM. The marginal improvement over LASSO (RMSE 0.005170 vs 0.005175) suggests the L2 component adds modest stability without changing the feature selection conclusion.",
}

patched = 0
for cell in nb["cells"]:
    if cell["cell_type"] != "markdown":
        continue
    src = "".join(cell["source"])
    for old, new in PATCHES.items():
        if old in src:
            src = src.replace(old, new)
            patched += 1
            print(f"  [PATCH] Updated: {old[:60]}…")
    cell["source"] = [src]

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1)

print(f"\nDone. {patched} markdown patch(es) applied.")
