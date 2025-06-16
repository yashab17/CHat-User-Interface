from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any

router = APIRouter()

class StoreEmbeddingsRequest(BaseModel):
    embeddings: List[Any]  # Adjust type as needed (e.g., List[List[float]])

@router.post("/store-in-vector-db")
async def store_in_vector_db(request: StoreEmbeddingsRequest):
    
    # Connect to Qdrant/Milvus and upsert vectors
    # Example: upsert_vectors(request.embeddings)
    return {"message": "Stored in vector database."}