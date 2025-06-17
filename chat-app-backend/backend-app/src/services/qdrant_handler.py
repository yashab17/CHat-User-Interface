# exports.storeEmbeddings = async (embeddings) => {
#   // Store in Qdrant, Pinecone, Weaviate, etc.
# };

# exports.querySimilar = async (queryEmbedding) => {
#   // Retrieve top-k relevant documents
# };


from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid

class QdrantHandler:
    def __init__(self, collection_name, dim=768):
        # Initialize an in-memory Qdrant client and recreate collection
        self.client = QdrantClient(":memory:")
        self.collection_name = collection_name
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
        )

    def upload(self, nodes):
        """
        Upload a list of nodes (TextNode or ImageNode) with embeddings and metadata to Qdrant.
        Each node must have `.embedding`, `.metadata`, and `.json()` method (as supported by LlamaIndex nodes).
        """
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=node.embedding,
                payload={**node.metadata, "_node_content": node.json()}
            )
            for node in nodes
        ]
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, vector, top_k=5):
        """
        Search for similar vectors in Qdrant.
        Returns a list of results with payloads and scores.
        """
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k * 10,
            with_payload=True
        )