


# // const { extractFrames } = require("../services/frameExtractor");
# // const { extractAudio } = require("../services/audioExtractor");
# // const { transcribe } = require("../services/whisperTranscriber");

# // exports.extractFramesAndAudio = async (req, res) => {
# //   const { videoPath, outputPath } = req.body;
# //   await extractFrames(videoPath, outputPath);
# //   await extractAudio(videoPath, outputPath);
# //   res.send("Frames and audio extracted.");
# // };

# // exports.transcribeAudio = async (req, res) => {
# //   const { audioPath } = req.body;
# //   const transcript = await transcribe(audioPath);
# //   res.json({ transcript });
# // };


from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from services.FrameExtractor import extract_frames
from services.AudioExtractor import extract_audio
from services.Transcriber import transcribe


# Import your Python service functions here
# from app.services.frame_extractor import extract_frames
# from app.services.audio_extractor import extract_audio
# from app.services.whisper_transcriber import transcribe

router = APIRouter()

class ExtractRequest(BaseModel):
    videoPath: str
    outputPath: str

class TranscribeRequest(BaseModel):
    audioPath: str

@router.post("/extract-frames-audio")
async def extract_frames_and_audio(request: ExtractRequest):
    Frames=extract_frames(request.videoPath, request.outputPath)
    Audio=extract_audio(request.videoPath, request.outputPath)


    # Replace above with actual function calls
    return Frames,Audio

@router.post("/transcribe-audio")
async def transcribe_audio(request: TranscribeRequest):
    transcript = transcribe(request.audioPath)
    return transcript