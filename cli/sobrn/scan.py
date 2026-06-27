from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .pricing import catalog_model_ids, load_catalog
from .utils import iter_project_files, read_text, relpath


PROVIDER_PATTERNS = [
    ("openai", "OpenAI SDK", re.compile(r"\b(from\s+openai\s+import|import\s+OpenAI|require\(['\"]openai['\"]\)|from\s+['\"]openai['\"]|@langchain/openai)\b")),
    ("anthropic", "Anthropic SDK", re.compile(r"\b(from\s+anthropic\s+import|import\s+Anthropic|@anthropic-ai/sdk|require\(['\"]@anthropic-ai/sdk['\"]\))\b")),
    ("google", "Google Gemini SDK", re.compile(r"\b(google-generativeai|@google/generative-ai|from\s+google\s+import\s+genai|GoogleGenerativeAI)\b")),
    ("cohere", "Cohere SDK", re.compile(r"\b(import\s+cohere|from\s+cohere\s+import|require\(['\"]cohere-ai['\"]\)|cohere-ai)\b")),
    ("mistral", "Mistral SDK", re.compile(r"\b(@mistralai/mistralai|from\s+mistralai\s+import|import\s+Mistral)\b")),
    ("groq", "Groq SDK", re.compile(r"\b(from\s+groq\s+import|import\s+Groq|groq-sdk)\b")),
    ("ollama", "Ollama", re.compile(r"\b(ollama|localhost:11434|OLLAMA_HOST)\b")),
    ("litellm", "LiteLLM", re.compile(r"\b(import\s+litellm|from\s+litellm\s+import|litellm\.completion)\b")),
    ("langchain", "LangChain", re.compile(r"\b(langchain|@langchain/)\b")),
    ("llamaindex", "LlamaIndex", re.compile(r"\b(llama_index|llamaindex)\b")),
]

MODEL_PATTERN = re.compile(
    r"(?<![A-Za-z0-9_./:-])("
    r"gpt-[A-Za-z0-9_.:-]+|"
    r"claude-[A-Za-z0-9_.:-]+|"
    r"gemini-[A-Za-z0-9_.:-]+|"
    r"llama[0-9.:-]*[A-Za-z0-9_.:-]*|"
    r"mistral[A-Za-z0-9_.:-]*|"
    r"mixtral[A-Za-z0-9_.:-]*|"
    r"qwen[0-9.:-]*[A-Za-z0-9_.:-]*|"
    r"phi[0-9.:-]*[A-Za-z0-9_.:-]*|"
    r"deepseek[A-Za-z0-9_.:-]*|"
    r"command-[A-Za-z0-9_.:-]+"
    r")(?![A-Za-z0-9_./:-])",
    re.IGNORECASE,
)

API_KEY_PATTERN = re.compile(
    r"\b([A-Z][A-Z0-9_]*(?:OPENAI|ANTHROPIC|GEMINI|GOOGLE|COHERE|MISTRAL|GROQ|AI|LLM)[A-Z0-9_]*_API_KEY|(?:OPENAI|ANTHROPIC|GEMINI|GOOGLE|COHERE|MISTRAL|GROQ)_API_KEY)\b"
)
BASE_URL_PATTERN = re.compile(r"https?://[A-Za-z0-9_.:/-]+(?:/v1)?")
PROMPT_HINT_PATTERN = re.compile(
    r"\b(system|developer|user|assistant|role|prompt|instruction|messages|chat_template)\b",
    re.IGNORECASE,
)


def scan_path(root: Path, catalog_path: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    catalog = load_catalog(catalog_path)
    known_model_ids = catalog_model_ids(catalog)
    provider_hits: list[dict[str, Any]] = []
    model_hits: list[dict[str, Any]] = []
    prompt_hits: list[dict[str, Any]] = []
    api_key_hits: list[dict[str, Any]] = []
    base_url_hits: list[dict[str, Any]] = []

    files = iter_project_files(root)
    for file_path in files:
        text = read_text(file_path)
        for line_number, line in enumerate(text.splitlines(), start=1):
            clean = line.strip()
            if not clean:
                continue
            relative_file = relpath(file_path, root)

            for provider, label, pattern in PROVIDER_PATTERNS:
                if pattern.search(line):
                    provider_hits.append(
                        {
                            "provider": provider,
                            "label": label,
                            "file": relative_file,
                            "line": line_number,
                            "snippet": _snippet(clean),
                        }
                    )

            for model in _find_models(line, known_model_ids):
                model_hits.append(
                    {
                        "model": model,
                        "file": relative_file,
                        "line": line_number,
                        "snippet": _snippet(clean),
                    }
                )

            for api_key in sorted(set(API_KEY_PATTERN.findall(line))):
                api_key_hits.append(
                    {
                        "name": api_key,
                        "file": relative_file,
                        "line": line_number,
                        "snippet": _snippet(clean),
                    }
                )

            for url in sorted(set(BASE_URL_PATTERN.findall(line))):
                if any(token in url.lower() for token in ("openai", "anthropic", "google", "localhost", "11434", "/v1")):
                    base_url_hits.append(
                        {
                            "url": url,
                            "file": relative_file,
                            "line": line_number,
                            "snippet": _snippet(clean),
                        }
                    )

            if _looks_like_prompt(clean):
                prompt_hits.append(
                    {
                        "file": relative_file,
                        "line": line_number,
                        "snippet": _snippet(clean),
                    }
                )

    return {
        "root": root.as_posix(),
        "files_scanned": len(files),
        "provider_hits": _dedupe_hits(provider_hits),
        "model_hits": _dedupe_hits(model_hits),
        "prompt_hits": _dedupe_hits(prompt_hits)[:50],
        "api_key_hits": _dedupe_hits(api_key_hits),
        "base_url_hits": _dedupe_hits(base_url_hits),
        "summary": {
            "providers": sorted({hit["provider"] for hit in provider_hits}),
            "models": sorted({hit["model"] for hit in model_hits}),
            "api_keys": sorted({hit["name"] for hit in api_key_hits}),
            "base_urls": sorted({hit["url"] for hit in base_url_hits}),
            "prompt_like_lines": len(_dedupe_hits(prompt_hits)),
        },
    }


def _find_models(line: str, known_model_ids: set[str]) -> set[str]:
    found = {match.group(1) for match in MODEL_PATTERN.finditer(line)}
    for model_id in known_model_ids:
        if _contains_model_token(line, model_id):
            found.add(model_id)
        short_id = model_id.split("/", 1)[-1]
        if short_id and _contains_model_token(line, short_id):
            found.add(short_id)
    return found


def _contains_model_token(line: str, model: str) -> bool:
    return bool(
        re.search(
            rf"(?<![A-Za-z0-9_./:-]){re.escape(model)}(?![A-Za-z0-9_./:-])",
            line,
        )
    )


def _looks_like_prompt(line: str) -> bool:
    if not PROMPT_HINT_PATTERN.search(line):
        return False
    lower = line.lower()
    if "response.choices" in lower or ".message.content" in lower:
        return False
    if "http" in lower and "prompt" not in lower:
        return False
    return any(marker in line for marker in ("=", ":", "{", "[", "(", '"', "'"))


def _snippet(line: str, limit: int = 140) -> str:
    compact = " ".join(line.split())
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3] + "..."


def _dedupe_hits(hits: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[tuple[str, str], ...]] = set()
    deduped: list[dict[str, Any]] = []
    for hit in hits:
        key = tuple(sorted((str(k), str(v)) for k, v in hit.items()))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(hit)
    return deduped
