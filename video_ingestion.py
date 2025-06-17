import os
import json
from frame_extractor import FrameExtractor
from audio_extractor import AudioExtractor
from transcriber import AudioTranscriber
from embedder import EmbeddingProcessor
from qdrant_handler import QdrantHandler
from text_image_indexer import TextImageIndexer
import config

CACHE_FILE = "embedded_videos.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

def select_video(video_folder):
    video_files = [f for f in os.listdir(video_folder) if f.endswith(".mp4")]
    cache = load_cache()

    if not video_files:
        print("❌ No MP4 videos found in the folder.")
        return None

    print("\n🎬 Available Videos:")
    for i, video in enumerate(video_files):
        video_name = os.path.splitext(video)[0]
        status = "✅ Embedded" if cache.get(video_name) == "embedded" else "❌ Not embedded"
        print(f"{i + 1}. {video}  [{status}]")

    while True:
        try:
            selection = int(input("\n👉 Select a video by number: ")) - 1
            if 0 <= selection < len(video_files):
                return os.path.join(video_folder, video_files[selection])
        except ValueError:
            pass
        print("❗ Invalid selection. Please try again.")

def ingest_video(video_path: str, working_dir: str):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    cache = load_cache()

    # ✅ Check if this specific video is already embedded using cache
    if cache.get(video_name) == "embedded":
        print(f"✅ '{video_name}' is already embedded (via cache). Skipping...")
        return None, None

    # Output dirs
    frame_dir = os.path.join(working_dir, "Frames")
    audio_dir = os.path.join(working_dir, "Audio")
    transcript_dir = os.path.join(working_dir, "Transcript")

    print("📼 Extracting frames...")
    FrameExtractor(config.FRAME_RATE).extract_frames(os.path.dirname(video_path), frame_dir)

    print("🔊 Extracting audio...")
    AudioExtractor().extract_audio(os.path.dirname(video_path), audio_dir)

    print("📝 Transcribing audio...")
    AudioTranscriber(config.TRANSCRIPTION_MODEL).transcribe(audio_dir, transcript_dir)

    print("📊 Generating embeddings...")
    embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
    indexer = TextImageIndexer(embedder, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    text_nodes = indexer.index_text(transcript_dir)
    image_nodes = indexer.index_images(frame_dir)

    print("🧠 Uploading embeddings to Qdrant...")
    qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM, recreate=False)
    qdrant.upload(text_nodes + image_nodes)

    # ✅ Mark video as embedded in local cache
    cache[video_name] = "embedded"
    save_cache(cache)

    print(f"✅ '{video_name}' successfully embedded and uploaded.")
    return qdrant, embedder

if __name__ == "__main__":
    VIDEO_FOLDER = r"C:\Users\KrupaShah\Downloads\OneDrive_2025-06-04\test_video\WHat makes computer work"
    WORKING_DIR = r"C:\Users\KrupaShah\Downloads\OneDrive_2025-06-04\test video\Other_Folder"

    selected_video = select_video(VIDEO_FOLDER)
    if selected_video:
        qdrant_client, embedder_model = ingest_video(selected_video, WORKING_DIR)
        if qdrant_client:
            print("🔎 Ready to query! Run the query server or script.")
