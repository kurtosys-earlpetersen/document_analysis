# Document analysis tool for marketing compliance
_Exported on 24/03/2026 at 8:14:10 GMT+2 from Cursor (2.6.21)_

---

**User**

How can I go about creating a document analysis tool. It would pertain to all marketing documents distributed by asset managers across all jurisdiction, metrics for compliance and adherance to document content legislation as well as focusing on accessibility and assistive technology.

---

**Cursor**

Exploring your workspace to see what's already present, then outlining how we can build the document analysis tool.


Here’s a structured way to approach building your document analysis tool for asset manager marketing materials.

---

## 1. **Define scope and inputs**

- **Document types**: Fact sheets, KIIDs/KIDs, prospectuses, fund summaries, presentations, brochures, website content, etc.
- **Formats**: PDF, Word, HTML, possibly PowerPoint and Excel.
- **Jurisdictions**: EU (MiFID II, PRIIPs, UCITS, SFDR, etc.), UK (FCA), US (SEC), other regions you care about.
- **Languages**: If you need multi‑jurisdiction, decide which languages to support (and whether you analyse in original language or after translation).

---

## 2. **Core pillars of the tool**

| Pillar | Purpose |
|--------|--------|
| **Legislation & compliance** | Map rules to checks; flag non‑compliance and missing/incorrect content. |
| **Metrics & reporting** | Scores, pass/fail, trends, exceptions, audit trail. |
| **Accessibility** | WCAG, PDF/UA, readable structure, colour contrast, etc. |
| **Assistive technology** | Ensure content works with screen readers, keyboard nav, reflow, etc. |

---

## 3. **Legislation and rules (by pillar)**

**A. Document content / disclosure rules (examples)**  
- **EU**: PRIIPs KID, UCITS KIID, SFDR (sustainability), MiFID II suitability and disclosure.  
- **UK**: FCA COBS, PRIIPs UK, Key Information Documents.  
- **US**: SEC Rule 482 (advertising), prospectus rules, Form N‑1A, etc.  
- **Other**: Local equivalents (e.g. HK, SG, AU) if you need them.

**B. Accessibility**  
- **WCAG 2.1 (2.2)** for web/digital.  
- **PDF/UA (ISO 14289)** for PDFs.  
- **EN 301 549** (EU accessibility) where relevant.  
- Jurisdiction‑specific laws (e.g. EAA, ADA, UK EA 2010).

You’ll need a **rules engine** (or config) that says: “For document type X in jurisdiction Y, require fields Z and checks W.”

---

## 4. **High‑level architecture**

```
┌─────────────────────────────────────────────────────────────────┐
│                     Document ingestion                           │
│  (upload / API / batch: PDF, DOCX, HTML, etc.)                   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                     Extraction & parsing                         │
│  • Text + structure (headings, lists, tables)                   │
│  • Metadata (language, jurisdiction if tagged)                  │
│  • Images, charts (for alt text / accessibility)                │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                     Analysis engines                             │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────────┐ │
│  │ Compliance   │ │ Accessibility│ │ Assistive tech readiness │ │
│  │ (rules per   │ │ (WCAG/PDF-UA)│ │ (structure, semantics,   │ │
│  │  jurisdiction)│ │              │ │  reading order)          │ │
│  └──────────────┘ └──────────────┘ └──────────────────────────┘ │
└─────────────────────────────┬───────────────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────────────┐
│                     Metrics & reporting                          │
│  Scores, pass/fail, findings list, trends, export (Excel/API)   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 5. **Compliance and content checks**

- **Presence checks**: Required sections/fields exist (e.g. “Risk section”, “Costs”, “Performance”).  
- **Content checks**: Warnings/disclaimers present and not stripped; prescribed wording where required.  
- **Consistency**: Figures/dates aligned across sections or vs. a source of truth.  
- **Jurisdiction tagging**: Document or fund tagged with jurisdiction so the right rule set is applied.

Implementation options: rule config (YAML/JSON) + scripts, or a proper rules engine (e.g. Drools, or custom in Python/TypeScript). Start with a small set of critical rules per jurisdiction and expand.

---

## 6. **Accessibility and assistive technology**

- **PDF**: Tagging, reading order, alt text for images, language, heading hierarchy. Tools: pdfua.org checks, Adobe accessibility checker, or libraries (e.g. PyMuPDF, pdfminer) for structure extraction + custom checks.  
- **Web/HTML**: Semantic HTML, ARIA, heading levels, colour contrast, focus order. Use axe-core, Pa11y, or WAVE in a pipeline.  
- **Word**: Headings, alt text, table headers; can be automated via python-docx or similar.

Output: per-document accessibility score and a list of issues (with standard/success criterion and severity).

---

## 7. **Metrics that matter**

- **Compliance**: % of documents passing each rule set; count of breaches by rule and jurisdiction.  
- **Accessibility**: Overall score; counts by WCAG level (A/AA/AAA) or PDF/UA.  
- **Trends**: Pass rate over time; most common failure types.  
- **Assistive tech**: “Screen-reader readiness” score based on structure, alt text, and semantics.

Store results in a DB (e.g. PostgreSQL) and build dashboards (e.g. Grafana, Metabase, or a simple web UI).

---

## 8. **Tech stack suggestions**

- **Language**: Python (good for PDF/Word parsing, NLP, and quick pipelines) or Node/TypeScript if you’re more web‑centric.  
- **Parsing**: PyMuPDF, pdfminer, python-docx, Beautiful Soup / Playwright for HTML.  
- **Accessibility**: axe-core (via axe-core Python or Puppeteer), Pa11y, or WAVE API.  
- **Storage**: SQLite/PostgreSQL for runs, findings, and metrics.  
- **UI**: Optional web app (React/Vue) for upload, job status, and report viewing.

---

## 9. **Practical way to start**

1. **Pick one jurisdiction and one document type** (e.g. EU PRIIPs KID or UK KIID).  
2. **List the exact rules** (required sections, key phrases, structure).  
3. **Build a minimal pipeline**: ingest PDF → extract text/structure → run 5–10 compliance checks + basic accessibility (e.g. headings, alt text).  
4. **Define metrics**: pass/fail per rule, simple compliance and accessibility scores.  
5. **Add more jurisdictions and document types** and refactor into a configurable rules engine.

If you tell me your preferred stack (e.g. Python vs Node) and whether you want to start with **compliance**, **accessibility**, or **both in one prototype**, I can outline a concrete project structure (folders, modules, and example checks) and, if you want, stub a minimal repo in your `Document_analysis_tool` folder.

---

**User**

Not sure about the stack. Do what you feel is best.

---

**Cursor**

Choosing Python for its document-parsing ecosystem, accessibility tooling, and fast iteration. Creating a well-structured project scaffold.


Adding metrics storage and the CLI.


Checking ingestion imports and fixing JSONL handling for batch output:


Collecting runs when analysing multiple documents and output is `.json`, then writing a single JSON array.


Fixing output logic: when multiple documents and output is `.json`, write once at the end; otherwise write or append per run.


Summary of what’s in place:

---

## Stack: **Python 3.11+**

- **Document parsing**: PyMuPDF (PDF), python-docx (DOCX)  
- **Config**: YAML jurisdiction rules  
- **CLI**: Click + Rich  
- **Output**: JSON / JSONL for metrics and reporting  

---

## What’s in the repo

| Area | What’s there |
|------|----------------|
| **Ingestion** | `ingestion/` – PDF and DOCX parsing, extraction of text and structure (headings, paragraphs, tables, images) |
| **Compliance** | `compliance/engine.py` – rule engine that runs jurisdiction-specific rules (required sections, required phrases, min length). Configs under `config/jurisdictions/` for **EU** (PRIIPs-style), **UK** (FCA), **US** (SEC). |
| **Accessibility** | `accessibility/checks.py` – heading presence, heading hierarchy (no level jumps), image alt text, basic structure for assistive tech |
| **Metrics** | `metrics/reporting.py` – `AnalysisRun` dataclass, `store_run()` to JSON/JSONL, `format_summary()` for console |
| **CLI** | `cli.py` – `analyze <path>` with `--jurisdiction`, `--output`, `-v` |

---

## How to run

```bash
cd Document_analysis_tool
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .

# Single file
python -m document_analysis_tool.cli analyze path/to/file.pdf -j EU -v

# Directory, output to JSONL
python -m document_analysis_tool.cli analyze path/to/folder/ -j UK -o report.jsonl
```

Supported jurisdictions: **EU**, **UK**, **US** (add more by adding YAML files under `config/jurisdictions/`).

---

## Possible next steps

- **More rule types** – e.g. forbidden phrases, date checks, consistency checks across sections.  
- **PDF/UA** – deeper PDF tagging/reading-order checks (e.g. with `pdfminer` or a dedicated checker).  
- **HTML** – add an HTML parser and plug in axe-core for WCAG.  
- **Database** – replace or complement JSONL with SQLite/PostgreSQL for runs and dashboards.  
- **Web UI** – upload + run + view reports (e.g. FastAPI + React).

The README in the project root has full usage and structure; extend the YAML rule files to match your real compliance and accessibility requirements.

---

**User**

How can I preview the UI?

---

**Cursor**

Adding a simple web UI so we can preview the tool in the browser. Using Streamlit for a quick, runnable preview.


Using a cross-platform temp directory for the upload:


Here’s how to **preview the UI**:

---

### 1. From the project root, install and run Streamlit

```bash
cd /Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool
source .venv/bin/activate   # if you use a venv
pip install streamlit
streamlit run app.py
```

### 2. Open the app in your browser

Streamlit will print something like:

```text
  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

Open **http://localhost:8501** in your browser.

### 3. Use the UI

- **Sidebar**: choose **Jurisdiction** (EU, UK, US).
- **Main area**: use **“Upload a PDF or Word document”** and pick a `.pdf` or `.docx`.
- After upload, the app runs the same compliance and accessibility logic as the CLI and shows:
  - Compliance and accessibility scores
  - Per-rule pass/fail for compliance
  - Per-check pass/fail for accessibility
  - An expandable raw summary

The README now has a short **“Preview the UI”** section with the same run instructions.

---

**User**

Install and run Streamlit

---

**Cursor**

Using `python -m pip` because `pip` wasn't found:


Streamlit is being installed and the app is starting in the background. The exact server output (including the URL) may not show in this environment.

**Do this on your machine:**

1. **Open a terminal** in the project folder:
   ```bash
   cd /Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool
   ```

2. **Activate your venv** (if you use one):
   ```bash
   source .venv/bin/activate
   ```

3. **Install and run:**
   ```bash
   python3 -m pip install streamlit
   python3 -m streamlit run app.py
   ```

4. **In the browser:** open **http://localhost:8501** (Streamlit will also print this URL in the terminal).

If you already have a venv and want to use it, run the same commands from the project directory with that venv activated; the install and run were done with `python3 -m pip` and `python3 -m streamlit` because `pip` wasn’t on your PATH.

Checking the project environment and starting Streamlit so the app is reachable:


Starting Streamlit from the project directory:


Running the app in the foreground to capture any startup error:


Installing Streamlit, then starting the app:


Streamlit isn’t installed in the environment used here, and installing it hit a network timeout. So you’ll need to run the app **on your machine** in a terminal where you have internet and your usual Python.

**In your own terminal (with internet):**

1. **Go to the project folder**
   ```bash
   cd "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool"
   ```

2. **Use a virtual environment (recommended)**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Start Streamlit**
   ```bash
   streamlit run app.py
   ```
   Or:
   ```bash
   python -m streamlit run app.py
   ```

4. **Open the app**  
   When you see something like `Local URL: http://localhost:8501`, open **http://localhost:8501** in your browser.

Adding a small run script so you can use one command after the venv is set up:


**Summary:** The connection failed because Streamlit wasn’t running. I can’t install or run it from this environment (no network to PyPI), so you need to start it locally.

**One-time setup in your terminal (with internet):**
```bash
cd "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Then start the UI:**
```bash
./run_ui.sh
```
or:
```bash
streamlit run app.py
```

When Streamlit prints `Local URL: http://localhost:8501`, open that URL in your browser. The “Connection refused” error will stop once Streamlit is running in that terminal.

---

**User**

open the browser

---

**Cursor**

Your default browser should have opened to **http://localhost:8501**.

If you see “Connection refused,” start the Streamlit app first in a terminal:

```bash
cd "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool"
source .venv/bin/activate
streamlit run app.py
```

Then refresh the browser tab.

---

**User**

Error Code: -102 URL: http://localhost:8501/

---

**Cursor**

Starting the Streamlit server so something is listening on port 8501:


Opening the app in your browser:


The Streamlit app is running and your browser should have opened to **http://localhost:8501**.

You should see the Document Analysis Tool: upload a PDF or Word file, pick a jurisdiction in the sidebar, and view the compliance and accessibility results.

**Note:** The server is running in the background. To stop it later, either close that terminal or run:
```bash
pkill -f "streamlit run app.py"
```
To start it again next time, from the project folder run:
```bash
source .venv/bin/activate && streamlit run app.py
```
or use `./run_ui.sh`.

Installing PyMuPDF — the `fitz` module is provided by the `pymupdf` package (import name `fitz`). Installing it in the project environment:


Installing the full project dependencies into the venv so Streamlit uses them:


PyMuPDF is installed and `import fitz` works. Restart Streamlit so it picks up the new package. Relaxing the requirements so the full install succeeds next time:


Restarting Streamlit so the app runs with the updated packages:


Here’s what was done:

1. **Installed PyMuPDF** – The `fitz` module comes from the `pymupdf` package; it’s now installed in your Python environment.

2. **Adjusted `requirements.txt`** – The version constraint for `axe-selenium-python` was set to a version that exists on PyPI so `pip install -r requirements.txt` can complete.

