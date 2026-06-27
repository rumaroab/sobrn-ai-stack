# Code Scanner

The SOBRN scanner looks for AI-related dependencies and coupling points in a local codebase.

It currently detects:

- provider SDK imports and package references
- local/Ollama references
- LiteLLM, LangChain, and LlamaIndex references
- model-looking strings such as `gpt-4o-mini`, `claude-*`, `llama3.1:8b`, and catalog model IDs
- API-key environment variable names
- AI-ish base URLs such as OpenAI-compatible `/v1` endpoints
- prompt-like lines containing roles, prompt variables, messages, or instructions

Run:

```bash
PYTHONPATH=cli python3 -m sobrn scan --path .
```

The scanner is heuristic. It is meant to surface review targets quickly, not to prove that a codebase has no AI dependencies.

## Practical Use

Use scanner output to answer:

- Which provider SDKs are directly imported?
- Are model names hard-coded in application code?
- Are prompts embedded in code rather than templates or configuration?
- Does the app already use an OpenAI-compatible endpoint or portability layer?
