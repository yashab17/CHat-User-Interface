from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams, PointStruct
import uuid

class QdrantHandler:
    def __init__(self, collection_name, dim=768, recreate=False):
        self.client = QdrantClient(host="localhost", port=6333)
        self.collection_name = collection_name

        existing = [c.name for c in self.client.get_collections().collections]
        if recreate or self.collection_name not in existing:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE)
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
