from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

# 1) 유튜브 검색 엔드포인트
class Query(BaseModel):
    query: str
    max_results: int

@app.post("/youtube_scraper")
async def youtube_scraper(query: Query):
    return {
        "choices": [
            {
                "message": {
                    "content": f"{query.query} 관련 영상 {query.max_results}개 가져오기 완료!"
                }
            }
        ]
    }

# 2) 자막 가져오기 엔드포인트
class VideoIDRequest(BaseModel):
    video_id: str

@app.post("/get_subtitles")
async def get_subtitles(req: VideoIDRequest):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            req.video_id,
            languages=["ko", "en"]
        )
        full_text = "\n".join(seg["text"] for seg in transcript)
        return {
            "video_id": req.video_id,
            "subtitles": full_text
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

# 3) 헬스체크 루트
@app.get("/")
def root():
    return {"message": "✅ FastAPI 서버 작동 중!"}

# 4) Render용 포트 바인딩
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)