## 오늘의 목표

1일차에서는 **검사할 위치를 정하고 ROI를 확보하는 방법**을 배웠습니다.

2일차에서는 이미지의 `Brightness`, `Contrast`, `Noise`, `Blur`를 확인하고 영상.이미지 품질을 개선하는 방법을 배웠습니다.

3일차에서는 병뚜껑을 대상으로 `Area Ratio`, `Count`, `BBox`, `Center` 같은 Feature를 숫자로 측정하고 간단한 Candidate Rule을 만들어 보았습니다.

4일차에서는 광천김 로고를 대상으로 `Template Matching`, `ORB`, `SIFT`, `RANSAC`, `Homography`를 사용하여 로고를 비교하고 측정하는 여러 방법을 실습했습니다.

5일차에서는 여기서 한 단계 더 나아갑니다.

> 여러 정상·불량 이미지의 측정값을 비교하여 실제 OK / NG 기준을 만들고, 그 기준이 새로운 이미지에서도 잘 동작하는지 확인합니다.


오늘의 핵심 질문은 다음과 같습니다.

> 여러 이미지에서 측정한 값을 이용해 어디까지 OK이고 어디부터 NG인지 어떻게 정하고, 
> 그 기준이 새로운 이미지에서도 잘 동작하는지 어떻게 확인할까요?

오늘 수업이 끝나면 다음을 할 수 있어야 합니다.

- Calibration 데이터로 `OK / NG` 기준을 만들 수 있다.
- 여러 Feature를 비교하여 필요한 Rule을 선택할 수 있다.
- 결정한 Rule을 고정하여 새로운 Test 이미지에 적용할 수 있다.
- `TP / TN / FP / FN`으로 검사 결과를 평가할 수 있다.
- 실패한 이미지의 원인을 확인할 수 있다.
- 다른 제품에서도 `Calibration → Rule → Test` 과정을 반복할 수 있다.

> 5일차의 핵심은 Threshold 숫자를 외우는 것이 아니라, 
> 데이터를 근거로 검사 기준을 만들고 검증하는 과정을 익히는 것입니다.

---

# 1. 5일차의 전체 흐름

5일차는 새로운 Matching 알고리즘을 계속 추가하는 날이 아닙니다.

4일차에서 배운 `Template Matching`, `SIFT`, `RANSAC`, `Homography`를 여러 이미지에 반복 적용하여 실제 검사 Rule을 만들고 검증하는 날입니다.

### 5일차 전체 흐름

![[Pasted image 20261028152721.png]]

| 용어              | 의미                           |
| --------------- | ---------------------------- |
| Threshold       | OK/NG를 구분하는 숫자 기준            |
| Threshold 후보 탐색 | 여러 기준값을 시험하는 과정              |
| Calibration     | 정상·불량 데이터를 측정하고 기준 후보를 찾는 과정 |
| Rule            | Threshold를 조합한 판정 규칙         |
| Rule Freeze     | 결정한 판정 규칙을 고정하는 작업           |

그림의 흐름을 간단히 읽으면 다음과 같습니다.

```text
PART1  실습 환경 + 데이터 준비
7~9
        ↓
PART2  측정 이해 + 공통 함수
10~15
        ↓
PART3  Calibration
16~22
측정 → 분포 확인 → Threshold 후보 찾기
        ↓
PART4  Baseline Rule 결정
23~25
Rule 선택 → JSON 저장 → Freeze
        ↓
PART5  Test
26~28
처음 보는 6장에 동결 Rule 적용
        ↓
PART6  Evaluation
29~31
TP / TN / FP / FN + 성능 평가
        ↓
PART7  Mini Challenge
32~38
다른 제품에서
Calibration → Rule → Test 직접 반복
        ↓
PART8  정리
39~43
README + 자가체크 + Git 기록
```

## 2.1 PART1 — 실습 환경과 데이터를 준비합니다

먼저 오늘 사용할 폴더와 데이터를 준비합니다.

```
- Calibration 데이터
- Test 데이터
- Reference 이미지
- 결과 저장 폴더
```

즉, 실습을 시작할 수 있는 기본 환경을 만드는 단계입니다.

---

## 2.2 PART2 — 공통 측정 함수를 준비합니다

4일차에서 배운:

```
- Template Matching
- SIFT
- Homography
```

를 여러 이미지에 반복 적용할 수 있도록 공통 함수로 정리합니다.

![[Pasted image 20261028153154.png]]

---

## 2.3 PART3 — Calibration으로 기준 후보를 찾습니다

Calibration 12장을 측정하고:

```
- OK / NG 값 비교
- X-Y 분포 확인
- Threshold 후보 비교
```

를 통해 판정 기준 후보를 찾습니다.

![[Pasted image 20261028153919.png]]

### X-Y 분포도는 무엇을 비교하나요?

5일차 그림에서는 다음 두 가지 측정값을 사용합니다.

- X축: SIFT Good Match — 기준 로고와 비슷하게 연결된 특징점의 개수
- Y축: Homography Inlier Ratio — 연결된 특징점 중 기하학적 위치 관계까지 일치하는 비율

---

## 2.4 PART4 — 사용할 Rule을 결정합니다

Calibration에서 찾은 기준 중 하나를 선택하고:

```
- 복합 Rule 결정
- JSON 저장
- Baseline Freeze
```

까지 진행합니다.

![[Pasted image 20261028154445.png]]

---

## 2.5 PART5 — 처음 보는 Test 이미지에 적용합니다

동결한 Rule을 Test 6장에 그대로 적용하여:

```
- OK / NG 판정
- 실제 정답과 비교
```

를 진행합니다.

---

## 2.6 PART6 — Test 결과를 평가합니다

Test 결과에서:

```
- TP / TN / FP / FN
- Accuracy
- Precision
- Recall
```

을 확인하고 잘못 판정된 이미지도 살펴봅니다.

| 용어            | 영어             | 이번 수업에서의 의미                 |
| ------------- | -------------- | --------------------------- |
| **TP**        | True Positive  | 실제 NG → NG로 맞게 검출           |
| **TN**        | True Negative  | 실제 OK → OK로 맞게 판정           |
| **FP**        | False Positive | 실제 OK → NG로 잘못 판정           |
| **FN**        | False Negative | 실제 NG → OK로 잘못 통과           |
| **Accuracy**  | Accuracy       | 전체 중 얼마나 많이 맞혔는가            |
| **Precision** | Precision      | NG라고 판정한 것 중 실제 NG가 얼마나 되는가 |
| **Recall**    | Recall         | 실제 NG 중 얼마나 놓치지 않고 찾아냈는가    |

---

## 2.7 PART7 — 다른 제품으로 직접 반복합니다

광천김이 아닌 다른 제품을 사용하여:

```
Calibration → Rule → Test
```

과정을 직접 다시 해봅니다.

---

## 2.8 PART8 — 결과를 정리합니다

마지막으로:

```
- README 정리
- 자가체크
- Git Commit
```

까지 진행하고 5일차를 마무리합니다.

---

# 2. 4일차 데이터에서 5일차를 시작합니다

4일차에서는 **광천김 포장지의 로고 영역**을 검사 대상으로 사용했습니다.

기준이 되는 로고 이미지를 만들고, 같은 제품에 위치·회전·크기 변화를 주어 다음 방법들의 측정 결과를 비교했습니다.

```text
광천김 포장지
        ↓
기준 로고 준비
        ↓
normal / shift / rot15 / scale90
        ↓
Template Matching
ORB
SIFT
Homography
        ↓
Score / Match / Inlier 등
측정값 비교
```

4일차의 목적은 이러한 값을 **측정하고 비교하는 것**이었기 때문에 아직 최종 OK / NG 기준은 정하지 않았습니다.

5일차에서는 여기서 이어서 **같은 광천김 로고 검사 문제를 사용합니다.**

기준 데이터는 4일차에서 만든 다음 파일을 사용합니다.

```
samples/day04/reference/reference_label.jpg
samples/day04/targets/target_normal.jpg
```

그리고 새로운 Calibration 이미지와 Test 이미지를 추가하여 여러 이미지의 측정값을 모읍니다.

```
4일차
광천김 로고의 Matching 방법 학습
        ↓
측정값 확인
        ↓
아직 Rule 확정 X

        ↓

5일차
같은 광천김 로고 검사 계속 사용
        ↓
Calibration 이미지 여러 장 측정
        ↓
정상 / 불량 측정값 비교
        ↓
Threshold 결정
        ↓
복합 Rule
        ↓
Test
        ↓
실패 분석
```

4일차가 ==`“어떻게 측정할 것인가?”`==를 배우는 날이었다면, 
5일차는 ==`“측정한 값을 어떤 기준으로 OK / NG 판정에 사용할 것인가?”`==를 배우는 날입니다.

---

# 3. 오늘 무엇을 검사할까요?

5일차에서도 4일차와 같은 **광천김 로고 검사**를 계속 사용합니다.

## 검사 대상

```text
광천김 포장지의
KC + (주)광천김 + 영문 로고 영역
```

기준이 되는 로고 이미지는 다음 파일입니다.

`reference_label.jpg` : 정답처럼 비교할 기준 로고
![[Pasted image 20260831114455.png]]

이 이미지는 “정상 로고는 이렇게 생겼다”라고 알려주는 기준 이미지입니다.

그리고 실제 검사 대상 이미지는 다음과 같습니다.

`target_normal.jpg` : 그 기준 로고를 찾아볼 검사 이미지
![[Pasted image 20260831114641.png]]

```
reference_label.jpg
→ 찾고 싶은 정상 로고

target_normal.jpg
→ 그 로고가 들어 있는 검사 이미지
```

5일차에서는 이 관계를 기준으로 여러 정상·불량 이미지를 추가하여 검사합니다.

```text
기준 로고
        +
여러 검사 이미지
        ↓
Matching 값 측정
        ↓
정상과 불량 비교
        ↓
OK / NG 기준 결정
```

오늘의 기본 검사 질문은 하나입니다.

```
검사 이미지 안에 기준과 같은 광천김 로고가 정상적으로 존재하는가?
```

### OK

```
로고가 정상적으로 보이고
기준 로고와 충분히 Matching됨
        ↓
OK
```

제품이 조금 이동하거나 회전하더라도 같은 로고가 정상적으로 확인된다면 OK로 볼 수 있습니다.

### NG

```
로고 일부가 가려짐
또는
기준 로고와 충분히 Matching되지 않음
        ↓
NG
```

즉 5일차에서는:

> 정상 로고는 OK로 통과시키고, 로고가 정상적으로 확인되지 않는 이미지는 NG로 검출하는 검사 기준을 만들어 봅니다.

이후에는 여러 Calibration 이미지의 실제 측정값을 비교하여 어느 정도부터 OK / NG로 판단할 것인지 Threshold와 Rule을 결정합니다.

---

# 4. 오늘은 여러 이미지에서 검사값을 비교합니다

4일차에서는 광천김 로고를 찾기 위해 여러 방법을 사용해 보았습니다.

```text
Template Matching
SIFT
Homography
```

그리고 각 방법에서 다음과 같은 **숫자 결과**가 나온다는 것도 확인했습니다.

```text
Template Matching
→ 로고가 얼마나 비슷한가?

SIFT
→ 서로 비슷한 특징점이 얼마나 많이 연결되는가?

Homography
→ 연결된 특징점 중 실제로 올바른 대응이 얼마나 남는가?
```

하지만 이미지 한 장의 결과만 보고 바로:

```
이 값 이상이면 OK
이 값보다 작으면 NG
```

라고 정할 수는 없습니다.

왜냐하면 같은 정상 제품이라도 촬영할 때마다 값이 조금씩 달라질 수 있기 때문입니다.

그래서 오늘은 여러 정상·불량 이미지를 검사하여 실제 값이 어느 정도 나오는지 먼저 확인합니다.

```
정상 이미지 여러 장
        +
불량 이미지 여러 장
        ↓
검사값 측정
        ↓
정상과 불량의 차이 비교
        ↓
OK / NG 기준 결정
```

5일차의 핵심은 검사 기준값을 미리 정하는 것이 아니라 실제 데이터를 측정한 뒤 결정하는 것입니다.

---

# 5. 오늘 사용할 이미지는 역할을 나누어 준비합니다

5일차 본 실습에서는 이미지를 목적에 따라 `Calibration`과 `Test`로 나누어 사용합니다.

| 데이터           | 쉽게 말하면               | 오늘 하는 일                            |
| ------------- | -------------------- | ---------------------------------- |
| `Calibration` | **기준을 만드는 연습용 데이터**  | 정상·불량 값을 비교하여 OK / NG 기준을 결정       |
| `Test`        | **정해진 기준을 시험하는 데이터** | 처음 보는 이미지에서도 판정이 잘 되는지 확인          |

사용 순서는 다음과 같습니다.

```text
Calibration 이미지
        ↓
여러 장을 측정
        ↓
OK / NG 기준 결정
        ↓
Rule 저장

        ↓

Test 이미지
        ↓
정해진 Rule 그대로 검사
        ↓
맞게 판정되는지 확인

```

여기서 중요한 규칙은 하나입니다.

> **Test 결과가 마음에 들지 않는다고 기준을 계속 바꾸지 않습니다.**

기준을 정하는 것은 `Calibration`, 정한 기준을 평가하는 것은 `Test`의 역할이기 때문입니다.

그리고 4일차에서 만든 `reference_label.jpg`는 이 세 그룹과는 다릅니다.

```
reference_label.jpg
→ "이 로고를 찾아라"라고 알려주는 기준 로고

Calibration
→ 얼마부터 OK로 볼지 결정

Test
→ 그 기준이 잘 작동하는지 확인
```

---

```
32_day04_challenge.py
4일차 — 이미지 매칭 방법 실습 완료
            ↓
day05_logo_features.py
Template·SIFT·Homography 공통 측정 함수
            ↓
33_day05_check_features.py
대표 이미지 1장으로 정상 동작 확인
            ↓
34_day05_measure_calibration.py
Calibration 12장 측정 → CSV 저장
            ↓
35_day05_analyze_calibration.py
OK / NG 분포 분석 → Threshold 후보 탐색
            ↓
36_day05_freeze_rule.py
복합 Rule 확정 → JSON 저장
            ↓
37_day05_test.py
새로운 Test 6장 → OK / NG 판정
            ↓
38_day05_evaluate.py
성능 평가 → FP / FN 실패 분석
            ↓
39_day05_mini_challenge.py
다른 제품으로 전체 과정 자율 실습
```

| 파일명                               | 역할                     | 설명                                                                                                             |
| --------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------- |
| `32_day04_challenge.py`           | 4일차 Mini Challenge     | 새로운 실제 촬영 이미지에서 Template·ORB·SIFT·Homography 중 적합한 검사 방법을 직접 선택하고 결과를 비교합니다.                                   |
| `day05_logo_features.py`          | 로고 특징값 측정 공통 함수        | 4일차에서 배운 Template Matching·SIFT·Homography를 함수로 정리하여 여러 이미지의 Score·Good Match·Inlier Ratio 등을 반복 측정할 수 있게 합니다. |
| `33_day05_check_features.py`      | 공통 함수 정상 작동 확인         | 광천김 이미지 1장을 먼저 검사하여 Template Score·SIFT Good Match·Homography·Inlier Ratio가 정상적으로 계산되는지 확인합니다.                 |
| `34_day05_measure_calibration.py` | Calibration 데이터 측정     | 정상(OK) 6장과 불량(NG) 6장, 총 12장의 특징값을 측정하고 결과를 CSV로 저장합니다.                                                         |
| `35_day05_analyze_calibration.py` | 판정 기준(Threshold) 후보 분석 | Calibration 측정값의 정상·불량 분포를 그래프로 비교하고, SIFT·Inlier Ratio 기준값 조합을 시험하여 오류가 적은 Rule 후보를 찾습니다.                     |
| `36_day05_freeze_rule.py`         | 복합 Rule 확정·동결          | Calibration에서 선택한 판정 기준을 JSON 파일로 저장하고, 이후 Test에서 동일한 기준을 사용하도록 고정합니다.                                         |
| `37_day05_test.py`                | 새로운 이미지 OK / NG 검사     | 확정된 Rule을 처음 보는 Test 이미지 6장에 적용하여 OK / NG를 판정하고, 실제 정답 및 판정 이유를 CSV와 결과 이미지로 저장합니다.                            |
| `38_day05_evaluate.py`            | 성능 평가·실패 분석            | Test 결과에서 TP·TN·FP·FN과 Accuracy·Precision·Recall을 계산하고, 잘못 판정한 이미지를 별도 폴더에 모읍니다.                               |
| `39_day05_mini_challenge.py`      | 나만의 검사 Rule 만들기        | 다른 제품의 로고를 사용하여 Calibration → Threshold 결정 → Rule 확정 → Test → 실패 분석 과정을 학생 스스로 수행합니다.                          |
![[Pasted image 20261028160132.png]]

---

# 6. 5일차 데이터는 새 폴더에 분리합니다

4일차 파일을 덮어쓰지 않습니다.

다음 구조를 사용합니다.

```text
subject9_machinevision/
│
├── samples/
│   ├── day02/
│   ├── day03/
│   ├── day04/
│   │
│   └── day05/
│       ├── reference/
│       │   ├── reference_label.jpg
│       │   └── expected_normal.jpg
│       │
│       ├── resized/
│       │   ├── ok_01.jpg ~ ok_06.jpg
│       │   ├── ng_01.jpg ~ ng_06.jpg
│       │   ├── test_ok_01.jpg ~ test_ok_03.jpg
│       │   └── test_ng_01.jpg ~ test_ng_03.jpg
│       │
│       └── mini_challenge/
│           ├── reference/
│           ├── calibration/
│           │   ├── ok/
│           │   └── ng/
│           └── test/
│               ├── ok/
│               └── ng/
│
├── outputs/
│   └── day05/
│       ├── calibration/
│       ├── test/
│       ├── fp/
│       └── fn/
│
├── configs/
│   └── day05_logo_rules.json
│
├── src/
│   ├── ...
│   ├── 32_day04_challenge.py
│   ├── day05_logo_features.py
│   ├── 33_day05_check_features.py
│   ├── 34_day05_measure_calibration.py
│   ├── 35_day05_analyze_calibration.py
│   ├── 36_day05_freeze_rule.py
│   ├── 37_day05_test.py
│   ├── 38_day05_evaluate.py
│   └── 39_day05_mini_challenge.py
│
└── reports/
    ├── day05_calibration_measurements.csv
    ├── day05_rule_candidates.csv
    ├── day05_test_results.csv
    ├── day05_test_metrics.md
    └── day05_mini_challenge.md
```

4일차 마지막 코드가 `32_day04_challenge.py`였으므로 5일차 실행 파일은 `33`부터 이어집니다.

공통 Feature 함수는 여러 실행 파일에서 재사용할 것이므로 숫자를 붙이지 않고:

```text
src/day05_logo_features.py
```

로 둡니다.

---
# PART1 실습 환경 + 데이터 준비 (7~9)

---

# 7. Day05 폴더를 만듭니다

프로젝트 폴더로 이동합니다.

```bash
cd ~/ai_vision/subject9_machinevision
```

가상환경을 활성화합니다.

```bash
source .venv/bin/activate
```

폴더를 만듭니다.

```bash
mkdir -p samples/day05/reference
mkdir -p samples/day05/resized

mkdir -p samples/day05/mini_challenge/reference
mkdir -p samples/day05/mini_challenge/calibration/ok
mkdir -p samples/day05/mini_challenge/calibration/ng
mkdir -p samples/day05/mini_challenge/test/ok
mkdir -p samples/day05/mini_challenge/test/ng

mkdir -p outputs/day05/calibration
mkdir -p outputs/day05/test
mkdir -p outputs/day05/fp
mkdir -p outputs/day05/fn

mkdir -p configs
mkdir -p reports
```

---

# 8. 4일차 Reference를 Day05에 복사하여 고정합니다

4일차 파일을 직접 수정하지 않도록 복사합니다.

```bash
cp samples/day04/reference/reference_label.jpg \
   samples/day05/reference/reference_label.jpg

cp samples/day04/targets/target_normal.jpg \
   samples/day05/reference/expected_normal.jpg
```

확인합니다.

```bash
ls -lh samples/day05/reference
```

다음 두 파일이 있으면 됩니다.

```text
reference_label.jpg
expected_normal.jpg
```

---
# 9. 5일차 Calibration과 Test 데이터를 확인합니다

5일차 실습을 위해 광천김 이미지를 총 **18장** 준비했습니다.

모든 이미지는 동일하게 다음 해상도를 사용합니다.

```
1920 × 1080
```

데이터는 역할에 따라 다음과 같이 나누어 사용합니다.

```
Calibration
├── OK 6장
└── NG 6장

Test
├── OK 3장
└── NG 3장

총 18장
```

현재 준비된 파일은 다음과 같습니다.

```
ok_01.jpg
ok_02.jpg
ok_03.jpg
ok_04.jpg
ok_05.jpg
ok_06.jpg

ng_01.jpg
ng_02.jpg
ng_03.jpg
ng_04.jpg
ng_05.jpg
ng_06.jpg

test_ok_01.jpg
test_ok_02.jpg
test_ok_03.jpg

test_ng_01.jpg
test_ng_02.jpg
test_ng_03.jpg
```

---

## 9.1 Calibration 데이터는 기준을 만드는 데 사용합니다

먼저 다음 12장을 `Calibration` 데이터로 사용합니다.

![[Pasted image 20261028160553.png]]

```
OK
ok_01.jpg
ok_02.jpg
ok_03.jpg
ok_04.jpg
ok_05.jpg
ok_06.jpg

NG
ng_01.jpg
ng_02.jpg
ng_03.jpg
ng_04.jpg
ng_05.jpg
ng_06.jpg
```

`OK` 이미지는 광천김 로고가 정상적으로 보이는 사진입니다.

```
제품 위치가 조금 다름
촬영 각도가 조금 다름
촬영 거리가 조금 다름

하지만

KC + (주)광천김 + 영문 로고
→ 정상적으로 확인됨
```

`NG` 이미지는 같은 검사 대상에서 로고가 정상적으로 확인되지 않도록 준비한 사진입니다.

```
로고 일부 가림
로고의 다른 부분 가림
가려진 범위 증가
        ↓
Reference와 정상적인 Matching이
어려워지도록 만든 이미지
```

이 12장의 측정값을 비교하여 **어느 정도의 값을 OK / NG 기준으로 사용할 것인지 결정**합니다.

---

## 9.2 Test 데이터는 정해진 기준을 확인하는 데 사용합니다

다음 6장은 Calibration에 사용하지 않고 따로 보관합니다.

![[Pasted image 20261028160704.png]]

```
OK
test_ok_01.jpg
test_ok_02.jpg
test_ok_03.jpg

NG
test_ng_01.jpg
test_ng_02.jpg
test_ng_03.jpg
```

사용 순서는 다음과 같습니다.

```
Calibration 12장
        ↓
측정값 비교
        ↓
OK / NG Rule 결정
        ↓
Rule 동결
        ↓
Test 6장
        ↓
처음 보는 이미지에서도
판정이 잘 되는지 확인
```

> Test 이미지를 보고 기준값을 다시 정하는 것이 아니라, Calibration에서 정한 기준이 새로운 이미지에서도 동작하는지를 확인합니다.

---
# PART2 무엇을 측정할지 이해 + 공통 함수 (10~15)

---

# 10. 데이터를 준비했으니 이제 무엇을 할까요?

앞의 9번 실습에서 광천김 이미지 18장을 `samples/day05/resized/`에 준비했습니다.

이 가운데 **Calibration 12장(OK 6장, NG 6장)**은 검사 기준을 만드는 데 사용하고, **Test 6장(OK 3장, NG 3장)**은 기준을 확정한 뒤에 사용합니다.

이제 해야 할 일은 **광천김 로고를 비교해 숫자로 측정하는 Python 코드를 작성하는 것**입니다. 그 숫자가 모이면 정상과 불량을 구별할 기준을 찾을 수 있습니다.

## 10.1 이번 PART2에서는 어디까지 하나요?

이번 PART2(10~15번)에서는 먼저 **공통 측정 함수를 만들고, 정상 이미지 한 장으로 동작을 확인**합니다.

Calibration 12장 전체를 측정하고 판정 기준을 찾는 작업은 다음 PART3에서 진행합니다.

## 10.2 앞으로 어떤 Python 파일을 사용하나요?

|파일|언제 사용하나요?|하는 일|
|---|---|---|
|`day05_logo_features.py`|PART2|이미지에서 로고 관련 측정값을 계산하는 **공통 함수**를 정의합니다.|
|`33_day05_check_features.py`|PART2|정상 이미지 `ok_01.jpg` 한 장으로 공통 함수가 작동하는지 확인합니다.|
|`34_day05_measure_calibration.py`|PART3|공통 함수를 이용해 Calibration 12장을 측정하고 CSV로 저장합니다.|
|`35_day05_analyze_calibration.py`|PART3|CSV의 OK/NG 측정값을 비교해 Threshold 후보를 찾습니다.|

첫 번째 파일은 다른 프로그램에서 **불러 사용하는 함수 모듈**입니다. 두 번째 파일부터는 그 함수를 호출하여 실제 작업을 실행합니다.

## 10.3 기억할 데이터 사용 순서

**지금은 측정 프로그램을 준비하는 단계**입니다.

이후 Calibration 12장으로 기준 후보를 만들고, `36_day05_freeze_rule.py`에서 기준을 확정한 다음에야 Test 6장으로 성능을 확인합니다.

Test 이미지는 기준을 고르는 데 사용하지 않습니다.

---

# 11. 어떤 값을 측정할까요?

4일차에서 배운 Template Matching·SIFT·RANSAC·Homography를 이용하면 이미지 한 장에서 다음 정보를 얻을 수 있습니다.

|측정값|초보자를 위한 의미|
|---|---|
|**Template Score**|검사 이미지에서 기준 로고와 **모양이 얼마나 비슷한 영역을 찾았는지** 나타내는 점수|
|**SIFT Good Match**|두 이미지 사이에서 **비슷하다고 선택된 특징점 연결 개수**|
|**Homography Inlier**|연결된 특징점 중 **위치 관계까지 일관된 연결 개수**|
|**Inlier Ratio**|Good Match 중 Inlier가 차지하는 비율 (`Inlier ÷ Good Match`)|
|**Homography Found**|Homography 계산에 성공했는지 여부 (`1`: 성공, `0`: 실패)|

예를 들어 Good Match가 100개이고 Inlier가 80개라면 **Inlier Ratio는 0.80**입니다.

이 숫자는 로고의 **유사도·특징점 연결·위치 관계**를 표현하는 측정 결과입니다.

아직 어떤 값부터 OK인지 정하지 않았으므로, 측정값이 높거나 Homography Found가 `1`이라고 해서 바로 OK로 판정하지 않습니다.

---

# 12. 왜 4일차 코드를 공통 함수로 정리하나요?

4일차에는 `27_template_matching.py`, `29_sift_matching.py`, `30_homography.py`처럼 기술별 프로그램을 따로 작성했습니다.

각 기술을 배우기에는 좋았지만, 5일차에서 이미지마다 그 코드를 다시 작성하면 같은 내용이 반복됩니다.

그래서 **한 장의 이미지를 전달하면 필요한 측정값을 한 번에 돌려주는 함수**로 정리합니다.

이 함수들을 보관할 파일이 다음 공통 모듈입니다.

```
src/day05_logo_features.py
```

5일차 공통 모듈에는 **Template Matching + SIFT + RANSAC·Homography** 측정을 넣습니다.

4일차에 학습했던 ORB는 이번 공통 모듈의 필수 측정 항목에 포함되지 않습니다.

공통 함수를 만들면 나중에 검사할 이미지 수가 늘어나더라도 **함수 코드를 복사하지 않고 이미지 경로만 바꾸어 호출**할 수 있습니다.

---

# 13. 공통 함수 파일 안에는 어떤 기능을 만들까요?

이번 파일은 다음 **세 가지 함수**로 구성합니다.

|함수|역할|
|---|---|
|`read_image()`|전달받은 이미지 경로에서 사진을 읽습니다.|
|`prepare_reference()`|기준 로고를 읽고 SIFT 특징점 정보를 **한 번 준비**합니다.|
|`measure_target()`|검사 이미지 한 장을 기준 로고와 비교하고 측정값을 반환합니다.|

함수들의 연결을 보면 다음과 같습니다.

```
기준 로고(reference_label.jpg)
      ↓ prepare_reference() : 한 번 준비
기준 로고의 특징점 정보(reference_data)
      │
      ├── 검사 이미지(ok_01.jpg)
      │         ↓ measure_target()
      │       측정값 반환
      │
      └── 이후 다른 검사 이미지도 같은 함수 호출
```

여기서 `measure_target()`이 반환하는 것은 **이미지 한 장의 측정값**입니다.

Calibration 12장을 반복 실행하고 CSV로 저장하는 작업은 나중에 작성할 `34_day05_measure_calibration.py`가 담당합니다.

---

# 14. `day05_logo_features.py` — 로고 측정 공통 함수를 만듭니다

이제 앞에서 알아본 세 함수를 실제 Python 코드로 작성합니다.

프로젝트의 `src` 폴더에 다음 파일을 만듭니다.

```
src/day05_logo_features.py
```

**현재 파일은 측정만 담당합니다.**

OK/NG 판정 기준(Threshold), 복합 Rule, JSON 저장, FP/FN 평가는 아직 구현하지 않습니다. 이 기능들은 Calibration 분석 결과를 확인한 뒤 다른 실습에서 다룹니다.

아래 코드를 작성합니다.

