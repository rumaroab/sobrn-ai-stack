# SOBRN CLI

`sobrn` is a local pre-flight AI pricing and portability checker.

It helps answer:

- Which AI providers, SDKs, model names, prompts, and API keys appear in this codebase?
- What will the configured AI usage probably cost under local assumptions?
- How portable does this app look if you need to switch providers or run local/open-weight models?

The CLI does not call external APIs. It reads `sobrn.yml`, scans local files, and uses the local catalog in `pricing/models.json`.

## Install for Development

From the repository root:

```bash
python3 -m pip install -e ./cli
```

Then run:

```bash
sobrn check --config examples/pricing-checker/sobrn.yml --path examples --output reports/example-pricing-report.md
```

Without installation:

```bash
PYTHONPATH=cli python3 -m sobrn check --config examples/pricing-checker/sobrn.yml --path examples
```

## Commands

```bash
sobrn check
sobrn estimate --config sobrn.yml
sobrn scan --path .
sobrn portability --path .
```

`check` is the main workflow. It estimates costs, scans the codebase, calculates a basic portability score, and writes a Markdown report.

## Configuration

Create a `sobrn.yml` file:

```yaml
project:
  name: Example App

usage:
  requests_per_month: 100000
  input_tokens_per_request: 1200
  output_tokens_per_request: 500

scenarios:
  - name: Hosted baseline
    model: openai/gpt-4o-mini
  - name: Local option
    model: ollama/llama3.1:8b
```

Scenario-level values override top-level `usage` values.

## Price Catalog

Prices are local snapshots for planning, not live billing guarantees. Update `pricing/models.json` for your own providers, negotiated rates, or self-hosting assumptions.
