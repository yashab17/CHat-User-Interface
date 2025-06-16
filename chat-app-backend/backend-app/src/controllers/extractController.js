


const { extractFrames } = require("../services/frameExtractor");
const { extractAudio } = require("../services/audioExtractor");
const { transcribe } = require("../services/whisperTranscriber");

exports.extractFramesAndAudio = async (req, res) => {
  const { videoPath, outputPath } = req.body;
  await extractFrames(videoPath, outputPath);
  await extractAudio(videoPath, outputPath);
  res.send("Frames and audio extracted.");
};

exports.transcribeAudio = async (req, res) => {
  const { audioPath } = req.body;
  const transcript = await transcribe(audioPath);
  res.json({ transcript });
};
