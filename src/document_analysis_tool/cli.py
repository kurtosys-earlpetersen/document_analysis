"""CLI for document analysis: compliance + accessibility."""

from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from .ingestion import ingest, SUPPORTED_EXTENSIONS
from .compliance import run_compliance
from .accessibility import run_accessibility
from .metrics import build_run, store_run, format_summary

console = Console()


@click.group()
@click.version_option(version="0.1.0", prog_name="document-analysis-tool")
def main() -> None:
    """Analyse asset manager marketing documents for compliance and accessibility."""


@main.command("analyze")
@click.argument("path", type=click.Path(exists=True, path_type=Path))
@click.option("--jurisdiction", "-j", default="EU", help="Jurisdiction (EU, UK, US, etc.)")
@click.option("--output", "-o", type=click.Path(path_type=Path), help="Output file (JSON or JSONL)")
@click.option("-v", "--verbose", is_flag=True, help="Verbose output")
def analyze(path: Path, jurisdiction: str, output: Path | None, verbose: bool) -> None:
    """Analyse a document or directory of documents."""
    paths: list[Path] = []
    if path.is_file():
        paths = [path]
    elif path.is_dir():
        for ext in SUPPORTED_EXTENSIONS:
            paths.extend(path.glob(f"*{ext}"))
        paths = sorted(paths)
    else:
        console.print("[red]Path must be a file or directory.[/red]")
        raise SystemExit(1)

    if not paths:
        console.print("[yellow]No supported documents found (PDF or DOCX).[/yellow]")
        raise SystemExit(0)

    runs: list = []
    for i, doc_path in enumerate(paths):
        if verbose:
            console.print(f"\n[bold]Analysing ({i+1}/{len(paths)}):[/bold] {doc_path.name}")

        doc = ingest(doc_path)
        if doc is None:
            console.print(f"[red]Skip (unsupported): {doc_path.name}[/red]")
            continue

        if verbose:
            console.print(f"  Extracted {len(doc.raw_text)} chars, {len(doc.blocks)} blocks")

        compliance_result = run_compliance(doc, jurisdiction)
        if compliance_result.get("error"):
            console.print(f"  [red]Compliance: {compliance_result['error']}[/red]")
        elif verbose:
            console.print(f"  Compliance: {compliance_result.get('compliance_score', 0):.1f}%")

        accessibility_result = run_accessibility(doc)
        if verbose:
            console.print(f"  Accessibility: {accessibility_result.get('accessibility_score', 0):.1f}%")

        run = build_run(doc_path, jurisdiction, compliance_result, accessibility_result)
        runs.append(run)
        console.print(format_summary(run))

        if compliance_result.get("results"):
            t = Table(title="Compliance rules")
            t.add_column("Rule", style="cyan")
            t.add_column("Passed", style="green")
            t.add_column("Message")
            for r in compliance_result["results"]:
                t.add_row(
                    r.get("name") or r.get("rule_id", ""),
                    "Yes" if r.get("passed") else "No",
                    (r.get("message") or "")[:60],
                )
            console.print(t)

        if accessibility_result.get("results"):
            t = Table(title="Accessibility checks")
            t.add_column("Check", style="cyan")
            t.add_column("Passed", style="green")
            t.add_column("Message")
            for r in accessibility_result["results"]:
                t.add_row(
                    r.get("check", ""),
                    "Yes" if r.get("passed") else "No",
                    (r.get("message") or "")[:60],
                )
            console.print(t)

        if output:
            out_path = Path(output)
            if out_path.suffix.lower() == ".jsonl":
                store_run(out_path, run)
            elif len(paths) == 1:
                store_run(out_path, run)
    if output and runs:
        if len(runs) > 1 and Path(output).suffix.lower() == ".json":
            import json
            from .metrics.reporting import asdict
            out_path = Path(output)
            out_path.parent.mkdir(parents=True, exist_ok=True)
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump([asdict(r) for r in runs], f, indent=2, default=str)
        console.print(f"\n[dim]Results written to {output}[/dim]")


if __name__ == "__main__":
    main()