```python
from pathlib import Path

import cv2
import numpy as np


# --------------------------------------------------
# 1. 이미지 파일을 읽는 공통 함수
#
# 무엇을 하나요?
# - 전달받은 이미지 경로를 Path 객체로 변환합니다.
# - OpenCV로 이미지를 읽습니다.
# - 이미지가 없거나 읽을 수 없으면 오류를 발생시킵니다.
# - 정상적으로 읽었다면 이미지를 반환합니다.
#
# 왜 필요한가요?
# Reference와 Target을 읽는 코드를
# 여러 곳에서 반복하지 않기 위해서입니다.
#
# 입력: 이미지 파일 경로
# 출력: OpenCV 이미지(BGR)
# --------------------------------------------------

def read_image(path):

    path = Path(path)

    image = cv2.imread(
        str(path)
    )

    if image is None:
        raise FileNotFoundError(
            f"이미지를 읽지 못했습니다: {path}"
        )

    return image


# --------------------------------------------------
# 2. 기준 이미지(Reference)를 읽고 흑백으로 변환
#
# 무엇을 하나요?
# - 1번에서 만든 read_image()를 호출합니다.
# - 광천김 기준 로고 이미지를 읽습니다.
# - SIFT 특징점을 검출하기 위해 Grayscale로 변환합니다.
#
# 왜 필요한가요?
# Reference는 앞으로 검사할 모든 Target에서
# 동일하게 사용하는 기준 로고이기 때문입니다.
#
# 입력: Reference 이미지 경로
# --------------------------------------------------

def prepare_reference(reference_path):

    reference = read_image(
        reference_path
    )

    reference_gray = cv2.cvtColor(
        reference,
        cv2.COLOR_BGR2GRAY
    )


    # --------------------------------------------------
    # 3. 현재 OpenCV에서 SIFT 사용 가능 여부 확인
    #
    # 무엇을 하나요?
    # - OpenCV에 SIFT_create가 있는지 확인합니다.
    # - SIFT 기능이 없으면 오류를 발생시킵니다.
    #
    # 왜 필요한가요?
    # 이후 Reference와 Target에서 SIFT 특징점을
    # 추출해야 하므로 실행 가능 여부를 먼저 확인합니다.
    # --------------------------------------------------

    if not hasattr(
        cv2,
        "SIFT_create"
    ):
        raise RuntimeError(
            "현재 OpenCV에서 SIFT를 사용할 수 없습니다."
        )


    # --------------------------------------------------
    # 4. SIFT 생성 및 Reference 특징점 추출
    #
    # 무엇을 하나요?
    # - SIFT 특징점 검출기를 생성합니다.
    # - 기준 로고에서 Keypoint를 찾습니다.
    # - 각 Keypoint의 Descriptor를 생성합니다.
    #
    # Keypoint:
    # 이미지에서 특징적인 위치
    #
    # Descriptor:
    # 특징점 주변의 정보를 표현한 숫자 데이터
    #
    # nfeatures=1500:
    # SIFT에서 유지할 주요 특징점 수의
    # 목표 상한을 지정합니다.
    #
    # 특징점이 4개 미만이거나 Descriptor가 없으면
    # Homography 계산이 어려우므로 중단합니다.
    # --------------------------------------------------

    sift = cv2.SIFT_create(
        nfeatures=1500
    )


    ref_keypoints, ref_descriptors = (
        sift.detectAndCompute(
            reference_gray,
            None
        )
    )


    if (
        ref_descriptors is None
        or len(ref_keypoints) < 4
    ):
        raise RuntimeError(
            "Reference에서 충분한 SIFT 특징점을 찾지 못했습니다."
        )


    # --------------------------------------------------
    # 5. Reference 측정 정보를 딕셔너리로 반환
    #
    # 무엇을 하나요?
    # - Reference 원본 이미지와 흑백 이미지를 저장합니다.
    # - SIFT 객체를 저장합니다.
    # - Keypoint와 Descriptor를 저장합니다.
    # - Reference 이미지의 가로·세로 크기를 저장합니다.
    #
    # 왜 필요한가요?
    # 여러 Target을 검사할 때 Reference 특징점을
    # 매번 다시 계산하지 않고 재사용하기 위해서입니다.
    #
    # 반환값:
    # reference_data 딕셔너리
    # --------------------------------------------------

    return {
        "image": reference,
        "gray": reference_gray,
        "sift": sift,
        "keypoints": ref_keypoints,
        "descriptors": ref_descriptors,
        "width": reference.shape[1],
        "height": reference.shape[0],
    }


# --------------------------------------------------
# 6. Target 이미지 한 장을 읽고 흑백으로 변환
#
# 무엇을 하나요?
# - 검사할 Target 이미지 한 장을 입력받습니다.
# - read_image() 함수를 이용해 이미지를 읽습니다.
# - Grayscale로 변환합니다.
#
# 왜 필요한가요?
# Template Matching과 SIFT에 사용할
# 검사 이미지를 준비하기 위해서입니다.
#
# 입력:
# target_path   : 검사 이미지 경로
# reference_data: 5번에서 준비한 기준 정보
#
# 출력:
# 이미지 한 장의 여러 측정값
# --------------------------------------------------

def measure_target(
    target_path,
    reference_data
):

    target = read_image(
        target_path
    )

    target_gray = cv2.cvtColor(
        target,
        cv2.COLOR_BGR2GRAY
    )


    # --------------------------------------------------
    # 7. Reference에서 미리 계산한 정보 가져오기
    #
    # 무엇을 하나요?
    # - Reference의 흑백 이미지를 가져옵니다.
    # - Reference의 Keypoint와 Descriptor를 가져옵니다.
    # - 이미 생성한 SIFT 객체를 가져옵니다.
    #
    # 왜 필요한가요?
    # Target마다 Reference 특징점을 다시 계산하지 않고
    # 동일한 기준을 재사용하기 위해서입니다.
    # --------------------------------------------------

    reference_gray = (
        reference_data["gray"]
    )

    ref_keypoints = (
        reference_data["keypoints"]
    )

    ref_descriptors = (
        reference_data["descriptors"]
    )

    sift = (
        reference_data["sift"]
    )


    # --------------------------------------------------
    # 8. Template Matching으로 로고 유사도 측정
    #
    # 무엇을 하나요?
    # - Target 이미지에서 Reference와 비슷한 영역을 찾습니다.
    # - TM_CCOEFF_NORMED 방법으로 유사도를 계산합니다.
    # - 가장 높은 Template Score와 그 위치를 가져옵니다.
    #
    # template_score:
    # 가장 유사한 영역의 정규화 상관계수 점수
    #
    # template_location:
    # 가장 높은 점수가 나온 위치의 왼쪽 위 좌표
    #
    # 주의:
    # 현재 코드는 Reference 크기를 바꾸지 않고
    # Target을 검색하는 기본 Template Matching입니다.
    # Reference는 Target보다 크지 않아야 합니다.
    #
    # 아직 OK / NG를 판정하지 않습니다.
    # --------------------------------------------------

    template_result = cv2.matchTemplate(
        target_gray,
        reference_gray,
        cv2.TM_CCOEFF_NORMED
    )


    (
        _,
        template_score,
        _,
        template_location
    ) = cv2.minMaxLoc(
        template_result
    )


    # --------------------------------------------------
    # 9. Target의 SIFT Keypoint와 Descriptor 추출
    #
    # 무엇을 하나요?
    # - Target 이미지에서 SIFT 특징점을 찾습니다.
    # - 각 특징점의 Descriptor를 생성합니다.
    #
    # 왜 필요한가요?
    # Reference와 Target의 특징점을 비교하여
    # 같은 로고가 존재하는지 확인하기 위해서입니다.
    #
    # good_matches:
    # Ratio Test를 통과한 특징점 대응을 저장할 리스트
    # --------------------------------------------------

    target_keypoints, target_descriptors = (
        sift.detectAndCompute(
            target_gray,
            None
        )
    )


    good_matches = []


    # --------------------------------------------------
    # 10. BFMatcher로 Reference와 Target 특징점 비교
    #
    # 무엇을 하나요?
    # - Target Descriptor가 있는지 확인합니다.
    # - BFMatcher를 생성합니다.
    # - L2 Distance로 두 이미지의 Descriptor를 비교합니다.
    # - 가장 가까운 후보 2개를 찾습니다.
    #
    # k=2:
    # 첫 번째로 가까운 후보와
    # 두 번째로 가까운 후보를 찾는 설정입니다.
    #
    # 왜 필요한가요?
    # 다음 Ratio Test에서 두 후보의 거리를 비교하여
    # 모호한 Match를 제거하기 위해서입니다.
    # --------------------------------------------------

    if target_descriptors is not None:

        matcher = cv2.BFMatcher(
            cv2.NORM_L2
        )


        knn_matches = matcher.knnMatch(
            ref_descriptors,
            target_descriptors,
            k=2
        )


        # --------------------------------------------------
        # 11. Ratio Test로 Good Match 선별
        #
        # 무엇을 하나요?
        # - 가장 가까운 후보와 두 번째 후보를 비교합니다.
        # - 첫 번째 후보가 충분히 가까울 때만 남깁니다.
        #
        # 조건:
        # 첫 번째 거리 < 두 번째 거리 × 0.75
        #
        # 조건을 통과한 대응점을 Good Match라고 합니다.
        #
        # 왜 필요한가요?
        # 여러 위치에서 비슷하게 보이는 특징점의
        # 잘못된 대응 가능성을 줄이기 위해서입니다.
        # --------------------------------------------------

        for pair in knn_matches:

            if len(pair) < 2:
                continue


            m, n = pair


            if (
                m.distance
                < 0.75 * n.distance
            ):

                good_matches.append(
                    m
                )


    # --------------------------------------------------
    # 12. Homography 측정값 초기화
    #
    # 무엇을 하나요?
    # - Homography 계산 결과를 저장할 변수를 준비합니다.
    #
    # homography_found:
    # Homography 계산 성공 여부 (0 또는 1)
    #
    # inlier_count:
    # RANSAC을 통과한 대응점 개수
    #
    # inlier_ratio:
    # Good Match 중 Inlier가 차지하는 비율
    #
    # polygon:
    # Target에서 검출한 로고 영역의 네 모서리 좌표
    #
    # 왜 필요한가요?
    # 특징점이 부족하여 Homography 계산에 실패해도
    # 기본 측정값을 반환할 수 있도록 하기 위해서입니다.
    # --------------------------------------------------

    homography_found = 0

    inlier_count = 0

    inlier_ratio = 0.0

    polygon = None


    # --------------------------------------------------
    # 13. Homography 계산에 필요한 대응점 좌표 준비
    #
    # 무엇을 하나요?
    # - Good Match가 최소 4개인지 확인합니다.
    # - Reference의 특징점 좌표를 추출합니다.
    # - 그에 대응하는 Target 특징점 좌표를 추출합니다.
    #
    # queryIdx:
    # Reference 특징점의 인덱스
    #
    # trainIdx:
    # Target 특징점의 인덱스
    #
    # 왜 필요한가요?
    # Homography를 계산하려면 두 이미지에서
    # 서로 대응되는 점의 좌표가 필요하기 때문입니다.
    #
    # 주의:
    # 대응점이 4개 이상이어도 위치 관계가 부적절하면
    # Homography 계산에 실패할 수 있습니다.
    # --------------------------------------------------

    if len(good_matches) >= 4:

        source_points = np.float32(
            [
                ref_keypoints[
                    match.queryIdx
                ].pt
                for match in good_matches
            ]
        ).reshape(
            -1,
            1,
            2
        )


        target_points = np.float32(
            [
                target_keypoints[
                    match.trainIdx
                ].pt
                for match in good_matches
            ]
        ).reshape(
            -1,
            1,
            2
        )


        # --------------------------------------------------
        # 14. RANSAC을 이용하여 Homography 계산
        #
        # 무엇을 하나요?
        # - 두 이미지의 대응점으로 Homography를 계산합니다.
        # - RANSAC을 이용해 잘못된 대응점의 영향을 줄입니다.
        # - Homography 행렬과 Inlier Mask를 반환받습니다.
        #
        # Homography:
        # 한 평면의 위치가 다른 이미지에서
        # 어떻게 변했는지 설명하는 변환 행렬입니다.
        #
        # RANSAC:
        # 전체 대응점 중에서 기하학적으로
        # 일관된 대응점을 찾아내는 알고리즘입니다.
        #
        # 5.0:
        # RANSAC의 재투영 오차 허용 기준(픽셀)입니다.
        #
        # Homography가 계산되면
        # homography_found를 1로 설정합니다.
        # --------------------------------------------------

        homography, mask = (
            cv2.findHomography(
                source_points,
                target_points,
                cv2.RANSAC,
                5.0
            )
        )


        if (
            homography is not None
            and mask is not None
        ):

            homography_found = 1


            # --------------------------------------------------
            # 15. Inlier 개수와 Inlier Ratio 계산
            #
            # 무엇을 하나요?
            # - RANSAC이 선택한 Inlier 개수를 계산합니다.
            # - Good Match 전체에서 Inlier 비율을 계산합니다.
            #
            # Inlier Count:
            # Homography 관계에 잘 맞는 대응점 개수
            #
            # Inlier Ratio:
            # Inlier Count / Good Match Count
            #
            # 예:
            # Good Match = 100개
            # Inlier = 90개
            #
            # Inlier Ratio = 90 / 100 = 0.90
            #
            # 즉 Good Match의 90%가
            # 계산된 Homography 관계를 따른다는 뜻입니다.
            # --------------------------------------------------

            inlier_count = int(
                mask.ravel().sum()
            )


            inlier_ratio = (
                inlier_count
                / len(good_matches)
            )


            # --------------------------------------------------
            # 16. Reference 로고의 네 모서리 좌표 준비
            #
            # 무엇을 하나요?
            # - Reference의 가로·세로 크기를 가져옵니다.
            # - 기준 로고의 네 모서리 좌표를 만듭니다.
            #
            # 네 모서리:
            # ① 왼쪽 위
            # ② 오른쪽 위
            # ③ 오른쪽 아래
            # ④ 왼쪽 아래
            #
            # 왜 필요한가요?
            # 이 네 점에 Homography를 적용하면
            # Target에서 로고가 위치하는 영역을
            # 계산할 수 있기 때문입니다.
            # --------------------------------------------------

            ref_width = (
                reference_data["width"]
            )

            ref_height = (
                reference_data["height"]
            )


            corners = np.float32(
                [
                    [0, 0],

                    [
                        ref_width - 1,
                        0
                    ],

                    [
                        ref_width - 1,
                        ref_height - 1
                    ],

                    [
                        0,
                        ref_height - 1
                    ],
                ]
            ).reshape(
                -1,
                1,
                2
            )


            # --------------------------------------------------
            # 17. Reference 모서리를 Target 위치로 변환
            #
            # 무엇을 하나요?
            # - Homography를 이용해 네 모서리 좌표를 변환합니다.
            # - 변환 결과가 유한한 숫자인지 확인합니다.
            # - 정상이라면 polygon에 네 점을 저장합니다.
            #
            # cv2.perspectiveTransform():
            # Homography를 이용하여 좌표를 변환하는 함수
            #
            # np.isfinite():
            # 결과에 NaN이나 무한대가 있는지 확인하는 함수
            #
            # polygon:
            # 나중에 검사 이미지 위에 로고의 위치를
            # 사각형으로 표시할 때 사용할 좌표입니다.
            # --------------------------------------------------

            projected = (
                cv2.perspectiveTransform(
                    corners,
                    homography
                )
            )


            if np.isfinite(
                projected
            ).all():

                polygon = (
                    projected
                    .reshape(-1, 2)
                )


    # --------------------------------------------------
    # 18. 이미지 한 장의 전체 측정 결과 반환
    #
    # 무엇을 하나요?
    # - Template Matching 측정값을 반환합니다.
    # - SIFT Good Match 개수를 반환합니다.
    # - Homography 계산 성공 여부를 반환합니다.
    # - Inlier 개수와 비율을 반환합니다.
    # - 로고 영역 좌표와 원본 Target 이미지를 반환합니다.
    #
    # 왜 필요한가요?
    # 이후 Calibration과 Test에서 동일한 측정 함수를
    # 호출하여 검사값을 재사용하기 위해서입니다.
    #
    # 중요:
    # 이 함수는 측정만 수행합니다.
    # 아직 최종 OK / NG를 판정하지 않습니다.
    # --------------------------------------------------

    return {

        "target_path":
            str(target_path),

        "template_score":
            float(template_score),

        "template_x":
            int(
                template_location[0]
            ),

        "template_y":
            int(
                template_location[1]
            ),

        "sift_good_matches":
            int(
                len(good_matches)
            ),

        "homography_found":
            int(
                homography_found
            ),

        "homography_inliers":
            int(
                inlier_count
            ),

        "inlier_ratio":
            float(
                inlier_ratio
            ),

        "polygon":
            polygon,

        "target_image":
            target,
    }
```

### 의사코드

```
[1. 이미지 파일을 읽는 공통 함수]

read_image() 함수를 만든다.

이미지 경로를 전달받는다.
Path 객체로 변환한다.
OpenCV로 이미지를 읽는다.

이미지를 읽지 못하면 오류를 발생시킨다.

이미지를 정상적으로 읽으면 반환한다.

          ↓

[2. 기준 이미지(Reference)를 읽고 흑백으로 변환]

prepare_reference() 함수를 만든다.

광천김 기준 로고 이미지 경로를 전달받는다.
read_image()를 호출한다.

Reference 이미지를 읽는다.
Grayscale로 변환한다.

          ↓

[3. 현재 OpenCV에서 SIFT 사용 가능 여부 확인]

OpenCV에 SIFT_create 기능이 있는지 확인한다.

사용할 수 없다면 오류를 발생시킨다.
사용할 수 있다면 다음 단계로 진행한다.

          ↓

[4. SIFT 생성 및 Reference 특징점 추출]

SIFT 객체를 생성한다.
nfeatures를 1500으로 설정한다.

Reference에서 Keypoint를 찾는다.
각 Keypoint의 Descriptor를 생성한다.

Descriptor가 없거나
Keypoint가 4개 미만이면 실행을 중단한다.

          ↓

[5. Reference 측정 정보를 딕셔너리로 반환]

Reference 원본 이미지를 저장한다.
Grayscale 이미지를 저장한다.

SIFT 객체를 저장한다.
Keypoint와 Descriptor를 저장한다.

Reference의 가로·세로 크기를 저장한다.

이 정보를 reference_data로 반환한다.

          ↓

[6. Target 이미지 한 장을 읽고 흑백으로 변환]

measure_target() 함수를 만든다.

검사할 Target 이미지 경로를 전달받는다.
Reference 정보를 함께 전달받는다.

Target 이미지를 읽는다.
Grayscale로 변환한다.

          ↓

[7. Reference에서 미리 계산한 정보 가져오기]

reference_data에서 다음 정보를 가져온다.

Reference Grayscale
Reference Keypoint
Reference Descriptor
SIFT 객체

Target과 비교할 준비를 한다.

          ↓

[8. Template Matching으로 로고 유사도 측정]

Target 이미지에서 Reference와
비슷한 영역을 검색한다.

TM_CCOEFF_NORMED 방식으로 비교한다.

Template Score를 계산한다.
점수가 가장 높은 위치를 찾는다.

Template Score와 위치를 저장한다.

          ↓

[9. Target의 SIFT Keypoint와 Descriptor 추출]

Target에서 SIFT Keypoint를 찾는다.
각 Keypoint의 Descriptor를 생성한다.

Good Match를 저장할 빈 리스트를 준비한다.

          ↓

[10. BFMatcher로 Reference와 Target 특징점 비교]

Target Descriptor가 있는지 확인한다.

Descriptor가 없다면 Matching을 생략한다.

Descriptor가 있다면 BFMatcher를 준비한다.
비교 방법은 L2 Distance로 설정한다.

Reference 특징점마다
가장 가까운 Target 후보 2개를 찾는다.

          ↓

[11. Ratio Test로 Good Match 선별]

각 Match 후보를 하나씩 확인한다.

후보가 2개 미만이면 건너뛴다.

가장 가까운 후보와
두 번째 후보의 거리를 비교한다.

첫 번째 거리 < 두 번째 거리 × 0.75

조건을 만족하면 Good Match에 추가한다.

          ↓

[12. Homography 측정값 초기화]

Homography Found를 0으로 설정한다.
Inlier Count를 0으로 설정한다.
Inlier Ratio를 0.0으로 설정한다.
Polygon을 None으로 설정한다.

          ↓

[13. Homography 계산에 필요한 대응점 좌표 준비]

Good Match가 4개 이상인지 확인한다.

4개 미만이면
Homography 계산을 생략한다.

4개 이상이면:

Reference의 Good Match 좌표를 추출한다.
Target의 대응되는 Match 좌표를 추출한다.

두 이미지의 대응점 배열을 준비한다.

          ↓

[14. RANSAC을 이용하여 Homography 계산]

Reference와 Target의 대응점을 입력한다.

RANSAC으로 Homography를 계산한다.
재투영 오차 허용 기준은 5.0픽셀로 설정한다.

Homography 행렬과 Inlier Mask를 얻는다.

계산에 실패하면
Homography Found는 0을 유지한다.

계산에 성공하면
Homography Found를 1로 설정한다.

          ↓

[15. Inlier 개수와 Inlier Ratio 계산]

RANSAC의 Inlier Mask를 확인한다.

Inlier로 인정된 대응점 개수를 센다.

Inlier Ratio =
Inlier Count / Good Match Count

를 계산한다.

          ↓

[16. Reference 로고의 네 모서리 좌표 준비]

Reference 이미지의 가로 크기를 가져온다.
Reference 이미지의 세로 크기를 가져온다.

왼쪽 위 좌표를 만든다.
오른쪽 위 좌표를 만든다.
오른쪽 아래 좌표를 만든다.
왼쪽 아래 좌표를 만든다.

네 모서리 좌표를 배열로 저장한다.

          ↓

[17. Reference 모서리를 Target 위치로 변환]

Homography를 사용하여
Reference의 네 모서리를 Target 좌표로 변환한다.

변환 결과가 유한한 숫자인지 확인한다.

모든 좌표가 유효하면
Polygon에 네 모서리 좌표를 저장한다.

          ↓

[18. 이미지 한 장의 전체 측정 결과 반환]

Target 이미지 경로를 반환한다.

Template Score를 반환한다.
Template Matching 위치를 반환한다.

SIFT Good Match 개수를 반환한다.

Homography Found를 반환한다.
Homography Inlier 개수를 반환한다.
Inlier Ratio를 반환한다.

Polygon 좌표를 반환한다.
Target 원본 이미지를 반환한다.

          ↓

[최종 결과]

Target 이미지 한 장
        +
Reference 정보
        ↓
Template Matching
        ↓
SIFT Keypoint / Descriptor
        ↓
BFMatcher
        ↓
Ratio Test
        ↓
Good Match
        ↓
RANSAC + Homography
        ↓
Inlier Count / Inlier Ratio
        ↓
측정 결과 딕셔너리 반환

          ↓

이후 Calibration과 Test에서
동일한 공통 측정 함수를 재사용한다.
```

---

## 14.1 이 공통 함수는 무엇을 하나요?

코드가 길어 보이지만 역할은 크게 세 부분입니다.

### `read_image()`

이미지를 읽습니다.

```
이미지 경로
        ↓
OpenCV로 이미지 읽기
        ↓
이미지 반환
```

---

### `prepare_reference()`

4일차에서 만든 기준 로고를 준비합니다.

사용하는 파일은 다음입니다.

```
samples/day04/reference/reference_label.jpg
```

처리 과정은:

```
reference_label.jpg
        ↓
Gray
        ↓
SIFT
        ↓
Keypoint
        ↓
Descriptor
```

입니다.

기준 로고는 12장의 Calibration 이미지에서 계속 똑같이 사용합니다.

따라서 이미지마다 다시 만들 필요 없이 한 번만 계산해서 재사용합니다.

---

### `measure_target()`

이 함수가 실제 측정을 담당합니다.

예를 들어:

```
samples/day05/resized/ok_01.jpg
```

을 넣으면:

```
reference_label.jpg
        +
ok_01.jpg
        ↓
Template Matching
        ↓
SIFT Matching
        ↓
RANSAC
        ↓
Homography
```

를 실행한 뒤 다음 값을 반환합니다.

```
template_score

sift_good_matches

homography_found

homography_inliers

inlier_ratio
```

즉 앞으로는 긴 코드를 다시 작성하지 않고:

```python
measurement = measure_target(
    image_path,
    reference_data
)
```

처럼 호출하면 이미지 한 장의 검사값을 한 번에 측정할 수 있습니다.

---

# 15. 공통 함수가 실제 이미지에서 동작하는지 먼저 확인합니다

공통 함수를 만들었다고 바로 Calibration 12장을 처리하지 않습니다.

먼저 이미지 한 장만 넣어 정상적으로 측정되는지 확인합니다.

이런 확인 작업을 흔히 간단한 Smoke Test라고 생각하면 됩니다.

```
공통 함수 작성
        ↓
이미지 1장으로 먼저 확인
        ↓
정상 동작
        ↓
Calibration 12장 전체 적용
```

확인용 파일을 만듭니다.

```
src/33_day05_check_features.py
```

다음 코드를 작성합니다.

```python
from pathlib import Path

# --------------------------------------------------
# 앞에서 작성한 공통 측정 함수 가져오기
#
# prepare_reference():
# - 기준 로고의 SIFT 특징점을 준비하는 함수
#
# measure_target():
# - 검사 이미지 한 장에서
#   Template, SIFT, Homography 측정값을 구하는 함수
#
# 두 함수는 앞에서 작성한
# day05_logo_features.py에 정의되어 있습니다.
# --------------------------------------------------

from day05_logo_features import (
    prepare_reference,
    measure_target,
)


# --------------------------------------------------
# 검사에 사용할 이미지 경로 설정
#
# REFERENCE_PATH:
# - 비교 기준인 광천김 로고 이미지
#
# TARGET_PATH:
# - 공통 측정 함수가 정상적으로 동작하는지
#   확인할 정상 이미지 한 장
#
# 이번에는 Calibration 12장을 모두 검사하지 않고
# ok_01.jpg 한 장만 먼저 측정합니다.
# --------------------------------------------------

REFERENCE_PATH = Path(
    "samples/day04/reference/reference_label.jpg"
)

TARGET_PATH = Path(
    "samples/day05/resized/ok_01.jpg"
)


# --------------------------------------------------
# 1. Reference 이미지의 특징점 준비
#
# 무엇을 하나요?
# - prepare_reference() 함수를 호출합니다.
# - 기준 로고 이미지를 읽습니다.
# - Grayscale로 변환합니다.
# - SIFT Keypoint와 Descriptor를 생성합니다.
# - 측정에 필요한 Reference 정보를 반환받습니다.
#
# 왜 필요한가요?
# 이후 Target 이미지와 비교할
# 기준 로고의 특징점 정보가 필요하기 때문입니다.
#
# reference_data:
# - Reference 원본 이미지
# - Grayscale 이미지
# - SIFT 객체
# - Keypoint
# - Descriptor
# - 이미지 가로·세로 크기
#
# Reference Keypoints:
# 기준 이미지에서 추출한 특징점 개수를 출력합니다.
# --------------------------------------------------

reference_data = prepare_reference(
    REFERENCE_PATH
)


print(
    "Reference Keypoints:",
    len(
        reference_data["keypoints"]
    )
)


# --------------------------------------------------
# 2. 실제 Target 이미지 한 장 측정
#
# 무엇을 하나요?
# - measure_target() 함수를 호출합니다.
# - 검사할 ok_01.jpg와 Reference 정보를 전달합니다.
#
# 함수 내부에서 수행하는 작업:
#
# ① Target 이미지를 읽습니다.
# ② Template Matching으로 유사도를 측정합니다.
# ③ SIFT Keypoint와 Descriptor를 추출합니다.
# ④ BFMatcher로 특징점을 비교합니다.
# ⑤ Ratio Test로 Good Match를 선별합니다.
# ⑥ RANSAC으로 Homography를 계산합니다.
# ⑦ Inlier Count와 Inlier Ratio를 계산합니다.
#
# 왜 필요한가요?
# 앞에서 작성한 공통 측정 함수가
# 실제 이미지에서도 정상적으로 실행되는지
# 확인하기 위해서입니다.
#
# measurement:
# 검사 이미지 한 장의 측정값이 저장된 딕셔너리
#
# 주의:
# 이 단계에서는 아직 OK / NG를 판정하지 않습니다.
# --------------------------------------------------

measurement = measure_target(
    TARGET_PATH,
    reference_data
)


# --------------------------------------------------
# 3. Target 이미지의 전체 측정 결과 확인
#
# 무엇을 하나요?
# - 검사한 Target 이미지 이름을 출력합니다.
# - Template Matching 점수를 출력합니다.
# - SIFT Good Match 개수를 출력합니다.
# - Homography 계산 성공 여부를 출력합니다.
# - Homography Inlier 개수를 출력합니다.
# - Inlier Ratio를 출력합니다.
#
# 왜 필요한가요?
# 이후 Calibration 12장을 검사하기 전에
# 공통 측정 함수가 정상적으로 값을 반환하는지
# 한 장의 이미지로 확인하기 위해서입니다.
#
# 측정값 설명:
#
# Template Score:
# 기준 로고와 가장 유사한 영역의 점수
#
# SIFT Good Match:
# Ratio Test를 통과한 특징점 대응 개수
#
# Homography Found:
# Homography 계산 성공 여부
# 1 = 계산 성공, 0 = 계산 실패
#
# Homography Inlier:
# RANSAC의 변환 관계에 잘 맞는 대응점 개수
#
# Inlier Ratio:
# Inlier Count / Good Match Count
#
# round(값, 4):
# 출력할 숫자를 소수점 넷째 자리까지 반올림합니다.
# --------------------------------------------------

print()
print("=" * 60)


# 검사한 Target 이미지 이름
print(
    "Target:",
    TARGET_PATH.name
)


# Template Matching의 최대 유사도
print(
    "Template Score:",
    round(
        measurement["template_score"],
        4
    )
)


# Ratio Test를 통과한 SIFT Good Match 개수
print(
    "SIFT Good Match:",
    measurement[
        "sift_good_matches"
    ]
)


# Homography 계산 성공 여부
print(
    "Homography Found:",
    measurement[
        "homography_found"
    ]
)


# RANSAC이 선택한 Inlier 개수
print(
    "Homography Inlier:",
    measurement[
        "homography_inliers"
    ]
)


# Good Match 중 Inlier가 차지하는 비율
print(
    "Inlier Ratio:",
    round(
        measurement["inlier_ratio"],
        4
    )
)


print("=" * 60)
```

실행합니다.

```
python src/33_day05_check_features.py
```

### 의사코드

```
[실습 준비 — 공통 함수와 이미지 경로 설정]

앞에서 작성한 day05_logo_features.py에서
두 함수를 가져온다.

prepare_reference()
measure_target()

광천김 Reference 이미지 경로를 정한다.

samples/day04/reference/reference_label.jpg

검사할 Target 이미지 경로를 정한다.

samples/day05/resized/ok_01.jpg

          ↓

[1. Reference 이미지의 특징점 준비]

prepare_reference() 함수를 호출한다.

광천김 기준 로고 이미지를 읽는다.

Reference를 Grayscale로 변환한다.

SIFT 객체를 생성한다.

Reference에서 Keypoint를 찾는다.

각 Keypoint의 Descriptor를 만든다.

Reference 이미지와 특징점 정보를
reference_data 딕셔너리에 저장한다.

Reference Keypoint 개수를 출력한다.

          ↓

[2. 실제 Target 이미지 한 장 측정]

measure_target() 함수를 호출한다.

Target 이미지 ok_01.jpg를 전달한다.

앞에서 준비한 reference_data도 전달한다.

          ↓

Target 이미지를 읽는다.

          ↓

Template Matching을 실행한다.

기준 로고와 비슷한 영역을 찾는다.

Template Score를 계산한다.

          ↓

Target에서 SIFT 특징점을 추출한다.

Keypoint와 Descriptor를 만든다.

          ↓

BFMatcher로 Reference와 Target의
Descriptor를 비교한다.

          ↓

Ratio Test를 적용한다.

비교적 확실한 Good Match만 남긴다.

          ↓

Good Match가 4개 이상이면
RANSAC과 Homography를 계산한다.

          ↓

RANSAC의 Inlier 개수를 센다.

Inlier Ratio를 계산한다.

          ↓

측정 결과를
measurement 딕셔너리로 반환받는다.

          ↓

[3. Target 이미지의 전체 측정 결과 확인]

measurement에 저장된 값을 읽는다.

검사한 이미지 이름을 출력한다.

Template Score를 출력한다.

SIFT Good Match 개수를 출력한다.

Homography 계산 성공 여부를 출력한다.

Homography Inlier 개수를 출력한다.

Inlier Ratio를 출력한다.

          ↓

[최종 결과]

광천김 Reference
        +
Target 정상 이미지 ok_01.jpg
        ↓
공통 측정 함수 실행
        ↓
Template Score
SIFT Good Match
Homography Found
Homography Inlier
Inlier Ratio
        ↓
터미널에 측정값 출력
        ↓
공통 측정 함수의 정상 동작 확인
        ↓
다음 실습에서 Calibration 12장에
동일한 측정 함수를 반복 적용
```

---

## 15.1 여기서는 무엇을 확인하나요?

아직 OK / NG 판정을 하는 것이 아닙니다.

확인할 것은:

```
reference_label.jpg를 정상적으로 읽었는가?

SIFT 특징점을 만들었는가?

ok_01.jpg를 정상적으로 읽었는가?

Template Score가 계산되는가?

SIFT Good Match가 계산되는가?

Homography가 계산되는가?

Inlier Ratio가 계산되는가?
```

입니다.

출력은 다음과 같은 형태가 됩니다.

```
Reference Keypoints: 675

============================================================
Target: ok_01.jpg
Template Score: 0.5358
SIFT Good Match: 174
Homography Found: 1
Homography Inlier: 167
Inlier Ratio: 0.9598
============================================================
```

숫자는 현재 촬영한 광천김 이미지에 따라 달라집니다.

---

## 15.2 첫 번째 실제 측정 결과를 읽어봅니다

아직 이 숫자로 `OK / NG`를 판정하지 않습니다.

지금은 각 숫자가 무엇을 의미하는지 확인합니다.

### Reference Keypoints = 675

```
Reference Keypoints: 675
```

기준 이미지인 `reference_label.jpg`에서 SIFT가 675개의 특징점 후보를 찾았다는 뜻입니다.

광천김 로고에는 글자와 모서리, 선과 무늬가 많기 때문에 비교에 사용할 특징점이 충분히 만들어졌습니다.

### Template Score = 0.5358

```
Template Score: 0.5358
```

Template Matching으로 기준 로고와 `ok_01.jpg`를 비교했을 때 얻은 유사도입니다.

```
Template Matching
→ 기준 로고 전체 모양을 그대로 비교

현재 측정값
→ 0.5358
```

`ok_01.jpg`는 정상 이미지이지만 Score가 반드시 `0.9`처럼 매우 높게 나오는 것은 아닙니다.

실제 촬영에서는 위치, 크기, 각도, 밝기 등의 작은 차이가 생길 수 있기 때문입니다.

따라서 지금은:

```
0.5358이면 OK
```

라고 판단하지 않습니다.

나머지 OK와 NG 이미지에서도 값을 측정한 뒤 비교해야 합니다.

---

### SIFT Good Match = 174

```
SIFT Good Match: 174
```

기준 로고와 `ok_01.jpg` 사이에서 SIFT가 찾은 특징점 중 서로 비슷하다고 판단하여 남긴 대응점이 174개라는 뜻입니다.

```
Reference 특징점
        ↓
Target 특징점과 비교
        ↓
Ratio Test
        ↓
174개의 Good Match
```

즉 기준 로고와 검사 이미지 사이에서 상당히 많은 특징점이 연결되었습니다.

---

### Homography Inlier = 167

```
Homography Inlier: 167
```

174개의 Good Match가 모두 정확한 연결이라는 보장은 없습니다.

그래서 RANSAC을 사용하여 서로 일관된 위치 관계를 갖는 Match만 다시 선택했습니다.

```
Good Match 174개
        ↓
RANSAC
        ↓
실제로 일관성 있게 맞는 점
167개
```

이 167개를 `Inlier`라고 합니다.

---

### Inlier Ratio = 0.9598

```
Inlier Ratio: 0.9598
```

Good Match 174개 중 167개가 Inlier로 남았습니다.

```
167 / 174
≈ 0.9598
≈ 95.98%
```

즉, SIFT가 찾은 대응점의 약 96%가 Homography에서도 일관된 대응점으로 인정된 것입니다.

현재 `ok_01.jpg`에서는 기준 로고와 검사 이미지 사이의 특징점 관계가 상당히 안정적으로 만들어졌다고 볼 수 있습니다.

---

## 15.3 `Homography Found = 1`은 무엇인가요?

```
Homography Found: 1
```

은 다음 과정이 성공했다는 뜻입니다.

```
reference_label.jpg
        +
ok_01.jpg
        ↓
SIFT 특징점 비교
        ↓
Good Match 확보
        ↓
RANSAC
        ↓
Homography 계산 성공
```

즉 프로그램이 기준 로고와 검사 이미지 사이의 위치 관계를 계산할 수 있었다는 의미입니다.

반대로:

```
Homography Found: 0
```

이면 충분한 대응점을 확보하지 못했거나 일관된 Homography를 계산하지 못했다는 뜻입니다.

다만 여기서도 주의합니다.

```
Homography Found = 1
→ 무조건 OK라는 뜻 X

Homography Found = 0
→ 무조건 NG라는 뜻 X
```

현재는 **측정 결과**일 뿐입니다.

---

## 15.4 이번 한 장에서 무엇을 확인했나요?

`ok_01.jpg` 한 장을 측정해 보니 다음과 같은 특징이 나타났습니다.

```
Template Score
→ 0.5358

SIFT Good Match
→ 174개

Homography Inlier
→ 167개

Inlier Ratio
→ 0.9598

Homography
→ 계산 성공
```

특히 눈여겨볼 부분은 다음입니다.

```
Template Score는 0.5358

하지만

SIFT 특징점은 많이 연결되었고
그중 약 96%가 RANSAC에서도
일관된 대응점으로 남음
```

즉 같은 정상 이미지를 보더라도 검사 방법에 따라 결과를 표현하는 숫자가 다릅니다.

그래서 한 장의 결과만 보고 기준을 정하지 않습니다.

다음 단계에서는 동일한 공통 측정 함수를:

```
OK 6장
+
NG 6장
```

에 모두 적용합니다.

그 결과를 비교하면서:

> Template Score, SIFT Good Match, Inlier Ratio 중 어떤 값이 실제로 OK와 NG를 잘 구분하는가?

를 확인합니다.

이것이 다음 Calibration 실습의 핵심입니다.


---

## 15.5 왜 이미지 한 장만 먼저 확인했나요?

12장을 한꺼번에 처리했는데 코드에 문제가 있다면 어느 부분에서 문제가 생겼는지 찾기 어렵습니다.

따라서 실제 개발에서도:

```
공통 함수 작성
        ↓
대표 이미지 1장으로 확인
        ↓
정상 동작 확인
        ↓
여러 데이터에 반복 적용
```

순서로 진행하는 것이 안전합니다.

---
# PART3 **Calibration** — 12장 측정 → 분포 비교 → Rule 후보 찾기 (16~22)

---

# 16. Calibration 12장의 여러 검사값을 한 번에 측정합니다

앞에서 `ok_01.jpg` 한 장을 이용하여 공통 측정 함수가 정상적으로 동작하는 것을 확인했습니다.

이제 같은 측정을 Calibration 데이터 전체에 적용합니다.

사용할 이미지는 다음 12장입니다.

```
samples/day05/resized/

OK
├── ok_01.jpg
├── ok_02.jpg
├── ok_03.jpg
├── ok_04.jpg
├── ok_05.jpg
└── ok_06.jpg

NG
├── ng_01.jpg
├── ng_02.jpg
├── ng_03.jpg
├── ng_04.jpg
├── ng_05.jpg
└── ng_06.jpg
```

`test_ok_01.jpg`, `test_ng_01.jpg` 등의 Test 이미지는 아직 사용하지 않습니다.

---

## 15.1 이번 실습에서는 무엇을 하나요?

모든 Calibration 이미지에 완전히 같은 검사 조건을 적용합니다.

```
같은 Reference
reference_label.jpg

        ↓
같은 Template Matching
        ↓
같은 SIFT 설정
        ↓
같은 Ratio Test
        ↓
같은 RANSAC 조건
        ↓
같은 Homography 계산
```

그리고 이미지마다 다음 값을 기록합니다.

```
Template Score

SIFT Good Match

Homography 계산 성공 여부

Homography Inlier 수

Inlier Ratio
```

예를 들어:

```
ok_01.jpg
→ Template Score
→ SIFT Good Match
→ Inlier
→ Inlier Ratio

ok_02.jpg
→ 같은 값 측정

...

ng_06.jpg
→ 같은 값 측정
```

이렇게 해야 나중에:

```
OK 6장에서는 어떤 값이 나오는가?

NG 6장에서는 어떤 값이 나오는가?

어떤 측정값이
OK와 NG를 가장 잘 구분하는가?
```

를 비교할 수 있습니다.

> 지금은 여러 방법을 함께 **측정**하는 단계입니다. 여러 조건을 묶어서 OK / NG를 판정하는 **복합 Rule은 아직 만들지 않습니다.**

---

## 15.2 왜 여러 값을 함께 측정하나요?

한 가지 측정값만 보고 검사 기준을 만들면 실제 촬영환경에서 불안정할 수 있습니다.

예를 들어 정상 이미지인데도:

```
Template Score
→ 생각보다 낮을 수 있음
```

앞에서 실제 `ok_01.jpg`에서도:

```
Template Score = 0.5358
```

이 나왔습니다.

하지만 같은 이미지에서:

```
SIFT Good Match = 174

Homography Inlier = 167

Inlier Ratio = 0.9598
```

로 특징점 대응은 상당히 안정적이었습니다.

따라서 지금부터는 한 값만 보는 것이 아니라:

```
Template은 어떻게 변하는가?

SIFT는 어떻게 변하는가?

Homography는 어떻게 변하는가?
```

를 같은 12장의 이미지에서 나란히 비교합니다.

---

# 17. `34_day05_measure_calibration.py` — Calibration 전체를 측정합니다

==`Calibration 12장 측정 : 이미지에서 숫자를 뽑아 CSV에 모으는 코드`==

먼저 12장을 측정합니다

```
Calibration 12장
OK 6장 + NG 6장
        ↓
34_day05_measure_calibration.py
        ↓
각 이미지에서 측정

Template Score
SIFT Good Match
Homography Inlier
Inlier Ratio
        ↓
CSV 저장
```

결과:

```
reports/day05_calibration_measurements.csv
```

아직 Rule을 찾는 코드가 아니고 검사값을 수집하는 코드를 작성합니다.

파일을 만듭니다.

```
src/34_day05_measure_calibration.py
```

다음 코드를 작성합니다.

