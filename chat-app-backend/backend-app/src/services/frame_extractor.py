# exports.extractFrames = async (videoPath, outputPath) => {
#   // Use ffmpeg or opencv bindings in Node.js
# };

import cv2
import os
from datetime import timedelta
from collections import defaultdict

class FrameExtractor:
    def __init__(self, frame_rate=2):
        self.frame_rate = frame_rate

    def extract_frames(self, video_folder, output_folder):
        os.makedirs(output_folder, exist_ok=True)

        for video_file in os.listdir(video_folder):
            if video_file.endswith(".mp4"):
                video_path = os.path.join(video_folder, video_file)
                cap = cv2.VideoCapture(video_path)
                fps = cap.get(cv2.CAP_PROP_FPS)

                output_subfolder = os.path.join(output_folder, os.path.splitext(video_file)[0])
                os.makedirs(output_subfolder, exist_ok=True)

                second_frame_counter = defaultdict(int)
                success, image = cap.read()
                frame_number = 0

                while success:
                    # Extract frames at the specified rate
                    if frame_number % int(fps // self.frame_rate) == 0:
                        seconds = int(frame_number / fps)
                        timestamp = str(timedelta(seconds=seconds)).replace(":", "-")

                        second_frame_counter[timestamp] += 1
                        index = second_frame_counter[timestamp]

                        output_filename = os.path.join(output_subfolder, f"{timestamp}_{index}.jpg")
                        cv2.imwrite(output_filename, image)

                    success, image = cap.read()
                    frame_number += 1

                cap.release()