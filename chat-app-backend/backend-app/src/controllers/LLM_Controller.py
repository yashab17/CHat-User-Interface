from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

from services.Searcher import MultimodalSearcher as MS
from services.Ollama_Service import call_llm

router = APIRouter()

class LLMRequest(BaseModel):
    queryEmbedding: List[float]
    originalQuery: str

@router.post("/synthesize")
async def synthesize(request: LLMRequest):
    try:
        results = await MS.search(request.queryEmbedding, 3)
        context = "\n".join(r["payload"].get("text") or r["payload"].get("source") for r in results)
        final_prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {request.originalQuery}"
        answer = await call_llm(final_prompt)
        return {"answer": answer, "contextUsed": context}
    except Exception:
        raise HTTPException(status_code=500, detail="LLM failed to respond.")