```python
from pathlib import Path
import csv

# 앞에서 작성한 공통 측정 함수 가져오기
#
# prepare_reference():
# - 기준 로고의 SIFT 특징점을 준비합니다.
#
# measure_target():
# - 이미지 한 장에서 Template Matching,
#   SIFT, Homography 측정값을 계산합니다.

from day05_logo_features import (
    prepare_reference,
    measure_target,
)


# --------------------------------------------------
# 1. Reference, Calibration 이미지 및 CSV 경로 설정
#
# 무엇을 하나요?
# - 검사 기준인 광천김 Reference 경로를 지정합니다.
# - Calibration 이미지 12장이 있는 폴더를 지정합니다.
# - 측정값을 저장할 CSV 경로를 지정합니다.
#
# REFERENCE_PATH:
# 비교 기준으로 사용할 정상 로고 이미지
#
# DATA_DIR:
# OK 6장과 NG 6장이 저장된 폴더
#
# OUTPUT_CSV:
# 12장의 측정 결과를 저장할 CSV 파일
#
# 왜 필요한가요?
# 프로그램이 어떤 이미지를 읽고
# 결과를 어디에 저장해야 하는지 알아야 하기 때문입니다.
# --------------------------------------------------

REFERENCE_PATH = Path(
    "samples/day04/reference/reference_label.jpg"
)

DATA_DIR = Path(
    "samples/day05/resized"
)

OUTPUT_CSV = Path(
    "reports/day05_calibration_measurements.csv"
)


# --------------------------------------------------
# 2. Calibration 이미지 목록과 실제 상태(OK/NG) 준비
#
# 무엇을 하나요?
# - find_calibration_images() 함수를 정의합니다.
# - ok_로 시작하는 이미지들을 찾습니다.
# - ng_로 시작하는 이미지들을 찾습니다.
# - 각 이미지에 실제 정답인 OK 또는 NG를 연결합니다.
#
# 예:
# ok_01.jpg → OK
# ok_02.jpg → OK
# ng_01.jpg → NG
# ng_02.jpg → NG
#
# 왜 필요한가요?
# 나중에 프로그램이 측정한 값과
# 사람이 알고 있는 실제 정상/불량 상태를
# 비교하여 검사 기준을 만들기 위해서입니다.
#
# 주의:
# 지금은 파일명에 따라 실제 상태를 기록합니다.
# 프로그램이 OK/NG를 예측하는 단계는 아닙니다.
# --------------------------------------------------

def find_calibration_images():

    # 이미지 경로와 실제 정답을 저장할 리스트
    image_infos = []


    # --------------------------------------------------
    # 2-1. 정상(OK) 이미지 목록 만들기
    #
    # - ok_*.jpg 패턴의 이미지를 찾습니다.
    # - sorted()로 파일명 순서대로 정렬합니다.
    # - 이미지 경로와 "OK"를 함께 저장합니다.
    # --------------------------------------------------

    # OK 6장
    for image_path in sorted(
        DATA_DIR.glob("ok_*.jpg")
    ):

        image_infos.append(
            (
                image_path,
                "OK"
            )
        )


    # --------------------------------------------------
    # 2-2. 불량(NG) 이미지 목록 만들기
    #
    # - ng_*.jpg 패턴의 이미지를 찾습니다.
    # - sorted()로 파일명 순서대로 정렬합니다.
    # - 이미지 경로와 "NG"를 함께 저장합니다.
    # --------------------------------------------------

    # NG 6장
    for image_path in sorted(
        DATA_DIR.glob("ng_*.jpg")
    ):

        image_infos.append(
            (
                image_path,
                "NG"
            )
        )


    # 준비한 이미지 경로와 정답 목록 반환
    return image_infos


# --------------------------------------------------
# 3. 결과 폴더 생성 및 Reference 특징점 준비
#
# 무엇을 하나요?
# - main() 함수를 정의합니다.
# - 결과 CSV를 저장할 reports 폴더를 준비합니다.
# - prepare_reference() 함수를 호출합니다.
# - Reference의 SIFT 특징점을 추출합니다.
# - 기준 이미지의 특징점 개수를 출력합니다.
#
# 왜 필요한가요?
# Calibration 이미지 12장 모두 같은 Reference를
# 사용하므로 기준 특징점을 한 번만 계산하여
# 반복해서 재사용하기 위해서입니다.
#
# reference_data에는:
# - Reference 원본 이미지
# - Grayscale 이미지
# - SIFT 객체
# - Keypoint / Descriptor
# - 이미지 크기
# 등의 정보가 저장됩니다.
# --------------------------------------------------

def main():

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # 기준 로고 준비
    reference_data = prepare_reference(
        REFERENCE_PATH
    )


    # 기준 로고의 특징점 개수 출력
    print(
        "Reference Keypoints:",
        len(
            reference_data["keypoints"]
        )
    )


    # --------------------------------------------------
    # 4. Calibration 이미지 목록과 수량 확인
    #
    # 무엇을 하나요?
    # - 2번에서 만든 함수를 호출합니다.
    # - 이미지 경로와 실제 정답을 가져옵니다.
    # - Calibration 이미지의 전체 개수를 확인합니다.
    #
    # 이번 수업에서 예상하는 데이터:
    # OK 6장 + NG 6장 = 총 12장
    #
    # 왜 필요한가요?
    # 측정하기 전에 필요한 데이터가
    # 준비되어 있는지 확인하기 위해서입니다.
    #
    # 주의:
    # 현재 코드는 12장이 아니어도 경고만 출력하고
    # 프로그램을 계속 진행합니다.
    #
    # rows:
    # 이미지별 측정값을 저장할 빈 리스트입니다.
    # --------------------------------------------------

    image_infos = (
        find_calibration_images()
    )


    print(
        "Calibration Images:",
        len(image_infos)
    )


    if len(image_infos) != 12:

        print(
            "주의: Calibration 이미지는 "
            "OK 6장 + NG 6장 = 12장을 예상합니다."
        )


    rows = []


    # --------------------------------------------------
    # 5. Calibration 이미지 12장에 같은 측정 반복
    #
    # 무엇을 하나요?
    # - Calibration 이미지를 한 장씩 가져옵니다.
    # - measure_target() 공통 측정 함수를 호출합니다.
    # - 각 이미지의 측정값을 계산합니다.
    # - 측정값과 실제 정답을 하나의 딕셔너리로 정리합니다.
    #
    # measure_target() 내부 처리:
    #
    # ① Target 이미지 읽기
    # ② Template Matching
    # ③ SIFT 특징점 추출
    # ④ BFMatcher로 특징점 비교
    # ⑤ Ratio Test
    # ⑥ RANSAC + Homography
    # ⑦ Inlier Count / Inlier Ratio 계산
    #
    # 왜 필요한가요?
    # 모든 정상·불량 이미지에서 같은 측정값을
    # 얻어야 나중에 공정하게 비교할 수 있기 때문입니다.
    #
    # 주의:
    # 현재는 특징값을 측정하는 단계입니다.
    # 아직 Threshold나 OK/NG 판정 Rule은 적용하지 않습니다.
    # --------------------------------------------------

    for image_path, actual in image_infos:

        # 이미지 한 장의 특징값 측정
        measurement = measure_target(
            image_path,
            reference_data
        )


        # --------------------------------------------------
        # 5-1. 이미지 한 장의 측정값을 딕셔너리로 정리
        #
        # file:
        # 검사 이미지 이름
        #
        # actual:
        # 파일명으로 구분한 실제 정답(OK/NG)
        #
        # template_score:
        # 기준 로고와 가장 비슷한 영역의 유사도
        #
        # sift_good_matches:
        # Ratio Test를 통과한 SIFT 특징점 대응 개수
        #
        # homography_found:
        # Homography 계산 성공 여부
        # 1 = 성공 / 0 = 실패
        #
        # homography_inliers:
        # RANSAC의 변환 관계에 잘 맞는 대응점 개수
        #
        # inlier_ratio:
        # Inlier Count / Good Match Count
        #
        # round(값, 6):
        # 측정값을 소수점 여섯째 자리까지 반올림
        # --------------------------------------------------

        row = {

            "file":
                image_path.name,

            "actual":
                actual,

            "template_score":
                round(
                    measurement[
                        "template_score"
                    ],
                    6
                ),

            "sift_good_matches":
                measurement[
                    "sift_good_matches"
                ],

            "homography_found":
                measurement[
                    "homography_found"
                ],

            "homography_inliers":
                measurement[
                    "homography_inliers"
                ],

            "inlier_ratio":
                round(
                    measurement[
                        "inlier_ratio"
                    ],
                    6
                ),
        }


        # --------------------------------------------------
        # 5-2. 측정 결과를 리스트에 추가하고 출력
        #
        # 무엇을 하나요?
        # - 이미지 한 장의 측정 결과를 rows에 추가합니다.
        # - 현재 이미지의 결과를 터미널에 출력합니다.
        #
        # 반복문이 끝나면 rows에는
        # 모든 Calibration 이미지의 측정값이 저장됩니다.
        # --------------------------------------------------

        rows.append(
            row
        )


        print(
            row
        )


    # --------------------------------------------------
    # 6. Calibration 전체 측정값을 CSV 파일로 저장
    #
    # 무엇을 하나요?
    # - CSV의 컬럼명을 정의합니다.
    # - CSV 파일을 생성합니다.
    # - 각 이미지의 측정값을 한 행씩 저장합니다.
    #
    # 저장할 파일:
    # reports/day05_calibration_measurements.csv
    #
    # utf-8-sig:
    # Excel 등에서 한글이 깨지는 문제를 줄이기 위한 인코딩
    #
    # writer.writeheader():
    # CSV 첫 번째 행에 컬럼명 작성
    #
    # writer.writerows(rows):
    # 모든 Calibration 측정값 저장
    #
    # 왜 필요한가요?
    # 다음 실습에서 정상과 불량의 측정값을 비교하고
    # Threshold 후보를 찾기 위해서입니다.
    # --------------------------------------------------

    fieldnames = [

        "file",

        "actual",

        "template_score",

        "sift_good_matches",

        "homography_found",

        "homography_inliers",

        "inlier_ratio",
    ]


    with OUTPUT_CSV.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


    # --------------------------------------------------
    # 7. Calibration 측정 완료 및 저장 결과 확인
    #
    # 무엇을 하나요?
    # - Calibration 측정이 끝났음을 출력합니다.
    # - 측정한 이미지의 전체 개수를 출력합니다.
    # - 결과 CSV 파일의 저장 경로를 출력합니다.
    #
    # 왜 필요한가요?
    # 프로그램이 전체 이미지를 처리하고
    # 결과를 어디에 저장했는지 확인하기 위해서입니다.
    #
    # 이 단계에서 만드는 것은 측정 결과 CSV이며,
    # 최종 검사 기준은 다음 실습에서 결정합니다.
    # --------------------------------------------------

    print()
    print("=" * 70)

    print(
        "Calibration 측정 완료"
    )

    print(
        "전체 이미지:",
        len(rows)
    )

    print(
        "저장:",
        OUTPUT_CSV
    )

    print("=" * 70)


# --------------------------------------------------
# 8. Python 파일을 직접 실행할 때 main() 호출
#
# 무엇을 하나요?
# - 이 파일을 직접 실행한 경우 main()을 호출합니다.
#
# __name__ == "__main__":
# 현재 Python 파일을 직접 실행하고 있는지 확인합니다.
#
# 왜 필요한가요?
# 다른 파일에서 이 코드를 import할 때
# Calibration 측정 작업이 자동 실행되지 않도록
# 구분하기 위해서입니다.
#
# 실행 명령어:
# python src/34_day05_measure_calibration.py
# --------------------------------------------------

if __name__ == "__main__":
    main()
```
### 의사코드

```
[1. Reference, Calibration 이미지 및 CSV 경로 설정]

광천김 Reference 이미지 경로를 정한다.

samples/day04/reference/reference_label.jpg

Calibration 이미지 폴더를 지정한다.

samples/day05/resized/

결과 CSV 저장 경로를 정한다.

reports/day05_calibration_measurements.csv

          ↓

[2. Calibration 이미지 목록과 실제 상태 준비]

find_calibration_images() 함수를 만든다.

이미지 정보를 저장할 빈 리스트를 만든다.

          ↓

ok_로 시작하는 JPG 이미지를 찾는다.

각 이미지의 경로와
실제 정답 "OK"를 함께 저장한다.

          ↓

ng_로 시작하는 JPG 이미지를 찾는다.

각 이미지의 경로와
실제 정답 "NG"를 함께 저장한다.

          ↓

이미지 경로와 실제 정답 목록을 반환한다.

          ↓

[3. 결과 폴더 생성 및 Reference 특징점 준비]

main() 함수를 만든다.

결과 CSV를 저장할 reports 폴더를 준비한다.

prepare_reference() 함수를 호출한다.

Reference 이미지를 읽는다.

Reference를 Grayscale로 변환한다.

SIFT 특징점과 Descriptor를 추출한다.

Reference 정보를 reference_data에 저장한다.

Reference Keypoint 개수를 출력한다.

          ↓

[4. Calibration 이미지 목록과 수량 확인]

find_calibration_images() 함수를 호출한다.

준비된 Calibration 이미지 목록을 가져온다.

전체 이미지 개수를 출력한다.

          ↓

총 12장인지 확인한다.

12장이 아니라면 경고를 출력한다.

현재 코드는 경고 후에도 계속 진행한다.

          ↓

측정값을 저장할 rows 리스트를 만든다.

          ↓

[5. Calibration 이미지 12장에 같은 측정 반복]

첫 번째 Calibration 이미지를 선택한다.

이미지 경로와 실제 정답을 가져온다.

          ↓

measure_target() 함수를 호출한다.

Target 이미지와 reference_data를 전달한다.

          ↓

Template Matching을 실행한다.

Template Score를 측정한다.

          ↓

Target 이미지에서 SIFT 특징점을 추출한다.

          ↓

BFMatcher로 특징점 후보를 비교한다.

          ↓

Ratio Test로 Good Match를 선별한다.

          ↓

Good Match가 충분하면
RANSAC + Homography를 계산한다.

          ↓

Homography 계산 성공 여부를 확인한다.

Inlier Count를 측정한다.

Inlier Ratio를 계산한다.

          ↓

[5-1. 이미지별 측정값 정리]

현재 이미지 이름을 기록한다.

실제 상태 OK 또는 NG를 기록한다.

Template Score를 기록한다.

SIFT Good Match 개수를 기록한다.

Homography Found를 기록한다.

Homography Inlier 개수를 기록한다.

Inlier Ratio를 기록한다.

          ↓

[5-2. 측정 결과 저장]

현재 이미지의 측정값을
rows 리스트에 추가한다.

측정 결과를 터미널에 출력한다.

          ↓

아직 측정할 이미지가 남아 있다면
5번으로 돌아가 다음 이미지를 측정한다.

모든 이미지 측정이 끝나면
6번으로 이동한다.

          ↓

[6. Calibration 전체 측정값을 CSV 파일로 저장]

CSV에 저장할 컬럼명을 준비한다.

file
actual
template_score
sift_good_matches
homography_found
homography_inliers
inlier_ratio

          ↓

day05_calibration_measurements.csv 파일을 연다.

첫 번째 행에 컬럼명을 작성한다.

rows에 저장된 측정값을 한 행씩 작성한다.

CSV 파일을 저장한다.

          ↓

[7. Calibration 측정 완료 및 저장 결과 확인]

Calibration 측정 완료 메시지를 출력한다.

측정한 이미지의 전체 개수를 출력한다.

CSV 저장 경로를 출력한다.

          ↓

[8. 프로그램 실행]

Python 파일을 직접 실행하면
main() 함수를 호출한다.

          ↓

[최종 결과]

광천김 Reference 1장
        +
Calibration 12장
OK 6장 + NG 6장
        ↓
동일한 공통 측정 함수 사용
        ↓
Template Score
SIFT Good Match
Homography Found
Homography Inlier
Inlier Ratio
        ↓
이미지별 측정 결과 정리
        ↓
day05_calibration_measurements.csv 저장
        ↓
다음 실습
OK / NG 측정값 비교
        ↓
Threshold 후보 탐색
```

코드 실행

```bash
python src/34_day05_measure_calibration.py
```

프로그램은 다음 순서로 동작합니다.

```
reference_label.jpg 준비

        ↓

SIFT 특징점 미리 계산

        ↓

ok_01.jpg 측정
ok_02.jpg 측정
ok_03.jpg 측정
ok_04.jpg 측정
ok_05.jpg 측정
ok_06.jpg 측정

        ↓

ng_01.jpg 측정
ng_02.jpg 측정
ng_03.jpg 측정
ng_04.jpg 측정
ng_05.jpg 측정
ng_06.jpg 측정

        ↓

12장의 측정값을
CSV에 한 줄씩 저장
```

Calibration 측정 결과

```
Reference Keypoints: 675
Calibration Images: 12
{'file': 'ok_01.jpg', 'actual': 'OK', 'template_score': 0.535846, 'sift_good_matches': 174, 'homography_found': 1, 'homography_inliers': 167, 'inlier_ratio': 0.95977}
{'file': 'ok_02.jpg', 'actual': 'OK', 'template_score': 0.544862, 'sift_good_matches': 174, 'homography_found': 1, 'homography_inliers': 158, 'inlier_ratio': 0.908046}
{'file': 'ok_03.jpg', 'actual': 'OK', 'template_score': 0.556364, 'sift_good_matches': 184, 'homography_found': 1, 'homography_inliers': 164, 'inlier_ratio': 0.891304}
{'file': 'ok_04.jpg', 'actual': 'OK', 'template_score': 0.425379, 'sift_good_matches': 151, 'homography_found': 1, 'homography_inliers': 142, 'inlier_ratio': 0.940397}
{'file': 'ok_05.jpg', 'actual': 'OK', 'template_score': 0.552585, 'sift_good_matches': 161, 'homography_found': 1, 'homography_inliers': 147, 'inlier_ratio': 0.913043}
{'file': 'ok_06.jpg', 'actual': 'OK', 'template_score': 0.440258, 'sift_good_matches': 74, 'homography_found': 1, 'homography_inliers': 60, 'inlier_ratio': 0.810811}
{'file': 'ng_01.jpg', 'actual': 'NG', 'template_score': 0.531258, 'sift_good_matches': 126, 'homography_found': 1, 'homography_inliers': 120, 'inlier_ratio': 0.952381}
{'file': 'ng_02.jpg', 'actual': 'NG', 'template_score': 0.442885, 'sift_good_matches': 99, 'homography_found': 1, 'homography_inliers': 81, 'inlier_ratio': 0.818182}
{'file': 'ng_03.jpg', 'actual': 'NG', 'template_score': 0.484058, 'sift_good_matches': 141, 'homography_found': 1, 'homography_inliers': 109, 'inlier_ratio': 0.77305}
{'file': 'ng_04.jpg', 'actual': 'NG', 'template_score': 0.536214, 'sift_good_matches': 161, 'homography_found': 1, 'homography_inliers': 139, 'inlier_ratio': 0.863354}
{'file': 'ng_05.jpg', 'actual': 'NG', 'template_score': 0.525607, 'sift_good_matches': 107, 'homography_found': 1, 'homography_inliers': 94, 'inlier_ratio': 0.878505}
{'file': 'ng_06.jpg', 'actual': 'NG', 'template_score': 0.461591, 'sift_good_matches': 109, 'homography_found': 1, 'homography_inliers': 91, 'inlier_ratio': 0.834862}

======================================================================
Calibration 측정 완료
전체 이미지: 12
저장: reports/day05_calibration_measurements.csv
```

현재 결과물은:

```
터미널
→ 이미지별 측정값 확인

CSV
→ 12장의 측정값 저장
```

입니다.

---

## 17.1 결과는 어디에 저장되나요?

실행이 끝나면 다음 파일이 생성됩니다.

```
reports/day05_calibration_measurements.csv
```

CSV에는 다음 항목이 들어갑니다.

|항목|의미|
|---|---|
|`file`|검사한 이미지 이름|
|`actual`|실제 정답인 OK / NG|
|`template_score`|Template Matching 유사도|
|`sift_good_matches`|SIFT에서 남은 좋은 대응점 수|
|`homography_found`|Homography 계산 성공 여부|
|`homography_inliers`|RANSAC을 통과한 대응점 수|
|`inlier_ratio`|Good Match 중 Inlier의 비율|

| 파일          | 실제 상태 | Template | SIFT Good | Inlier | Inlier Ratio |
| ----------- | ----- | -------: | --------: | -----: | -----------: |
| `ok_01.jpg` | OK    |   0.5358 |       174 |    167 |       0.9598 |
| `ok_02.jpg` | OK    |   0.5449 |       174 |    158 |       0.9080 |
| `ok_03.jpg` | OK    |   0.5564 |       184 |    164 |       0.8913 |
| `ok_04.jpg` | OK    |   0.4254 |       151 |    142 |       0.9404 |
| `ok_05.jpg` | OK    |   0.5526 |       161 |    147 |       0.9130 |
| `ok_06.jpg` | OK    |   0.4403 |        74 |     60 |       0.8108 |
| `ng_01.jpg` | NG    |   0.5313 |       126 |    120 |       0.9524 |
| `ng_02.jpg` | NG    |   0.4429 |        99 |     81 |       0.8182 |
| `ng_03.jpg` | NG    |   0.4841 |       141 |    109 |       0.7731 |
| `ng_04.jpg` | NG    |   0.5362 |       161 |    139 |       0.8634 |
| `ng_05.jpg` | NG    |   0.5256 |       107 |     94 |       0.8785 |
| `ng_06.jpg` | NG    |   0.4616 |       109 |     91 |       0.8349 |

##### 세 가지 측정값의 차이

|측정값|높을 때|낮을 때|
|---|---|---|
|SIFT Good Match|비슷하게 연결된 특징점이 많음|연결된 특징점이 적음|
|Inlier|위치 관계까지 일치하는 특징점이 많음|일관된 위치 관계를 가진 특징점이 적음|
|Inlier Ratio|연결된 특징점 중 일관된 대응점의 비율이 높음|일관된 대응점의 비율이 낮음|

쉽게 이해하면 다음과 같습니다.

- SIFT Good Match: 얼마나 많은 특징점이 연결되었는가?
    
- Inlier: 그중 위치 관계까지 맞는 특징점은 몇 개인가?
    
- Inlier Ratio: 연결된 특징점 중 몇 %가 위치 관계에 일치하는가?

여기서 주목할 부분은 다음 두 가지입니다.

① `ok_06`은 정상인데 수치가 낮습니다.
② `ng_01`은 불량인데 Inlier Ratio가 0.9524로 매우 높습니다.

즉, Inlier Ratio가 95%라고 해서 로고의 95%가 정상이라는 뜻은 아닙니다. 연결된 특징점 가운데 약 95%가 계산된 위치 관계에 일치한다는 의미입니다.

아래에서 좀더 상세히 분석해 보겠습니다.


```
ok_01.jpg
→ 사람이 알고 있는 실제 정답 = OK

ng_01.jpg
→ 사람이 알고 있는 실제 정답 = NG
```

그 옆의 숫자들이 OpenCV가 실제 이미지에서 측정한 값입니다.

---

## 17.2 먼저 Template Score를 비교합니다

정상과 불량의 범위를 확인합니다.

```
OK
0.4254 ~ 0.5564

NG
0.4429 ~ 0.5362
```

두 범위를 놓고 보면 상당히 많이 겹칩니다.

```
OK  ────────────────
     0.425       0.556

NG     ────────────
       0.443     0.536
```

예를 들어:

```
ok_04.jpg
Template = 0.4254

ng_04.jpg
Template = 0.5362
```

입니다.

오히려 NG인 `ng_04.jpg`의 Template Score가 정상인 `ok_04.jpg`보다 높습니다.

따라서 현재 데이터에서는:

> Template Score가 높다고 무조건 OK라고 판정할 수 없습니다.

라는 사실을 확인할 수 있습니다.

4일차에서 배운 것처럼 Template Matching은 촬영 위치·회전·크기 변화에 영향을 받을 수 있기 때문입니다.

쉽게 다시 설명하면

```
OK와 NG의 Template Score가 서로 다른 구간으로 나뉘지 않고 같은 숫자 영역에 섞여 있다는 뜻
```

입니다.

예를 들어 `0.50` 정도의 값은 OK에서도 나올 수 있고 NG에서도 나올 수 있습니다.

```
OK 범위 : 0.4254 ~ 0.5564 
NG 범위 : 0.4429 ~ 0.5362 

겹치는 구간 
→ 약 0.4429 ~ 0.5362
```

즉 이 겹치는 구간에서는 Template Score만 보고는 이 이미지가 OK인지 NG인지 확실히 구분하기 어렵습니다.

따라서 Template Score 하나만으로 기준을 만들기보다, SIFT Good Match나 Inlier Ratio 같은 
다른 측정값도 함께 비교해야 합니다.

---

## 17.3 SIFT Good Match를 비교합니다

이번에는 특징점 대응 개수를 확인합니다.

```
OK
74 ~ 184개

NG
99 ~ 161개
```

평균적으로 보면:

```
OK 평균
약 153개

NG 평균
약 124개
```

로 정상 이미지에서 더 많은 Match가 만들어졌습니다.

하지만 이것도 완전히 분리되지는 않습니다.

예를 들어:

```
ok_06.jpg
→ 74개

ng_04.jpg
→ 161개
```

입니다.

즉:

```
SIFT Match가 많다
→ 정상일 가능성이 높아질 수 있음

하지만

Match 수 하나만으로
모든 OK / NG를 구분할 수는 없음
```

이라는 것을 실제 데이터에서 확인했습니다.

---

## 17.4 Homography Inlier도 비교합니다

RANSAC을 통과한 실제 대응점 수입니다.

```
OK
60 ~ 167개

NG
81 ~ 139개
```

참고] RANSAC(랜색): 여러 Match 중에서 잘못 연결된 점을 제외하고, 서로 일관되게 맞는 점들만 골라내는 방법.

평균은:

```
OK
약 140개

NG
약 106개
```

입니다.

정상 이미지가 전체적으로 높은 편이지만 여기에서도 범위가 겹칩니다.

따라서 Inlier 개수 역시 단독으로 바로 Threshold를 정하기에는 부족할 가능성이 있습니다.

---

## 17.5 Inlier Ratio를 비교합니다

이번에는 Good Match 중 실제로 일관된 Match의 비율을 확인합니다.

```
OK
0.8108 ~ 0.9598

NG
0.7731 ~ 0.9524
```

정상 평균은 약:

```
0.904
```

불량 평균은 약:

```
0.853
```

으로 정상 쪽이 조금 더 높습니다.

하지만 중요한 결과가 하나 있습니다.

```
ok_06.jpg
→ 0.8108

ng_01.jpg
→ 0.9524
```

불량인 `ng_01.jpg`가 정상인 `ok_06.jpg`보다 훨씬 높은 Inlier Ratio를 보입니다.

따라서:

> Inlier Ratio가 높다고 반드시 정상 로고라는 뜻도 아닙니다.

SIFT와 Homography는 로고 일부가 가려져 있더라도 남아 있는 특징점끼리 정확하게 대응되면 높은 값을 만들 수 있기 때문입니다.

이것이 이번 NG 데이터에서 확인한 중요한 특징입니다.

---

## 17.6 Homography Found는 어떻게 나왔나요?

12장 모두:

```
homography_found = 1
```

이 나왔습니다.

즉:

```
OK 6장
→ Homography 계산 성공

NG 6장
→ Homography 계산 성공
```

입니다.

왜 NG인데도 Homography를 찾았을까요?

현재 NG 이미지는 로고를 일부 가린 형태입니다.

```
로고 일부 가림
        ↓
가려지지 않은 글자와 모서리는 남아 있음
        ↓
SIFT가 남아 있는 특징점을 찾음
        ↓
Homography 계산 가능
```

따라서:

```
Homography Found = 1
→ 로고와 대응되는 특징점이 존재한다
```

는 뜻이지,

```
Homography Found = 1
→ 제품이 정상이다
```

라는 뜻은 아닙니다.

---

## 17.7 이번 Calibration에서 발견한 핵심

처음에는 다음과 같이 예상했을 수 있습니다.

```
OK
→ 높은 값

NG
→ 낮은 값

        ↓

중간에 Threshold 하나 설정
```

하지만 실제 결과는 그렇게 단순하지 않았습니다.

```
Template Score
→ OK / NG가 많이 겹침

SIFT Good Match
→ 정상 평균은 높지만 일부 겹침

Homography Inlier
→ 정상 평균은 높지만 일부 겹침

Inlier Ratio
→ 정상 평균은 높지만 일부 NG도 매우 높음

Homography Found
→ 12장 모두 1
```

즉 현재 데이터에서는 한 가지 숫자만 보고 정상과 불량을 완벽하게 나누기 어렵습니다.

이 결과는 실습 실패가 아닙니다.

오히려 이것이 Calibration을 하는 이유입니다.

```
실제 데이터 측정
        ↓
예상과 실제가 같은지 확인
        ↓
값이 겹치는 것을 발견
        ↓
어떤 Feature를 사용할지 고민
        ↓
여러 조건을 조합할 필요가 있는지 확인
```

---

## 17.8 특히 확인해야 할 이미지가 있습니다

다음 이미지는 이후 분석에서 다시 살펴볼 가치가 있습니다.

실제 사진을 다시 보고:

```
회전이 컸는가?
거리가 달랐는가?
로고가 작게 촬영되었는가?
Blur가 있었는가?
빛 반사가 있었는가?
```

를 확인할 필요가 있습니다.

실제 이미지를 보면

```
ok_06.jpg

SIFT Good Match = 74
Inlier = 60
Inlier Ratio = 0.8108
```

정상 이미지인데 다른 OK 이미지보다 값이 크게 낮습니다.

`ok_06.jpg`
![[Pasted image 20260831190251.png|325]]

### 실제 이미지를 확인한 결과

사진을 보면 제품이 다른 정상 이미지보다 조금 멀리 촬영되어 로고가 작게 보이고, 촬영 각도와 포장지의 반사도 조금 다릅니다.

```
로고 자체
→ 정상

하지만

촬영 거리 / 크기 / 각도 차이
        ↓
특징점 Matching 감소
        ↓
SIFT와 Inlier 값이 낮아짐
```

즉 제품은 정상이어도 촬영조건이 달라지면 Matching 값이 낮아질 수 있음을 확인할 수 있습니다.


반대로:

```
ng_01.jpg

SIFT Good Match = 126
Inlier = 120
Inlier Ratio = 0.9524
```

는 불량인데도 매우 높은 Inlier Ratio가 나왔습니다.

`ng_01.jpg`
![[Pasted image 20260831190350.png|357]]

### 실제 이미지를 확인한 결과

카드로 로고 일부를 가렸지만 가려지지 않은 영역에는 여전히 로고의 글자와 특징점이 많이 남아 있습니다.

```
로고 일부 가림
        ↓
Good Match 수는 감소
        ↓
하지만 남아 있는 Match들은
서로 위치관계가 매우 잘 맞음
        ↓
Inlier Ratio는 높게 나옴
```

즉 Inlier Ratio가 높다고 반드시 정상이라는 뜻은 아니라는 것을 실제 이미지에서 확인할 수 있습니다.


또:

```
ng_04.jpg

SIFT Good Match = 161
Inlier = 139
```

NG인데도 SIFT Good Match가 정상 이미지와 비슷하게 많이 나왔습니다.

`ng_04.jpg`
![[Pasted image 20260831190427.png|357]]

### 실제 이미지를 확인한 결과

로고 일부가 가려져 있지만 **주변의 글자와 로고 특징이 상당 부분 그대로 남아 있기 때문에 SIFT가 많은 특징점을 연결할 수 있습니다.**

```
일부 로고 가림
        ↓
남아 있는 특징이 많음
        ↓
SIFT Good Match는 높게 나옴

하지만

일부 대응점의 위치관계가 불안정
        ↓
Inlier Ratio는 0.8634로 낮아짐
```

따라서 SIFT Match 개수 하나만으로도 OK / NG를 판단하기 어렵다는 것을 확인할 수 있습니다.

### 세 이미지를 통해 확인한 핵심

```
ok_06
→ 정상이어도 촬영조건 때문에 값이 낮아질 수 있음

ng_01
→ 불량이어도 Inlier Ratio가 높을 수 있음

ng_04
→ 불량이어도 SIFT Match가 많을 수 있음
```

> 그래서 하나의 측정값만으로 판정하지 않고, SIFT Good Match와 Inlier Ratio 같은 여러 값을 함께 비교하여 복합 Rule을 만드는 것입니다.

---

## 17.9 지금까지 한 일을 정리합니다

이번 실습에서는:

```
광천김 Calibration 이미지 12장
        ↓
같은 Reference 사용
        ↓
같은 측정 조건 적용
        ↓
Template Score
SIFT Good Match
Homography Inlier
Inlier Ratio
        ↓
CSV 저장
        ↓
OK와 NG 결과 비교
```

까지 진행했습니다.

아직 Threshold와 Rule은 정하지 않았습니다.

실제 결과를 보니 한 가지 Feature로는 정상과 불량이 깔끔하게 나뉘지 않았습니다.

따라서 다음 단계에서는 이 CSV를 이용하여:

```
어떤 Threshold 후보가 있는가?
        ↓
한 가지 조건으로 충분한가?
        ↓
여러 Feature를 조합하면
더 잘 구분할 수 있는가?
        ↓
복합 Rule 후보 만들기
```

를 실제 데이터로 확인합니다.

![[Pasted image 20261028170927.png]]

---

# 18. 이제 Rule 후보에 사용할 값을 정합니다

앞에서 Calibration 12장의 실제 측정값을 비교했습니다.

그 결과 한 가지 값만으로는 OK와 NG를 확실하게 나누기 어렵다는 것을 확인했습니다.

그래서 이번에는 다음 두 값을 함께 사용합니다.

| 측정값               | 쉽게 말하면                        |
| ----------------- | ----------------------------- |
| `SIFT Good Match` | 비슷한 특징점이 충분히 많이 연결되었는가?       |
| `Inlier Ratio`    | 연결된 특징점들이 실제 위치관계에서도 제대로 맞는가? |

쉽게 생각하면 다음과 같습니다.

```
특징점이 충분히 많이 연결되었는가?
                +
그 연결이 실제로도 잘 맞는가?
```

따라서 앞으로 시험할 Rule의 기본 모양은 다음과 같습니다.

![[Pasted image 20260831201251.png]]

```
Homography 계산 성공

        AND

SIFT Good Match >= ?

        AND

Inlier Ratio >= ?

        ↓

모두 만족
→ OK

하나라도 부족
→ NG
```

여기서 아직 모르는 것은 두 개입니다.

```
SIFT는 몇 이상이어야 할까?

Inlier Ratio는 몇 이상이어야 할까?
```

이 숫자가 바로 Threshold입니다.

> 다음 단계에서는 이 숫자를 사람이 감으로 정하지 않고, Calibration 데이터를 이용하여 여러 Threshold 후보를 직접 시험해 봅니다.

---

# 19. 여러 Threshold 후보를 시험하여 좋은 Rule을 찾아봅니다

이제 해야 할 일은 간단합니다.

```
SIFT 기준값
        +
Inlier Ratio 기준값
        ↓
어떤 조합이
OK와 NG를 가장 잘 구분할까?
```

예를 들어 다음과 같은 여러 후보를 생각할 수 있습니다.

![[Pasted image 20260831201736.png]]

```
후보 A
SIFT >= 100
Inlier Ratio >= 0.80

후보 B
SIFT >= 120
Inlier Ratio >= 0.85

후보 C
SIFT >= 140
Inlier Ratio >= 0.90
```

하지만 어떤 후보가 좋은지는 숫자만 보고 알 수 없습니다.

그래서 각 후보를 Calibration 12장에 실제로 적용해 봅니다.

```
Threshold 후보 하나 선택
        ↓
Calibration 12장에 적용
        ↓
프로그램이 OK / NG 판정
        ↓
사람이 알고 있는 실제 정답과 비교
        ↓
TP / TN / FP / FN 확인
        ↓
오류 개수 기록
```

그리고 다른 Threshold 조합으로 같은 작업을 반복합니다.

```
후보 A 적용
→ 오류 확인

후보 B 적용
→ 오류 확인

후보 C 적용
→ 오류 확인

...

        ↓

오류가 적은 후보 찾기
```

특히 이번 제조검사에서는 **불량을 OK로 잘못 통과시키는 FN을 중요하게 봅니다.**

따라서 프로그램은 후보들을 비교한 뒤:

```
FN이 적고
        ↓
전체 오류가 적고
        ↓
FP도 적은 후보
```

를 위쪽에 보여줍니다.

---

## 19.1 그래프로 생각하면 더 쉽습니다

이번 Rule은 두 개의 값을 사용하므로 X-Y 그래프로 볼 수 있습니다.

![[Pasted image 20260831202313.png]]

```
Y축
Inlier Ratio
    ↑
    │                   ● OK
    │             ●
    │
────┼────────────────────  ← Inlier Threshold
    │         × NG
    │    ×
    │
    └────────│────────────→ X축
             SIFT Threshold
             SIFT Good Match
```

기준선은 두 개입니다.

```
세로선
→ SIFT Good Match 기준

가로선
→ Inlier Ratio 기준
```

현재 Rule에서는:

```
세로선보다 오른쪽
        AND
가로선보다 위쪽
        ↓
OK
```

입니다.

즉 Threshold 후보를 찾는다는 것은 쉽게 말하면:

> “세로선과 가로선을 어디에 그어야 실제 OK와 NG를 가장 적게 틀릴까?”를 여러 번 시험하는 과정입니다.

---

이 작업을 프로그램으로 수행하는 것이 다음 코드입니다.

```
src/35_day05_analyze_calibration.py
```

이 프로그램의 입력과 출력은 다음과 같습니다.

```
입력
reports/day05_calibration_measurements.csv

        ↓

35_day05_analyze_calibration.py

        ↓

출력 1
reports/day05_rule_candidates.csv
→ Threshold 후보별 결과

출력 2
outputs/day05/calibration/
sift_inlier_distribution.png
→ OK / NG 분포 그래프
```

