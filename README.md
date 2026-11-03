# Subject 9 Machine Vision

OpenCV 기반 제조 머신비전 검사기술을 10일간 단계적으로 학습하는 교과 폴더입니다.
`main`에는 폴더 구조만 있고, 실습 내용은 팀원별 브랜치에 있습니다.

## 환경 준비

```bash
cd subject9_machinevision
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install opencv-python numpy
python -m pip freeze > requirements.txt
```

모든 코드는 **이 폴더(`subject9_machinevision/`)에서** `python src/파일명.py`로 실행합니다.

## 폴더 구조

```text
subject9_machinevision/
├── data/          # calibration · train · validation · test · challenge (Git 제외)
├── samples/       # 실습 이미지·영상 (Git 제외)
├── outputs/       # 실행 결과 (Git 제외)
├── src/           # 실습 코드 00 ~
├── reports/       # 문제 정의 · 파라미터 표 · 판단 기록
├── .gitignore
└── README.md
```

## 일차별 구성

| 일차 | 주제 | 파일 |
|---|---|---|
| Day 01 | 검사문제 설계 · ROI · 영상/실시간 입력 | `00 ~ 08` |
| Day 02 | Image Enhancement · Threshold / Otsu | `09 ~ 17` |
| Day 03 | Morphology · Contour · Rule 판정 | `18 ~ 23` |
| Day 04 | GrabCut · Template · Feature Matching · Homography | `24 ~ 32` |
| Day 05 | Calibration · Rule Freeze · Test | `33 ~ 39` |
| Day 06 | OCR | `40 ~ 49` |
| Day 07 | Anomaly Detection | `50 ~ 61` |
| Day 08 | One-shot / Few-shot | `62 ~ 69` |
| Day 09 | 재현성 · Experiment · Hybrid | `70 ~ 79` |
| Day 10 | 서비스화 (FastAPI · Dashboard) | `80 ~ 83` |

## Day 01 — 검사 문제 정의와 ROI 설정

병뚜껑 유무를 검사 대상으로 정하고, 뚜껑이 있는 상태를 OK, 없는 상태를 NG로 구분했다. 먼저 정지 이미지에서 ROI를 정한 뒤 여러 이미지와 영상에 같은 검사 영역을 적용해 보았다.

- `03_roi_crop.py`에서는 `(170, 120, 470, 450)` 영역을 사용했다. `04_batch_roi.py`에서는 병 입구까지 포함되도록 아래쪽 경계를 500으로 늘려 5개 이미지에 적용했다.
- `05_video_input.py`, `06_video_roi.py`로 동영상 프레임을 읽고 ROI를 추출했다. 영상에서는 병이 움직이면 고정된 ROI와 실제 병뚜껑 위치가 어긋날 수 있다는 점을 확인했다.
- `08_phone_camera_roi.py`에서는 스마트폰 실시간 영상에서 직접 ROI를 지정하고 `cap_on.jpg`, `cap_off.jpg`를 저장했다. 이 사진을 2일차 기준 이미지로 활용했다.

병뚜껑을 보려면 병 전체보다 상단의 뚜껑과 병 입구가 함께 들어오는 영역이 중요했다. 다만 1일차에는 ROI를 확보하는 데 집중했으며, 자동 OK/NG 판정 기준은 만들지 않았다.

- 코드: `src/00_check_env.py` ~ `src/08_phone_camera_roi.py`
- 보고서: `reports/day01_problem_definition.md`, `reports/dataset_roles.csv`

## Day 02 — 영상 전처리 및 Otsu 비교

1일차에서 정한 ROI를 이용해 Color Space, 밝기·대비 조정, Gamma, CLAHE, Gaussian/Median/Bilateral Filter, Sharpening, Threshold와 Otsu를 실습했다. 파라미터가 바뀌면 이미지의 선명도와 밝기는 달라지지만, 그것이 곧바로 객체 분리 개선을 의미하지는 않았다.

Mini Challenge에서는 밝은 병뚜껑과 회색 배경의 명도가 비슷해 Otsu만으로는 분리가 잘되지 않는 사진을 사용했다. 아래 조건으로 비교했다.

| 방법 | 비교한 조건 | 관찰 |
|---|---|---|
| CLAHE | `clipLimit=1.0/2.0/3.0` | 3.0에서는 표면과 배경 잡음이 지나치게 강조됨 |
| Gamma | `1.2/1.5` | 전체 밝기는 달라졌지만 뚜껑과 배경의 분리는 개선되지 않음 |
| Gaussian | `5×5` | 작은 잡음은 줄었으나 밝은 객체와 배경을 구분하는 문제는 남음 |

