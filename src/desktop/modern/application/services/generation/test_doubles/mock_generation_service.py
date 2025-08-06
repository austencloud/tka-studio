"""
Mock Generation Services for Testing and Fallback

Provides simple mock implementations of generation services that can be used
when the real services are not available or for testing purposes.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Optional

from desktop.modern.core.interfaces.generation_services import (
    GenerationMode,
    IGenerationService,
    ISequenceConfigurationService,
    LetterType,
    PropContinuity,
    ValidationResult,
)
from desktop.modern.domain.models.enums import GridMode
from desktop.modern.domain.models.generation_models import (
    GenerationConfig,
    GenerationMetadata,
    GenerationResult,
)

logger = logging.getLogger(__name__)


class MockGenerationService(IGenerationService):
    """Mock generation service that creates simple test sequences."""

    def __init__(self, container=None):
        self.container = container
        logger.info("✅ Mock generation service initialized")

    def generate_freeform_sequence(self, config: GenerationConfig) -> GenerationResult:
        """Generate a mock freeform sequence."""
        try:
            logger.info(f"🎯 Mock freeform generation: length={config.length}")
            
            # Create simple mock sequence data
            sequence_data = []
            for i in range(config.length):
                beat_data = {
                    "beat": i + 1,
                    "letter": "A",  # Simple mock letter
                    "start_position": "alpha1",
                    "end_position": "alpha2",
                    "motions": [],
                    "metadata": {"mock": True}
                }
                sequence_data.append(beat_data)

            # Create mock metadata
            metadata = GenerationMetadata(
                generation_time_ms=50,
                algorithm_used="mock_freeform",
                parameters_hash="mock_hash",
                warnings=[]
            )

            logger.info(f"✅ Mock freeform sequence generated: {len(sequence_data)} beats")
            
            return GenerationResult(
                success=True,
                sequence_data=sequence_data,
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"❌ Mock freeform generation failed: {e}")
            return GenerationResult(
                success=False,
                error_message=f"Mock generation failed: {e}"
            )

    def generate_circular_sequence(self, config: GenerationConfig) -> GenerationResult:
        """Generate a mock circular sequence."""
        try:
            logger.info(f"🎯 Mock circular generation: length={config.length}")
            
            # Create simple mock sequence data
            sequence_data = []
            for i in range(config.length):
                beat_data = {
                    "beat": i + 1,
                    "letter": "B",  # Different letter for circular
                    "start_position": "beta1",
                    "end_position": "beta2", 
                    "motions": [],
                    "metadata": {"mock": True, "circular": True}
                }
                sequence_data.append(beat_data)

            # Create mock metadata
            metadata = GenerationMetadata(
                generation_time_ms=75,
                algorithm_used="mock_circular",
                parameters_hash="mock_hash_circular",
                warnings=[]
            )

            logger.info(f"✅ Mock circular sequence generated: {len(sequence_data)} beats")
            
            return GenerationResult(
                success=True,
                sequence_data=sequence_data,
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"❌ Mock circular generation failed: {e}")
            return GenerationResult(
                success=False,
                error_message=f"Mock generation failed: {e}"
            )

    def auto_complete_sequence(self, current_sequence: Any) -> GenerationResult:
        """Mock auto-complete functionality."""
        try:
            logger.info("🎯 Mock auto-complete")
            
            # Simple mock auto-completion
            sequence_data = [
                {
                    "beat": 1,
                    "letter": "C",
                    "start_position": "gamma1",
                    "end_position": "gamma2",
                    "motions": [],
                    "metadata": {"mock": True, "auto_complete": True}
                }
            ]

            metadata = GenerationMetadata(
                generation_time_ms=25,
                algorithm_used="mock_auto_complete",
                parameters_hash="mock_auto_hash",
                warnings=[]
            )

            return GenerationResult(
                success=True,
                sequence_data=sequence_data,
                metadata=metadata
            )

        except Exception as e:
            logger.error(f"❌ Mock auto-complete failed: {e}")
            return GenerationResult(
                success=False,
                error_message=f"Mock auto-complete failed: {e}"
            )

    def validate_generation_parameters(self, config: GenerationConfig) -> ValidationResult:
        """Mock validation that always passes."""
        return ValidationResult(
            is_valid=True,
            warnings=["Using mock generation service"]
        )


class MockSequenceConfigurationService(ISequenceConfigurationService):
    """Mock configuration service with default settings."""

    def __init__(self, container=None):
        self.container = container
        self._current_config = self._create_default_config()
        logger.info("✅ Mock configuration service initialized")

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
            
            logger.debug(f"Mock config updated: {list(updates.keys())}")
            
        except Exception as e:
            logger.error(f"Failed to update mock config: {e}")

    def save_config_as_preset(self, name: str) -> None:
        """Mock save preset (no-op)."""
        logger.info(f"Mock: Saved preset '{name}'")

    def load_config_preset(self, name: str) -> GenerationConfig:
        """Mock load preset (returns default)."""
        logger.info(f"Mock: Loaded preset '{name}'")
        return self._create_default_config()

    def get_default_config(self) -> GenerationConfig:
        """Get default configuration."""
        return self._create_default_config()

    def get_preset_names(self) -> list[str]:
        """Get mock preset names."""
        return ["Default", "Mock Preset 1", "Mock Preset 2"]
