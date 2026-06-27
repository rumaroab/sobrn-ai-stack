from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .estimate import estimate_assumptions, load_assumptions
from .portability import score_portability
from .pricing import DEFAULT_PRICING_PATH, load_catalog
from .report import render_portability_section, render_report, render_scan_section
from .scan import scan_path
from .utils import write_text


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (OSError, ValueError) as exc:
        print(f"sobrn: {exc}", file=sys.stderr)
        return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sobrn",
        description="Local pre-flight AI pricing and portability checker.",
    )
    parser.add_argument("--version", action="version", version="sobrn 0.1.0")
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser("check", help="Estimate cost, scan code, and write a Markdown report.")
    add_common_paths(check)
    check.add_argument("--output", "-o", type=Path, default=Path("reports/pricing-report.md"))
    check.set_defaults(func=run_check)

    estimate = subparsers.add_parser("estimate", help="Estimate configured model costs.")
    estimate.add_argument("--config", "-c", type=Path, default=Path("sobrn.yml"))
    estimate.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    estimate.add_argument("--output", "-o", type=Path)
    estimate.set_defaults(func=run_estimate)

    scan = subparsers.add_parser("scan", help="Scan code for AI dependencies and prompt/model references.")
    scan.add_argument("--path", "-p", type=Path, default=Path("."))
    scan.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    scan.add_argument("--output", "-o", type=Path)
    scan.set_defaults(func=run_scan)

    portability = subparsers.add_parser("portability", help="Scan code and print the portability score.")
    portability.add_argument("--path", "-p", type=Path, default=Path("."))
    portability.add_argument("--config", "-c", type=Path)
    portability.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)
    portability.add_argument("--output", "-o", type=Path)
    portability.set_defaults(func=run_portability)

    return parser


def add_common_paths(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", "-c", type=Path, default=Path("sobrn.yml"))
    parser.add_argument("--path", "-p", type=Path, default=Path("."))
    parser.add_argument("--pricing", type=Path, default=DEFAULT_PRICING_PATH)


def run_check(args: argparse.Namespace) -> int:
    assumptions = load_assumptions(args.config)
    catalog = load_catalog(args.pricing)
    estimates = estimate_assumptions(assumptions, catalog)
    scan_result = scan_path(args.path, args.pricing)
    portability = score_portability(scan_result, catalog, assumptions)
    project = assumptions.get("project", {}) if isinstance(assumptions.get("project"), dict) else {}
    project_name = str(project.get("name", "SOBRN"))
    markdown = render_report(
        project_name=project_name,
        config_path=args.config.as_posix(),
        pricing_catalog=catalog,
        estimates=estimates,
        scan_result=scan_result,
        portability=portability,
    )
    write_or_print(args.output, markdown)
    if args.output:
        print(f"Wrote {args.output}")
    return 0


def run_estimate(args: argparse.Namespace) -> int:
    assumptions = load_assumptions(args.config)
    catalog = load_catalog(args.pricing)
    estimates = estimate_assumptions(assumptions, catalog)
    project = assumptions.get("project", {}) if isinstance(assumptions.get("project"), dict) else {}
    markdown = render_report(
        project_name=str(project.get("name", "SOBRN")),
        config_path=args.config.as_posix(),
        pricing_catalog=catalog,
        estimates=estimates,
    )
    write_or_print(args.output, markdown)
    return 0


def run_scan(args: argparse.Namespace) -> int:
    result = scan_path(args.path, args.pricing)
    markdown = render_scan_section(result) + "\n"
    write_or_print(args.output, markdown)
    return 0


def run_portability(args: argparse.Namespace) -> int:
    catalog = load_catalog(args.pricing)
    assumptions = load_assumptions(args.config) if args.config else None
    scan_result = scan_path(args.path, args.pricing)
    score = score_portability(scan_result, catalog, assumptions)
    markdown = render_portability_section(score) + "\n"
    write_or_print(args.output, markdown)
    return 0


def write_or_print(path: Path | None, content: str) -> None:
    if path:
        write_text(path, content)
    else:
        print(content)
