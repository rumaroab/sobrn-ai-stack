from openai import OpenAI


client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="llama3.1:8b",
    messages=[
        {
            "role": "user",
            "content": "Explain local-first AI in two sentences.",
        }
    ],
)

print(response.choices[0].message.content)
