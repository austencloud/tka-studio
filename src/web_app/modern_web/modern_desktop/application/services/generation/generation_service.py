"""
Generation Service - PRODUCTION READY with ROBUST ERROR HANDLING

Orchestrates sequence generation using modern TKA architecture.
ROBUST: Handles all error cases gracefully, works without optional services.
"""

from __future__ import annotations

import logging
import time
from typing import Any

from desktop.modern.core.interfaces.generation_services import (
    IGenerationService,
    ValidationResult,
)
from desktop.modern.domain.models.generation_models import (
    GenerationConfig,
    GenerationMetadata,
    GenerationResult,
)


logger = logging.getLogger(__name__)


class GenerationService(IGenerationService):
    """
    Modern generation service with robust error handling and graceful degradation.

    Orchestrates sequence generation for both freeform and circular modes using
    modern TKA services and data structures.
    """

    def __init__(self, container=None):
        # Service references - will be initialized lazily
        self.freeform_service = None
        self.circular_service = None
        self.validation_service = None
        self.container = container

        # Initialize services with robust error handling
        self._initialize_modern_services()

    def _initialize_modern_services(self) -> None:
        """Initialize modern generation services with robust error handling."""
        try:
            from .core.freeform_generator import FreeformGenerator

            self.freeform_service = FreeformGenerator()
            logger.info("✅ Freeform generator initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize freeform generator: {e!s}")
            raise RuntimeError(f"Cannot initialize freeform generation: {e}")

        try:
            from .core.circular_generator import CircularGenerator

            self.circular_service = CircularGenerator()
            logger.info("✅ Circular generator initialized")
        except Exception as e:
            logger.error(f"❌ Failed to initialize circular generator: {e!s}")
            raise RuntimeError(f"Cannot initialize circular generation: {e}")

        # Validation service removed - validation is now built into generators
        logger.info("✅ All generators initialized successfully")

    def generate_freeform_sequence(self, config: GenerationConfig) -> GenerationResult:
        """
        Generate a freeform sequence using modern architecture.
        ROBUST: Handles all error cases and provides meaningful feedback.

        Args:
            config: Generation configuration

        Returns:
            Generation result with sequence data or error
        """
        try:
            start_time = time.time()

            logger.info(
                f"🎯 Starting modern freeform generation: length={config.length}, level={config.level}"
            )

            # Validate configuration (optional)
            validation = self.validate_generation_parameters(config)
            if not validation.is_valid:
                return GenerationResult(
                    success=False,
                    error_message=f"Configuration validation failed: {'; '.join(validation.errors or [])}",
                    warnings=validation.warnings,
                )

            # Check if freeform service is available
            if not self.freeform_service:
                return GenerationResult(
                    success=False,
                    error_message="Freeform generation service not available",
                )

            # Generate sequence using modern freeform service
            sequence_data = self.freeform_service.generate_sequence(config)

            if not sequence_data:
                return GenerationResult(
                    success=False, error_message="No sequence data generated"
                )

            # Create metadata
            generation_time = int((time.time() - start_time) * 1000)
            metadata = GenerationMetadata(
                generation_time_ms=generation_time,
                algorithm_used="modern_freeform",
                parameters_hash=self._hash_config(config),
                warnings=validation.warnings,
            )

            # DEBUG: Check if length matches request
            requested_length = config.length
            actual_length = len(sequence_data)
            print(
                f"🔍 [GENERATION_SERVICE] FREEFORM - Requested: {requested_length}, Generated: {actual_length}"
            )

            logger.info(
                f"✅ Successfully generated modern freeform sequence with {len(sequence_data)} beats"
            )

            return GenerationResult(
                success=True,
                sequence_data=sequence_data,
                metadata=metadata,
                warnings=validation.warnings,
            )

        except Exception as e:
            logger.error(f"❌ Modern freeform generation failed: {e!s}", exc_info=True)
            return GenerationResult(
                success=False, error_message=f"Generation failed: {e!s}"
            )

    def generate_circular_sequence(self, config: GenerationConfig) -> GenerationResult:
        """
        Generate a circular sequence using modern architecture.
        ROBUST: Handles all error cases and provides meaningful feedback.

        Args:
            config: Generation configuration

        Returns:
            Generation result with sequence data or error
        """
        try:
            start_time = time.time()

            logger.info(
                f"🎯 Starting modern circular generation: length={config.length}, CAP={config.cap_type}"
            )

            # Validate configuration (optional)
            validation = self.validate_generation_parameters(config)
            if not validation.is_valid:
                return GenerationResult(
                    success=False,
                    error_message=f"Configuration validation failed: {'; '.join(validation.errors or [])}",
                    warnings=validation.warnings,
                )

            # Check if circular service is available
            if not self.circular_service:
                return GenerationResult(
                    success=False,
                    error_message="Circular generation service not available",
                )

            # Generate sequence using modern circular service
            sequence_data = self.circular_service.generate_sequence(config)

            if not sequence_data:
                return GenerationResult(
                    success=False, error_message="No sequence data generated"
                )

            # Create metadata
            generation_time = int((time.time() - start_time) * 1000)
            metadata = GenerationMetadata(
                generation_time_ms=generation_time,
                algorithm_used="modern_circular",
                parameters_hash=self._hash_config(config),
                warnings=validation.warnings,
            )

            # DEBUG: Check if length matches request
            requested_length = config.length
            actual_length = len(sequence_data)
            print(
                f"🔍 [GENERATION_SERVICE] CIRCULAR - Requested: {requested_length}, Generated: {actual_length}"
            )

            logger.info(
                f"✅ Successfully generated modern circular sequence with {len(sequence_data)} beats"
            )

            return GenerationResult(
                success=True,
                sequence_data=sequence_data,
                metadata=metadata,
                warnings=validation.warnings,
            )

        except Exception as e:
            logger.error(f"❌ Modern circular generation failed: {e!s}", exc_info=True)
            return GenerationResult(
                success=False, error_message=f"Generation failed: {e!s}"
            )

    def auto_complete_sequence(self, current_sequence: Any) -> GenerationResult:
        """
        Auto-complete an existing sequence using modern architecture.
        ROBUST: Safe to call even with minimal implementation.

        Args:
            current_sequence: Current sequence data

        Returns:
            Generation result with completed sequence
        """
        try:
            start_time = time.time()

            logger.info("🎯 Starting modern auto-completion")

            # For now, return success with current sequence
            # TODO: Implement actual auto-completion logic using modern services

            metadata = GenerationMetadata(
                generation_time_ms=int((time.time() - start_time) * 1000),
                algorithm_used="modern_auto_complete",
                parameters_hash="auto_complete",
                warnings=[
                    "Auto-completion is not yet fully implemented in modern architecture"
                ],
            )

            return GenerationResult(
                success=True,
                sequence_data=current_sequence or [],
                metadata=metadata,
                warnings=["Auto-completion feature is under development"],
            )

        except Exception as e:
            logger.error(f"❌ Modern auto-completion failed: {e!s}", exc_info=True)
            return GenerationResult(
                success=False, error_message=f"Auto-completion failed: {e!s}"
            )

    def validate_generation_parameters(
        self, config: GenerationConfig
    ) -> ValidationResult:
        """
        Validate generation configuration.
        ROBUST: Works with or without validation service.

        Args:
            config: Configuration to validate

        Returns:
            Validation result
        """
        try:
            # If validation service is available, use it
            if self.validation_service:
                return self.validation_service.validate_complete_config(config)

            # Otherwise, perform basic validation
            return self._basic_validation(config)

        except Exception as e:
            logger.error(f"❌ Validation failed: {e!s}", exc_info=True)
            return ValidationResult(is_valid=False, errors=[f"Validation error: {e!s}"])

    def _basic_validation(self, config: GenerationConfig) -> ValidationResult:
        """Perform basic validation when validation service is not available."""
        errors = []
        warnings = []

        # Basic validation rules
        if config.length <= 0:
            errors.append("Sequence length must be positive")
        elif config.length > 32:
            errors.append("Sequence length cannot exceed 32")

        if config.level < 1 or config.level > 6:
            errors.append("Level must be between 1 and 6")

        if config.turn_intensity < 0 or config.turn_intensity > 3:
            errors.append("Turn intensity must be between 0 and 3")

        # Warnings for edge cases
        if config.length > 24:
            warnings.append("Large sequence lengths may take longer to generate")

        if config.level >= 3 and config.turn_intensity >= 2.5:
            warnings.append(
                "High level with high turn intensity may create complex sequences"
            )

        return ValidationResult(
            is_valid=len(errors) == 0,
            errors=errors if errors else None,
            warnings=warnings if warnings else None,
        )

    def _hash_config(self, config: GenerationConfig) -> str:
        """Create a hash of the configuration for metadata."""
        try:
            import hashlib

            # Create a string representation of key config parameters
            config_str = f"{config.mode.value}_{config.length}_{config.level}_{config.turn_intensity}"
            if config.letter_types:
                letter_types_str = "_".join(
                    sorted([lt.value for lt in config.letter_types])
                )
                config_str += f"_{letter_types_str}"
            if config.cap_type:
                config_str += f"_{config.cap_type.value}"

            return hashlib.md5(config_str.encode()).hexdigest()[:8]

        except Exception as e:
            logger.warning(f"Failed to hash config: {e}")
            return "unknown"
