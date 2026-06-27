import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://localhost:11434/v1",
  apiKey: "ollama",
});

const response = await client.chat.completions.create({
  model: "llama3.1:8b",
  messages: [
    {
      role: "user",
      content: "Explain local-first AI in two sentences.",
    },
  ],
});

console.log(response.choices[0].message.content);
