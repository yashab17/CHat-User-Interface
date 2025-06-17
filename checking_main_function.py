from frame_extractor import FrameExtractor
from audio_extractor import AudioExtractor
from transcriber import AudioTranscriber
from embedder import EmbeddingProcessor
from qdrant_handler import QdrantHandler
from text_image_indexer import TextImageIndexer
import os
import config
import hashlib
import json

def get_video_hash(video_path):
    BUF_SIZE = 65536
    sha256 = hashlib.sha256()
    with open(video_path, 'rb') as f:
        while chunk := f.read(BUF_SIZE):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_video_processed(hash_str, record_file='embedded_videos.json'):
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            processed = json.load(f)
    else:
        processed = {}
    return hash_str in processed

def mark_video_processed(hash_str, record_file='embedded_videos.json'):
    if os.path.exists(record_file):
        with open(record_file, 'r') as f:
            processed = json.load(f)
    else:
        processed = {}

    processed[hash_str] = "embedded"

    with open(record_file, 'w') as f:
        json.dump(processed, f, indent=2)

def run_pipeline(video_path, working_dir):
    video_hash = get_video_hash(video_path)
    print("Hash Created")
    if is_video_processed(video_hash):
        print("⚠️ Video already processed. Skipping embedding and upload.")
        qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
        embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
        return qdrant, embedder

    # Create output dirs
    frame_dir = os.path.join(working_dir, "Frames")
    audio_dir = os.path.join(working_dir, "Audio")
    transcript_dir = os.path.join(working_dir, "Transcript")

    print("📼 Extracting frames...")
    FrameExtractor(config.FRAME_RATE).extract_frames(video_path, frame_dir)

    print("🔊 Extracting audio...")
    AudioExtractor().extract_audio(video_path, audio_dir)

    print("📝 Transcribing audio...")
    mp3_files = [f for f in os.listdir(audio_dir) if f.endswith(".mp3")]
    if not mp3_files:
        raise FileNotFoundError(f"No .mp3 file found in {audio_dir}")
    audio_path = os.path.join(audio_dir, mp3_files[0])

    AudioTranscriber(config.TRANSCRIPTION_MODEL).transcribe(audio_path, transcript_dir)

    print("📊 Generating embeddings...")
    embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
    indexer = TextImageIndexer(embedder, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    text_nodes = indexer.index_text(transcript_dir)
    image_nodes = indexer.index_images(frame_dir)

    print("🧠 Uploading embeddings to Qdrant...")
    qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
    qdrant.upload(text_nodes + image_nodes)

    mark_video_processed(video_hash)
    print("✅ All data uploaded to Qdrant!")
    return qdrant, embedder

# Entrypoint
if __name__ == "__main__":
    input_path = r"C:\Users\KrupaShah\Downloads\OneDrive_2025-06-04\test_video\WHat makes computer work"
    working_directory = r"C:\Users\KrupaShah\Downloads\OneDrive_2025-06-04\test_video\Output"

    if os.path.isdir(input_path):
        for filename in os.listdir(input_path):
            if filename.lower().endswith(".mp4"):
                video_file = os.path.join(input_path, filename)
                print(f"\n▶️ Running pipeline for: {video_file}")
                qdrant_client, embedder_model = run_pipeline(video_file, working_directory)
    elif os.path.isfile(input_path) and input_path.lower().endswith(".mp4"):
        print(f"\n▶️ Running pipeline for single file: {input_path}")
        qdrant_client, embedder_model = run_pipeline(input_path, working_directory)
    else:
        print(f"❌ Invalid input: {input_path} is neither a .mp4 file nor a folder containing videos.")