> **이번 실습의 핵심은 좋은 Threshold 숫자를 외우는 것이 아니라, 여러 후보를 실제 데이터에 적용하여 오류가 적은 기준을 찾는 방법을 이해하는 것입니다.**


![[Pasted image 20260831153638.png]]

---

## 19.3 `35_day05_analyze_calibration.py` — 후보 Rule을 비교합니다

==`측정값 분석 + Rule 후보 탐색 :  CSV를 보고 어떤 기준값이 좋은지 찾아보는 코드 `==

`34_day05_measure_calibration.py`에서 만든 CSV를 분석합니다

```
day05_calibration_measurements.csv
        ↓
35_day05_analyze_calibration.py
        ↓
OK / NG 값의 분포 확인
        ↓
SIFT Threshold 후보 생성
+
Inlier Ratio Threshold 후보 생성
        ↓
여러 조합 시험
        ↓
Calibration 12장에 적용
        ↓
TP / TN / FP / FN 비교
        ↓
오류가 적은 Rule 후보 찾기
```

그리고 두 가지 결과를 만듭니다.

```
day05_rule_candidates.csv
→ 어떤 Threshold 조합이 좋았는지

sift_inlier_distribution.png
→ OK / NG가 그래프에서 어떻게 분포하는지
```

즉 `35_day05_analyze_calibration.py` 이코드는 측정한 숫자를 분석해서 Rule 후보를 찾는 코드를 작성하는 겁니다.

이번 프로그램의 입력과 출력은 다음과 같습니다.

```
입력
reports/day05_calibration_measurements.csv

        ↓
여러 Threshold 후보 시험
        ↓
출력 1
reports/day05_rule_candidates.csv

출력 2
outputs/day05/calibration/
sift_inlier_distribution.png
```

코드 작성전 먼저 이번 실습에 필요한 라이브러리를 설치합니다.

```bash
python -m pip install pandas matplotlib
```

각 라이브러리의 역할은 다음과 같습니다.

| 라이브러리        | 이번 실습에서 하는 일                       |
| ------------ | ---------------------------------- |
| `Pandas`     | Calibration CSV를 읽고 OK/NG 측정값을 분석함 |
| `Matplotlib` | SIFT와 Inlier Ratio의 분포를 그래프로 그림    |
```
Pandas
→ CSV를 읽고 측정값을 표처럼 분석

NumPy
→ 여러 Threshold 후보값 생성

Matplotlib
→ OK와 NG의 측정값 분포를 그래프로 표현
```

파일생성:

```text
src/35_day05_analyze_calibration.py
```

다음 코드를 작성합니다.

```python
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# 1. Calibration 입력 CSV와 결과 저장 경로 설정
#
# 무엇을 하나요?
# - 앞에서 측정한 Calibration CSV 경로를 지정합니다.
# - Threshold 후보별 결과를 저장할 CSV 경로를 정합니다.
# - OK/NG 측정값 분포를 저장할 그래프 경로를 정합니다.
#
# CSV_PATH:
# Calibration 12장의 실제 측정값이 저장된 파일
#
# CANDIDATE_CSV:
# 여러 Threshold 조합의 성능을 저장할 파일
#
# PLOT_PATH:
# SIFT Good Match와 Inlier Ratio의
# OK/NG 분포를 시각화할 그래프 파일
#
# 왜 필요한가요?
# 측정된 데이터를 읽고,
# 분석 결과를 다시 확인할 수 있도록
# CSV와 이미지 파일로 저장하기 위해서입니다.
# --------------------------------------------------

CSV_PATH = Path(
    "reports/day05_calibration_measurements.csv"
)

CANDIDATE_CSV = Path(
    "reports/day05_rule_candidates.csv"
)

PLOT_PATH = Path(
    "outputs/day05/calibration/sift_inlier_distribution.png"
)


# --------------------------------------------------
# 2. Threshold 후보값을 생성하는 함수
#
# 무엇을 하나요?
# - CSV의 측정값에서 최소값과 최대값을 찾습니다.
# - 최소값과 최대값 사이의 후보값을 생성합니다.
# - 기본적으로 15개의 후보값을 만듭니다.
#
# Threshold란?
# 측정값이 정상 기준을 만족하는지 판단할 경계값입니다.
#
# 예:
# SIFT Good Match >= 129
# Inlier Ratio >= 0.8664
#
# series:
# 후보를 만들 측정값 데이터
#
# count=15:
# 생성할 후보값의 기본 개수
#
# integer=False:
# 소수점 값을 사용할지 결정하는 설정
#
# integer=True:
# SIFT Good Match처럼 정수 기준값 생성
#
# integer=False:
# Inlier Ratio처럼 소수 기준값 생성
#
# 왜 필요한가요?
# Threshold를 감으로 하나만 정하는 대신
# 실제 측정값 범위에서 여러 기준을 시험하기 위해서입니다.
# --------------------------------------------------

def make_candidates(
    series,
    count=15,
    integer=False,
):

    # --------------------------------------------------
    # 2-1. 측정값을 숫자로 변환하고 빈 값 제거
    #
    # pd.to_numeric():
    # 데이터를 숫자 형태로 변환합니다.
    #
    # errors="coerce":
    # 숫자로 변환할 수 없는 값은 NaN으로 처리합니다.
    #
    # dropna():
    # NaN 값을 제거합니다.
    # --------------------------------------------------

    values = pd.to_numeric(
        series,
        errors="coerce",
    ).dropna()


    # 사용할 측정값이 없다면 빈 리스트 반환
    if values.empty:
        return []


    # --------------------------------------------------
    # 2-2. 측정값의 최소값과 최대값 찾기
    #
    # low:
    # 가장 작은 측정값
    #
    # high:
    # 가장 큰 측정값
    #
    # 이 범위에서 Threshold 후보를 생성합니다.
    # --------------------------------------------------

    low = float(
        values.min()
    )

    high = float(
        values.max()
    )


    # --------------------------------------------------
    # 2-3. 모든 측정값이 같은 경우 처리
    #
    # 최소값과 최대값이 같으면
    # 서로 다른 후보를 만들 수 없습니다.
    #
    # 따라서 현재 값 하나만 후보로 반환합니다.
    # --------------------------------------------------

    if low == high:

        if integer:
            return [int(low)]

        return [low]


    # --------------------------------------------------
    # 2-4. 최소값부터 최대값까지 후보 생성
    #
    # np.linspace():
    # 시작값과 끝값 사이를 균등하게 나누어
    # 지정한 개수의 숫자를 생성하는 함수입니다.
    #
    # 예:
    # 최소값 100, 최대값 200, count=5
    #
    # 후보:
    # 100, 125, 150, 175, 200
    #
    # 이번에는 기본적으로 15개를 생성합니다.
    # --------------------------------------------------

    candidates = np.linspace(
        low,
        high,
        count,
    )


    # --------------------------------------------------
    # 2-5. 정수 Threshold 후보 정리
    #
    # integer=True이면:
    # - 각 후보를 반올림하여 정수로 변환합니다.
    # - 중복값을 제거합니다.
    # - 작은 값부터 정렬합니다.
    #
    # SIFT Good Match 개수에 사용합니다.
    # --------------------------------------------------

    if integer:

        return sorted(
            set(
                int(round(value))
                for value in candidates
            )
        )


    # --------------------------------------------------
    # 2-6. 소수 Threshold 후보 정리
    #
    # integer=False이면:
    # - 소수점 넷째 자리까지 반올림합니다.
    # - 중복값을 제거합니다.
    # - 작은 값부터 정렬합니다.
    #
    # Inlier Ratio 기준값에 사용합니다.
    #
    # 주의:
    # 중복 제거로 최종 후보 수가 15개보다 적을 수도 있습니다.
    # --------------------------------------------------

    return sorted(
        set(
            round(
                float(value),
                4,
            )
            for value in candidates
        )
    )


# --------------------------------------------------
# 3. 실제 정답과 프로그램 판정을 비교하는 함수
#
# 무엇을 하나요?
# - Calibration 이미지의 실제 정답과
#   프로그램이 임시 Rule로 판정한 값을 비교합니다.
# - 결과를 TP, TN, FP, FN으로 구분합니다.
#
# 이번 제조검사에서는 NG를 Positive로 정의합니다.
#
# TP:
# 실제 NG → 프로그램 NG
# 불량을 올바르게 검출
#
# TN:
# 실제 OK → 프로그램 OK
# 정상을 올바르게 통과
#
# FP:
# 실제 OK → 프로그램 NG
# 정상을 불량으로 잘못 판단
#
# FN:
# 실제 NG → 프로그램 OK
# 불량을 정상으로 잘못 통과
#
# 왜 필요한가요?
# Threshold 후보를 비교할 때
# 단순히 맞힌 개수뿐 아니라
# 어떤 종류의 오류가 발생했는지 확인하기 위해서입니다.
# --------------------------------------------------

def classify_error(
    actual,
    predicted,
):

    # 실제 NG를 NG로 올바르게 검출
    if (
        actual == "NG"
        and predicted == "NG"
    ):
        return "TP"


    # 실제 OK를 OK로 올바르게 판정
    if (
        actual == "OK"
        and predicted == "OK"
    ):
        return "TN"


    # 실제 OK를 NG로 잘못 판정
    if (
        actual == "OK"
        and predicted == "NG"
    ):
        return "FP"


    # 실제 NG를 OK로 잘못 통과
    if (
        actual == "NG"
        and predicted == "OK"
    ):
        return "FN"


    # 예상하지 못한 값이 들어온 경우
    return "UNKNOWN"


# --------------------------------------------------
# 4. Calibration CSV를 읽고 데이터 수량 확인
#
# 무엇을 하나요?
# - main() 함수를 정의합니다.
# - 앞에서 만든 CSV가 존재하는지 확인합니다.
# - Pandas로 CSV를 읽습니다.
# - 전체 이미지 개수와 실제 OK/NG 개수를 확인합니다.
#
# 이번 수업에서 예상하는 데이터:
# OK 6장 + NG 6장 = 총 12장
#
# pd.read_csv():
# CSV 파일을 DataFrame 형태로 읽는 함수
#
# value_counts():
# 각 값이 몇 번 나타나는지 세는 함수
#
# 왜 필요한가요?
# Threshold를 분석하기 전에
# 사용할 Calibration 데이터의 구성을 확인하기 위해서입니다.
# --------------------------------------------------

def main():

    if not CSV_PATH.exists():

        raise FileNotFoundError(
            CSV_PATH
        )


    df = pd.read_csv(
        CSV_PATH
    )


    print("=" * 70)
    print("Calibration 데이터")
    print("=" * 70)

    print(
        "전체 이미지:",
        len(df)
    )


    print(
        df["actual"].value_counts()
    )


    # --------------------------------------------------
    # 5. OK와 NG의 측정값 기본 통계 확인
    #
    # 무엇을 하나요?
    # - 분석할 숫자 컬럼 4개를 선택합니다.
    # - 실제 OK/NG를 구분하여 통계를 계산합니다.
    #
    # 측정 항목:
    # template_score:
    # Template Matching 유사도
    #
    # sift_good_matches:
    # SIFT Good Match 개수
    #
    # homography_inliers:
    # RANSAC Inlier 개수
    #
    # inlier_ratio:
    # Good Match 중 Inlier의 비율
    #
    # min:
    # 가장 작은 값
    #
    # mean:
    # 평균값
    #
    # max:
    # 가장 큰 값
    #
    # 왜 필요한가요?
    # 정상과 불량의 측정값이 어느 정도 다르고
    # 서로 겹치는 범위가 있는지 확인하기 위해서입니다.
    #
    # 주의:
    # 여기서는 네 가지 측정값의 통계를 확인하지만,
    # 이후 Rule 후보 생성에는 SIFT와 Inlier Ratio를 사용합니다.
    # --------------------------------------------------

    numeric_columns = [
        "template_score",
        "sift_good_matches",
        "homography_inliers",
        "inlier_ratio",
    ]


    print()

    print("=" * 70)
    print("OK / NG 측정값 통계")
    print("=" * 70)


    statistics = (
        df.groupby("actual")[
            numeric_columns
        ]
        .agg(
            [
                "min",
                "mean",
                "max",
            ]
        )
    )


    print(
        statistics
    )


    # --------------------------------------------------
    # 6. SIFT와 Inlier Ratio의 Threshold 후보 생성
    #
    # 무엇을 하나요?
    # - 2번에서 만든 make_candidates()를 호출합니다.
    # - SIFT Good Match의 Threshold 후보를 생성합니다.
    # - Inlier Ratio의 Threshold 후보를 생성합니다.
    #
    # SIFT:
    # 특징점 개수이므로 정수 후보를 사용합니다.
    #
    # Inlier Ratio:
    # 비율이므로 소수 후보를 사용합니다.
    #
    # 예:
    # SIFT >= 129
    # Inlier Ratio >= 0.8664
    #
    # 왜 필요한가요?
    # 여러 기준값을 조합하여
    # 실제 OK와 NG를 잘 구분하는 Rule을 찾기 위해서입니다.
    # --------------------------------------------------

    sift_candidates = make_candidates(
        df["sift_good_matches"],
        count=15,
        integer=True,
    )


    inlier_candidates = make_candidates(
        df["inlier_ratio"],
        count=15,
        integer=False,
    )


    print()

    print(
        "SIFT Threshold 후보:"
    )

    print(
        sift_candidates
    )


    print()

    print(
        "Inlier Ratio Threshold 후보:"
    )

    print(
        inlier_candidates
    )


    # --------------------------------------------------
    # 7. SIFT와 Inlier Ratio의 모든 Threshold 조합 시험
    #
    # 무엇을 하나요?
    # - SIFT 후보 하나를 선택합니다.
    # - Inlier Ratio 후보 하나를 선택합니다.
    # - 두 값을 조합하여 임시 Rule을 만듭니다.
    # - 현재 Rule을 Calibration 전체 이미지에 적용합니다.
    #
    # 임시 Rule:
    #
    # Homography 계산 성공
    #        AND
    # SIFT Good Match >= 후보값
    #        AND
    # Inlier Ratio >= 후보값
    #
    # 모두 만족하면 OK
    # 하나라도 만족하지 못하면 NG
    #
    # 왜 필요한가요?
    # 여러 Threshold 조합 중
    # 어떤 조합이 실제 정상과 불량을
    # 가장 적게 잘못 판정하는지 확인하기 위해서입니다.
    #
    # 후보가 각각 15개라면:
    # 15 × 15 = 225개 조합을 시험합니다.
    #
    # 단, 중복 후보가 제거되면 실제 조합 수는 줄어듭니다.
    # --------------------------------------------------

    rows = []


    for sift_min in sift_candidates:

        for inlier_min in inlier_candidates:

            # 현재 후보 Rule의 평가값 초기화
            tp = 0
            tn = 0
            fp = 0
            fn = 0


            # --------------------------------------------------
            # 7-1. Calibration 이미지마다 임시 Rule 적용
            #
            # 무엇을 하나요?
            # - CSV의 각 이미지 측정값을 하나씩 확인합니다.
            # - 현재 Threshold 조합을 적용합니다.
            # - 조건을 모두 만족하면 OK로 판정합니다.
            # - 하나라도 실패하면 NG로 판정합니다.
            #
            # 여기서는 이미 저장한 측정값을 사용합니다.
            # 원본 이미지를 다시 읽거나 SIFT를 재실행하지 않습니다.
            # --------------------------------------------------

            for _, row in df.iterrows():

                predicted = (
                    "OK"

                    if (
                        int(
                            row["homography_found"]
                        )
                        == 1

                        and int(
                            row["sift_good_matches"]
                        )
                        >= sift_min

                        and float(
                            row["inlier_ratio"]
                        )
                        >= inlier_min
                    )

                    else "NG"
                )


                # --------------------------------------------------
                # 7-2. 실제 정답과 임시 판정을 비교
                #
                # 무엇을 하나요?
                # - classify_error() 함수를 호출합니다.
                # - 현재 이미지의 결과를 TP/TN/FP/FN으로 구분합니다.
                # - 해당 오류 유형의 개수를 1 증가시킵니다.
                #
                # 특히 FN은 실제 불량을 정상으로 통과시키는
                # 오류이므로 이번 제조검사에서 중요하게 확인합니다.
                # --------------------------------------------------

                error = classify_error(
                    row["actual"],
                    predicted,
                )


                if error == "TP":
                    tp += 1

                elif error == "TN":
                    tn += 1

                elif error == "FP":
                    fp += 1

                elif error == "FN":
                    fn += 1


            # --------------------------------------------------
            # 8. 현재 Threshold 조합의 Accuracy와 오류 기록
            #
            # 무엇을 하나요?
            # - TP/TN/FP/FN을 합하여 평가 이미지 수를 계산합니다.
            # - 올바르게 판정한 비율인 Accuracy를 계산합니다.
            # - 현재 Threshold 후보의 평가 결과를 저장합니다.
            #
            # Accuracy:
            # (TP + TN) / (TP + TN + FP + FN)
            #
            # total_error:
            # FP + FN
            #
            # 예:
            # 12장 중 11장을 맞혔다면
            # Accuracy = 11 / 12 ≈ 0.9167
            #
            # rows에는 모든 Threshold 조합의 결과가 저장됩니다.
            # --------------------------------------------------

            total = (
                tp
                + tn
                + fp
                + fn
            )


            accuracy = (
                (tp + tn) / total
                if total > 0
                else 0.0
            )


            rows.append(
                {
                    "sift_good_matches_min":
                        sift_min,

                    "inlier_ratio_min":
                        inlier_min,

                    "accuracy":
                        round(
                            accuracy,
                            4,
                        ),

                    "tp":
                        tp,

                    "tn":
                        tn,

                    "fp":
                        fp,

                    "fn":
                        fn,

                    "total_error":
                        fp + fn,
                }
            )


    # --------------------------------------------------
    # 9. Threshold 후보를 오류가 적은 순서로 정렬
    #
    # 무엇을 하나요?
    # - 후보별 평가 결과를 DataFrame으로 변환합니다.
    # - 정해진 우선순위에 따라 후보를 정렬합니다.
    #
    # 정렬 우선순위:
    #
    # ① fn
    #    불량을 정상으로 놓친 개수가 적은 후보
    #
    # ② total_error
    #    전체 오류(FP + FN)가 적은 후보
    #
    # ③ fp
    #    정상을 불량으로 잘못 판정한 개수가 적은 후보
    #
    # ④ sift_good_matches_min
    #    앞 조건까지 같으면 SIFT 기준값이 작은 후보
    #
    # ⑤ inlier_ratio_min
    #    앞 조건까지 같으면 Inlier Ratio 기준값이 작은 후보
    #
    # 왜 필요한가요?
    # 제조검사에서는 불량을 정상으로 통과시키는 FN을
    # 특히 중요하게 보기 때문입니다.
    #
    # 주의:
    # 현재 정렬 방식은 Accuracy 최대값보다
    # FN 최소화를 먼저 우선합니다.
    # --------------------------------------------------

    result_df = pd.DataFrame(
        rows
    )


    result_df = (
        result_df.sort_values(
            [
                "fn",
                "total_error",
                "fp",
                "sift_good_matches_min",
                "inlier_ratio_min",
            ],
            ascending=[
                True,
                True,
                True,
                True,
                True,
            ],
        )
        .reset_index(drop=True)
    )


    # --------------------------------------------------
    # 10. Threshold 후보 평가 결과를 CSV로 저장
    #
    # 무엇을 하나요?
    # - 결과를 저장할 폴더를 생성합니다.
    # - 정렬된 모든 후보 Rule의 성능을 CSV로 저장합니다.
    # - 상위 15개 후보를 터미널에 출력합니다.
    #
    # 저장 파일:
    # reports/day05_rule_candidates.csv
    #
    # CSV에는 다음 값이 포함됩니다.
    #
    # SIFT Threshold
    # Inlier Ratio Threshold
    # Accuracy
    # TP / TN / FP / FN
    # Total Error
    #
    # 왜 필요한가요?
    # 여러 후보 Rule의 평가 결과를 나중에 다시
    # 확인하고 비교하기 위해서입니다.
    # --------------------------------------------------

    CANDIDATE_CSV.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    result_df.to_csv(
        CANDIDATE_CSV,
        index=False,
        encoding="utf-8-sig",
    )


    print()

    print("=" * 70)
    print("후보 Rule 상위 15개")
    print("=" * 70)


    print(
        result_df
        .head(15)
        .to_string(
            index=False
        )
    )


    print()

    print(
        "저장:",
        CANDIDATE_CSV
    )


    # --------------------------------------------------
    # 11. 정렬된 결과에서 첫 번째 Rule 후보 선택
    #
    # 무엇을 하나요?
    # - 정렬된 후보 중 첫 번째 행을 가져옵니다.
    # - 해당 후보의 SIFT Threshold를 확인합니다.
    # - Inlier Ratio Threshold를 확인합니다.
    # - Accuracy, FP, FN을 출력합니다.
    #
    # best:
    # 현재 정렬 기준에서 가장 위에 있는 후보
    #
    # best_sift:
    # 선택된 SIFT Good Match 기준값
    #
    # best_inlier:
    # 선택된 Inlier Ratio 기준값
    #
    # 왜 필요한가요?
    # 다음 실습에서 실제 사용할 Baseline Rule을
    # 결정할 때 검토할 후보를 확인하기 위해서입니다.
    #
    # 주의:
    # 이 후보는 Calibration 데이터에서 선택한 것입니다.
    # 새로운 Test 데이터에서의 성능까지 보장하지는 않습니다.
    # --------------------------------------------------

    best = result_df.iloc[0]


    best_sift = int(
        best["sift_good_matches_min"]
    )

    best_inlier = float(
        best["inlier_ratio_min"]
    )


    print()

    print("=" * 70)
    print("현재 가장 좋은 후보")
    print("=" * 70)

    print(
        "SIFT Good Match >=",
        best_sift
    )

    print(
        "Inlier Ratio >=",
        best_inlier
    )

    print(
        "Accuracy:",
        best["accuracy"]
    )

    print(
        "FP:",
        int(best["fp"])
    )

    print(
        "FN:",
        int(best["fn"])
    )


    # --------------------------------------------------
    # 12. SIFT와 Inlier Ratio의 OK/NG 분포 그래프 생성
    #
    # 무엇을 하나요?
    # - Calibration 이미지의 측정값을 X-Y 그래프로 표시합니다.
    # - 실제 OK와 NG를 서로 다른 모양으로 표시합니다.
    # - 선택된 Threshold를 세로선과 가로선으로 표시합니다.
    #
    # X축:
    # SIFT Good Match
    #
    # Y축:
    # Homography Inlier Ratio
    #
    # 원형(o):
    # 실제 OK 이미지
    #
    # X 모양(x):
    # 실제 NG 이미지
    #
    # 세로 점선:
    # SIFT Threshold
    #
    # 가로 점선:
    # Inlier Ratio Threshold
    #
    # 왜 필요한가요?
    # 정상과 불량의 측정값이
    # Threshold를 기준으로 어떻게 분포하는지
    # 눈으로 확인하기 위해서입니다.
    #
    # 현재 Rule에서는 두 기준을 모두 만족하는
    # 오른쪽 위 영역이 OK 판정 영역입니다.
    # --------------------------------------------------

    PLOT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    # 그래프 크기 설정
    plt.figure(
        figsize=(9, 6)
    )


    # --------------------------------------------------
    # 12-1. 실제 OK와 NG 측정값을 점으로 표시
    #
    # 무엇을 하나요?
    # - 실제 정답을 기준으로 OK와 NG를 분리합니다.
    # - SIFT 값을 X축에 표시합니다.
    # - Inlier Ratio를 Y축에 표시합니다.
    # - 각 점에 이미지 파일명을 표시합니다.
    #
    # plt.scatter():
    # 데이터의 위치를 점으로 표시하는 함수
    #
    # plt.annotate():
    # 점 옆에 설명이나 파일명을 표시하는 함수
    # --------------------------------------------------

    for actual, marker in [
        ("OK", "o"),
        ("NG", "x"),
    ]:

        subset = df[
            df["actual"] == actual
        ]


        plt.scatter(
            subset["sift_good_matches"],
            subset["inlier_ratio"],
            label=actual,
            marker=marker,
        )


        # 각 점에 이미지 파일명 표시
        for _, row in subset.iterrows():

            plt.annotate(
                row["file"],
                (
                    row["sift_good_matches"],
                    row["inlier_ratio"],
                ),
                xytext=(4, 4),
                textcoords="offset points",
                fontsize=8,
            )


    # --------------------------------------------------
    # 12-2. 선택된 SIFT Threshold를 세로선으로 표시
    #
    # plt.axvline():
    # X축의 특정 위치에 세로선을 그립니다.
    #
    # 예:
    # SIFT >= 129
    #
    # 129 이상인 점은 선의 오른쪽에 위치합니다.
    # --------------------------------------------------

    plt.axvline(
        best_sift,
        linestyle="--",
        label=(
            f"SIFT >= {best_sift}"
        ),
    )


    # --------------------------------------------------
    # 12-3. 선택된 Inlier Ratio Threshold를 가로선으로 표시
    #
    # plt.axhline():
    # Y축의 특정 위치에 가로선을 그립니다.
    #
    # 예:
    # Inlier Ratio >= 0.8664
    #
    # 0.8664 이상인 점은 선의 위쪽에 위치합니다.
    # --------------------------------------------------

    plt.axhline(
        best_inlier,
        linestyle="--",
        label=(
            f"Inlier >= {best_inlier:.4f}"
        ),
    )


    # --------------------------------------------------
    # 12-4. 그래프 제목과 축 이름 설정
    #
    # xlabel:
    # X축 이름
    #
    # ylabel:
    # Y축 이름
    #
    # title:
    # 그래프 제목
    #
    # legend:
    # OK, NG, Threshold 선의 범례 표시
    #
    # grid:
    # 측정값의 위치를 쉽게 확인할 수 있도록
    # 보조 격자선을 표시합니다.
    # --------------------------------------------------

    plt.xlabel(
        "SIFT Good Matches"
    )

    plt.ylabel(
        "Homography Inlier Ratio"
    )

    plt.title(
        "Day05 Calibration Distribution"
    )


    plt.legend()

    plt.grid(
        alpha=0.2
    )


    # --------------------------------------------------
    # 12-5. 분포 그래프를 PNG 파일로 저장
    #
    # plt.savefig():
    # 현재 그래프를 이미지 파일로 저장합니다.
    #
    # dpi=150:
    # 출력 이미지 해상도 설정
    #
    # bbox_inches="tight":
    # 그래프 주변의 불필요한 여백을 줄입니다.
    #
    # plt.close():
    # 그래프 작업이 끝난 후 리소스를 정리합니다.
    #
    # 저장 파일:
    # sift_inlier_distribution.png
    # --------------------------------------------------

    plt.savefig(
        PLOT_PATH,
        dpi=150,
        bbox_inches="tight",
    )


    plt.close()


    print()

    print(
        "분포 이미지:",
        PLOT_PATH
    )


# --------------------------------------------------
# 13. Python 파일을 직접 실행할 때 main() 호출
#
# 무엇을 하나요?
# - 현재 파일을 직접 실행했는지 확인합니다.
# - 직접 실행했다면 main() 함수를 호출합니다.
#
# 왜 필요한가요?
# 다른 Python 파일에서 이 코드를 import할 때
# Calibration 분석이 자동 실행되지 않도록 하기 위해서입니다.
#
# 실행 명령어:
# python src/35_day05_analyze_calibration.py
# --------------------------------------------------

if __name__ == "__main__":
    main()
```

코드가 길어 보이지만 실제로 하는 일은 그림에서 본 순서와 같습니다.

```
① CSV 읽기
        ↓
② OK / NG 측정값 확인
        ↓
③ SIFT Threshold 후보 생성
        +
   Inlier Ratio Threshold 후보 생성
        ↓
④ 두 후보를 여러 가지로 조합
        ↓
⑤ Calibration 12장에 하나씩 적용
        ↓
⑥ 실제 정답과 비교
        ↓
⑦ FP / FN 등 오류 계산
        ↓
⑧ 오류가 적은 후보를 위로 정렬
        ↓
⑨ CSV와 그래프로 저장
```
### 의사코드

```text
[1. Calibration 입력 CSV와 결과 저장 경로 설정]

Calibration 측정 결과 CSV 경로를 정한다.

reports/day05_calibration_measurements.csv

Threshold 후보 결과 CSV 경로를 정한다.

reports/day05_rule_candidates.csv

OK/NG 분포 그래프 저장 경로를 정한다.

outputs/day05/calibration/
sift_inlier_distribution.png

          ↓

[2. Threshold 후보값을 생성하는 함수]

make_candidates() 함수를 정의한다.

후보를 만들 측정값을 전달받는다.

측정값을 숫자로 변환한다.
숫자가 아닌 값과 빈 값을 제거한다.

          ↓

남은 측정값이 없다면
빈 리스트를 반환한다.

          ↓

측정값의 최소값과 최대값을 찾는다.

최소값과 최대값이 같으면
현재 값 하나만 후보로 사용한다.

          ↓

최소값과 최대값이 다르면
np.linspace()로 후보값 15개를 생성한다.

          ↓

SIFT처럼 정수 기준이면
후보를 정수로 반올림한다.

Inlier Ratio처럼 소수 기준이면
소수점 넷째 자리까지 반올림한다.

          ↓

중복값을 제거한다.
작은 값부터 정렬한다.

Threshold 후보 리스트를 반환한다.

          ↓

[3. 실제 정답과 프로그램 판정을 비교하는 함수]

classify_error() 함수를 정의한다.

실제 정답 actual을 전달받는다.
프로그램의 예측 predicted를 전달받는다.

          ↓

실제 NG이고 예측 NG이면
TP를 반환한다.

실제 OK이고 예측 OK이면
TN을 반환한다.

실제 OK인데 예측 NG이면
FP를 반환한다.

실제 NG인데 예측 OK이면
FN을 반환한다.

어느 조건에도 해당하지 않으면
UNKNOWN을 반환한다.

          ↓

[4. Calibration CSV를 읽고 데이터 수량 확인]

main() 함수에서 분석을 시작한다.

Calibration 측정 결과 CSV가 있는지 확인한다.

파일이 없으면 오류를 발생시킨다.

파일이 있다면 Pandas로 CSV를 읽는다.

          ↓

전체 Calibration 이미지 개수를 출력한다.

실제 OK 이미지 개수를 확인한다.
실제 NG 이미지 개수를 확인한다.

          ↓

[5. OK와 NG의 측정값 기본 통계 확인]

분석할 측정값 4개를 선택한다.

Template Score
SIFT Good Match
Homography Inlier
Inlier Ratio

          ↓

실제 정답을 기준으로
OK 그룹과 NG 그룹을 나눈다.

          ↓

각 그룹의 측정값에서
최소값을 계산한다.
평균값을 계산한다.
최대값을 계산한다.

          ↓

OK와 NG의 통계 결과를 출력한다.

          ↓

[6. SIFT와 Inlier Ratio의 Threshold 후보 생성]

make_candidates() 함수를 호출한다.

SIFT Good Match의
최소값과 최대값 사이에서
정수 Threshold 후보를 만든다.

          ↓

Inlier Ratio의
최소값과 최대값 사이에서
소수 Threshold 후보를 만든다.

          ↓

각 후보 리스트를 출력한다.

          ↓

[7. SIFT와 Inlier Ratio의 모든 Threshold 조합 시험]

평가 결과를 저장할 rows 리스트를 만든다.

SIFT Threshold 후보 하나를 선택한다.
Inlier Ratio Threshold 후보 하나를 선택한다.

          ↓

두 Threshold를 조합하여
임시 검사 Rule을 만든다.

          ↓

TP, TN, FP, FN을 0으로 초기화한다.

          ↓

[7-1. Calibration 이미지마다 임시 Rule 적용]

Calibration 이미지 12장을 하나씩 확인한다.

각 이미지의 저장된 측정값을 읽는다.

          ↓

Homography Found == 1

        AND

SIFT Good Match >= 현재 SIFT 후보값

        AND

Inlier Ratio >= 현재 Inlier 후보값

          ↓

세 조건을 모두 만족하면
Predicted = OK

하나라도 만족하지 않으면
Predicted = NG

          ↓

[7-2. 실제 정답과 임시 판정 비교]

classify_error() 함수를 호출한다.

실제 정답과 예측 결과를 비교한다.

          ↓

TP이면 TP 개수를 1 증가시킨다.
TN이면 TN 개수를 1 증가시킨다.
FP이면 FP 개수를 1 증가시킨다.
FN이면 FN 개수를 1 증가시킨다.

          ↓

아직 평가할 Calibration 이미지가 남아 있으면
7-1번으로 돌아가 같은 Rule을 적용한다.

전체 이미지의 평가가 끝나면
8번으로 이동한다.

          ↓

[8. 현재 Threshold 조합의 Accuracy와 오류 기록]

TP, TN, FP, FN을 모두 더한다.

전체 평가 이미지 개수를 계산한다.

          ↓

Accuracy =
(TP + TN) / 전체 이미지 개수

          ↓

Total Error =
FP + FN

          ↓

현재 SIFT Threshold를 기록한다.
현재 Inlier Ratio Threshold를 기록한다.

Accuracy를 기록한다.
TP / TN / FP / FN을 기록한다.
Total Error를 기록한다.

          ↓

현재 후보 Rule의 결과를
rows 리스트에 추가한다.

          ↓

시험하지 않은 Threshold 조합이 있다면
7번으로 돌아가 다음 조합을 시험한다.

모든 조합을 시험했다면
9번으로 이동한다.

          ↓

[9. Threshold 후보를 오류가 적은 순서로 정렬]

모든 후보의 평가 결과를
Pandas DataFrame으로 변환한다.

          ↓

다음 우선순위로 정렬한다.

1순위: FN이 적은 후보
2순위: 전체 오류가 적은 후보
3순위: FP가 적은 후보
4순위: SIFT 기준이 작은 후보
5순위: Inlier Ratio 기준이 작은 후보

          ↓

정렬된 후보 결과를 준비한다.

          ↓

[10. Threshold 후보 평가 결과를 CSV로 저장]

결과 저장 폴더를 준비한다.

정렬된 전체 후보 Rule 결과를
day05_rule_candidates.csv로 저장한다.

          ↓

후보 Rule 중 상위 15개를 선택한다.

각 후보의 다음 값을 출력한다.

SIFT Threshold
Inlier Ratio Threshold
Accuracy
TP / TN / FP / FN
Total Error

          ↓

CSV 저장 경로를 출력한다.

          ↓

[11. 정렬된 결과에서 첫 번째 Rule 후보 선택]

정렬된 후보 결과의 첫 번째 행을 읽는다.

          ↓

SIFT Threshold를 가져온다.
Inlier Ratio Threshold를 가져온다.

          ↓

선택한 후보의 Accuracy를 출력한다.
FP 개수를 출력한다.
FN 개수를 출력한다.

          ↓

현재 Calibration에서 우선 검토할
Rule 후보를 확인한다.

          ↓

[12. SIFT와 Inlier Ratio의 OK/NG 분포 그래프 생성]

분포 그래프 저장 폴더를 준비한다.

9 × 6 크기의 그래프를 만든다.

          ↓

[12-1. 실제 OK와 NG 측정값을 점으로 표시]

실제 OK 데이터와 NG 데이터를 분리한다.

X축에는 SIFT Good Match를 사용한다.
Y축에는 Inlier Ratio를 사용한다.

OK 이미지는 원형 점으로 표시한다.
NG 이미지는 X 모양으로 표시한다.

각 점 옆에 이미지 파일명을 표시한다.

          ↓

[12-2. SIFT Threshold를 세로선으로 표시]

선택된 SIFT 기준값을 가져온다.

해당 위치에 세로 점선을 그린다.

          ↓

[12-3. Inlier Ratio Threshold를 가로선으로 표시]

선택된 Inlier Ratio 기준값을 가져온다.

해당 위치에 가로 점선을 그린다.

          ↓

[12-4. 그래프 제목과 축 이름 설정]

X축 이름을 작성한다.
Y축 이름을 작성한다.

그래프 제목을 작성한다.
OK/NG 및 Threshold 범례를 표시한다.

보조 격자선을 표시한다.

          ↓

[12-5. 분포 그래프를 PNG로 저장]

완성한 그래프를
sift_inlier_distribution.png로 저장한다.

그래프 리소스를 정리한다.
저장 경로를 출력한다.

          ↓

[13. 프로그램 실행]

Python 파일을 직접 실행하면
main() 함수를 호출한다.

          ↓

[최종 결과]

Calibration 측정 결과 CSV
OK 6장 + NG 6장
        ↓
OK / NG 측정값 통계 확인
        ↓
SIFT Threshold 후보 생성
        +
Inlier Ratio Threshold 후보 생성
        ↓
여러 Threshold 조합 만들기
        ↓
Calibration 12장에 각 Rule 적용
        ↓
실제 정답과 비교
        ↓
TP / TN / FP / FN 계산
        ↓
Accuracy / Total Error 계산
        ↓
오류가 적은 후보 순서로 정렬
        ↓
첫 번째 Rule 후보 확인
        ↓
┌──────────────────────────────┐
│ 결과 1                        │
│ day05_rule_candidates.csv    │
│ Threshold 후보별 평가 결과     │
└──────────────────────────────┘
        +
┌──────────────────────────────┐
│ 결과 2                        │
│ sift_inlier_distribution.png │
│ OK/NG 측정값 분포 그래프        │
└──────────────────────────────┘
        ↓
다음 실습에서 사용할
Baseline Rule 결정
        ↓
JSON 저장 및 Rule Freeze
```

