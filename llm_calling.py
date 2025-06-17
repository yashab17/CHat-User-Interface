from searcher import MultimodalSearcher
#from OllamaService import call_llm
from embedder import EmbeddingProcessor
from qdrant_handler import QdrantHandler
import config

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
    final_output = call_llm(similarity_search_results, prompt=Query)
    
    return final_output




