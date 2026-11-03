import json
from pathlib import Path

import numpy as np
import pandas as pd

from day07_anomaly_core import (
    anomaly_map,
    anomaly_score,
    create_backbone,
    extract_features,
    load_reference,
)

VARIANT_DIR = Path('samples/day07/mini_challenge/variants')
REFERENCE = Path('artifacts/day07/normal_reference.npz')
GLOBAL_RULE = Path('configs/day07_anomaly_rules.json')
SPATIAL_RULE = Path('configs/day07_spatial_rules.json')
OUTPUT = Path('reports/day07_mini_combined_check.csv')

for path in [VARIANT_DIR, REFERENCE, GLOBAL_RULE, SPATIAL_RULE]:
    if not path.exists():
        raise FileNotFoundError(f'Missing: {path}')

images = sorted(VARIANT_DIR.glob('mini_*.png'))
if len(images) != 3:
    raise RuntimeError(f'Expected 3 mini images; found {len(images)}. Do not rerun 61 until checking missing images.')

global_limit = float(json.loads(GLOBAL_RULE.read_text(encoding='utf-8'))['anomaly_threshold'])
spatial_limit = float(json.loads(SPATIAL_RULE.read_text(encoding='utf-8'))['threshold'])
reference_vector, reference_map = load_reference(REFERENCE)
model = create_backbone()
rows = []

for path in images:
    vector, feature_map = extract_features(model, path)
    global_score = anomaly_score(vector, reference_vector)
    spatial_score = float(np.max(anomaly_map(feature_map, reference_map)))
    global_ng = global_score > global_limit
    spatial_ng = spatial_score > spatial_limit
    combined_ng = global_ng or spatial_ng

    rows.append({
        'image': path.name,
        'global_score': round(global_score, 6),
        'global_result': 'FP' if global_ng else 'PASS',
        'spatial_score': round(spatial_score, 6),
        'spatial_result': 'FP' if spatial_ng else 'PASS',
        'combined_result': 'FP' if combined_ng else 'PASS',
    })

result = pd.DataFrame(rows)
OUTPUT.parent.mkdir(parents=True, exist_ok=True)
result.to_csv(OUTPUT, index=False, encoding='utf-8-sig')
print(f'Global threshold: {global_limit:.6f}')
print(f'Spatial threshold: {spatial_limit:.6f}')
print('\n=== Mini Challenge: Global vs Spatial vs Combined ===')
print(result.to_string(index=False))
print(f'\nSaved: {OUTPUT}')
