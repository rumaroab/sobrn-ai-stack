# Pricing Checker

SOBRN's CLI is a pre-flight pricing checker for AI apps. It does not observe production traffic or call provider APIs. Instead, it combines your local usage assumptions with a local model-price catalog.

## Configure Assumptions

Create `sobrn.yml`:

```yaml
project:
  name: My AI App

usage:
  requests_per_month: 100000
  input_tokens_per_request: 1200
  output_tokens_per_request: 500

scenarios:
  - name: Hosted baseline
    model: openai/gpt-4o-mini
  - name: Local fallback
    model: ollama/llama3.1:8b
```

Top-level `usage` values are defaults. A scenario can override any usage value:

```yaml
scenarios:
  - name: Expensive admin workflow
    model: openai/gpt-4o
    requests_per_month: 5000
    input_tokens_per_request: 8000
    output_tokens_per_request: 2000
```

## Run

```bash
PYTHONPATH=cli python3 -m sobrn estimate --config sobrn.yml
```

Or generate the full report:

```bash
PYTHONPATH=cli python3 -m sobrn check --config sobrn.yml --path . --output reports/pricing-report.md
```

## Pricing Catalog

The default catalog is `pricing/models.json`.

Prices are per 1 million tokens:

- `input_per_1m`
- `output_per_1m`

Local models can use `0.0` token prices, but that does not mean the workload is free. Add hardware, hosting, support, power, and operations costs to your own planning.
