# Portability Score

SOBRN's portability score is a rough pre-flight signal from 0 to 100.

It is based on five dimensions:

| Dimension | Meaning |
| --- | --- |
| Provider coupling | Whether app code directly imports closed-provider SDKs or names provider API keys. |
| Model configurability | Whether model names appear hard-coded, and whether scenarios are declared in `sobrn.yml`. |
| Prompt externalization | Whether prompt-like text appears embedded in source files. |
| Local readiness | Whether local/open-weight models or Ollama appear in config or code. |
| Standards alignment | Whether OpenAI-compatible endpoints, Ollama, LiteLLM, LangChain, or LlamaIndex appear. |

The score is not a compliance result. It is a review aid.

## How to Improve the Score

- Put provider clients behind a small adapter owned by your app.
- Move model names into environment-specific configuration.
- Keep important prompts in versioned templates instead of burying them inside business logic.
- Add at least one local/open-weight model scenario to `sobrn.yml`.
- Test one OpenAI-compatible local path, such as Ollama, even if production uses a hosted model.

Run:

```bash
PYTHONPATH=cli python3 -m sobrn portability --path . --config sobrn.yml
```
