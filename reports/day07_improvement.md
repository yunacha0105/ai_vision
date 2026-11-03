# Day 07 — Anomaly Detection 추가 개선 실험

## 1. 실험 목적

기본 실습에서는 ResNet18의 layer3에서 추출한 전체 Feature Vector를 정상 기준과 비교했다. Test 83장 중 77장을 올바르게 판정했지만, 작은 파손 22장 중 4장을 정상으로 판단했다. 이미지 전체의 특징을 하나로 요약하면서 작은 결함의 차이가 약하게 반영됐을 가능성을 확인해 보고자 했다.

Mini Challenge에서는 별도로 어두운 정상 이미지가 FP로 판정되는 문제도 나왔다. 이 문서의 Spatial·Combined 실험은 **작은 파손의 FN을 줄이기 위한 실험**이고, Mini Challenge의 조명 FP는 별도로 확인했다.

## 2. Spatial 방식 적용

기존 Global Score는 이미지 전체 Feature Vector와 Normal Reference Vector의 유클리드 거리다. 추가로 같은 ResNet18에서 추출한 위치별 Feature Map을 정상 기준 Map과 비교하고, 가장 큰 위치별 거리를 Spatial Score로 사용했다.

기존 Normal Reference는 재사용했고, Spatial Threshold는 정상 Validation 42장의 점수에서 95 Percentile로 정했다. Test 결과를 기준으로 Threshold를 다시 맞추지는 않았다.

- Global Threshold: 0.067458
- Spatial Threshold: 0.715893

계산 방식이 다른 두 점수는 수치의 크기를 직접 비교할 수 없다.

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

Spatial 방식에서는 작은 파손 22장을 모두 검출했다. 그러나 기존 Global에서는 모두 검출했던 오염 이미지 21장 중 6장을 놓쳤다. FP는 1건 줄었지만 전체 FN이 4건에서 6건으로 늘어, Spatial만으로 Baseline을 대체하기는 어려웠다.

## 4. Global + Spatial 결합

두 방식에서 놓치는 결함 종류가 달랐기 때문에, Global 또는 Spatial 중 하나라도 Anomaly로 판정하면 최종 Anomaly로 처리하는 OR 결합을 비교했다. 각 방식의 Threshold는 그대로 사용했고, 이미 측정한 Test 결과 CSV를 결합했다. 새 모델을 학습한 것은 아니다.

| 지표 | Global | Spatial | Combined |
|---|---:|---:|---:|
| Accuracy | 92.77% | 91.57% | 97.59% |
| Precision | 96.72% | 98.28% | 96.92% |
| Recall | 93.65% | 90.48% | 100.00% |
| TP | 59 | 57 | 63 |
| TN | 18 | 19 | 18 |
| FP | 2 | 1 | 2 |
| FN | 4 | 6 | 0 |

Combined에서는 결함 63장을 모두 검출했다. Global이 놓쳤던 작은 파손 4장은 Spatial이 보완했고, Spatial이 놓쳤던 오염 6장은 Global이 보완했다. 정상 20장 중 2장은 여전히 FP였다.

## 5. Mini Challenge와의 연결 확인

결합 방식이 촬영 환경의 오탐에도 도움이 되는지, Mini Challenge에서 만든 정상 변형 3장을 다시 검사했다.

| 변형 | Global | Spatial | Combined |
|---|---|---|---|
| Blur | PASS | PASS | PASS |
| Dark | FP | PASS | FP |
| Rotation | PASS | PASS | PASS |

Dark에서는 Spatial이 정상으로 판단했지만 OR 결합의 특성상 Global의 FP가 남았다. 따라서 Combined의 Test Recall이 100%라는 결과만으로 조명 변화에도 강하다고 말할 수는 없다.

Dark FP를 줄이려고 Gamma 0.7과 CLAHE도 시험했다. 하지만 기존 Global Threshold를 유지한 상태에서 Original은 3장 중 FP 1건, Gamma와 CLAHE는 각각 FP 3건이었다. 보정 후 Dark 점수는 각각 0.099575와 0.144286으로, 보정 전 0.089038보다 더 높았다. 이번 전처리 시도는 개선되지 않았다. 자세한 조건과 이미지별 점수는 `reports/day07_mini_challenge.md`에 기록했다.

## 6. 결과 분석과 한계

작은 파손 검출에서는 전체 특징과 위치별 특징의 차이를 함께 활용하는 방식이 유리했다. 반면 조명 변화에 따른 FP는 결합 방식과 이번 밝기 보정으로 해결되지 않았다. 같은 모델을 사용하더라도 검사 점수의 정의와 촬영 환경에 따라 결과가 달라진다는 점을 확인했다.

이번 결합 방식은 Baseline Test의 실패 사례를 확인한 뒤 설계한 **탐색적 개선**이다. 따라서 97.59% Accuracy와 100% Recall을 새로운 데이터에서도 재현할 수 있다고 단정할 수 없다. 독립적인 미사용 Test 데이터가 필요하다. 또한 밝기 보정은 입력 이미지만 바꾼 결과이므로, 실제로 전처리를 도입하려면 정상 기준과 Validation도 함께 구성해 평가해야 한다.

## 7. 정리

Spatial만 사용했을 때는 작은 파손을 모두 검출했지만 오염 미검출이 생겼다. Global과 Spatial을 결합하자 이번 Test에서는 FN이 4건에서 0건으로 줄었고 FP는 2건으로 유지됐다. 다만 Mini Challenge에서 나타난 Dark FP는 그대로였고, Gamma·CLAHE 실험도 실패했다.

이번 결과는 결함 미검출을 줄이는 문제와 촬영 조건 변화에 의한 오탐을 줄이는 문제가 서로 다르다는 점을 보여준다. 두 문제를 함께 해결했다고 기록하지 않고, 각각의 실험 결과와 한계를 분리해 남겼다.

## 8. 관련 파일

- `src/day07_improve_spatial_score.py` — Spatial 점수 및 평가
- `src/day07_improve_combined.py` — Global + Spatial OR 결합
- `src/day07_check_mini_combined.py` — Mini Challenge 판정 비교
- `src/day07_improve_lighting.py` — Gamma·CLAHE 실험
- `reports/day07_spatial_results.csv`, `reports/day07_spatial_comparison.csv`
- `reports/day07_combined_results.csv`, `reports/day07_combined_comparison.csv`
- `reports/day07_mini_combined_check.csv`, `reports/day07_lighting_experiment.csv`
- `reports/day07_mini_challenge.md` — 촬영 조건·보정 실패 상세 기록
- `configs/day07_anomaly_rules.json`, `configs/day07_spatial_rules.json`