3. **Restarted Streamlit** – The app was restarted so it runs with the environment that has `pymupdf`.

Refresh **http://localhost:8501** and upload a PDF again. The “No module named 'fitz'” error should be gone.

If you use a virtualenv (e.g. `.venv`), install dependencies there and run Streamlit from the same env:

```bash
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

**User**

Still getting the error in the browser:

ModuleNotFoundError: No module named 'docx'
Traceback:
File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Cli
from document_analysis_tool. ingestion import ingest
File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Cli
from . docx_parser import parse_docx
File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Cli
from docx import Document
Copy. Ask Google Ask ChatGPT

---

**Cursor**

Installing `python-docx` (provides the `docx` import) and ensuring all app dependencies are installed:


Restarting Streamlit so it uses the Python that has `docx`:


Updating the run script so we always use an environment with all dependencies installed:


Here’s what’s in place:

1. **Installed `python-docx`** (the package that provides the `docx` import) in the same Python environment we’ve been using.
2. **Restarted Streamlit** so it runs with that environment.
3. **Updated `run_ui.sh`** so it checks for `docx`, `fitz`, and `streamlit` before starting and tells you to run `pip install -r requirements.txt` if any are missing.

**Refresh http://localhost:8501** and try uploading a document again.

---

**If the error is still there**, Streamlit is probably running under a different Python (e.g. a venv or another terminal). Do this in **the same terminal/environment you use to start Streamlit**:

```bash
cd "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool"
pip install -r requirements.txt
# Then start the app (e.g.):
python3 -m streamlit run app.py
```

Or with a venv:

```bash
source .venv/bin/activate
pip install -r requirements.txt
./run_ui.sh
```

Using one environment and installing everything there with `pip install -r requirements.txt` keeps `fitz` (PyMuPDF), `docx` (python-docx), and Streamlit in sync.

---

**User**

Now getting this error

---

**Cursor**

I don’t see the actual error message or a screenshot.

Please paste the full error text (including the traceback), or attach a screenshot of the error. Then I can tell you exactly what’s wrong and how to fix it.

---

**User**

AttributeError: module 'streamlit' has no attribute 'pre'
Traceback:
File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool/app.py", line 93, in <module>
    st.pre(format_summary(run))
    ^^^^^^

---

**Cursor**

Replacing nonexistent `st.pre()` with `st.code()` for the raw summary.


Updated the app: Streamlit doesn’t provide `st.pre()`, so the raw summary is now shown with **`st.code()`**, which is the right way to display preformatted text.

Refresh the page and expand “Raw summary” again; that error should be gone.

---

**User**

How can I view this document analysis tool? If I shared a ChatGPT chat with you that contains the context for creating this tool. 

How would it be possible to share that with you?

---

**Cursor**

## How to view / use the document analysis tool

You have two main ways:

### 1. **Web UI (Streamlit)**  
In a terminal, from the project folder:

```bash
cd "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool"
source .venv/bin/activate   # if you use a venv
pip install -r requirements.txt   # once, if needed
streamlit run app.py
```

Then open **http://localhost:8501** in your browser, upload a PDF or DOCX, pick a jurisdiction.

### 2. **CLI**  
Same fold

---

**User**

If I shared a ChatGPT chat with you that contains the context for creating this tool. 

How would it be possible to share that with you?

---

**Cursor**

There’s no automatic “import ChatGPT into Cursor” link. You can still give me that context in a few practical ways:

### 1. **Paste into this chat**  
Copy the parts that matter (requirements, decisions, examples) and paste them here. Short, focused excerpts work best; you can say “full chat is long—here are the key bits.”

### 2. **Put it in a file in the project** (best for ongoing work)  
Create something like `docs/chatgpt-context.md` (or `CONTEXT.md`) in your repo, paste the relevant conversation or a summary, and save it. In Cursor you can `@`-mention that file or ask me to read it—I can use the file as stable context across sessions.

### 3. **ChatGPT “share” link**  
If ChatGPT gives you a share URL, you can paste the URL here. I may not always be able to open external pages reliably; if something doesn’t load, copy the text from that shared view into a file or message instead.

### 4. **Summarize instead of dumping everything**  
A short bullet list (goals, jurisdictions, rule types, UI expectations, stack preferences) often works as well as a long transcript.

**Recommendation:** For this document analysis tool, add a **`docs/requirements.md`** or **`CONTEXT.md`** with goals + constraints from ChatGPT, then keep the repo as the single source of truth so any assistant in Cursor can read it.

---

**User**

https://chatgpt.com/g/g-p-690f45c4d4ac8191bce558905ee48611-document-comparison-tool/project 

---

**Cursor**

Checking whether that page is publicly readable:



I opened that link, but **ChatGPT only shows a login / “Get started” page** to anything that isn’t logged in as you. So I **can’t see your project instructions, chats, or files** from that URL.

**What you can do instead:**

1. **Copy the important parts** from the ChatGPT project (instructions, custom instructions, pasted requirements, key messages) and **paste them here**, or  
2. **Save them in your repo** as e.g. `docs/chatgpt-project-context.md`, then tell me to read that file (or `@` it in Cursor).

If the project has **“Project instructions”** or **“Files”**, those are especially useful to export into that markdown file so this tool stays aligned with what you defined in ChatGPT.

**Note:** Your link points to a **document comparison** GPT/project; your local folder is a **document analysis** tool (compliance + accessibility). If you want them to match, paste or file the comparison-tool spec and we can align features or naming.

---

**User**

@Document Benchmarking Project.pdf Use this instead

---

**Cursor**

Extracting text from the PDF we found in your project folder:



Saving the PDF as project documentation and adding a benchmarking config so we can align the tool with the framework.



Here’s what we did with **`Document Benchmarking Project.pdf`** (it’s in your project root):

### 1. **`docs/DOCUMENT_BENCHMARKING_PROJECT.md`**
Markdown version of the PDF: taxonomy, peer group, benchmarking matrix (clarity → usability), BSC mapping, accessibility standards, regulations, methodology, and recommendations. Use this as the **written spec** for the tool.

### 2. **`config/benchmarking_framework.yaml`**
Structured copy of the **six evaluation dimensions** (1–5 scale), BSC perspectives, scoring labels, and taxonomy category IDs—ready to wire into scoring/reporting later.

### 3. **`README.md`**
New section that points to the PDF, the markdown doc, and the YAML so anyone (including Cursor) knows where the “official” context lives.

---

**How to use it with me in Cursor**

- Type **`@DOCUMENT_BENCHMARKING_PROJECT.md`** or **`@benchmarking_framework.yaml`** in chat, or  
- Say “follow `docs/DOCUMENT_BENCHMARKING_PROJECT.md`” — I can read those files from the repo.

That replaces the ChatGPT link: the PDF stays the source; the markdown + YAML are what we can reliably read and extend in code.

If you want next steps, we can map the six dimensions to **explicit 1–5 scores** in the Streamlit UI (today we only approximate some of that via compliance + accessibility checks).

---

**User**

ollow docs/DOCUMENT_BENCHMARKING_PROJECT.md and use the requirements and specifications to build a new UI for the document analysis tool.

---

**Cursor**

Now building the full new UI.

Now installing plotly and restarting Streamlit.

Plotly installed. Now restarting Streamlit:

The new UI is running at **http://localhost:8501** and your browser should have opened it. Here's what was built, directly from the benchmarking project spec:

---

### New modules created

**`src/document_analysis_tool/benchmarking/scoring.py`** — Scores documents across the **six evaluation dimensions** (1–5 scale):

| Dimension | How it's scored |
|-----------|----------------|
| **Clarity** | Average sentence length + long-word ratio (plain language proxy) |
| **Transparency** | Presence of 15 disclosure keywords (risk, fees, disclaimer, etc.) |
| **Design** | Heading count, block type variety, heading level depth |
| **Accessibility** | Maps existing accessibility check results to 1–5 |
| **Compliance** | Maps existing compliance check results to 1–5 |
| **Usability** | Navigable headings, total blocks, table count |

**`src/document_analysis_tool/benchmarking/taxonomy.py`** — Detects which of the **8 taxonomy categories** (Fund Overview, Performance, Portfolio, Fees, Risk, ESG, Disclosures, Operational) are present via keyword matching.

---

### New UI (`app.py`) — 7 tabs

| Tab | Content |
|-----|---------|
| **Scorecard** | Six colour-coded dimension cards + overall score + document stats |
| **Radar Chart** | Plotly radar chart of all 6 dimensions vs. "adequate" baseline |
| **Taxonomy** | 8-category coverage with progress bars and matched keywords |
| **Compliance** | Jurisdiction rules with severity icons and pass/fail |
| **Accessibility** | WCAG/PDF-UA checks, standards reference, assistive tech compatibility |
| **Balanced Scorecard** | Four BSC perspectives (Customer, Internal, Learning, Financial) mapped to dimensions |
| **Insights** | Strengths, weaknesses, recommendations, and industry insights |

The sidebar includes jurisdiction selection, document type picker, and the peer benchmark set (BlackRock, Vanguard, etc.) from the project spec.

---

**User**

Looking good, but I'm going to need that UI to look a whole lot better.

Determine if a document needs ESG content based on the type of sectors and holdings.

Here is more context:

Peer group creation guide.

Excellent — I’ll structure this so it works operationally inside a **Balanced Scorecard (BSC)** framework and can also support **weekly resource utilisation tracking**.

Below is:

1. **Balanced Scorecard structure tailored to investor documentation**
2. **Peer benchmarking matrix template (ready to operationalise)**
3. **Scoring model (1–5 maturity scale)**
4. **How to link this to weekly resource utilisation tracking**

---

# 1️⃣ Balanced Scorecard Framework for Document Benchmarking

We’ll map document quality and competitiveness across the four classic BSC perspectives:

| BSC Perspective         | Document Benchmarking Focus                     | Strategic Question                                        |
| ----------------------- | ----------------------------------------------- | --------------------------------------------------------- |
| **Financial**           | Cost efficiency, scalability, automation, reuse | Are we producing documents competitively and efficiently? |
| **Customer / Investor** | Clarity, usability, accessibility, segmentation | Do our documents meet investor needs better than peers?   |
| **Internal Process**    | Governance, compliance workflow, update cadence | How efficient and controlled is our document lifecycle?   |
| **Learning & Growth**   | Innovation, digitalisation, ESG evolution       | Are we future-proofing our documentation capability?      |

---

# 2️⃣ Peer Document Benchmarking Matrix Template

You can use this as:

* Excel scoring grid
* Airtable/Notion database
* Structured internal audit tool

---

## A. MASTER MATRIX STRUCTURE

### Columns (Horizontal)

| Peer | BlackRock | Vanguard | Fidelity | SSGA | JPM AM | Amundi | PIMCO | Capital Group | Schroders | T. Rowe |
| ---- | --------- | -------- | -------- | ---- | ------ | ------ | ----- | ------------- | --------- | ------- |

---

### Rows (Vertical – BSC Structured Criteria)

---

# 🔵 I. FINANCIAL PERSPECTIVE

### 1. Production Efficiency

* Modular content architecture
* Template standardisation level
* Reuse across jurisdictions
* Evidence of automation (dynamic factsheets, APIs)
* Localisation scalability

### 2. Cost Signalling

* Cost transparency clarity
* Fee breakdown visualisation
* Ongoing charges communication quality

### 3. Commercial Effectiveness

* Clear value proposition articulation
* Performance framing strength
* Call-to-action strength (retail documents)

---

# 🟢 II. CUSTOMER / INVESTOR PERSPECTIVE

### 4. Clarity & Readability

* Plain language usage
* Readability score (Flesch or equivalent)
* Logical information hierarchy
* Visual data storytelling

### 5. Segmentation Effectiveness

* Retail vs Institutional differentiation
* Professional/advisor adaptation
* Region-specific tailoring

### 6. Accessibility & Inclusion

* WCAG compliance signals
* Screen-reader friendly PDFs
* Colour contrast compliance
* Multi-format availability (HTML, PDF, interactive)

### 7. ESG & Transparency Communication

* SFDR clarity (if EU)
* ESG metric standardisation
* Stewardship reporting clarity
* Sustainability claims substantiation

---

# 🟠 III. INTERNAL PROCESS PERSPECTIVE

### 8. Regulatory Compliance Structure

* PRIIPs KID structure quality
* Prospectus clarity
* Risk disclosure presentation
* Cross-border regulatory adaptation

### 9. Update Discipline

* Frequency of factsheet updates
* Performance data timeliness
* Version control transparency
* Archive accessibility

### 10. Governance & Risk Management

* Disclaimer clarity
* Risk scale standardisation
* Conflict of interest disclosure
* Data source transparency

---

# 🟣 IV. LEARNING & GROWTH PERSPECTIVE

### 11. Digital Innovation

* Interactive factsheets
* Personalised document capability
* API-driven data integration
* ESG dashboarding

### 12. Thought Leadership Integration

* Market outlook quality
* Research integration into fund materials
* Investor education content depth

### 13. Future-Readiness

* AI-driven content adaptation signals
* Sustainability taxonomy evolution
* Alternative data usage in reporting

---

# 3️⃣ Scoring Model (Standardised for BSC Reporting)

Use a 1–5 maturity scale:

| Score | Maturity Level | Description                   |
| ----- | -------------- | ----------------------------- |
| 1     | Basic          | Regulatory minimum only       |
| 2     | Developing     | Structured but inconsistent   |
| 3     | Competitive    | In line with industry leaders |
| 4     | Advanced       | Strong differentiation        |
| 5     | Best-in-Class  | Market-leading innovation     |

You can then calculate:

* **Average per BSC Perspective**
* **Overall Peer Index Score**
* **Gap vs Your Organisation**

---

# 4️⃣ BSC Dashboard Output Structure

Once scored, your Balanced Scorecard view becomes:

| Perspective       | Your Score | Peer Average | Leader    | Gap  |
| ----------------- | ---------- | ------------ | --------- | ---- |
| Financial         | 3.1        | 3.8          | BlackRock | -0.7 |
| Customer          | 2.9        | 4.2          | Vanguard  | -1.3 |
| Internal Process  | 3.5        | 4.0          | Amundi    | -0.5 |
| Learning & Growth | 2.2        | 4.3          | BlackRock | -2.1 |

This gives your executive team:

* Clear prioritisation
* Strategic resource allocation signals
* Evidence-based improvement roadmap

---

# 5️⃣ Integration with Weekly Resource Utilisation Tracking

Since your organisation measures resource utilisation weekly, you can connect this matrix operationally.

## A. Link Improvement Themes to Resource Buckets

Example:

| BSC Gap                 | Initiative                  | Resource Owner         | Weekly Utilisation Target |
| ----------------------- | --------------------------- | ---------------------- | ------------------------- |
| Low Accessibility Score | WCAG 2.2 upgrade programme  | Design Team            | 15% allocation            |
| ESG Clarity Gap         | SFDR disclosure redesign    | Compliance + Marketing | 10% allocation            |
| Digital Innovation Gap  | Interactive factsheet pilot | Product + IT           | 20% allocation            |

---

## B. Weekly Tracking Overlay

You can align:

* % time spent on **regulatory maintenance**
* % time on **strategic enhancement**
* % time on **innovation**

This allows you to see whether resources are:

* Reactive (compliance-driven)
* Optimisation-focused
* Future-building

---

# 6️⃣ Optional Advanced Layer: Peer Heatmap Output

You can create a visual:

* Red = below peer average
* Amber = in line
* Green = outperforming
* Blue = leading

Very powerful for Board-level communication.

---

# If You’d Like Next

I can now:

* Build this into a **ready-to-copy Excel structure**
* Create a **Board-level executive summary template**
* Or design a **document intake scoring sheet** for analysts doing the comparison work

Which type of document are you analysing first (e.g., factsheets, KIDs, annual reports, pitchbooks)?


Marketing document taxonomy:

Absolutely — here are all five deliverables, designed to be **implementation-ready** for a document comparison tool in asset management.

---

## 1) Normalized Master Component Dictionary (de-duplicated)

A reusable “master library” of components that appear across factsheets, pitchbooks, KID/KIID, annual reports, DDQs, presentations, websites, etc.

### 1.1 Component groups and canonical components

**A. Identity & Product Metadata**

* `product_name`
* `share_class`
* `isin` / `sedol` / `ticker`
* `domicile`
* `base_currency`
* `launch_date`
* `aum`
* `benchmark_name`
* `benchmark_type` (official/custom/composite)
* `distribution_status` (retail/professional/institutional)
* `vehicle_type` (UCITS, AIF, ETF, SMA, mandate, etc.)
* `manufacturer` / `management_company`
* `depositary` / `trustee`
* `administrator` / `transfer_agent`
* `auditor`
* `custodian`

**B. Investor Proposition**

* `value_proposition_summary`
* `target_investor_profile`
* `suitability_constraints` (risk tolerance, horizon, currency)
* `investment_horizon`
* `key_benefits` (bullet set)
* `key_risks_summary` (bullet set)

**C. Objective, Strategy, Process**

* `investment_objective`
* `investment_strategy_overview`
* `investment_universe_definition`
* `alpha_sources`
* `portfolio_construction_rules`
* `risk_management_framework`
* `liquidity_profile_summary`
* `capacity_statement`
* `use_of_derivatives`
* `leverage_policy`
* `esg_integration_statement` (if applicable)
* `stewardship_policy_summary`

**D. Team & Governance**

* `portfolio_manager_bios`
* `team_structure`
* `investment_committee_description`
* `succession_plan_statement` (often ODD / institutional)
* `governance_overview`
* `ownership_structure`

**E. Performance & Analytics**

* `performance_time_series` (1M/3M/YTD/1Y/3Y/5Y/SI)
* `calendar_year_returns`
* `benchmark_relative_returns`
* `performance_chart`
* `performance_attribution_summary`
* `factor_exposures` (if used)
* `peer_comparison`
* `risk_adjusted_metrics` (Sharpe, Information Ratio, etc.)
* `drawdown_metrics`
* `portfolio_turnover`

**F. Portfolio & Exposure**

* `top_holdings`
* `sector_allocation`
* `geographic_allocation`
* `asset_allocation`
* `duration` / `ytm` / `spread` (FI)
* `credit_quality_breakdown` (FI)
* `style_box` (if used)
* `valuation_metrics` (P/E, P/B, etc.)
* `derivatives_exposure_summary`
* `cash_position`

**G. Costs, Terms, Dealing**

* `management_fee`
* `ongoing_charges`
* `performance_fee`
* `entry_exit_fees`
* `transaction_costs`
* `minimum_investment`
* `dealing_frequency`
* `settlement_terms`
* `liquidity_terms` (notice, gates, lock-ups)
* `share_class_features` (hedged, distributing/accumulating)

**H. ESG, Impact, Stewardship**

* `esg_policy_link_or_summary`
* `sfdr_classification` (where relevant)
* `paI_statement_summary` (where relevant)
* `carbon_metrics` (WACI, emissions, etc.)
* `engagement_case_studies`
* `proxy_voting_summary`
* `impact_objectives` (impact funds)

**I. Disclosures & Legal**

* `past_performance_disclaimer`
* `risk_disclosure_long`
* `benchmark_disclosure`
* `derivatives_risk_disclosure`
* `country_restrictions`
* `marketing_restrictions`
* `gips_compliance_statement` (if used)
* `data_sources_disclosure`
* `conflicts_of_interest_summary`
* `complaints_process`
* `contact_details`

**J. Operational Due Diligence (institutional-heavy)**

* `valuation_policy_summary`
* `trade_execution_policy`
* `business_continuity_summary`
* `cyber_security_summary`
* `compliance_monitoring_summary`
* `service_provider_overview`
* `regulatory_licenses_summary`

### 1.2 Canonical naming and de-dup rules

* One canonical component name per concept (e.g., `ongoing_charges` covers “OCF”, “TER”, “ongoing costs” as aliases).
* Each component has:

  * **datatype** (text/number/date/table/chart/link)
  * **audience** (retail/professional/institutional)
  * **requiredness by document type**
  * **regulatory tags**
  * **versioning rules** (e.g., monthly factsheet vs quarterly report)

---

## 2) Regulatory Mapping Taxonomy (PRIIPs/UCITS/UK/EU/US + generic)

This is a **taxonomy**, not jurisdiction-specific legal advice — it’s meant to tag components for compliance workflows.

### 2.1 Regulatory tags (high-level)

Use tags like:

* `REG_PRIIPS_KID`
* `REG_UCITS_KIID` (legacy contexts)
* `REG_UK_COBS` (financial promotions ruleset tag)
* `REG_EU_MIFID_MARKETING`
* `REG_US_SEC_1940_ACT`
* `REG_US_SEC_ADVISERS_ACT`
* `REG_GIPS` (standards, not law)
* `REG_SFDR`
* `REG_TCFD` / `REG_ISSB` (where used in reporting)
* `REG_LOCAL_FSCA` (South Africa marker, if applicable)

### 2.2 Component → regulatory relevance examples

**PRIIPs KID (typical)**

* `product_identification` → `REG_PRIIPS_KID`
* `risk_indicator` → `REG_PRIIPS_KID`
* `performance_scenarios` → `REG_PRIIPS_KID`
* `costs_breakdown` (incl RIY) → `REG_PRIIPS_KID`
* `recommended_holding_period` → `REG_PRIIPS_KID`
* `complaints_process` → `REG_PRIIPS_KID`

**UCITS retail documents (typical)**

* `objective_strategy_summary` → `REG_UCITS_KIID` / `REG_UCITS`
* `charges` → `REG_UCITS_KIID`
* `past_performance_presentation` → `REG_UCITS_KIID`
* `risk_reward_profile` → `REG_UCITS_KIID`

**Marketing/financial promotions (generic controls)**

* `past_performance_disclaimer` → `REG_UK_COBS` / `REG_EU_MIFID_MARKETING` / `REG_US_SEC_MARKETING_RULE`(tag)
* `risk_disclosure_long` → same
* `target_investor_profile` → suitability alignment tags
* `no_offer_no_advice_language` → promotion control tags

**US SEC Marketing Rule style tagging**

* `performance_methodology_disclosure`
* `net_vs_gross_returns`
* `benchmark_description`
* `time_period_requirements` (presentation rules)
* `testimonials_endorsements_disclosure` (if used in marketing)

**SFDR/ESG**

* `sfdr_classification`
* `paI_statement_summary`
* `sustainability_risk_disclosure`
* `principal_adverse_impacts_metrics` (if used)
* `engagement_and_voting_disclosure`

### 2.3 Implementation tip

Treat “regulatory mapping” as:

* **Document-level tags** (what the doc claims to be)
* **Component-level tags** (what must/may appear)
* **Claim-level tags** (e.g., “ESG impact claim”, “guarantee-like language”, “capital protection claim”)

---

## 3) Document Comparison Scoring Framework

A practical scoring model for comparing two versions (or two managers) across **completeness, consistency, compliance, and quality**.

### 3.1 Pillars and weights (baseline)

You can tune weights per channel.

1. **Completeness (25%)**

* Required components present (by doc type + channel)
* Optional components coverage

2. **Consistency & Reconciliation (25%)**

* Same values across documents (AUM, benchmark, inception date, fees)
* Same definitions (returns methodology, share class naming)
* Cross-doc consistency (factsheet vs pitchbook vs KID)

3. **Compliance Readiness (25%)**

* Mandatory disclosures present
* Risk warnings present and positioned correctly
* Performance presentation rules satisfied (net/gross, benchmark, time periods)
* Marketing restriction language and distribution legends present

4. **Quality & Clarity (15%)**

* Readability (plain language, jargon density)
* Visual integrity (charts labeled, axes, time period)
* Narrative clarity (objective, process, risk)

5. **Data Integrity & Timeliness (10%)**

* Data dates shown (as-of date)
* Update cadence matches doc type (monthly factsheet, quarterly commentary)
* Source references / calculation notes

### 3.2 Scoring mechanics (implementation-friendly)

**Per component scoring**

* `0` = missing
* `1` = present but weak (wrong format, ambiguous, out of date)
* `2` = present and acceptable
* `3` = best practice (clear, reconciled, correctly disclosed)

**Per pillar**

* Weighted average of its components, with “critical” components having multipliers.

**Critical component penalty**

* If a critical compliance component is missing: apply an automatic cap on compliance pillar (e.g., max 40%).

### 3.3 Example “critical” sets by document type

**Factsheet critical set**

* `as_of_date`
* `performance_time_series`
* `benchmark_disclosure`
* `past_performance_disclaimer`
* `risk_disclosure_short`
* `fees_summary`

**Pitchbook critical set**

* `strategy_description`
* `team`
* `risk_framework`
* `track_record_methodology` (esp if composites)
* `disclosures`

**PRIIPs KID critical set**

* `risk_indicator`
* `performance_scenarios`
* `costs_breakdown`
* `rhp`
* `complaints_process`

---

## 4) JSON-ready Schema for System Implementation

This is a pragmatic schema you can implement in a database + API. It supports:

* component library
* document templates
* extracted instances
* comparisons
* scoring + issues

```json
{
  "component_library": [
    {
      "component_id": "ongoing_charges",
      "name": "Ongoing Charges",
      "aliases": ["OCF", "TER", "Ongoing costs"],
      "group": "Costs, Terms, Dealing",
      "datatype": "number_percent",
      "format_rules": {
        "precision": 2,
        "range_min": 0.0,
        "range_max": 10.0
      },
      "audiences": ["retail", "professional", "institutional"],
      "regulatory_tags": ["REG_PRIIPS_KID", "REG_UCITS_KIID"],
      "best_practice_notes": "Show as-of date, include what it excludes/includes if relevant."
    }
  ],
  "document_types": [
    {
      "document_type_id": "fund_factsheet",
      "name": "Fund Factsheet",
      "channel": ["retail", "professional"],
      "cadence": "monthly",
      "required_components": [
        { "component_id": "product_name", "critical": true },
        { "component_id": "share_class", "critical": true },
        { "component_id": "as_of_date", "critical": true },
        { "component_id": "performance_time_series", "critical": true },
        { "component_id": "benchmark_disclosure", "critical": true },
        { "component_id": "past_performance_disclaimer", "critical": true },
        { "component_id": "ongoing_charges", "critical": true }
      ],
      "optional_components": [
        { "component_id": "performance_attribution_summary" },
        { "component_id": "factor_exposures" },
        { "component_id": "engagement_case_studies" }
      ]
    }
  ],
  "documents": [
    {
      "document_id": "doc_2026_02_factsheet_A",
      "document_type_id": "fund_factsheet",
      "manager_id": "manager_001",
      "product_id": "fund_ABC",
      "share_class_id": "ABC_ZAR_A",
      "version": "2026-02",
      "as_of_date": "2026-01-31",
      "source": {
        "file_name": "ABC_Factsheet_Feb2026.pdf",
        "ingested_at": "2026-02-20T08:00:00Z"
      },
      "component_instances": [
        {
          "component_id": "ongoing_charges",
          "value": 0.85,
          "value_as_text": "0.85%",
          "value_date": "2026-01-31",
          "location": { "page": 2, "bbox": [0.12, 0.44, 0.35, 0.47] },
          "confidence": 0.93,
          "notes": "Matches prospectus fee table."
        }
      ]
    }
  ],
  "comparison": {
    "comparison_id": "cmp_docA_vs_docB",
    "left_document_id": "doc_2026_02_factsheet_A",
    "right_document_id": "doc_2026_02_factsheet_B",
    "results": [
      {
        "component_id": "ongoing_charges",
        "status": "mismatch",
        "left": { "value": 0.85, "value_as_text": "0.85%" },
        "right": { "value": 0.95, "value_as_text": "0.95%" },
        "severity": "high",
        "issue_tags": ["DATA_RECONCILIATION", "INVESTOR_IMPACT"]
      }
    ],
    "scores": {
      "completeness": 0.92,
      "consistency": 0.74,
      "compliance": 0.88,
      "quality": 0.81,
      "data_integrity": 0.77,
      "overall": 0.83
    }
  }
}
```

---

## 5) Balanced Scorecard Alignment Overlay (asset management marketing ops)

Since your org uses **BSC** and measures **weekly resource utilisation**, this overlay ties **document production + quality** to BSC metrics.

### 5.1 BSC perspectives → document KPIs

**Financial**

* Cost per document (by type/channel)
* Rework rate cost (hours x blended rate)
* Distribution efficiency (cost per qualified lead / per institutional meeting)
* AUM influenced (attribution model if available)

**Customer (Investor/Distributor)**

* On-time delivery rate (factsheets, quarterlies)
* Investor query reduction (fewer follow-ups due to clearer disclosure)
* Content satisfaction / usability (sales feedback, client surveys)
* Win-rate uplift (pitchbook completeness vs mandate wins)

**Internal Process**

* SLA adherence (monthly cycle close)
* First-pass approval rate (compliance/legal)
* Defect density (missing critical components per doc)
* Cross-doc consistency rate (factsheet vs KID vs website)
* Data freshness compliance (as-of dates, benchmark updates)

**Learning & Growth**

* Template reuse rate (component reuse across docs)
* Automation coverage (components auto-populated)
* Staff capability (training completion, errors by editor)
* Knowledge base growth (new component patterns)

### 5.2 Weekly resource utilisation metrics (practical)

Track weekly by team and doc type:

* `planned_hours` vs `actual_hours`
* `% time on new build` vs `% time on rework`
* `cycle_time_days` by document type
* `bottleneck_stage` (data, content, design, compliance)

### 5.3 Recommended operational scorecard (example)

* **Weekly “Document Ops Health”**

  * On-time: target 95%+
  * First-pass compliance approval: target 85%+
  * Critical missing components: target 0
  * Rework hours / total hours: target < 15%
  * Consistency index (key fields reconciled): target 98%+

---

Document list clarity:

Below is a **curated list of the top marketing and investor-facing documents used in the asset management industry**, across different investor types (retail, wealth advisers, institutional). Included are **links to real examples or authoritative libraries** where you can access or view these documents.

---

## 📈 **Top 10 Asset Management Marketing / Investor Documents**

### 1) **Fund Factsheets (Performance & Fund Overview)**

* One-page summaries of key fund information — objectives, performance, holdings, fees and risk metrics — used by retail and professional investors. ([confluencegp.com][1])
  🔗 **Examples & templates:**
  • [Top 10 Fund Factsheet Templates With Examples and Samples (Diverse industry templates)](https://www.slideteam.net/blog/top-10-fund-factsheet-templates-with-examples-and-samples?utm_source=chatgpt.com)
  • [Fund Fact Sheets Template | Collaborative Docs (Structured doc template)](https://penno.io/templates/d/fund-fact-sheets?utm_source=chatgpt.com)

---

### 2) **Prospectus / Offering Documents**

* Formal regulatory documents providing full details on investment strategy, risks and legal disclosures for mutual funds, ETFs, and alternative products.
  🔗 **Examples:**
  • [Morningstar Document Library (Prospectuses, annual reports & filings)](https://doc.morningstar.com/Home.aspx?utm_source=chatgpt.com)
  • [Fund Documents | J.P. Morgan Asset Management (Fund doc portal)](https://am.jpmorgan.com/us/en/asset-management/adv/products/fund-documents/?utm_source=chatgpt.com)

---

### 3) **Pitch Books / Institutional Presentations**

* Customized sales presentations used to pitch capabilities to institutional investors, consultant groups, or advisors. ([acuityanalytics.com][2])
  🔗 **Reference:**
  • Wikipedia definition with context around usage: [Pitch book (investor marketing context)](https://en.wikipedia.org/wiki/Pitch_book?utm_source=chatgpt.com)

---

### 4) **Investment Policy Statements (IPS)**

* Formal documents that outline investment goals and constraints agreed between manager and client — useful in institutional and high-net-worth wealth channels. ([Wikipedia][3])
  🔗 **Glossary (definition & context):**
  • [Investment policy statement (Wikipedia)](https://en.wikipedia.org/wiki/Investment_policy_statement?utm_source=chatgpt.com)

---

### 5) **Quarterly / Annual Performance Reports**

* Comprehensive performance reporting for clients and prospects, often including commentary from portfolio managers and market outlooks.
  🔗 **Where to find:**
  • Morningstar’s document library (performance reports & filings): [Morningstar Document Library](https://doc.morningstar.com/Home.aspx?utm_source=chatgpt.com)

---

### 6) **White Papers & Research Reports**

* In-depth thematic investment research, macro outlooks or thought leadership content that establishes authority with institutional and professional audiences.
  🔗 **Example guide:**
  • [Professionalizing Investor Marketing Materials and Content (fund marketing guide PDF)](https://richeymay.com/wp-content/uploads/2025/02/Exponential-AUM-Richey-May-Guide-for-New-and-Emerging-Fund-Managers.pdf?utm_source=chatgpt.com)

---

### 7) **Sales Brochures / Capability Statements**

* Branded marketing brochures that succinctly communicate a firm’s value proposition, capabilities, differentiators and service offerings.
  🔗 **Provider example:**
  • Acuity’s asset management brochure offers context for these materials: [Fund Factsheets & Financial Marketing Materials – Acuity Analytics](https://www.acuityanalytics.com/services/fund-factsheets-and-marketing-material/?utm_source=chatgpt.com)

---

### 8) **RFP Responses / Manager Due Diligence Cases**

* Detailed responses to consultant or institutional Requests for Proposals (RFPs) that articulate strategy, process, performance and risk management to win mandates.
  🔗 **Morningstar library:**
  • Can host RFP attachments and support docs via: [Morningstar Document Library](https://doc.morningstar.com/Home.aspx?utm_source=chatgpt.com)

---

### 9) **ESG / Sustainable Investing Reports**

* Documents highlighting environmental, social and governance strategy, metrics and outcomes — increasingly critical for institutional and retail demand.
  🔗 **Library access:**
  • ESG sections often included with fund docs in the Morningstar library: [Morningstar Document Library](https://doc.morningstar.com/Home.aspx?utm_source=chatgpt.com)

---

### 10) **Advisory & Client Communication Letters**

* Regular letters from portfolio managers or client service teams summarizing performance, outlook and positioning for clients — used for retention and trust building.
  🔗 **Where to locate:**
  • Fund managers’ document portals typically include client letters and updates (e.g., J.P. Morgan AM documents). ([J.P. Morgan][4])

---

## 🧠 **How These Documents Work Together**

* **Awareness & Engagement:** Factsheets, brochures, white papers establish early interest. ([Morningstar, Inc.][5])
* **Conversion / Due Diligence:** Pitch books, RFP responses and prospectuses support professional and institutional evaluation. ([acuityanalytics.com][2])
* **Retention & Trust:** Performance reports, IPS, ESG reports and advisor letters sustain investor confidence and loyalty. ([Wikipedia][3])

---

### 📌 Pro Tip

Most major asset managers (e.g., BlackRock, Vanguard, J.P. Morgan, Goldman Sachs) have **document libraries** where you can download actual versions of these materials by fund or strategy — excellent references for best practice formats and compliance standards. ([J.P. Morgan][4])

---

If you want, I can **organize this into a downloadable template pack** or provide **examples for a specific investor segment** (e.g., institutional vs retail).

[1]: https://www.confluencegp.com/glossary/factsheet?utm_source=chatgpt.com "Factsheet: Key Elements of a Professional Fund Factsheet"
[2]: https://www.acuityanalytics.com/services/fund-factsheets-and-marketing-material/?utm_source=chatgpt.com "Fund Factsheets & Financial Marketing Materials | Acuity Analytics"
[3]: https://en.wikipedia.org/wiki/Investment_policy_statement?utm_source=chatgpt.com "Investment policy statement"
[4]: https://am.jpmorgan.com/us/en/asset-management/adv/products/fund-documents/?utm_source=chatgpt.com "Fund Documents | J.P. Morgan Asset Management"
[5]: https://www.morningstar.com/business/insights/blog/asset-management-marketing?utm_source=chatgpt.com "Asset Management Marketing: Overcoming a Competitive Market"

Here’s a **practical set of real-world examples** of asset management marketing and investor-facing documents tailored for **three specific investor segments** — **Institutional**, **Retail**, and **Professional/Advisor**. Where possible I’ve included **links to actual libraries, templates, or example resources** you can review or download.

---

## 🏛️ **1. Institutional Investors**

These documents are designed for pension funds, sovereign wealth funds, endowments, insurers, OCIOs, and other large allocators. They emphasise **process, risk controls, track record, governance, and detailed analytics** — all essential to win institutional mandates.([Viktori][1])

### 🔹 Institutional Example Documents

1. **Institutional Pitch Book / Presentation** – A structured template to present capabilities, strategy, process, team, and performance.
   🔗 **Institutional Pitch Book Template (example & guidance)** – FinanceWorld (template & guidance to structure data-rich decks) ([Hedge Fund Signals][2])

2. **LP Investor Pitch Deck (Private Funds)** – Best practices + sample elements for LP-focused capital raising decks.
   🔗 **Investor Pitch Deck Tips & Template** – Carta (free guidance + typical pitch deck structure) ([Carta][3])

3. **Institutional Fund Factsheets** – Formal periodic reports with detailed holdings, risk metrics, and performance histories (used by consultants and institutional allocators).
   🔗 Example libraries often held by large managers (example: **Goldman Sachs Asset Management Document Library**) ([Goldman Sachs Asset Management][4])

4. **Detailed Prospectus / Offering Memorandum** – Full legal disclosure and strategy overview for institutional vehicles (e.g., separate accounts, institutional share classes).
   🔗 See fund document portals of major asset managers (e.g., Goldman Sachs) ([Goldman Sachs Asset Management][4])

5. **Manager Due Diligence Questionnaire (DDQ) / RFP Response** – Standardised institutional due diligence documentation tailored to allocator questions (performance, ops, risk, compliance).
   🔗 (Often part of institutional pitchbooks or bespoke submissions — see typical templates in DDQ libraries online)

---

## 🛍️ **2. Retail Investors**

Retail documents are simpler, highly visual, and compliance-focused. They help individual investors understand products in plain language, with clear disclosures and comparative info.

### 🔹 Retail Example Documents

1. **Retail Fund Factsheets / One-Pagers** – Key performance, objective, risk highlights and fees for public consumption.
   🔗 Many asset managers provide these online — for example, **Goldman Sachs Asset Management Fund Documents** has retail factsheets & prospectuses available. ([Goldman Sachs Asset Management][4])

2. **Prospectus & Summary Prospectus (Mutual Funds / ETFs)** – Regulatory required offering documents for retail products with key terms, risks, fees, and objectives.
   🔗 Often downloadable from managers’ public document libraries (e.g., GS AM or Vanguard / BlackRock websites).

3. **Quarterly or Annual Reports / Shareholder Letters** – Investor letters summarising performance, strategy outlook, portfolio activity.
   🔗 Refer to major fund document libraries (e.g., GS AM). ([Goldman Sachs Asset Management][4])

4. **Tear Sheets / Product Brochures** – Short product brochures designed for public and intermediated channels.
   🔗 Providers like Emerson Ward showcase examples of these collateral formats. ([em-ward.com][5])

5. **Educational Guides / How-To Content** – Easy-to-digest guides on investing basics, risk tolerance, and product differences (common on Vanguard, Fidelity educational sections).

---

## 🧑‍💼 **3. Professional / Advisor Investors**

This segment includes financial advisers, wealth managers, broker-dealers, and consultant audiences. Documents here are **technical but practical**, often combining institutional depth with retail clarity.

### 🔹 Professional/Advisor Example Documents

1. **Advisor Pitchbooks / Sales Presentations** – Decks crafted to help advisers understand product universes, suitability, and client fit.
   🔗 Solutions and examples for pitchbooks and sales presentations — e.g., **Kurtosys Pitchbooks & Sales Presentations** tools with sample outputs. ([Kurtosys][6])

2. **Product Fact Sheets oriented for Advisors** – More detailed than retail factsheets, including analytics and comparative tables suited to client conversations.

3. **White Papers / Research Reports** – Thought leadership pieces on macro themes or strategy insights targeted at professional audiences.

4. **Model Portfolios & Strategy Papers** – Package of model portfolios with rationale, risk characteristics, and implementation guidance for advisers.

5. **Marketing Brochures for Intermediary Channels** – Brochures tailored to advisor platforms (RIA/BD) focusing on differentiation, support, tools, and service levels.

---

## 📘 How These Documents Differ by Investor Type

| Document Type | Institutional                    | Professional/Advisor             | Retail                         |
| ------------- | -------------------------------- | -------------------------------- | ------------------------------ |
| Factsheets    | Detailed analytics, risk metrics | Strategy + advisor routing tools | Simple performance + risk band |
| Pitchbooks    | Deep dive with governance & ops  | Advisor-oriented sales story     | High-level product intro       |
| Prospectus    | Comprehensive legal              | Selective relevant disclosures   | Mandatory clear language       |
| Reports       | Complex commentary               | Advisor actionable insights      | Accessible summary             |
| Educational   | Allocator research               | Professional enablement          | Investor education             |

---

## 📥 Useful Public Links to Examples

* **Goldman Sachs Asset Management Document Library** – fund documents, prospectuses, reports (multisegment) ([Goldman Sachs Asset Management][4])
* **Institutional Pitch Book Template Example** – FinanceWorld guidance ([Hedge Fund Signals][2])
* **Private Fund Investor Pitch Guides & Templates** – Carta resource on LP pitch decks ([Carta][3])
* **Professional Pitchbook Tools & Examples** – Kurtosys (sample pitchbook approach) ([Kurtosys][6])

---

If you want, I can **assemble real downloadable examples** (PDFs or links from major managers like Vanguard, BlackRock, Fidelity) specific to **one of these segments (e.g., Institutional)** — just specify which one.

[1]: https://viktori.co/asset-management-pitch-deck-examples/?utm_source=chatgpt.com "3 Asset Management Pitch Deck Examples (2026 Update)"
[2]: https://financeworld.io/learn/institutional-pitch-book-template/?utm_source=chatgpt.com "Institutional Pitch Book Template - FinanceWorld - Trading Signals and ..."
[3]: https://carta.com/learn/private-funds/management/portfolio-management/investor-pitch-deck/?utm_source=chatgpt.com "LP Investor Pitch Deck: Free Template for Fund Managers - Carta"
[4]: https://am.gs.com/en-us/advisors/documents?utm_source=chatgpt.com "Document Library - Goldman Sachs Asset Management"
[5]: https://www.em-ward.com/pitch-books?utm_source=chatgpt.com "Pitch Books, Tear Sheets & Fund Materials - Emerson Ward"
[6]: https://www.kurtosys.com/investment-management/pitchbooks-sales-presentations/?utm_source=chatgpt.com "Pitchbooks For Asset Managers | Kurtosys"


Below are **real, downloadable examples and live links to investor documents** from **major asset managers** — *BlackRock*, *Vanguard*, and *Fidelity* — organized by **investor segment** (Institutional, Professional/Advisor, Retail). These include **prospectuses, summary prospectuses, regulatory documents, and fund libraries** that you can access now.

---

## 🏛️ **Institutional Investor Documents**

### **BlackRock**

1. **BlackRock Global Funds Prospectus (PDF)** – Comprehensive prospectus for range of BlackRock funds.
   🔗 [https://www.blackrock.com/uk/literature/prospectus/blackrock-global-funds-prospectus-en.pdf](https://www.blackrock.com/uk/literature/prospectus/blackrock-global-funds-prospectus-en.pdf) ([BlackRock][1])

2. **BlackRock Strategic Funds Prospectus (PDF)** – Prospectus for strategic fund offerings.
   🔗 [https://www.blackrock.com/uk/literature/prospectus/blackrock-strategic-funds-prospectus-en.pdf](https://www.blackrock.com/uk/literature/prospectus/blackrock-strategic-funds-prospectus-en.pdf) ([BlackRock][2])

3. **BlackRock UCITS Funds Prospectus (PDF)** – Detailed European UCITS fund disclosures.
   🔗 [https://www.blackrock.com/uk/literature/prospectus/blackrock-ucits-funds-prospectus-en.pdf](https://www.blackrock.com/uk/literature/prospectus/blackrock-ucits-funds-prospectus-en.pdf) ([BlackRock][3])

4. **BlackRock Institutional Advisor Library** – BlackRock’s central document library including prospectuses, regulatory docs, and reports (searchable).
   🔗 [https://www.blackrock.com/cash/en-us/library](https://www.blackrock.com/cash/en-us/library) ([BlackRock][4])

### **Fidelity Institutional / Advisor**

5. **Fidelity Advisor Funds Regulatory Documents** – Prospectuses, shareholder reports, holdings, and fact sheets for advisor/institutional share classes.
   🔗 [https://institutional.fidelity.com/app/tabbed/literature/FIIS_FL_REGDOCS_ADVISOR_DPL2.html?navId=320&productLine=2&tab=literature](https://institutional.fidelity.com/app/tabbed/literature/FIIS_FL_REGDOCS_ADVISOR_DPL2.html?navId=320&productLine=2&tab=literature) ([institutional.fidelity.com][5])

6. **Fidelity Institutional Model Portfolios** – Example model portfolio documentation used with institutional/advisor clients.
   🔗 [https://institutional.fidelity.com/advisors/investment-solutions/model-portfolios](https://institutional.fidelity.com/advisors/investment-solutions/model-portfolios) ([institutional.fidelity.com][6])

---

## 🧑‍💼 **Professional / Advisor Investor Documents**

### **BlackRock**

7. **BlackRock Summary Prospectus (US example)** – Summary prospectus for one BlackRock mutual fund (simplified investor version, useful for advisors).
   🔗 [https://www.blackrock.com/us/individual/literature/summary-prospectus/sumpro-brfunds-exchangeport-blk-us.pdf](https://www.blackrock.com/us/individual/literature/summary-prospectus/sumpro-brfunds-exchangeport-blk-us.pdf) ([BlackRock][7])

8. **BlackRock 80/20 Target Allocation Fund Summary Prospectus (PDF)** – Another sample US mutual fund summary prospectus.
   🔗 [https://www.blackrock.com/us/individual/literature/summary-prospectus/spro-brglobalallocationfund-k-us.pdf](https://www.blackrock.com/us/individual/literature/summary-prospectus/spro-brglobalallocationfund-k-us.pdf) ([BlackRock][8])

### **Fidelity**

9. **Fidelity Fund Summary Prospectus (example PDF)** – Example fund summary prospectus outlining key details for advisors reviewing with clients.
   🔗 [Fidelity Fund Summary Prospectus (PDF)](https://www.actionsxchangerepository.fidelity.com/ShowDocument/documentPDF.htm?_fax=-18%2342%23-61%23-110%23114%2378%23117%2320%23-1%2396%2339%23-62%23-21%2386%23-100%2337%2316%2335%23-68%2391%23-66%2354%23103%23-16%2369%23-30%2358%23-20%2376%23-84%2348%23-52%23-21%23-96%23-58%23-33%23-107%23-46%2393%23113%23-112%23127%23-42%23-97%2330%23-58%23-23%2384%23117%23-35%23-30%2342%23-18%2351%2343%23-101%2349%2336%2311%2364%23-12%2396%23-42%23-22%23-11%2360%2318%2396%23-99%2375%23103%2397%23-93%2316%23117%2380%233%2316%2326%2358%23-72%23-108%2383%2369%23-10%23103%2380%23-89%2369%23-17%23-14%23-98%23123%23-18%2345%23-59%2367%23-93%23-15%23-126%2377%23-126%23120%2376%23-8%2340%234%23-24%2383%2399%230) ([Fidelity Actions Exchange Repository][9])

---

## 🛍️ **Retail Investor Documents**

### **Vanguard**

10. **Vanguard Prospectuses & Reports Library** – Central location for all mutual fund and ETF prospectuses, summary prospectuses, and shareholder reports.
    🔗 [https://vanguard.com/us/literature/reports/mutualfunds](https://vanguard.com/us/literature/reports/mutualfunds) ([Vanguard][10])

11. **Vanguard 500 ETF Prospectus (PDF)** – Example Vanguard ETF prospectus you can download directly.
    🔗 [https://personal.vanguard.com/pub/Pdf/p968.pdf](https://personal.vanguard.com/pub/Pdf/p968.pdf) ([Vanguard Personal][11])

### **Fidelity**

12. **Fidelity Shareholder Reports & Prospectuses** – Database to search and download prospectuses and shareholder reports for Fidelity mutual funds.
    🔗 [https://fundresearch.fidelity.com/prospectus/funds](https://fundresearch.fidelity.com/prospectus/funds) ([Fidelity Fund Research][12])

### **BlackRock (Retail-oriented)**

13. **BlackRock Summary Prospectus (High Yield or Target Allocation)** – Sample simple fund disclosures retail investors often receive.
    🔗 [https://www.blackrock.com/us/individual/literature/summary-prospectus/sumpro-taf8020-inv-us.pdf](https://www.blackrock.com/us/individual/literature/summary-prospectus/sumpro-taf8020-inv-us.pdf) ([BlackRock][13])

14. **BlackRock Individual Investors Library** – Library with prospectuses, regulatory docs, and fund disclosures for retail products.
    🔗 [https://www.blackrock.com/cash/en-us/library](https://www.blackrock.com/cash/en-us/library) ([BlackRock][4])

---

## 📊 **Additional Useful Libraries**

* **SEC Filings Search (Prospectuses & Mutual Fund Filings)** – Use to find any fund’s latest regulatory filings including prospectus and shareholder reports.
  🔗 [https://www.sec.gov/search-filings/mutual-funds-search](https://www.sec.gov/search-filings/mutual-funds-search) ([SEC][14])

---

### 📌 Tips to Use These Documents

* **Institutional docs** (like BlackRock global/UCITS prospectuses) are best for deep due diligence and mandate review.
* **Advisor/professional docs** (summary prospectuses + advisor libraries) strike a balance between depth and readability.
* **Retail docs** (simple prospectuses + shareholder reports) are designed for public investor education and regulatory compliance.

---

If you want, I can **extract key sections** (e.g., fees, performance tables, risk factors) from any of the specific PDFs above to build a side-by-side comparison for your segment of interest.

[1]: https://www.blackrock.com/uk/literature/prospectus/blackrock-global-funds-prospectus-en.pdf?utm_source=chatgpt.com "BlackRock Global Funds Prospectus 16 December 2025"
[2]: https://www.blackrock.com/uk/literature/prospectus/blackrock-strategic-funds-prospectus-en.pdf?utm_source=chatgpt.com "BlackRock Strategic Funds Prospectus 3 December 2025"
[3]: https://www.blackrock.com/uk/literature/prospectus/blackrock-ucits-funds-prospectus-en.pdf?utm_source=chatgpt.com "BLACKROCK UCITS FUNDS PROSPECTUS"
[4]: https://www.blackrock.com/cash/en-us/library?utm_source=chatgpt.com "Library - BlackRock"
[5]: https://institutional.fidelity.com/app/tabbed/literature/FIIS_FL_REGDOCS_ADVISOR_DPL2.html?navId=320&productLine=2&tab=literature&utm_source=chatgpt.com "Fidelity Advisor Funds Regulatory Documents | Fidelity Institutional"
[6]: https://institutional.fidelity.com/advisors/investment-solutions/model-portfolios?utm_source=chatgpt.com "Model Portfolios - Fidelity Institutional"
[7]: https://www.blackrock.com/us/individual/literature/summary-prospectus/sumpro-brfunds-exchangeport-blk-us.pdf?utm_source=chatgpt.com "BLACKROCK FUNDSSM"
[8]: https://www.blackrock.com/us/individual/literature/summary-prospectus/spro-brglobalallocationfund-k-us.pdf?utm_source=chatgpt.com "Summary Prospectus - BlackRock"
[9]: https://www.actionsxchangerepository.fidelity.com/ShowDocument/documentPDF.htm?_fax=-18%2342%23-61%23-110%23114%2378%23117%2320%23-1%2396%2339%23-62%23-21%2386%23-100%2337%2316%2335%23-68%2391%23-66%2354%23103%23-16%2369%23-30%2358%23-20%2376%23-84%23-11%23-87%2348%23-52%23-21%23-96%23-58%23-33%23-107%23-46%2393%23113%23-112%23127%23-42%23-97%2330%23-58%23-23%2384%23117%23-35%23-30%2342%23-18%2351%2343%23-101%23-94%23111%2379%23-104%23-49%23-19%23-77%2362%2359%2372%23-69%23-107%2312%23-48%2361%23-67%23-76%2311%23-2%23-108%23127%23-55%23-45%23-28%23-62%23-34%235%23-33%23-100%23-122%23-21%2364%2358%23-118%23-78%2342%23-24%2380%23-75%23-123%23-36%23-32%2325%2370%2319%23101%2349%2336%2311%2364%23-12%2396%23-42%23-22%23-11%2360%2318%23-99%2375%23103%2397%23-93%2316%23117%2380%233%2316%2326%2358%23-72%23-108%2383%2369%23-10%23103%2380%23-89%2369%23-17%23-14%23-98%23123%23-18%2345%23-59%23-82%23112%238%23105%23-76%2371%2392%23-43%23-20%23-96%23-76%23-108%2325%23-13%23-74%23-92%23-79%23-4%23-28%2354%23-57%2367%23-93%23-15%23-126%23&utm_source=chatgpt.com "Fidelity® Fund Class/Ticker Fidelity® Fund/FFIDX Summary Prospect"
[10]: https://vanguard.com/us/literature/reports/mutualfunds?utm_source=chatgpt.com "Vanguard - Prospectuses"
[11]: https://personal.vanguard.com/pub/Pdf/p968.pdf?utm_source=chatgpt.com "Vanguard S&P 500 ETF"
[12]: https://fundresearch.fidelity.com/prospectus/funds?utm_source=chatgpt.com "Fidelity Shareholder Reports"
[13]: https://www.blackrock.com/us/individual/literature/summary-prospectus/sumpro-taf8020-inv-us.pdf?utm_source=chatgpt.com "Summary Prospectus - BlackRock"
[14]: https://www.sec.gov/search-filings/mutual-funds-search?utm_source=chatgpt.com "Mutual Funds Search - SEC.gov"

Accessibility requirements for all Jurisdictions:

Below is a **comprehensive list of accessibility and assistive-technology requirements** that customer-facing financial services documents (retail, institutional, professional) should adhere to. This applies to PDFs, Word documents, web-based documents, presentations, factsheets, KIIDs, PRIIPs KIDs, reports, and marketing materials.

I’ve grouped this by:

1. **Legal & Regulatory Standards**
2. **Technical Accessibility Standards**
3. **Document Structure & Formatting Requirements**
4. **Assistive Technology Compatibility**
5. **Visual & Design Requirements**
6. **Multimedia Accessibility**
7. **Digital Distribution Requirements**
8. **Testing & Governance Requirements**

---

# 1️⃣ Legal & Regulatory Requirements

Depending on jurisdiction, documents must comply with:

### 🇪🇺 European Union

* **European Accessibility Act (EAA) (Directive (EU) 2019/882)**
* **Web Accessibility Directive (2016/2102)**
* EN 301 549 (EU accessibility standard referencing WCAG)
* Equality legislation (e.g., national disability acts)

### 🇬🇧 UK

* Equality Act 2010
* Public Sector Bodies Accessibility Regulations (if applicable)
* FCA “clear, fair and not misleading” + vulnerability guidance

### 🇺🇸 USA

* Americans with Disabilities Act (ADA)
* Section 508 (for government-linked entities)
* WCAG 2.1 AA (industry standard benchmark)

### Global Best Practice Standard

* **WCAG 2.1 or 2.2 Level AA** (minimum benchmark)
* PDF/UA (ISO 14289) for accessible PDFs

---

# 2️⃣ Core Technical Accessibility Standards

Documents must meet:

### WCAG 2.1/2.2 AA Principles:

* **Perceivable**
* **Operable**
* **Understandable**
* **Robust**

Key technical success criteria include:

### A. Text Alternatives

* Alt text for:

  * Images
  * Charts
  * Graphs
  * Icons
  * Infographics
* Decorative images marked as decorative
* Complex charts require long descriptions

---

### B. Structure & Semantics

* Proper heading hierarchy (H1 → H2 → H3)
* Tagged PDF structure
* Logical reading order
* Lists properly tagged
* Tables correctly structured with:

  * Header rows identified
  * Scope defined
  * No merged cells that break screen readers

---

### C. Keyboard Accessibility

* All interactive elements accessible via keyboard
* Logical tab order
* Visible focus indicators

---

### D. Colour & Contrast

* Minimum contrast ratio:

  * 4.5:1 for normal text
  * 3:1 for large text
* No meaning conveyed by colour alone
* Charts must not rely solely on colour

---

### E. Reflow & Zoom

* Text resizable up to 200% without loss of content
* No horizontal scrolling at standard breakpoints
* Responsive layout (for HTML documents)

---

### F. Forms (if applicable)

* Properly labelled fields
* Error messages clearly described
* Instructions programmatically associated
* Accessible CAPTCHA alternatives

---

# 3️⃣ Document-Specific Requirements (PDF, Word, PPT)

## 📄 Accessible PDFs (Critical for Financial Services)

Must include:

* Tagged PDF
* Defined document language
* Title metadata
* Bookmarks for long documents
* Logical reading order
* No scanned image-only PDFs (must be OCR’d and tagged)
* Accessible links (descriptive link text, not “click here”)
* No text embedded in images
* Table headers properly coded
* Footnotes properly structured
* Accessible signature fields (if applicable)

Preferred standard:

* **PDF/UA compliant**

---

## 📝 Word Documents

* Use built-in heading styles
* No manual formatting as structure
* Alt text for images
* Accessible tables
* Proper list formatting
* Avoid floating objects
* Defined document language
* Use Accessibility Checker

---

## 📊 PowerPoint

* Use slide layouts (not text boxes)
* Logical reading order
* Alt text for visuals
* Sufficient contrast
* Avoid automatic slide transitions
* Avoid flashing animations
* Accessible charts

---

# 4️⃣ Assistive Technology Compatibility

Documents must function with:

### Screen Readers

* JAWS
* NVDA
* VoiceOver
* TalkBack

### Magnification Software

* ZoomText
* Built-in OS magnifiers

### Speech Recognition

* Dragon NaturallySpeaking
* OS-level dictation

### Keyboard-Only Navigation

* No mouse dependency

---

# 5️⃣ Visual & Cognitive Accessibility

### Plain Language Requirements

* Avoid jargon (or define it clearly)
* Short sentences
* Clear section headings
* Summary sections
* Consistent terminology

### Layout Requirements

* Adequate white space
* Left-aligned text (avoid justified blocks)
* Minimum 12pt font (14pt preferred for consumer docs)
* Sans-serif fonts preferred
* Avoid ALL CAPS for body text

---

# 6️⃣ Charts, Graphs & Financial Data (High-Risk Area)

Financial documents often fail here.

Requirements:

* Data tables accompanying charts
* Pattern differentiation (not colour alone)
* Axis labels clear and readable
* Legends accessible
* Alt text explaining:

  * Trend direction
  * Key figures
  * Comparative performance
* No embedded images of performance tables

---

# 7️⃣ Multimedia (If Included)

For embedded video/audio:

* Closed captions
* Transcripts
* Audio descriptions (if visual content critical)
* No autoplay
* Accessible media players

---

# 8️⃣ Digital Distribution Requirements

For documents hosted online:

* Accessible download links
* File size disclosed (if large)
* HTML alternative where possible
* Mobile accessibility
* No time-limited access without warning
* No inaccessible document gates (e.g., inaccessible forms)

---

# 9️⃣ Additional Financial Services-Specific Considerations

Given the regulatory environment:

### Vulnerable Customers

* Alternative formats available on request:

  * Large print
  * Braille
  * Audio
  * Easy-read versions

### Mandatory Disclosures

* Risk warnings must:

  * Meet contrast requirements
  * Not be visually minimized
  * Be screen-reader accessible
  * Not be embedded as images

### ESG / Impact Reporting

* Complex charts must have textual equivalents
* Interactive dashboards must meet WCAG

---

# 🔟 Testing & Governance Requirements

Organizations should:

* Run automated accessibility testing tools
* Conduct manual screen reader testing
* Use PAC 2021 (for PDF/UA validation)
* Perform usability testing with disabled users
* Maintain accessibility statement
* Keep documented remediation process

---

# 🚨 Common Failures in Asset Management Documents

* Untagged PDFs
* Performance tables as images
* Poor colour contrast in brand templates
* Risk warnings in small font
* Incorrect reading order
* Broken table tagging
* Inaccessible footnotes
* No alt text on charts

---

# 📌 Minimum Compliance Baseline (Best Practice)

For customer-facing financial documents:

* WCAG 2.1 AA compliant
* PDF/UA compliant
* EN 301 549 compliant (EU)
* ADA aligned (US)
* Alternative formats available
* Accessibility statement published

---

Just let me know which direction you want to take.


---

**Cursor**

This is a substantial upgrade. I'll rebuild the UI from scratch with a polished, professional design and incorporate all the new context — ESG detection, expanded taxonomy, comprehensive accessibility checks, the 5-pillar scoring framework, full BSC integration, and peer benchmarking.

Now rebuilding the full UI.

The app is running at **http://localhost:8501**. Here's everything that changed:

---

### New modules

**`benchmarking/esg_detector.py`** — Determines whether a document needs ESG content by scanning for:
- ESG-sensitive sectors (energy, mining, tobacco, weapons, etc.)
- ESG-positive themes (renewables, green bonds, impact, etc.)
- Regulatory signals (SFDR, Article 8/9, TCFD, EU Taxonomy)
- Strategy signals (ESG integration, stewardship, proxy voting)
- Holdings triggers (controversial weapons, thermal coal, supply chain)
- Also checks which of 6 required ESG elements are present vs missing

### Expanded modules

**`accessibility/checks.py`** — Now 12 checks across 5 categories (Structure, Text Alternatives, Visual, Cognitive, Financial Services, Navigation), each tagged with WCAG criterion, severity level, and standard (WCAG 2.1, PDF/UA, EN 301 549).

**`benchmarking/scoring.py`** — Now includes both the **6-dimension evaluation** (1–5 maturity scale) and the **5-pillar comparison framework** (Completeness, Consistency, Compliance, Quality, Data Integrity) scored 0–100%.

**`benchmarking/taxonomy.py`** — Expanded to 10 categories matching the master component dictionary (Identity & Metadata, Investor Proposition, Objective/Strategy, Team/Governance, Performance, Portfolio, Costs, ESG, Disclosures, Operational DD).

### Rebuilt UI — 8 tabs

| Tab | What's there |
|-----|-------------|
| **Overview** | Hero metrics, 6-dimension score cards, 5-pillar horizontal bar charts |
| **Radar & Heatmap** | Plotly radar chart with baseline references + colour-coded heatmaps for dimensions and pillars |
| **Taxonomy** | 10-category coverage with progress bars, matched keywords, missing category warnings |
| **Compliance** | Jurisdiction rules with severity badges (critical/major/minor), regulatory framework reference table |
| **Accessibility** | 12 checks grouped by category, severity badges, WCAG criterion tags, assistive tech reference |
| **ESG Assessment** | Needs-ESG determination, sector detection, regulatory signals, missing ESG elements |
| **Balanced Scorecard** | 4 BSC perspectives with mapped dimensions, scores, and peer comparison template |
| **Insights** | Strengths/weaknesses cards, actionable recommendations, peer benchmarking matrix |

The sidebar includes jurisdiction, document type, target audience, and the peer benchmark set. Upload a document and try it out.

---

**User**

Can you emulate the look and feel of the UI in the attachment?

There is not enough colour contrast on the field values in the sidebar in light mode, screenshot attached for reference.

As a user I want to be able to upload multiple documents of various types.

I want to be able to see a data table showing all of the documents I have analysed. 

The data table must have filters for the different document types.

The data table must have sort options. E.g reorder by date, name, document type etc.

I want to export the results in a pdf.

Please use the Plus Jakart Sans font throught the design.

I want the colours in the 3rd attacment I added to be the prevalant palette for the UI design.

---

**Cursor**

This is a big overhaul. Let me rebuild the full app with all your requirements — new palette, font, multi-doc upload, data table, PDF export, and the dashboard style from the reference.

Now rebuilding the entire app.

The app is live at **http://localhost:8501**. Here's everything that changed:

---

### Design overhaul

- **Font**: Plus Jakarta Sans everywhere (body, headings, tabs, inputs, metrics)
- **Colour palette** from your reference:
  - Blue 600 `#071935` (sidebar, headers) / Blue 500 `#0342E4` (accents, active tabs)
  - Slate 400 `#3A4051` / Slate 300 `#4A5267` (body text)
  - Grey 400 `#B0B8CB` / Grey 300 `#C3C9D9` (borders, secondary text)
  - White `#FFFFFF` (cards, backgrounds)
  - Green 500 `#2E7D32` / Green 400 `#00C761` (success states)
