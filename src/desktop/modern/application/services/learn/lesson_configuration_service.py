"""
Lesson Configuration Service Implementation

Provides lesson configurations and types for the learning module.
Manages static lesson data and configuration parameters.
"""

import logging
from typing import Optional

from desktop.modern.core.interfaces.learn_services import ILessonConfigurationService
from desktop.modern.domain.models.learn import LessonConfig, LessonType

logger = logging.getLogger(__name__)


class LessonConfigurationService(ILessonConfigurationService):
    """
    Production implementation of lesson configuration management.

    Provides access to lesson configurations matching the legacy system
    with proper type safety and error handling.
    """

    def __init__(self):
        """Initialize lesson configuration service."""
        self._lesson_configs: dict[str, LessonConfig] = {}
        self._setup_lesson_configs()

    def _setup_lesson_configs(self) -> None:
        """Setup lesson configurations matching legacy system."""
        try:
            # Lesson 1: Pictograph to Letter
            self._lesson_configs["Lesson1"] = LessonConfig(
                lesson_type=LessonType.PICTOGRAPH_TO_LETTER,
                question_format="pictograph",
                answer_format="button",
                quiz_description="pictograph_to_letter",
                question_prompt="Choose the letter for:",
            )

            # Lesson 2: Letter to Pictograph
            self._lesson_configs["Lesson2"] = LessonConfig(
                lesson_type=LessonType.LETTER_TO_PICTOGRAPH,
                question_format="letter",
                answer_format="pictograph",
                quiz_description="letter_to_pictograph",
                question_prompt="Choose the pictograph for:",
            )

            # Lesson 3: Valid Next Pictograph
            self._lesson_configs["Lesson3"] = LessonConfig(
                lesson_type=LessonType.VALID_NEXT_PICTOGRAPH,
                question_format="pictograph",
                answer_format="pictograph",
                quiz_description="valid_next_pictograph",
                question_prompt="Which pictograph can follow?",
            )

            logger.info(
                f"Initialized {len(self._lesson_configs)} lesson configurations"
            )

        except Exception as e:
            logger.error(f"Failed to setup lesson configurations: {e}")
            raise

    def get_all_lesson_configs(self) -> dict[str, LessonConfig]:
        """
        Get all available lesson configurations.

        Returns:
            Dictionary mapping lesson identifiers to configurations
        """
        return self._lesson_configs.copy()

    def get_lesson_config(self, lesson_type: LessonType) -> Optional[LessonConfig]:
        """
        Get configuration for specific lesson type.

        Args:
            lesson_type: Type of lesson to get configuration for

        Returns:
            Lesson configuration or None if not found
        """
        try:
            # Find configuration by lesson type
            for config in self._lesson_configs.values():
                if config.lesson_type == lesson_type:
                    return config

            logger.warning(f"No configuration found for lesson type: {lesson_type}")
            return None

        except Exception as e:
            logger.error(f"Failed to get lesson config for {lesson_type}: {e}")
            return None

    def get_lesson_names(self) -> list[str]:
        """
        Get list of all lesson display names.

        Returns:
            List of human-readable lesson names
        """
        try:
            lesson_names = []

            # Map lesson types to display names
            type_to_name = {
                LessonType.PICTOGRAPH_TO_LETTER: "Lesson 1",
                LessonType.LETTER_TO_PICTOGRAPH: "Lesson 2",
                LessonType.VALID_NEXT_PICTOGRAPH: "Lesson 3",
            }

            for config in self._lesson_configs.values():
                display_name = type_to_name.get(config.lesson_type, "Unknown Lesson")
                lesson_names.append(display_name)

            return sorted(lesson_names)

        except Exception as e:
            logger.error(f"Failed to get lesson names: {e}")
            return []

    def get_lesson_config_by_name(self, lesson_name: str) -> Optional[LessonConfig]:
        """
        Get lesson configuration by display name.

        Args:
            lesson_name: Display name of lesson (e.g., "Lesson 1")

        Returns:
            Lesson configuration or None if not found
        """
        try:
            # Map display names to lesson identifiers
            name_to_id = {
                "Lesson 1": "Lesson1",
                "Lesson 2": "Lesson2",
                "Lesson 3": "Lesson3",
            }

            lesson_id = name_to_id.get(lesson_name)
            if lesson_id:
                return self._lesson_configs.get(lesson_id)

            logger.warning(f"No configuration found for lesson name: {lesson_name}")
            return None

        except Exception as e:
            logger.error(f"Failed to get lesson config by name {lesson_name}: {e}")
            return None

    def validate_lesson_config(self, config: LessonConfig) -> bool:
        """
        Validate lesson configuration integrity.

        Args:
            config: Configuration to validate

        Returns:
            True if configuration is valid, False otherwise
        """
        try:
            # Check required fields
            if not config.lesson_type or not config.question_format:
                return False

            if not config.answer_format or not config.quiz_description:
                return False

            if not config.question_prompt:
                return False

            # Validate format combinations
            valid_combinations = {
                ("pictograph", "button"): LessonType.PICTOGRAPH_TO_LETTER,
                ("letter", "pictograph"): LessonType.LETTER_TO_PICTOGRAPH,
                ("pictograph", "pictograph"): LessonType.VALID_NEXT_PICTOGRAPH,
            }

            format_combo = (config.question_format, config.answer_format)
            expected_type = valid_combinations.get(format_combo)

            if expected_type != config.lesson_type:
                logger.warning(
                    f"Invalid format combination for lesson type {config.lesson_type}: "
                    f"{format_combo}"
                )
                return False

            return True

        except Exception as e:
            logger.error(f"Failed to validate lesson config: {e}")
            return False
