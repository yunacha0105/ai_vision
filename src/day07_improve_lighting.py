
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import json

from day07_anomaly_core import (
    create_backbone,
    extract_features,
    load_reference,
    anomaly_score,
)

INPUT_DIR = Path("samples/day07/mini_challenge/variants")
OUTPUT_DIR = Path("outputs/day07/lighting_experiment")
OUTPUT_CSV = Path("reports/day07_lighting_experiment.csv")

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

rules = json.loads(
    Path("configs/day07_anomaly_rules.json").read_text()
)
threshold = float(rules["anomaly_threshold"])

reference_vector, _ = load_reference(
    Path("artifacts/day07/normal_reference.npz")
)
model = create_backbone()


def gamma_correction(image, gamma=0.7):
    lut = np.array([
        np.clip((i / 255.0) ** gamma * 255, 0, 255)
        for i in range(256)
    ], dtype=np.uint8)
    return cv2.LUT(image, lut)


def clahe_correction(image):
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8),
    )
    l = clahe.apply(l)

    merged = cv2.merge([l, a, b])
    return cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)


rows = []

for path in sorted(INPUT_DIR.glob("mini_*.png")):
    image = cv2.imread(str(path))

    if image is None:
        raise FileNotFoundError(path)

    variants = {
        "Original": image,
        "Gamma_0.7": gamma_correction(image),
        "CLAHE": clahe_correction(image),
    }

    for method, processed in variants.items():
        save_path = OUTPUT_DIR / f"{path.stem}_{method}.png"
        cv2.imwrite(str(save_path), processed)

        vector, _ = extract_features(model, save_path)
        score = anomaly_score(vector, reference_vector)

        result = "FP" if score > threshold else "PASS"

        rows.append({
            "image": path.name,
            "method": method,
            "score": round(score, 6),
            "threshold": threshold,
            "result": result,
        })

df = pd.DataFrame(rows)
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print("\n=== DAY07 LIGHTING EXPERIMENT ===")
print(df.to_string(index=False))
print("\nSaved:", OUTPUT_CSV)

