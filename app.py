from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn  # ← 꼭 필요!

app = FastAPI()

class Query(BaseModel):
    query: str
    max_results: int

@app.post("/youtube_scraper")
async def youtube_scraper(query: Query):
    return {
        "choices": [
            {"message": {"content": f"{query.query} 관련 영상 {query.max_results}개 가져오기 완료!"}}
        ]
    }

@app.get("/")
def root():
    return {"message": "✅ FastAPI 서버 작동 중!"}

# ✅ 반드시 아래 코드 추가!
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000)