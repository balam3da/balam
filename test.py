from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from youtube_transcript_api import YouTubeTranscriptApi

app = FastAPI()

class Query(BaseModel):
    query: str
    max_results: int

class VideoIDRequest(BaseModel):
    video_id: str

@app.post("/youtube_scraper")
async def youtube_scraper(query: Query):
    print("🔍 [요청 수신] Query:", query)
    print("🔎 query.query:", query.query)
    print("🔢 query.max_results:", query.max_results)

    return {
        "choices": [
            {
                "message": {
                    "content": f"{query.query} 관련 영상 {query.max_results}개 가져오기 완료!"
                }
            }
        ]
    }

@app.post("/get_subtitles")
async def get_subtitles(req: VideoIDRequest):
    """
    video_id를 받아 YouTubeTranscriptApi로 자막을 가져와 리턴합니다.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            req.video_id,
            languages=["ko", "en"]
        )
        full_text = "\n".join([seg["text"] for seg in transcript])
        return {
            "video_id": req.video_id,
            "subtitles": full_text
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/")
def root():
    return {"message": "✅ FastAPI 서버 작동 중!"}

# ✅ Render용 포트 설정
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("test:app", host="0.0.0.0", port=port)