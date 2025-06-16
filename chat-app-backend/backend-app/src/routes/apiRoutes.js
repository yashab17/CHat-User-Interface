const express = require("express");
const router = express.Router();
const {
  extractFramesAndAudio,
  transcribeAudio
} = require("../controllers/extractController");

const {
  generateEmbeddings,
  storeInVectorDB
} = require("../controllers/embedController");

const {
  queryVectorDB
} = require("../controllers/searchController");

const {
  getLLMResponse
} = require("../controllers/llmController");

// Video processing
router.post("/extract", extractFramesAndAudio);
router.post("/transcribe", transcribeAudio);

// Embedding + Store
router.post("/embed", generateEmbeddings);
router.post("/store", storeInVectorDB);

// Query + LLM
router.post("/query", queryVectorDB);
router.post("/synthesize", getLLMResponse);

module.exports = router;
