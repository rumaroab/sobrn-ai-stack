from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .utils import read_text, repo_root


DEFAULT_PRICING_PATH = repo_root() / "pricing" / "models.json"


@dataclass(frozen=True)
class ModelPrice:
    id: str
    provider: str
    display_name: str
    input_per_1m: float
    output_per_1m: float
    currency: str = "USD"
    context_window: int | None = None
    open_weight: bool = False
    local: bool = False
    openai_compatible: bool = False
    notes: str = ""


def load_catalog(path: Path | None = None) -> dict[str, Any]:
    catalog_path = path or DEFAULT_PRICING_PATH
    data = json.loads(read_text(catalog_path))
    if "models" not in data or not isinstance(data["models"], list):
        raise ValueError(f"{catalog_path} must contain a 'models' list")
    return data


def model_prices(catalog: dict[str, Any]) -> dict[str, ModelPrice]:
    prices: dict[str, ModelPrice] = {}
    for item in catalog.get("models", []):
        model = ModelPrice(
            id=str(item["id"]),
            provider=str(item.get("provider", "unknown")),
            display_name=str(item.get("display_name", item["id"])),
            input_per_1m=float(item.get("input_per_1m", 0)),
            output_per_1m=float(item.get("output_per_1m", 0)),
            currency=str(item.get("currency", "USD")),
            context_window=item.get("context_window"),
            open_weight=bool(item.get("open_weight", False)),
            local=bool(item.get("local", False)),
            openai_compatible=bool(item.get("openai_compatible", False)),
            notes=str(item.get("notes", "")),
        )
        prices[model.id] = model
    return prices


def catalog_model_ids(catalog: dict[str, Any]) -> set[str]:
    return set(model_prices(catalog))
