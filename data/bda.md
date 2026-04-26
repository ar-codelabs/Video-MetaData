# Amazon Bedrock Data Automation (BDA) — 추출 데이터 항목 전체 정리

BDA는 영상을 구조화된 JSON으로 변환합니다.  
별도 모델 관리 없이 단일 API 호출로 아래 모든 데이터를 추출할 수 있습니다.

> 📎 공식 문서: https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html  
> 📎 BDA 개요: https://aws.amazon.com/bedrock/bda  
> 📎 BDA 블로그: https://aws.amazon.com/blogs/machine-learning/simplify-multimodal-generative-ai-with-amazon-bedrock-data-automation/

---

## 1. 영상 메타데이터 (`metadata`)

영상 파일 자체의 기술적 정보입니다.

> 📎 레퍼런스: [BDA Video Standard Output 예시](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html) — `metadata` 객체

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `asset_id` | string | BDA 내부 자산 ID | `"0"` |
| `semantic_modality` | string | 콘텐츠 유형 | `"VIDEO"` |
| `s3_bucket` | string | 원본 파일 S3 버킷 | `"my-bucket"` |
| `s3_key` | string | 원본 파일 S3 경로 | `"sports-videos/game.avi"` |
| `format` | string | 영상 컨테이너 포맷 | `"AVI"`, `"QuickTime / MOV"` |
| `codec` | string | 영상 코덱 | `"h264"`, `"mpeg4"` |
| `frame_rate` | number | 초당 프레임 수 | `30` |
| `frame_width` | number | 가로 해상도 (px) | `1920` |
| `frame_height` | number | 세로 해상도 (px) | `1080` |
| `duration_millis` | number | 전체 재생시간 (ms) | `5400000` |

---

## 2. 통계 (`statistics`)

영상 분석 결과 요약 수치입니다.

> 📎 레퍼런스: [BDA Video Standard Output 예시](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html) — `statistics` 객체

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `shot_count` | number | 감지된 총 샷(컷) 수 | `148` |
| `chapter_count` | number | 분리된 챕터 수 | `11` |
| `speaker_count` | number | 감지된 고유 화자 수 | `4` |

---

## 3. 전체 요약 (`summary`)

영상 전체 내용을 AI가 자연어로 요약합니다.

> 📎 레퍼런스: [BDA Video Output — Full Video Summary](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html)

| 필드 | 타입 | 설명 |
|---|---|---|
| `summary` | string | 영상 전체 주제·핵심 이벤트·결론을 담은 요약 텍스트 |

- 화자 이름이 음성/자막으로 확인되면 이름으로 표기
- 확인 불가 시 `speaker_0`, `speaker_1` 형태로 표기

---

## 4. 챕터 분석 (`chapters[]`)

영상을 의미 단위로 분리한 챕터 목록입니다.  
각 챕터는 시각·청각 신호를 기반으로 자동 분리됩니다.

> 📎 레퍼런스: [BDA Video Output — Chapter Summaries](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html) — `chapters` 배열

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `start_timecode_smpte` | string | 챕터 시작 타임코드 | `"00:00:00:00"` |
| `end_timecode_smpte` | string | 챕터 종료 타임코드 | `"00:02:15:12"` |
| `start_timestamp_millis` | number | 시작 시간 (ms) | `0` |
| `end_timestamp_millis` | number | 종료 시간 (ms) | `135500` |
| `start_frame_index` | number | 시작 프레임 번호 | `0` |
| `end_frame_index` | number | 종료 프레임 번호 | `4065` |
| `duration_millis` | number | 챕터 길이 (ms) | `135500` |
| `shot_indices` | number[] | 포함된 샷 인덱스 목록 | `[0, 1, 2, 3]` |
| `summary` | string | 챕터 내용 AI 요약 | `"전반전 15분, 홈팀이..."` |

---

## 5. 샷 분리 (`shots[]`)

편집 컷(cut) 단위로 분리된 샷 목록입니다.  
챕터보다 세밀한 단위이며, 카메라 전환 기준으로 분리됩니다.

