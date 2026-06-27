# Example AI App AI Pricing and Portability Report

Generated: 2026-06-28
Config: `examples/pricing-checker/sobrn.yml`
Pricing catalog snapshot: `2026-06-27`

## Cost Estimate

| Scenario | Provider | Model | Requests/mo | Input tokens/mo | Output tokens/mo | Est. monthly cost |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Hosted baseline | openai | `openai/gpt-4o-mini` | 100,000 | 120,000,000 | 50,000,000 | $48.00 |
| Higher quality hosted | openai | `openai/gpt-4o` | 100,000 | 120,000,000 | 50,000,000 | $800.00 |
| Local portability check | ollama | `ollama/llama3.1:8b` | 100,000 | 120,000,000 | 50,000,000 | $0.00 |

### Pricing Notes

- Public price snapshot; update for current rates.
- Token fees modeled as $0. Add hardware, hosting, and operations costs separately.

## Code Scan

Files scanned: `8`

- Providers/tooling: ollama, openai
- Model references: `llama3.1:8b`, `ollama/llama3.1:8b`, `openai/gpt-4o`, `openai/gpt-4o-mini`
- API key env vars: `none detected`
- AI-ish base URLs: `http://localhost:11434/v1`
- Prompt-like lines: `4`

### Provider Hits

- `openai-compatible-node/README.md:24` - Ollama
- `openai-compatible-node/README.md:26` - Ollama
- `openai-compatible-node/index.js:1` - OpenAI SDK
- `openai-compatible-node/index.js:4` - Ollama
- `openai-compatible-node/index.js:5` - Ollama
- `openai-compatible-python/README.md:26` - Ollama
- `openai-compatible-python/README.md:28` - Ollama
- `openai-compatible-python/main.py:1` - OpenAI SDK
- `openai-compatible-python/main.py:5` - Ollama
- `openai-compatible-python/main.py:6` - Ollama

### Model Hits

- `openai-compatible-node/README.md:11` - llama3.1:8b
- `openai-compatible-node/README.md:25` - llama3.1:8b
- `openai-compatible-node/index.js:9` - llama3.1:8b
- `openai-compatible-python/README.md:11` - llama3.1:8b
- `openai-compatible-python/README.md:27` - llama3.1:8b
- `openai-compatible-python/main.py:10` - llama3.1:8b
- `pricing-checker/sobrn.yml:11` - openai/gpt-4o-mini
- `pricing-checker/sobrn.yml:13` - openai/gpt-4o
- `pricing-checker/sobrn.yml:15` - ollama/llama3.1:8b

### Possible Prompts

- `openai-compatible-node/index.js:10` - messages: [
- `openai-compatible-node/index.js:12` - role: "user",
- `openai-compatible-python/main.py:11` - messages=[
- `openai-compatible-python/main.py:13` - "role": "user",

## Portability Score

Score: **88/100 (A)**

| Dimension | Score |
| --- | ---: |
| Provider Coupling | 85/100 |
| Model Configurability | 82/100 |
| Prompt Externalization | 80/100 |
| Local Readiness | 100/100 |
| Standards Alignment | 100/100 |

### Findings

- Closed-provider SDKs detected: openai.
- Hard-coded or directly referenced model names detected: llama3.1:8b, ollama/llama3.1:8b, openai/gpt-4o, openai/gpt-4o-mini.
- 4 prompt-like code lines detected.
- Portability-friendly tooling detected: ollama.

### Recommendations

- Put provider clients behind a small internal adapter.
- Move model names into configuration and test at least one fallback model.
- Externalize important prompts or templates so they can be evaluated across models.

## Caveats

- Estimates use local assumptions from `sobrn.yml`; they are not billing statements.
- The pricing catalog is a local snapshot. Update `pricing/models.json` for current public prices, negotiated rates, or self-hosted infrastructure costs.
- Scanner findings are heuristic and intended for pre-flight review, not compliance certification.