- **Sidebar contrast fix**: Select boxes now have a **white background** with dark slate text (`#3A4051`) — fully readable in both light and dark mode
- **Dashboard card style**: Clean white cards with subtle grey borders, rounded corners (16–18px), hover shadows — matching the financial dashboard reference

### Multi-document upload

- Upload **multiple files at once** (the uploader accepts multiple PDFs/DOCX)
- Each file is analysed and stored in session state
- Upload more files at any time — they're added to the existing collection

### Data table

- Shows all analysed documents with columns: Document, Type, Jurisdiction, Audience, Overall, Compliance, Accessibility, ESG Needed, Date
- **Filters**: multiselect for document type and jurisdiction
- **Sort**: by date (newest/oldest), name (A–Z/Z–A), overall score, compliance score, accessibility score
- Built with `st.dataframe` for smooth interaction

### PDF export

- Select any document from the table and click **Export PDF**
- Generates a downloadable PDF report with: scores, dimension breakdown, compliance rules, accessibility checks, taxonomy coverage, strengths, weaknesses, and recommendations

### Document detail view

- Select any analysed document to see the full 8-tab detail view (Overview, Radar, Taxonomy, Compliance, Accessibility, ESG, BSC, Insights)

---

**User**

Please improve the UI based on the previous prompt.

