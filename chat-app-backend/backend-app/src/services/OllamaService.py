# // const axios = require("axios");

# // // Call Ollama for synthesis
# // async function callLLM(prompt) {
# //   try {
# //     const response = await axios.post('http://localhost:11434/api/generate', {
# //       model: 'llama3',   // or other model you've pulled
# //       prompt: prompt,
# //       stream: false
# //     });
# //     return response.data.response;
# //   } catch (error) {
# //     console.error("Error calling LLM:", error.message);
# //     throw error;
# //   }
# // }

# // module.exports = { callLLM };

# // exports.callLLM = async (query, contextChunks) => {
# //   // Call OpenAI or local LLM (e.g., Ollama) using prompt + context
# // };

import httpx

async def call_llm(prompt: str) -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "Qwen2.5 VL",  # or other model you've pulled
                    "prompt": prompt,
                    "stream": False
                }
            )
            response.raise_for_status()
            return response.json()["response"]
    except Exception as error:
        print("Error calling LLM:", str(error))
        raise

