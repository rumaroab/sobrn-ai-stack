# OpenAI-Compatible Node.js Example

This example uses the OpenAI Node.js SDK against local Ollama.

Start the stack and pull a model first:

```bash
cd ../..
cp .env.example .env
docker compose up -d
./scripts/pull-model.sh llama3.1:8b
```

Run the example:

```bash
cd examples/openai-compatible-node
npm install
npm start
```

The example uses:

- base URL: `http://localhost:11434/v1`
- model: `llama3.1:8b`
- API key: `ollama`