Update the fonts and colours as requested too.

I want to save my analysed documents to some sort of library/repository.

I want to be able to login and register as a user in the app.

When I log in I want to access my analysis history in the library/repository.

---

**Cursor**

Now rebuilding the full app with auth, library, and the improved UI.

The app is now running at **http://localhost:8501** with all the requested changes. Here's a summary of what's been built:

**Authentication**
- **Sign In / Register** screens with a clean card-style UI using the Plus Jakarta Sans font and your colour palette
- Passwords are securely hashed with bcrypt
- User sessions persist via Streamlit session state

**SQLite Database**
- `users` table for authentication (email, name, hashed password)
- `analyses` table storing every analysis per user (filename, doc type, jurisdiction, audience, scores, full results as JSON)
- Located at `data/benchmarking.db` in the project root

**Library / History**
- When you log in, all your previously saved analyses load automatically from the database
- New uploads are analysed and saved to the library in real-time
- The **Library** tab shows a data table of all your documents with filters (type, jurisdiction) and sort options (date, name, scores)
- You can export individual results as PDF or remove entries from the library

**Document Detail**
- The **Document Detail** tab gives you the full 8-tab breakdown: Overview, Radar & Heatmap, Taxonomy, Compliance, Accessibility, ESG, Balanced Scorecard, and Insights

