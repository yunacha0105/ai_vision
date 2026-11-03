
# Day 08 — Support Count Challenge
# 정상/불량 Support 수를 1, 3, 5장으로 바꿔 성능 비교

import csv
from pathlib import Path

from day08_feature_core import (
    create_feature_model,
    extract_feature,
    build_prototype,
    cosine_similarity,
)

SUPPORT_ROOT = Path("samples/day08/few_shot/support")
QUERY_ROOT = Path("samples/day08/common_query")

SUMMARY_CSV = Path("reports/day08_support_count_challenge.csv")
DETAIL_CSV = Path("reports/day08_support_count_details.csv")

SUPPORT_COUNTS = [1, 3, 5]

# 기존 Few-shot과 동일한 ResNet18 사용
model = create_feature_model()

normal_files = sorted(
    (SUPPORT_ROOT / "normal").glob("*.png")
)
anomaly_files = sorted(
    (SUPPORT_ROOT / "anomaly").glob("*.png")
)

query_items = []

for path in sorted(
    (QUERY_ROOT / "normal").glob("*.png")
):
    query_items.append((path, "Normal"))

for path in sorted(
    (QUERY_ROOT / "anomaly/broken_small").glob("*.png")
):
    query_items.append((path, "Anomaly"))

if len(normal_files) < 5 or len(anomaly_files) < 5:
    raise RuntimeError("Support 이미지가 5장씩 필요합니다.")

if not query_items:
    raise RuntimeError("Common Query 이미지가 없습니다.")

# 이미지별 Feature는 한 번씩만 추출
normal_features = [
    extract_feature(model, path)
    for path in normal_files
]

anomaly_features = [
    extract_feature(model, path)
    for path in anomaly_files
]

query_features = [
    extract_feature(model, path)
    for path, _ in query_items
]

summary_rows = []
detail_rows = []

for count in SUPPORT_COUNTS:

    # 앞에서부터 count장 선택
    normal_prototype = build_prototype(
        normal_features[:count]
    )
    anomaly_prototype = build_prototype(
        anomaly_features[:count]
    )

    tp = tn = fp = fn = 0

    for (path, actual), feature in zip(
        query_items, query_features
    ):

        normal_sim = cosine_similarity(
            feature, normal_prototype
        )
        anomaly_sim = cosine_similarity(
            feature, anomaly_prototype
        )

        predicted = (
            "Normal"
            if normal_sim >= anomaly_sim
            else "Anomaly"
        )

        if actual == "Anomaly" and predicted == "Anomaly":
            result = "TP"
            tp += 1
        elif actual == "Normal" and predicted == "Normal":
            result = "TN"
            tn += 1
        elif actual == "Normal":
            result = "FP"
            fp += 1
        else:
            result = "FN"
            fn += 1

        sample_id = (
            f"normal/{path.name}"
            if actual == "Normal"
            else f"anomaly/broken_small/{path.name}"
        )

        detail_rows.append({
            "support_count": count,
            "sample_id": sample_id,
            "actual": actual,
            "predicted": predicted,
            "normal_similarity": round(normal_sim, 6),
            "anomaly_similarity": round(anomaly_sim, 6),
            "error_type": result,
            "correct": actual == predicted,
        })

    total = tp + tn + fp + fn
    accuracy = (tp + tn) / total
    precision = tp / (tp + fp) if tp + fp else 0
    recall = tp / (tp + fn) if tp + fn else 0

    summary_rows.append({
        "support_count": count,
        "samples": total,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "tp": tp,
        "tn": tn,
        "fp": fp,
        "fn": fn,
    })

# CSV 저장
SUMMARY_CSV.parent.mkdir(parents=True, exist_ok=True)

for output_path, rows in [
    (SUMMARY_CSV, summary_rows),
    (DETAIL_CSV, detail_rows),
]:
    with output_path.open(
        "w", newline="", encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=rows[0].keys()
        )
        writer.writeheader()
        writer.writerows(rows)

# 결과 출력
print("=" * 70)
print("DAY08 SUPPORT COUNT CHALLENGE")
print("=" * 70)

for row in summary_rows:
    print(
        f"Support {row['support_count']} | "
        f"Accuracy={row['accuracy']:.4f} | "
        f"Precision={row['precision']:.4f} | "
        f"Recall={row['recall']:.4f} | "
        f"TP={row['tp']} TN={row['tn']} "
        f"FP={row['fp']} FN={row['fn']}"
    )

print()
print("Saved:", SUMMARY_CSV)
print("Saved:", DETAIL_CSV)
