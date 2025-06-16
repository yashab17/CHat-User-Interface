from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class EmbeddingRequest(BaseModel):
    textChunks: List[str]
    imagePaths: List[str] 

@router.post("/generate-embeddings")
async def generate_embeddings(request: EmbeddingRequest):
# Use CLIP or similar model to embed both
    textChunks = request.textChunks
    imagePaths = request.imagePaths
    










    return {"message": "Embeddings generated."}