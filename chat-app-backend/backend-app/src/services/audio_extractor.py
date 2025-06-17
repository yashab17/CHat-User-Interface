# exports.extractAudio = async (videoPath, outputPath) => {
#   // Use ffmpeg to extract audio as .mp3 or .wav
  
# };

import os
from moviepy import VideoFileClip

class AudioExtractor:
    def extract_audio(self, video_folder, output_folder):
        os.makedirs(output_folder, exist_ok=True)

        for video_file in os.listdir(video_folder):
            if video_file.endswith(".mp4"):
                video_path = os.path.join(video_folder, video_file)
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