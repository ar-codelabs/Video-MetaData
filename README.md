# 🏟️ 스포츠 영상 데이터 추출 데모

Amazon Bedrock 하나로 BDA(Data Automation) + Twelve Labs(Pegasus 1.2 / Marengo Embed)를 모두 호출해  
스포츠 영상에서 추출 가능한 모든 데이터를 시각화하는 데모 애플리케이션입니다.

> 별도 Twelve Labs API 키 없이, AWS 자격증명만으로 동작합니다.

---

## 📁 프로젝트 구조

```
├── app.py                  # Flask 백엔드 (BDA + Bedrock Pegasus/Marengo)
├── templates/
│   └── index.html          # 3탭 UI (업로드 / BDA / Twelve Labs via Bedrock)
├── data_video/             # 분석할 영상 파일을 여기에 넣으세요
├── requirements.txt
├── .env.example
├── data/
│   ├── bda.md              # BDA 추출 데이터 항목 전체 정리
│   └── twelvelabs.md       # Twelve Labs 추출 데이터 항목 전체 정리
```

---

## 🚀 빠른 시작

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열고 아래 값을 채워주세요:

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
S3_BUCKET_NAME=your-bucket-name
```

### 3. 영상 파일 준비

`data_video/` 폴더에 분석할 영상 파일을 넣어주세요:

```bash
cp your_video.mp4 data_video/
```

지원 포맷: `.mp4`, `.avi`, `.mov`, `.mkv`, `.webm`, `.flv`, `.wmv`, `.m4v`

### 4. Bedrock 모델 액세스 활성화

AWS 콘솔 → Amazon Bedrock → Model access에서 아래 모델을 활성화해주세요:

- `TwelveLabs Pegasus 1.2`
- `TwelveLabs Marengo Embed 2.7`

### 5. 서버 실행

```bash
python app.py
```

브라우저에서 `http://localhost:5000` 접속

---

## 🖥️ UI 구성 (3탭)

| 탭 | 기능 | 사용 서비스 |
|---|---|---|
| ① S3 업로드 | 로컬 영상 → Amazon S3 업로드 | S3 |
| ② BDA 분석 | 구조화 데이터 추출 (10개 카테고리) | Bedrock Data Automation |
| ③ Twelve Labs 분석 | 영상 의미 분석 (7개 분석 + 임베딩) | Bedrock → Pegasus 1.2 / Marengo |

---

## 🔧 아키텍처

```
로컬 영상 파일
      │
      ▼
  Amazon S3 (원본 저장)
      │
  ┌───┴───┐
  │       │
  ▼       ▼
 BDA    Bedrock Runtime
  │     ├─ Pegasus 1.2 (InvokeModel) — 7개 프롬프트 분석
  │     └─ Marengo Embed (StartAsyncInvoke) — 벡터 임베딩
  │       │
  └───┬───┘
      │
      ▼
  Flask UI (결과 테이블 렌더링)
```

모든 호출이 AWS 내부에서 이루어지며, 외부 API 키가 필요하지 않습니다.

---

## 📊 추출 데이터 상세

- **BDA 추출 항목** → [`data/bda.md`](data/bda.md)
- **Twelve Labs 추출 항목** → [`data/twelvelabs.md`](data/twelvelabs.md)

---

## ⚙️ 기술 스택

| 구분 | 기술 |
|---|---|
| 백엔드 | Python 3.10+, Flask, boto3 |
| 영상 분석 1 | Amazon Bedrock Data Automation (BDA) |
| 영상 분석 2 | Amazon Bedrock → TwelveLabs Pegasus 1.2 |
| 임베딩 | Amazon Bedrock → TwelveLabs Marengo Embed 2.7 |
| 스토리지 | Amazon S3 |
| 프론트엔드 | Vanilla JS, HTML/CSS (의존성 없음) |

---

## 📋 사전 요구사항

- AWS 계정 및 IAM 권한 (`bedrock:*`, `s3:*`)
- Amazon S3 버킷 생성
- Bedrock 모델 액세스 활성화 (Pegasus 1.2, Marengo Embed 2.7)
- Python 3.10 이상

---

## 🔑 환경 변수 전체 목록

| 변수 | 필수 | 기본값 | 설명 |
|---|---|---|---|
| `AWS_ACCESS_KEY_ID` | ✅ | - | AWS IAM 액세스 키 |
| `AWS_SECRET_ACCESS_KEY` | ✅ | - | AWS IAM 시크릿 키 |
| `AWS_REGION` | - | `us-east-1` | AWS 리전 |
| `S3_BUCKET_NAME` | ✅ | - | S3 버킷 이름 |
| `VIDEO_DIR` | - | `data_video` | 영상 파일 폴더 경로 |
| `S3_PREFIX` | - | `sports-videos` | S3 업로드 경로 prefix |
| `S3_OUTPUT_PREFIX` | - | `bda-output` | BDA 출력 경로 prefix |
| `PORT` | - | `5000` | Flask 서버 포트 |
| `PEGASUS_MODEL_ID` | - | `twelvelabs.pegasus-1-2-v1:0` | Bedrock Pegasus 모델 ID |
| `MARENGO_MODEL_ID` | - | `twelvelabs.marengo-embed-2-7-v1:0` | Bedrock Marengo 모델 ID |

---

## 📄 라이선스

MIT
