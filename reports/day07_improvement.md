# Day 07 — Anomaly Detection 개선 실험

## 1. 실험 목적

7일차 기본 실습에서는 정상 이미지의 평균 특징과 검사 이미지의 특징을 비교해 이상 여부를 판단했다. Test 83장 중 77장을 올바르게 판정했지만, 작은 파손 4장을 정상으로 판단하는 문제가 있었다.

작은 결함은 이미지 전체의 특징을 하나로 요약했을 때 차이가 충분히 드러나지 않을 수 있다고 생각했다. 그래서 기존 Global 방식 대신 위치별 특징을 비교하면 결과가 달라지는지 확인했다.

## 2. Spatial 방식 적용

기존 Global 방식은 ResNet18에서 추출한 전체 Feature Vector와 정상 기준 Vector 사이의 거리를 Anomaly Score로 사용했다.

추가 실험에서는 같은 모델의 Feature Map을 이용했다. 검사 이미지와 정상 기준의 위치별 특징 차이를 계산한 다음, 그중 최댓값을 Spatial Score로 사용했다.

기존 Normal Reference는 그대로 사용했고, Spatial 방식의 Threshold는 정상 Validation 42장에서 다시 계산했다.

- 기존 Global Threshold: 0.067458
- Spatial Threshold: 0.715893
- Threshold 기준: 정상 Validation Score의 95 Percentile

두 점수는 계산 방식과 척도가 다르므로 Threshold의 크기만으로 어느 방식이 더 민감하다고 비교할 수는 없다.

## 3. Spatial 실험 결과

| 지표 | Global | Spatial |
|---|---:|---:|
| Accuracy | 92.77% | 91.57% |
| Precision | 96.72% | 98.28% |
| Recall | 93.65% | 90.48% |
| TP | 59 | 57 |
| TN | 18 | 19 |
| FP | 2 | 1 |
| FN | 4 | 6 |

Spatial 방식에서는 작은 파손 22장을 모두 검출했다. 기존 Global 방식에서 놓친 4장도 검출된 것이다.

하지만 오염 이미지 21장 중 6장을 정상으로 판단했다. FP는 1건 줄었지만 FN은 전체적으로 4건에서 6건으로 증가했다.

작은 파손 검출은 좋아졌으나 전체 성능은 오히려 떨어졌기 때문에 Spatial 방식만으로 Baseline을 대체하기는 어려웠다.

## 4. Global + Spatial 결합

두 방식에서 놓치는 결함 종류가 달랐기 때문에, 하나의 방식만 선택하지 않고 판정 결과를 결합해 보았다.

Global 또는 Spatial 중 하나라도 Anomaly로 판정하면 최종 Anomaly로 처리하는 OR 조건을 적용했다. 두 방식의 Threshold는 앞에서 정한 값을 그대로 사용했다.

이미 계산한 Test 결과 CSV를 합쳐 판정했으며, ResNet18을 다시 학습하거나 특징을 새로 추출하지는 않았다.

## 5. 결합 실험 결과

| 지표 | Global | Spatial | Combined |
|---|---:|---:|---:|
| Accuracy | 92.77% | 91.57% | 97.59% |
| Precision | 96.72% | 98.28% | 96.92% |
| Recall | 93.65% | 90.48% | 100.00% |
| TP | 59 | 57 | 63 |
| TN | 18 | 19 | 18 |
| FP | 2 | 1 | 2 |
| FN | 4 | 6 | 0 |

결합 방식에서는 결함 이미지 63장을 모두 Anomaly로 판정했다. 기존에 놓쳤던 작은 파손 4장도 검출됐으며, Spatial 방식에서 놓쳤던 오염 6장도 Global 판정으로 보완됐다.

정상 이미지 20장 중 18장은 정상으로 통과했고 2장은 FP였다. 결합 후에도 정상 오탐 건수는 기존 Global 방식과 같았다.

## 6. 결과 분석

처음에는 위치별 특징을 사용하면 작은 파손 검출이 좋아질 것으로 예상했다. 실제로 작은 파손은 모두 검출했지만, 예상하지 못했던 오염 미검출이 발생했다.

Global과 Spatial이 같은 ResNet18을 사용하더라도 특징을 비교하는 방법에 따라 결과가 달라진다는 점을 확인했다.

두 방식의 판정을 OR 조건으로 결합하니 이번 Test에서는 서로 놓친 결함을 보완할 수 있었다. 반면 OR 조건은 한쪽 검사에서 FP가 발생해도 최종 FP가 될 수 있으므로, 다른 데이터에서도 정상 오탐이 유지될지는 알 수 없다.

또 이번 개선은 Baseline의 Test 결과를 확인한 뒤 진행했다. 따라서 Combined의 높은 성능은 이미 사용한 Test 데이터에 대한 탐색적 결과이며, 독립적인 미사용 Test 데이터에서 다시 검증해야 한다.

## 7. 정리

Spatial 방식만 사용했을 때는 작은 파손 검출이 개선됐지만 전체 Recall은 떨어졌다. 반대로 Global과 Spatial을 결합했을 때는 이번 Test에서 FN을 4건에서 0건으로 줄일 수 있었다.

이번 실험을 통해 단순히 점수 계산 방법을 바꾸는 것보다 서로 다른 방식의 결과를 함께 활용하는 방법도 비교할 필요가 있다는 점을 알게 됐다.

다만 정상 이미지 2장의 FP는 남아 있다. Mini Challenge에서도 밝기를 낮춘 정상 이미지가 FP로 판정됐기 때문에, 다음에는 조명 조건이 달라졌을 때 결합 방식이 어떻게 반응하는지도 확인해 보고 싶다.

## 8. 관련 파일

- `src/day07_improve_spatial_score.py` — 위치별 Feature Map을 이용한 점수 계산 및 평가
- `src/day07_improve_combined.py` — Global + Spatial OR 결합
- `configs/day07_spatial_rules.json` — Spatial Threshold
- `reports/day07_spatial_results.csv` — Spatial 이미지별 판정 결과
- `reports/day07_spatial_comparison.csv` — Baseline과 Spatial 비교
- `reports/day07_combined_results.csv` — 결합 방식의 이미지별 판정 결과
- `reports/day07_combined_comparison.csv` — 세 방식 성능 비교