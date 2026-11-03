
# Day 08 — Mini Challenge: Support 수 비교 및 결함 합성

## 1. 실험 목적

8일차에서는 데이터가 적은 상황에서 One-shot과 Few-shot을 이용해 정상·불량을 판정하고, Cut-Paste 방식으로 부족한 결함 데이터를 생성했다.

Mini Challenge에서는 앞서 학습한 방법을 바탕으로 다음 세 가지를 추가로 진행했다.

1. 정상·불량 Support 수를 1장, 3장, 5장으로 바꾸어 성능 비교
2. 기존 `broken_small` 대신 `contamination` 결함 합성
3. 데이터 보유 상황에 따른 검사 방법 선택

## 2. Challenge 1 — Support 수에 따른 성능 비교

기본 Few-shot에서는 정상 Support 5장과 불량 Support 5장으로 각각 Prototype을 생성했다.

이번에는 Support 수를 1장, 3장, 5장으로 변경했다. 정상과 불량 Support 수는 동일하게 유지했으며, 각 조건에서 파일명 순서대로 앞의 1장, 3장, 5장을 사용했다.

평가에는 동일한 Common Query 20장(정상 10장, 작은 파손 10장)을 사용했다. 특징 추출 모델과 판정 방식은 변경하지 않았다.

### 실험 결과

| 지표 | 1장 | 3장 | 5장 |
|---|---:|---:|---:|
| Accuracy | 70.00% | 80.00% | 90.00% |
| Precision | 83.33% | 100.00% | 100.00% |
| Recall | 50.00% | 60.00% | 80.00% |
| TP | 5 | 6 | 8 |
| TN | 9 | 10 | 10 |
| FP | 1 | 0 | 0 |
| FN | 5 | 4 | 2 |

Support 수가 증가하면서 Accuracy는 70%에서 90%로, Recall은 50%에서 80%로 상승했다.

특히 불량을 정상으로 판단한 FN이 5건에서 2건으로 감소했고, 정상 오탐 FP는 1건에서 0건으로 줄었다.

이번 실험에서는 5장의 Support를 사용했을 때 가장 좋은 결과를 얻었다.

다만 Support 이미지 한 조합으로 비교했기 때문에, 이미지 수를 늘리면 항상 성능이 향상된다고 일반화할 수는 없다. 어떤 이미지를 Support로 선택하는지도 결과에 영향을 줄 수 있다.

## 3. Challenge 2 — Contamination 결함 합성

기본 Cut-Paste 실습에서는 `broken_small` 결함을 이용해 합성 이미지를 생성했다.

이번에는 다른 결함 유형에서도 같은 합성 방식이 적용되는지 확인하기 위해 `contamination`을 사용했다.

### 실험 조건

| 항목 | 설정 |
|---|---|
| Dataset | MVTec AD bottle |
| Defect Type | contamination |
| 정상 이미지 | 5장 |
| 결함 원본 | 2장 |
| 생성 이미지 | 5장 |
| Seed | 42 |
| Scale | 0.6~1.0 |
| Rotation | -10°~+10° |

`day08_cutpaste_core.py`의 공통 함수를 이용해 실제 결함 이미지와 Ground Truth Mask에서 Patch를 추출하고, 정상 이미지에 합성했다.

### 생성 결과

설정에 따라 `synthetic_000.png`부터 `synthetic_004.png`까지 총 5장의 합성 이미지를 생성했다.

이미지를 직접 확인한 결과, 갈색의 원형 결함 영역이 병 내부에 삽입된 모습이 나타났다.

특히 일부 이미지에서는 결함의 크기가 지나치게 크거나 병 내부 경계와 겹쳐 실제 오염보다 별도의 원형 물체를 붙여 놓은 것처럼 보였다.

| 이미지 | 관찰 결과 |
|---|---|
| synthetic_000.png | 갈색 결함이 크고 병 내부 상단을 넓게 가림 |
| synthetic_001.png | 결함이 내부에 위치하지만 원형 경계가 뚜렷함 |
| synthetic_002.png | 병 중앙 하단에 큰 원형 결함이 나타남 |
| synthetic_003.png | 결함이 병 내부 경계와 겹쳐 부자연스러움 |
| synthetic_004.png | 상대적으로 결함이 덜 두드러지지만 원형 구조와 경계가 남아 있음 |

상대적으로 자연스러운 이미지는 `synthetic_004.png`, 가장 어색한 이미지는 `synthetic_003.png`로 판단했다.

### 결과 분석

Cut-Paste를 이용하면 실제 결함 이미지와 Mask를 재사용해 새로운 합성 데이터를 만들 수 있었다.

하지만 합성 이미지의 생성 성공과 실제 결함 이미지로서의 품질은 별개였다.

이번 결과에서는 결함의 과도한 크기, 합성 위치, 원형 경계 등이 시각적 품질을 떨어뜨렸다. 따라서 합성 데이터를 검사 모델에 사용하기 전에 위치와 형태, 경계가 자연스러운지 확인할 필요가 있었다.

## 4. Challenge 3 — 데이터 상황별 방법 선택

8일차에서 학습한 방법을 실제 데이터 상황에 맞추어 선택했다.

| 데이터 상황 | 선택한 방법 | 선택 이유 |
|---|---|---|
| 정상 데이터는 충분하지만 불량 예제가 없음 | Anomaly Detection | 정상 데이터로 기준을 구성하고 기준에서 벗어나는 특징을 검출할 수 있음 |
| 정상 Reference 1장과 Calibration용 정상 데이터가 있음 | One-shot | 정상 Reference와의 유사도를 계산하고 정상 Calibration 데이터로 Threshold를 설정할 수 있음 |
| 정상·불량 예제가 각각 몇 장씩 있음 | Few-shot | 소수의 정상·불량 이미지로 Prototype을 생성해 비교할 수 있음 |
| 실제 불량 이미지가 부족해 데이터 보강이 필요함 | Defect Generation | 기존 결함과 Mask를 이용해 합성 데이터를 생성할 수 있음 |

Defect Generation은 자체적으로 정상·불량을 판정하는 검사 방법이 아니라 데이터 보강 방법이다. 따라서 합성 데이터를 실제 학습에 활용하려면 별도의 검사 모델과 성능 검증이 필요하다.

## 5. Mini Challenge 정리

Support 수 비교에서는 1장에서 5장으로 늘렸을 때 Accuracy가 70%에서 90%로 향상됐고, FN은 5건에서 2건으로 감소했다.

Contamination Cut-Paste에서는 새로운 결함 유형의 합성 이미지 5장을 만들었지만, 일부 이미지에서 결함 크기와 위치가 부자연스러웠다.

마지막으로 데이터가 어떤 형태로 확보되어 있는지에 따라 One-shot, Few-shot, Anomaly Detection, Defect Generation의 활용 목적이 다르다는 점을 정리했다.

이번 실습을 통해 적은 데이터로 검사할 때는 이미지 수뿐 아니라 Support 이미지의 대표성과 합성 데이터의 품질도 중요하다는 점을 확인했다.

## 6. 관련 파일

- `src/day08_support_count_challenge.py` — Support 수 1·3·5장 비교
- `src/day08_mini_challenge.py` — Contamination Cut-Paste
- `reports/day08_support_count_challenge.csv` — Support 수별 성능
- `reports/day08_support_count_details.csv` — 이미지별 판정
- `reports/day08_mini_challenge_metadata.csv` — 합성 이미지 정보
- `outputs/day08/mini_challenge/generated/` — 합성 이미지 5장
