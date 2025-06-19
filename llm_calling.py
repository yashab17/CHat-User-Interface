from searcher import MultimodalSearcher
#from OllamaService import call_llm
from embedder import EmbeddingProcessor
from llm_response_generator import LLMResponder 
from qdrant_handler import QdrantHandler
import config
from dotenv import load_dotenv
import os

# 🧠 Initialize once here (hardcoded setup)
embedder_model = EmbeddingProcessor(config.EMBEDDING_MODEL)
qdrant_client = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)

def final_pipeline(Query):
    """
    Final pipeline to perform multimodal search and LLM call.
    """
    print("🔍 Performing search...")
    Video_Transcript = MultimodalSearcher(
        qdrant_handler=qdrant_client,
        embedder=embedder_model,
        collection_name=config.COLLECTION_NAME
    )

    similarity_search_results = Video_Transcript.search(query=Query)

    print("💬 Calling LLM...")
    Output_generation=LLMResponder()
    final_output = Output_generation.call_llm(Query,similarity_search_results)
    
    return final_output

if __name__ == "__main__":
    final_pipeline(Query)



    print("Final Output:", Output)









