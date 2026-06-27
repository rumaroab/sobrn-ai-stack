# OpenAI-Compatible Python Example

This example uses the OpenAI Python SDK against local Ollama.

Start the stack and pull a model first:

```bash
cd ../..
cp .env.example .env
docker compose up -d
./scripts/pull-model.sh llama3.1:8b
```

Run the example:

```bash
cd examples/openai-compatible-python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The example uses:

- base URL: `http://localhost:11434/v1`
- model: `llama3.1:8b`
- API key: `ollama`