**UI Improvements**
- Plus Jakarta Sans font applied globally
- Dark navy (`#071935`) sidebar with high-contrast white text and white input fields
- Hero metric cards, dimension pills, pillar progress bars, and finding rows all use the requested colour palette
- Gradient header banner with personalised welcome message

---

**User**

I'm gettig a "All fields are required" on the register screen, even when all the fields are completed.

Not being able to register leaves me stuck and I can't access the UI.

---

**Cursor**

This is a classic Streamlit issue — when you click the button, the page reruns and the widget values can be lost before the validation runs. The fix is to use `st.form` which batches the inputs and submits them together.

Now I can see the issue clearly. The `st.button` triggers a rerun before the text input values are captured. Switching both forms to use `st.form` will fix this — it batches all widget values and only submits on button press.

The fix is live. The root cause was that `st.button` triggers a full Streamlit rerun, which clears the local variables from `st.text_input` before the validation logic executes. By wrapping both forms in `st.form`, all input values are batched and only submitted when you press the submit button — so `name`, `email`, `pw1`, and `pw2` are all guaranteed to contain your typed values at the time of validation.

Refresh the page at **http://localhost:8501** and try registering again. The "All fields are required" error should no longer appear when the fields are filled in.

---

**User**

When I export to pdf, I get the following error.fpdf.errors.FPDFUnicodeEncodingException: Character "—" at index 106 in text is outside the range of characters supported by the font used: "helvetica". Please consider using a Unicode font.

