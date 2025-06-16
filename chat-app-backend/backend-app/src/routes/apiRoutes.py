from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any, Optional

router = APIRouter()

# --- Request Schemas ---
class ExtractRequest(BaseModel):
    videoPath: str
    outputPath: str

class TranscribeRequest(BaseModel):
    audioPath: str

class EmbeddingRequest(BaseModel):
    textChunks: List[str]
    imagePaths: Optional[List[str]] = None

class StoreEmbeddingsRequest(BaseModel):
    embeddings: List[Any]  # Adjust as needed

class QueryRequest(BaseModel):
    query: str

class SynthesizeRequest(BaseModel):
    prompt: str

# --- Endpoints ---
@router.post("/process")
async def input_processing(request: ExtractRequest,TranscribeRequest,EmbeddingRequest,StoreEmbedding):
    # Implement your logic he
    




@router.post("/query")
async def query_vector_db(request: QueryRequest):
    # Implement your logic here
    return {"results": []}

