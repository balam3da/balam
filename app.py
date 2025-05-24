from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import re

app = FastAPI()

# 1. 받는 데이터 구조 정의
class SubtitleInput(BaseModel):
    title: str
    raw_subtitles: str

# 2. 자막 파싱 함수: 타임스탬프 제거
def parse_transcript(text: str) -> str:
    """
    확장 프로그램 Transcript에서 복사한 자막 텍스트를 정제합니다.
    - 00:00, 00:00:00 등 시간 제거
    - 빈 줄 제거
    - 앞뒤 공백 정리
    """
    lines = text.splitlines()
    cleaned_lines = []

    for line in lines:
        line = line.strip()
        if re.match(r'^\d{2}:\d{2}(:\d{2})?$', line):  # 시간 형식 제거
            continue
        if line:  # 빈 줄 제외
            cleaned_lines.append(line)

    return "\n".join(cleaned_lines)

# 3. 요약 함수 (간단하게 앞부분만 반환)
def summarize_subtitles(text: str) -> str:
    if len(text) < 200:
        return text
    return text[:150] + "..."

# 4. 실제 API 엔드포인트
@app.post("/get_subtitles")
async def get_subtitles(data: SubtitleInput):
    title = data.title
    raw = data.raw_subtitles

    # ⏬ 자막 정제
    cleaned = parse_transcript(raw)

    # ⏬ 자막 요약
    summary = summarize_subtitles(cleaned)

    return JSONResponse(content={
        "title": title,
        "cleaned_subtitles": cleaned,
        "summary": summary
    })