실행합니다.

```bash
python src/35_day05_analyze_calibration.py
```

결과는 다음 두 파일입니다.

```text
reports/day05_rule_candidates.csv
outputs/day05/calibration/sift_inlier_distribution.png
```

---
## 19.5 실행 결과

vscode 터미널 결과

```
======================================================================
Calibration 데이터
======================================================================
전체 이미지: 12
actual
OK    6
NG    6
Name: count, dtype: int64

======================================================================
OK / NG 측정값 통계
======================================================================
       template_score                      ... inlier_ratio                    
                  min      mean       max  ...          min      mean       max
actual                                     ...                                 
NG           0.442885  0.496935  0.536214  ...     0.773050  0.853389  0.952381
OK           0.425379  0.509216  0.556364  ...     0.810811  0.903895  0.959770

[2 rows x 12 columns]

SIFT Threshold 후보:
[74, 82, 90, 98, 105, 113, 121, 129, 137, 145, 153, 160, 168, 176, 184]

Inlier Ratio Threshold 후보:
[0.7731, 0.7864, 0.7997, 0.8131, 0.8264, 0.8397, 0.8531, 0.8664, 0.8797, 0.8931, 0.9064, 0.9198, 0.9331, 0.9464, 0.9598]

======================================================================
후보 Rule 상위 15개
======================================================================
 sift_good_matches_min  inlier_ratio_min  accuracy  tp  tn  fp  fn  total_error
                   129            0.8664    0.9167   6   5   1   0            1
                   129            0.8797    0.9167   6   5   1   0            1
                   137            0.8664    0.9167   6   5   1   0            1
                   137            0.8797    0.9167   6   5   1   0            1
                   145            0.8664    0.9167   6   5   1   0            1
                   145            0.8797    0.9167   6   5   1   0            1
                   129            0.8931    0.8333   6   4   2   0            2
                   129            0.9064    0.8333   6   4   2   0            2
                   137            0.8931    0.8333   6   4   2   0            2
                   137            0.9064    0.8333   6   4   2   0            2
                   145            0.8931    0.8333   6   4   2   0            2
                   145            0.9064    0.8333   6   4   2   0            2
                   153            0.8664    0.8333   6   4   2   0            2
                   153            0.8797    0.8333   6   4   2   0            2
                   160            0.8664    0.8333   6   4   2   0            2

저장: reports/day05_rule_candidates.csv

======================================================================
현재 가장 좋은 후보
======================================================================
SIFT Good Match >= 129
Inlier Ratio >= 0.8664
Accuracy: 0.9167
FP: 1
FN: 0

분포 이미지: outputs/day05/calibration/sift_inlier_distribution.png
```

---

## 19.6 상위 Rule 후보를 확인합니다

프로그램을 실행한 결과 여러 Threshold 조합 중 가장 위에 나온 후보는 다음과 같습니다.

```
SIFT Good Match >= 129
Inlier Ratio >= 0.8664

Accuracy = 0.9167
FP = 1
FN = 0
```

쉽게 말하면 현재 후보 Rule은 다음과 같습니다.

```
SIFT Good Match가 129 이상
        AND
Inlier Ratio가 0.8664 이상
        ↓
OK

둘 중 하나라도 기준 미달
        ↓
NG
```

이 후보를 Calibration 이미지 12장에 적용한 결과:

```
12장 중 11장
→ 올바르게 판정

1장
→ 잘못 판정

Accuracy
→ 약 91.67%

FP = 1
→ 정상 1장을 NG로 잘못 판정

FN = 0
→ 불량을 OK로 통과시킨 경우 없음
```

이라는 결과가 나왔습니다.

즉 이번 분석에서는 **Calibration 데이터를 이용하여 OK와 NG를 비교적 잘 구분하는 Baseline Rule 후보를 찾은 것**입니다.

> 아직 최종 Rule로 확정한 것은 아닙니다. 다음 단계에서 이 후보의 결과를 확인한 뒤, 실제 Test에 사용할 Baseline Rule로 결정하고 동결합니다.
> 
---

# 20. 그래프에서 기준이 어떻게 나뉘는지 확인합니다

다음 그래프가 만들어졌습니다.

```
outputs/day05/calibration/sift_inlier_distribution.png
```

![[Pasted image 20260831163846.png]]

![[Pasted image 20261029075227.png]]

그래프는 Calibration 12장의 위치를 한눈에 보여줍니다.

```
X축
→ SIFT Good Match

Y축
→ Inlier Ratio

●
→ 실제 OK

×
→ 실제 NG
```

---
## 전체 과정을 한 번에 보면

![[Pasted image 20260831202603.png]]

![[Pasted image 20261029081318.png]]

![[Pasted image 20261029081528.png]]

35번 코드에 다음과 같이 작성되어 있습니다.

```python
sift_candidates = make_candidates(
    df["sift_good_matches"],
    count=15,
    integer=True,
)

inlier_candidates = make_candidates(
    df["inlier_ratio"],
    count=15,
    integer=False,
)
```

`count=15`는 각 측정값마다 기준 후보를 15개씩 만들라는 뜻입니다.

현재 우리의 실험에서는 12장의 이미지를 통해 후보를 결정하고 있지만 
실무에서는 이미지 장수보다 측정값이 얼마나 다양하게 분포하는지와 기준값을 얼마나 정밀하게 탐색할 필요가 있는지가 더 중요합니다.

수천 장의 데이터라면 처음에는 Threshold 후보를 15~30개 정도로 설정하여 탐색하고, 결과가 만족스럽지 않으면 후보를 더 촘촘하게 탐색하는 방법을 사용할 수 있습니다.

```
Calibration 측정값 CSV
        ↓
SIFT Threshold 후보 만들기
        +
Inlier Ratio Threshold 후보 만들기
        ↓
여러 조합 만들기
        ↓
Calibration 12장에 적용
        ↓
실제 OK / NG와 비교
        ↓
TP / TN / FP / FN 계산
        ↓
오류가 적은 후보 순서로 정렬
        ↓
좋은 Rule 후보 확인
```

---

두 개의 점선은 현재 선택된 기준 후보입니다.

```
세로선
→ SIFT = 129

가로선
→ Inlier Ratio = 0.8664
```

현재 Rule에서는:

```
세로선 오른쪽
        AND
가로선 위쪽
        ↓
OK
```

로 판단합니다.

즉 두 조건을 동시에 만족해야 정상입니다.

![[Pasted image 20260831205228.png]]

---

## 20.1 왜 두 조건을 같이 사용했나요?

그래프에서 `ng_01.jpg`를 보면:

```
SIFT Good Match = 126
Inlier Ratio = 0.9524
```

입니다.

Inlier Ratio는 높지만:

```
126 < 129
```

이므로 SIFT 기준을 통과하지 못합니다.

따라서:

```
SIFT → 실패
Inlier Ratio → 통과
        ↓
NG
```

가 됩니다.

반대로 `ng_04.jpg`는:

```
SIFT Good Match = 161
Inlier Ratio = 0.8634
```

입니다.

이번에는 SIFT는 통과하지만:

```
0.8634 < 0.8664
```

이므로 Inlier Ratio에서 실패합니다.

```
SIFT → 통과
Inlier Ratio → 실패
        ↓
NG
```

즉:

```
SIFT만 사용
→ ng_04가 통과할 수 있음

Inlier Ratio만 사용
→ ng_01이 통과할 수 있음

두 조건을 함께 사용
→ 둘 다 NG로 판정
```

할 수 있었습니다.

이것이 이번에 **복합 Rule을 사용하는 이유**입니다.

---

# 21. 한 장은 왜 잘못 판정되었나요?

현재 결과는:

```
FP = 1
FN = 0
```

입니다.

잘못 판정된 이미지는 `ok_06.jpg`입니다.

실제 측정값은:

```
ok_06.jpg

SIFT Good Match = 74
Inlier Ratio = 0.8108
```

현재 기준과 비교하면:

```
SIFT
74 < 129
→ 실패

Inlier Ratio
0.8108 < 0.8664
→ 실패
```

입니다.

따라서 프로그램은:

```
실제 상태
OK

        ↓

프로그램 판정
NG
```

로 판단했습니다.

즉 **정상 이미지를 불량으로 잘못 판정한 한 건**이 발생한 것입니다.

---

## 21.1 FP와 FN을 이번 결과로 이해합니다

이번 수업에서는 `NG`를 검출해야 할 대상으로 봅니다.

|실제 상태|프로그램 판정|구분|의미|
|---|---|---|---|
|NG|NG|TP|불량을 올바르게 검출|
|OK|OK|TN|정상을 올바르게 통과|
|OK|NG|FP|정상을 불량으로 잘못 판정|
|NG|OK|FN|불량을 정상으로 잘못 통과|

이번 결과는:

```
TP = 6
→ NG 6장을 모두 검출

TN = 5
→ OK 6장 중 5장을 정상 통과

FP = 1
→ 정상 1장을 NG로 잘못 판정

FN = 0
→ 불량을 OK로 통과시킨 경우 없음
```

입니다.

특히 제조검사에서는:

```
FN

실제 NG
→ 프로그램 OK
→ 불량품 통과
```

가 중요한 오류입니다.

이번 Calibration에서는:

```
FN = 0
```

이므로 준비한 NG 6장은 모두 잡아냈습니다.

---

# 22. 현재 후보 Rule을 정리합니다

이번 Calibration 분석에서 나온 첫 번째 후보는 다음과 같습니다.

```
Homography 계산 성공

        AND

SIFT Good Match >= 129

        AND

Inlier Ratio >= 0.8664

        ↓

OK
```

하나라도 조건을 만족하지 못하면:

```
NG
```

입니다.

쉽게 읽으면:

```
① 기준 로고와
   위치 관계를 계산할 수 있는가?

        ↓ YES

② 서로 비슷하게 연결된 특징점이
   129개 이상인가?

        ↓ YES

③ 그 특징점 중
   실제로 일관되게 맞는 비율이
   약 86.64% 이상인가?

        ↓ YES

        OK
```

---

## 22.1 `129`와 `0.8664`가 유일한 정답은 아닙니다

실제 출력 결과를 보면 다음과 같은 후보들도 있습니다.

```
129 / 0.8797
137 / 0.8664
137 / 0.8797
145 / 0.8664
145 / 0.8797
```

이 후보들도 모두:

```
Accuracy = 0.9167
FP = 1
FN = 0
```

으로 같은 결과를 냈습니다.

따라서:

```
129 / 0.8664
```

가 절대적인 정답이라는 뜻은 아닙니다.

여러 후보를 시험한 결과 현재 Calibration 12장에서는 비슷하게 잘 동작하는 기준이 여러 개 존재한다는 뜻입니다.

---

## 22.2 이번 실습에서 무엇을 한 건가요?

이번 단계의 핵심을 한 번만 정리하면 다음과 같습니다.

```
Calibration 이미지 12장 측정
        ↓
측정값 CSV 생성
        ↓
SIFT와 Inlier Ratio 분포 확인
        ↓
여러 Threshold 조합 시험
        ↓
실제 OK / NG와 비교
        ↓
오류가 적은 후보 확인
        ↓
현재 후보
SIFT >= 129
Inlier Ratio >= 0.8664
```

즉 이번 실습은:

> 실제 데이터를 이용하여 여러 기준을 시험해 보고, OK와 NG를 비교적 잘 구분하는 Rule 후보를 찾는 과정

이었습니다.

![[Pasted image 20260831205444.png]]

---

# PART4 실제 검사에 사용할 Baseline Rule로 결정하고 파일로 저장하는 단계 (23~25)

---

# 23. 후보 Rule을 실제 사용할 Baseline Rule로 결정합니다

앞에서는 Calibration 이미지 12장을 이용하여 여러 판정 기준을 시험했습니다.

그 결과 상위 후보 중 하나로 다음 기준을 찾았습니다.

```
Homography 계산 성공

     AND

SIFT Good Match >= 129

     AND

Inlier Ratio >= 0.8664
```

Calibration 12장에 적용했을 때:

```
Accuracy = 91.67%

FP = 1
FN = 0
```

의 결과가 나왔습니다.

지금까지는 이것을 **Rule 후보**라고 불렀습니다.

```
Calibration
        ↓
여러 Threshold 조합 시험
        ↓
성능 비교
        ↓
상위 Rule 후보 발견
```

이제 다음 단계로 넘어가기 위해 이 후보를 **첫 번째 Baseline Rule**로 선택합니다.

```
현재 후보

SIFT >= 129
Inlier Ratio >= 0.8664
        ↓
Baseline Rule로 선택
        ↓
다음 Test에서 사용할 기준
```

여기서 `Baseline Rule`은 쉽게 말하면:

> **앞으로 Test할 때 기준으로 사용할 첫 번째 검사 규칙**입니다.

---

## 23.1 왜 Rule을 파일로 저장할까요?

기준값을 Python 코드 안에 직접 작성할 수도 있습니다.

예를 들어:

```
if sift_good_matches >= 129:
```

처럼 사용할 수 있습니다.

하지만 이렇게 하면 검사 기준이 코드 안에 섞이게 됩니다.

5일차에서는 역할을 다음처럼 나눕니다.

```
Python 코드
→ 어떻게 검사할 것인가?

JSON 설정 파일
→ 어떤 기준값으로 판정할 것인가?
```

따라서 Baseline Rule은 다음 파일에 따로 저장합니다.

```
configs/day05_logo_rules.json
```

이렇게 해두면 이후 Test 프로그램은 Python 코드에 숫자를 다시 적지 않고 **JSON에 저장된 동일한 기준을 읽어서 사용**할 수 있습니다.

```
day05_logo_rules.json

SIFT >= 129
Inlier Ratio >= 0.8664
Homography 성공

        ↓

Test 프로그램이 읽음

        ↓

항상 같은 기준으로
OK / NG 판정
```

---

## 23.2 저장할 Baseline Rule을 다시 확인합니다

JSON에 저장할 첫 번째 Baseline Rule은 다음과 같습니다.

```
조건 1
Homography 계산 성공

        AND

조건 2
SIFT Good Match >= 129

        AND

조건 3
Inlier Ratio >= 0.8664

        ↓

세 조건 모두 만족
→ OK

하나라도 만족하지 못함
→ NG
```

이 Rule에는 버전 이름을 붙입니다.

```
day05-logo-v1.0
```

`v1.0`은 **현재 Calibration 결과를 바탕으로 처음 결정한 Baseline Rule 버전**이라는 의미입니다.

현재 상태를 정리하면:

```
Calibration 완료
        ↓
Rule 후보 비교 완료
        ↓
Baseline Rule 선택 완료
        ↓
아직 파일 저장 전
```

> 이제 다음 실습에서 이 Baseline Rule을 JSON 파일에 저장하여 **Rule Freeze를 완료**합니다.

---

# 24. `36_day05_freeze_rule.py` — 결정한 검사 기준을 JSON으로 저장합니다

앞의 35번 실습에서는 Calibration 이미지 12장을 이용하여 여러 Threshold 후보를 비교했습니다.

그 결과 다음 기준을 Baseline Rule로 선택했습니다.

|검사 항목|결정한 기준|의미|
|---|---|---|
|Homography Found|1 (성공)|로고의 위치 관계 계산에 성공해야 함|
|SIFT Good Match|129개 이상|비슷하게 연결된 특징점이 129개 이상이어야 함|
|Inlier Ratio|0.8664 이상|연결된 특징점 중 약 86.64% 이상이 위치 관계에 일치해야 함|

**세 조건을 모두 만족하면 OK, 하나라도 만족하지 못하면 NG**로 판정하기로 결정했습니다.

## 24.1 이번 코드는 무엇을 하나요?

지금까지는 검사 기준을 찾고 비교하는 과정이었습니다.

이제 결정한 기준을 나중에 다른 Python 프로그램에서도 사용할 수 있도록 **JSON 파일에 저장하고 고정(Freeze)**하겠습니다.

```
35번 코드
Calibration으로 Rule 후보 비교
             ↓
최종 Baseline Rule 결정
SIFT ≥ 129
Inlier Ratio ≥ 0.8664
Homography 계산 성공
             ↓
36_day05_freeze_rule.py
             ↓
JSON 파일로 저장
configs/day05_logo_rules.json
             ↓
Rule 버전 기록
day05-logo-v1.0
             ↓
Rule Freeze 완료
```

여기서 **Freeze(동결)**란 결정한 검사 기준을 이후 Test 과정에서 임의로 변경하지 않고 그대로 사용한다는 뜻입니다.

`day05-logo-v1.0`은 이번에 결정한 검사 기준의 버전 이름입니다. 나중에 기준을 변경한다면 기존 버전과 구분할 수 있습니다.

## 24.2 JSON 파일로 저장하는 이유는 무엇인가요?

검사 기준을 Python 코드마다 다시 작성하면 숫자를 잘못 입력하거나 서로 다른 기준을 사용하는 문제가 생길 수 있습니다.

따라서 검사 기준을 별도의 JSON 파일에 저장하면 이후 37번 Test 코드에서 **동일한 기준을 불러와 사용할 수 있습니다.**

이번 36번 코드에서는 이미 선택한 기준값을 직접 지정하여 JSON으로 저장합니다. Threshold를 다시 탐색하지 않습니다.

또한 **36번은 이미지 검사나 성능 평가를 하는 코드가 아닙니다.** 실제로 새로운 Test 이미지 6장을 검사하는 것은 37번, 검사 성능을 평가하는 것은 38번에서 진행합니다.

## 24.3 Python 파일을 만들겠습니다

프로젝트의 `src` 폴더에 다음 파일을 생성합니다.

```
src/36_day05_freeze_rule.py
```

이제 아래 Python 코드를 작성하여 결정한 Baseline Rule을 JSON 파일로 저장하겠습니다.

```python
from pathlib import Path
import json


# --------------------------------------------------
# 1. Baseline Rule을 저장할 JSON 파일 경로 설정
#
# 무엇을 하나요?
# - Calibration에서 결정한 검사 기준을
#   저장할 JSON 파일의 위치를 지정합니다.
#
# 저장할 파일:
# configs/day05_logo_rules.json
#
# JSON이란?
# 데이터를 Key와 Value 형태로 저장하는 파일 형식입니다.
#
# 왜 필요한가요?
# 검사 기준값을 Python 코드와 분리하여
# 다음 Test 프로그램에서도 동일한 기준을
# 읽어 사용할 수 있도록 하기 위해서입니다.
# --------------------------------------------------

OUTPUT_PATH = Path(
    "configs/day05_logo_rules.json"
)


# --------------------------------------------------
# 2. Calibration 분석에서 선택한 Threshold 준비
#
# 무엇을 하나요?
# - 앞에서 분석한 Calibration 결과를 바탕으로
#   사용할 두 가지 Threshold를 지정합니다.
#
# SIFT_GOOD_MATCHES_MIN = 129
# → SIFT Good Match가 129개 이상이어야 합니다.
#
# INLIER_RATIO_MIN = 0.8664
# → Inlier Ratio가 0.8664 이상이어야 합니다.
#
# 왜 필요한가요?
# 실제 검사에서 어느 정도의 측정값을
# 정상(OK) 기준으로 사용할지 정하기 위해서입니다.
#
# 주의:
# 이 값은 모든 로고에 적용되는 정답이 아닙니다.
# 이번 광천김 Calibration 데이터를 이용하여
# 선택한 Baseline Threshold입니다.
#
# 이 코드는 Threshold를 다시 계산하지 않고
# 앞에서 선택한 값을 그대로 사용합니다.
# --------------------------------------------------

SIFT_GOOD_MATCHES_MIN = 129

INLIER_RATIO_MIN = 0.8664


# --------------------------------------------------
# 3. Baseline Rule 정보를 딕셔너리로 구성
#
# 무엇을 하나요?
# - main() 함수를 정의합니다.
# - 검사 기준에 필요한 정보를 하나로 정리합니다.
# - Python 딕셔너리 형태로 rules를 만듭니다.
#
# 저장할 주요 정보:
#
# ① Baseline Rule 버전
# ② 검사 대상
# ③ Positive Class
# ④ Reference 이미지 경로
# ⑤ 실제 OK/NG 판정 조건
# ⑥ Calibration 평가 결과
#
# 왜 필요한가요?
# 이후 Test 프로그램이 어떤 기준으로
# 검사해야 하는지 알 수 있도록
# 관련 정보를 함께 저장하기 위해서입니다.
# --------------------------------------------------

def main():

    rules = {

        # ----------------------------------------------
        # 3-1. Rule 버전 기록
        #
        # baseline_version:
        # 현재 Baseline Rule의 버전 이름입니다.
        #
        # day05-logo-v1.0:
        # 5일차에 처음 확정한 로고 검사 기준이라는 뜻입니다.
        #
        # 버전명을 기록하면 이후 개선된 Rule과
        # 기존 Rule을 구분할 수 있습니다.
        # ----------------------------------------------

        "baseline_version": "day05-logo-v1.0",


        # ----------------------------------------------
        # 3-2. 검사 대상 기록
        #
        # inspection_target:
        # 어떤 제품의 무엇을 검사하는지 기록합니다.
        #
        # 이번 실습:
        # 광천김 포장지의 로고가 기준 로고와
        # 충분히 일치하는지 검사합니다.
        # ----------------------------------------------

        "inspection_target":
            "광천김 로고 존재 및 정합 검사",


        # ----------------------------------------------
        # 3-3. Positive Class 정의
        #
        # positive_class = NG
        #
        # 제조검사에서는 불량을 찾아내는 것이 중요하므로
        # 이번 실습에서는 NG를 Positive로 정의합니다.
        #
        # 이 설정은 이후 성능 평가에서
        # TP / TN / FP / FN을 해석할 때 사용합니다.
        #
        # 예:
        # TP = 실제 NG를 NG로 올바르게 검출
        # FN = 실제 NG를 OK로 잘못 통과
        # ----------------------------------------------

        "positive_class": "NG",


        # ----------------------------------------------
        # 3-4. 검사에 사용할 Reference 이미지 경로
        #
        # 무엇을 하나요?
        # - 비교 기준이 되는 광천김 로고 경로를 저장합니다.
        #
        # 왜 필요한가요?
        # 이후 Test 프로그램이 같은 Reference를
        # 사용하도록 하기 위해서입니다.
        # ----------------------------------------------

        "reference": {
            "reference_label":
                "samples/day04/reference/reference_label.jpg"
        },


        # ----------------------------------------------
        # 3-5. 실제 OK / NG 판정에 사용할 복합 Rule 저장
        #
        # 무엇을 하나요?
        # - Homography 성공 여부를 검사 조건으로 정합니다.
        # - SIFT Good Match의 최소 기준을 정합니다.
        # - Inlier Ratio의 최소 기준을 정합니다.
        #
        # 판정 조건:
        #
        # Homography 계산 성공
        #          AND
        # SIFT Good Match >= 129
        #          AND
        # Inlier Ratio >= 0.8664
        #
        # 세 조건을 모두 만족하면 OK
        # 하나라도 만족하지 않으면 NG
        #
        # 왜 복합 Rule을 사용하나요?
        # SIFT Match 개수나 Inlier Ratio 한 가지만으로는
        # 정상과 불량을 충분히 구분하기 어려웠기 때문입니다.
        #
        # 주의:
        # 이 코드는 Rule을 저장하는 역할만 합니다.
        # 실제 판정은 다음 Test 프로그램에서 수행합니다.
        # ----------------------------------------------

        "required_rules": {

            "homography_found":
                True,

            "sift_good_matches_min":
                SIFT_GOOD_MATCHES_MIN,

            "inlier_ratio_min":
                INLIER_RATIO_MIN,
        },


        # ----------------------------------------------
        # 3-6. Calibration에서 얻은 평가 결과 기록
        #
        # 무엇을 하나요?
        # - 앞에서 선택한 Rule 후보의 성능을 저장합니다.
        #
        # accuracy = 0.9167
        # → Calibration 12장 중 11장 정답
        # → 약 91.67%
        #
        # fp = 1
        # → 실제 OK 1장을 NG로 잘못 판정
        #
        # fn = 0
        # → Calibration에서 NG를 OK로
        #   잘못 통과시킨 경우 없음
        #
        # 왜 필요한가요?
        # 이 Rule이 어떤 Calibration 결과를
        # 바탕으로 결정되었는지 기록하기 위해서입니다.
        #
        # 주의:
        # 이 값들은 앞선 분석에서 얻은 결과를
        # 직접 기록한 것입니다.
        # 현재 코드에서 다시 계산하지 않습니다.
        # ----------------------------------------------

        "calibration_result": {

            "accuracy":
                0.9167,

            "fp":
                1,

            "fn":
                0,
        },


        # ----------------------------------------------
        # 3-7. Rule에 대한 설명 기록
        #
        # 현재 Rule이 어떤 목적으로 만들어졌는지
        # 사람이 이해할 수 있도록 설명을 남깁니다.
        # ----------------------------------------------

        "note":
            "Calibration 결과로 결정한 Day05 Baseline Rule"
    }


    # --------------------------------------------------
    # 4. JSON 파일을 저장할 폴더 생성
    #
    # 무엇을 하나요?
    # - OUTPUT_PATH의 상위 폴더를 확인합니다.
    # - configs 폴더가 없으면 새로 만듭니다.
    #
    # parents=True:
    # 필요한 상위 폴더까지 함께 생성합니다.
    #
    # exist_ok=True:
    # 폴더가 이미 있어도 오류를 발생시키지 않습니다.
    #
    # 왜 필요한가요?
    # JSON을 저장할 폴더가 존재하지 않으면
    # 파일 저장 과정에서 오류가 발생할 수 있기 때문입니다.
    # --------------------------------------------------

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # --------------------------------------------------
    # 5. Baseline Rule을 JSON 파일로 저장
    #
    # 무엇을 하나요?
    # - 앞에서 만든 rules 딕셔너리를 JSON으로 저장합니다.
    #
    # OUTPUT_PATH.open("w"):
    # JSON 파일을 쓰기 모드로 엽니다.
    #
    # json.dump():
    # Python 딕셔너리를 JSON 파일로 저장합니다.
    #
    # ensure_ascii=False:
    # 한글을 읽을 수 있는 형태로 저장합니다.
    #
    # indent=2:
    # 들여쓰기를 적용하여 읽기 쉽게 저장합니다.
    #
    # 저장 파일:
    # configs/day05_logo_rules.json
    #
    # 왜 필요한가요?
    # 이후 Test 프로그램이 동일한 Baseline Rule을
    # 불러와 검사에 사용하도록 하기 위해서입니다.
    #
    # 주의:
    # "w" 모드이므로 파일이 이미 있으면 덮어씁니다.
    # Rule Freeze는 기준을 고정해 사용한다는 운영 원칙이며,
    # 파일 자체가 수정 불가능해지는 것은 아닙니다.
    # --------------------------------------------------

    with OUTPUT_PATH.open(
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            rules,
            file,
            ensure_ascii=False,
            indent=2
        )


    # --------------------------------------------------
    # 6. Rule 저장 완료 메시지와 JSON 내용 출력
    #
    # 무엇을 하나요?
    # - Baseline Rule 저장 완료 메시지를 출력합니다.
    # - JSON 저장 위치를 출력합니다.
    # - 실제 저장한 Rule 정보를 터미널에 표시합니다.
    #
    # json.dumps():
    # Python 딕셔너리를 JSON 문자열로 변환합니다.
    #
    # json.dump()와 json.dumps() 차이:
    #
    # json.dump():
    # → JSON 내용을 파일에 저장
    #
    # json.dumps():
    # → JSON 문자열을 생성
    #
    # 왜 필요한가요?
    # 학생들이 저장한 기준값과 버전이
    # 올바른지 직접 확인하기 위해서입니다.
    # --------------------------------------------------

    print("=" * 70)

    print(
        "Rule 동결 완료"
    )

    print("=" * 70)

    print(
        "저장:",
        OUTPUT_PATH
    )

    print()

    print(
        json.dumps(
            rules,
            ensure_ascii=False,
            indent=2
        )
    )


# --------------------------------------------------
# 7. Python 파일을 직접 실행하면 main() 호출
#
# 무엇을 하나요?
# - 현재 파일이 직접 실행되었는지 확인합니다.
# - 직접 실행한 경우 main()을 호출합니다.
#
# 왜 필요한가요?
# 다른 Python 파일에서 이 코드를 import할 때
# JSON 저장 작업이 자동으로 실행되지 않도록
# 구분하기 위해서입니다.
#
# 실행 명령어:
# python src/36_day05_freeze_rule.py
# --------------------------------------------------

if __name__ == "__main__":
    main()
```
### 의사코드

```
[1. Baseline Rule을 저장할 JSON 파일 경로 설정]

검사 기준을 저장할 경로를 정한다.

configs/day05_logo_rules.json

이 파일에 Calibration에서 결정한
판정 기준을 저장할 준비를 한다.

          ↓

[2. Calibration 분석에서 선택한 Threshold 준비]

앞에서 선택한 SIFT 기준값을 준비한다.

SIFT Good Match >= 129

          ↓

앞에서 선택한 Inlier Ratio 기준값을 준비한다.

Inlier Ratio >= 0.8664

          ↓

이 두 기준값을 변수에 저장한다.

          ↓

[3. Baseline Rule 정보를 딕셔너리로 구성]

main() 함수를 만든다.

검사 기준을 저장할
rules 딕셔너리를 만든다.

          ↓

[3-1. Rule 버전 기록]

Baseline Rule의 버전 이름을 정한다.

day05-logo-v1.0

          ↓

[3-2. 검사 대상 기록]

무엇을 검사하는지 기록한다.

광천김 로고 존재 및 정합 검사

          ↓

[3-3. Positive Class 정의]

이번 제조검사에서는
불량을 찾아내는 것이 중요하므로

Positive Class = NG

로 기록한다.

          ↓

[3-4. Reference 이미지 경로 기록]

검사에 사용할 기준 로고 경로를 저장한다.

samples/day04/reference/reference_label.jpg

          ↓

[3-5. OK / NG 판정에 사용할 복합 Rule 저장]

첫 번째 조건을 기록한다.

Homography 계산 성공

          AND

두 번째 조건을 기록한다.

SIFT Good Match >= 129

          AND

세 번째 조건을 기록한다.

Inlier Ratio >= 0.8664

          ↓

세 조건을 모두 만족하면 OK

하나라도 만족하지 않으면 NG

          ↓

이 판정 기준을
required_rules에 저장한다.

          ↓

[3-6. Calibration 평가 결과 기록]

앞에서 측정한 Calibration 결과를 기록한다.

Accuracy = 0.9167

FP = 1

FN = 0

          ↓

현재 Baseline Rule이
어떤 결과를 바탕으로 선택되었는지 기록한다.

          ↓

[3-7. Rule 설명 기록]

현재 Rule이 Calibration 분석으로
결정된 Baseline Rule임을 설명하는
문장을 저장한다.

          ↓

[4. JSON 파일을 저장할 폴더 생성]

configs 폴더가 있는지 확인한다.

폴더가 없다면 새로 만든다.

폴더가 이미 있다면 그대로 사용한다.

          ↓

[5. Baseline Rule을 JSON 파일로 저장]

day05_logo_rules.json 파일을
쓰기 모드로 연다.

          ↓

rules 딕셔너리를 JSON으로 변환한다.

한글을 읽을 수 있도록 저장한다.
들여쓰기를 적용한다.

          ↓

JSON 파일에 Baseline Rule을 저장한다.

          ↓

[6. Rule 저장 완료 메시지와 JSON 내용 출력]

Rule 동결 완료 메시지를 출력한다.

JSON 저장 경로를 출력한다.

          ↓

저장한 Rule의 내용을 출력한다.

Baseline 버전
검사 대상
Positive Class
Reference 경로
Required Rules
Calibration 결과
설명

          ↓

[7. Python 파일을 직접 실행하면 main() 호출]

현재 Python 파일을 직접 실행했는지 확인한다.

직접 실행했다면
main() 함수를 호출한다.

          ↓

[최종 결과]

Calibration 분석 결과
        ↓
SIFT Good Match >= 129
        +
Inlier Ratio >= 0.8664
        +
Homography 계산 성공
        ↓
Baseline Rule 결정
        ↓
rules 딕셔너리 생성
        ↓
JSON 파일로 저장
        ↓
configs/day05_logo_rules.json
        ↓
Baseline Rule 버전
day05-logo-v1.0
        ↓
다음 실습
37_day05_test.py
        ↓
처음 보는 Test 이미지 6장에
동일한 판정 기준 적용
        ↓
OK / NG 판정 및 성능 확인
```

코드를 실행합니다

```
python src/36_day05_freeze_rule.py
```

실행 결과

```
======================================================================
Rule 동결 완료
======================================================================
저장: configs/day05_logo_rules.json
```

이 출력됩니다.

그리고 다음 파일이 생성됩니다.

```
configs/
└── day05_logo_rules.json
```

---

## 24.1 만들어진 JSON을 확인합니다

다음 파일을 엽니다.

```
configs/day05_logo_rules.json
```

다음과 같은 내용이 저장되어 있어야 합니다.

```json
{
  "baseline_version": "day05-logo-v1.0",
  "inspection_target": "광천김 로고 존재 및 정합 검사",
  "positive_class": "NG",
  "reference": {
    "reference_label": "samples/day04/reference/reference_label.jpg"
  },
  "required_rules": {
    "homography_found": true,
    "sift_good_matches_min": 129,
    "inlier_ratio_min": 0.8664
  },
  "calibration_result": {
    "accuracy": 0.9167,
    "fp": 1,
    "fn": 0
  },
  "note": "Calibration 결과로 결정한 Day05 Baseline Rule"
}
```

여기서 가장 중요한 부분은 다음 세 가지입니다.

```
homography_found = true

sift_good_matches_min = 129

inlier_ratio_min = 0.8664
```

앞으로 검사 프로그램은 이 값을 읽어서:

```
Homography 성공?
        AND
SIFT >= 129?
        AND
Inlier Ratio >= 0.8664?
        ↓
OK / NG
```

를 판단하게 됩니다.

---

### 실제 산업현장에서 사용하는 AI 검사 시스템의 데이터 수집 → 추론 → 분석 → 성능 개선 구조

```
[1] 실시간 카메라 영상 수집
           ↓
[2] OpenCV 이미지 전처리
           ↓
[3] 검사 기준 JSON 불러오기
    SIFT ≥ 129 / Ratio ≥ 0.8664
           ↓
[4] Rule 기반 판정 또는 AI 추론
           ↓
       OK / NG 판정
           ↓
[5] 결과 저장 및 대시보드 표시
           ↓
[6] NG 이미지와 검사 수치 축적
           ↓
[7] Lakehouse에서 데이터 분석
    Raw → 정제 → 분석용 데이터
           ↓
[8] 오판정·새로운 불량 유형 분석
           ↓
[9] Threshold 개선 또는 AI 재학습
           ↓
[10] 새 기준의 성능 검증
           ↓
[11] 새로운 Rule JSON / AI 모델 배포
           ↓
    실시간 검사에 다시 적용
           ↺
```

실제로는 실시간 검사와 Lakehouse 저장을 병렬로 처리하는 것이 좋습니다. 즉, Raw 데이터를 Lakehouse에 저장하는 동안 실시간 판정은 별도로 빠르게 수행하고, 이미지·판정 결과·측정값을 함께 축적합니다.

### 핵심 파일의 역할

| 구성 요소          | 역할                    |
| -------------- | --------------------- |
| `rules.json`   | 현재 적용할 검사 기준과 버전 저장   |
| Raw Data       | 카메라 원본 이미지·영상 보존      |
| Lakehouse      | 원본·정제·검사 결과 데이터 통합 관리 |
| AI / OpenCV    | 실제 OK/NG 추론 및 판정      |
| NG 데이터         | 불량 유형과 판정 오류 분석에 활용   |
| 새 Rule / AI 모델 | 검증 후 개선된 기준으로 교체      |

우리가 최종 목표로 하는 시스넴은 다음 흐름과 같습니다.

```
제품이 컨베이어벨트에서 카메라 앞을 지나가면 자동 촬영 
→ 원본 이미지 및 촬영 정보 수집 → 원본 데이터 저장(Bronze·Raw Data) 
→ 제품 영역 검출 및 이미지 전처리 
→ OpenCV/AI 특징값 분석 
→ JSON 검사 기준 적용 
→ OK/NG 자동 판정 
→ 검사 결과 및 측정값 저장 
→ 원본과 검사 결과 연결·정제(Silver) 
→ 검사량·불량률 등 분석용 데이터 집계(Gold·Data Mart) 
→ 실시간 대시보드 표시 
→ NG 데이터 분석 및 오판정 확인 
→ 검사 Rule/AI 모델 개선 
→ 성능 검증 후 새로운 버전 적용까지 자동화하는 시스템입니다.
```

