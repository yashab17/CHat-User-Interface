from frame_extractor import FrameExtractor
from audio_extractor import AudioExtractor
from transcriber import AudioTranscriber
#from summarizer import TranscriptSummarizer
from embedder import EmbeddingProcessor
from qdrant_handler import QdrantHandler
from text_image_indexer import TextImageIndexer
from searcher import MultimodalSearcher
import os
import config

def run_pipeline(video_folder, working_dir):
    frame_dir = os.path.join(working_dir, "Frames")
    audio_dir = os.path.join(working_dir, "Audio")
    transcript_dir = os.path.join(working_dir, "Transcript")
    summary_dir = os.path.join(working_dir, "Summary")

    print("📼 Extracting frames...")
    FrameExtractor(config.FRAME_RATE).extract_frames(video_folder, frame_dir)

    print("🔊 Extracting audio...")
    AudioExtractor().extract_audio(video_folder, audio_dir)

    print("📝 Transcribing audio...")
    AudioTranscriber(config.TRANSCRIPTION_MODEL).transcribe(audio_dir, transcript_dir)

 #   print("🧠 Summarizing transcripts...")
 #   TranscriptSummarizer().summarize(transcript_dir, summary_dir)

    print("📊 Generating embeddings...")
    embedder = EmbeddingProcessor(config.EMBEDDING_MODEL)
    indexer = TextImageIndexer(embedder, config.CHUNK_SIZE, config.CHUNK_OVERLAP)
    text_nodes = indexer.index_text(transcript_dir)
    image_nodes = indexer.index_images(frame_dir)

    print("🧠 Uploading embeddings to Qdrant...")
    qdrant = QdrantHandler(config.COLLECTION_NAME, dim=config.VECTOR_DIM)
    qdrant.upload(text_nodes + image_nodes)

    print("✅ All data uploaded to Qdrant!")
    return qdrant, embedder

if __name__ == "__main__":
    video_folder_path = r"C:\Users\Yash S\Documents\vrag_videos"
    working_directory = r"C:\Users\Yash S\Documents\vrag_videos\Output_Videos"

    qdrant_client, embedder_model = run_pipeline(video_folder_path, working_directory)