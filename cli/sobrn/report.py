from __future__ import annotations

from datetime import date
from typing import Any

from .estimate import Estimate


def render_report(
    *,
    project_name: str,
    config_path: str,
    pricing_catalog: dict[str, Any],
    estimates: list[Estimate],
    scan_result: dict[str, Any] | None = None,
    portability: dict[str, Any] | None = None,
) -> str:
    catalog_date = pricing_catalog.get("as_of", "unknown")
    lines = [
        f"# {project_name} AI Pricing and Portability Report",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Config: `{config_path}`",
        f"Pricing catalog snapshot: `{catalog_date}`",
        "",
        "## Cost Estimate",
        "",
        "| Scenario | Provider | Model | Requests/mo | Input tokens/mo | Output tokens/mo | Est. monthly cost |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: |",
    ]

    for estimate in estimates:
        lines.append(
            "| "
            + " | ".join(
                [
                    _cell(estimate.name),
                    _cell(estimate.provider),
                    f"`{_cell(estimate.model)}`",
                    f"{estimate.requests_per_month:,}",
                    f"{estimate.monthly_input_tokens:,}",
                    f"{estimate.monthly_output_tokens:,}",
                    _money(estimate.total_cost, estimate.currency),
                ]
            )
            + " |"
        )

    notes = [estimate.notes for estimate in estimates if estimate.notes]
    if notes:
        lines.extend(["", "### Pricing Notes", ""])
        for note in sorted(set(notes)):
            lines.append(f"- {note}")

    if scan_result:
        lines.extend(["", render_scan_section(scan_result)])

    if portability:
        lines.extend(["", render_portability_section(portability)])

    lines.extend(
        [
            "",
            "## Caveats",
            "",
            "- Estimates use local assumptions from `sobrn.yml`; they are not billing statements.",
            "- The pricing catalog is a local snapshot. Update `pricing/models.json` for current public prices, negotiated rates, or self-hosted infrastructure costs.",
            "- Scanner findings are heuristic and intended for pre-flight review, not compliance certification.",
            "",
        ]
    )
    return "\n".join(lines)


def render_scan_section(scan_result: dict[str, Any]) -> str:
    summary = scan_result.get("summary", {})
    lines = [
        "## Code Scan",
        "",
        f"Files scanned: `{scan_result.get('files_scanned', 0)}`",
        "",
        f"- Providers/tooling: {_list_or_none(summary.get('providers', []))}",
        f"- Model references: {_list_or_none(summary.get('models', []), code=True)}",
        f"- API key env vars: {_list_or_none(summary.get('api_keys', []), code=True)}",
        f"- AI-ish base URLs: {_list_or_none(summary.get('base_urls', []), code=True)}",
        f"- Prompt-like lines: `{summary.get('prompt_like_lines', 0)}`",
    ]

    for title, key, label in [
        ("Provider Hits", "provider_hits", "label"),
        ("Model Hits", "model_hits", "model"),
        ("Possible Prompts", "prompt_hits", "snippet"),
    ]:
        hits = scan_result.get(key, [])[:10]
        if not hits:
            continue
        lines.extend(["", f"### {title}", ""])
        for hit in hits:
            value = hit.get(label, hit.get("snippet", ""))
            lines.append(
                f"- `{hit.get('file')}:{hit.get('line')}` - {_cell(str(value))}"
            )
    return "\n".join(lines)


def render_portability_section(portability: dict[str, Any]) -> str:
    lines = [
        "## Portability Score",
        "",
        f"Score: **{portability['score']}/100 ({portability['grade']})**",
        "",
        "| Dimension | Score |",
        "| --- | ---: |",
    ]
    for name, score in portability.get("dimensions", {}).items():
        lines.append(f"| {name.replace('_', ' ').title()} | {score}/100 |")

    lines.extend(["", "### Findings", ""])
    for finding in portability.get("findings", []):
        lines.append(f"- {finding}")

    lines.extend(["", "### Recommendations", ""])
    for recommendation in portability.get("recommendations", []):
        lines.append(f"- {recommendation}")
    return "\n".join(lines)


def _money(value: float | None, currency: str) -> str:
    if value is None:
        return "Unknown"
    symbol = "$" if currency.upper() == "USD" else f"{currency} "
    return f"{symbol}{value:,.2f}"


def _cell(value: str) -> str:
    return value.replace("|", "\\|")


def _list_or_none(values: list[str], code: bool = False) -> str:
    if not values:
        return "`none detected`"
    if code:
        return ", ".join(f"`{_cell(str(value))}`" for value in values)
    return ", ".join(_cell(str(value)) for value in values)
