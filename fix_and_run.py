"""
Patch section2_model_build.ipynb:
  - Replace df["nikkei"].replace(0, np.nan).ffill()
    with    df["nikkei"].replace(0, np.nan).ffill().bfill()
  - Clear stale error outputs from the data-load cell
  - Reset all execution_count fields
Then execute the notebook in place using nbconvert.
"""
import json, re, subprocess, sys

NB_PATH = "section2_model_build.ipynb"

with open(NB_PATH, "r") as f:
    nb = json.load(f)

patched = 0
for cell in nb["cells"]:
    if cell["cell_type"] != "code":
        continue

    # Join source lines for easy searching
    src = "".join(cell["source"])

    if 'df["nikkei"].replace(0, np.nan).ffill()' in src:
        cell["source"] = [
            line.replace(
                'df["nikkei"].replace(0, np.nan).ffill()',
                'df["nikkei"].replace(0, np.nan).ffill().bfill()  # bfill fixes leading holiday NaN on row 0'
            )
            for line in cell["source"]
        ]
        # Clear any stale error outputs
        cell["outputs"] = []
        cell["execution_count"] = None
        patched += 1
        print(f"  [PATCH] Fixed NIKKEI ffill cell")

    # Reset execution counts everywhere so nbconvert runs clean
    cell["execution_count"] = None
    if cell.get("outputs") and any(o.get("output_type") == "error" for o in cell["outputs"]):
        cell["outputs"] = []

with open(NB_PATH, "w") as f:
    json.dump(nb, f, indent=1)

print(f"\nNotebook patched ({patched} cell(s) fixed). Saving…")

# Now execute via nbconvert using the venv's jupyter
JUPYTER = "/home/rahul/venv_coursework/bin/jupyter"
cmd = [
    JUPYTER, "nbconvert",
    "--to", "notebook",
    "--execute",
    "--inplace",
    "--ExecutePreprocessor.timeout=600",
    "--ExecutePreprocessor.kernel_name=python3",
    NB_PATH,
]

print("Running: " + " ".join(cmd))
print("=" * 60)
result = subprocess.run(cmd, capture_output=False)
sys.exit(result.returncode)
