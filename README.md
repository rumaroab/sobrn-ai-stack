# SOBRN

Pre-flight AI pricing and portability checking for developers.

SOBRN helps you understand what your AI app depends on before pricing, access, policy, or infrastructure constraints force a rushed migration.

It answers three practical questions:

- What AI providers, SDKs, prompts, and models does my app depend on?
- What will my AI usage probably cost under realistic assumptions?
- How portable is my AI app if I need to switch providers or run open-weight/local models?

SOBRN also includes a small local AI stack with Ollama and Open WebUI, so you can test open-weight models on infrastructure you control.

## Mission

Most AI apps depend completely on a small number of closed providers. That is convenient until pricing, access, policy, privacy requirements, or outages change.

This project is not anti-frontier AI. It is pro-portability: use local and open-weight models where they fit, and use hosted frontier models where they are the right tool.

Run what you can. Rent what you must.

## What SOBRN Is

- A local Python CLI called `sobrn`
- A local pricing catalog for model cost estimates
- A scanner for provider SDKs, model names, API keys, base URLs, and prompt-like code
- A basic portability score with findings and recommendations
- A Docker Compose local AI stack for Ollama and Open WebUI

SOBRN runs locally and does not call external APIs.

## What SOBRN Is Not

SOBRN is not trying to replace Langfuse, LangSmith, Helicone, LiteLLM, Ollama, Open WebUI, or vLLM.

Those are runtime, observability, gateway, model-serving, and local-model tools. SOBRN's wedge is the pre-flight check: before you commit to a provider, model, prompt architecture, or deployment path, it gives you a local report on cost and portability.

## Quick Start: Pricing and Portability

Requirements:

- Python 3.10+

Run the bundled example:

```bash
PYTHONPATH=cli python3 -m sobrn check \
  --config examples/pricing-checker/sobrn.yml \
  --path examples \
  --output reports/example-pricing-report.md
```

The report includes:

- monthly cost estimates from `sobrn.yml`
- code scan findings
- a portability score
- recommendations for reducing provider and model lock-in

Install the CLI locally:

```bash
python3 -m pip install -e ./cli
sobrn check --config examples/pricing-checker/sobrn.yml --path examples
```

More detail:

- [Pricing checker](docs/pricing-checker.md)
- [Scanner](docs/scanner.md)
- [Portability score](docs/portability-score.md)

## Quick Start: Local AI Stack

Requirements:

- Docker
- Docker Compose

Start the stack:

```bash
cp .env.example .env
docker compose up -d
```

Pull a first model:

```bash
./scripts/pull-model.sh llama3.1:8b
```

If you do not pass a model name, the script defaults to `llama3.1:8b`:

```bash
./scripts/pull-model.sh
```

Open Open WebUI:

[http://localhost:3000](http://localhost:3000)

Check the stack:

```bash
./scripts/healthcheck.sh
```

Stop the stack:

```bash
docker compose down
```

## Local OpenAI-Compatible API

Ollama exposes an OpenAI-compatible API at:

```text
http://localhost:11434/v1
```

Example request:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "messages": [
      {
        "role": "user",
        "content": "Explain local-first AI in one paragraph."
      }
    ]
  }'
```

SDK examples:

- [Python example](examples/openai-compatible-python/README.md)
- [Node.js example](examples/openai-compatible-node/README.md)

More detail: [OpenAI-compatible API docs](docs/openai-compatible-api.md).

## Recommended First Models

- `llama3.1:8b` for first local chat
- `phi3:mini` for lightweight machines
- `qwen2.5-coder:7b` for coding
- `mistral:7b` for multilingual and general use

See [models.md](docs/models.md) for notes and tradeoffs.

## Documentation

- [Getting started](docs/getting-started.md)
- [Models](docs/models.md)
- [Hardware](docs/hardware.md)
- [OpenAI-compatible API](docs/openai-compatible-api.md)
- [Pricing checker](docs/pricing-checker.md)
- [Scanner](docs/scanner.md)
- [Portability score](docs/portability-score.md)

## Project Status

Early MVP.

The first stack goal is intentionally small: clone the repo, start Docker Compose, open Open WebUI, pull an open-weight model, and call a local OpenAI-compatible API.

The first CLI goal is also intentionally small: run a fully local pre-flight pricing and portability check using static assumptions, a local pricing catalog, and heuristic code scanning.

## Roadmap

- Add optional GPU notes for common local setups
- Add more OpenAI-compatible API examples
- Add backup and restore guidance for Docker volumes
- Add model evaluation and prompt-testing examples
- Improve pricing catalog coverage and scenario modeling
- Add richer scanner language support and CI examples
- Add optional self-hosted deployment profiles
- Add an optional production-oriented vLLM profile
- Add security hardening guidance for remote deployments

## License

Apache-2.0. See [LICENSE](LICENSE).
