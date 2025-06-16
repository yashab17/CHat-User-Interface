# from ..services.ollamaService import OllamaService

# export class QueryController {
#     private ollamaService: OllamaService;

#     constructor() {
#         this.ollamaService = new OllamaService();
#     }

#     public async handleQuery(req: Request, res: Response): Promise<void> {
#         const query = req.body.query;

#         try {
#             const response = await this.ollamaService.sendQuery(query);
#             res.status(200).json({ response });
#         } catch (error) {
#             res.status(500).json({ error: 'An error occurred while processing your query.' });
#         }
#     }
# }

# // exports.processQuery = async (req, res) => {
# //   const query = req.body.query;

# //   // 1. Tokenize query and embed
# //   // 2. Search in vector DB for top-k
# //   // 3. Call LLM with context + query
# //   // 4. Return synthesized response

# //   res.send("Answer generated.");
# // };


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.ollama_service import OllamaService
 
router = APIRouter()

class QueryRequest(BaseModel):
    query: str

@router.post("/query")
async def handle_query(request: QueryRequest):
    ollama_service = OllamaService()
    try:
        response = await ollama_service.send_query(request.query)
        return {"response": response}
    except Exception:
        raise HTTPException(status_code=500, detail="An error occurred while processing your query.")