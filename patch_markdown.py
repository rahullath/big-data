"""
Comprehensive patch for section2_model_build.ipynb:
1. Refine Ridge §2.7 markdown per academic framing
2. Refine MLP §2.11 markdown to explicitly call out CV_RMSE gap
3. Insert loss curve cell after MLP fit cell
"""
import json

NB_PATH = "section2_model_build.ipynb"

with open(NB_PATH, "r") as f:
    nb = json.load(f)

# ── 1. Markdown patches ─────────────────────────────────────────────────────

MARKDOWN_PATCHES = {

    # §2.7 Ridge — tighten framing: α=0.0001 is a FINDING not a near-miss
    "the optimal α=0.0001 is negligibly small, meaning Ridge converges to OLS — a sign that the training signal is strong enough that aggressive shrinkage would hurt.":
    "the optimal α=0.0001 — the minimum of the search grid — was selected, yielding metrics identical to OLS. **This is a finding, not a bug**: Ridge converged to minimal regularisation, suggesting the features are not severely multicollinear at the level that L2 penalisation addresses. The dataset is clean enough that shrinkage provides no benefit beyond the OLS baseline.",

    # §2.11 MLP — explicitly flag CV_RMSE gap as the key diagnostic
    "Note: MLP produced the weakest test performance (RMSE 0.006244, R²=0.749) and a very high CV RMSE (0.037), indicating the neural network overfits despite early stopping — likely because 428 training rows is insufficient for a (64,64,32) architecture to generalise.":
    "Note: MLP produced the weakest test performance (RMSE 0.006244, R²=0.749). Critically, the **CV_RMSE of 0.037 is 6× the test RMSE of 0.006** — a red flag for high variance and model instability across folds. This gap is a known limitation of MLPs on small financial datasets (536 rows total, 428 train): the architecture has too many parameters relative to the sample size. This should be cited as a **limitation** in the write-up: ANN performance degrades significantly when training data is scarce, making simpler regularised models more reliable in practice.",
}

md_patched = 0
for cell in nb["cells"]:
    if cell["cell_type"] != "markdown":
        continue
    src = "".join(cell["source"])
    for old, new in MARKDOWN_PATCHES.items():
        if old in src:
            src = src.replace(old, new)
            md_patched += 1
            print(f"  [MD PATCH] {old[:65]}…")
    cell["source"] = [src]

# ── 2. Insert loss curve cell after MLP fit cell ────────────────────────────

MLP_FIT_CELL_ID = "40d04121"   # the cell that does mlp_gs.fit(...)

LOSS_CURVE_MD = {
    "cell_type": "markdown",
    "id": "loss_curve_md",
    "metadata": {},
    "source": [
        "## 2.11b ANN Training Loss Curve\n\n",
        "The loss curve shows how the MLP's training loss decreased over iterations "
        "for the best hyperparameter combination found by `GridSearchCV`. "
        "A steadily decreasing curve confirms the network was learning; "
        "if it plateaus early it indicates `early_stopping` triggered before convergence.\n"
    ]
}

LOSS_CURVE_CODE = {
    "cell_type": "code",
    "execution_count": None,
    "id": "loss_curve_code",
    "metadata": {},
    "outputs": [],
    "source": [
        "# --- Fig 7 (plan): ANN training loss curve ---\n",
        "loss_curve = mlp_best.loss_curve_\n",
        "\n",
        "fig, ax = plt.subplots(figsize=(9, 4))\n",
        "ax.plot(loss_curve, color='steelblue', lw=1.5)\n",
        "ax.set_xlabel('Iteration')\n",
        "ax.set_ylabel('MSE Loss')\n",
        "ax.set_title(\n",
        "    f'MLP Training Loss Curve  '\n",
        "    f'(best config: {mlp_gs.best_params_[\"hidden_layer_sizes\"]} '\n",
        "    f'α={mlp_gs.best_params_[\"alpha\"]} '\n",
        "    f'lr={mlp_gs.best_params_[\"learning_rate\"]})',\n",
        "    fontweight='bold'\n",
        ")\n",
        "ax.annotate(\n",
        "    f'Final loss: {loss_curve[-1]:.6f}\\n'\n",
        "    f'Iterations: {len(loss_curve)}',\n",
        "    xy=(len(loss_curve)-1, loss_curve[-1]),\n",
        "    xytext=(-80, 30), textcoords='offset points',\n",
        "    arrowprops=dict(arrowstyle='->', color='grey'),\n",
        "    fontsize=9\n",
        ")\n",
        "plt.tight_layout()\n",
        "plt.savefig('plots/fig_07_ann_loss_curve.png', bbox_inches='tight')\n",
        "plt.show()\n",
        "print(f'Fig 7 saved — {len(loss_curve)} iterations, final loss {loss_curve[-1]:.6f}')"
    ]
}

inserted = False
new_cells = []
for cell in nb["cells"]:
    new_cells.append(cell)
    if cell.get("id") == MLP_FIT_CELL_ID:
        new_cells.append(LOSS_CURVE_MD)
        new_cells.append(LOSS_CURVE_CODE)
        inserted = True
        print(f"  [CELL INSERT] Loss curve cells inserted after id={MLP_FIT_CELL_ID}")

nb["cells"] = new_cells

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1)

print(f"\nDone. {md_patched} markdown patches, loss curve inserted: {inserted}")
