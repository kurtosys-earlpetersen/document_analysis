# Document Analysis Tool

Analyse asset manager marketing documents for **compliance**, **legislation adherence**, and **accessibility** across jurisdictions.

## Features

- **Multi-format ingestion**: PDF, Word (DOCX)
- **Compliance engine**: Configurable rules per jurisdiction (EU PRIIPs/UCITS, UK FCA, US SEC, etc.)
- **Accessibility & assistive tech**: Structure checks, alt text, reading order, WCAG-oriented metrics
- **Metrics & reporting**: Pass/fail scores, findings, trends (SQLite storage)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
pip install -e .   # optional: install package so you can run from any directory
```

## K2-9227 Visualisation

A standalone HTML UI visualises the **K2-9227: Design & Product Consultant Responsibilities (2026)** content: process flows, ownership/RACI tables, overlap areas, principles, and checklist. Open in any browser:

```bash
open k2-9227-visual.html   # macOS
# or double-click k2-9227-visual.html, or open from file manager
```

No server required. File: `k2-9227-visual.html`.

## Preview the UI

A Streamlit web UI is included. From the project root:

```bash
pip install streamlit   # if not already installed
streamlit run app.py
```

Then open the URL shown (usually http://localhost:8501), upload a PDF or DOCX, choose a jurisdiction, and view compliance and accessibility results.

## CLI usage

Run from the project root. Either set the Python path or install in editable mode:

```bash
# From project root, with editable install:
pip install -e .
python -m document_analysis_tool.cli analyze path/to/document.pdf --jurisdiction EU

# Or without installing (from project root):
PYTHONPATH=src python -m document_analysis_tool.cli analyze path/to/document.pdf --jurisdiction EU
```

Analyse a directory (use `--output report.jsonl` to append each result):

```bash
python -m document_analysis_tool.cli analyze path/to/folder/ --jurisdiction UK --output report.jsonl
```

Run with verbose output:

```bash
python -m document_analysis_tool.cli analyze doc.pdf --jurisdiction EU -v
```

## Project structure

```
src/document_analysis_tool/
  ingestion/     # PDF, DOCX parsers
  extraction/    # Text, structure, metadata
  compliance/    # Rules engine, jurisdiction configs
  accessibility/ # WCAG-style and assistive-tech checks
  metrics/       # Storage, scoring, reporting
  cli.py         # Entrypoint
config/          # Jurisdiction rule definitions (YAML)
```

## Document Benchmarking Project (requirements context)

The PDF **`Document Benchmarking Project.pdf`** in the project root defines the benchmarking methodology (taxonomy, peer set, evaluation matrix, BSC, accessibility standards, regulations). For Cursor and collaborators:

- **Human-readable summary:** [`docs/DOCUMENT_BENCHMARKING_PROJECT.md`](docs/DOCUMENT_BENCHMARKING_PROJECT.md)
- **Machine-readable dimensions (for future scoring):** [`config/benchmarking_framework.yaml`](config/benchmarking_framework.yaml)

Point the assistant at those files (or `@` them in chat) instead of a ChatGPT link.

## Configuration

Edit `config/jurisdictions/` to add or change compliance rules per region and document type. See `config/jurisdictions/eu_prriips.yaml` for the schema.

## License

Internal use / Kurtosys.