File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool/app.py", line 429, in <module>
    st.download_button("⬇ Download", data=gen_pdf(entry), file_name=f"benchmark_{exp_doc.rsplit('.',1)[0]}.pdf", mime="application/pdf", key="dl_pdf")
                                          ~~~~~~~^^^^^^^
File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool/app.py", line 385, in gen_pdf
    pdf.cell(0,5,f"  [{st_txt}] {r.get('name',r.get('check',''))} - {r.get('message','')}",new_x="LMARGIN",new_y="NEXT")
    ~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/fpdf/fpdf.py", line 281, in wrapper
    return fn(*args, **kwargs)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/fpdf/deprecation.py", line 36, in wrapper
    return fn(*args, **kwargs)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/fpdf/fpdf.py", line 3910, in cell
    text = self.normalize_text(text)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/fpdf/fpdf.py", line 5683, in normalize_text
    raise FPDFUnicodeEncodingException(
    ...<3 lines>...
    ) from error

---

**Cursor**

The built-in Helvetica font in fpdf2 doesn't support Unicode characters like em dashes. I'll switch the PDF generator to use DejaVu Sans, which ships with fpdf2 and has full Unicode support.

Let me check the actual font path so this doesn't break if the venv path differs.

fpdf2 doesn't bundle DejaVu fonts as files. Instead, I should use `fpdf2`'s built-in `add_font` with a system font or use a different approach. Let me use the `uni=True` approach with a system font that's guaranteed on macOS.

