from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Any, Optional
from main import run_pipeline
from LLm_Calling import final_pipeline

router = APIRouter()

# --- Request Schemas ---
class ExtractRequest(BaseModel):
    videoPath: str
    outputPath: str

class QueryRequest(BaseModel):
    query: str
    

class SynthesizeRequest(BaseModel):
    prompt: str

# --- Endpoints ---
@router.post("/process")
async def input_processing(request: ExtractRequest):
    # Implement your logic he
    video_input= request.videoPath
    output_path = request.outputPath
    return  run_pipeline(video_input, output_path)




@router.post("/query")
async def query_vector_db(request: QueryRequest):
    # Implement your logic here
    query = request.query
    # Assuming you have a Qdrant client and embedder model initialized  
    qdrant_client=request.qdrant_client
    embedder_model=request.embedder_model
    config = {      "COLLECTION_NAME": "multimodal_video_data",
        "VECTOR_DIM": 768,  # Adjust as needed                      
        "CHUNK_SIZE": 512,  # Adjust as needed                          
        "CHUNK_OVERLAP": 50  # Adjust as needed
    }
    final_output = final_pipeline(qdrant_client, embedder_model, config, query) 
    return {"result": final_output}

@router.get("/query")


