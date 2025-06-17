from searcher import MultimodalSearcher
from llm_response_generator import LLMResponder
from qdrant_client import QdrantClient

class VideoQAInterface:
    def __init__(self, qdrant_handler, embedder, collection_name, openai_key):
        self.qdrant = qdrant_handler
        self.embedder = embedder
        self.collection_name = collection_name
        self.llm = LLMResponder(openai_key)
        self.searcher = MultimodalSearcher(qdrant_handler, embedder, self.collection_name)

    def _check_collection_has_data(self):
        """
        Verifies whether the Qdrant collection exists and contains any vectors.
        """
        try:
            client = QdrantClient(host="localhost", port=6333)
            collections = client.get_collections().collections
            if not any(col.name == self.collection_name for col in collections):
                print(f"❌ Collection '{self.collection_name}' not found in Qdrant.")
                return False

            count = client.count(collection_name=self.collection_name).count
            if count == 0:
                print(f"❌ Collection '{self.collection_name}' exists but contains 0 vectors.")
                return False

            return True
        except Exception as e:
            print(f"❌ Error while connecting to Qdrant: {e}")
            return False

    def ask(self, user_query, top_k=5, min_score=0.5):
        if not self._check_collection_has_data():
            return "⚠️ Qdrant collection is empty or unavailable."

        results = self.searcher.search(user_query, top_k=top_k, min_score=min_score)

        if not results or not results["top_text"]:
            return "❌ No relevant content found."

        top_text_chunks = [r["text"] for r in results["top_text"]]
        answer = self.llm.generate_answer(user_query, top_text_chunks)

        print("\n🤖 LLM-Generated Answer:")
        print(answer)
        return answer


if __name__ == "__main__":
    from embedder import EmbeddingProcessor
    from qdrant_handler import QdrantHandler
    import config
    import os

    qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM, recreate=False)
    embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "sk-...")  # Replace or export via env

    interface = VideoQAInterface(qdrant, embedder, config.COLLECTION_NAME, openai_key=OPENAI_API_KEY)

    print("💬 Multimodal Video QA System")
    print("Type your question below. Type 'exit' to quit.\n")

    while True:
        user_query = input("❓ Ask a question: ")
        if user_query.lower() in ["exit", "quit"]:
            break

        interface.ask(user_query, top_k=5, min_score=0.5)
        print("\n" + "="*80 + "\n")