`Arial Unicode.ttf` is perfect -- full Unicode coverage and available on macOS. Let me also check for a bold variant, but even just using the regular file for both will work.

Now the app will reload automatically since Streamlit detects file changes. Refresh the page and try the PDF export again -- it will now use Arial Unicode which fully supports em dashes, curly quotes, and all other Unicode characters in your analysis results.

---

**User**

Now I'm getting the following error when trying to export:

streamlit.errors.StreamlitAPIException: Invalid binary data format: <class 'bytearray'>

File "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool/app.py", line 438, in <module>
    st.download_button("⬇ Download", data=gen_pdf(entry), file_name=f"benchmark_{exp_doc.rsplit('.',1)[0]}.pdf", mime="application/pdf", key="dl_pdf")
    ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/streamlit/runtime/metrics_util.py", line 532, in wrapped_func
    result = non_optional_func(*args, **kwargs)
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/streamlit/elements/widgets/button.py", line 771, in download_button
    return self._download_button(
           ~~~~~~~~~~~~~~~~~~~~~^
        label=label,
        ^^^^^^^^^^^^
    ...<14 lines>...
        shortcut=shortcut,
        ^^^^^^^^^^^^^^^^^^
    )
    ^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/streamlit/elements/widgets/button.py", line 1228, in _download_button
    marshall_file(
    ~~~~~~~~~~~~~^
        self.dg._get_delta_path_str(), data, download_button_proto, mime, file_name
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    )
    ^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/streamlit/elements/widgets/button.py", line 1560, in marshall_file
    data_as_bytes, inferred_mime_type = convert_data_to_bytes_and_infer_mime(
                                        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        data,
        ^^^^^
    ...<2 lines>...
        ),
        ^^
    )
    ^
File "/Library/Frameworks/Python.framework/Versions/3.13/lib/python3.13/site-packages/streamlit/runtime/download_data_util.py", line 51, in convert_data_to_bytes_and_infer_mime
    raise unsupported_error

---

**Cursor**

Streamlit's `download_button` expects `bytes`, but `FPDF.output()` returns a `bytearray`. Quick fix:

Refresh the page and try the export again -- `pdf.output()` returns a `bytearray` which Streamlit doesn't accept, so wrapping it in `bytes()` resolves it.

---

**User**

There is no colour contrast on the sign out button in light mode.

I want to be able to change my name, email address and password in a profile editor.

I want the session to keep me logged in.

---

**Cursor**

Now let me read the auth and DB modules to add the profile update functions.

Now I have the full picture. I need to:

1. Add a `sessions` table + `update_user` + `change_password` to the DB layer
2. Add session persistence via a token stored in a local file
3. Fix sign-out button contrast in CSS
4. Add a profile editor in the sidebar
5. Wire up session persistence in `app.py`

Now I'll update `app.py` with all three remaining changes together: button contrast fix, profile editor, and persistent sessions.

Now fix the sidebar button contrast:

Now replace the session state init and auth gate to add persistent sessions, and the sidebar to include the profile editor:

Now update `show_login` to persist the session token on login:

Update `show_register` similarly:

Now update the auth gate to auto-load the library after session restore:

Now replace the sidebar with the sign-out fix and profile editor:

Add `.session_token` to gitignore:

Now let me verify the app restarts cleanly:

The app is back up. Here's what changed:

**Sign-out button contrast** -- Sidebar buttons now have a white background with dark navy text and a subtle border, providing clear contrast against the dark sidebar in both light and dark modes.

**Profile editor** -- Click the "Profile" button next to "Sign out" in the sidebar to expand a profile panel where you can:
- Edit your **name** and **email** (with a Save button)
- Change your **password** (current + new + confirm, with validation)
- Click "Close profile" to collapse it

**Persistent session** -- When you log in or register, a cryptographically random session token is created in the database and written to `data/.session_token`. On every page load/refresh, the app checks for this file and automatically restores your session without requiring you to sign in again. Signing out destroys the token from both the database and the file.

Refresh the page at **http://localhost:8501** to try it out. If you were previously logged in you'll need to register once more (the DB schema was extended with a new `sessions` table), and after that refreshing the page will keep you signed in.

---

**User**

Can you create a "forgot password" functionality?

---

**Cursor**

I'll add a forgot-password flow with a time-limited reset code. Since this is a local tool without an email server, the code will be displayed on-screen (in production it would be emailed).

Now let me read the login screen section in app.py to see exactly where to add the "Forgot password" link.

Now I'll add the reset code functions to the DB layer and the forgot-password screen to the app. First, the DB table and functions:

Now add the reset functions at the end of auth.py:

Update the `__init__.py` exports:

Now update `app.py` -- add the imports, the forgot-password screen, and a "Forgot password?" link on the login page:

Now add a "Forgot password?" button to the login screen and create the forgot-password screen. Replace the login function to add the link, and add the new screen after `show_register`:

Now add the forgot-password screen right after `show_register`:

Now add the auth gate for the "forgot" page:

The app will auto-reload. Here's how the forgot-password flow works:

**Step 1** -- On the login screen, click "Forgot password?" and enter your registered email. A 6-digit reset code is generated and stored in the database with a 15-minute expiry.

**Step 2** -- The code is displayed on-screen (in production this would be emailed). Enter the code along with your new password and confirmation.

**Step 3** -- Once verified, your password is updated and the code is marked as used. You're taken back to sign in with your new credentials.

The flow includes validation for expired codes, incorrect codes, password length, and password confirmation mismatch. Each code is single-use and expires after 15 minutes.

---

**User**

push to github and make it live

---

**Cursor**

There are two blockers. Git requires the Xcode license to be accepted, and the GitHub CLI (`gh`) isn't installed. Let me check what's available:

Git is installed but blocked by the Xcode license. I need you to run two commands in your terminal first:

**1. Accept the Xcode license** (requires your password):
```bash
sudo xcodebuild -license accept
```

**2. Install the GitHub CLI**:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then:
```bash
brew install gh
gh auth login
```

Alternatively, if you already have Homebrew installed elsewhere, just run `brew install gh && gh auth login`.

Once those two steps are done, let me know and I'll handle the rest -- initialising the repo, creating it on GitHub, pushing all the code, and setting it up for Streamlit Cloud deployment.

---

**User**

sudo xcodebuild -license accept

---

**Cursor**

That command requires your admin password, so it needs to be run directly in your local terminal -- I can't enter passwords from here.

Please open **Terminal.app** (or your preferred terminal) and run:

```bash
sudo xcodebuild -license accept
```

It will ask for your Mac password. Once that's done, come back and let me know -- I'll then be able to use git from here.

For the GitHub CLI, you'll also need to run these in your terminal:

```bash
brew install gh
gh auth login
```

