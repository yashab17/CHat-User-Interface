import openai

class LLMResponder:
    def __init__(self, api_key):
        openai.api_key = api_key

    def generate_answer(self, query, context_chunks):
        context_text = "\n\n".join(context_chunks)
        prompt = f"""You are a helpful assistant. Answer the question based only on the following context:

{context_text}

Question: {query}
Answer:"""

        response = openai.ChatCompletion.create(
            model="gpt-4",  # or "gpt-3.5-turbo"
            messages=[
                {"role": "system", "content": "You are a multimodal assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=300
        )

        return response.choices[0].message["content"]
