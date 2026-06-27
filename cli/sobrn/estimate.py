from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .pricing import model_prices
from .utils import load_yaml


@dataclass(frozen=True)
class Estimate:
    name: str
    model: str
    provider: str
    requests_per_month: int
    input_tokens_per_request: int
    output_tokens_per_request: int
    monthly_input_tokens: int
    monthly_output_tokens: int
    input_cost: float | None
    output_cost: float | None
    total_cost: float | None
    currency: str
    notes: str


def load_assumptions(path: Path) -> dict[str, Any]:
    config = load_yaml(path)
    if "scenarios" not in config:
        raise ValueError("sobrn.yml must define at least one scenario")
    if not isinstance(config["scenarios"], list):
        raise ValueError("sobrn.yml 'scenarios' must be a list")
    return config


def estimate_assumptions(config: dict[str, Any], catalog: dict[str, Any]) -> list[Estimate]:
    usage_defaults = config.get("usage", {}) or {}
    if not isinstance(usage_defaults, dict):
        raise ValueError("sobrn.yml 'usage' must be a mapping")

    prices = model_prices(catalog)
    estimates: list[Estimate] = []
    for index, scenario in enumerate(config.get("scenarios", []), start=1):
        if not isinstance(scenario, dict):
            raise ValueError("Each scenario must be a mapping")
        model_id = str(scenario.get("model", "")).strip()
        if not model_id:
            raise ValueError(f"Scenario {index} is missing 'model'")

        name = str(scenario.get("name") or model_id)
        requests = _int_setting(scenario, usage_defaults, "requests_per_month")
        input_tokens = _int_setting(scenario, usage_defaults, "input_tokens_per_request")
        output_tokens = _int_setting(scenario, usage_defaults, "output_tokens_per_request")

        monthly_input = requests * input_tokens
        monthly_output = requests * output_tokens
        price = prices.get(model_id)

        if price is None:
            estimates.append(
                Estimate(
                    name=name,
                    model=model_id,
                    provider="unknown",
                    requests_per_month=requests,
                    input_tokens_per_request=input_tokens,
                    output_tokens_per_request=output_tokens,
                    monthly_input_tokens=monthly_input,
                    monthly_output_tokens=monthly_output,
                    input_cost=None,
                    output_cost=None,
                    total_cost=None,
                    currency=str(catalog.get("currency", "USD")),
                    notes="Model not found in local pricing catalog.",
                )
            )
            continue

        input_cost = monthly_input / 1_000_000 * price.input_per_1m
        output_cost = monthly_output / 1_000_000 * price.output_per_1m
        total = input_cost + output_cost
        notes = price.notes
        if price.local:
            notes = (
                notes
                or "Local/open-weight entry models token fees as $0; infrastructure cost is not included."
            )

        estimates.append(
            Estimate(
                name=name,
                model=model_id,
                provider=price.provider,
                requests_per_month=requests,
                input_tokens_per_request=input_tokens,
                output_tokens_per_request=output_tokens,
                monthly_input_tokens=monthly_input,
                monthly_output_tokens=monthly_output,
                input_cost=input_cost,
                output_cost=output_cost,
                total_cost=total,
                currency=price.currency,
                notes=notes,
            )
        )
    return estimates


def _int_setting(
    scenario: dict[str, Any], defaults: dict[str, Any], key: str, fallback: int = 0
) -> int:
    value = scenario.get(key, defaults.get(key, fallback))
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"'{key}' must be an integer") from exc
    if number < 0:
        raise ValueError(f"'{key}' must be zero or greater")
    return number
