
import json
from pathlib import Path

import pandas as pd

# 기존 두 실험 결과
GLOBAL_CSV = Path("reports/day07_anomaly_scores.csv")
SPATIAL_CSV = Path("reports/day07_spatial_results.csv")

GLOBAL_RULE = Path("configs/day07_anomaly_rules.json")
SPATIAL_RULE = Path("configs/day07_spatial_rules.json")

OUTPUT_CSV = Path("reports/day07_combined_results.csv")
COMPARISON_CSV = Path("reports/day07_combined_comparison.csv")

# 1. 기존 실험 결과 불러오기
global_df = pd.read_csv(GLOBAL_CSV)
spatial_df = pd.read_csv(SPATIAL_CSV)

global_rule = json.loads(GLOBAL_RULE.read_text(encoding="utf-8"))
spatial_rule = json.loads(SPATIAL_RULE.read_text(encoding="utf-8"))

global_threshold = float(global_rule["anomaly_threshold"])
spatial_threshold = float(spatial_rule["threshold"])

# 2. 각 이미지의 결과 연결
global_df = global_df[
    ["file", "actual", "defect_type", "anomaly_score", "predicted"]
].rename(columns={
    "anomaly_score": "global_score",
    "predicted": "global_predicted",
})

spatial_df = spatial_df[
    ["file", "actual", "defect_type", "spatial_score", "predicted"]
].rename(columns={
    "predicted": "spatial_predicted",
})

df = global_df.merge(
    spatial_df,
    on=["file", "actual", "defect_type"],
    how="inner",
    validate="one_to_one",
)

if len(df) != len(global_df) or len(df) != len(spatial_df):
    raise RuntimeError("두 실험의 이미지 목록이 다릅니다.")

# 3. 두 기준 중 하나라도 초과하면 Anomaly
global_ng = df["global_score"] > global_threshold
spatial_ng = df["spatial_score"] > spatial_threshold

df["combined_predicted"] = (
    global_ng | spatial_ng
).map({True: "Anomaly", False: "Normal"})

# 4. TP / TN / FP / FN 판정
def get_error_type(actual, predicted):
    if actual == "Anomaly":
        return "TP" if predicted == "Anomaly" else "FN"
    return "FP" if predicted == "Anomaly" else "TN"


df["error_type"] = [
    get_error_type(a, p)
    for a, p in zip(df["actual"], df["combined_predicted"])
]

# 5. 성능 계산
def evaluate(actual, predicted):
    types = [
        get_error_type(a, p)
        for a, p in zip(actual, predicted)
    ]

    counts = pd.Series(types).value_counts()
    tp = int(counts.get("TP", 0))
    tn = int(counts.get("TN", 0))
    fp = int(counts.get("FP", 0))
    fn = int(counts.get("FN", 0))
    total = tp + tn + fp + fn

    return {
        "Accuracy": (tp + tn) / total,
        "Precision": tp / (tp + fp) if tp + fp else 0,
        "Recall": tp / (tp + fn) if tp + fn else 0,
        "TP": tp,
        "TN": tn,
        "FP": fp,
        "FN": fn,
    }


comparison = pd.DataFrame({
    "Global": evaluate(df["actual"], df["global_predicted"]),
    "Spatial": evaluate(df["actual"], df["spatial_predicted"]),
    "Combined": evaluate(df["actual"], df["combined_predicted"]),
})

# 6. 결과 저장
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
comparison.to_csv(COMPARISON_CSV, encoding="utf-8-sig")

print("=" * 60)
print("DAY07 GLOBAL + SPATIAL COMPARISON")
print("=" * 60)
print(comparison.to_string())

print("\n=== Combined defect type results ===")
print(pd.crosstab(df["defect_type"], df["error_type"]))

print("\nSaved:", OUTPUT_CSV)
print("Saved:", COMPARISON_CSV)
