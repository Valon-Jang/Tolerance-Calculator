# Tolerance Calculator

<p align="center">
  <img src="assets/tolerance-calculator-icon.png" alt="Tolerance Calculator icon" width="240">
</p>

Worst-case Gap/Overlap 분석, 치수 영향도, Current-vs-Alternative 비교를 위한 범용 엔지니어링 공차 계산기입니다.

[English README](README.md)

## 목적

공차 검토는 보통 스프레드시트에서 시작하지만 치수, 부호, 대안이 늘어나면 계산 근거를 추적하기 어려워집니다. Tolerance Calculator는 핵심 계산을 명시적이고 재현 가능하게 유지합니다.

- 비대칭 `+ / -` 공차
- 부호를 가진 공차 체인 계수
- Worst-case 최소 / 최대
- Gap / Overlap 판정
- 치수별 영향도
- Current vs Alternative 비교
- 자동화와 AI 연동을 위한 JSON 입출력

공개 버전에는 회사, 고객, 제품, 생산 데이터가 포함되어 있지 않습니다.

## 빠른 실행

Python 3.10+가 필요하며 런타임은 표준 라이브러리만 사용합니다.

```bash
python -m tolerance_calculator examples/basic_case.json --pretty
```

로컬 설치 후 CLI 명령으로도 실행할 수 있습니다.

```bash
python -m pip install -e .
tolerance-calculator examples/basic_case.json --pretty
```

결과의 부호는 clearance 기준입니다.

- 전체 구간이 양수: `GAP_ONLY`
- 전체 구간이 음수: `OVERLAP_ONLY`
- 0을 가로지름: `GAP_OR_OVERLAP`

## Current vs Alternative

JSON 입력에 `alternative_dimensions`를 넣으면 같은 체인에 대안 치수를 적용해 다시 계산하고 `comparison` 결과를 반환합니다. 포함된 예제에 대안 치수가 들어 있습니다.

```bash
python -m tolerance_calculator examples/basic_case.json --pretty
```

Nominal, Minimum, Maximum, Span, 판정 변화와 Gap/Overlap 위험 제거 여부를 비교합니다.

## Python API

```python
from tolerance_calculator import Dimension, ChainTerm, analyze_chain
```

## 영향도

Worst-case 기준 각 치수의 기여도는 다음으로 계산합니다.

`abs(coefficient) × total tolerance span`

이 값을 전체 공차 span 대비 비율로 정규화해 어떤 치수가 Worst-case 범위를 가장 크게 지배하는지 보여줍니다. 통계적 공정능력 모델은 아닙니다.

## v0.1 범위

현재 포함:

- 비대칭 공차
- 양/음 체인 계수
- Worst-case stack-up
- Gap/Overlap 판정
- 치수 영향도 순위
- Current/Alternative 비교
- JSON CLI

아직 포함하지 않음:

- RSS / 통계 공차
- Monte Carlo
- GD&T 관계
- 단위 변환
- Excel Import/Export
- Revision DB
- 그래픽 Stack Editor
- AI 추천 계층

위 항목은 향후 확장 후보이며 현재 구현됐다는 의미가 아닙니다.

## 설계 원칙

- **계산 투명성** — 모든 결과는 명시된 치수와 계수에서 계산됩니다.
- **Deterministic first** — 핵심 공차 계산은 LLM에 의존하지 않습니다.
- **AI-friendly** — JSON 인터페이스로 AI/자동화 시스템에서 쉽게 호출할 수 있습니다.
- **범용 공개 데이터** — 예제는 모두 합성 데이터입니다.

## 배경

이 공개 구현은 엔지니어링 공차 검토를 더 반복 가능하고 비교 가능하며 감사 가능한 형태로 만들기 위한 소프트웨어/AI 실험에서 출발했습니다. 공개 저장소는 회사별 Workflow나 실제 데이터가 아니라 재사용 가능한 계산 코어에 집중합니다.