> 📎 레퍼런스: [BDA Video Standard Output 예시](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html) — `shots` 배열

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `shot_index` | number | 샷 순번 | `3` |
| `start_timecode_smpte` | string | 샷 시작 타임코드 | `"00:00:08:19"` |
| `end_timecode_smpte` | string | 샷 종료 타임코드 | `"00:00:09:25"` |
| `start_timestamp_millis` | number | 시작 시간 (ms) | `8633` |
| `end_timestamp_millis` | number | 종료 시간 (ms) | `9833` |
| `start_frame_index` | number | 시작 프레임 번호 | `259` |
| `end_frame_index` | number | 종료 프레임 번호 | `295` |
| `duration_smpte` | string | 샷 길이 (SMPTE) | `"00:00:01:06"` |
| `duration_millis` | number | 샷 길이 (ms) | `1200` |
| `duration_frames` | number | 샷 길이 (프레임 수) | `36` |
| `confidence` | number | 샷 경계 감지 신뢰도 (0~1) | `0.9956` |
| `chapter_indices` | number[] | 소속 챕터 인덱스 | `[1]` |

---

## 6. 음성 트랜스크립트 (`transcript`)

영상 내 모든 음성을 텍스트로 변환합니다.  
화자 구분(Speaker Diarization)이 포함됩니다.

> 📎 레퍼런스: [BDA Video Output — Full Audio Transcript](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html)  
> ⚠️ 주의: 공식 문서에 트랜스크립트 세부 JSON 구조(필드명)는 공개되어 있지 않습니다. 아래 필드명은 기능 설명 기반 추정치이며, 실제 응답 구조는 다를 수 있습니다.

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `start_timecode_smpte` | string | 발화 시작 타임코드 | `"00:01:23:05"` |
| `end_timecode_smpte` | string | 발화 종료 타임코드 | `"00:01:25:18"` |
| `speaker_label` | string | 화자 식별자 | `"speaker_0"`, `"김해설"` |
| `text` | string | 발화 텍스트 | `"골이 들어갑니다!"` |

> 화자 이름은 음성 자기소개 또는 화면 자막에서 자동 추출됩니다.

---

## 7. 프레임 텍스트 (`frames[].text_words[]`)

화면에 표시된 텍스트를 프레임 단위로 추출합니다.  
선수 이름 자막, 점수판, 광고 배너, 저지 번호 등이 포함됩니다.

> 📎 레퍼런스: [BDA Video Output — Text in Video](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html) — `frames[].text_words` 배열

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `timecode_smpte` | string | 해당 프레임 타임코드 | `"00:00:03:15"` |
| `timestamp_millis` | number | 해당 프레임 시간 (ms) | `3500` |
| `frame_index` | number | 프레임 번호 | `105` |
| `text_words[].id` | string | 텍스트 요소 고유 ID | UUID |
| `text_words[].text` | string | 감지된 텍스트 | `"ANDREA"`, `"23"` |
| `text_words[].confidence` | number | 텍스트 인식 신뢰도 (0~1) | `0.9984` |
| `text_words[].locations[].bounding_box.left` | number | 텍스트 좌측 위치 (0~1 비율) | `0.1056` |
| `text_words[].locations[].bounding_box.top` | number | 텍스트 상단 위치 (0~1 비율) | `0.7363` |
| `text_words[].locations[].bounding_box.width` | number | 텍스트 너비 (0~1 비율) | `0.1981` |
| `text_words[].locations[].bounding_box.height` | number | 텍스트 높이 (0~1 비율) | `0.0684` |
| `text_words[].locations[].polygon` | object[] | 텍스트 영역 다각형 좌표 | `[{x, y}, ...]` |
| `text_words[].line_id` | string | 같은 줄 텍스트 그룹 ID | UUID |

---

## 8. 콘텐츠 모더레이션 (`frames[].content_moderation[]`)

부적절한 콘텐츠를 프레임 단위로 감지합니다.  
BDA는 7개 카테고리를 지원합니다.

> 📎 레퍼런스: [BDA Video Output — Content Moderation](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html)

| 카테고리 | 설명 |
|---|---|
| `Explicit` | 명시적 성인 콘텐츠 |
| `Non-Explicit Nudity of Intimate parts and Kissing` | 비명시적 신체 노출 및 키스 |
| `Swimwear or Underwear` | 수영복 또는 속옷 |
| `Violence` | 폭력적 장면 |
| `Drugs & Tobacco` | 마약 및 담배 |
| `Alcohol` | 알코올 |
| `Hate symbols` | 혐오 상징 |

