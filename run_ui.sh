#!/usr/bin/env bash
# Run the Document Analysis Tool UI (Streamlit).
# Install deps first: pip install -r requirements.txt (or use a venv and install there)

cd "$(dirname "$0")"
if [[ -d .venv ]]; then
  source .venv/bin/activate
fi
# Use same python that we run with, so deps must be installed there
if ! python3 -c "import docx, fitz, streamlit" 2>/dev/null; then
  echo "Missing dependencies. Run: pip install -r requirements.txt"
  exit 1
fi
python3 -m streamlit run app.py
