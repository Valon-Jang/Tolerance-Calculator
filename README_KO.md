# TolCalc

**Worst Case Gap/Overlap, 영향도, Current/Alt 비교를 위한 범용 조립공차 분석 도구**

TolCalc는 단순히 공차 숫자 하나를 계산하는 도구가 아니라, 공차 검토를 반복 가능한 엔지니어링 업무 흐름으로 만들기 위한 실험 프로젝트입니다.

공개 `v0.1`은 회사/고객/제품별 정보 없이 범용 계산 코어만 분리한 버전입니다. 모든 예제 데이터는 합성 데이터입니다.

## 현재 기능

- 비대칭 `+/-` 공차 입력
- 양수/음수 계수를 사용하는 공차 Chain
- Worst Case `Min / Nominal / Max`
- Gap / Overlap(간섭) 가능성 판정
- Worst Case 폭 기준 치수별 영향도 순위
- Current / Alternative 설계안 비교
- JSON 입출력
- Python 표준 라이브러리 기반 계산 코어
- Unit Test 및 GitHub Actions CI

## 실행

Python 3.10 이상이 필요합니다.

```bash
python -m pip install -e .
tolcalc examples/basic_case.json --pretty
```

설치 없이도 실행할 수 있습니다.

```bash
python -m tolcalc.cli examples/basic_case.json --pretty
```

Signed clearance 결과에서 양수는 **Gap**, 음수는 **Overlap / Interference**를 의미합니다.

## 설계 원칙

**Calculation first, AI second.**

공차 계산은 결정적이고 독립적으로 검증 가능해야 합니다. 향후 유사 과거사례 검색, 검토 Point 제안, 설계대안 추천 같은 AI 기능을 추가하더라도 검증된 계산 코어 위에서 동작하도록 분리합니다.

향후 계획은 [ROADMAP.md](docs/ROADMAP.md)를 참고하세요.

## 공개 범위

이 저장소에는 회사 고유 치수, 제품명, 고객 정보, 내부 기준표, 사내 DB, 실제 프로젝트 데이터가 포함되지 않습니다.

## Author

**Valon Jang** — Packaging & Product Development Engineer, South Korea 🇰🇷
