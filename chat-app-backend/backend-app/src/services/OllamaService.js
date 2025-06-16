const axios = require("axios");

// Call Ollama for synthesis
async function callLLM(prompt) {
  try {
    const response = await axios.post('http://localhost:11434/api/generate', {
      model: 'llama3',   // or other model you've pulled
      prompt: prompt,
      stream: false
    });
    return response.data.response;
  } catch (error) {
    console.error("Error calling LLM:", error.message);
    throw error;
  }
}

module.exports = { callLLM };

exports.callLLM = async (query, contextChunks) => {
  // Call OpenAI or local LLM (e.g., Ollama) using prompt + context
};

