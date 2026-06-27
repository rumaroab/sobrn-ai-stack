# Pricing Checker Example

This example shows the first SOBRN pre-flight workflow.

From the repository root:

```bash
PYTHONPATH=cli python3 -m sobrn check \
  --config examples/pricing-checker/sobrn.yml \
  --path examples \
  --output reports/example-pricing-report.md
```

The command:

1. reads usage assumptions from `sobrn.yml`
2. estimates monthly token costs using `pricing/models.json`
3. scans the example code for AI SDKs, model names, API-ish URLs, and possible prompts
4. writes a Markdown report with a portability score
