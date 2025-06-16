const { querySimilar } = require("../services/vectorStore");
const { callLLM } = require("../services/llmService");

exports.getLLMResponse = async (req, res) => {
  const { queryEmbedding, originalQuery } = req.body;

  try {
    const results = await querySimilar(queryEmbedding, 3);
    const context = results.map(r => r.payload.text || r.payload.source).join("\n");

    const finalPrompt = `Use the following context to answer the question:\n\n${context}\n\nQuestion: ${originalQuery}`;
    const answer = await callLLM(finalPrompt);

    res.json({ answer, contextUsed: context });
  } catch (error) {
    res.status(500).json({ error: "LLM failed to respond." });
  }
};
