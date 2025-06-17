from searcher import MultimodalSearcher
from OllamaService import call_llm

def final_pipeline(qdrant_client, embedder_model, config, Query):
    """
    Final pipeline to perform multimodal search and LLM call.
    """
    # Perform multimodal search
    Video_Transcript = MultimodalSearcher(qdrant_handler=qdrant_client, embedder=embedder_model, collection_name=config.COLLECTION_NAME)
    similarity_search_results = Video_Transcript.search(query=Query)

    # Call LLM with the search results
    final_output = call_llm(similarity_search_results, prompt=Query)
    
    return final_output

# Video_Transcript=MultimodalSearcher(qdrant_handler=qdrant_client, embedder=embedder_model, collection_name=config.COLLECTION_NAME)
# similarity_search_results = Video_Transcript.search(
#     query="What is the video about?",)

# final_output=   call_llm(
#     similarity_search_results,
#     prompt="What is the video about?")


