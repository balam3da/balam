from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

# ✅ video_id는 아예 받지 않음!
class SubtitleInput(BaseModel):
    title: str
    raw_subtitles: str

@app.post("/get_subtitles")
async def get_subtitles(data: SubtitleInput):
    title = data.title
    raw = data.raw_subtitles

    # 자막 클린 처리
    cleaned = clean_subtitles(raw)

    # 간단 요약 처리
    summary = summarize_subtitles(cleaned)

    return JSONResponse(content={
        "title": title,
        "cleaned_subtitles": cleaned,
        "summary": summary
    })

# 🧹 타임스탬프/숫자 제거 등 정제 함수
def clean_subtitles(raw_text: str) -> str:
    import re
    lines = raw_text.splitlines()
    cleaned_lines = []

    for line in lines:
        if re.match(r'^\d+$', line):  # 숫자만 있는 줄 제거
            continue
        if re.match(r'^\d{2}:\d{2}:\d{2}', line):  # 00:00:00 형식 제거
            continue
        if re.match(r'^\d{2}:\d{2}', line):  # 00:00 형식 제거
            continue
        cleaned_lines.append(line.strip())

    return "\n".join(cleaned_lines)

# ✨ 단순 요약 함수 (GPT 연동 가능)
def summarize_subtitles(text: str) -> str:
    if len(text) < 200:
        return text
    return text[:150] + "..."