핵심: 원본 데이터 저장과 실시간 검사는 병렬로 진행하며, NG 분석 후 검사 기준 변경은 검증과 승인을 거쳐 적용합니다.

![[Pasted image 20261029084845.png]]

---

# 25. 왜 이것을 `Freeze`라고 하나요?

지금까지는 Calibration 데이터를 보면서 기준을 찾는 과정이었습니다.

```
Calibration
        ↓
측정
        ↓
값 비교
        ↓
여러 후보 시험
        ↓
Rule 선택
```

여기까지는 기준값을 바꾸어도 됩니다.

하지만 이제:

```
day05_logo_rules.json
```

으로 기준을 저장했습니다.

이 시점부터는 이 기준을 **Baseline Rule**로 사용합니다.

```
Calibration 종료
        ↓
Rule 결정

SIFT >= 129
Inlier Ratio >= 0.8664
        ↓
JSON 저장
        ↓
day05-logo-v1.0
```

이 상태를 Rule Freeze라고 합니다.

쉽게 말하면:

> Calibration에서 기준을 정하는 작업은 끝났고, 이제부터는 같은 기준을 사용한다는 뜻입니다.

---

## 25.1 왜 기준을 고정해야 하나요?

앞으로 새로운 데이터를 검사했는데 결과가 마음에 들지 않는다고 기준을 계속 바꾸면 문제가 생깁니다.

예를 들어:

```
새 이미지 검사
        ↓
틀림
        ↓
Threshold 수정
        ↓
다시 검사
        ↓
또 틀림
        ↓
Threshold 또 수정
```

을 반복하면 우리가 만든 Rule이 실제 새로운 데이터에서도 잘 작동하는지 알 수 없습니다.

따라서:

```
Calibration
→ 기준을 만드는 데이터

Rule Freeze
→ 기준 확정

이후 새로운 데이터
→ 확정한 기준으로 검사
```

순서를 지킵니다.

---

## 25.2 지금까지의 흐름을 정리합니다

5일차의 흐름이 여기서 한 단계 완성됩니다.

![[Pasted image 20260831211034.png]]

```
광천김 Calibration 12장
        ↓
Template / SIFT / Homography 측정
        ↓
측정값 CSV
        ↓
OK / NG 분포 비교
        ↓
Threshold 후보 여러 개 시험
        ↓
후보 Rule 비교
        ↓
선택

SIFT >= 129
Inlier Ratio >= 0.8664
        ↓
JSON 저장
        ↓
Baseline Rule
day05-logo-v1.0
```

즉 이번 실습에서 한 것은:

> 앞에서 데이터로 찾아낸 판정 기준을 코드 속 임시 숫자로 두지 않고, 이후에도 동일하게 사용할 수 있도록 JSON 설정 파일로 저장한 것입니다.

---
# PART5 **Test** — 처음 보는 6장에 Rule 적용 (26~28)

---
# 26. 동결한 Rule을 처음 보는 Test 이미지에 적용합니다

Calibration 단계에서는 12장의 데이터를 이용하여 판정 기준을 만들었습니다.

현재 선택한 기준은 다음과 같습니다.

```
Homography 계산 성공

AND

SIFT Good Match >= 129

AND

Inlier Ratio >= 0.8664

        ↓

OK
```

그리고 이 기준을 다음 파일에 저장했습니다.

```
configs/day05_logo_rules.json
```

이제부터는 기준을 만드는 작업이 아니라, 만들어 놓은 기준이 새로운 이미지에서도 잘 작동하는지 확인하는 작업입니다.

이를 `Test`라고 합니다.

---

## 26.1 이번 Test에서는 무엇을 하나요?

앞에서 따로 준비해 둔 Test 이미지 6장을 사용합니다.

```
samples/day05/resized/

test_ok_01.jpg
test_ok_02.jpg
test_ok_03.jpg

test_ng_01.jpg
test_ng_02.jpg
test_ng_03.jpg
```

이 6장은 Calibration 기준을 결정할 때 사용하지 않았습니다.

따라서 다음 순서로 검사합니다.

```
동결한 Rule JSON
        +
Test 이미지 한 장
        ↓
4일차와 같은 방법으로 측정
        ↓
SIFT Good Match
Inlier Ratio
Homography Found
        ↓
JSON의 기준값과 비교
        ↓
Predicted
OK / NG
        ↓
사람이 알고 있는 실제 정답과 비교
```

예를 들어:

```
test_ok_01.jpg

실제 정답
→ OK

프로그램 판정
→ ?

두 결과를 비교
```

합니다.

> Test의 목적은 기준을 다시 찾는 것이 아니라, Calibration에서 정한 기준이 새로운 데이터에서도 잘 작동하는지 확인하는 것입니다.

---

## 26.2 Test에서는 기준을 바꾸지 않습니다

Test를 하면서 결과가 마음에 들지 않아도 다음 값은 그대로 사용합니다.

```
SIFT >= 129

Inlier Ratio >= 0.8664
```

즉:

```
Test 결과가 틀림
        ↓
Threshold 바로 수정 X

먼저
왜 틀렸는지 분석
```

합니다.

이렇게 해야 현재 Rule의 실제 성능을 알 수 있습니다.

---

## 26.3 `37_day05_test.py` — Test 데이터 6장을 검사합니다

파일을 만듭니다.

```
src/37_day05_test.py
```

다음 코드를 작성합니다.

```python
from pathlib import Path
import csv
import json

import cv2
import numpy as np

# 앞에서 만든 공통 측정 함수
#
# prepare_reference():
# 기준 로고의 특징점을 준비합니다.
#
# measure_target():
# 이미지 한 장의 Template, SIFT, Homography
# 측정값을 계산합니다.

from day05_logo_features import (
    prepare_reference,
    measure_target,
)


# --------------------------------------------------
# 1. Rule JSON, Test 이미지 및 결과 저장 경로 설정
#
# 무엇을 하나요?
# - 동결한 Baseline Rule JSON 경로를 지정합니다.
# - Test 이미지가 있는 폴더를 지정합니다.
# - 검사 결과 이미지와 CSV의 저장 경로를 정합니다.
#
# RULE_PATH:
# Calibration에서 선택한 판정 기준이 저장된 JSON
#
# DATA_DIR:
# 정상 Test 3장과 불량 Test 3장이 있는 폴더
#
# OUTPUT_DIR:
# 판정 결과를 표시한 이미지를 저장할 폴더
#
# OUTPUT_CSV:
# 이미지별 측정값과 OK/NG 판정을 기록할 파일
#
# 왜 필요한가요?
# Test에서는 기준값을 새로 만드는 것이 아니라
# 앞에서 동결한 JSON을 읽어서 사용하기 때문입니다.
# --------------------------------------------------

RULE_PATH = Path(
    "configs/day05_logo_rules.json"
)

DATA_DIR = Path(
    "samples/day05/resized"
)

OUTPUT_DIR = Path(
    "outputs/day05/test"
)

OUTPUT_CSV = Path(
    "reports/day05_test_results.csv"
)


# --------------------------------------------------
# 2. Test 이미지 목록과 실제 정답 준비
#
# 무엇을 하나요?
# - test_ok_*.jpg 패턴의 이미지를 찾습니다.
# - test_ng_*.jpg 패턴의 이미지를 찾습니다.
# - 각 이미지에 실제 정답인 OK 또는 NG를 연결합니다.
#
# 예상 데이터:
# test_ok_01.jpg ~ test_ok_03.jpg
# test_ng_01.jpg ~ test_ng_03.jpg
#
# actual:
# 사람이 미리 알고 있는 실제 정답입니다.
#
# 주의:
# 여기서는 파일명으로 실제 정답을 지정합니다.
# 프로그램이 예측한 결과는 나중에 따로 계산합니다.
# --------------------------------------------------

def find_test_images():

    image_infos = []

    # --------------------------------------------------
    # 2-1. 실제 정상(OK) Test 이미지 찾기
    #
    # - test_ok_로 시작하는 이미지를 찾습니다.
    # - 파일명 순서대로 정렬합니다.
    # - 이미지 경로와 실제 정답 "OK"를 저장합니다.
    # --------------------------------------------------

    for image_path in sorted(
        DATA_DIR.glob("test_ok_*.jpg")
    ):

        image_infos.append(
            (
                image_path,
                "OK"
            )
        )

    # --------------------------------------------------
    # 2-2. 실제 불량(NG) Test 이미지 찾기
    #
    # - test_ng_로 시작하는 이미지를 찾습니다.
    # - 파일명 순서대로 정렬합니다.
    # - 이미지 경로와 실제 정답 "NG"를 저장합니다.
    # --------------------------------------------------

    for image_path in sorted(
        DATA_DIR.glob("test_ng_*.jpg")
    ):

        image_infos.append(
            (
                image_path,
                "NG"
            )
        )

    # 이미지 경로와 실제 정답 목록 반환
    return image_infos


# --------------------------------------------------
# 3. 측정값에 동결한 Rule을 적용하는 판정 함수
#
# 무엇을 하나요?
# - measure_target()에서 계산한 측정값을 받습니다.
# - JSON에 저장된 검사 기준과 비교합니다.
# - 조건을 만족하지 못한 이유를 기록합니다.
# - 최종 OK 또는 NG를 판정합니다.
#
# 이번 Baseline Rule:
#
# Homography 계산 성공
#           AND
# SIFT Good Match >= 129
#           AND
# Inlier Ratio >= 0.8664
#
# 세 조건을 모두 만족하면 OK입니다.
# 하나라도 만족하지 못하면 NG입니다.
#
# 입력:
# measurement → 이미지의 측정값
# rules       → JSON에서 읽은 검사 기준
#
# 반환:
# predicted → OK 또는 NG
# reasons   → 기준을 만족하지 못한 이유
# --------------------------------------------------

def judge_measurement(
    measurement,
    rules,
):

    # 실패 이유를 저장할 빈 리스트
    reasons = []

    # JSON의 required_rules 가져오기
    required = rules[
        "required_rules"
    ]

    # --------------------------------------------------
    # 3-1. Homography 계산 성공 여부 검사
    #
    # 무엇을 하나요?
    # - JSON에서 Homography가 필수 조건인지 확인합니다.
    # - 필수인데 계산에 실패했다면 NG 이유를 기록합니다.
    #
    # HOMOGRAPHY_NOT_FOUND:
    # 두 이미지 사이의 Homography 계산에 실패
    #
    # 주의:
    # Homography 성공은 로고가 정상이라는 의미가 아니라
    # 기하학적 변환 행렬을 계산했다는 의미입니다.
    # --------------------------------------------------

    if (
        required["homography_found"]
        and measurement["homography_found"] != 1
    ):

        reasons.append(
            "HOMOGRAPHY_NOT_FOUND"
        )

    # --------------------------------------------------
    # 3-2. SIFT Good Match 기준 검사
    #
    # 무엇을 하나요?
    # - 측정한 SIFT Good Match 개수를 확인합니다.
    # - JSON의 최소 기준값과 비교합니다.
    #
    # 예:
    # 측정값 = 105
    # 기준값 = 129
    #
    # 105 < 129 이므로 기준 미달입니다.
    #
    # LOW_SIFT_MATCH:
    # 특징점 대응 개수가 부족하다는 의미입니다.
    # --------------------------------------------------

    if (
        measurement["sift_good_matches"]
        < required["sift_good_matches_min"]
    ):

        reasons.append(
            "LOW_SIFT_MATCH"
        )

    # --------------------------------------------------
    # 3-3. Inlier Ratio 기준 검사
    #
    # 무엇을 하나요?
    # - 측정한 Inlier Ratio를 확인합니다.
    # - JSON의 최소 기준값과 비교합니다.
    #
    # 예:
    # 측정값 = 0.8397
    # 기준값 = 0.8664
    #
    # 0.8397 < 0.8664 이므로 기준 미달입니다.
    #
    # LOW_INLIER_RATIO:
    # 일관된 특징점 대응의 비율이 부족하다는 의미입니다.
    # --------------------------------------------------

    if (
        measurement["inlier_ratio"]
        < required["inlier_ratio_min"]
    ):

        reasons.append(
            "LOW_INLIER_RATIO"
        )

    # --------------------------------------------------
    # 3-4. 검사 실패 이유를 확인하여 최종 판정
    #
    # 무엇을 하나요?
    # - reasons 리스트가 비어 있는지 확인합니다.
    #
    # 실패 이유 없음:
    # 세 조건을 모두 통과했으므로 OK
    #
    # 실패 이유 있음:
    # 하나 이상의 조건을 통과하지 못했으므로 NG
    #
    # 반환값:
    # predicted와 reasons
    # --------------------------------------------------

    if not reasons:

        predicted = "OK"

    else:

        predicted = "NG"

    return predicted, reasons


# --------------------------------------------------
# 4. 실제 정답과 프로그램 판정을 비교하는 함수
#
# 무엇을 하나요?
# - 사람이 알고 있는 실제 정답(actual)과
#   프로그램의 판정(predicted)을 비교합니다.
# - 결과를 TP, TN, FP, FN으로 구분합니다.
#
# 이번 제조검사에서는 NG를 Positive로 정의합니다.
#
# TP:
# 실제 NG → 프로그램 NG
# 불량을 올바르게 검출
#
# TN:
# 실제 OK → 프로그램 OK
# 정상을 올바르게 통과
#
# FP:
# 실제 OK → 프로그램 NG
# 정상을 불량으로 잘못 판정
#
# FN:
# 실제 NG → 프로그램 OK
# 불량을 정상으로 잘못 통과
#
# 왜 필요한가요?
# 전체 Accuracy뿐 아니라 어떤 종류의
# 판정 오류가 발생했는지 확인하기 위해서입니다.
# --------------------------------------------------

def classify_error(
    actual,
    predicted,
):

    # 실제 NG를 NG로 올바르게 검출
    if (
        actual == "NG"
        and predicted == "NG"
    ):
        return "TP"

    # 실제 OK를 OK로 올바르게 판정
    if (
        actual == "OK"
        and predicted == "OK"
    ):
        return "TN"

    # 실제 OK를 NG로 잘못 판정
    if (
        actual == "OK"
        and predicted == "NG"
    ):
        return "FP"

    # 실제 NG를 OK로 잘못 통과
    if (
        actual == "NG"
        and predicted == "OK"
    ):
        return "FN"

    return "UNKNOWN"


# --------------------------------------------------
# 5. 판정 결과와 로고 위치를 이미지에 표시하는 함수
#
# 무엇을 하나요?
# - 검사 이미지의 복사본을 만듭니다.
# - Homography로 계산한 로고 위치를 사각형으로 표시합니다.
# - OK/NG에 따라 사각형 색상을 구분합니다.
# - 실제 정답, 프로그램 판정, 측정값, NG 이유를 표시합니다.
#
# 왜 필요한가요?
# CSV의 숫자만 보는 것보다 실제 이미지에서
# 어떤 위치를 찾았고 왜 NG가 되었는지
# 쉽게 확인할 수 있기 때문입니다.
#
# 주의:
# 사각형은 Homography로 계산한 위치이며,
# 실제 로고가 정확히 검출되었음을 보증하지 않습니다.
# --------------------------------------------------

def annotate_result(
    measurement,
    actual,
    predicted,
    reasons,
):

    # 원본 Target을 수정하지 않도록 복사
    image = (
        measurement["target_image"]
        .copy()
    )

    # Homography로 계산한 로고 영역 좌표
    polygon = measurement.get(
        "polygon"
    )

    # --------------------------------------------------
    # 5-1. Homography로 찾은 로고 영역 표시
    #
    # 무엇을 하나요?
    # - polygon 좌표가 있는지 확인합니다.
    # - 네 모서리 좌표를 정수로 변환합니다.
    # - 네 점을 연결할 수 있는 형태로 변환합니다.
    #
    # np.int32():
    # 좌표를 정수로 변환합니다.
    #
    # reshape(-1, 1, 2):
    # OpenCV의 polylines()에서 사용할 배열 형태입니다.
    # --------------------------------------------------

    if polygon is not None:

        points = np.int32(
            polygon
        ).reshape(
            -1,
            1,
            2
        )

        # --------------------------------------------------
        # 5-2. 프로그램 판정에 따라 사각형 색상 선택
        #
        # Predicted = OK:
        # 초록색 (0, 255, 0)
        #
        # Predicted = NG:
        # 빨간색 (0, 0, 255)
        #
        # OpenCV는 BGR 색상 순서를 사용합니다.
        #
        # 중요:
        # 색상은 프로그램 판정을 나타냅니다.
        # 실제 정답과 일치한다는 뜻은 아닙니다.
        # --------------------------------------------------

        if predicted == "OK":

            line_color = (
                0,
                255,
                0
            )

        else:

            line_color = (
                0,
                0,
                255
            )

        # --------------------------------------------------
        # 5-3. 계산된 로고 영역에 사각형 그리기
        #
        # cv2.polylines():
        # 여러 점을 선으로 연결하는 함수
        #
        # True:
        # 마지막 점과 처음 점을 연결하여 도형을 닫습니다.
        #
        # 3:
        # 선의 두께입니다.
        # --------------------------------------------------

        cv2.polylines(
            image,
            [points],
            True,
            line_color,
            3
        )

    # --------------------------------------------------
    # 5-4. 검사 실패 이유를 표시할 문자열 만들기
    #
    # 무엇을 하나요?
    # - 실패 이유가 여러 개이면 +로 연결합니다.
    # - 실패 이유가 없다면 PASS로 표시합니다.
    #
    # 예:
    # LOW_SIFT_MATCH+LOW_INLIER_RATIO
    #
    # 또는:
    # PASS
    #
    # 이 문자열은 결과 이미지에 표시할 때 사용합니다.
    # --------------------------------------------------

    reason_text = (
        "+".join(reasons)
        if reasons
        else "PASS"
    )

    # --------------------------------------------------
    # 5-5. 결과 이미지에 표시할 측정 정보 준비
    #
    # 표시 항목:
    #
    # Actual:
    # 실제 정답인 OK 또는 NG
    #
    # Predicted:
    # 프로그램이 판정한 OK 또는 NG
    #
    # SIFT Good:
    # Good Match 개수
    #
    # Inlier Ratio:
    # 기하학적으로 일관된 대응점 비율
    #
    # Template:
    # Template Matching 유사도
    #
    # Reason:
    # NG 판정 이유 또는 PASS
    # --------------------------------------------------

    lines = [

        f"Actual: {actual}",

        f"Predicted: {predicted}",

        (
            "SIFT Good: "
            f"{measurement['sift_good_matches']}"
        ),

        (
            "Inlier Ratio: "
            f"{measurement['inlier_ratio']:.4f}"
        ),

        (
            "Template: "
            f"{measurement['template_score']:.4f}"
        ),

        f"Reason: {reason_text}",
    ]

    # --------------------------------------------------
    # 5-6. 결과 이미지에 측정값을 문자로 표시
    #
    # 무엇을 하나요?
    # - 준비한 lines를 한 줄씩 가져옵니다.
    # - 이미지의 왼쪽 위부터 순서대로 표시합니다.
    #
    # cv2.putText():
    # 이미지 위에 문자를 작성하는 함수
    #
    # (30, y):
    # 문자를 표시할 위치
    #
    # (255, 255, 255):
    # 흰색
    #
    # y += 35:
    # 다음 줄을 아래로 35픽셀 이동합니다.
    # --------------------------------------------------

    y = 40

    for line in lines:

        cv2.putText(
            image,
            line,
            (30, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
            cv2.LINE_AA
        )

        y += 35

    # 결과 문자가 표시된 이미지 반환
    return image


# --------------------------------------------------
# 6. 동결한 Baseline Rule JSON 읽기
#
# 무엇을 하나요?
# - main() 함수를 정의합니다.
# - 이전 실습에서 저장한 JSON이 있는지 확인합니다.
# - JSON을 Python 딕셔너리로 읽습니다.
# - 사용할 Rule 버전과 Threshold를 출력합니다.
#
# 왜 필요한가요?
# Calibration에서 결정한 기준을
# Test에서 변경하지 않고 그대로 사용하기 위해서입니다.
#
# json.load():
# JSON 파일의 데이터를 Python 객체로 읽는 함수입니다.
#
# Rule JSON이 없다면:
# 먼저 36_day05_freeze_rule.py를 실행해야 합니다.
# --------------------------------------------------

def main():

    if not RULE_PATH.exists():

        raise FileNotFoundError(
            "Rule JSON이 없습니다. "
            "먼저 36_day05_freeze_rule.py를 실행하세요."
        )

    with RULE_PATH.open(
        "r",
        encoding="utf-8"
    ) as file:

        rules = json.load(
            file
        )

    # Rule 버전과 Threshold 확인
    print("=" * 70)

    print(
        "Baseline Rule:",
        rules["baseline_version"]
    )

    print(
        "SIFT >=",
        rules[
            "required_rules"
        ][
            "sift_good_matches_min"
        ]
    )

    print(
        "Inlier Ratio >=",
        rules[
            "required_rules"
        ][
            "inlier_ratio_min"
        ]
    )


    # --------------------------------------------------
    # 7. JSON에 기록된 Reference 이미지 준비
    #
    # 무엇을 하나요?
    # - JSON에 저장된 Reference 이미지 경로를 읽습니다.
    # - prepare_reference() 공통 함수를 호출합니다.
    # - 기준 로고의 SIFT 특징점을 한 번 준비합니다.
    #
    # 왜 필요한가요?
    # Calibration과 Test에서 동일한 Reference를 사용하고
    # Target마다 특징점을 다시 계산하지 않기 위해서입니다.
    # --------------------------------------------------

    reference_path = Path(
        rules[
            "reference"
        ][
            "reference_label"
        ]
    )

    reference_data = prepare_reference(
        reference_path
    )


    # --------------------------------------------------
    # 8. Test 이미지 6장 확인 및 결과 저장 폴더 준비
    #
    # 무엇을 하나요?
    # - find_test_images() 함수를 호출합니다.
    # - 실제 OK 3장과 NG 3장의 목록을 가져옵니다.
    # - 전체 이미지 개수를 확인합니다.
    # - 결과 이미지와 CSV를 저장할 폴더를 생성합니다.
    #
    # 예상 데이터:
    # OK 3장 + NG 3장 = 총 6장
    #
    # 주의:
    # 현재 코드는 6장이 아니더라도 경고만 출력하고
    # 프로그램을 계속 진행합니다.
    #
    # rows:
    # 이미지별 검사 결과를 저장할 리스트입니다.
    # --------------------------------------------------

    image_infos = (
        find_test_images()
    )

    print(
        "Test Images:",
        len(image_infos)
    )

    if len(image_infos) != 6:

        print(
            "주의: Test 이미지는 "
            "OK 3장 + NG 3장 = 6장을 예상합니다."
        )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_CSV.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    rows = []


    # --------------------------------------------------
    # 9. Test 이미지마다 공통 측정 함수 실행
    #
    # 무엇을 하나요?
    # - Test 이미지를 하나씩 가져옵니다.
    # - measure_target() 공통 함수를 호출합니다.
    # - 이미지의 Template, SIFT, Homography 측정값을 구합니다.
    #
    # measure_target() 내부 처리:
    #
    # ① Target 이미지 읽기
    # ② Template Matching
    # ③ SIFT Keypoint / Descriptor 추출
    # ④ BFMatcher
    # ⑤ Ratio Test
    # ⑥ RANSAC + Homography
    # ⑦ Inlier Count / Inlier Ratio 계산
    #
    # 아직 이 단계에서는 판정하지 않고
    # 측정값만 구합니다.
    # --------------------------------------------------

    for image_path, actual in image_infos:

        measurement = measure_target(
            image_path,
            reference_data
        )


        # --------------------------------------------------
        # 10. 측정값에 동결한 Baseline Rule 적용
        #
        # 무엇을 하나요?
        # - 3번에서 만든 judge_measurement()를 호출합니다.
        # - 측정값과 JSON 기준을 비교합니다.
        #
        # 모든 기준 통과:
        # predicted = OK
        #
        # 하나라도 기준 미달:
        # predicted = NG
        #
        # reasons:
        # 기준을 통과하지 못한 이유를 저장합니다.
        #
        # 왜 필요한가요?
        # Calibration에서 결정한 복합 Rule을
        # 새로운 Test 이미지에 그대로 적용하기 위해서입니다.
        # --------------------------------------------------

        predicted, reasons = (
            judge_measurement(
                measurement,
                rules
            )
        )


        # --------------------------------------------------
        # 11. 실제 정답과 프로그램 판정 비교
        #
        # 무엇을 하나요?
        # - 4번에서 만든 classify_error()를 호출합니다.
        # - 실제 정답과 예측 결과를 비교합니다.
        # - TP, TN, FP, FN 중 하나로 구분합니다.
        #
        # 예:
        # actual = OK
        # predicted = NG
        #
        # 결과:
        # FP
        #
        # 왜 필요한가요?
        # Test 이미지에서 프로그램이
        # 몇 장을 올바르게 판정했는지 평가하기 위해서입니다.
        # --------------------------------------------------

        error_type = classify_error(
            actual,
            predicted
        )


        # --------------------------------------------------
        # 12. 검사 결과 이미지 생성 및 저장
        #
        # 무엇을 하나요?
        # - annotate_result() 함수를 호출합니다.
        # - 로고 위치와 측정값을 이미지에 표시합니다.
        # - Target 이름을 이용하여 결과 파일명을 만듭니다.
        # - 결과 이미지를 JPG로 저장합니다.
        #
        # 예:
        # test_ok_01.jpg
        #        ↓
        # test_ok_01_result.jpg
        #
        # 저장 위치:
        # outputs/day05/test/
        #
        # 왜 필요한가요?
        # 실제 이미지에서 어떤 위치를 검출했고
        # 어떤 이유로 판정했는지 눈으로 확인하기 위해서입니다.
        # --------------------------------------------------

        result_image = annotate_result(
            measurement,
            actual,
            predicted,
            reasons
        )

        output_image = (
            OUTPUT_DIR
            / (
                f"{image_path.stem}"
                "_result.jpg"
            )
        )

        cv2.imwrite(
            str(output_image),
            result_image
        )


        # --------------------------------------------------
        # 13. 이미지별 판정 결과를 CSV용 데이터로 정리
        #
        # 무엇을 하나요?
        # - 현재 Test 이미지의 측정값과 판정 결과를 정리합니다.
        # - 하나의 딕셔너리로 저장합니다.
        # - rows 리스트에 추가합니다.
        # - 터미널에 현재 검사 결과를 출력합니다.
        #
        # 주요 저장 항목:
        #
        # file:
        # 이미지 이름
        #
        # actual:
        # 실제 정답
        #
        # predicted:
        # 프로그램 판정
        #
        # error_type:
        # TP / TN / FP / FN
        #
        # ng_reason:
        # NG 판정 이유 또는 PASS
        #
        # template_score:
        # Template Matching 유사도
        #
        # sift_good_matches:
        # SIFT Good Match 개수
        #
        # homography_found:
        # Homography 계산 성공 여부
        #
        # homography_inliers:
        # RANSAC Inlier 개수
        #
        # inlier_ratio:
        # Inlier 비율
        #
        # result_image:
        # 결과 이미지 저장 경로
        # --------------------------------------------------

        row = {

            "file":
                image_path.name,

            "actual":
                actual,

            "predicted":
                predicted,

            "error_type":
                error_type,

            "ng_reason":
                (
                    ";".join(reasons)
                    if reasons
                    else "PASS"
                ),

            "template_score":
                round(
                    measurement[
                        "template_score"
                    ],
                    6
                ),

            "sift_good_matches":
                measurement[
                    "sift_good_matches"
                ],

            "homography_found":
                measurement[
                    "homography_found"
                ],

            "homography_inliers":
                measurement[
                    "homography_inliers"
                ],

            "inlier_ratio":
                round(
                    measurement[
                        "inlier_ratio"
                    ],
                    6
                ),

            "result_image":
                str(output_image),
        }

        rows.append(
            row
        )

        print(
            row
        )


    # --------------------------------------------------
    # 14. Test 6장의 측정 및 판정 결과를 CSV로 저장
    #
    # 무엇을 하나요?
    # - CSV 컬럼명을 정합니다.
    # - CSV 파일을 생성합니다.
    # - Test 이미지별 측정값과 판정을 저장합니다.
    #
    # 저장 파일:
    # reports/day05_test_results.csv
    #
    # utf-8-sig:
    # Excel에서 한글이 깨질 가능성을 줄입니다.
    #
    # writer.writeheader():
    # 첫 번째 행에 컬럼명을 기록합니다.
    #
    # writer.writerows(rows):
    # 모든 이미지의 검사 결과를 기록합니다.
    #
    # 왜 필요한가요?
    # 이후 성능 평가와 실패 분석에서
    # 동일한 검사 결과를 재사용하기 위해서입니다.
    # --------------------------------------------------

    fieldnames = [
        "file",
        "actual",
        "predicted",
        "error_type",
        "ng_reason",
        "template_score",
        "sift_good_matches",
        "homography_found",
        "homography_inliers",
        "inlier_ratio",
        "result_image",
    ]

    with OUTPUT_CSV.open(
        "w",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames
        )

        writer.writeheader()

        writer.writerows(
            rows
        )


    # --------------------------------------------------
    # 15. Test 전체의 TP/TN/FP/FN과 Accuracy 계산
    #
    # 무엇을 하나요?
    # - 각 이미지에서 기록한 error_type을 확인합니다.
    # - TP, TN, FP, FN의 전체 개수를 계산합니다.
    # - Test 전체 Accuracy를 계산합니다.
    #
    # Accuracy:
    # (TP + TN) / 전체 Test 이미지 수
    #
    # 예:
    # 6장 중 3장을 올바르게 판정하면
    # Accuracy = 3 / 6 = 0.5
    #
    # 왜 필요한가요?
    # Calibration에서 선택한 Rule이
    # 새로운 이미지에서도 얼마나 정확하게
    # 동작하는지 평가하기 위해서입니다.
    #
    # 주의:
    # 현재 코드는 이미 기록된 error_type을 집계하며,
    # Rule을 다시 변경하거나 재학습하지 않습니다.
    # --------------------------------------------------

    tp = sum(
        row["error_type"] == "TP"
        for row in rows
    )

    tn = sum(
        row["error_type"] == "TN"
        for row in rows
    )

    fp = sum(
        row["error_type"] == "FP"
        for row in rows
    )

    fn = sum(
        row["error_type"] == "FN"
        for row in rows
    )

    total = len(rows)

    accuracy = (
        (tp + tn) / total
        if total
        else 0.0
    )


    # --------------------------------------------------
    # 16. Test 완료 및 전체 검사 결과 출력
    #
    # 무엇을 하나요?
    # - 검사한 Test 이미지 수를 출력합니다.
    # - Accuracy를 출력합니다.
    # - TP, TN, FP, FN 개수를 출력합니다.
    # - CSV와 결과 이미지의 저장 위치를 출력합니다.
    #
    # 왜 필요한가요?
    # Baseline Rule이 Test 데이터에서
    # 어떻게 동작했는지 한눈에 확인하기 위해서입니다.
    #
    # 특히 확인할 값:
    #
    # FP:
    # 정상 이미지를 NG로 잘못 판정한 개수
    #
    # FN:
    # 불량 이미지를 OK로 잘못 통과시킨 개수
    # --------------------------------------------------

    print()

    print("=" * 70)

    print(
        "Test 완료"
    )

    print("=" * 70)

    print(
        "전체:",
        total
    )

    print(
        "Accuracy:",
        round(
            accuracy,
            4
        )
    )

    print(
        "TP:",
        tp
    )

    print(
        "TN:",
        tn
    )

    print(
        "FP:",
        fp
    )

    print(
        "FN:",
        fn
    )

    print(
        "CSV:",
        OUTPUT_CSV
    )

    print(
        "결과 이미지:",
        OUTPUT_DIR
    )


# --------------------------------------------------
# 17. Python 파일을 직접 실행하면 main() 호출
#
# 무엇을 하나요?
# - 현재 파일이 직접 실행되었는지 확인합니다.
# - 직접 실행했다면 main() 함수를 호출합니다.
#
# 왜 필요한가요?
# 다른 파일에서 이 코드를 import할 때
# Test 작업이 자동으로 실행되지 않도록 하기 위해서입니다.
#
# 실행 명령어:
# python src/37_day05_test.py
# --------------------------------------------------

if __name__ == "__main__":
    main()
```
### 의사코드

