# Twelve Labs API — 추출 데이터 항목 전체 정리

Twelve Labs는 영상을 "이해"하는 데 특화된 멀티모달 AI 플랫폼입니다.  
Pegasus 1.2(프롬프트 기반 분석)와 Pegasus 1.5(타임스탬프 기반 세그먼트)를 함께 사용합니다.

> 📎 공식 문서 — Analyze Videos: https://docs.twelvelabs.io/v1.3/docs/guides/analyze-videos  
> 📎 공식 문서 — Segment Videos (Pegasus 1.5): https://docs.twelvelabs.io/v1.3/docs/guides/segment-videos  
> 📎 공식 문서 — Create Embeddings: https://docs.twelvelabs.io/docs/guides/create-embeddings  
> 📎 API Reference — Async Analysis: https://docs.twelvelabs.io/v1.3/api-reference/analyze-videos/create-async-analysis-task  
> 📎 가격 계산기: https://www.twelvelabs.io/pricing-calculator

---

## 모델 개요

| 모델 | 특징 | 주요 용도 |
|---|---|---|
| **Pegasus 1.2** | 자연어 프롬프트로 영상 전체 분석 (max_tokens: 4,096) | 요약, 선수 분석, 전술, 감정 등 |
| **Pegasus 1.5** | 타임스탬프 기반 구조화 세그먼트 추출 (max_tokens: 32,768) | 장면 분리, 커스텀 메타데이터 |
| **Marengo** | 시맨틱 임베딩 + 검색 | 자연어 장면 검색, 유사 클립 추천 |

