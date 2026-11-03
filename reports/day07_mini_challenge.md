# Day 07 — Mini Challenge: 촬영 조건 변화와 조명 보정 비교

## 1. 실습 내용

7일차에는 MVTec AD bottle의 정상 이미지를 기준으로 이상 여부를 판정했다. Mini Challenge에서는 정상 Test 이미지 `001.png`에 밝기, 흐림, 회전 변화를 주고, 이미 정해 둔 Baseline Rule이 그대로 적용되는지 확인했다.

세 이미지 모두 실제로는 정상이다. 따라서 Anomaly로 판정되면 FP(정상 오탐), Normal로 판정되면 PASS로 기록했다. 기존 ResNet18, Normal Reference, Global Threshold는 바꾸지 않았다.

## 2. Mini Challenge 조건과 최초 결과

- 원본 이미지: `samples/day07/test/normal/001.png`
- Dark: Alpha 0.75
- Blur: Gaussian Kernel 7×7
- Rotation: 10°
- Global Threshold: 0.067458 (정상 Validation의 95 Percentile)

| 이미지 | Global Score | 예측 | 결과 |
|---|---:|---|---|
| `mini_blur.png` | 0.050097 | Normal | PASS |
| `mini_dark.png` | 0.089038 | Anomaly | FP |
| `mini_rotation.png` | 0.046322 | Normal | PASS |

Blur와 Rotation은 정상 판정을 유지했지만, Dark에서는 실제 결함이 없는데도 Score가 Threshold를 넘어 FP가 발생했다. 이 세 조건에서는 밝기를 낮춘 변형이 가장 큰 문제였다.

## 3. 기존 개선 방식으로 재검사

기본 실습의 Global 방식 외에, 위치별 Feature Map 차이의 최댓값을 사용하는 Spatial 방식과 두 방식의 OR 결합 결과도 같은 이미지에 적용해 보았다. OR 방식은 Global과 Spatial 중 하나라도 Anomaly면 최종 Anomaly로 판정한다.

- Global Threshold: 0.067458
- Spatial Threshold: 0.715893 (정상 Validation의 95 Percentile)

| 이미지 | Global Score | Global | Spatial Score | Spatial | Combined |
|---|---:|---|---:|---|---|
| `mini_blur.png` | 0.050097 | PASS | 0.405296 | PASS | PASS |
| `mini_dark.png` | 0.089038 | FP | 0.413865 | PASS | FP |
| `mini_rotation.png` | 0.046322 | PASS | 0.462891 | PASS | PASS |

Dark를 Spatial 방식으로 검사했을 때는 정상으로 통과했지만, Combined에서는 Global의 FP가 그대로 반영됐다. 앞서 Combined 방식이 작은 파손의 미검출을 줄였던 것과는 별개로, 밝기 변화로 생긴 FP까지 해결한 것은 아니었다.

## 4. 밝기 보정 추가 실험

Dark FP를 줄일 수 있는지 확인하기 위해 입력 이미지에 Gamma 0.7과 CLAHE를 각각 적용했다. 보정된 이미지에서 Global Score를 다시 계산했고, 기존 Global Threshold 0.067458은 그대로 사용했다. 원본 정상 기준은 다시 만들지 않았다.

| 이미지 | Original | Gamma 0.7 | CLAHE |
|---|---:|---:|---:|
| `mini_blur.png` | 0.050097 (PASS) | 0.091344 (FP) | 0.120596 (FP) |
| `mini_dark.png` | 0.089038 (FP) | 0.099575 (FP) | 0.144286 (FP) |
| `mini_rotation.png` | 0.046322 (PASS) | 0.095089 (FP) | 0.120981 (FP) |
| **FP 합계** | **1/3** | **3/3** | **3/3** |

기대한 것과 달리 두 보정 방법 모두 Dark의 FP를 줄이지 못했다. 오히려 원래 정상으로 통과했던 Blur와 Rotation도 FP로 바뀌었다. 시험한 세 이미지에서는 보정 후 모든 Score가 증가했다.

## 5. 실패 분석

Normal Reference는 원본 정상 이미지에서 추출한 특징으로 만들었다. 이번에는 그 기준을 유지한 채 검사 이미지만 보정했으므로, 보정이 정상 기준과 입력 이미지 사이의 특징 차이를 더 크게 만들었을 가능성이 있다. 다만 이 결과만으로 정확한 원인을 확정할 수는 없다.

또 Gamma 0.7이나 CLAHE가 일반적인 시각적 밝기·대비 개선에 유용하더라도, ResNet18이 계산한 이상 점수를 반드시 낮춰 주는 것은 아니라는 점을 확인했다.

이번 실험은 정상 이미지 한 장에서 만든 변형 3개를 대상으로 한 탐색적 비교다. 여기에서 FP가 몇 개 발생했는지만으로 전처리의 일반적인 성능을 평가할 수는 없다. 보정 방법을 실제 검사 파이프라인에 넣으려면 정상 기준과 Validation 설정을 함께 검토하고, 별도의 정상·결함 이미지로 재평가해야 한다.

## 6. 결과 정리

Mini Challenge에서는 Dark 조건의 FP가 발생했다. 앞서 만든 Spatial 방식은 Dark를 정상으로 판정했지만, OR 결합 방식은 Global의 FP를 그대로 유지했다. 이어서 Gamma 0.7과 CLAHE를 적용했으나 오탐을 줄이지 못했고, 세 이미지 모두 FP로 판정됐다.

따라서 이번에는 조명 변화 문제를 해결했다고 기록하지 않았다. 작은 파손 미검출 개선과 조명 변화에 대한 강건성은 구분해서 검증해야 한다는 점을 확인했다.

## 7. 실행 코드 및 결과 파일

- `src/61_day07_mini_challenge.py` — Dark·Blur·Rotation 최초 검사
- `src/day07_check_mini_combined.py` — Global·Spatial·Combined 재검사
- `src/day07_improve_lighting.py` — Gamma·CLAHE 비교
- `reports/day07_mini_combined_check.csv` — 세 판정 방식 비교
- `reports/day07_lighting_experiment.csv` — 보정 전후 Global Score
- `configs/day07_anomaly_rules.json`, `configs/day07_spatial_rules.json` — 기존 Threshold
