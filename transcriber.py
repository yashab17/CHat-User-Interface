# transcriber.py

from faster_whisper import WhisperModel
import os

class AudioTranscriber:
    def __init__(self, model_name="base", device="cpu"):
        self.model = WhisperModel(model_name, device="cpu", compute_type="int8")

    def transcribe(self, audio_path, output_folder):  # ✅ accepts a file now
        audio_files = [f for f in os.listdir(audio_path) if f.endswith('.mp3')]

        if len(audio_files) != 1:
            raise ValueError(f"❌ Expected exactly one .mp3 file in {audio_path}, found {len(audio_files)}")

        audio_path = os.path.join(audio_path, audio_files[0])
        
        os.makedirs(output_folder, exist_ok=True)
        print(f"🔊 Transcribing: {audio_path}")

        segments, _ = self.model.transcribe(audio_path)
        transcript_text = " ".join(segment.text.strip() for segment in segments)

        filename = os.path.basename(audio_path).replace(".mp3", "_plain.txt")
        transcript_path = os.path.join(output_folder, filename)

        with open(transcript_path, "w", encoding="utf-8") as f:
            f.write(transcript_text)

        print(f"✅ Transcript saved: {transcript_path}")