```
[1. Rule JSON, Test 이미지 및 결과 저장 경로 설정]

동결한 Rule JSON 파일의 경로를 지정한다.

configs/day05_logo_rules.json

Test 이미지가 있는 폴더를 지정한다.

samples/day05/resized/

결과 이미지를 저장할 폴더를 지정한다.

outputs/day05/test/

검사 결과 CSV 경로를 지정한다.

reports/day05_test_results.csv

          ↓

[2. Test 이미지 목록과 실제 정답 준비]

find_test_images() 함수를 만든다.

이미지 정보를 저장할 빈 리스트를 만든다.

          ↓

[2-1. 정상 Test 이미지 찾기]

test_ok_로 시작하는 JPG 이미지를 찾는다.

각 이미지의 경로를 저장한다.
실제 정답을 OK로 기록한다.

          ↓

[2-2. 불량 Test 이미지 찾기]

test_ng_로 시작하는 JPG 이미지를 찾는다.

각 이미지의 경로를 저장한다.
실제 정답을 NG로 기록한다.

          ↓

Test 이미지 목록과 실제 정답을 반환한다.

          ↓

[3. 측정값에 동결한 Rule을 적용하는 판정 함수]

judge_measurement() 함수를 만든다.

이미지의 측정값을 전달받는다.
JSON에서 읽은 Rule을 전달받는다.

실패 이유를 저장할 빈 리스트를 만든다.

          ↓

[3-1. Homography 성공 여부 확인]

JSON의 Homography 필수 조건을 확인한다.

Homography가 필수이고 계산에 실패했다면

HOMOGRAPHY_NOT_FOUND

를 실패 이유에 추가한다.

          ↓

[3-2. SIFT Good Match 검사]

SIFT Good Match 측정값을 읽는다.
JSON의 최소 SIFT 기준값을 읽는다.

SIFT Good Match < 기준값

이면

LOW_SIFT_MATCH

를 실패 이유에 추가한다.

          ↓

[3-3. Inlier Ratio 검사]

Inlier Ratio 측정값을 읽는다.
JSON의 최소 Inlier Ratio 기준값을 읽는다.

Inlier Ratio < 기준값

이면

LOW_INLIER_RATIO

를 실패 이유에 추가한다.

          ↓

[3-4. 최종 OK / NG 판정]

실패 이유 리스트를 확인한다.

실패 이유가 없다면
Predicted = OK

실패 이유가 하나라도 있다면
Predicted = NG

          ↓

Predicted와 실패 이유 리스트를 반환한다.

          ↓

[4. 실제 정답과 프로그램 판정을 비교하는 함수]

classify_error() 함수를 만든다.

실제 정답 Actual을 전달받는다.
프로그램 판정 Predicted를 전달받는다.

          ↓

실제 NG / 예측 NG
→ TP 반환

실제 OK / 예측 OK
→ TN 반환

실제 OK / 예측 NG
→ FP 반환

실제 NG / 예측 OK
→ FN 반환

그 외의 값
→ UNKNOWN 반환

          ↓

[5. 판정 결과와 로고 위치를 이미지에 표시하는 함수]

annotate_result() 함수를 만든다.

Target 이미지의 복사본을 만든다.

Homography로 계산한
Polygon 좌표가 있는지 확인한다.

          ↓

[5-1. 로고 영역 좌표 준비]

Polygon 좌표가 있다면
네 모서리 좌표를 정수로 변환한다.

OpenCV에서 사각형을 그릴 수 있도록
좌표 배열을 준비한다.

          ↓

[5-2. 판정에 따라 색상 선택]

프로그램 판정이 OK라면
초록색을 선택한다.

프로그램 판정이 NG라면
빨간색을 선택한다.

          ↓

[5-3. 로고 영역 사각형 그리기]

Homography로 계산한 네 점을
선으로 연결한다.

선택된 색상으로 로고 영역을 표시한다.

          ↓

[5-4. NG Reason 문자열 만들기]

실패 이유가 여러 개라면
+ 기호로 연결한다.

실패 이유가 없다면
PASS라고 기록한다.

          ↓

[5-5. 결과 이미지에 표시할 정보 준비]

Actual을 준비한다.
Predicted를 준비한다.
SIFT Good Match를 준비한다.
Inlier Ratio를 준비한다.
Template Score를 준비한다.
NG Reason을 준비한다.

          ↓

[5-6. 측정값과 판정 결과 표시]

이미지 왼쪽 위부터 문자를 표시한다.

한 줄을 표시한 뒤
다음 줄은 35픽셀 아래에 표시한다.

모든 정보를 표시한
결과 이미지를 반환한다.

          ↓

[6. 동결한 Baseline Rule JSON 읽기]

main() 함수를 만든다.

Rule JSON 파일이 있는지 확인한다.

파일이 없다면
오류를 발생시킨다.

파일이 있다면
json.load()로 내용을 읽는다.

          ↓

Rule 버전을 출력한다.
SIFT Threshold를 출력한다.
Inlier Ratio Threshold를 출력한다.

          ↓

[7. JSON에 기록된 Reference 이미지 준비]

JSON에서 기준 로고 경로를 가져온다.

prepare_reference() 함수를 호출한다.

Reference 이미지를 읽는다.
SIFT 특징점을 계산한다.

Reference 정보를 저장한다.

          ↓

[8. Test 이미지와 결과 폴더 준비]

find_test_images() 함수를 호출한다.

Test 이미지 목록을 가져온다.

전체 이미지 개수를 확인한다.

          ↓

Test 이미지가 6장이 아니라면
경고를 출력한다.

          ↓

결과 이미지 폴더를 준비한다.
CSV 저장 폴더를 준비한다.

검사 결과를 저장할
빈 rows 리스트를 만든다.

          ↓

[9. Test 이미지마다 공통 측정 함수 실행]

첫 번째 Test 이미지를 선택한다.

이미지 경로와 실제 정답을 가져온다.

measure_target() 함수를 호출한다.

          ↓

Template Score를 계산한다.
SIFT Good Match 개수를 계산한다.
Homography 계산 성공 여부를 확인한다.
Homography Inlier 개수를 계산한다.
Inlier Ratio를 계산한다.

          ↓

측정값을 measurement에 저장한다.

          ↓

[10. 동결한 Baseline Rule 적용]

judge_measurement() 함수를 호출한다.

측정값과 JSON Rule을 전달한다.

          ↓

Homography 계산 성공 여부를 확인한다.

SIFT Good Match 기준을 확인한다.

Inlier Ratio 기준을 확인한다.

          ↓

모두 통과하면 OK

하나라도 실패하면 NG

          ↓

Predicted와 NG Reason을 반환받는다.

          ↓

[11. 실제 정답과 프로그램 판정 비교]

classify_error() 함수를 호출한다.

Actual과 Predicted를 비교한다.

          ↓

TP / TN / FP / FN 중
해당하는 결과를 저장한다.

          ↓

[12. 검사 결과 이미지 생성 및 저장]

annotate_result() 함수를 호출한다.

          ↓

로고 위치를 사각형으로 표시한다.
실제 정답을 표시한다.
프로그램 판정을 표시한다.
측정값과 NG Reason을 표시한다.

          ↓

결과 이미지 파일명을 만든다.

예:
test_ok_01_result.jpg

          ↓

JPG 파일로 저장한다.

          ↓

[13. 이미지별 판정 결과 정리]

현재 이미지의 검사 결과를
하나의 딕셔너리로 만든다.

          ↓

이미지 이름을 기록한다.
실제 정답을 기록한다.
프로그램 판정을 기록한다.
TP/TN/FP/FN을 기록한다.

          ↓

NG Reason을 기록한다.
Template Score를 기록한다.
SIFT Good Match를 기록한다.
Homography Found를 기록한다.
Homography Inlier를 기록한다.
Inlier Ratio를 기록한다.
결과 이미지 경로를 기록한다.

          ↓

rows 리스트에 추가한다.

현재 검사 결과를 터미널에 출력한다.

          ↓

아직 검사할 Test 이미지가 남았다면
9번으로 돌아가 다음 이미지를 검사한다.

모든 Test 이미지 검사가 끝나면
14번으로 이동한다.

          ↓

[14. Test 결과 CSV 저장]

CSV 컬럼명을 준비한다.

          ↓

day05_test_results.csv 파일을 연다.

첫 번째 행에 컬럼명을 작성한다.

모든 Test 이미지의 결과를
한 행씩 저장한다.

          ↓

[15. TP/TN/FP/FN과 Accuracy 계산]

rows에서 TP 개수를 센다.
rows에서 TN 개수를 센다.
rows에서 FP 개수를 센다.
rows에서 FN 개수를 센다.

          ↓

전체 Test 이미지 개수를 계산한다.

Accuracy =
(TP + TN) / 전체 이미지 개수

          ↓

전체 판정 정확도를 계산한다.

          ↓

[16. Test 완료 및 전체 결과 출력]

Test 완료 메시지를 출력한다.

전체 이미지 개수를 출력한다.

Accuracy를 출력한다.

TP 개수를 출력한다.
TN 개수를 출력한다.
FP 개수를 출력한다.
FN 개수를 출력한다.

CSV 저장 경로를 출력한다.
결과 이미지 저장 경로를 출력한다.

          ↓

[17. 프로그램 실행]

Python 파일을 직접 실행했다면
main() 함수를 호출한다.

          ↓

[최종 결과]

Calibration에서 동결한 Rule JSON
          +
Test 이미지 6장
          ↓
Reference 특징점 준비
          ↓
Test 이미지 한 장 측정
          ↓
Template / SIFT / Homography
          ↓
JSON의 복합 Rule 적용
          ↓
OK / NG 판정
          ↓
실제 정답과 비교
          ↓
TP / TN / FP / FN
          ↓
결과 이미지 저장
          +
측정 결과 CSV 저장
          ↓
Accuracy 계산
          ↓
Test 전체 성능 확인
          ↓
다음 실습
38_day05_evaluate.py
          ↓
Precision / Recall 평가
          +
FP / FN 실패 분석
```
### 실행합니다

```
python src/37_day05_test.py
```

이번에는 결과가 **숫자만 저장되는 것이 아닙니다.**

다음 두 종류의 결과물이 만들어집니다.

```
reports/day05_test_results.csv
```

```
outputs/day05/test/

test_ok_01_result.jpg
test_ok_02_result.jpg
test_ok_03_result.jpg

test_ng_01_result.jpg
test_ng_02_result.jpg
test_ng_03_result.jpg
```

![[{5341ACDB-44B5-4519-B2B9-2152F6EF5F92}.png]]

---

# 27. 실제 Test 결과를 확인합니다

앞에서 동결한 Baseline Rule을 처음 보는 Test 이미지 6장에 적용했습니다.

사용한 기준은 다음과 같습니다.

```
Baseline Rule: day05-logo-v1.0
SIFT >= 129
Inlier Ratio >= 0.8664
Test Images: 6
{'file': 'test_ok_01.jpg', 'actual': 'OK', 'predicted': 'NG', 'error_type': 'FP', 'ng_reason': 'LOW_INLIER_RATIO', 'template_score': 0.581604, 'sift_good_matches': 169, 'homography_found': 1, 'homography_inliers': 132, 'inlier_ratio': 0.781065, 'result_image': 'outputs/day05/test/test_ok_01_result.jpg'}
{'file': 'test_ok_02.jpg', 'actual': 'OK', 'predicted': 'NG', 'error_type': 'FP', 'ng_reason': 'LOW_INLIER_RATIO', 'template_score': 0.45615, 'sift_good_matches': 156, 'homography_found': 1, 'homography_inliers': 131, 'inlier_ratio': 0.839744, 'result_image': 'outputs/day05/test/test_ok_02_result.jpg'}
{'file': 'test_ok_03.jpg', 'actual': 'OK', 'predicted': 'NG', 'error_type': 'FP', 'ng_reason': 'LOW_INLIER_RATIO', 'template_score': 0.500078, 'sift_good_matches': 204, 'homography_found': 1, 'homography_inliers': 174, 'inlier_ratio': 0.852941, 'result_image': 'outputs/day05/test/test_ok_03_result.jpg'}
{'file': 'test_ng_01.jpg', 'actual': 'NG', 'predicted': 'NG', 'error_type': 'TP', 'ng_reason': 'LOW_SIFT_MATCH;LOW_INLIER_RATIO', 'template_score': 0.392391, 'sift_good_matches': 58, 'homography_found': 1, 'homography_inliers': 43, 'inlier_ratio': 0.741379, 'result_image': 'outputs/day05/test/test_ng_01_result.jpg'}
{'file': 'test_ng_02.jpg', 'actual': 'NG', 'predicted': 'NG', 'error_type': 'TP', 'ng_reason': 'LOW_SIFT_MATCH;LOW_INLIER_RATIO', 'template_score': 0.515177, 'sift_good_matches': 111, 'homography_found': 1, 'homography_inliers': 85, 'inlier_ratio': 0.765766, 'result_image': 'outputs/day05/test/test_ng_02_result.jpg'}
{'file': 'test_ng_03.jpg', 'actual': 'NG', 'predicted': 'NG', 'error_type': 'TP', 'ng_reason': 'LOW_SIFT_MATCH', 'template_score': 0.536272, 'sift_good_matches': 105, 'homography_found': 1, 'homography_inliers': 96, 'inlier_ratio': 0.914286, 'result_image': 'outputs/day05/test/test_ng_03_result.jpg'}

======================================================================
Test 완료
======================================================================
전체: 6
Accuracy: 0.5
TP: 3
TN: 0
FP: 3
FN: 0
CSV: reports/day05_test_results.csv
결과 이미지: outputs/day05/test
```


```
Baseline Rule
day05-logo-v1.0

Homography 계산 성공

AND

SIFT Good Match >= 129

AND

Inlier Ratio >= 0.8664
```

실행 결과는 다음과 같습니다.

| 파일               | 실제  | 판정  | SIFT | Inlier Ratio | 결과  |
| ---------------- | --- | --- | ---: | -----------: | --- |
| `test_ok_01.jpg` | OK  | NG  |  169 |       0.7811 | FP  |
| `test_ok_02.jpg` | OK  | NG  |  156 |       0.8397 | FP  |
| `test_ok_03.jpg` | OK  | NG  |  204 |       0.8529 | FP  |
| `test_ng_01.jpg` | NG  | NG  |   58 |       0.7414 | TP  |
| `test_ng_02.jpg` | NG  | NG  |  111 |       0.7658 | TP  |
| `test_ng_03.jpg` | NG  | NG  |  105 |       0.9143 | TP  |

전체 결과는:

```
Test 이미지 = 6장

TP = 3
TN = 0
FP = 3
FN = 0

Accuracy = 0.5
         = 50%
```

입니다.

쉽게 말하면:

```
불량 3장
→ 모두 불량으로 검출
→ 성공

정상 3장
→ 모두 불량으로 판정
→ 실패
```

따라서 현재 Baseline은 불량을 놓치지는 않았지만 정상 제품까지 너무 많이 NG로 판정하는 상태입니다.

---

## 27.1 정상 Test 이미지 3장은 왜 모두 NG가 되었나요?

정상 이미지 세 장의 결과를 먼저 봅니다.

```
test_ok_01
SIFT = 169        → 통과
Ratio = 0.7811    → 실패

test_ok_02
SIFT = 156        → 통과
Ratio = 0.8397    → 실패

test_ok_03
SIFT = 204        → 통과
Ratio = 0.8529    → 실패
```

현재 기준은:

```
SIFT >= 129
AND
Inlier Ratio >= 0.8664
```

입니다.

세 이미지 모두 SIFT는 충분했습니다.

하지만:

```
0.7811 < 0.8664

0.8397 < 0.8664

0.8529 < 0.8664
```

로 **Inlier Ratio 기준을 통과하지 못했습니다.**

따라서:

```
실제 상태
OK

SIFT
통과

Homography
성공

Inlier Ratio
기준 미달
        ↓
Predicted = NG
        ↓
FP
```

가 되었습니다.

> 이번 Test에서는 정상 이미지의 주요 실패 원인이 `LOW_INLIER_RATIO`로 동일하게 나타났습니다.

---

## 27.2 불량 Test 이미지 3장은 어떻게 판정되었나요?

불량 이미지 세 장은 모두 올바르게 NG로 판정되었습니다.

### `test_ng_01.jpg`

```
SIFT = 58
→ 129보다 낮음

Inlier Ratio = 0.7414
→ 0.8664보다 낮음

Reason
LOW_SIFT_MATCH
+
LOW_INLIER_RATIO

→ NG
→ TP
```

### `test_ng_02.jpg`

```
SIFT = 111
→ 기준 미달

Inlier Ratio = 0.7658
→ 기준 미달

Reason
LOW_SIFT_MATCH
+
LOW_INLIER_RATIO

→ NG
→ TP
```

### `test_ng_03.jpg`

이 이미지는 조금 다릅니다.

```
SIFT = 105
→ 기준 미달

Inlier Ratio = 0.9143
→ 기준 통과
```

즉 Inlier Ratio는 높았지만 SIFT가 부족했기 때문에:

```
SIFT
실패

Inlier Ratio
통과
        ↓
NG
        ↓
TP
```

가 되었습니다.

이 결과에서도 **두 조건을 함께 사용하는 이유**를 확인할 수 있습니다.

---

## 27.3 결과 이미지는 무엇을 확인해야 하나요?

생성된 결과 이미지도 함께 확인합니다.

```
outputs/day05/test/
```

결과 이미지에는:

```
Actual
Predicted
SIFT Good Match
Inlier Ratio
Template Score
Reason
```

이 표시됩니다.

또 Homography가 계산되었다면 프로그램이 찾은 로고 영역도 사각형으로 표시됩니다.

이번 6장에서는 모두:

```
homography_found = 1
```

이었습니다.

즉 **로고 위치관계 자체는 모두 계산할 수 있었지만, 최종 OK / NG 판정에서는 SIFT와 Inlier Ratio 기준 때문에 결과가 달라진 것**입니다.

---

## 27.4 이번 Test에서 발견한 핵심

Calibration에서는 현재 Rule이:

```
12장 중 11장 정답
Accuracy = 91.67%
```

이었습니다.

하지만 처음 보는 Test에서는:

```
6장 중 3장 정답
Accuracy = 50%
```

으로 크게 떨어졌습니다.

특히:

```
Calibration에서는 잘 동작

        ↓

처음 보는 정상 Test 이미지

        ↓

Inlier Ratio가 예상보다 낮아짐

        ↓

정상 3장을 모두 NG로 판정
```

했습니다.

> 이것이 Test를 따로 하는 이유입니다. Calibration에서 성능이 좋았다고 해서 새로운 이미지에서도 같은 성능이 보장되는 것은 아닙니다.

---

# 28. NG Reason과 실제 Failure Cause를 구분합니다

이번 Test 결과에는 다음과 같은 `NG Reason`이 기록되었습니다.

```
LOW_SIFT_MATCH

LOW_INLIER_RATIO
```

이것은 **프로그램이 어떤 조건 때문에 NG라고 판정했는지 알려주는 값**입니다.

예를 들어 정상 이미지인 `test_ok_01.jpg`는:

```
Actual
→ OK

Predicted
→ NG

Reason
→ LOW_INLIER_RATIO
```

입니다.

이 뜻은 정확히:

```
Inlier Ratio = 0.7811
        <
Threshold = 0.8664
```

였다는 것입니다.

하지만 이것이 실제 원인까지 설명하는 것은 아닙니다.

---

## 28.1 이번 실제 결과에서 Failure Cause를 생각해 봅니다

정상 Test 이미지 세 장을 보면 모두:

```
Homography
→ 성공

SIFT
→ 129 이상

하지만

Inlier Ratio
→ 기준보다 낮음
```

이라는 공통적인 특징이 있습니다.

즉 프로그램 수준의 **NG Reason**은 명확합니다.

```
LOW_INLIER_RATIO
```

하지만 실제 **Failure Cause**는 이미지를 함께 보면서 확인해야 합니다.

예를 들어:

```
촬영 각도가 Calibration과 달랐는가?

제품 크기나 거리가 달라졌는가?

포장지의 구김이나 반사가 달라졌는가?

로고 주변 모습이 Calibration 이미지와 달랐는가?
```

등을 확인할 수 있습니다.

따라서 다음처럼 구분합니다.

|구분|이번 결과에서의 의미|
|---|---|
|**NG Reason**|Inlier Ratio가 `0.8664`보다 낮았음|
|**Failure Cause**|왜 정상 이미지의 Inlier Ratio가 낮아졌는지 실제 이미지를 보고 분석|

> `LOW_INLIER_RATIO`는 **측정 결과**이고, 촬영 각도·거리·반사 등의 차이는 그 결과가 발생한 **가능한 실제 원인**입니다.

---

## 28.2 이번 Test 결과가 알려주는 것은 무엇인가요?

이번 결과를 가장 간단히 정리하면:

```
NG 3장
→ 모두 잡음
→ FN = 0

하지만

OK 3장
→ 모두 NG로 판정
→ FP = 3
```

입니다.

따라서 현재 Baseline은:

```
불량을 놓치지 않는 데는 강함

하지만

정상 이미지에 대한 기준이 너무 엄격함
```

이라는 특성을 보였습니다.

특히 이번 Test에서는:

```
SIFT 기준
129
→ 정상 3장 모두 통과

Inlier Ratio 기준
0.8664
→ 정상 3장 모두 실패
```

했으므로 **현재 Rule에서 정상 Test 이미지의 판정을 가로막은 핵심 조건은 Inlier Ratio Threshold**였다는 것을 확인할 수 있습니다.

하지만 여기서 바로:

```
0.8664를 낮추자
```

라고 수정하지 않습니다.

다음 순서를 지킵니다.

```
Test 결과 확인
        ↓
FP = 3 확인
        ↓
공통 NG Reason 확인
LOW_INLIER_RATIO
        ↓
실제 이미지 확인
        ↓
왜 정상 이미지의 Ratio가
낮아졌는지 원인 분석
        ↓
현재 Baseline의 한계 기록
```

> **이번 Test는 실패한 실습이 아닙니다. Calibration에서 만든 Rule이 새로운 정상 이미지에는 충분히 일반화되지 않았다는 중요한 사실을 발견한 실습입니다.**

---
# PART6 **Evaluation** — 전체 성능 + FP/FN + 실패 원인 확인 (29~31)

---

# 29. Test 전체 성능을 계산합니다

앞의 Test 실습에서는 이미지마다 다음과 같은 결과를 만들었습니다.

```
test_ok_01.jpg
→ 실제 OK
→ 프로그램 판정 OK 또는 NG

test_ng_01.jpg
→ 실제 NG
→ 프로그램 판정 OK 또는 NG
```

그리고 모든 결과가 다음 파일에 저장되었습니다.

```
reports/day05_test_results.csv
```

이번에는 이 CSV를 읽어서 **Test 6장 전체에서 우리 Rule이 얼마나 잘 작동했는지 계산**합니다.

```
개별 이미지 판정 결과
        ↓
전체 결과 집계
        ↓
TP / TN / FP / FN
        ↓
Accuracy
Precision
Recall
```

> 26번이 **이미지 한 장씩 검사하는 실습**이었다면, 29번은 **그 검사 결과 전체를 평가하는 실습**입니다.

---

## 29.1 왜 Accuracy만 계산하지 않나요?

예를 들어 6장 중 5장을 맞혔다면:

```
Accuracy
= 5 / 6
≈ 83.3%
```

입니다.

하지만 **어떤 한 장을 틀렸는가**도 중요합니다.

예를 들어:

```
정상 제품을 NG라고 판단
→ FP

불량 제품을 OK라고 통과
→ FN
```

은 의미가 다릅니다.

특히 이번 제조검사에서는 불량을 찾아내는 것을 중요하게 보기 때문에 **NG를 Positive**로 정합니다.

|실제|프로그램 판정|구분|의미|
|---|---|---|---|
|NG|NG|TP|불량을 올바르게 검출|
|OK|OK|TN|정상을 올바르게 통과|
|OK|NG|FP|정상을 불량으로 잘못 판정|
|NG|OK|FN|불량을 정상으로 잘못 통과|

따라서 이번에는 다음 값을 함께 확인합니다.

```
Accuracy
→ 전체적으로 얼마나 맞혔는가?

NG Precision
→ NG라고 판정한 것 중
   실제 NG는 얼마나 되는가?

NG Recall
→ 실제 NG 중
   얼마나 놓치지 않고 찾아냈는가?

FP
→ 정상 과검출은 몇 건인가?

FN
→ 불량 미검출은 몇 건인가?
```

---

## 29.2 `38_day05_evaluate.py` — Test 결과를 평가합니다

파일을 만듭니다.

```
src/38_day05_evaluate.py
```

다음 코드를 작성합니다.

```python
from pathlib import Path
import shutil
import json

import pandas as pd


# --------------------------------------------------
# 1. Test 결과 CSV와 Baseline Rule JSON 경로 설정
#
# 무엇을 하나요?
# - 앞에서 실행한 Test 결과 CSV의 경로를 정합니다.
# - Test에 사용했던 Baseline Rule JSON 경로를 정합니다.
#
# RESULT_CSV:
# 이미지별 실제 정답, 프로그램 판정,
# TP/TN/FP/FN 등이 기록된 파일입니다.
#
# RULE_PATH:
# Calibration에서 확정하고 동결한
# Baseline Rule 정보가 저장된 JSON 파일입니다.
#
# 왜 필요한가요?
# Test 결과를 평가하고
# 어떤 버전의 Rule을 사용했는지 기록하기 위해서입니다.
# --------------------------------------------------

RESULT_CSV = Path(
    "reports/day05_test_results.csv"
)

RULE_PATH = Path(
    "configs/day05_logo_rules.json"
)


# --------------------------------------------------
# 2. 평가 보고서 및 FP/FN 이미지 저장 경로 설정
#
# 무엇을 하나요?
# - 성능 평가 보고서를 저장할 경로를 정합니다.
# - FP 이미지를 모아 둘 폴더를 지정합니다.
# - FN 이미지를 모아 둘 폴더를 지정합니다.
#
# REPORT_PATH:
# Accuracy, Precision, Recall 등을 기록할
# Markdown 보고서 파일입니다.
#
# FP_DIR:
# 실제 OK인데 NG로 잘못 판정한 이미지 저장 폴더
#
# FN_DIR:
# 실제 NG인데 OK로 잘못 통과한 이미지 저장 폴더
#
# 왜 필요한가요?
# 잘못 판정한 이미지만 따로 모아서
# 어떤 원인으로 오류가 발생했는지 분석하기 위해서입니다.
# --------------------------------------------------

REPORT_PATH = Path(
    "reports/day05_test_metrics.md"
)

FP_DIR = Path(
    "outputs/day05/fp"
)

FN_DIR = Path(
    "outputs/day05/fn"
)


# --------------------------------------------------
# 3. 0으로 나누는 오류를 방지하는 공통 함수
#
# 무엇을 하나요?
# - 두 숫자를 전달받아 나눗셈을 수행합니다.
# - 분모가 0이면 0.0을 반환합니다.
#
# a:
# 분자
#
# b:
# 분모
#
# 예:
# safe_divide(3, 6) → 0.5
# safe_divide(3, 0) → 0.0
#
# 왜 필요한가요?
# Accuracy, Precision, Recall 계산 중
# 분모가 0이 되면 ZeroDivisionError가 발생하기 때문입니다.
#
# 주의:
# 분모가 0인 경우의 0.0은 계산을 위한 기본값입니다.
# 해당 지표가 실제로 0%라는 의미와는 구분해야 합니다.
# --------------------------------------------------

def safe_divide(a, b):

    if b == 0:
        return 0.0

    return a / b


# --------------------------------------------------
# 4. Test 결과 CSV 읽기 및 필수 컬럼 확인
#
# 무엇을 하나요?
# - main() 함수를 정의합니다.
# - Test 결과 CSV가 존재하는지 확인합니다.
# - Pandas로 CSV를 읽습니다.
# - 평가에 필요한 컬럼이 있는지 검사합니다.
#
# 필수 컬럼:
#
# file:
# 검사 이미지 이름
#
# actual:
# 실제 정답인 OK 또는 NG
#
# predicted:
# 프로그램이 판정한 OK 또는 NG
#
# error_type:
# TP / TN / FP / FN
#
# result_image:
# 검사 결과 이미지 저장 경로
#
# 왜 필요한가요?
# 앞 단계에서 만들어진 Test 결과가 있어야
# 전체 성능을 평가할 수 있기 때문입니다.
#
# 필수 컬럼이 없다면 프로그램을 중단합니다.
# --------------------------------------------------

def main():

    # Test 결과 CSV 존재 여부 확인
    if not RESULT_CSV.exists():

        raise FileNotFoundError(
            "Test 결과 CSV가 없습니다. "
            "먼저 37_day05_test.py를 실행하세요."
        )


    # CSV를 Pandas DataFrame으로 읽기
    df = pd.read_csv(
        RESULT_CSV
    )


    # 평가에 필요한 컬럼 목록
    required_columns = {
        "file",
        "actual",
        "predicted",
        "error_type",
        "result_image",
    }


    # CSV에서 누락된 컬럼 찾기
    missing = (
        required_columns
        - set(df.columns)
    )


    # 필수 컬럼이 없으면 오류 발생
    if missing:

        raise RuntimeError(
            f"필요한 컬럼이 없습니다: {missing}"
        )


    # --------------------------------------------------
    # 5. Test에 사용한 Baseline Rule 버전 확인
    #
    # 무엇을 하나요?
    # - Rule 버전의 기본값을 UNKNOWN으로 설정합니다.
    # - JSON 파일이 있으면 내용을 읽습니다.
    # - baseline_version 값을 가져옵니다.
    #
    # 예:
    # day05-logo-v1.0
    #
    # 왜 필요한가요?
    # 어떤 Rule을 사용하여 Test했는지
    # 평가 보고서에 기록하기 위해서입니다.
    #
    # 주의:
    # JSON이 없으면 UNKNOWN으로 기록합니다.
    #
    # 또한 이 코드는 현재 JSON의 버전명을 읽는 것이므로
    # CSV를 생성할 당시 사용한 버전과 동일한지까지
    # 자동으로 검증하지는 않습니다.
    # --------------------------------------------------

    baseline_version = "UNKNOWN"


    if RULE_PATH.exists():

        with RULE_PATH.open(
            "r",
            encoding="utf-8"
        ) as file:

            rules = json.load(
                file
            )


        baseline_version = rules.get(
            "baseline_version",
            "UNKNOWN"
        )


    # --------------------------------------------------
    # 6. Test 결과에서 TP / TN / FP / FN 개수 집계
    #
    # 무엇을 하나요?
    # - CSV의 error_type 컬럼을 확인합니다.
    # - TP, TN, FP, FN이 각각 몇 개인지 계산합니다.
    #
    # 이번 제조검사에서는 NG를 Positive로 정의합니다.
    #
    # TP (True Positive):
    # 실제 NG → 프로그램 NG
    # 불량을 올바르게 검출한 경우
    #
    # TN (True Negative):
    # 실제 OK → 프로그램 OK
    # 정상을 올바르게 통과시킨 경우
    #
    # FP (False Positive):
    # 실제 OK → 프로그램 NG
    # 정상을 불량으로 잘못 판정한 경우
    #
    # FN (False Negative):
    # 실제 NG → 프로그램 OK
    # 불량을 정상으로 잘못 통과시킨 경우
    #
    # value_counts():
    # 각 error_type이 나타난 횟수를 계산합니다.
    #
    # counts.get("TP", 0):
    # TP가 없으면 0을 반환합니다.
    #
    # 왜 필요한가요?
    # 전체 정확도뿐 아니라
    # 어떤 종류의 판정 오류가 발생했는지
    # 확인하기 위해서입니다.
    # --------------------------------------------------

    counts = (
        df["error_type"]
        .value_counts()
        .to_dict()
    )


    # 불량을 올바르게 검출한 개수
    tp = int(
        counts.get("TP", 0)
    )


    # 정상을 올바르게 통과한 개수
    tn = int(
        counts.get("TN", 0)
    )


    # 정상을 NG로 잘못 판정한 개수
    fp = int(
        counts.get("FP", 0)
    )


    # 불량을 OK로 잘못 통과시킨 개수
    fn = int(
        counts.get("FN", 0)
    )


    # TP / TN / FP / FN으로 분류된 전체 이미지 수
    total = (
        tp
        + tn
        + fp
        + fn
    )


    # --------------------------------------------------
    # 7. Accuracy / NG Precision / NG Recall 계산
    #
    # 무엇을 하나요?
    # - 전체 판정 정확도를 계산합니다.
    # - NG라고 판정한 결과의 정밀도를 계산합니다.
    # - 실제 NG를 얼마나 검출했는지 계산합니다.
    #
    # ① Accuracy
    #
    # 전체 이미지 중 올바르게 판정한 비율
    #
    # Accuracy = (TP + TN) / 전체 이미지 수
    #
    # ② NG Precision
    #
    # 프로그램이 NG라고 판정한 이미지 중
    # 실제 NG가 차지하는 비율
    #
    # Precision = TP / (TP + FP)
    #
    # ③ NG Recall
    #
    # 실제 NG 이미지 중
    # 프로그램이 NG로 검출한 비율
    #
    # Recall = TP / (TP + FN)
    #
    # 왜 필요한가요?
    # Accuracy 하나만으로는
    # 정상 과검출과 불량 미검출을
    # 충분히 구분하기 어렵기 때문입니다.
    #
    # 제조검사에서는 특히
    # 실제 불량을 OK로 통과시키는 FN을
    # 중요하게 확인합니다.
    # --------------------------------------------------

    # 전체 정확도
    accuracy = safe_divide(
        tp + tn,
        total
    )


    # NG라고 판정한 것 중 실제 NG의 비율
    # NG를 Positive로 정의합니다.
    precision_ng = safe_divide(
        tp,
        tp + fp
    )


    # 실제 NG 중 올바르게 검출한 비율
    recall_ng = safe_divide(
        tp,
        tp + fn
    )


    # --------------------------------------------------
    # 8. 기존 FP / FN 이미지 폴더 초기화
    #
    # 무엇을 하나요?
    # - 이전 실행에서 저장한 FP/FN 폴더를 확인합니다.
    # - 폴더가 있다면 삭제합니다.
    # - 새로운 빈 FP/FN 폴더를 생성합니다.
    #
    # shutil.rmtree():
    # 폴더와 그 안의 파일을 모두 삭제하는 함수
    #
    # mkdir():
    # 폴더를 만드는 함수
    #
    # 왜 필요한가요?
    # 이전 Test에서 만들어진 실패 이미지가
    # 현재 Test 결과에 섞이지 않도록 하기 위해서입니다.
    #
    # 주의:
    # FP_DIR과 FN_DIR 안의 기존 파일은
    # 모두 삭제되므로 별도 자료를 보관하면 안 됩니다.
    # --------------------------------------------------

    for folder in [
        FP_DIR,
        FN_DIR,
    ]:

        # 기존 폴더가 있다면 삭제
        if folder.exists():

            shutil.rmtree(
                folder
            )


        # 새로운 빈 폴더 생성
        folder.mkdir(
            parents=True,
            exist_ok=True
        )


    # --------------------------------------------------
    # 9. FP / FN으로 잘못 판정한 결과 이미지를 분리
    #
    # 무엇을 하나요?
    # - Test 결과 CSV의 각 행을 확인합니다.
    # - 각 이미지의 error_type을 읽습니다.
    # - 결과 이미지 경로를 확인합니다.
    #
    # FP인 경우:
    # outputs/day05/fp/ 폴더에 복사
    #
    # FN인 경우:
    # outputs/day05/fn/ 폴더에 복사
    #
    # shutil.copy2():
    # 원본 파일을 보존하면서 파일을 복사합니다.
    # 가능한 파일 메타데이터도 함께 보존합니다.
    #
    # 왜 필요한가요?
    # 정상인데 NG로 잘못 판정한 이미지와
    # 불량인데 OK로 잘못 통과한 이미지를
    # 구분해서 분석하기 위해서입니다.
    #
    # 주의:
    # 결과 이미지 파일이 없으면
    # 현재 코드는 해당 행을 건너뜁니다.
    # 따라서 오류 개수와 복사된 이미지 수가
    # 다를 수 있습니다.
    # --------------------------------------------------

    for _, row in df.iterrows():

        # 현재 이미지의 오류 유형
        error_type = row[
            "error_type"
        ]


        # 검사 결과 이미지 경로
        source = Path(
            row["result_image"]
        )


        # 이미지가 없으면 건너뛰기
        if not source.exists():
            continue


        # FP: 실제 OK → 프로그램 NG
        if error_type == "FP":

            shutil.copy2(
                source,
                FP_DIR / source.name
            )


        # FN: 실제 NG → 프로그램 OK
        elif error_type == "FN":

            shutil.copy2(
                source,
                FN_DIR / source.name
            )


    # --------------------------------------------------
    # 10. 전체 Test 성능을 Markdown 보고서로 저장
    #
    # 무엇을 하나요?
    # - 보고서를 저장할 폴더를 준비합니다.
    # - Baseline Rule 버전을 기록합니다.
    # - TP/TN/FP/FN을 Confusion Matrix로 정리합니다.
    # - Accuracy, Precision, Recall을 기록합니다.
    # - FP와 FN의 의미를 설명합니다.
    #
    # Confusion Matrix:
    # 실제 정답과 프로그램 판정을 비교하는 표입니다.
    #
    # 보고서 파일:
    # reports/day05_test_metrics.md
    #
    # 왜 필요한가요?
    # Test 결과를 문서로 남겨
    # 이후 Baseline 성능과 실패 원인을
    # 확인할 수 있도록 하기 위해서입니다.
    #
    # 주의:
    # 이 보고서는 집계된 평가 결과를 기록합니다.
    # 실제 Failure Cause를 자동으로 분석하지는 않습니다.
    # --------------------------------------------------

    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    # Markdown 형식의 보고서 내용 작성
    report = f"""# Day05 Test Metrics

## Baseline

- Rule Version: {baseline_version}
- Positive Class: NG
- Test Images: {total}

## Confusion Matrix

| Actual / Predicted | NG | OK |
|---|---:|---:|
| NG | TP = {tp} | FN = {fn} |
| OK | FP = {fp} | TN = {tn} |

## Metrics

- Accuracy: {accuracy:.4f}
- NG Precision: {precision_ng:.4f}
- NG Recall: {recall_ng:.4f}
- FP: {fp}
- FN: {fn}

## Interpretation

- FP: 실제 OK인데 NG로 잘못 판정
- FN: 실제 NG인데 OK로 잘못 통과
"""


    # Markdown 파일 저장
    REPORT_PATH.write_text(
        report,
        encoding="utf-8"
    )


    # --------------------------------------------------
    # 11. 전체 평가 결과와 저장 경로를 터미널에 출력
    #
    # 무엇을 하나요?
    # - 사용한 Rule 버전을 출력합니다.
    # - Test 이미지 개수를 출력합니다.
    # - TP/TN/FP/FN을 출력합니다.
    # - Accuracy, Precision, Recall을 출력합니다.
    # - 평가 보고서와 FP/FN 이미지 폴더 경로를 출력합니다.
    #
    # 왜 필요한가요?
    # 평가 결과를 파일로 열기 전에도
    # 터미널에서 전체 성능을 확인하기 위해서입니다.
    # --------------------------------------------------

    print("=" * 70)

    print(
        "Day05 Test Evaluation"
    )

    print("=" * 70)


    # 사용한 Baseline Rule 버전
    print(
        "Rule:",
        baseline_version
    )


    # 전체 평가 이미지 수
    print(
        "Test Images:",
        total
    )

    print()


    # TP / TN / FP / FN 출력
    print(
        "TP:",
        tp
    )

    print(
        "TN:",
        tn
    )

    print(
        "FP:",
        fp
    )

    print(
        "FN:",
        fn
    )

    print()


    # Accuracy 출력
    print(
        "Accuracy:",
        round(
            accuracy,
            4
        )
    )


    # NG Precision 출력
    print(
        "NG Precision:",
        round(
            precision_ng,
            4
        )
    )


    # NG Recall 출력
    print(
        "NG Recall:",
        round(
            recall_ng,
            4
        )
    )

    print()


    # 결과물 저장 경로 확인
    print(
        "평가 보고서:",
        REPORT_PATH
    )

    print(
        "FP 이미지:",
        FP_DIR
    )

    print(
        "FN 이미지:",
        FN_DIR
    )


# --------------------------------------------------
# 12. Python 파일을 직접 실행하면 main() 호출
#
# 무엇을 하나요?
# - 현재 파일이 직접 실행되었는지 확인합니다.
# - 직접 실행했다면 main() 함수를 호출합니다.
#
# 왜 필요한가요?
# 다른 파일에서 이 코드를 import할 때
# 평가 작업이 자동 실행되지 않도록 하기 위해서입니다.
#
# 실행 명령어:
# python src/38_day05_evaluate.py
# --------------------------------------------------

if __name__ == "__main__":
    main()
```

실행합니다

```
python src/38_day05_evaluate.py
```

### 의사코드

