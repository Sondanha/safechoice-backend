# SAFECHOICE Backend

피싱·스캠 대응 **행동 선택 기반 교육 시뮬레이션 서비스** SAFECHOICE의 백엔드 레포지토리이다.

본 프로젝트는 탐지 중심의 기존 피싱 대응 방식에서 벗어나,  
**사용자의 실제 판단·행동 과정을 시뮬레이션하고 분석하여 취약성을 교정하는 예방 교육 서비스**를 목표로 한다.

---

## 1. 프로젝트 목표

SAFECHOICE는 피싱·스캠을 단순한 “차단 대상 위협”이 아니라  
**사용자의 반응을 관찰하고 학습시키는 경험 과정**으로 재정의한다.

- 실제 범죄 스크립트를 기반으로 한 시뮬레이션 제공
- 사용자 선택·반응 속도·검증 시도 등의 행동 로그 수집
- 룰 기반 분석을 통해 개인별 취약성 도출
- 분석 결과를 설명 중심의 피드백으로 제공

MVP 단계에서는 다음 범위까지만 구현한다.

- 시뮬레이션 세션 관리
- 사용자 이벤트 로그 수집
- 행동 지표(feature) 집계
- 취약성 점수 및 리포트 생성

LLM 및 RAG는 **판단 로직이 아닌 설명 보조 역할**로만 사용하며,  
현재는 뼈대 코드만 두고 실제 연동은 후순위로 둔다.

---

## 2. 기술 및 설계 원칙

- Framework: **FastAPI (Python)**
- Architecture: **DDD-lite**
  - Domain 중심 설계
  - 룰 기반 로직 우선
  - LLM은 설명 전용
- MVP 기준:
  - 단순성
  - 설명 가능성
  - 확장 가능성

### DDD 적용 범위

- 사용함:
  - Entity
  - Domain Service
  - Infra 분리
- 사용하지 않음:
  - Bounded Context 분리
  - CQRS / Event Sourcing
  - Repository 추상화 남발

---

## 3. 핵심 도메인 개념

SAFECHOICE 백엔드는 다음 6개 개념으로 구성된다.

- **Session**  
  하나의 시뮬레이션 실행 단위
- **Scenario**  
  실제 범죄 사례 기반 시뮬레이션 흐름
- **Step**  
  시나리오 내 단계
- **Event**  
  사용자 행동 로그 (클릭, 입력, 대기 등)
- **Feature**  
  이벤트를 집계한 행동·심리 지표
- **Report**  
  취약성 점수 및 설명 결과

---

## 4. 현재 디렉토리 구조

```text
safechoice-backend/
 └─ app/
    ├─ main.py
    ├─ api/
    │  ├─ sessions.py     # 세션 생성/진행 API (첫 step 반환)
    │  ├─ events.py       # 사용자 이벤트 수집 + 다음 step 반환
    │  └─ reports.py      # 분석 결과 조회 API
    ├─ domain/
    │  ├─ scenario.py     # (MVP) DUMMY_SCENARIO 포함
    │  ├─ session.py      # Session 도메인
    │  ├─ event.py        # Event, EventType 정의
    │  ├─ feature.py      # 행동 지표(Feature)
    │  └─ report.py       # 리포트 도메인
    ├─ service/
    │  ├─ scenario_engine.py  # 룰 기반 step 전환
    │  ├─ analysis_engine.py  # 이벤트→Feature 집계 + 점수 산식
    │  └─ feedback_engine.py  # 룰 기반 요약/피드백 템플릿
    ├─ infra/
    │  └─ collector/
    │     └─ skeleton.py  # 외부 시나리오/문서 자동 수집 뼈대(비활성)
    └─ core/
       └─ config.py       # env 로딩(현재는 최소)
```

---

## 5. API 범위 (MVP)

- `GET /health`
  서버 상태 확인
- `POST /sessions`
  세션 생성 + 첫 step 반환
- `POST /events`
  이벤트 수집 + 다음 step 반환 (종료 시 ended=true)
- `GET /reports/{session_id}`
  분석 결과 조회

---

## 6. 이벤트 payload 계약 (FE ↔ BE)

`POST /events` 요청의 `payload`는 다음 키를 포함한다.

- `current_step_id` (string): 현재 step id
- `option_id` (string): 사용자가 선택한 옵션 id
- `step_index` (number): 단계 깊이(전환 단계 지표)
- `trigger` (string, optional): 심리 트리거 (urgency/authority/curiosity/loss_avoidance 등)
- `verification` (boolean, optional): 검증 시도 여부

예시:

```json
{
  "session_id": "uuid",
  "type": "click",
  "payload": {
    "current_step_id": "step_1",
    "option_id": "reply",
    "step_index": 1,
    "trigger": "urgency",
    "verification": false
  },
  "timestamp": "2026-02-05T12:00:00"
}
```

---

## 7. 분석 모델 (MVP 1차)

본 MVP는 다음 평가 축을 기반으로 **룰 기반 분석**을 수행한다.

- 행동 반응: 반응 속도, 전환 단계
- 심리 반응: 트리거(긴급성/권위/호기심/손실회피) 반응
- 행동 신중성: 발신자/링크 검증 시도 여부

LLM은 판단에 관여하지 않으며, 현재는 룰 기반 템플릿으로 피드백을 생성한다.

---

## 8. 자동 수집 관련 설계

외부 범죄 사례/문서 자동 수집은 운영 서비스에서는 사용하지 않으며,
확장 가능성 증명을 위해 뼈대 코드만 유지한다.

---

## 9. 실행 방법

### 가상환경

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 의존성 설치

```bash
pip install -r requirements.txt
```

### 실행

```bash
uvicorn app.main:app --reload
```

- Swagger: `http://127.0.0.1:8000/docs`

---

## 10. 진행 상태

- [x] FastAPI 프로젝트 기동
- [x] 시나리오(step) 기반 룰 엔진(ScenarioEngine)
- [x] 세션 생성 → 첫 step 반환
- [x] 이벤트 수집 → 다음 step 반환
- [x] 이벤트 → Feature 집계(AnalysisEngine)
- [x] 점수 산식 + 룰 기반 피드백(FeedbackEngine)
- [x] Swagger 기반 API 테스트 완료
- [ ] DB 실제 연결 및 영속화 (후순위)
- [ ] LLM/RAG 연동 (후순위)
- [ ] 자동 수집 파이프라인 구현 (후순위)

---

## 11. 개발 원칙 요약

- 비즈니스 로직은 Router에 두지 않는다
- 판단은 룰 기반, 설명만 LLM
- MVP에서는 “되는 것”이 아니라 “설명 가능한 것”을 만든다
- 확장은 구조로만 열어두고, 구현은 미룬다
