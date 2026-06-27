from __future__ import annotations

from pathlib import Path
from typing import Any


IGNORED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".venv",
    "venv",
    "env",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "dist",
    "build",
    ".next",
    ".nuxt",
    "target",
    "vendor",
    ".terraform",
}


TEXT_EXTENSIONS = {
    ".cjs",
    ".cs",
    ".env",
    ".go",
    ".java",
    ".js",
    ".json",
    ".jsx",
    ".kt",
    ".md",
    ".mjs",
    ".php",
    ".py",
    ".rb",
    ".rs",
    ".scala",
    ".sh",
    ".swift",
    ".toml",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def iter_project_files(root: Path, max_bytes: int = 750_000) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if any(part in IGNORED_DIRS for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            if path.stat().st_size > max_bytes:
                continue
        except OSError:
            continue
        files.append(path)
    return sorted(files)


def load_yaml(path: Path) -> dict[str, Any]:
    text = read_text(path)
    try:
        import yaml  # type: ignore
    except ImportError:
        parsed = _parse_sobrn_yaml(text, path)
    else:
        loaded = yaml.safe_load(text) or {}
        if not isinstance(loaded, dict):
            raise ValueError(f"{path} must contain a YAML mapping at the top level")
        parsed = loaded
    if not isinstance(parsed, dict):
        raise ValueError(f"{path} must contain a YAML mapping at the top level")
    return parsed


def _parse_sobrn_yaml(text: str, path: Path) -> dict[str, Any]:
    """Parse the documented sobrn.yml subset when PyYAML is unavailable."""

    data: dict[str, Any] = {}
    section: str | None = None
    current_scenario: dict[str, Any] | None = None

    for raw in text.splitlines():
        line = raw.split("#", 1)[0].rstrip()
        if not line.strip():
            continue

        indent = len(line) - len(line.lstrip(" "))
        content = line.strip()

        if indent == 0:
            key, value = _split_key_value(content)
            section = key
            current_scenario = None
            if value:
                data[key] = _parse_scalar(value)
            else:
                data[key] = [] if key == "scenarios" else {}
            continue

        if section == "scenarios":
            scenarios = data.setdefault("scenarios", [])
            if not isinstance(scenarios, list):
                raise ValueError(f"{path} 'scenarios' must be a list")
            if content.startswith("- "):
                current_scenario = {}
                scenarios.append(current_scenario)
                inline = content[2:].strip()
                if inline:
                    key, value = _split_key_value(inline)
                    current_scenario[key] = _parse_scalar(value)
            elif current_scenario is not None:
                key, value = _split_key_value(content)
                current_scenario[key] = _parse_scalar(value)
            else:
                raise ValueError(f"Unexpected line in {path}: {raw}")
            continue

        if section and isinstance(data.get(section), dict):
            key, value = _split_key_value(content)
            data[section][key] = _parse_scalar(value)
            continue

        raise ValueError(f"Unexpected line in {path}: {raw}")

    return data


def _split_key_value(content: str) -> tuple[str, str]:
    if ":" not in content:
        raise ValueError(f"Expected 'key: value' YAML line, got: {content}")
    key, value = content.split(":", 1)
    key = key.strip()
    if not key:
        raise ValueError(f"Expected a YAML key, got: {content}")
    return key, value.strip()


def _parse_scalar(value: str) -> Any:
    if value == "":
        return ""
    lowered = value.lower()
    if lowered in {"true", "false"}:
        return lowered == "true"
    if lowered in {"null", "none", "~"}:
        return None
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def relpath(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