```
[1. Test 결과 CSV와 Baseline Rule JSON 경로 설정]

Test 결과 CSV 경로를 정한다.

reports/day05_test_results.csv

사용한 Baseline Rule JSON 경로를 정한다.

configs/day05_logo_rules.json

          ↓

[2. 평가 보고서 및 FP/FN 이미지 저장 경로 설정]

평가 보고서 경로를 정한다.

reports/day05_test_metrics.md

FP 이미지 저장 폴더를 정한다.

outputs/day05/fp/

FN 이미지 저장 폴더를 정한다.

outputs/day05/fn/

          ↓

[3. 0으로 나누는 오류 방지 함수]

safe_divide() 함수를 만든다.

분자 a와 분모 b를 전달받는다.

          ↓

분모가 0인지 확인한다.

분모가 0이면 0.0을 반환한다.

분모가 0이 아니면
a / b 결과를 반환한다.

          ↓

[4. Test 결과 CSV 읽기 및 필수 컬럼 확인]

main() 함수를 시작한다.

Test 결과 CSV가 있는지 확인한다.

파일이 없다면 오류를 발생시킨다.

          ↓

Pandas로 CSV를 읽는다.

          ↓

필수 컬럼이 있는지 확인한다.

file
actual
predicted
error_type
result_image

          ↓

필수 컬럼이 누락되었다면
오류를 발생시킨다.

모든 컬럼이 있다면
다음 단계로 이동한다.

          ↓

[5. Test에 사용한 Baseline Rule 버전 확인]

Baseline Rule 버전의 기본값을
UNKNOWN으로 설정한다.

          ↓

Rule JSON 파일이 있는지 확인한다.

파일이 있다면 JSON을 읽는다.

          ↓

baseline_version 값을 가져온다.

예:
day05-logo-v1.0

          ↓

[6. TP / TN / FP / FN 개수 집계]

Test 결과 CSV의
error_type 컬럼을 확인한다.

          ↓

실제 NG이고 프로그램 판정도 NG인
TP 개수를 센다.

실제 OK이고 프로그램 판정도 OK인
TN 개수를 센다.

실제 OK인데 프로그램이 NG라고 판정한
FP 개수를 센다.

실제 NG인데 프로그램이 OK라고 판정한
FN 개수를 센다.

          ↓

TP + TN + FP + FN

을 계산한다.

전체 평가 이미지 개수를 구한다.

          ↓

[7. Accuracy / NG Precision / NG Recall 계산]

전체 정확도 Accuracy를 계산한다.

Accuracy =
(TP + TN) / 전체 이미지 수

          ↓

NG Precision을 계산한다.

Precision =
TP / (TP + FP)

          ↓

NG Recall을 계산한다.

Recall =
TP / (TP + FN)

          ↓

계산 과정에서 분모가 0이면
safe_divide()가 0.0을 반환한다.

          ↓

[8. 기존 FP / FN 이미지 폴더 초기화]

FP 이미지 폴더가 있는지 확인한다.

폴더가 있으면 삭제한다.

새로운 빈 FP 폴더를 생성한다.

          ↓

FN 이미지 폴더가 있는지 확인한다.

폴더가 있으면 삭제한다.

새로운 빈 FN 폴더를 생성한다.

          ↓

이전 실행에서 저장한 이미지가
현재 결과에 섞이지 않도록 준비한다.

          ↓

[9. FP / FN 결과 이미지 분리]

Test 결과 CSV를 한 행씩 읽는다.

          ↓

현재 이미지의 error_type을 확인한다.

결과 이미지 경로를 가져온다.

          ↓

결과 이미지 파일이 없다면
현재 행을 건너뛴다.

          ↓

error_type이 FP이면

결과 이미지를
outputs/day05/fp/ 폴더에 복사한다.

          ↓

error_type이 FN이면

결과 이미지를
outputs/day05/fn/ 폴더에 복사한다.

          ↓

나머지 Test 결과도 같은 과정을 반복한다.

          ↓

[10. 전체 Test 성능을 Markdown 보고서로 저장]

평가 보고서 저장 폴더를 준비한다.

          ↓

Baseline Rule 버전을 기록한다.

Positive Class가 NG임을 기록한다.

Test 이미지 개수를 기록한다.

          ↓

Confusion Matrix를 작성한다.

실제 NG / 예측 NG → TP
실제 NG / 예측 OK → FN
실제 OK / 예측 NG → FP
실제 OK / 예측 OK → TN

          ↓

Accuracy를 기록한다.

NG Precision을 기록한다.

NG Recall을 기록한다.

FP 개수를 기록한다.

FN 개수를 기록한다.

          ↓

FP와 FN의 의미를 설명한다.

          ↓

day05_test_metrics.md 파일로 저장한다.

          ↓

[11. 전체 평가 결과를 터미널에 출력]

사용한 Baseline Rule 버전을 출력한다.

전체 Test 이미지 개수를 출력한다.

          ↓

TP를 출력한다.
TN을 출력한다.
FP를 출력한다.
FN을 출력한다.

          ↓

Accuracy를 출력한다.

NG Precision을 출력한다.

NG Recall을 출력한다.

          ↓

평가 보고서 경로를 출력한다.

FP 이미지 폴더 경로를 출력한다.

FN 이미지 폴더 경로를 출력한다.

          ↓

[12. 프로그램 실행]

Python 파일을 직접 실행했는지 확인한다.

직접 실행했다면
main() 함수를 호출한다.

          ↓

[최종 결과]

37_day05_test.py
        ↓
Test 이미지 6장 검사 결과
        ↓
day05_test_results.csv
        ↓
38_day05_evaluate.py
        ↓
TP / TN / FP / FN 집계
        ↓
Accuracy 계산
        ↓
NG Precision 계산
        ↓
NG Recall 계산
        ↓
FP / FN 이미지 분리
        ↓
┌────────────────────────────────┐
│ 결과 1                          │
│ day05_test_metrics.md          │
│ 전체 Test 성능 평가 보고서        │
└────────────────────────────────┘
        +
┌────────────────────────────────┐
│ 결과 2                          │
│ outputs/day05/fp/              │
│ 정상 이미지를 NG로 잘못 판정      │
│ FP 이미지 저장                  │
└────────────────────────────────┘
        +
┌────────────────────────────────┐
│ 결과 3                          │
│ outputs/day05/fn/              │
│ 불량 이미지를 OK로 잘못 통과      │
│ FN 이미지 저장                  │
└────────────────────────────────┘
        ↓
실패한 이미지 확인
        ↓
NG Reason과 실제 Failure Cause 구분
        ↓
Baseline Rule의 한계 분석
        ↓
5일차 Test 평가 완료
```

---

## 29.3 실행 결과를 확인합니다

실제 실행 결과는 다음과 같습니다.

```
======================================================================
Day05 Test Evaluation
======================================================================
Rule: day05-logo-v1.0
Test Images: 6

TP: 3
TN: 0
FP: 3
FN: 0

Accuracy: 0.5
NG Precision: 0.5
NG Recall: 1.0

평가 보고서: reports/day05_test_metrics.md
FP 이미지: outputs/day05/fp
FN 이미지: outputs/day05/fn
```

평가 결과는 다음 파일에도 저장됩니다.

```
reports/day05_test_metrics.md
```

그리고 오판정 이미지는 오류 종류에 따라 별도 폴더로 모입니다.

```
outputs/day05/fp/
→ FP 이미지 저장

outputs/day05/fn/
→ FN 이미지 저장
```

이번 실제 결과에서는:

```
FP = 3
FN = 0
```

이므로:

```
outputs/day05/fp/
├── test_ok_01_result.jpg
├── test_ok_02_result.jpg
└── test_ok_03_result.jpg

outputs/day05/fn/
└── 비어 있음
```

이 맞습니다.

즉 전체 결과 구조는 다음과 같습니다.

```
Test 결과 CSV
        ↓
38_day05_evaluate.py
        ↓
├─ 성능 보고서
│  reports/day05_test_metrics.md
│
├─ FP 이미지
│  outputs/day05/fp/
│  → 3장
│
└─ FN 이미지
   outputs/day05/fn/
   → 0장
```

> `fn` 폴더가 비어 있는 것은 오류가 아니라, 이번 Test에서 불량을 OK로 잘못 통과시킨 경우가 없었다는 뜻입니다.

---

# 30. 실제 평가 결과를 어떻게 읽나요?

이번 Test의 실제 성능은 다음과 같습니다.

```
TP = 3
TN = 0
FP = 3
FN = 0

Accuracy = 0.5000
NG Precision = 0.5000
NG Recall = 1.0000
```

하나씩 읽어보겠습니다.

### Accuracy = 0.5

```
6장 중
올바르게 판정한 이미지 = 3장

3 / 6
= 0.5
= 50%
```

즉 전체 Test 이미지의 **절반을 올바르게 판정했습니다.**

---

### NG Precision = 0.5

이번 프로그램은 Test 6장을 **모두 NG라고 판정**했습니다.

그중 실제 NG는 3장이었습니다.

```
프로그램이 NG라고 판정
→ 6장

그중 실제 NG
→ 3장

3 / 6
= 0.5
= 50%
```

즉:

> NG라고 판정한 이미지 중 절반만 실제 NG였습니다.

정상 제품도 3장이나 NG라고 판정했기 때문에 Precision이 낮아졌습니다.

---

### NG Recall = 1.0

실제 NG는 3장이었습니다.

```
실제 NG
→ 3장

프로그램이 NG로 검출
→ 3장

3 / 3
= 1.0
= 100%
```

즉:

> 실제 불량 3장은 하나도 놓치지 않고 모두 검출했습니다.

그래서:

```
FN = 0
```

입니다.

---

## 30.1 이번 결과를 한눈에 보면

|실제 상태|프로그램 판정|개수|결과|
|---|---|---|---|
|NG|NG|3|TP|
|NG|OK|0|FN|
|OK|OK|0|TN|
|OK|NG|3|FP|

쉽게 말하면:

```
불량 검출
NG 3장
→ 모두 잡음
→ 좋음

하지만

정상 통과
OK 3장
→ 모두 NG로 잘못 판정
→ 문제
```

따라서 현재 Baseline은:

> 불량을 놓치지는 않았지만, 정상 제품까지 너무 엄격하게 NG로 판정하는 Rule

이라고 해석할 수 있습니다.

---

## 30.2 FP 이미지를 직접 확인합니다

이번 Test에서는 FP가 3건 발생했습니다.

```
outputs/day05/fp/
```

에 다음 이미지가 저장되어 있습니다.

```
test_ok_01_result.jpg
test_ok_02_result.jpg
test_ok_03_result.jpg
```

세 이미지 모두:

```
Actual
→ OK

Predicted
→ NG

Error Type
→ FP
```

입니다.

그런데 측정값을 살펴보면 공통적인 특징이 있습니다.

|파일|SIFT Good|기준 129|Inlier Ratio|기준 0.8664|
|---|---|---|---|---|
|`test_ok_01.jpg`|169|통과|0.7811|실패|
|`test_ok_02.jpg`|156|통과|0.8397|실패|
|`test_ok_03.jpg`|204|통과|0.8529|실패|

즉 세 정상 이미지 모두:

```
Homography
→ 성공

SIFT Good Match
→ 기준 통과

하지만

Inlier Ratio
→ 기준 미달
```

이었습니다.

따라서 세 FP의 직접적인 `NG Reason`은 모두:

```
LOW_INLIER_RATIO
```

입니다.

---

## 30.3 FN 폴더에는 왜 이미지가 없나요?

이번 결과는:

```
FN = 0
```

입니다.

FN은:

```
실제 NG
        ↓
프로그램이 OK라고 판정
```

한 경우입니다.

이번에는 실제 NG 3장을 모두 NG로 검출했기 때문에:

```
outputs/day05/fn/
```

에 복사할 이미지가 없습니다.

즉 폴더가 비어 있는 것이 정상 결과입니다.

---

## 30.4 NG Reason과 실제 Failure Cause를 구분합니다

이번 FP 3장의 `NG Reason`은 모두 명확합니다.

```
LOW_INLIER_RATIO
```

이것은:

```
Inlier Ratio
<
0.8664
```

였다는 **프로그램 내부의 직접적인 판정 이유**입니다.

하지만 왜 정상 이미지의 Inlier Ratio가 낮아졌는지는 별도로 살펴봐야 합니다.

실제 이미지를 보면서 다음과 같은 조건을 확인합니다.

```
Calibration 이미지와
촬영 각도가 달랐는가?

제품 크기나 거리가 달랐는가?

포장지 구김이 달라졌는가?

빛 반사가 있었는가?

로고의 보이는 형태가
Calibration과 달라졌는가?
```

정리하면:

```
NG Reason
→ LOW_INLIER_RATIO
→ 프로그램이 NG라고 한 직접 이유

Failure Cause
→ 왜 Inlier Ratio가 낮아졌는가?
→ 실제 이미지를 보고 원인 분석
```

입니다.

---

# 31. Test에서 틀렸다고 바로 Rule을 바꾸지 않습니다

이번 Test에서는 정상 이미지 3장이 모두 FP가 되었습니다.

결과만 보면:

```
Inlier Ratio 기준
0.8664

        ↓

너무 높은 것 아닌가?

        ↓

기준을 낮추면 되지 않을까?
```

라고 생각할 수 있습니다.

하지만 **지금 바로 Threshold를 수정하지 않습니다.**

이번 Test의 목적은:

> **Calibration에서 만든 `day05-logo-v1.0`이 처음 보는 데이터에서 실제로 얼마나 잘 작동하는지 확인하는 것**

이기 때문입니다.

---

## 31.1 이번 결과에서 왜 바로 수정하지 않나요?

현재 실제 결과를 보면:

```
Calibration

Accuracy
→ 91.67%

        ↓

같은 Rule을 Test에 적용

        ↓

Test Accuracy
→ 50%
```

로 성능이 크게 떨어졌습니다.

그리고 정상 Test 이미지 세 장에서 공통적으로:

```
LOW_INLIER_RATIO
```

가 발생했습니다.

이것은 매우 중요한 결과입니다.

```
Calibration에서는 잘 동작했던 기준

        ↓

처음 보는 정상 이미지에서는
Inlier Ratio가 기준보다 낮아짐

        ↓

FP 3건 발생
```

즉 현재 Baseline이 **새로운 정상 이미지의 변화까지 충분히 받아들이지 못하고 있을 가능성**을 확인한 것입니다.

여기서 바로:

```
0.8664
↓
0.84
```

처럼 바꾸면 Test 데이터를 보고 Rule을 맞추는 것이 됩니다.

그러면 더 이상 이 Test 데이터로 현재 Baseline의 객관적인 성능을 평가하기 어렵습니다.

---

## 31.2 이번 실패 결과를 먼저 기록합니다

이번 Test에서는 FP 3건의 공통점을 다음과 같이 기록할 수 있습니다.

```
Baseline
day05-logo-v1.0

Actual
OK

Predicted
NG

FP
3건

공통 NG Reason
LOW_INLIER_RATIO

SIFT Good Match
→ 정상 3장 모두 기준 통과

Homography
→ 정상 3장 모두 계산 성공

Inlier Ratio
→ 정상 3장 모두 0.8664 미만
```

대표적으로:

```
test_ok_01.jpg

Actual
→ OK

Predicted
→ NG

SIFT Good Match
→ 169
→ 기준 통과

Inlier Ratio
→ 0.7811
→ 기준 미달

Error Type
→ FP

NG Reason
→ LOW_INLIER_RATIO
```

입니다.

다른 두 정상 이미지도 같은 유형입니다.

```
test_ok_02
Ratio = 0.8397
→ LOW_INLIER_RATIO

test_ok_03
Ratio = 0.8529
→ LOW_INLIER_RATIO
```

따라서 이번 Test에서 확인한 핵심은:

```
Test 실패
        ↓
즉시 Threshold 수정 X
        ↓
FP 이미지 확인
        ↓
공통 NG Reason 확인

LOW_INLIER_RATIO
        ↓
왜 정상 이미지에서
Ratio가 낮아졌는지 분석
        ↓
현재 Baseline의 한계로 기록
```

입니다.

> 현재 `day05-logo-v1.0`은 불량 3장을 모두 검출하여 NG Recall은 100%였지만, 정상 3장도 모두 NG로 판정하여 FP가 3건 발생했습니다. 따라서 현재 Rule은 불량 검출에는 강하지만 정상 제품을 통과시키는 데에는 지나치게 엄격한 특성을 보였습니다.

---

# PART7 Mini Challenge — 다른 제품으로 5일차 흐름을 스스로 반복합니다 (32~38)

### Mini Challenge 주제

> 다른 제품의 로고가 정상적으로 보이는지 검사하는 Rule을 직접 만들어 보세요.

제품은 팀별로 다음 중 하나를 선택하게 하면 좋습니다.

```
과자 봉지 로고
음료수 라벨
라면 봉지 로고
제품 박스 로고
책 또는 노트 표지
```

가능하면 글자와 모서리가 뚜렷하고 로고가 크게 보이는 제품을 선택합니다.

데이터는 직접 촬영을 합니다.

```
Reference
1장
→ 정면에서 정상 로고 촬영

Calibration OK
3장
→ 위치 / 거리 / 각도를 조금씩 변화

Calibration NG
3장
→ 로고 일부를 카드나 종이로 가림

Test OK
2장
→ Calibration에 사용하지 않은 새 사진

Test NG
2장
→ 다른 위치를 가린 새 사진
```

총:

```
Reference 1장
+
Calibration 6장
+
Test 4장

= 11장
```

이면 충분합니다.

특히 NG는 실제 제품을 훼손할 필요 없이:

```
포스트잇
종이
카드

        ↓

로고 일부 가림
```

으로 만들면 됩니다.

---
# 32. Mini Challenge에서는 무엇을 하나요?

지금까지 광천김을 이용하여 다음 과정을 함께 실습했습니다.

```
Reference 준비
        ↓
Calibration 이미지 측정
        ↓
Template / SIFT / Homography 값 확인
        ↓
OK / NG 분포 비교
        ↓
Threshold 후보 선택
        ↓
Rule 결정
        ↓
JSON으로 Rule Freeze
        ↓
처음 보는 Test 이미지 검사
        ↓
TP / TN / FP / FN 확인
        ↓
실패 원인 분석
```

Mini Challenge에서는 이 과정을 다른 제품에서 직접 다시 해봅니다.

새로운 알고리즘을 배우는 문제가 아닙니다.

> 5일차에서 배운 검사 개발 순서를 스스로 다시 적용할 수 있는지 확인하는 실습입니다.

강사는 광천김과 다른 간단한 제품 이미지를 제공합니다.

예:

```
과자 봉지 로고
음료수 라벨
제품 박스 로고
책 표지
인쇄 카드
```

가능하면 글자와 모서리가 어느 정도 있는 제품을 선택하는 것이 좋습니다.

---

# 33. Mini Challenge 데이터는 작게 준비합니다

Mini Challenge는 대규모 성능평가가 아닙니다.

작은 데이터로 전체 흐름을 다시 경험하는 것이 목적입니다.

권장 데이터는 다음 정도면 충분합니다.

```
Reference
→ 1장

Calibration
→ OK 3장
→ NG 3장

Test
→ OK 2장
→ NG 2장
```

예:

```
samples/day05/mini_challenge/
│
├── reference/
│   └── reference_label.jpg
│
├── calibration/
│   ├── ok/
│   │   ├── ok_01.jpg
│   │   ├── ok_02.jpg
│   │   └── ok_03.jpg
│   │
│   └── ng/
│       ├── ng_01.jpg
│       ├── ng_02.jpg
│       └── ng_03.jpg
│
└── test/
    ├── ok/
    │   ├── test_ok_01.jpg
    │   └── test_ok_02.jpg
    │
    └── ng/
        ├── test_ng_01.jpg
        └── test_ng_02.jpg
```

Mini Challenge에서는 별도의 `Lighting / Rotation / Blur / Glare` 스트레스 테스트 데이터를 추가로 만들지 않습니다.

5일차의 핵심은 `Calibration → Rule Freeze → Test → 실패 분석`의 전체 흐름을 다른 제품에 다시 적용하는 것이므로, Mini Challenge도 이 범위에 집중합니다.

---

# 34. 해야 할 일을 순서대로 확인합니다

Mini Challenge에서는 다음 순서를 지킵니다.

```
① 검사 대상 확인
        ↓
② Reference 준비
        ↓
③ Calibration OK / NG 측정
        ↓
④ 측정값 비교
        ↓
⑤ 사용할 Feature 선택
        ↓
⑥ Threshold 결정
        ↓
⑦ Rule 고정
        ↓
⑧ Test 실행
        ↓
⑨ 실제 정답과 비교
        ↓
⑩ 결과 해석
```

## 34.1 어떤 Feature를 사용할까요?

5일차에서 실제로 측정한 다음 값 중에서 선택합니다.

```
Template Score

SIFT Good Match

Homography Inlier

Inlier Ratio
```

최소 **2개 정도를 비교**하면 충분합니다.

광천김 실습에서는 실제 데이터를 확인한 결과:

```
SIFT Good Match
+
Inlier Ratio
```

를 사용했습니다.

하지만 새로운 제품에서도 똑같은 값이 가장 좋다는 보장은 없습니다.

먼저 측정값을 보고 판단합니다.

```
Template Score는
OK / NG 차이가 있는가?

SIFT Good Match는
어느 쪽이 높은가?

Inlier Ratio는
정상과 불량을 구분하는 데 도움이 되는가?
```

> Feature를 많이 사용하는 것이 목표가 아니라 **새로운 데이터에서 실제로 도움이 되는 Feature를 선택하는 것**이 목표입니다.

현재 공통 함수에서 측정하지 않는 `Position Error`, `Scale Ratio`는 이번 Mini Challenge에서는 사용하지 않습니다.

---

# 35. `39_day05_mini_challenge.py` — 직접 완성합니다

본 실습의 실행 파일은 `38_day05_evaluate.py`까지 이어졌습니다.

Mini Challenge에서는 다음 파일을 사용합니다.

```
src/39_day05_mini_challenge.py
```

이번에는 정답 코드를 모두 제공하지 않습니다.

학생은 오늘 만든 코드를 참고하여 필요한 부분을 직접 완성합니다.

```python
from pathlib import Path

from day05_logo_features import (
    prepare_reference,
    measure_target,
)


ROOT = Path(
    "samples/day05/mini_challenge"
)

REFERENCE_PATH = (
    ROOT
    / "reference/reference_label.jpg"
)

CALIBRATION_DIR = (
    ROOT
    / "calibration"
)

TEST_DIR = (
    ROOT
    / "test"
)


# --------------------------------------------------
# TODO 1
#
# Reference를 준비합니다.
#
# prepare_reference()를 사용합니다.
# --------------------------------------------------


# --------------------------------------------------
# TODO 2
#
# calibration/ok
# calibration/ng
#
# 이미지를 모두 읽어서 측정합니다.
#
# 확인할 값:
#
# template_score
# sift_good_matches
# homography_found
# homography_inliers
# inlier_ratio
# --------------------------------------------------


# --------------------------------------------------
# TODO 3
#
# OK와 NG 측정값을 비교합니다.
#
# 어떤 Feature가 구분에 도움이 되는지
# 최소 2개 확인합니다.
# --------------------------------------------------


# --------------------------------------------------
# TODO 4
#
# Calibration 결과를 보고
# Threshold를 결정합니다.
#
# 예:
#
# SIFT >= ?
# Inlier Ratio >= ?
#
# 숫자를 임의로 정하지 않습니다.
# --------------------------------------------------


# --------------------------------------------------
# TODO 5
#
# 결정한 Rule을 고정합니다.
#
# Test를 시작한 뒤에는
# Threshold를 수정하지 않습니다.
# --------------------------------------------------


# --------------------------------------------------
# TODO 6
#
# test/ok
# test/ng
#
# 이미지에 같은 Rule을 적용합니다.
# --------------------------------------------------


# --------------------------------------------------
# TODO 7
#
# Actual과 Predicted를 비교합니다.
#
# TP
# TN
# FP
# FN
#
# 을 확인합니다.
# --------------------------------------------------


print(
    "Day05 Mini Challenge를 완성하세요."
)
```

다음 코드를 참고할 수 있습니다.

```
day05_logo_features.py

34_day05_measure_calibration.py
→ 여러 이미지 측정 방법

35_day05_analyze_calibration.py
→ 측정값 비교와 Threshold 후보

36_day05_freeze_rule.py
→ Rule 저장 방법

37_day05_test.py
→ Test 적용 방법

38_day05_evaluate.py
→ TP / TN / FP / FN 계산 방법
```

중요한 것은 코드를 전부 암기하는 것이 아닙니다.

```
어떤 기존 코드를
어디에서 재사용해야 하는가?
```

를 스스로 판단하는 것도 Mini Challenge의 일부입니다.

---

# 36. Mini Challenge는 이 정도까지만 하면 됩니다

반드시 확인할 결과는 다음입니다.

```
Calibration에서

OK와 NG의 측정값이
어떻게 달랐는가?

        ↓

어떤 Feature를 선택했는가?

        ↓

Threshold를 얼마로 정했는가?

        ↓

Test에서

몇 장을 맞혔는가?

        ↓

FP / FN이 있었는가?
```

정확도가 낮게 나왔다고 Mini Challenge 실패가 아닙니다.

예를 들어:

```
Test 4장 중
3장 성공
1장 실패
```

했다면 실패한 한 장을 확인합니다.

```
실제 상태
→ OK

프로그램 판정
→ NG

SIFT Good Match
→ Threshold보다 낮음

가능한 이유
→ 촬영 각도 또는 Blur
```

정도만 설명할 수 있어도 충분합니다.

> 좋은 숫자를 만드는 것보다 자신이 만든 Rule이 왜 그렇게 동작했는지 설명할 수 있는 것이 더 중요합니다.

---

# 37. Mini Challenge 결과를 짧게 기록합니다

결과는 다음 파일 하나에 간단히 작성합니다.

```
reports/day05_mini_challenge.md
```

다음 정도면 충분합니다.

```
# Day05 Mini Challenge

## 검사 대상

작성:

## OK 기준

작성:

## NG 기준

작성:

## Calibration 데이터

- OK: 3장
- NG: 3장

## 확인한 Feature

- Feature 1:
- Feature 2:

## Calibration 결과

### OK

작성:

### NG

작성:

## 선택한 Rule

예:

SIFT Good Match >= ?

AND

Inlier Ratio >= ?

## Test 결과

- Test 이미지: 4장
- TP:
- TN:
- FP:
- FN:

## 가장 눈에 띄는 결과

파일:

Actual:

Predicted:

측정값:

왜 이런 결과가 나왔다고 생각하는가?

작성:

## 한 줄 정리

이번 제품에서 어떤 Feature가 가장 유용했는가?

작성:
```

별도의 긴 Failure Analysis 보고서나 Experiment Log를 다시 작성할 필요는 없습니다.

---

# 38. Mini Challenge 완료 기준

다음 항목까지 수행했다면 Mini Challenge는 완료입니다.

- [ ] 광천김과 다른 제품을 사용했다.
- [ ] Reference 이미지를 준비했다.
- [ ] Calibration OK / NG를 구분했다.
- [ ] Calibration 이미지를 실제로 측정했다.
- [ ] 최소 2개의 Feature를 비교했다.
- [ ] 측정값을 보고 Threshold를 결정했다.
- [ ] Test 전에 Rule을 고정했다.
- [ ] Test 이미지에 같은 Rule을 적용했다.
- [ ] TP / TN / FP / FN을 확인했다.
- [ ] 틀린 결과가 있다면 원인을 한 건 이상 확인했다.
- [ ] day05_mini_challenge.md에 결과를 짧게 기록했다.

Mini Challenge에서는 다음까지 할 필요는 없습니다.

```
새로운 AI 모델 학습 X

OCR 추가 X

Anomaly Detection 추가 X

GUI 제작 X

별도의 Lighting / Rotation / Blur / Glare
스트레스 테스트 추가 X

새로운 Feature 알고리즘 개발 X

높은 Accuracy가 나올 때까지
Threshold 반복 수정 X
```
---
# PART8 5일차 정리 · 자가체크 · Git 기록 (39~43)

---

# 39. README에 5일차 결과를 정리합니다

5일차에서 무엇을 했는지 나중에도 확인할 수 있도록 `README.md`에 핵심 결과만 기록합니다.

다음 형식을 참고하여 **자신이 실제 실행한 결과**를 작성합니다.

```
## Day 05 — Calibration · Rule Freeze · Test

### 검사 대상

광천김 포장지의 기준 로고 존재 및 정합 검사

### 사용한 기술

- Template Matching
- SIFT
- RANSAC
- Homography

### Calibration

- OK: 6장
- NG: 6장
- 측정값:
  - Template Score
  - SIFT Good Match
  - Homography Inlier
  - Inlier Ratio

### Baseline Rule

- Version: day05-logo-v1.0
- Homography Found: True
- SIFT Good Match >= 129
- Inlier Ratio >= 0.8664

### Test

- Test 이미지: 6장
- Accuracy:
- TP:
- TN:
- FP:
- FN:
- NG Precision:
- NG Recall:

### Test 실패 분석

- FP: 3
- FN: 0
- 공통 NG Reason: `LOW_INLIER_RATIO`
- Test 결과를 보고 Threshold를 다시 맞추지 않고 현재 Baseline의 한계로 기록

### Mini Challenge

검사한 다른 제품:

작성:

선택한 Feature:

작성:

Test 결과:

작성:

### 핵심 결과 파일

- reports/day05_calibration_measurements.csv
- reports/day05_rule_candidates.csv
- configs/day05_logo_rules.json
- reports/day05_test_results.csv
- reports/day05_test_metrics.md
- reports/day05_mini_challenge.md

### 오늘의 핵심

Calibration 데이터로 판정 기준을 결정하고,
기준을 동결한 뒤 처음 보는 Test 데이터에 적용했다.

Test 결과에서는 Accuracy뿐 아니라 FP와 FN을 확인했고,
FP 3건의 공통 NG Reason을 분석하여 현재 Baseline의 한계를 확인했다.
```

README는 보고서를 길게 다시 작성하는 문서가 아닙니다.

> **5일차에 무엇을 만들었고 어떤 결과가 나왔는지 다시 확인할 수 있을 정도만 기록하면 됩니다.**

---

# 40. 5일차 결과를 Git에 기록합니다

먼저 변경된 파일을 확인합니다.

```bash
git status
```

5일차에서 작성한 코드와 설정, 보고서, README를 추가합니다.

```bash
git add src configs reports README.md
```

Commit 합니다.

```bash
git commit -m "feat: complete day05 calibration rule test"
```

정상적으로 기록되었는지 확인합니다.

```bash
git log --oneline -5
```

5일차 Baseline을 별도로 표시하고 싶다면 Tag를 남길 수도 있습니다.

```bash
git tag day05-logo-v1.0
```

확인합니다.

```bash
git tag
```

---

## 40.1 GitHub 사용이 허용된 환경이라면 업로드합니다

Remote가 이미 연결되어 있다면:

```bash
git remote -v
```

를 먼저 확인합니다.

현재 브랜치를 확인합니다.

```bash
git branch --show-current
```

예를 들어 `main` 브랜치라면:

```bash
git push origin main
```

Tag까지 업로드하려면:

```bash
git push origin day05-logo-v1.0
```

합니다.

기관 정책상 외부 GitHub 업로드가 허용되지 않는 환경에서는 **`git push`를 하지 않고 Local Git Commit까지만** 진행합니다.

---

# 41. 5일차 자가체크

수업을 마치기 전에 직접 확인합니다.

## 데이터와 측정

- [ ]  Calibration과 Test의 역할 차이를 설명할 수 있다.
- [ ]  Calibration OK 6장과 NG 6장을 측정했다.
- [ ]  Template Score를 확인했다.
- [ ]  SIFT Good Match를 확인했다.
- [ ]  Homography Inlier와 Inlier Ratio를 확인했다.
- [ ]  한 장의 측정값만 보고 Threshold를 정하지 않았다.

## Calibration과 Rule

- [ ]  OK와 NG의 측정값 분포를 비교했다.
- [ ]  여러 Threshold 후보를 시험했다.
- [ ]  SIFT와 Inlier Ratio를 함께 사용하는 이유를 이해했다.
- [ ]  사용할 Rule을 결정했다.
- [ ]  `day05_logo_rules.json`을 만들었다.
- [ ]  Test 전에 Rule을 동결했다.

## Test와 평가

- [ ]  처음 보는 Test 이미지 6장에 같은 Rule을 적용했다.
- [ ]  Test 중 Threshold를 수정하지 않았다.
- [ ]  Actual과 Predicted를 비교했다.
- [ ]  TP / TN / FP / FN을 구분할 수 있다.
- [ ]  Accuracy를 확인했다.
- [ ]  FP와 FN이 있다면 결과 이미지를 직접 확인했다.
- [ ]  NG Reason과 실제 Failure Cause의 차이를 이해했다.

## Mini Challenge

- [ ]  광천김과 다른 제품을 사용했다.
- [ ]  새로운 Reference를 준비했다.
- [ ]  Calibration OK / NG를 측정했다.
- [ ]  최소 2개의 Feature를 비교했다.
- [ ]  직접 Threshold를 결정했다.
- [ ]  Test 전에 Rule을 고정했다.
- [ ]  새로운 Test 이미지에 Rule을 적용했다.
- [ ]  TP / TN / FP / FN을 확인했다.
- [ ]  결과를 `day05_mini_challenge.md`에 정리했다.

## 기록

- [ ]  README에 5일차 결과를 작성했다.
- [ ]  `git status`로 변경 내용을 확인했다.
- [ ]  Git Commit을 완료했다.
- [ ]  필요한 경우 `day05-logo-v1.0` Tag를 만들었다.
- [ ]  외부 업로드가 허용된 경우 GitHub에 Push했다.

---

# 42. 5일차에서 반드시 이해해야 할 핵심

5일차에서 가장 중요한 개념을 마지막으로 확인합니다.

### Calibration은 무엇인가요?

여러 정상·불량 이미지의 측정값을 비교하여:

```
어디까지 OK이고
어디부터 NG인가?
```

라는 검사 기준을 결정하는 과정입니다.

### Rule Freeze는 무엇인가요?

Calibration에서 결정한 기준을 고정하여:

```
이제부터 이 기준으로 검사한다.
```

라고 확정하는 과정입니다.

### Test는 무엇인가요?

동결한 Rule을 처음 보는 데이터에 적용하여:

```
새로운 이미지에서도
잘 동작하는가?
```

를 확인하는 과정입니다.

### FP와 FN은 무엇인가요?

이번 수업에서는 NG를 Positive로 사용했습니다.

```
FP
실제 OK → 프로그램 NG
→ 정상 과검출

FN
실제 NG → 프로그램 OK
→ 불량 미검출
```

특히 제조검사에서는 **불량을 정상으로 통과시키는 FN**을 주의해서 봅니다.

### 실패 분석은 무엇인가요?

Test에서 틀린 결과를 바로 Threshold 수정으로 덮지 않고, `FP / FN`, `NG Reason`, 실제 이미지를 함께 확인하여 현재 Rule이 어떤 조건에서 실패했는지 설명하는 과정입니다.

이번 Test에서는 정상 이미지 3장이 모두 `LOW_INLIER_RATIO`로 FP가 되었고, 이를 현재 Baseline의 한계로 기록했습니다.

### Mini Challenge는 무엇인가요?

광천김에서 강사와 함께 배운:

```
Calibration
→ Threshold
→ Rule
→ Freeze
→ Test
→ 평가
```

과정을 **다른 제품에서 학생이 스스로 다시 수행하는 실습**입니다.

---

# 43. 1~5일차 전체 흐름을 연결합니다

지금까지 배운 내용을 하나로 연결하면 다음과 같습니다.

```
[1일차]

무엇을 검사할 것인가?
        ↓
카메라 / 이미지
        ↓
ROI 설정


[2일차]

이미지 품질 확인
        ↓
Brightness
Contrast
Noise
Blur
        ↓
Image Enhancement


[3일차]

병뚜껑 검사
        ↓
Binary
Morphology
Contour
        ↓
Area / Count / BBox / Center
        ↓
Candidate Rule


[4일차]

광천김 로고 검사
        ↓
Template Matching
ORB
SIFT
RANSAC
Homography
        ↓
여러 측정 방법 비교


[5일차]

광천김 Calibration 데이터
        ↓
여러 이미지 측정
        ↓
OK / NG 분포 비교
        ↓
Threshold 후보 비교
        ↓
복합 Rule 결정
        ↓
Rule Freeze
        ↓
처음 보는 Test
        ↓
TP / TN / FP / FN
        ↓
성능 평가
        ↓
FP / FN 및 실패 원인 확인
        ↓
Mini Challenge
        ↓
다른 제품으로
학생이 전체 과정 직접 반복
```

5일차에서 외워야 할 가장 중요한 흐름은 이것입니다.

```
측정
→ 비교
→ 기준 결정
→ 기준 동결
→ Test
→ 평가
→ 실패 원인 확인
```

> 좋은 Threshold 숫자를 외우는 것이 목적이 아니라, 데이터를 근거로 검사 기준을 만들고 새로운 데이터에서 검증하는 머신비전 검사 개발 절차를 이해하는 것이 5일차의 핵심입니다.