from dataclasses import dataclass
from typing import Callable


@dataclass
class SortOption:
    """Represents a sorting option with an identifier, label, and action callback."""

    identifier: str
    label: str
    on_click: Callable[[], None]
