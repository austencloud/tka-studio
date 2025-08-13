"""
Question Generation Service Implementation

Generates quiz questions based on lesson types and pictograph data.
Handles different question formats and answer generation.
"""

import logging
import random
from datetime import datetime
from typing import Any

from desktop.modern.core.interfaces.learn_services import (
    IQuestionGenerationService,
    IQuizSessionService,
)
from desktop.modern.core.interfaces.pictograph_services import IPictographDataManager
from desktop.modern.domain.models.learn import LessonConfig, LessonType, QuestionData

logger = logging.getLogger(__name__)


class QuestionGenerationService(IQuestionGenerationService):
    """
    Production implementation of question generation for quiz lessons.

    Generates questions matching legacy behavior with proper randomization,
    avoiding repetition, and supporting all lesson types.
    """

    def __init__(
        self,
        session_service: IQuizSessionService,
        pictograph_data_service: IPictographDataManager,
    ):
        """
        Initialize question generation service.

        Args:
            session_service: Service for session management
            pictograph_data_service: Service for pictograph data access
        """
        self.session_service = session_service
        self.pictograph_data_service = pictograph_data_service

        # Track previous questions to avoid repetition
        self._previous_correct_letters: dict[str, Any] = {}
        self._previous_pictographs: dict[str, set[str]] = {}

        # Debug: Check what type of pictograph service we got
        service_type = type(self.pictograph_data_service).__name__
        logger.info(f"Question generation service initialized with {service_type}")

        if "Mock" in service_type:
            logger.warning(
                "🚨 Using MockPictographDataService - real pictographs will not be rendered!"
            )
        else:
            logger.info(
                "✅ Using real pictograph data service for actual pictograph rendering"
            )

    def generate_question(
        self, session_id: str, lesson_config: LessonConfig
    ) -> QuestionData:
        """
        Generate next question for the session.

        Args:
            session_id: Session to generate question for
            lesson_config: Configuration for the lesson type

        Returns:
            Generated question data

        Raises:
            ValueError: If session not found or invalid lesson type
        """
        try:
            session = self.session_service.get_session(session_id)
            if not session:
                raise ValueError(f"Session not found: {session_id}")

            lesson_type = lesson_config.lesson_type

            # Generate question based on lesson type
            if lesson_type == LessonType.PICTOGRAPH_TO_LETTER:
                question = self._generate_pictograph_to_letter_question(session_id)
            elif lesson_type == LessonType.LETTER_TO_PICTOGRAPH:
                question = self._generate_letter_to_pictograph_question(session_id)
            elif lesson_type == LessonType.VALID_NEXT_PICTOGRAPH:
                question = self._generate_valid_next_pictograph_question(session_id)
            else:
                raise ValueError(f"Unknown lesson type: {lesson_type}")

            # Add metadata
            lesson_type_str = (
                lesson_type.value if hasattr(lesson_type, "value") else str(lesson_type)
            )
            question.lesson_type = lesson_type_str
            question.generation_timestamp = datetime.now().isoformat()

            logger.debug(
                f"Generated {lesson_type_str} question for session {session_id}"
            )
            return question

        except Exception as e:
            logger.error(f"Failed to generate question for session {session_id}: {e}")
            raise

    def _generate_pictograph_to_letter_question(self, session_id: str) -> QuestionData:
        """Generate pictograph → letter question."""
        try:
            pictograph_dataset = self.get_pictograph_dataset()

            # Get correct letter (avoid previous)
            correct_letter = self._generate_correct_letter(
                session_id, pictograph_dataset
            )
            self._previous_correct_letters[session_id] = correct_letter

            # Get random pictograph for this letter
            correct_pictograph_data = random.choice(pictograph_dataset[correct_letter])

            # Debug: Log what pictograph data we're using
            logger.info(
                f"🎨 Selected pictograph for question: {correct_pictograph_data.get('id', 'unknown')}"
            )
            logger.info(f"   Type: {correct_pictograph_data.get('type', 'unknown')}")
            if "data" in correct_pictograph_data:
                pictograph_obj = correct_pictograph_data["data"]
                logger.info(f"   PictographData: {type(pictograph_obj)}")
                if hasattr(pictograph_obj, "arrows"):
                    logger.info(f"   Arrows: {len(pictograph_obj.arrows)} arrows")
                if hasattr(pictograph_obj, "grid_data"):
                    logger.info(
                        f"   Grid: {pictograph_obj.grid_data.grid_mode if pictograph_obj.grid_data else 'None'}"
                    )

            # Generate wrong answers (3 different letters)
            wrong_answers = self._generate_wrong_letters(
                correct_letter, pictograph_dataset
            )
            # Handle both string and enum correct_letter
            correct_letter_str = (
                correct_letter.value
                if hasattr(correct_letter, "value")
                else str(correct_letter)
            )
            options = [correct_letter_str] + wrong_answers
            random.shuffle(options)

            return QuestionData(
                question_content=correct_pictograph_data,
                answer_options=options,
                correct_answer=correct_letter_str,
                question_type="pictograph_to_letter",
            )

        except Exception as e:
            logger.error(f"Failed to generate pictograph to letter question: {e}")
            raise

    def _generate_letter_to_pictograph_question(self, session_id: str) -> QuestionData:
        """Generate letter → pictograph question."""
        try:
            pictograph_dataset = self.get_pictograph_dataset()

            # Get random letter and pictograph
            available_letters = list(pictograph_dataset.keys())
            correct_letter = random.choice(available_letters)

            # Filter by grid mode if necessary
            filtered_dataset = self._filter_pictograph_dataset_by_grid_mode(
                pictograph_dataset
            )
            correct_pictograph = random.choice(filtered_dataset[correct_letter])

            # Generate wrong pictographs (3 different letters)
            wrong_pictographs = self._generate_wrong_pictographs(
                correct_letter, filtered_dataset
            )
            pictographs = [correct_pictograph] + wrong_pictographs
            random.shuffle(pictographs)

            # Handle both string and enum correct_letter
            correct_letter_str = (
                correct_letter.value
                if hasattr(correct_letter, "value")
                else str(correct_letter)
            )

            return QuestionData(
                question_content=correct_letter_str,
                answer_options=pictographs,
                correct_answer=correct_pictograph,
                question_type="letter_to_pictograph",
            )

        except Exception as e:
            logger.error(f"Failed to generate letter to pictograph question: {e}")
            raise

    def _generate_valid_next_pictograph_question(self, session_id: str) -> QuestionData:
        """Generate valid next pictograph question."""
        try:
            pictograph_dataset = self.get_pictograph_dataset()
            filtered_dataset = self._filter_pictograph_dataset_by_grid_mode(
                pictograph_dataset
            )

            # Generate initial pictograph (start_pos == end_pos)
            initial_pictograph = self._generate_initial_pictograph(filtered_dataset)

            # Find valid next pictograph
            correct_next_pictograph = self._generate_correct_next_pictograph(
                initial_pictograph, filtered_dataset
            )

            # Generate wrong options (3 pictographs that can't follow)
            wrong_pictographs = self._generate_wrong_next_pictographs(
                correct_next_pictograph, filtered_dataset
            )

            options = [correct_next_pictograph] + wrong_pictographs
            random.shuffle(options)

            return QuestionData(
                question_content=initial_pictograph,
                answer_options=options,
                correct_answer=correct_next_pictograph,
                question_type="valid_next_pictograph",
            )

        except Exception as e:
            logger.error(f"Failed to generate valid next pictograph question: {e}")
            raise

    def get_pictograph_dataset(self) -> dict[Any, list[dict]]:
        """
        Get pictograph dataset for question generation.

        Returns:
            Dictionary mapping letters to pictograph data lists
        """
        try:
            return self.pictograph_data_service.get_pictograph_dataset()
        except Exception as e:
            logger.error(f"Failed to get pictograph dataset: {e}")
            # Return empty dataset to prevent crashes
            return {}

    def validate_question(self, question: QuestionData) -> bool:
        """
        Validate that a question is properly formed.

        Args:
            question: Question to validate

        Returns:
            True if question is valid, False otherwise
        """
        try:
            # Use the built-in validation from QuestionData
            return question.is_valid()
        except Exception as e:
            logger.error(f"Failed to validate question: {e}")
            return False

    def _generate_correct_letter(self, session_id: str, dataset: dict) -> Any:
        """Generate correct letter avoiding previous."""
        try:
            letters = list(dataset.keys())
            previous = self._previous_correct_letters.get(session_id)

            if previous and previous in letters:
                letters.remove(previous)

            if not letters:
                # If no letters available, reset previous and use all
                self._previous_correct_letters[session_id] = None
                letters = list(dataset.keys())

            return random.choice(letters)

        except Exception as e:
            logger.error(f"Failed to generate correct letter: {e}")
            # Fallback to first available letter
            return list(dataset.keys())[0] if dataset else None

    def _generate_wrong_letters(self, correct_letter: Any, dataset: dict) -> list[str]:
        """Generate 3 wrong letter answers."""
        try:
            # Handle both string keys (mock service) and enum keys (real service)
            available_letters = []
            for letter in dataset:
                if letter != correct_letter:
                    # If letter is an enum, use .value, otherwise use as string
                    letter_str = (
                        letter.value if hasattr(letter, "value") else str(letter)
                    )
                    available_letters.append(letter_str)

            if len(available_letters) < 3:
                logger.warning(
                    f"Not enough letters for wrong answers: {len(available_letters)}"
                )
                return available_letters

            return random.sample(available_letters, 3)

        except Exception as e:
            logger.error(f"Failed to generate wrong letters: {e}")
            return []

    def _generate_wrong_pictographs(
        self, correct_letter: Any, dataset: dict
    ) -> list[dict]:
        """Generate 3 wrong pictographs with different letters."""
        try:
            available_letters = [
                letter for letter in dataset if letter != correct_letter
            ]
            wrong_pictographs = []

            while len(wrong_pictographs) < 3 and available_letters:
                letter = random.choice(available_letters)
                pictograph_data = random.choice(dataset[letter])
                wrong_pictographs.append(pictograph_data)
                available_letters.remove(letter)

            return wrong_pictographs

        except Exception as e:
            logger.error(f"Failed to generate wrong pictographs: {e}")
            return []

    def _generate_initial_pictograph(self, dataset: dict) -> dict:
        """Generate initial pictograph for next pictograph questions."""
        try:
            # Find pictographs where start_pos == end_pos
            valid_initial = []
            for letter_pictographs in dataset.values():
                for pictograph in letter_pictographs:
                    if self._get_start_pos(pictograph) == self._get_end_pos(pictograph):
                        valid_initial.append(pictograph)

            if not valid_initial:
                logger.warning("No valid initial pictographs found")
                # Fallback to any pictograph
                for letter_pictographs in dataset.values():
                    if letter_pictographs:
                        return letter_pictographs[0]
                raise ValueError("No pictographs available")

            return random.choice(valid_initial)

        except Exception as e:
            logger.error(f"Failed to generate initial pictograph: {e}")
            raise

    def _generate_correct_next_pictograph(
        self, initial_pictograph: dict, dataset: dict
    ) -> dict:
        """Find valid next pictograph that can follow initial."""
        try:
            end_pos = self._get_end_pos(initial_pictograph)
            valid_next = []

            for letter_pictographs in dataset.values():
                for pictograph in letter_pictographs:
                    if self._get_start_pos(pictograph) == end_pos:
                        valid_next.append(pictograph)

            if not valid_next:
                logger.warning(
                    f"No valid next pictographs found for end_pos: {end_pos}"
                )
                # Fallback to any pictograph
                for letter_pictographs in dataset.values():
                    if letter_pictographs:
                        return letter_pictographs[0]
                raise ValueError("No next pictographs available")

            return random.choice(valid_next)

        except Exception as e:
            logger.error(f"Failed to generate correct next pictograph: {e}")
            raise

    def _generate_wrong_next_pictographs(
        self, correct_pictograph: dict, dataset: dict
    ) -> list[dict]:
        """Generate 3 wrong next pictographs."""
        try:
            correct_start_pos = self._get_start_pos(correct_pictograph)
            wrong_pictographs = []
            attempts = 0
            max_attempts = 100

            while len(wrong_pictographs) < 3 and attempts < max_attempts:
                # Get random pictograph
                letter = random.choice(list(dataset.keys()))
                random_pictograph = random.choice(dataset[letter])

                # Check if it has different start_pos than correct answer
                if self._get_start_pos(random_pictograph) != correct_start_pos:
                    # Avoid duplicates
                    if random_pictograph not in wrong_pictographs:
                        wrong_pictographs.append(random_pictograph)

                attempts += 1

            if len(wrong_pictographs) < 3:
                logger.warning(
                    f"Could only generate {len(wrong_pictographs)} wrong pictographs"
                )

            return wrong_pictographs

        except Exception as e:
            logger.error(f"Failed to generate wrong next pictographs: {e}")
            return []

    def _filter_pictograph_dataset_by_grid_mode(self, dataset: dict) -> dict:
        """Filter pictograph dataset by grid mode (placeholder implementation)."""
        try:
            # For now, return the full dataset
            # In the future, this could filter by grid mode using GridModeChecker
            return dataset
        except Exception as e:
            logger.error(f"Failed to filter dataset by grid mode: {e}")
            return dataset

    def _get_start_pos(self, pictograph: dict) -> Any:
        """Get start position from pictograph data."""
        # Import constants to avoid circular imports
        try:
            from data.constants import START_POS

            # Try legacy format first (direct key access)
            if START_POS in pictograph:
                return pictograph[START_POS]
        except ImportError:
            pass

        # Try standard fallback
        if "start_pos" in pictograph:
            return pictograph["start_pos"]

        # Try modern format (nested in data)
        if "data" in pictograph:
            data = pictograph["data"]
            if hasattr(data, "start_position") and data.start_position:
                # Convert GridPosition enum to integer
                return self._convert_grid_position_to_int(data.start_position)
            if "start_pos" in data:
                return data["start_pos"]

        logger.warning(
            f"Could not extract start_pos from pictograph: {list(pictograph.keys())}"
        )
        return 1  # Default fallback

    def _get_end_pos(self, pictograph: dict) -> Any:
        """Get end position from pictograph data."""
        try:
            from data.constants import END_POS

            # Try legacy format first (direct key access)
            if END_POS in pictograph:
                return pictograph[END_POS]
        except ImportError:
            pass

        # Try standard fallback
        if "end_pos" in pictograph:
            return pictograph["end_pos"]

        # Try modern format (nested in data)
        if "data" in pictograph:
            data = pictograph["data"]
            if hasattr(data, "end_position") and data.end_position:
                # Convert GridPosition enum to integer
                return self._convert_grid_position_to_int(data.end_position)
            if "end_pos" in data:
                return data["end_pos"]

        logger.warning(
            f"Could not extract end_pos from pictograph: {list(pictograph.keys())}"
        )
        return 1  # Default fallback

    def _convert_grid_position_to_int(self, grid_position) -> int:
        """Convert GridPosition enum to integer for legacy compatibility."""
        if grid_position is None:
            return 1  # Default position

        # Map GridPosition enums to integers (1-4 for legacy compatibility)
        position_map = {
            # Alpha positions (diamond/radial grid)
            "ALPHA1": 1,
            "ALPHA2": 2,
            "ALPHA3": 3,
            "ALPHA4": 4,
            "ALPHA5": 1,
            "ALPHA6": 2,
            "ALPHA7": 3,
            "ALPHA8": 4,  # Wrap around
            # Beta positions (box grid)
            "BETA1": 1,
            "BETA2": 2,
            "BETA3": 3,
            "BETA4": 4,
            "BETA5": 1,
            "BETA6": 2,
            "BETA7": 3,
            "BETA8": 4,  # Wrap around
        }

        # Get position name (handle both enum and string)
        position_name = (
            grid_position.name if hasattr(grid_position, "name") else str(grid_position)
        )
        return position_map.get(position_name, 1)  # Default to 1 if not found
