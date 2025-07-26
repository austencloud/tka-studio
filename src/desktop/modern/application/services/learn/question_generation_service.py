"""
Question Generation Service Implementation

Generates quiz questions based on lesson types and pictograph data.
Handles different question formats and answer generation.
"""

import logging
import random
from datetime import datetime
from typing import Any, Dict, List, Optional, Set

from desktop.modern.core.interfaces.data_builder_services import IPictographDataService
from desktop.modern.core.interfaces.learn_services import (
    IQuestionGenerationService,
    IQuizSessionService,
)
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
        pictograph_data_service: IPictographDataService,
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
        self._previous_correct_letters: Dict[str, Any] = {}
        self._previous_pictographs: Dict[str, Set[str]] = {}

        logger.info("Question generation service initialized")

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
            question.lesson_type = lesson_type.value
            question.generation_timestamp = datetime.now().isoformat()

            logger.debug(
                f"Generated {lesson_type.value} question for session {session_id}"
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

            # Generate wrong answers (3 different letters)
            wrong_answers = self._generate_wrong_letters(
                correct_letter, pictograph_dataset
            )
            options = [correct_letter] + wrong_answers
            random.shuffle(options)

            return QuestionData(
                question_content=correct_pictograph_data,
                answer_options=options,
                correct_answer=correct_letter,
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
            correct_letter: str = random.choice(available_letters)

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

            return QuestionData(
                question_content=correct_letter,
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

    def get_pictograph_dataset(self) -> Dict[Any, List[Dict]]:
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

    def _generate_correct_letter(self, session_id: str, dataset: Dict) -> str:
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

    def _generate_wrong_letters(self, correct_letter: Any, dataset: Dict) -> List[str]:
        """Generate 3 wrong letter answers."""
        try:
            # Dataset keys are already strings, not enum objects
            available_letters = [
                letter for letter in dataset.keys() if letter != correct_letter
            ]

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
        self, correct_letter: Any, dataset: Dict
    ) -> List[Dict]:
        """Generate 3 wrong pictographs with different letters."""
        try:
            available_letters = [
                letter for letter in dataset.keys() if letter != correct_letter
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

    def _generate_initial_pictograph(self, dataset: Dict) -> Dict:
        """Generate initial pictograph for next pictograph questions."""
        try:
            # Filter dataset to only include TRUE start positions (start_pos == end_pos)
            # This should only include beta positions like beta1, beta3, beta5, beta7
            true_start_positions = []

            # Debug: Log first few pictographs to understand the data structure
            debug_count = 0
            for letter, letter_pictographs in dataset.items():
                for pictograph in letter_pictographs:
                    start_pos = self._get_start_pos(pictograph)
                    end_pos = self._get_end_pos(pictograph)

                    # Log first 5 pictographs for debugging
                    if debug_count < 5:
                        logger.info(
                            f"DEBUG: Letter '{letter}', start_pos='{start_pos}', end_pos='{end_pos}', equal={start_pos == end_pos}"
                        )
                        debug_count += 1

                    # Only include pictographs where start_pos == end_pos (true start positions)
                    if start_pos and end_pos and start_pos == end_pos:
                        # Accept any letter with start_pos == end_pos as a potential start position
                        # This includes β, B, and any other letters that might be start positions
                        true_start_positions.append(pictograph)
                        logger.info(
                            f"Found true start position: {letter} - {start_pos}"
                        )

            logger.info(
                f"Total true start positions found: {len(true_start_positions)}"
            )

            # Select from true start positions
            if true_start_positions:
                selected = random.choice(true_start_positions)
                logger.info(
                    f"Selected start position pictograph: {selected.get('letter', 'Unknown')} - {self._get_start_pos(selected)}"
                )
                return selected

            # Fallback: look for any start position (start_pos == end_pos) without beta requirement
            logger.warning(
                "No beta start positions found, looking for any start positions"
            )
            fallback_start_positions = []

            for letter, letter_pictographs in dataset.items():
                for pictograph in letter_pictographs:
                    start_pos = self._get_start_pos(pictograph)
                    end_pos = self._get_end_pos(pictograph)

                    if start_pos and end_pos and start_pos == end_pos:
                        fallback_start_positions.append(pictograph)

            if fallback_start_positions:
                selected = random.choice(fallback_start_positions)
                logger.warning(
                    f"Using fallback start position: {selected.get('letter', 'Unknown')} - {self._get_start_pos(selected)}"
                )
                return selected

            # Last resort: any pictograph
            logger.error("No start position pictographs found, using any pictograph")
            for letter_pictographs in dataset.values():
                if letter_pictographs:
                    return letter_pictographs[0]
            raise ValueError("No pictographs available")

        except Exception as e:
            logger.error(f"Failed to generate initial pictograph: {e}")
            raise

    def _generate_correct_next_pictograph(
        self, initial_pictograph: Dict, dataset: Dict
    ) -> Dict:
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
        self, correct_pictograph: Dict, dataset: Dict
    ) -> List[Dict]:
        """Generate 3 wrong next pictographs."""
        try:
            correct_start_pos = self._get_start_pos(correct_pictograph)
            wrong_pictographs = []

            # Collect all pictographs that CAN follow the initial pictograph but are different from correct answer
            valid_candidates = []
            for letter_pictographs in dataset.values():
                for pictograph in letter_pictographs:
                    # Valid candidate if it has the same start_pos (can follow) but is different from correct answer
                    if (
                        self._get_start_pos(pictograph) == correct_start_pos
                        and pictograph != correct_pictograph
                    ):
                        valid_candidates.append(pictograph)

            # If we don't have enough valid candidates, add some random pictographs as distractors
            if len(valid_candidates) < 3:
                logger.info(
                    f"Only {len(valid_candidates)} valid next pictographs found, adding random distractors"
                )

                # Add random pictographs as distractors
                all_pictographs = []
                for letter_pictographs in dataset.values():
                    all_pictographs.extend(letter_pictographs)

                # Remove the correct answer from all pictographs
                all_pictographs = [
                    p for p in all_pictographs if p != correct_pictograph
                ]

                # Add random distractors to reach at least 3 candidates
                random.shuffle(all_pictographs)
                for pictograph in all_pictographs:
                    if pictograph not in valid_candidates:
                        valid_candidates.append(pictograph)
                        if (
                            len(valid_candidates) >= 6
                        ):  # Get extra candidates for variety
                            break

            # Shuffle and take up to 3 unique wrong answers
            if valid_candidates:
                random.shuffle(valid_candidates)

                # Ensure we get unique pictographs (by letter and position)
                seen_keys = set()
                for pictograph in valid_candidates:
                    if len(wrong_pictographs) >= 3:
                        break

                    # Create unique key based on letter and positions
                    key = (
                        pictograph.get("letter", ""),
                        self._get_start_pos(pictograph),
                        self._get_end_pos(pictograph),
                    )

                    if key not in seen_keys:
                        wrong_pictographs.append(pictograph)
                        seen_keys.add(key)

            if len(wrong_pictographs) < 3:
                logger.warning(
                    f"Could only generate {len(wrong_pictographs)} wrong pictographs from {len(valid_candidates)} candidates"
                )

            return wrong_pictographs

        except Exception as e:
            logger.error(f"Failed to generate wrong next pictographs: {e}")
            return []

    def _filter_pictograph_dataset_by_grid_mode(self, dataset: Dict) -> Dict:
        """Filter pictograph dataset by grid mode (placeholder implementation)."""
        try:
            # For now, return the full dataset
            # In the future, this could filter by grid mode using GridModeChecker
            return dataset
        except Exception as e:
            logger.error(f"Failed to filter dataset by grid mode: {e}")
            return dataset

    def _get_start_pos(self, pictograph: Dict) -> Any:
        """Get start position from pictograph data."""
        # Import constants to avoid circular imports
        try:
            from data.constants import START_POS

            # Check if data is a PictographData object
            if "data" in pictograph and hasattr(pictograph["data"], "start_position"):
                return pictograph["data"].start_position
            # Try nested data structure as dict
            elif "data" in pictograph and isinstance(pictograph["data"], dict):
                return pictograph["data"].get(START_POS)
            return pictograph.get(START_POS)
        except ImportError:
            # Fallback if constants not available
            # Check if data is a PictographData object
            if "data" in pictograph and hasattr(pictograph["data"], "start_position"):
                return pictograph["data"].start_position
            # Try nested data structure as dict
            elif "data" in pictograph and isinstance(pictograph["data"], dict):
                return pictograph["data"].get("start_pos")
            return pictograph.get("start_pos")

    def _get_end_pos(self, pictograph: Dict) -> Any:
        """Get end position from pictograph data."""
        try:
            from data.constants import END_POS

            # Check if data is a PictographData object
            if "data" in pictograph and hasattr(pictograph["data"], "end_position"):
                return pictograph["data"].end_position
            # Try nested data structure as dict
            elif "data" in pictograph and isinstance(pictograph["data"], dict):
                return pictograph["data"].get(END_POS)
            return pictograph.get(END_POS)
        except ImportError:
            # Fallback if constants not available
            # Check if data is a PictographData object
            if "data" in pictograph and hasattr(pictograph["data"], "end_position"):
                return pictograph["data"].end_position
            # Try nested data structure as dict
            elif "data" in pictograph and isinstance(pictograph["data"], dict):
                return pictograph["data"].get("end_pos")
            return pictograph.get("end_pos")

    def _has_zero_turns(self, pictograph: Dict) -> bool:
        """Check if pictograph has zero turns in all motions."""
        try:
            # Check blue and red motion attributes for turns
            try:
                from data.constants import BLUE_ATTRS, RED_ATTRS
            except ImportError:
                BLUE_ATTRS = "blue_attributes"
                RED_ATTRS = "red_attributes"

            blue_attrs = pictograph.get(BLUE_ATTRS, {})
            red_attrs = pictograph.get(RED_ATTRS, {})

            # Check blue motion turns
            blue_turns = blue_attrs.get("turns", 0)
            if blue_turns != 0:
                return False

            # Check red motion turns
            red_turns = red_attrs.get("turns", 0)
            if red_turns != 0:
                return False

            # If we get here, all motions have 0 turns
            return True

        except Exception as e:
            logger.warning(f"Error checking turns for pictograph: {e}")
            # Default to True if we can't determine turns
            return True
