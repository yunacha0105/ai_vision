
from pathlib import Path
from day08_cutpaste_core import generate_synthetic_set

# Challenge 2 — contamination 결함 합성
NORMAL_DIR = Path("samples/day08/mini_challenge/normal")

DEFECT_ROOT = Path(
    "samples/day08/mini_challenge/defect_source/contamination"
)

OUTPUT_DIR = Path("outputs/day08/mini_challenge/generated")
METADATA_PATH = Path("reports/day08_mini_challenge_metadata.csv")

# 합성 조건
rows = generate_synthetic_set(
    normal_dir=NORMAL_DIR,
    defect_image_dir=DEFECT_ROOT / "images",
    defect_mask_dir=DEFECT_ROOT / "masks",
    output_dir=OUTPUT_DIR,
    metadata_path=METADATA_PATH,
    defect_type="contamination",
    count=5,
    seed=42,
    scale_range=(0.6, 1.0),
    angle_range=(-10.0, 10.0),
)

print("=" * 60)
print("DAY08 CHALLENGE 2 — CONTAMINATION")
print("=" * 60)
print("Generated:", len(rows))
print("Images:", OUTPUT_DIR)
print("Metadata:", METADATA_PATH)