최종적으로 `17_day02_challenge.py`에는 **`result = image.copy()`**를 적용해 전처리를 사용하지 않았다. 전처리 없이도 분리가 잘됐다는 뜻이 아니라, 시험한 방법들이 분리 문제를 충분히 개선하지 못했기 때문이다. Gaussian 5×5는 이후 형태 측정 단계에서 다시 비교할 후보로 남겼다.

- 코드: `src/09_color_space.py` ~ `src/17_day02_challenge.py`
- 보고서: `reports/day02_parameter_table.csv`, `reports/day02_preprocess_reason.md`

## Day 03 — 진행 상태

3일차의 Morphology, Contour, Rule 판정은 이번 정리에서 완료한 실습으로 기록하지 않았다. 별도로 보완할 예정이다.

## Day 04 — 객체 분리 및 이미지 매칭

광천김 포장지로 GrabCut, MeanShift, Template Matching, ORB, SIFT, Homography를 실습했다. GrabCut에서는 초기 사각형 크기에 따른 전경 분리 결과를, MeanShift에서는 `sp`, `sr` 값에 따른 색상 단순화 결과를 비교했다. 이후 같은 로고에 대해 Template Matching의 Score와 위치, ORB·SIFT의 Good Match, Homography의 Inlier를 확인했다.

기본 실습에서는 `24_day04_prepare.py`로 정면 원본 한 장에서 `normal`, `shift`, `rot15`, `scale90` 이미지를 생성했다. 회전하거나 크기가 달라졌을 때 Template Matching의 결과가 달라지는 점을 확인했고, ORB·SIFT와 Homography 결과도 비교했다.

### Mini Challenge

Mini Challenge에서는 비타민 음료병을 새로 촬영해 `VITAMIN C 1000 mg` 글자 영역을 찾았다. 실제 촬영에서는 위치뿐 아니라 회전·거리·반사에 따라 글자의 크기와 방향도 달라지므로 **SIFT + RANSAC + Homography**를 선택했다.

| 사진 | Good Match | Inlier | Inlier Ratio | 검출 결과 |
| --- | ---: | ---: | ---: | --- |
| `shift.jpg` | 44 | 32 | 72.73% | 정상 |
| `rotate.jpg` | 73 | 60 | 82.19% | 정상 |
| `distance.jpg` | 48 | 41 | 85.42% | 정상 |
| `tilt_glare.jpg` | 63 | 61 | 96.83% | 정상 |

네 조건 모두 결과 이미지의 녹색 사각형이 실제 글자 영역을 감싸고 있었다. 다만 같은 제품의 정상 로고만 검사했기 때문에 잘못된 로고에 대한 오검출 여부는 확인하지 못했다. 최종 OK/NG 기준은 5일차 Calibration에서 다룬다.

### 실행 및 결과 파일

프로젝트 폴더에서 다음 명령어를 실행한다.

```bash
python src/32_day04_challenge.py
```

실행 후 `full_front.jpg`에서 ROI를 선택하고 `SPACE` 또는 `ENTER`로 확정한다.

- 코드: `src/24_day04_prepare.py` ~ `src/32_day04_challenge.py`
- 기본 실습 비교표: `reports/day04_template_results.csv`, `day04_orb_results.csv`, `day04_sift_results.csv`, `day04_homography_results.csv`, `day04_rotation_compare.csv`
- Mini Challenge 결과: `reports/day04_challenge_results.csv`
- Mini Challenge 분석: `reports/day04_method_selection.md`
- 촬영 사진: `samples/day04/my_challenge/`
- 결과 이미지: `outputs/day04/my_challenge/`


## Day 05 — Calibration · 복합 Rule · Test

4일차에서 사용한 로고 매칭 값을 이용해 OK/NG 판정 기준을 정했다. 광천김 로고의 Template Score, SIFT Good Match, Inlier Ratio를 Calibration 12장에서 비교하고, SIFT와 Inlier Ratio를 함께 사용하는 복합 Rule을 적용했다.

광천김 Baseline은 SIFT Good Match ≥ 129, Inlier Ratio ≥ 0.8664, Homography Found = 1로 고정했다. Calibration에서는 12장 중 11장을 맞혔지만, Test에서는 NG 3장을 모두 검출하고 정상 3장도 모두 NG로 판정했다.

Test Accuracy는 50%, NG Recall은 100%였으며 FP 3건 모두 Inlier Ratio 기준 미달로 발생했다. Test 결과에 맞춰 기존 Rule을 수정하지는 않았다.

### Mini Challenge — 비타민 음료 로고

4일차에 사용한 `VITAMIN C 1000 mg` 라벨을 대상으로 정상 사진과 로고 일부를 가린 사진을 촬영했다. Calibration 6장(OK 3장, NG 3장)으로 기준을 정하고, 별도의 Test 4장(OK 2장, NG 2장)에 적용했다.

