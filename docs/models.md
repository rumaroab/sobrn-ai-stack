# Models

SOBRN AI Stack uses Ollama, so models are pulled with `ollama pull` inside the Ollama container.

Use the helper script:

```bash
./scripts/pull-model.sh llama3.1:8b
```

## Starter Recommendations

| Model | Good For | Notes |
| --- | --- | --- |
| `llama3.1:8b` | First local chat | A practical default for trying local chat on modern machines. |
| `phi3:mini` | Lightweight machines | Smaller and easier to run when CPU, memory, or disk are limited. |
| `qwen2.5-coder:7b` | Coding | Useful for code-focused local experiments. |
| `mistral:7b` | Multilingual and general use | A capable general-purpose model for many local workflows. |

Model recommendations will evolve as open-weight models, quantization, and local runtimes improve.

## Choosing a Model

Start with the smallest model that gives useful results for your task. Larger models often improve quality, but they need more memory, disk, and patience.

For a first run:

```bash
./scripts/pull-model.sh llama3.1:8b
```

For a lighter first run:

```bash
./scripts/pull-model.sh phi3:mini
```

For coding:

```bash
./scripts/pull-model.sh qwen2.5-coder:7b
```

## List Installed Models

```bash
curl http://localhost:11434/api/tags
```

Or from inside the container:

```bash
docker exec sobrn-ollama ollama list
```
