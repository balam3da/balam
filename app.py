from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
    CouldNotRetrieveTranscript,
)

app = FastAPI()

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

class VideoIDRequest(BaseModel):
    video_id: str

@app.post("/get_subtitles")
async def get_subtitles(req: VideoIDRequest):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            req.video_id,
            languages=["ko", "en"],
        )
        full_text = "\n".join(seg["text"] for seg in transcript)
        return {"video_id": req.video_id, "subtitles": full_text}
    except (TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, CouldNotRetrieveTranscript):
        # 자막이 없거나 차단됐을 때 빈 문자열로 대응
        return {"video_id": req.video_id, "subtitles": ""}
    except Exception as e:
        # 그 외 예기치 못한 에러는 500으로 반환
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"message": "✅ FastAPI 서버 작동 중!"}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