> 📎 모델별 스펙: [Async Analysis API Reference](https://docs.twelvelabs.io/v1.3/api-reference/analyze-videos/create-async-analysis-task)

---

## 1. 전체 요약 (Pegasus 1.2 — `summary`)

영상 전체를 종합적으로 요약합니다.

> 📎 레퍼런스: [Analyze Videos Guide](https://docs.twelvelabs.io/v1.3/docs/guides/analyze-videos)  
> ⚠️ 주의: 아래 "추출 항목"은 고정된 API 응답 필드가 아닙니다. Pegasus 1.2는 프롬프트 기반으로 동작하며, 프롬프트 내용에 따라 출력이 달라집니다. 아래는 스포츠 영상 분석용 프롬프트로 요청 시 기대할 수 있는 항목입니다.

| 추출 항목 | 설명 |
|---|---|
| 스포츠 종목 | 영상에서 진행 중인 스포츠 종류 |
| 참여 팀/선수 | 경기에 참여한 팀 또는 선수 이름 |
| 핵심 이벤트 | 경기 중 발생한 주요 사건 흐름 |
| 경기 결과 | 최종 스코어 또는 승패 결과 |
| 경기 맥락 | 리그, 대회, 경기 배경 정보 |

**출력 형태:** 자연어 텍스트 (단락)

---

## 2. 하이라이트 (Pegasus 1.2 — `highlights`)

경기에서 가장 중요한 순간들을 추출합니다.

> ⚠️ 프롬프트 기반 출력 — 고정 API 필드 아님 (1번과 동일)

| 추출 항목 | 설명 |
|---|---|
| 하이라이트 장면 설명 | 어떤 일이 일어났는지 텍스트 설명 |
| 관련 선수/팀 | 해당 장면에 등장한 선수 또는 팀 |
| 중요도 이유 | 왜 이 장면이 중요한지 설명 |
| 순서 | 경기 흐름 순서대로 나열 |

**출력 형태:** 번호 매긴 목록 (텍스트)

---

## 3. 선수 분석 (Pegasus 1.2 — `players`)

영상에 등장하는 모든 선수/참가자를 분석합니다.

> ⚠️ 프롬프트 기반 출력 — 고정 API 필드 아님

| 추출 항목 | 설명 |
|---|---|
| 선수 이름 | 확인 가능한 경우 실명 |
| 외형 특징 | 유니폼 색상, 번호, 체형 등 |
| 저지 번호 | 화면에서 확인된 등번호 |
| 소속 팀 | 선수가 속한 팀 |
| 주요 행동 | 해당 선수의 눈에 띄는 플레이 |
| 포지션 | 확인 가능한 경우 포지션 |

**출력 형태:** 선수별 설명 목록 (텍스트)

---

## 4. 동작 분석 (Pegasus 1.2 — `actions`)

영상에 등장하는 모든 운동 동작을 분류합니다.

> ⚠️ 프롬프트 기반 출력 — 고정 API 필드 아님

| 추출 항목 | 설명 |
|---|---|
| 동작 유형 | 슛, 패스, 드리블, 태클, 헤딩 등 |
| 수행 선수 | 해당 동작을 한 선수 |
| 동작 맥락 | 어떤 상황에서 발생했는지 |
| 성공/실패 여부 | 동작의 결과 |
| 시간적 맥락 | 경기 어느 시점에 발생했는지 |

**출력 형태:** 동작별 설명 목록 (텍스트)

---

## 5. 득점 이벤트 (Pegasus 1.2 — `score_events`)

모든 득점 및 점수 변화 순간을 추출합니다.

> ⚠️ 프롬프트 기반 출력 — 고정 API 필드 아님

| 추출 항목 | 설명 |
|---|---|
| 득점 방법 | 골, 3점슛, 홈런, 트라이 등 |
| 득점자 | 득점한 선수 또는 팀 |
| 점수 변화 | 득점 전후 스코어 |
| 득점 상황 | 어떤 상황에서 득점했는지 |
| 순서 | 경기 흐름 순서 |

**출력 형태:** 득점 이벤트별 목록 (텍스트)

---

## 6. 전술 분석 (Pegasus 1.2 — `tactics`)

경기에서 나타나는 전술적·전략적 요소를 분석합니다.

> ⚠️ 프롬프트 기반 출력 — 고정 API 필드 아님

| 추출 항목 | 설명 |
|---|---|
| 팀 포메이션 | 확인 가능한 진형 (4-3-3 등) |
| 공격 패턴 | 주요 공격 전개 방식 |
| 수비 전략 | 수비 조직 및 압박 방식 |
| 세트피스 | 코너킥, 프리킥 등 세트피스 전술 |
| 코칭 결정 | 교체, 전술 변화 등 |
| 팀별 강점/약점 | 경기에서 드러난 특징 |

**출력 형태:** 전술 요소별 설명 (텍스트)

---

## 7. 감정 및 분위기 (Pegasus 1.2 — `emotions`)

선수와 관중의 감정적 반응을 분석합니다.

> ⚠️ 프롬프트 기반 출력 — 고정 API 필드 아님

| 추출 항목 | 설명 |
|---|---|
| 선수 감정 | 환호, 실망, 항의, 집중 등 |
| 관중 반응 | 함성, 야유, 침묵 등 |
| 경기 분위기 | 전반적인 경기장 분위기 |
| 감정적 전환점 | 분위기가 바뀐 순간 |
| 팀별 사기 | 각 팀의 사기 변화 흐름 |

**출력 형태:** 감정 요소별 설명 (텍스트)

---

## 8. 타임스탬프 기반 장면 세그먼트 (Pegasus 1.5 — `segments`)

영상을 의미 있는 장면 단위로 분리하고, 각 장면에서 구조화된 메타데이터를 추출합니다.

> 📎 레퍼런스: [Segment Videos Guide](https://docs.twelvelabs.io/v1.3/docs/guides/segment-videos)  
> ✅ 이 기능은 `analysis_mode: "time_based_metadata"` + `model_name: "pegasus1.5"`로 호출하며, `segment_definitions`에 커스텀 필드를 정의합니다. 아래 필드(`description`, `sport_action`, `players`, `intensity`)는 데모에서 정의한 커스텀 스키마이며, 사용자가 자유롭게 변경 가능합니다.

### 세그먼트 구조

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `start_time` | number | 장면 시작 시간 (초) | `0.0` |
| `end_time` | number | 장면 종료 시간 (초) | `45.0` |
| `metadata.description` | string | 장면 내용 설명 | `"공격수가 페널티 박스 진입 후 슛 시도"` |
| `metadata.sport_action` | string | 주요 스포츠 동작 | `"슛"`, `"패스"`, `"태클"` |
| `metadata.players` | string | 장면에 등장한 선수 | `"10번 선수, 골키퍼"` |
| `metadata.intensity` | enum | 장면 강도 | `"low"`, `"medium"`, `"high"`, `"critical"` |

### 강도(intensity) 기준

| 값 | 의미 | 예시 |
|---|---|---|
| `low` | 낮은 강도 | 킥오프, 볼 소유 이동 |
| `medium` | 중간 강도 | 일반 공격 전개 |
| `high` | 높은 강도 | 위협적인 공격, 빠른 역습 |
| `critical` | 결정적 순간 | 골, 페널티킥, 퇴장 |

---

## 9. 시맨틱 검색 (Marengo — Search API)

자연어 쿼리로 영상 내 특정 장면을 검색합니다.

> 📎 레퍼런스: [Marengo 3.0 블로그](https://www.twelvelabs.io/blog/marengo-3-00)  
> ⚠️ 주의: 검색 옵션 `text_in_video`는 v1.2 Search API에서 사용되던 옵션입니다. v1.3 Analyze API와는 별도 기능이며, 인덱싱(Marengo)이 선행되어야 합니다.

| 검색 옵션 | 설명 |
|---|---|
| `visual` | 시각적 내용 기반 검색 |
| `conversation` | 음성/대화 내용 기반 검색 |
| `text_in_video` | 화면 텍스트 기반 검색 |

**검색 결과 필드:**

| 필드 | 타입 | 설명 |
|---|---|---|
| `video_id` | string | 영상 ID |
| `start` | number | 클립 시작 시간 (초) |
| `end` | number | 클립 종료 시간 (초) |
| `score` | number | 검색 관련도 점수 |
| `confidence` | string | 신뢰도 레벨 (`high`, `medium`, `low`) |

**검색 예시 쿼리:**
```
"골 넣는 장면"
"선수가 넘어지는 순간"
"감독이 항의하는 장면"
"관중이 환호하는 순간"
"페널티킥"
```

---

## 10. 임베딩 (Marengo — Embed API)

영상 구간을 벡터로 변환합니다. 추천 시스템 구축에 활용됩니다.

> 📎 레퍼런스: [Create Embeddings Guide](https://docs.twelvelabs.io/docs/guides/create-embeddings)  
> 📎 가격: [Twelve Labs Pricing Calculator](https://www.twelvelabs.io/pricing-calculator)

| 입력 유형 | 단가 | 설명 |
|---|---|---|
| 영상 | $0.042/분 | 영상 구간 벡터화 |
| 오디오 | $0.008/분 | 음성 구간 벡터화 |
| 이미지 | $0.100/1K건 | 이미지 벡터화 |
| 텍스트 | $0.070/1K건 | 텍스트 벡터화 |

**활용 예시:**
- 유사 장면 검색 (같은 유형의 골 장면 모아보기)
- 선수별 플레이 스타일 클러스터링
- 개인화 하이라이트 추천

---

## 요약 — Twelve Labs 추출 데이터 한눈에 보기

| 분석 유형 | 모델 | 출력 형태 | 스포츠 활용 예시 |
|---|---|---|---|
| 전체 요약 | Pegasus 1.2 | 텍스트 | 경기 결과 자동 리포트 |
| 하이라이트 | Pegasus 1.2 | 목록 | 하이라이트 릴 자동 생성 |
| 선수 분석 | Pegasus 1.2 | 목록 | 선수 등장 장면 태깅 |
| 동작 분석 | Pegasus 1.2 | 목록 | 플레이 유형 분류 |
| 득점 이벤트 | Pegasus 1.2 | 목록 | 득점 장면 자동 추출 |
| 전술 분석 | Pegasus 1.2 | 텍스트 | 코칭 스태프 분석 도구 |
| 감정·분위기 | Pegasus 1.2 | 텍스트 | 팬 감성 콘텐츠 큐레이션 |
| 장면 세그먼트 | Pegasus 1.5 | 구조화 JSON | 타임스탬프 기반 클립 편집 |
| 시맨틱 검색 | Marengo | 클립 목록 | 자연어로 장면 검색 |
| 임베딩 | Marengo | 벡터 | 유사 장면 추천 시스템 |

---

## BDA vs Twelve Labs 비교

| 기준 | BDA | Twelve Labs |
|---|---|---|
| 강점 | 구조화 메타데이터, 대량 처리 | 의미 이해, 자연어 분석 |
| 텍스트 추출 | ✅ OCR + 위치 좌표 | 제한적 |
| 음성 트랜스크립트 | ✅ 화자 구분 | ✅ 대화 검색 |
| 장면 요약 | ✅ 챕터 단위 | ✅ 더 상세한 자연어 |
| 로고 감지 | ✅ 35,000개 | 제한적 |
| 동작/폼 분석 | ❌ | ✅ 핵심 강점 |
| 자연어 검색 | Blueprint 커스텀 | ✅ 핵심 강점 |
| 감정 분석 | 제한적 | ✅ |
| 타임스탬프 세그먼트 | 챕터/샷 단위 | ✅ 커스텀 필드 |
| 비용 구조 | 처리 유형별 | 분당 과금 |
| 권장 사용 | 대량 아카이브 처리 | 의미 기반 개인화 |
