# SOBRN Pricing Catalog

`models.json` is a local pricing catalog used by the `sobrn` CLI.

It is intentionally simple:

- prices are stored per 1 million input and output tokens
- local/open-weight models can be represented with `$0` token pricing
- infrastructure, storage, GPU rental, support, and operations costs are not automatically modeled
- entries can represent public pricing, negotiated contracts, or internal cost assumptions

The catalog is a planning input, not a live price feed. Update it before using reports for financial decisions.

## Model Entry Shape

```json
{
  "id": "openai/gpt-4o-mini",
  "provider": "openai",
  "display_name": "GPT-4o mini",
  "input_per_1m": 0.15,
  "output_per_1m": 0.6,
  "currency": "USD",
  "context_window": 128000,
  "open_weight": false,
  "local": false,
  "openai_compatible": true,
  "notes": "Public price snapshot; update for current rates."
}
```