| 구분 | Good Match | Inlier Ratio |
|---|---:|---:|
| Calibration OK | 51~69 | 0.8551~0.9020 |
| Calibration NG | 22~47 | 0.6800~0.7872 |

Calibration 측정 범위를 기준으로 SIFT Good Match ≥ 50, Inlier Ratio ≥ 0.82, Homography Found = 1을 Baseline v1.0으로 고정했다. Calibration에서는 6장 모두 올바르게 판정됐다.

| Test | TP | TN | FP | FN | Accuracy |
|---|---:|---:|---:|---:|---:|
| 비타민 음료 4장 | 2 | 0 | 2 | 0 | 50% |

Test 정상 사진 두 장은 Good Match 기준을 통과했지만 Inlier Ratio가 낮아 NG로 판정됐다. 반대로 `test_ng_02.jpg`는 Inlier Ratio가 0.8571이었지만 Good Match가 7개여서 NG로 판정됐다.

Calibration에서 정한 기준이 Test 사진에도 그대로 적용되는지 확인했으며, 정상 사진의 Inlier Ratio가 예상보다 낮게 측정되는 문제가 있었다.

### 실행 코드 및 결과 파일

- 코드: `src/day05_logo_features.py`, `src/33_day05_check_features.py` ~ `src/41_day05_mini_test.py`
- 광천김 기본 실습: `reports/day05_calibration_measurements.csv`, `reports/day05_rule_candidates.csv`, `reports/day05_test_results.csv`, `reports/day05_test_metrics.md`
- 비타민 음료 결과: `reports/day05_mini_calibration.csv`, `reports/day05_mini_test_results.csv`, `reports/day05_mini_challenge.md`
- 판정 Rule: `configs/day05_logo_rules.json`, `configs/day05_vitamin_rules.json`

## Day 06 — OCR 기반 문자 검사

제품 측면에 인쇄된 SN 13자리를 OCR로 읽고, 실제 인쇄값 및 Expected SN과 비교해 OK/NG를 판정했다. 이미지마다 SN 위치가 달라 ROI를 각각 선택해 저장했고, 대표 이미지에서 Original, Gray, CLAHE, Otsu, CLAHE+Otsu를 비교했다. Original·Gray·CLAHE는 13자리를 정확히 읽었지만 Otsu와 CLAHE+Otsu에서는 일부 숫자가 잘못 인식됐다.

초기 ROI는 세로 범위를 너무 좁게 잡아 첫 번째 SN이 잘못 읽혔다. ROI를 다시 지정한 뒤 `original`, 4배 확대, PSM 7, 숫자 Whitelist를 `day06-ocr-v1.0`으로 사용했다. 최종 Batch 검사에서는 6장 모두 실제 인쇄값을 정확히 읽었고, 교육용 NG 2장을 포함한 제품 OK/NG 판정도 6장 모두 맞혔다.

환경 변화 테스트에서는 Low Contrast만 정확히 인식했다. Blur와 Glare는 문자를 읽지 못했고, Tilt에서는 `9728`만 인식했다. Tilt를 -8도로 보정한 경우에도 OCR 결과는 빈 문자열이었다. 정상 이미지에서는 맞던 설정이 영상 상태가 달라졌을 때는 그대로 유지되지 않았다.

### Mini Challenge — Ch.-B. 코드 검사

새 제품 이미지 4장에서는 `Ch.-B.` 코드 영역만 선택하고 영문·숫자·하이픈을 허용해 OCR을 실행했다. 4장 중 3장은 정확하게 읽었지만 `TI776224-2D`의 마지막 `D`를 `0`으로 인식해 OCR 정확도는 75%였다.

| 전처리 | `TI776224-2D` OCR 결과 |
|---|---|
| Original | `11776224-20` |
| Gray | `T1776224-20` |
| CLAHE | `TI776224-20` |
| Otsu | `TIT76724-20` |
| CLAHE + Otsu | `T1778224-20` |

같은 실패 이미지에 전처리 5가지를 적용했지만 정확한 문자열로 읽은 경우는 없었다. 이후 `^[A-Z0-9-]+$` 대신 `^[A-Z]{2}[0-9]{6}-[0-9][A-Z]$`를 적용하니 마지막 자리가 숫자로 잘못 읽힌 `TI776224-20`을 형식 오류로 걸러낼 수 있었다. OCR 정확도는 그대로 75%이며, 이번 수정은 문자열 형식 검사의 개선이다. 새 Regex는 실습 이미지 4장의 형식에 맞춰 정한 것으로 실제 제품의 공식 규격은 확인하지 않았다.

### 실행 코드 및 결과 파일

