"""
Domain repository interfaces for data_modern module.

These interfaces define the contracts for data access within the data_modern layer.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class PictographRepository(ABC):
    """Interface for pictograph data access."""
    
    @abstractmethod
    def get_pictograph_data(self, pictograph_id: str) -> Dict[str, Any]:
        """Retrieve pictograph data by ID."""
        pass

    @abstractmethod
    def save_pictograph_data(self, pictograph_id: str, data: Dict[str, Any]) -> bool:
        """Save pictograph data."""
        pass


class BeatFrameLayoutRepository(ABC):
    """Interface for beat frame layout data access."""
    
    @abstractmethod
    def get_layout(self, layout_type: str) -> Dict[str, Any]:
        """Get a specific layout by type."""
        pass

    @abstractmethod
    def get_all_layouts(self) -> Dict[str, Dict[str, Any]]:
        """Get all available layouts."""
        pass


class ArrowPlacementRepository(ABC):
    """Interface for arrow placement data access."""
    
    @abstractmethod
    def get_placement_data(self, pictograph_type: str) -> Dict[str, Any]:
        """Get arrow placement data for a pictograph type."""
        pass


class ConfigurationRepository(ABC):
    """Interface for configuration data access."""
    
    @abstractmethod
    def get_default_settings(self) -> Dict[str, Any]:
        """Get default configuration settings."""
        pass

    @abstractmethod
    def update_setting(self, key: str, value: Any) -> bool:
        """Update a configuration setting."""
        pass
