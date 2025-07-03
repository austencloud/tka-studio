"""
JSON Configuration Service

Pure service for loading and managing JSON configuration data.
Extracted from PropManagementService to follow single responsibility principle.

PROVIDES:
- Special placements JSON loading
- Configuration file path resolution
- JSON parsing and error handling
- Override key generation
"""

from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import json
import time
import logging
from pathlib import Path

from domain.models.core_models import BeatData


class IJSONConfigurationService(ABC):
    """Interface for JSON configuration operations."""

    @abstractmethod
    def load_special_placements(self) -> Dict[str, Any]:
        """Load special placement data from JSON configuration files."""

    @abstractmethod
    def generate_override_key(self, beat_data: BeatData) -> str:
        """Generate key for swap override lookup."""

    @abstractmethod
    def has_swap_override(self, beat_data: BeatData) -> bool:
        """Check if beat has manual swap override in special placements."""

    @abstractmethod
    def get_swap_override_data(self, beat_data: BeatData) -> Dict[str, Any]:
        """Get swap override data for beat."""


class JSONConfigurationService(IJSONConfigurationService):
    """
    Pure service for JSON configuration operations.

    Handles all JSON file I/O and configuration management without external dependencies.
    Uses immutable data patterns following TKA architecture.
    """

    def __init__(self, config_paths: Optional[list] = None):
        """Initialize with optional custom configuration paths and eager loading."""
        start_time = time.time()
        logger = logging.getLogger(__name__)

        self._config_paths = config_paths or self._get_default_config_paths()
        self._special_placements: Optional[Dict[str, Any]] = None

        # Eager load special placements during initialization
        self._load_special_placements()

        load_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        placement_count = len(self._special_placements or {})
        logger.info(
            f"JSON Configuration Service initialized: {placement_count} placements loaded in {load_time:.1f}ms"
        )

    def load_special_placements(self) -> Dict[str, Any]:
        """Load special placement data from JSON configuration files."""
        if self._special_placements is not None:
            return self._special_placements

        self._load_special_placements()
        return self._special_placements or {}

    def generate_override_key(self, beat_data: BeatData) -> str:
        """
        Generate key for swap override lookup.

        Based on validated logic for special placement keys.
        """
        if not beat_data.blue_motion or not beat_data.red_motion:
            return ""

        blue_type = beat_data.blue_motion.motion_type.value
        red_type = beat_data.red_motion.motion_type.value
        letter = beat_data.letter or ""

        # Generate key in standard format
        return f"{letter}_{blue_type}_{red_type}"

    def has_swap_override(self, beat_data: BeatData) -> bool:
        """Check if beat has manual swap override in special placements."""
        placements = self.load_special_placements()
        if not placements:
            return False

        override_key = self.generate_override_key(beat_data)
        return override_key in placements

    def get_swap_override_data(self, beat_data: BeatData) -> Dict[str, Any]:
        """Get swap override data for beat."""
        placements = self.load_special_placements()
        override_key = self.generate_override_key(beat_data)
        return placements.get(override_key, {})

    def reload_configuration(self) -> bool:
        """Reload configuration from files."""
        self._special_placements = None
        try:
            self._load_special_placements()
            return True
        except Exception:
            return False

    def get_configuration_status(self) -> Dict[str, Any]:
        """Get status of configuration loading."""
        return {
            "special_placements_loaded": self._special_placements is not None,
            "special_placements_count": len(self._special_placements or {}),
            "config_paths": self._config_paths,
        }

    def validate_configuration(self) -> Dict[str, Any]:
        """Validate loaded configuration data."""
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
        }

        placements = self.load_special_placements()

        # Validate special placements structure
        if not isinstance(placements, dict):
            validation_result["valid"] = False
            validation_result["errors"].append(
                "Special placements must be a dictionary"
            )
            return validation_result

        # Validate individual placement entries
        for key, value in placements.items():
            if not isinstance(key, str):
                validation_result["warnings"].append(f"Non-string key found: {key}")

            if not isinstance(value, dict):
                validation_result["warnings"].append(f"Non-dict value for key {key}")

        return validation_result

    def _load_special_placements(self) -> None:
        """Load special placement data from JSON configuration files."""
        for config_path in self._config_paths:
            try:
                if config_path.exists():
                    with open(config_path, "r") as f:
                        self._special_placements = json.load(f)
                    print(f"Loaded special placements from: {config_path}")
                    return
            except Exception as e:
                print(
                    f"Warning: Could not load special placements from {config_path}: {e}"
                )
                continue

        # No configuration file found
        print("Warning: No special placements configuration file found")
        self._special_placements = {}

    def _get_default_config_paths(self) -> list:
        """Get default configuration file paths."""
        return [
            Path("data/special_placements.json"),
            Path("v1/src/resources/special_placements.json"),
            Path("../data/special_placements.json"),
            Path("../../data/special_placements.json"),
        ]

    def add_config_path(self, path: Path) -> None:
        """Add additional configuration path."""
        if path not in self._config_paths:
            self._config_paths.append(path)

    def clear_cache(self) -> None:
        """Clear cached configuration data."""
        self._special_placements = None
