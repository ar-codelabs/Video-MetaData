import os
import json
import mimetypes
import boto3
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

AWS_REGION    = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET     = os.getenv("S3_BUCKET_NAME")
S3_PREFIX     = os.getenv("S3_PREFIX", "sports-videos")
S3_OUT_PREFIX = os.getenv("S3_OUTPUT_PREFIX", "bda-output")
PORT          = int(os.getenv("PORT", "5000"))
VIDEO_DIR     = os.getenv("VIDEO_DIR", "data_video")

PEGASUS_MODEL_ID = os.getenv("PEGASUS_MODEL_ID", "twelvelabs.pegasus-1-2-v1:0")
MARENGO_MODEL_ID = os.getenv("MARENGO_MODEL_ID", "twelvelabs.marengo-embed-2-7-v1:0")

VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv", ".m4v"}

s3         = boto3.client("s3", region_name=AWS_REGION)
bedrock    = boto3.client("bedrock-data-automation-runtime", region_name=AWS_REGION)
bedrock_da = boto3.client("bedrock-data-automation", region_name=AWS_REGION)
bedrock_rt = boto3.client("bedrock-runtime", region_name=AWS_REGION)
sts        = boto3.client("sts", region_name=AWS_REGION)

# AWS 계정 ID 자동 조회
try:
    AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]
except Exception:
    AWS_ACCOUNT_ID = None

# BDA 프로젝트 자동 생성/조회
BDA_PROJECT_ARN = None

def get_or_create_bda_project():
    global BDA_PROJECT_ARN
    if BDA_PROJECT_ARN:
        return BDA_PROJECT_ARN

    project_name = "sports-video-analyzer"

    # 기존 프로젝트 검색
    try:
        resp = bedrock_da.list_data_automation_projects()
        for proj in resp.get("projects", []):
            if proj.get("projectName") == project_name:
                BDA_PROJECT_ARN = proj["projectArn"]
                print(f"[BDA] 기존 프로젝트 사용: {BDA_PROJECT_ARN}")
                return BDA_PROJECT_ARN
    except Exception as e:
        print(f"[BDA] 프로젝트 목록 조회 실패: {type(e).__name__}: {e}")

    # 새 프로젝트 생성
    try:
        resp = bedrock_da.create_data_automation_project(
            projectName=project_name,
            projectStage="LIVE",
            standardOutputConfiguration={
                "video": {
                    "extraction": {
                        "category": {
                            "state": "ENABLED",
                            "types": ["CONTENT_MODERATION", "TEXT_DETECTION", "TRANSCRIPT"]
                        },
                        "boundingBox": {"state": "ENABLED"}
                    },
                    "generativeField": {
                        "state": "ENABLED",
                        "types": ["VIDEO_SUMMARY", "CHAPTER_SUMMARY", "IAB"]
                    }
                }
            },
        )
        BDA_PROJECT_ARN = resp["projectArn"]
        print(f"[BDA] 새 프로젝트 생성: {BDA_PROJECT_ARN}")
        return BDA_PROJECT_ARN
    except Exception as e:
        print(f"[BDA] 프로젝트 생성 실패: {type(e).__name__}: {e}")
        return None

def s3_uri(key): return f"s3://{S3_BUCKET}/{key}"
def guess_mime(filename):
    mime, _ = mimetypes.guess_type(filename)
    return mime or "application/octet-stream"
def basename_no_ext(filename):
    return os.path.splitext(os.path.basename(filename))[0]

# ─────────────────────────────────────────
# 공통
# ─────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html", s3_prefix=S3_PREFIX)

@app.route("/api/videos", methods=["GET"])
def list_videos():
    """data_video/ 폴더 내 영상 파일 목록 반환"""
    if not os.path.isdir(VIDEO_DIR):
        return jsonify({"files": []})
    files = [
        f for f in os.listdir(VIDEO_DIR)
        if os.path.isfile(os.path.join(VIDEO_DIR, f))
        and os.path.splitext(f)[1].lower() in VIDEO_EXTS
    ]
    files.sort()
    return jsonify({"files": files})

