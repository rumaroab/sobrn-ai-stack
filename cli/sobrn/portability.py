from __future__ import annotations

from typing import Any

from .pricing import model_prices


CLOSED_PROVIDERS = {"openai", "anthropic", "google", "cohere", "mistral", "groq"}
PORTABILITY_PROVIDERS = {"ollama", "litellm", "langchain", "llamaindex"}


def score_portability(
    scan_result: dict[str, Any],
    catalog: dict[str, Any] | None = None,
    assumptions: dict[str, Any] | None = None,
) -> dict[str, Any]:
    summary = scan_result.get("summary", {})
    providers = set(summary.get("providers", []))
    models = set(summary.get("models", []))
    prompt_count = int(summary.get("prompt_like_lines", 0))
    api_keys = set(summary.get("api_keys", []))
    base_urls = set(summary.get("base_urls", []))

    dimensions = {
        "provider_coupling": 100,
        "model_configurability": 100,
        "prompt_externalization": 100,
        "local_readiness": 50,
        "standards_alignment": 50,
    }

    closed_hits = providers & CLOSED_PROVIDERS
    if closed_hits:
        dimensions["provider_coupling"] -= min(45, 15 * len(closed_hits))
    if api_keys:
        dimensions["provider_coupling"] -= min(20, 5 * len(api_keys))

    if models:
        dimensions["model_configurability"] -= min(35, 7 * len(models))
    if assumptions and assumptions.get("scenarios"):
        dimensions["model_configurability"] += 10

    if prompt_count:
        dimensions["prompt_externalization"] -= min(45, prompt_count * 5)

    if providers & PORTABILITY_PROVIDERS:
        dimensions["standards_alignment"] += 20
    if any("/v1" in url or "localhost:11434" in url for url in base_urls):
        dimensions["standards_alignment"] += 20
    if "openai" in providers and base_urls:
        dimensions["standards_alignment"] += 10

    local_model_ids = set()
    open_weight_model_ids = set()
    if catalog:
        for model_id, price in model_prices(catalog).items():
            if price.local:
                local_model_ids.add(model_id)
                local_model_ids.add(model_id.split("/", 1)[-1])
            if price.open_weight:
                open_weight_model_ids.add(model_id)
                open_weight_model_ids.add(model_id.split("/", 1)[-1])

    configured_models = _configured_models(assumptions)
    if models & local_model_ids or configured_models & local_model_ids or "ollama" in providers:
        dimensions["local_readiness"] += 35
    if models & open_weight_model_ids or configured_models & open_weight_model_ids:
        dimensions["local_readiness"] += 15

    for key, value in list(dimensions.items()):
        dimensions[key] = max(0, min(100, value))

    weights = {
        "provider_coupling": 0.28,
        "model_configurability": 0.22,
        "prompt_externalization": 0.18,
        "local_readiness": 0.18,
        "standards_alignment": 0.14,
    }
    score = round(sum(dimensions[key] * weight for key, weight in weights.items()))

    findings = []
    if closed_hits:
        findings.append(
            "Closed-provider SDKs detected: " + ", ".join(sorted(closed_hits)) + "."
        )
    if models:
        findings.append(
            "Hard-coded or directly referenced model names detected: "
            + ", ".join(sorted(models)[:8])
            + ("." if len(models) <= 8 else ", ...")
        )
    if prompt_count:
        findings.append(f"{prompt_count} prompt-like code lines detected.")
    if providers & PORTABILITY_PROVIDERS:
        findings.append(
            "Portability-friendly tooling detected: "
            + ", ".join(sorted(providers & PORTABILITY_PROVIDERS))
            + "."
        )
    if not findings:
        findings.append("No obvious provider or prompt coupling was detected.")

    recommendations = []
    if closed_hits:
        recommendations.append("Put provider clients behind a small internal adapter.")
    if models:
        recommendations.append("Move model names into configuration and test at least one fallback model.")
    if prompt_count:
        recommendations.append("Externalize important prompts or templates so they can be evaluated across models.")
    if "ollama" not in providers and not configured_models & local_model_ids:
        recommendations.append("Add one local/open-weight scenario to sobrn.yml for a realistic portability baseline.")
    if not recommendations:
        recommendations.append("Keep the scanner in CI as a pre-flight check before provider or model changes.")

    return {
        "score": score,
        "grade": _grade(score),
        "dimensions": dimensions,
        "findings": findings,
        "recommendations": recommendations,
    }


def _configured_models(assumptions: dict[str, Any] | None) -> set[str]:
    if not assumptions:
        return set()
    models: set[str] = set()
    for scenario in assumptions.get("scenarios", []):
        if isinstance(scenario, dict) and scenario.get("model"):
            model = str(scenario["model"])
            models.add(model)
            models.add(model.split("/", 1)[-1])
    return models


def _grade(score: int) -> str:
    if score >= 85:
        return "A"
    if score >= 70:
        return "B"
    if score >= 55:
        return "C"
    if score >= 40:
        return "D"
    return "F"
