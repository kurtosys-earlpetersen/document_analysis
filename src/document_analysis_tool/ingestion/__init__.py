"""Document ingestion: detect type and delegate to the right parser."""

from pathlib import Path

from .models import ExtractedDocument
from .pdf_parser import parse_pdf
from .docx_parser import parse_docx

SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def get_parser(path: Path):
    """Return parser function for the given path, or None if unsupported."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        return parse_pdf
    if ext == ".docx":
        return parse_docx
    return None


def ingest(path: Path) -> ExtractedDocument | None:
    """Ingest a document from path. Returns ExtractedDocument or None if unsupported."""
    path = Path(path)
    if not path.is_file():
        return None
    parser = get_parser(path)
    if not parser:
        return None
    return parser(path)