# ─────────────────────────────────────────
# TAB 1 — S3 업로드
# ─────────────────────────────────────────
@app.route("/api/upload", methods=["POST"])
def upload_to_s3():
    filename = request.json.get("filename")
    if not filename:
        return jsonify({"error": "파일명이 지정되지 않았습니다."}), 400
    filepath = os.path.join(VIDEO_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": f"{filepath} 파일을 찾을 수 없습니다."}), 404
    s3_key = f"{S3_PREFIX}/{filename}"
    try:
        s3.upload_file(filepath, S3_BUCKET, s3_key,
                       ExtraArgs={"ContentType": guess_mime(filename)})
        return jsonify({"success": True, "s3_key": s3_key, "s3_uri": s3_uri(s3_key), "filename": filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# TAB 2 — BDA
# ─────────────────────────────────────────
@app.route("/api/bda/analyze", methods=["POST"])
def bda_analyze():
    data    = request.json
    s3_key  = data.get("s3_key")
    if not s3_key:
        return jsonify({"error": "s3_key가 필요합니다. 먼저 S3에 업로드해주세요."}), 400

    project_arn = get_or_create_bda_project()
    if not project_arn:
        return jsonify({"error": "BDA 프로젝트를 생성할 수 없습니다. AWS 권한을 확인해주세요."}), 500

    out_key = f"{S3_OUT_PREFIX}/{basename_no_ext(s3_key)}"
    try:
        invoke_params = {
            "inputConfiguration": {"s3Uri": s3_uri(s3_key)},
            "outputConfiguration": {"s3Uri": s3_uri(out_key)},
            "dataAutomationConfiguration": {
                "dataAutomationProjectArn": project_arn,
                "stage": "LIVE"
            },
            "notificationConfiguration": {
                "eventBridgeConfiguration": {
                    "eventBridgeEnabled": False
                }
            },
            "dataAutomationProfileArn": f"arn:aws:bedrock:{AWS_REGION}:{AWS_ACCOUNT_ID}:data-automation-profile/us.data-automation-v1",
        }
        resp = bedrock.invoke_data_automation_async(**invoke_params)
        return jsonify({"success": True,
                        "invocation_arn": resp["invocationArn"],
                        "output_prefix": out_key})
    except Exception as e:
        print(f"[BDA] invoke 실패: {type(e).__name__}: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/bda/status", methods=["POST"])
def bda_status():
    arn = request.json.get("invocation_arn")
    try:
        resp   = bedrock.get_data_automation_status(invocationArn=arn)
        return jsonify({"status": resp.get("status")})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/bda/results", methods=["POST"])
def bda_results():
    prefix = request.json.get("output_prefix")
    try:
        objs    = s3.list_objects_v2(Bucket=S3_BUCKET, Prefix=prefix).get("Contents", [])
        results = {}
        for obj in objs:
            key = obj["Key"]
            if key.endswith(".json"):
                body = s3.get_object(Bucket=S3_BUCKET, Key=key)["Body"].read()
                results[key.split("/")[-1]] = json.loads(body)
        return jsonify({"success": True, "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ─────────────────────────────────────────
# TAB 3 — Twelve Labs via Bedrock
# ─────────────────────────────────────────
def invoke_pegasus(prompt, s3_key):
    body = json.dumps({
        "inputPrompt": prompt,
        "mediaSource": {"s3Location": {"uri": s3_uri(s3_key), "bucketOwner": AWS_ACCOUNT_ID}},
        "temperature": 0.2,
        "maxOutputTokens": 4096,
    })
    resp = bedrock_rt.invoke_model(
        modelId=PEGASUS_MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=body,
    )
    result = json.loads(resp["body"].read())
    return result.get("message", "")


@app.route("/api/tl/analyze_all", methods=["POST"])
def tl_analyze_all():
    data   = request.json
    s3_key = data.get("s3_key")
    if not s3_key:
        return jsonify({"error": "s3_key가 필요합니다."}), 400

    prompts = {
        "summary": "Provide a comprehensive summary of this sports video. Include the sport type, key events, players/teams involved, and the overall outcome.",
        "highlights": "List all key highlight moments in this sports video. For each highlight, describe what happened, who was involved, and why it was significant.",
        "players": "Identify and list all players, athletes, or participants visible in this video. For each person, describe their appearance, jersey number if visible, team, and notable actions.",
        "actions": "Analyze all athletic actions and movements in this video. List each action with its type (e.g., shot, pass, tackle, goal), the player performing it, and the timestamp context.",
        "score_events": "Extract all scoring events, goals, points, or game-changing moments from this sports video. Include the score change, who scored, and the method.",
        "tactics": "Analyze the tactical and strategic elements visible in this sports video. Describe formations, plays, team strategies, and coaching decisions.",
        "emotions": "Describe the emotional moments and crowd reactions in this sports video. Include player celebrations, frustrations, crowd responses, and atmosphere.",
    }

    results = {}
    errors  = {}
    for key, prompt in prompts.items():
        try:
            results[key] = invoke_pegasus(prompt, s3_key)
        except Exception as e:
            errors[key] = str(e)

    try:
        embed_resp = bedrock_rt.start_async_invoke(
            modelId=MARENGO_MODEL_ID,
            modelInput={
                "inputType": "video",
                "inputText": "",
                "mediaSource": {"s3Location": {"uri": s3_uri(s3_key), "bucketOwner": AWS_ACCOUNT_ID}},
                "embeddingOption": ["visual-text"],
            },
            outputDataConfig={
                "s3OutputDataConfig": {
                    "s3Uri": s3_uri(f"{S3_OUT_PREFIX}/embeddings/{basename_no_ext(s3_key)}")
                }
            },
        )
        results["embeddings"] = {
            "status": "started",
            "invocation_arn": embed_resp.get("invocationArn", ""),
            "note": "임베딩은 비동기 처리됩니다. S3 출력 경로에서 결과를 확인하세요."
        }
    except Exception as e:
        errors["embeddings"] = str(e)

    return jsonify({"results": results, "errors": errors})


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
