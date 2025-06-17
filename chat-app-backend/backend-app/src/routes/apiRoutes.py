from fastapi import APIRouter, HTTPException,status, Depends,Header
from pydantic import BaseModel
from typing import List, Any, Optional
from main import run_pipeline
from LLM_Calling import final_pipeline
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env

API_KEY = os.getenv("API_KEY")


router = APIRouter()

# --- Request Schemas ---
class ExtractRequest(BaseModel):
    videoPath: str
    outputPath: str

class QueryRequest(BaseModel):
    query: str
    



def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API Key",
        )

# --- Endpoints ---
@router.post("/process")
async def input_processing(request: ExtractRequest,_ = Depends(verify_api_key)):
    # Implement your logic he
    video_input= request.videoPath
    output_path = request.outputPath
    return  run_pipeline(video_input, output_path)




@router.post("/query")
async def query_vector_db(request: QueryRequest,_ = Depends(verify_api_key)):
    # Implement your logic here
    query = request.query
    # Assuming you have a Qdrant client and embedder model initialized  
    final_output = final_pipeline(query) 
    return {"result": final_output}



