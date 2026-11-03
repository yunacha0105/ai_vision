
# Day08 Improvement — Cut-Paste 품질 개선
# 기존 합성 5장과 같은 원본을 사용해 개선 효과 비교

import csv
from pathlib import Path

import cv2
import numpy as np

from day08_cutpaste_core import extract_patch, rotate_pair


ROOT = Path("samples/day08/mini_challenge")
BASELINE_DIR = Path("outputs/day08/mini_challenge/generated")
INPUT_CSV = Path("reports/day08_mini_challenge_metadata.csv")

IMPROVED_DIR = Path("outputs/day08/improvement/generated")
COMPARE_DIR = Path("outputs/day08/improvement/comparison")
OUTPUT_CSV = Path("reports/day08_improvement_metadata.csv")

IMPROVED_DIR.mkdir(parents=True, exist_ok=True)
COMPARE_DIR.mkdir(parents=True, exist_ok=True)

# 실험 설정
SIZE_RATIO = 0.40
BLUR_KERNEL = (9, 9)

# 중앙 위치 제한 (이미지 너비·높이의 비율)
CENTER_X_RANGE = (0.35, 0.65)
CENTER_Y_RANGE = (0.25, 0.75)

with INPUT_CSV.open("r", encoding="utf-8-sig") as f:
    baseline_rows = list(csv.DictReader(f))

if len(baseline_rows) != 5:
    raise RuntimeError("기존 Challenge 2 메타데이터 5장이 필요합니다.")

results = []

for row in baseline_rows:
    name = row["synthetic_file"]

    normal_path = ROOT / "normal" / row["source_normal"]
    defect_root = ROOT / "defect_source/contamination"
    defect_path = defect_root / "images" / row["source_defect"]
    mask_path = (
        defect_root / "masks"
        / f"{Path(row['source_defect']).stem}_mask.png"
    )

    # 기존 결과와 원본 읽기
    baseline = cv2.imread(str(BASELINE_DIR / name))
    background = cv2.imread(str(normal_path))

    if baseline is None or background is None:
        raise FileNotFoundError(name)

    # 기존과 같은 결함 원본 및 회전각 사용
    patch, mask = extract_patch(defect_path, mask_path)

    original_scale = float(row["scale"])
    new_scale = original_scale * SIZE_RATIO
    angle = float(row["rotation"])

    new_w = max(4, int(patch.shape[1] * new_scale))
    new_h = max(4, int(patch.shape[0] * new_scale))

    patch = cv2.resize(
        patch, (new_w, new_h),
        interpolation=cv2.INTER_LINEAR
    )
    mask = cv2.resize(
        mask, (new_w, new_h),
        interpolation=cv2.INTER_NEAREST
    )
    patch, mask = rotate_pair(patch, mask, angle)

    # 기존 합성 위치의 중심을 최대한 유지
    image_h, image_w = background.shape[:2]
    old_cx = int(row["x"]) + int(row["width"]) // 2
    old_cy = int(row["y"]) + int(row["height"]) // 2

    # 중심이 지정 영역 밖이면 가장 가까운 위치로 조정
    cx = int(np.clip(
        old_cx,
        image_w * CENTER_X_RANGE[0],
        image_w * CENTER_X_RANGE[1],
    ))
    cy = int(np.clip(
        old_cy,
        image_h * CENTER_Y_RANGE[0],
        image_h * CENTER_Y_RANGE[1],
    ))

    x = int(np.clip(cx - new_w // 2, 0, image_w - new_w))
    y = int(np.clip(cy - new_h // 2, 0, image_h - new_h))

    # 기존보다 넓게 경계를 부드럽게 처리
    alpha = mask.astype(np.float32) / 255.0
    alpha = cv2.GaussianBlur(alpha, BLUR_KERNEL, 0)
    alpha = alpha[..., None]

    improved = background.copy()
    roi = improved[y:y + new_h, x:x + new_w]

    blended = (
        patch.astype(np.float32) * alpha
        + roi.astype(np.float32) * (1 - alpha)
    )
    improved[y:y + new_h, x:x + new_w] = np.clip(
        blended, 0, 255
    ).astype(np.uint8)

    # 개선 이미지 저장
    cv2.imwrite(str(IMPROVED_DIR / name), improved)

    # 기존 | 개선 결과를 나란히 저장
    comparison = np.hstack([baseline, improved])
    cv2.putText(
        comparison, "BASELINE", (25, 45),
        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 0, 255), 3
    )
    cv2.putText(
        comparison, "IMPROVED", (image_w + 25, 45),
        cv2.FONT_HERSHEY_SIMPLEX, 1.1, (0, 180, 0), 3
    )
    cv2.imwrite(str(COMPARE_DIR / name), comparison)

    results.append({
        "image": name,
        "source_normal": row["source_normal"],
        "source_defect": row["source_defect"],
        "baseline_scale": original_scale,
        "improved_scale": round(new_scale, 4),
        "rotation": angle,
        "x": x,
        "y": y,
        "width": new_w,
        "height": new_h,
        "blur_kernel": 9,
    })

with OUTPUT_CSV.open(
    "w", newline="", encoding="utf-8-sig"
) as f:
    writer = csv.DictWriter(
        f, fieldnames=results[0].keys()
    )
    writer.writeheader()
    writer.writerows(results)

print("=" * 65)
print("DAY08 CUT-PASTE IMPROVEMENT")
print("=" * 65)
print("Generated :", len(results))
print("Improved  :", IMPROVED_DIR)
print("Comparison:", COMPARE_DIR)
print("Metadata  :", OUTPUT_CSV)