- SN OCR 코드: `src/40_day06_check_ocr_env.py` ~ `src/48_day06_challenge.py`, `src/day06_ocr_utils.py`, `src/day06_ocr_validation.py`
- Mini Challenge 코드: `src/49_day06_mini_challenge.py` ~ `src/51_day06_mini_regex_check.py`
- SN 검사 결과: `reports/day06_preprocess_compare.csv`, `reports/day06_ocr_results.csv`, `reports/day06_ocr_metrics.md`
- 환경 변화 테스트: `reports/day06_challenge_results.csv`, `reports/day06_failure_analysis.md`
- Mini Challenge 결과: `reports/day06_mini_challenge_results.csv`, `reports/day06_mini_preprocess_compare.csv`, `reports/day06_mini_regex_results.csv`, `reports/day06_mini_challenge.md`
- OCR 설정 및 정답표: `configs/day06_ocr_rules.json`, `configs/day06_labels.csv`

## Day 07 — ResNet18 기반 Anomaly Detection

MVTec AD bottle 데이터셋으로 정상 이미지의 특징을 기준 삼아 이상을 검출했다. 사전학습된 ResNet18의 layer3에서 특징을 추출하고, 정상 Train 167장의 평균으로 Normal Reference를 만들었다. 정상 Validation 42장의 Score에서 95 Percentile Threshold를 정해 Test 83장을 평가했다.

Baseline은 Accuracy 92.77%, Precision 96.72%, Recall 93.65%였다. 큰 파손과 오염은 모두 검출했지만 작은 파손 22장 중 4장을 정상으로 판정했다.

### Mini Challenge — 촬영 조건 변화와 보정 시도

정상 Test 이미지 `001.png`에 Dark 0.75, Blur 7, Rotation 10°를 적용하고 기존 Global Threshold 0.067458로 검사했다.

| 조건 | Global Score | 결과 |
|---|---:|---|
| Dark | 0.089038 | FP |
| Blur | 0.050097 | PASS |
| Rotation | 0.046322 | PASS |

Dark에서만 FP가 발생했다. 이후 Spatial과 Global + Spatial OR 결합으로 재검사했지만, Combined에서도 Dark는 FP였다. Global이 이상으로 판정하면 Spatial이 정상으로 판정해도 OR 결합에서는 이상으로 처리되기 때문이다.

Gamma 0.7과 CLAHE를 각각 적용해 Global Score를 다시 측정했다. 원본에서는 FP가 1/3건이었지만 두 보정 방식에서는 각각 3/3건으로 늘었다. 보정만으로 Dark FP를 해결하지 못했고, 정상 기준을 유지한 상태에서 입력 이미지만 바꾸면 점수가 오히려 증가할 수 있음을 확인했다.

### 추가 개선 — 작은 파손 미검출

Global 방식에서 놓친 작은 파손 4장을 줄이기 위해 위치별 Feature Map의 최대 차이를 사용하는 Spatial 방식을 실험했다. Spatial은 작은 파손 22장을 모두 검출했지만 오염 6장을 놓쳤다. 그래서 두 방식 중 하나라도 Anomaly면 불량으로 판단하는 OR 결합을 적용했다.

| 지표 | Global | Spatial | Combined |
|---|---:|---:|---:|
| Accuracy | 92.77% | 91.57% | 97.59% |
| Precision | 96.72% | 98.28% | 96.92% |
| Recall | 93.65% | 90.48% | 100.00% |
| FP | 2 | 1 | 2 |
| FN | 4 | 6 | 0 |

Combined는 기존 Test에서 결함 63장을 모두 검출했고 FP는 2건으로 유지됐다. 다만 Baseline Test 실패를 확인한 뒤 만든 탐색적 결합이므로, 독립적인 미사용 데이터로 재검증해야 한다. 조명 변화 FP도 아직 해결되지 않았다.

### 실행 코드 및 결과 파일

- 기본 실습: `src/50_day07_check_anomaly_env.py` ~ `src/61_day07_mini_challenge.py`, `src/day07_anomaly_core.py`
- 추가 실험: `src/day07_improve_spatial_score.py`, `src/day07_improve_combined.py`, `src/day07_check_mini_combined.py`, `src/day07_improve_lighting.py`
- 기본 결과: `reports/day07_anomaly_scores.csv`, `reports/day07_test_metrics.md`, `reports/day07_challenge_results.csv`
- Mini Challenge 및 조명 비교: `reports/day07_mini_challenge.md`, `reports/day07_mini_combined_check.csv`, `reports/day07_lighting_experiment.csv`
- 개선 비교: `reports/day07_spatial_comparison.csv`, `reports/day07_combined_comparison.csv`, `reports/day07_improvement.md`
- 판정 Rule: `configs/day07_anomaly_rules.json`, `configs/day07_spatial_rules.json`
