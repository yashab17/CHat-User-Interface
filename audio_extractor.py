import os
from moviepy import VideoFileClip

class AudioExtractor:
    def extract_audio(self, video_path, output_folder):
        if not (os.path.isfile(video_path) and video_path.lower().endswith(".mp4")):
            raise ValueError(f"❌ Expected a single .mp4 file. Got: {video_path}")

        os.makedirs(output_folder, exist_ok=True)

        video_file = os.path.basename(video_path)
        output_audio_file = os.path.splitext(video_file)[0] + ".mp3"
        output_audio_path = os.path.join(output_folder, output_audio_file)

        try:
            clip = VideoFileClip(video_path)
            if clip.audio:
                clip.audio.write_audiofile(output_audio_path)
                print(f"✅ Extracted audio: {output_audio_path}")
            else:
                print(f"⚠️ No audio track found in: {video_file}")
        except Exception as e:
            print(f"❌ Error processing {video_file}: {e}")