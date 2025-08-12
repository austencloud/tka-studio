"""
Real Sequence Configuration Service

Provides actual configuration management for sequence generation.
Handles presets, validation, and configuration persistence.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.generation_services import (
    GenerationMode,
    ISequenceConfigurationService,
    LetterType,
    PropContinuity,
)
from desktop.modern.domain.models.enums import GridMode
from desktop.modern.domain.models.generation_models import GenerationConfig

logger = logging.getLogger(__name__)


class SequenceConfigurationService(ISequenceConfigurationService):
    """Real configuration service with preset management and persistence."""

    def __init__(self, container=None):
        self.container = container
        self._current_config = self._create_default_config()
        self._presets: dict[str, GenerationConfig] = {}
        self._config_file = Path("data/generation_config.json")
        self._load_config_from_file()
        logger.info("✅ Real sequence configuration service initialized")

    def _create_default_config(self) -> GenerationConfig:
        """Create a default configuration."""
        return GenerationConfig(
            mode=GenerationMode.FREEFORM,
            length=16,
            level=1,
            turn_intensity=1.0,
            grid_mode=GridMode.DIAMOND,
            prop_continuity=PropContinuity.CONTINUOUS,
            letter_types={LetterType.TYPE1, LetterType.TYPE2},
            slice_size=None,
            cap_type=None
        )

    def get_current_config(self) -> GenerationConfig:
        """Get current configuration."""
        return self._current_config

    def update_config(self, updates: dict[str, Any]) -> None:
        """Update configuration with new values."""
        try:
            # Create new config with updates
            current_dict = {
                "mode": self._current_config.mode,
                "length": self._current_config.length,
                "level": self._current_config.level,
                "turn_intensity": self._current_config.turn_intensity,
                "grid_mode": self._current_config.grid_mode,
                "prop_continuity": self._current_config.prop_continuity,
                "letter_types": self._current_config.letter_types,
                "slice_size": self._current_config.slice_size,
                "cap_type": self._current_config.cap_type,
            }
            
            # Apply updates
            current_dict.update(updates)
            
            # Create new config
            self._current_config = GenerationConfig(**current_dict)
            
            # Save to file
            self._save_config_to_file()
            
            logger.debug(f"Configuration updated: {list(updates.keys())}")
            
        except Exception as e:
            logger.error(f"Failed to update configuration: {e}")

    def save_config_as_preset(self, name: str) -> None:
        """Save current configuration as a preset."""
        try:
            self._presets[name] = self._current_config
            self._save_config_to_file()
            logger.info(f"Saved preset '{name}'")
        except Exception as e:
            logger.error(f"Failed to save preset '{name}': {e}")

    def load_config_preset(self, name: str) -> GenerationConfig:
        """Load configuration from preset."""
        try:
            if name in self._presets:
                self._current_config = self._presets[name]
                logger.info(f"Loaded preset '{name}'")
                return self._current_config
            else:
                logger.warning(f"Preset '{name}' not found")
                return self._create_default_config()
        except Exception as e:
            logger.error(f"Failed to load preset '{name}': {e}")
            return self._create_default_config()

    def get_default_config(self) -> GenerationConfig:
        """Get default configuration."""
        return self._create_default_config()

    def get_preset_names(self) -> list[str]:
        """Get list of available preset names."""
        return list(self._presets.keys())

    def _load_config_from_file(self) -> None:
        """Load configuration and presets from file."""
        try:
            if self._config_file.exists():
                with open(self._config_file, 'r') as f:
                    data = json.load(f)
                
                # Load current config
                if 'current_config' in data:
                    config_data = data['current_config']
                    self._current_config = self._dict_to_config(config_data)
                
                # Load presets
                if 'presets' in data:
                    for name, preset_data in data['presets'].items():
                        self._presets[name] = self._dict_to_config(preset_data)
                
                logger.info(f"Loaded configuration from {self._config_file}")
            else:
                logger.info("No configuration file found, using defaults")
                
        except Exception as e:
            logger.error(f"Failed to load configuration from file: {e}")

    def _save_config_to_file(self) -> None:
        """Save configuration and presets to file."""
        try:
            # Ensure directory exists
            self._config_file.parent.mkdir(parents=True, exist_ok=True)
            
            data = {
                'current_config': self._config_to_dict(self._current_config),
                'presets': {
                    name: self._config_to_dict(config) 
                    for name, config in self._presets.items()
                }
            }
            
            with open(self._config_file, 'w') as f:
                json.dump(data, f, indent=2)
                
            logger.debug(f"Saved configuration to {self._config_file}")
            
        except Exception as e:
            logger.error(f"Failed to save configuration to file: {e}")

    def _config_to_dict(self, config: GenerationConfig) -> dict:
        """Convert GenerationConfig to dictionary for JSON serialization."""
        return {
            'mode': config.mode.value,
            'length': config.length,
            'level': config.level,
            'turn_intensity': config.turn_intensity,
            'grid_mode': config.grid_mode.value,
            'prop_continuity': config.prop_continuity.value,
            'letter_types': [lt.value for lt in config.letter_types],
            'slice_size': config.slice_size.value if config.slice_size else None,
            'cap_type': config.cap_type.value if config.cap_type else None,
        }

    def _dict_to_config(self, data: dict) -> GenerationConfig:
        """Convert dictionary to GenerationConfig."""
        return GenerationConfig(
            mode=GenerationMode(data['mode']),
            length=data['length'],
            level=data['level'],
            turn_intensity=data['turn_intensity'],
            grid_mode=GridMode(data['grid_mode']),
            prop_continuity=PropContinuity(data['prop_continuity']),
            letter_types={LetterType(lt) for lt in data['letter_types']},
            slice_size=None,  # TODO: Add proper enum handling
            cap_type=None,    # TODO: Add proper enum handling
        )
