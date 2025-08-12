from __future__ import annotations
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional,Optional

from enums.letter.letter import Letter


@dataclass(frozen=True)
class DeterminationResult:
    letter: Letter | None
    matched_attributes: dict[str, str]