(If Homebrew isn't installed yet, install it first with the command from my previous message.)

Once both are ready, I'll handle the repo creation, commit, push, and deployment setup.

---

**User**

I'm getting the following error in Terminal

/private/etc/sudoers:65:5: syntax error
 ALL=(ALL) NOPASSWD: /bin/mkdir
    ^
/private/etc/sudoers:66:5: syntax error
 ALL=(ALL) NOPASSWD: /usr/sbin/chown
    ^
/private/etc/sudoers:67:5: syntax error
 ALL=(ALL) NOPASSWD: /usr/bin/cat
    ^
/private/etc/sudoers:68:5: syntax error
 ALL=(ALL) NOPASSWD: /usr/bin/touch
    ^
/private/etc/sudoers:69:5: syntax error
 ALL=(ALL) NOPASSWD: /bin/launchctl
    ^
Password:
Sorry, try again.
Password:
Sorry, try again.
Password:
sudo: 3 incorrect password attempts


[Process completed]



---

**Cursor**

Your `/etc/sudoers` file has syntax errors -- lines 65-69 are missing a username before `ALL=(ALL)`. This is a system-level issue that's breaking all `sudo` commands. That's separate from our task but important to fix.

**To fix the sudoers file** (requires Recovery Mode since `sudo` itself is broken):

1. Restart your Mac
2. **Apple Silicon**: Hold the power button until "Loading startup options" appears, then select **Options**
3. **Intel Mac**: Hold **Cmd + R** during boot
4. In Recovery Mode, open **Terminal** from the Utilities menu
5. Run:
```bash
csrutil disable
mount -uw /
visudo -f /Volumes/Macintosh\ HD/private/etc/sudoers
```
6. Fix lines 65-69 by adding your username before `ALL=`, e.g.:
```
earl.petersen ALL=(ALL) NOPASSWD: /bin/mkdir
```
Or simply delete those 5 lines if you don't need them.
7. Save, re-enable SIP with `csrutil enable`, and restart.

---

**In the meantime**, let's see if git actually works without the Xcode license acceptance -- sometimes basic operations still function:

Git is fully blocked. Let me check if there's an alternative git binary available:

Unfortunately git is completely blocked by the Xcode license, and there's no alternative installation. Since `sudo` is also broken, we're stuck on both fronts.

Here are your options, from quickest to most thorough:

**Option A -- Quick workaround (no Recovery Mode needed):**
Open Terminal and run this to accept the license without `sudo`:
```bash
/usr/bin/xcodebuild -license accept
```
It *might* work without sudo if you're already an admin. Worth trying.

**Option B -- Install a standalone git via conda/pip:**
```bash
python3 -m pip install dulwich
```
This gives us a pure-Python git implementation, but it's limited.

**Option C -- Fix sudoers in Recovery Mode** (recommended):
Follow the steps above, then run `sudo xcodebuild -license accept`, and we'll have full git + GitHub access.

Which would you like to try? Option C is the cleanest path since it also fixes your broken `sudo` for everything else on your system.

---

**User**

I just added a new repository in my github library

https://github.com/kurtosys-earlpetersen/document_analysis 

---

**Cursor**

Great, the repo is created. Let me try git again to see if we can push to it:

Git is working now. Let me get everything committed and pushed.

There are some files that don't belong in this project (the PDF, the HTML file, the SQL file, the echarts markdown). Let me update the gitignore and only commit relevant project files:

Clean set of files. Now let me commit and push:

Git needs authentication to push. Since the GitHub CLI isn't installed, you'll need to push from your terminal. The repo is fully committed and ready -- just run these two commands in **Terminal.app**:

```bash
cd "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool"
git push -u origin main
```

It will prompt you for your GitHub credentials. If you use two-factor auth, you'll need a [Personal Access Token](https://github.com/settings/tokens) as the password (GitHub no longer accepts account passwords for git operations).

**To create a token:**
1. Go to https://github.com/settings/tokens
2. Click **Generate new token (classic)**
3. Select scopes: `repo` (full control)
4. Copy the token and use it as your password when git prompts

Once pushed, let me know and I'll set up the Streamlit Cloud deployment to make it live.

---

**User**

No password was required for terminal run:

/usr/bin/cd: line 4: cd: "/Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool": No such file or directory

[Process completed]



---

**Cursor**

The quotes are being interpreted differently in your terminal. Try without the outer quotes -- the path needs escaping with backslashes instead:

```bash
cd /Users/earl.petersen/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool
```

Then:

```bash
git push -u origin main
```

If the `cd` still fails, the OneDrive path may have a slightly different name on disk. You can find it with:

```bash
ls /Users/earl.petersen/Library/CloudStorage/
```

That will show you the exact folder name to use.

---

**User**

OneDrive-Kurtosys
OneDrive-SharedLibraries-OneDriveCloudTemp

[Process completed]






















---

**Cursor**

Good, the OneDrive folder name is correct. Now try this in your terminal -- paste each line one at a time:

```bash
cd ~/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool
```

Then:

```bash
git push -u origin main
```

Using `~/` instead of the full `/Users/earl.petersen/` path avoids any copy-paste issues with special characters.

---

**User**

Not sure what I'm doing wrong here:

Last login: Mon Mar 23 09:54:33 on ttys007
earl.petersen@PetersenMP1-16W46G ~ % cd ~/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool
earl.petersen@PetersenMP1-16W46G Document_analysis_tool % git push -u origin main
Username for 'https://github.com': earl.petersen@kurtosys.com
Password for 'https://earl.petersen%40kurtosys.com@github.com': 
remote: Invalid username or token. Password authentication is not supported for Git operations.
fatal: Authentication failed for 'https://github.com/kurtosys-earlpetersen/document_analysis.git/'
earl.petersen@PetersenMP1-16W46G Document_analysis_tool % 

---

**Cursor**

You're doing everything right -- GitHub just no longer accepts passwords for git pushes. You need a Personal Access Token instead. Here's how:

1. Go to **https://github.com/settings/tokens** in your browser
2. Click **"Generate new token"** (choose **Classic**)
3. Give it a name like "document-analysis"
4. Set expiration to whatever you prefer (e.g. 90 days)
5. Check the **`repo`** scope (full control of private repositories)
6. Click **Generate token**
7. **Copy the token** (it starts with `ghp_...`)

Then back in your terminal, run `git push -u origin main` again:

- **Username**: `kurtosys-earlpetersen` (your GitHub username, not your email)
- **Password**: paste the token you just copied (it won't show characters as you paste -- that's normal)

```bash
git push -u origin main
```

---

**User**

Now I'm getting the following error:

remote: Permission to kurtosys-earlpetersen/document_analysis.git denied to kurtosys-earlpetersen.
fatal: unable to access 'https://github.com/kurtosys-earlpetersen/document_analysis.git/': The requested URL returned error: 403
earl.petersen@PetersenMP1-16W46G Document_analysis_tool % 

---

**Cursor**

This is likely caused by macOS caching old credentials in Keychain, or the token not having the right scope. Let's fix both:

**Step 1 -- Clear cached credentials.** Run this in your terminal:

```bash
git credential-osxkeychain erase
```

Then type these two lines and press Enter twice (the second Enter on an empty line):

```
host=github.com
protocol=https

```

**Step 2 -- Try pushing again:**

```bash
git push -u origin main
```

When prompted, enter:
- **Username**: `kurtosys-earlpetersen`
- **Password**: your token (the `ghp_...` one)

If it still fails with 403, the token likely needs the right scope. Go back to https://github.com/settings/tokens and verify:

1. The token has the **`repo`** checkbox ticked (not just sub-items, the top-level `repo` box)
2. If `kurtosys-earlpetersen` is an **organization** account, you may also need to click **"Configure SSO"** next to the token and authorize it for that org

If none of that works, try creating a **fine-grained token** instead:
1. https://github.com/settings/tokens?type=beta
2. Under **Repository access**, select **"Only select repositories"** and pick `document_analysis`
3. Under **Permissions > Repository permissions**, set **Contents** to **Read and write**
4. Generate and use that token

---

**User**

I think I got it:

Enumerating objects: 44, done.
Counting objects: 100% (44/44), done.
Delta compression using up to 10 threads
Compressing objects: 100% (43/43), done.
Writing objects: 100% (44/44), 39.19 KiB | 4.90 MiB/s, done.
Total 44 (delta 2), reused 0 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (2/2), done.
To https://github.com/kurtosys-earlpetersen/document_analysis.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
earl.petersen@PetersenMP1-16W46G Document_analysis_tool % 

---

**Cursor**

The code is now live on GitHub at **https://github.com/kurtosys-earlpetersen/document_analysis**.

To make the app publicly accessible, the easiest option for a Streamlit app is **Streamlit Community Cloud** (free). Here's how to deploy it:

1. Go to **https://share.streamlit.io**
2. Sign in with your GitHub account (`kurtosys-earlpetersen`)
3. Click **"New app"**
4. Select:
   - **Repository**: `kurtosys-earlpetersen/document_analysis`
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **Deploy**

Streamlit Cloud will install the dependencies from `requirements.txt` automatically and give you a public URL like `https://document-analysis-kurtosys.streamlit.app`.

One thing to note: the PDF export uses macOS system fonts (`Arial Unicode.ttf`) which won't exist on the cloud server. Let me add a fallback so it works everywhere:

I need to sanitize Unicode characters when falling back to Helvetica so the cloud deploy won't crash on em dashes etc:

Now wrap all the text outputs in the PDF with the sanitizer:

Now push the update. Let me try using the token in the remote URL this time:

The commit is ready. Since git can't authenticate from here, push it from your terminal again:

```bash
cd ~/Library/CloudStorage/OneDrive-Kurtosys/Kurtosys-Clients/Miscellaneous/Document_analysis_tool
git push
```

It should use your cached credentials this time so no username/password prompt.

After that, to deploy on Streamlit Cloud:

1. Go to **https://share.streamlit.io**
2. Sign in with your GitHub account
3. Click **"New app"**
4. Pick repo `kurtosys-earlpetersen/document_analysis`, branch `main`, file `app.py`
5. Click **Deploy**

You'll get a public URL within a couple of minutes.

You're on the right page. Now look for a **"Create app"** or **"New app"** button -- it should be in the top-right corner of that page. Click it and you'll see a form where you fill in:

- **Repository**: `kurtosys-earlpetersen/document_analysis`
- **Branch**: `main`
- **Main file path**: `app.py`

Then click **Deploy**.

If you don't see a "Create app" button, make sure you signed into Streamlit Cloud with the same GitHub account (`kurtosys-earlpetersen`) that owns the repository. You may need to grant Streamlit access to your GitHub repos when prompted.

---

**User**

I've done all of that already.

---

**Cursor**

Got it -- so after you filled in the repo/branch/file and clicked Deploy, did you get an error or did it just return you to the "My apps" page showing no apps?

If the deploy didn't start, it's likely a permissions issue. Try this:

1. Go to **https://share.streamlit.io** and click your profile icon (top right)
2. Go to **Settings**
3. Under **GitHub**, check if it shows your `kurtosys-earlpetersen` account as connected
4. If it says "No repositories", click **"Manage permissions"** -- this will take you to GitHub where you need to grant Streamlit access to the `document_analysis` repository

Alternatively, if the `kurtosys-earlpetersen` account is an **organization** account (not a personal one), Streamlit Cloud free tier only supports personal accounts. In that case you'd need to either:

- **Fork the repo** to a personal GitHub account and deploy from there
- Or deploy using a different hosting option like **Render** or **Railway** which support org accounts

Would you like me to walk you through an alternative deployment option?

---

**User**

Could it be that the deployment is simply in limbo and I have to wait a bit longer for the app to display?

---

**Cursor**

Your GitHub account is connected and the repo is public, so permissions look fine. It could be that the deploy is still building -- Streamlit Cloud can take 3-5 minutes to install dependencies and boot the app for the first time.

But if you already clicked Deploy and it just sent you back to the empty "My apps" page with no progress indicator or app card at all, then the deploy likely didn't register. Try again:

1. Close the settings panel
2. Click **"New app"** (top right of the "My apps" page)
3. Fill in:
   - **Repository**: `kurtosys-earlpetersen/document_analysis`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **Deploy**

You should then see a new app card appear on the "My apps" page with a spinning/building status. If you see that, just wait a few minutes for it to finish.

If the repo doesn't appear in the repository dropdown, click **"Connect here"** under the **Private access** section in your settings screenshot -- even though the repo is public, granting full access can sometimes fix visibility issues with the repo picker.

---

**User**

Can I make change requests here and it will push directly to github and streamlit?

---

**Cursor**

Yes, almost. Here's how the flow works:

1. **You request changes here** in Cursor -- I make the edits
2. **I commit** the changes via git
3. **You push** from your terminal with `git push` (one command)
4. **Streamlit Cloud auto-redeploys** whenever it sees new commits on `main` -- no manual action needed

So the only manual step is running `git push` in your terminal after I commit. Let me check if I can push directly from here now that your credentials are cached:

Even better -- your credentials are cached, so I **can** push directly from here. That means the full flow is seamless:

1. **You request a change** in this chat
2. **I edit, commit, and push** -- all automatic
3. **Streamlit Cloud redeploys** within a couple of minutes

No manual steps needed on your end. Go ahead and request any changes you'd like.

---

**User**

Use this palette for the UI design.

---

**Cursor**

The palette constants already match your colour swatch exactly. Let me verify the full set including greens and accent colours:

The palette is already using your exact colours:

| Your swatch | Variable | Value | Used for |
|---|---|---|---|
| blue/600 | `B6` | `#071935` | Sidebar bg, headings, dark text |
| blue/500 | `B5` | `#0342E4` | Active tabs, primary buttons, links |
| slate/400 | `S4` | `#3A4051` | Secondary text, labels |
| slate/300 | `S3` | `#4A5267` | Muted text, descriptions |
| grey/400 | `G4` | `#B0B8CB` | Captions, subtle icons |
| grey/300 | `G3` | `#C3C9D9` | Borders, dividers |
| white/100 | `W` | `#FFFFFF` | Cards, inputs, backgrounds |
| green/500 | `GR5` | `#2E7D32` | Strength indicators |
| green/400 | `GR4` | `#00C761` | Pass badges, positive scores |

However, the greens in your swatch are slightly different from what's currently set. Let me check -- your image shows green/500 as `#2E7D32` and green/400 as `#00C761`. Those match exactly.

The current `RED` (`#D32F2F`) and `AMB` (`#F59E0B`) aren't in your palette image but are functional colours for fail/warning states. I'll keep those as they serve accessibility purposes.

Now let me do a thorough check that the palette is consistently applied everywhere in the CSS -- some areas might still have hardcoded colours that don't match:

I can see some hardcoded colours that should be brought into the palette system. Let me clean these up -- replacing the off-palette purples and teals with palette-consistent alternatives, and tightening up the light tint colours:

Now replace the hardcoded hex values in the CSS and code with palette variables:

Now replace the off-palette purple and teal in the pillar colours with palette-derived colours:

Now commit and push:

Done -- committed and pushed. Every colour in the UI now comes exclusively from your brand palette:

| Swatch | Hex | Usage |
|---|---|---|
| **blue/600** | `#071935` | Sidebar, headings, dark text, header gradient |
| **blue/500** | `#0342E4` | Active tabs, primary buttons, recommendation cards, pillar bars |
| **slate/400** | `#3A4051` | Secondary text, labels, "major" severity badges, consistency pillar |
| **slate/300** | `#4A5267` | Muted descriptions, captions |
| **grey/400** | `#B0B8CB` | Icons, subtle labels, data integrity pillar |
| **grey/300** | `#C3C9D9` | Borders, dividers, card outlines |
| **white/100** | `#FFFFFF` | Card backgrounds, inputs, sidebar buttons |
| **green/500** | `#2E7D32` | Strength card text |
| **green/400** | `#00C761` | Pass badges, positive scores, compliance pillar |

The red (`#D32F2F`) and amber (`#F59E0B`) are kept as functional status colours only (fail/warning). If your Streamlit Cloud app is deployed, it will auto-redeploy with these changes in a couple of minutes.

---

**User**

Put the "Peer benchmark set" content in a single column

---

**Cursor**

Done -- the peer benchmark set now lists all 10 firms in a single column in the sidebar. Committed and pushed.

---

**User**

Please look at the style, look and feel of the attachement and match my UI design accordingly.

---

**Cursor**

Now let me also see the header and sidebar sections of the main app layout:

Now I have a clear picture. The Aurora dashboard style has: white sidebar, soft shadows instead of borders, large rounded cards, airy spacing, subtle active-state styling, and a clean flat look. Let me overhaul the CSS to match.

Now update the header banner to match the Aurora style -- cleaner, less gradient-heavy:

Now update the empty-state upload card to use shadow instead of dashed border:

Now commit and push:

Done -- committed and pushed. Here's what changed to match the Aurora dashboard style:

**Sidebar** -- Switched from dark navy to a clean white background with a subtle right border, matching Aurora's light sidebar. Text is now dark navy/slate, buttons transition to blue on hover.

**Cards** -- All cards (hero metrics, dimension pills, findings, taxonomy tiles, BSC) now use soft `box-shadow` instead of hard `1px solid` borders. Border radius increased to 20-24px for the rounded, modern feel. Hero cards and dimension pills have a subtle lift effect on hover.

**Tabs** -- Pill-style with a shadow container instead of a bordered one. Active tab uses the dark navy (`#071935`) with a subtle shadow, matching Aurora's active nav style.

**Header** -- Replaced the gradient banner with a clean white card showing "Dashboard" with a breadcrumb subtitle and a user badge on the right, matching Aurora's top bar.

**Auth screens** -- Login/register cards now have a deeper shadow and no border for a floating card feel.

**Overall** -- More whitespace, larger padding, smoother transitions. The design feels airy and spacious like the Aurora reference.

