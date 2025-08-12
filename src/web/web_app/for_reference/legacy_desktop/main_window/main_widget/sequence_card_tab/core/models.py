from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional,Optional


@dataclass
class SequenceCardData:
    """Immutable data structure for sequence card information."""

    path: Path
    word: str
    length: int
    metadata: dict[str, Any]
    thumbnail_path: Path | None = None
    high_res_path: Path | None = None


@dataclass
class ImageLoadRequest:
    """Data structure for image loading requests."""

    path: str
    word: str
    sequence_file: str
    metadata: dict[str, Any]
    priority: int = 0
    callback: callable | None = None


@dataclass
class SequenceCardBatch:
    """Data structure for batched sequence card processing."""

    sequences: list[dict[str, Any]]
    batch_size: int
    start_index: int
    end_index: int
    total_count: int
