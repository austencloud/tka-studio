from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any


class PropType(Enum):
    STAFF = "Staff"
    CLUB = "Club"
    FAN = "Fan"
    BUUGENG = "Buugeng"
    SWORD = "Sword"
    GUITAR = "Guitar"
    UKULELE = "Ukulele"


class IUserProfileService(ABC):
    @abstractmethod
    def get_current_user(self) -> str:
        pass

    @abstractmethod
    def set_current_user(self, user: str) -> None:
        pass

    @abstractmethod
    def get_all_users(self) -> list[str]:
        pass


class IPropTypeSettingsManager(ABC):
    @abstractmethod
    def get_current_prop_type(self) -> PropType:
        pass

    @abstractmethod
    def set_prop_type(self, prop_type: PropType) -> None:
        pass

    @abstractmethod
    def get_available_prop_types(self) -> list[PropType]:
        pass


class IVisibilitySettingsManager(ABC):
    @abstractmethod
    def get_glyph_visibility(self, glyph_name: str) -> bool:
        pass

    @abstractmethod
    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        pass

    @abstractmethod
    def get_motion_visibility(self, color: str) -> bool:
        pass

    @abstractmethod
    def set_motion_visibility(self, color: str, visible: bool) -> None:
        pass


class IVisibilityService(ABC):
    """Unified interface for visibility management operations."""

    @abstractmethod
    def get_glyph_visibility(self, glyph_name: str) -> bool:
        """Get visibility state for a specific glyph."""

    @abstractmethod
    def set_glyph_visibility(self, glyph_name: str, visible: bool) -> None:
        """Set visibility state for a specific glyph."""

    @abstractmethod
    def get_motion_visibility(self, color: str) -> bool:
        """Get visibility state for motion by color."""

    @abstractmethod
    def set_motion_visibility(self, color: str, visible: bool) -> None:
        """Set visibility state for motion by color."""

    @abstractmethod
    def toggle_glyph_visibility(self, glyph_name: str) -> bool:
        """Toggle glyph visibility and return new state."""

    @abstractmethod
    def toggle_motion_visibility(self, color: str) -> bool:
        """Toggle motion visibility and return new state."""


class IBeatLayoutService(ABC):
    @abstractmethod
    def get_layout_for_length(self, length: int) -> tuple[int, int]:
        pass

    @abstractmethod
    def set_layout_for_length(self, length: int, rows: int, cols: int) -> None:
        pass


class IImageExporter(ABC):
    @abstractmethod
    def get_export_option(self, option: str) -> Any:
        pass

    @abstractmethod
    def set_export_option(self, option: str, value: Any) -> None:
        pass

    @abstractmethod
    def get_all_export_options(self) -> dict[str, Any]:
        pass
