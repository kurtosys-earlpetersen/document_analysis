"""Shared models for extracted document content and structure."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class Block:
    """A logical block of content (heading, paragraph, list, table)."""
    kind: str  # "heading", "paragraph", "list", "table", "image"
    level: int | None = None  # heading level 1–6
    text: str = ""
    alt_text: str | None = None  # for images
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractedDocument:
    """Result of parsing a document: text, structure, metadata."""
    path: Path
    format: str  # "pdf" | "docx"
    title: str = ""
    language: str = ""
    raw_text: str = ""
    blocks: list[Block] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def has_structure(self) -> bool:
        return len(self.blocks) > 0

    def get_headings(self) -> list[Block]:
        return [b for b in self.blocks if b.kind == "heading"]

    def get_images(self) -> list[Block]:
        return [b for b in self.blocks if b.kind == "image"]
