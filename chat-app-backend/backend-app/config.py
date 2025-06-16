# Qdrant settings
QDRANT_URL = "http://localhost:6333"  # Use ":memory:" for in-memory if no persistent storage
COLLECTION_NAME = "multimodal_video_data"

# Embedding & transcription models
EMBEDDING_MODEL = "clip-ViT-L-14"        # Model from sentence-transformers
TRANSCRIPTION_MODEL = "base"             # Model for faster-whisper

# Frame extraction
FRAME_RATE = 2  # Extract 2 frames per second

# Text chunking
CHUNK_SIZE = 200
CHUNK_OVERLAP = 50

# Embedding dimensionality
VECTOR_DIM = 768