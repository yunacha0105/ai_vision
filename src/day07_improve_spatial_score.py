
import json
from pathlib import Path

import numpy as np
import pandas as pd

from day07_anomaly_core import (
    anomaly_map,
    create_backbone,
    extract_features,
    load_reference,
)

# 기존 정상 기준 재사용
REFERENCE_PATH = Path(
    "artifacts/day07/normal_reference.npz"
)
BASELINE_CSV = Path(
    "reports/day07_anomaly_scores.csv"
)
VAL_DIR = Path("samples/day07/validation/normal")
TEST_DIR = Path("samples/day07/test")
REPORT_DIR = Path("reports")
RULE_PATH = Path("configs/day07_spatial_rules.json")

# 기존 실험과 동일하게 95백분위수 사용
PERCENTILE = 95

_, reference_map = load_reference(REFERENCE_PATH)
model = create_backbone()


def get_spatial_score(image_path):
    """위치별 특징 차이 중 최댓값을 반환"""
    _, feature_map = extract_features(model, image_path)

    score_map = anomaly_map(feature_map, reference_map)
    return float(np.max(score_map))


# 1. 정상 Validation으로 새 Threshold 결정
val_files = sorted(VAL_DIR.glob("*.png"))
if not val_files:
    raise RuntimeError("Validation 이미지가 없습니다.")

val_scores = [
    get_spatial_score(path) for path in val_files
]

threshold = float(np.percentile(val_scores, PERCENTILE))

RULE_PATH.parent.mkdir(parents=True, exist_ok=True)
RULE_PATH.write_text(
    json.dumps({
        "version": "day07-spatial-v1.1-experimental",
        "score_method": "max_spatial_distance",
        "selected_percentile": PERCENTILE,
        "threshold": threshold,
        "reference_path": str(REFERENCE_PATH),
    }, indent=2),
    encoding="utf-8",
)

print("Spatial Threshold:", round(threshold, 6))

# 2. 고정한 새 Threshold로 Test
rows = []

folders = [
    (TEST_DIR / "normal", "Normal", "good"),
    (TEST_DIR / "anomaly/broken_large", "Anomaly", "broken_large"),
    (TEST_DIR / "anomaly/broken_small", "Anomaly", "broken_small"),
    (TEST_DIR / "anomaly/contamination", "Anomaly", "contamination"),
]

for folder, actual, defect_type in folders:
    for path in sorted(folder.glob("*.png")):
        score = get_spatial_score(path)
        predicted = "Anomaly" if score > threshold else "Normal"

        if actual == "Anomaly":
            error_type = "TP" if predicted == "Anomaly" else "FN"
        else:
            error_type = "FP" if predicted == "Anomaly" else "TN"

        rows.append({
            "file": str(path),
            "defect_type": defect_type,
            "actual": actual,
            "spatial_score": round(score, 6),
            "predicted": predicted,
            "error_type": error_type,
        })

df = pd.DataFrame(rows)
REPORT_DIR.mkdir(parents=True, exist_ok=True)

df.to_csv(
    REPORT_DIR / "day07_spatial_results.csv",
    index=False,
    encoding="utf-8-sig",
)

# 3. 기존 Baseline과 비교
baseline = pd.read_csv(BASELINE_CSV)
old_counts = baseline["error_type"].value_counts()
new_counts = df["error_type"].value_counts()


def metrics(counts):
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
    "Baseline": metrics(old_counts),
    "Spatial": metrics(new_counts),
})

print("\n=== Baseline vs Spatial ===")
print(comparison.to_string())

print("\n=== Spatial defect type results ===")
print(pd.crosstab(df["defect_type"], df["error_type"]))

comparison.to_csv(
    REPORT_DIR / "day07_spatial_comparison.csv",
    encoding="utf-8-sig",
)
