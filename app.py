from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    query: str
    max_results: int

@app.post("/youtube_scraper")
async def youtube_scraper(query: Query):
    return {
        "choices": [
            {"message": {"content": f"'{query.query}' 관련 영상 {query.max_results}개 가져오기 완료!"}}
        ]
    }

@app.get("/")
def root():
    return {"message": "✅ FastAPI 서버 작동 중!"}