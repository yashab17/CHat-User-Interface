# exports.transcribe = async (audioPath) => {
#   // Call Python script via child_process or use Whisper API
# };

from faster_whisper import WhisperModel
import os

class AudioTranscriber:
    def __init__(self, model_name="base", device="cpu"):
        # Initialize Whisper model with the given size and device
        self.model = WhisperModel(model_name, device=device, compute_type="int8")

    def transcribe(self, audio_folder, output_folder):
        os.makedirs(output_folder, exist_ok=True)

        for file in os.listdir(audio_folder):
            if file.endswith(".mp3"):
                audio_path = os.path.join(audio_folder, file)
                print(f"🔊 Transcribing: {audio_path}")

                segments, _ = self.model.transcribe(audio_path)
                transcript_text = " ".join(segment.text.strip() for segment in segments)

                transcript_filename = file.replace(".mp3", "_plain.txt")
                transcript_path = os.path.join(output_folder, transcript_filename)

                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(transcript_text)

                print(f"✅ Transcript saved: {transcript_path}")
