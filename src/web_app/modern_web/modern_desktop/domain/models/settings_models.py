"""
Immutable domain models for settings data.

Following TKA's clean architecture patterns with frozen dataclasses and .update() methods.
These models represent settings data without any UI coupling.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Optional

from desktop.modern.domain.models.enums import BackgroundType, GridMode, PropType


@dataclass(frozen=True)
class UserProfileData:
    """Immutable user profile data."""

    name: str
    created_at: Optional[str] = None
    last_used: Optional[str] = None
    preferences: dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs) -> UserProfileData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)


@dataclass(frozen=True)
class VisibilitySettingsData:
    """Immutable visibility settings data."""

    # Glyph visibility
    tka_visible: bool = True
    reversals_visible: bool = True
    vtg_visible: bool = True
    elemental_visible: bool = True
    positions_visible: bool = True

    # Motion visibility
    red_motion_visible: bool = True
    blue_motion_visible: bool = True

    # Special elements
    non_radial_visible: bool = True

    def update(self, **kwargs) -> VisibilitySettingsData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)

    def get_glyph_visibility(self, glyph_name: str) -> bool:
        """Get visibility for a specific glyph type."""
        glyph_map = {
            "TKA": self.tka_visible,
            "Reversals": self.reversals_visible,
            "VTG": self.vtg_visible,
            "Elemental": self.elemental_visible,
            "Positions": self.positions_visible,
            "Red Motion": self.red_motion_visible,
            "Blue Motion": self.blue_motion_visible,
            "Non-radial": self.non_radial_visible,
        }
        return glyph_map.get(glyph_name, True)


@dataclass(frozen=True)
class BeatLayoutData:
    """Immutable beat layout configuration data."""

    rows: int = 4
    cols: int = 4
    grow_sequence: bool = True
    auto_adjust: bool = True

    def update(self, **kwargs) -> BeatLayoutData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)

    @property
    def total_beats(self) -> int:
        """Calculate total beats for this layout."""
        return self.rows * self.cols


@dataclass(frozen=True)
class ImageExportSettingsData:
    """Immutable image export settings data."""

    include_start_position: bool = True
    add_beat_numbers: bool = True
    add_reversal_symbols: bool = True
    add_user_info: bool = True
    add_word: bool = True
    add_difficulty_level: bool = True
    combined_grids: bool = False
    quality: int = 95

    def update(self, **kwargs) -> ImageExportSettingsData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)


@dataclass(frozen=True)
class CodexExportSettingsData:
    """Immutable codex export settings data."""

    red_turns: float = 1.0
    blue_turns: float = 0.0
    grid_mode: GridMode = GridMode.DIAMOND
    generate_all: bool = False
    quality: int = 95
    include_metadata: bool = True

    def update(self, **kwargs) -> CodexExportSettingsData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)


@dataclass(frozen=True)
class GlobalSettingsData:
    """Immutable global application settings data."""

    # Core settings
    prop_type: PropType = PropType.STAFF
    grid_mode: GridMode = GridMode.DIAMOND
    background_type: BackgroundType = BackgroundType.AURORA

    # UI settings
    show_grid: bool = True
    enable_fades: bool = False
    animation_speed: float = 1.0

    # Application behavior
    auto_save: bool = True
    grow_sequence: bool = True
    show_welcome_screen: bool = False

    # Current state
    current_tab: str = "construct"
    current_settings_dialog_tab: str = "General"

    def update(self, **kwargs) -> GlobalSettingsData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)


@dataclass(frozen=True)
class SettingsData:
    """Immutable complete settings data."""

    # Core settings
    global_settings: GlobalSettingsData = field(default_factory=GlobalSettingsData)

    # User management
    current_user: str = "Default User"
    user_profiles: dict[str, UserProfileData] = field(default_factory=dict)

    # Tab-specific settings
    visibility: VisibilitySettingsData = field(default_factory=VisibilitySettingsData)
    beat_layouts: dict[int, BeatLayoutData] = field(
        default_factory=dict
    )  # keyed by sequence length
    image_export: ImageExportSettingsData = field(
        default_factory=ImageExportSettingsData
    )
    codex_export: CodexExportSettingsData = field(
        default_factory=CodexExportSettingsData
    )

    # Custom settings
    custom_settings: dict[str, Any] = field(default_factory=dict)

    def update(self, **kwargs) -> SettingsData:
        """Create a new instance with updated values."""
        return replace(self, **kwargs)

    def get_beat_layout(self, sequence_length: int) -> BeatLayoutData:
        """Get beat layout for a specific sequence length."""
        if sequence_length in self.beat_layouts:
            return self.beat_layouts[sequence_length]

        # Calculate default layout
        import math

        sqrt_len = int(math.sqrt(sequence_length))
        rows = sqrt_len
        cols = math.ceil(sequence_length / rows)

        return BeatLayoutData(rows=rows, cols=cols)

    def set_beat_layout(
        self, sequence_length: int, layout: BeatLayoutData
    ) -> SettingsData:
        """Set beat layout for a specific sequence length."""
        new_layouts = self.beat_layouts.copy()
        new_layouts[sequence_length] = layout
        return self.update(beat_layouts=new_layouts)

    def add_user_profile(self, name: str, profile: UserProfileData) -> SettingsData:
        """Add a new user profile."""
        new_profiles = self.user_profiles.copy()
        new_profiles[name] = profile
        return self.update(user_profiles=new_profiles)

    def remove_user_profile(self, name: str) -> SettingsData:
        """Remove a user profile."""
        if name not in self.user_profiles or len(self.user_profiles) <= 1:
            return self  # Don't remove if it's the only profile

        new_profiles = self.user_profiles.copy()
        del new_profiles[name]

        # If we removed the current user, switch to the first available
        current_user = self.current_user
        if current_user == name:
            current_user = next(iter(new_profiles.keys()))

        return self.update(user_profiles=new_profiles, current_user=current_user)


# Default settings instance
DEFAULT_SETTINGS = SettingsData()
