from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import uuid
import config  # ✅ Centralized config

class QdrantHandler:
    def __init__(self, collection_name=None, dim=None, recreate=False):
        self.collection_name = collection_name or config.COLLECTION_NAME
        self.vector_dim = dim or config.VECTOR_DIM

        # Use QDRANT_URL from config
        self.client = QdrantClient(url=config.QDRANT_URL)

        existing = [c.name for c in self.client.get_collections().collections]
        if recreate or self.collection_name not in existing:
            print(f"📦 Creating collection: {self.collection_name} (dim={self.vector_dim})")
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_dim, distance=Distance.COSINE)
            )

    def upload(self, nodes):
        points = [
            PointStruct(
                id=str(uuid.uuid4()),
                vector=node.embedding,
                payload={**node.metadata, "_node_content": node.json()}
            )
            for node in nodes
        ]
        print(f"🚀 Uploading {len(points)} vectors to Qdrant...")
        self.client.upsert(collection_name=self.collection_name, points=points)

    def search(self, vector, top_k=5):
        return self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=top_k * 10,
            with_payload=True
        )