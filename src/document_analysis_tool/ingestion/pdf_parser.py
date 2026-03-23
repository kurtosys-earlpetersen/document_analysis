"""PDF extraction using PyMuPDF."""

from pathlib import Path

import fitz

from .models import Block, ExtractedDocument


def parse_pdf(path: Path) -> ExtractedDocument:
    doc = fitz.open(path)
    blocks: list[Block] = []
    raw_chunks: list[str] = []

    for page in doc:
        for block in page.get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line.get("spans", []):
                    text = span.get("text", "").strip()
                    if not text:
                        continue
                    raw_chunks.append(text)
                    # Heuristic: treat short, bold or large text as heading
                    font_size = span.get("size", 0)
                    flags = span.get("flags", 0)
                    is_bold = bool(flags & 2**4)
                    if len(text) < 120 and (font_size > 12 or is_bold):
                        level = 1 if font_size >= 14 else 2
                        blocks.append(Block(kind="heading", level=level, text=text))
                    else:
                        blocks.append(Block(kind="paragraph", text=text))

        # Images
        for img in page.get_images():
            xref = img[0]
            blocks.append(Block(kind="image", metadata={"xref": xref}))

    raw_text = "\n".join(raw_chunks)
    page_count = len(doc)
    doc.close()

    return ExtractedDocument(
        path=path,
        format="pdf",
        raw_text=raw_text,
        blocks=blocks,
        metadata={"page_count": page_count},
    )