각 감지 항목 필드:

| 필드 | 타입 | 설명 |
|---|---|---|
| `category` | string | 감지된 카테고리명 |
| `confidence` | number | 감지 신뢰도 (0~1) |
| `bounding_box` | object | 감지 영역 좌표 (선택적) |

---

## 9. IAB 분류 (`iab_categories[]`)

IAB(Interactive Advertising Bureau) 광고 표준 분류 체계를 적용합니다.  
영상 장면을 광고 타겟팅에 활용 가능한 카테고리로 분류합니다.

> 📎 레퍼런스: [BDA Video Output — IAB Taxonomy](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html)  
> ⚠️ 주의: 공식 문서에 IAB 응답의 세부 JSON 필드명(`category_l1`, `category_l2`, `confidence`)은 명시되어 있지 않습니다. L1 24개 / L2 85개 카테고리 수는 공식 확인됨.

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `category_l1` | string | 1단계 대분류 (24개) | `"Sports"` |
| `category_l2` | string | 2단계 소분류 (85개) | `"Soccer"`, `"Basketball"` |
| `confidence` | number | 분류 신뢰도 (0~1) | `0.92` |

---

## 10. 로고 감지 (`logos[]`)

35,000개 이상의 기업 브랜드 로고를 감지합니다.  
유니폼 스폰서, 광고판, 방송 워터마크 등이 포함됩니다.

> ⚠️ 기본 비활성화 — BDA 프로젝트 설정에서 명시적으로 활성화 필요

> 📎 레퍼런스: [BDA Video Output — Logo Detection](https://docs.aws.amazon.com/bedrock/latest/userguide/bda-ouput-video.html)  
> 📎 35,000개 로고 수치 출처: [BDA 블로그 (2024.12)](https://aws.amazon.com/blogs/machine-learning/simplify-multimodal-generative-ai-with-amazon-bedrock-data-automation/)  
> ⚠️ 주의: 공식 문서에 "bounding box + confidence scores" 제공 언급만 있고, 세부 JSON 필드명(`name`, `timecode_smpte` 등)은 공개되어 있지 않습니다. 아래 필드는 기능 설명 기반 추정치입니다.

| 필드 | 타입 | 설명 | 예시 |
|---|---|---|---|
| `name` | string | 감지된 브랜드명 | `"Nike"`, `"Adidas"` |
| `timecode_smpte` | string | 감지 타임코드 | `"00:05:12:08"` |
| `confidence` | number | 감지 신뢰도 (0~1) | `0.87` |
| `bounding_box.left` | number | 로고 좌측 위치 (0~1) | `0.23` |
| `bounding_box.top` | number | 로고 상단 위치 (0~1) | `0.05` |
| `bounding_box.width` | number | 로고 너비 (0~1) | `0.08` |
| `bounding_box.height` | number | 로고 높이 (0~1) | `0.04` |

---

## 요약 — BDA 추출 데이터 한눈에 보기

| 카테고리 | 항목 수 | 스포츠 활용 예시 |
|---|---|---|
| 영상 메타데이터 | 10개 필드 | 영상 품질 검증, 아카이빙 |
| 통계 | 3개 필드 | 경기 복잡도 파악 |
| 전체 요약 | 텍스트 | 경기 결과 자동 리포트 |
| 챕터 분석 | 9개 필드/챕터 | 전반/후반/연장 자동 분리 |
| 샷 분리 | 11개 필드/샷 | 하이라이트 클립 자동 편집 |
| 음성 트랜스크립트 | 4개 필드/발화 | 해설 검색, 자막 생성 |
| 프레임 텍스트 | 10개 필드/단어 | 선수명·점수판 자동 추출 |
| 콘텐츠 모더레이션 | 7개 카테고리 | 방송 적합성 자동 검수 |
| IAB 분류 | L1 24개 / L2 85개 | 광고 타겟팅, 콘텐츠 분류 |
| 로고 감지 | 35,000+ 브랜드 | 스폰서 노출 측정 |
