from qdrant_client import QdrantClient

client = QdrantClient(host="localhost", port=6333)

collection_name = "multimodal_video_data"  # Change if needed

# 1. Check collection list
collections = client.get_collections().collections
if not any(col.name == collection_name for col in collections):
    print(f"❌ Collection '{collection_name}' not found.")
else:
    print(f"✅ Collection '{collection_name}' exists.")

    # 2. Check vector count
    count = client.count(collection_name=collection_name).count
    print(f"📊 Vector count: {count}")

    # 3. (Optional) View a few vector payloads
    if count > 0:
        results = client.scroll(collection_name=collection_name, limit=5, with_payload=True)
        for point in results[0]:
            print("🔎 Vector ID:", point.id)
            print("📦 Payload:", point.payload)
            print("—" * 40)
