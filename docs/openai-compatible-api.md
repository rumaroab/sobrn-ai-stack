# OpenAI-Compatible API

Ollama exposes an OpenAI-compatible API that works with many tools and SDKs expecting the OpenAI chat completions format.

In this stack, the local base URL is:

```text
http://localhost:11434/v1
```

Use any API key value for local Ollama. The examples use `ollama`.

## Curl Example

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {
        "role": "user",
        "content": "Write a short explanation of open-weight AI."
      }
    ]
  }'
```

## Python Example

See [examples/openai-compatible-python](../examples/openai-compatible-python/README.md).

Run:

```bash
cd examples/openai-compatible-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Node.js Example

See [examples/openai-compatible-node](../examples/openai-compatible-node/README.md).

Run:

```bash
cd examples/openai-compatible-node
npm install
npm start
```

## Notes

Pull the model before calling the API:

```bash
./scripts/pull-model.sh llama3.1:8b
```

If you changed `OLLAMA_PORT` in `.env`, update the base URL in your client code.
