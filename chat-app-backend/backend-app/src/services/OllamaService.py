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

# async def prepare_and_call_llm(prompt: str, results_final: list) -> str:
#     # Extract and format video frames
#     video_frames = []
#     transcripts = []
    
#     for result in results_final:
#         # Add transcript entries
#         if result["text"] and result["text_timestamp"]:
#             transcript_entry = {
#                 "text": result["text"],
#                 "timestamp": result["text_timestamp"]
#             }
#             transcripts.append(transcript_entry)
            
#         # Add frame entries if image data exists
#         if result["image_path"] and result["image_timestamp"]:
#             frame_entry = {
#                 "description": f"Frame from video {result['video_id']}",
#                 "timestamp": result["image_timestamp"],
#                 "path": result["image_path"],
#                 "frame_number": result["image_frame"]
#             }
#             video_frames.append(frame_entry)
    
#     # Sort by timestamp
#     video_frames.sort(key=lambda x: x["timestamp"])
#     transcripts.sort(key=lambda x: x["timestamp"])
    
#     # Call the LLM with the prepared context
#     try:
#         return await call_llm(
#             prompt=prompt,
#             video_frames=video_frames,
#             transcripts=transcripts
#         )
#     except Exception as error:
#         print(f"Error in prepare_and_call_llm: {str(error)}")
#         raise

# Example usage:
# response = await prepare_and_call_llm(
#     prompt="What is happening in this video?",
#     results_final=results_final
# )


async def call_llm(prompt: str, results_final:dict = None) -> str:
    try:
        # Prepare context from video frames and transcripts
        # context = ""
        # if video_frames:
        #     context += "\nVideo Frame Context:\n"
        #     for i, frame in enumerate(video_frames):
        #         context += f"Frame {i+1}: {frame['description']}\n"
                
        # if transcripts:
        #     context += "\nTranscript Context:\n"
        #     for i, transcript in enumerate(transcripts):
        #         context += f"Segment {i+1}: {transcript['text']} [{transcript['timestamp']}]\n"
        
        # # Combine prompt with context
        # enhanced_prompt = f"{context}\n\nUser Query: {prompt}"

        text_chunks = "\n\n".join(
        [
            f"Text Snippet {i + 1} [{item['timestamp']:.2f}s]:\n{item['text']}"
            for i, item in enumerate(results_final["text"])
        ]
    )

    # Build image references
        image_refs = "\n".join(
        [
            f"Image Frame {i + 1} (~{img['timestamp_guess']:.2f}s): {img['frame']}"
            for i, img in enumerate(results_final["images"])
        ]
    )

        # Compose final prompt
        final_prompt = f"""
You are an intelligent VideoRag Interface that helps users find answers from questions based on specific information from long-form videos.

The user has asked a question based on video content. You have access to the most relevant transcript excerpts and visual snapshots (frames) retrieved using semantic similarity from a vector database.

Use both the transcript and visual context to understand the intent behind the question and synthesize a clear, accurate, and concise response.
User Question: "{prompt}"

        Transcript Context:
        {text_chunks}

        Relevant Frame References:
        {image_refs}
        """
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:8000/query",
                json={
                    "model": "qwen/qwen2.5-vl-72b-instruct:free",
                    "prompt": final_prompt,
                    "stream": False 
                }
       )
            response.raise_for_status()
            return response.json()["response"]
    except Exception as error:
        print("Error calling LLM:", str(error))
        raise