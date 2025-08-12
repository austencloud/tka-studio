"""
Learn Data Service Implementation

Handles data persistence and retrieval for the learning module,
including lesson progress, results, and session data.
"""

from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.learn_services import ILearnDataService
from desktop.modern.core.interfaces.organization_services import IFileSystemService
from desktop.modern.domain.models.learn import LessonResults, LessonType


logger = logging.getLogger(__name__)


class LearnDataService(ILearnDataService):
    """
    Production implementation of learn tab data persistence.

    Handles saving and loading lesson progress, results, and session data
    with proper error handling and file management.
    """

    def __init__(self, file_system_service: IFileSystemService):
        """
        Initialize learn data service.

        Args:
            file_system_service: Service for file system operations
        """
        self.file_system_service = file_system_service

        # Setup data directory structure
        self._setup_data_directories()

        logger.info("Learn data service initialized")

    def _setup_data_directories(self) -> None:
        """Setup data directory structure for learn tab data."""
        try:
            # Navigate from service location to modern root
            modern_dir = Path(__file__).parent.parent.parent.parent.parent
            self.data_dir = modern_dir / "data" / "learn"

            # Create directories if they don't exist
            self.progress_dir = self.data_dir / "progress"
            self.results_dir = self.data_dir / "results"
            self.sessions_dir = self.data_dir / "sessions"

            for directory in [
                self.data_dir,
                self.progress_dir,
                self.results_dir,
                self.sessions_dir,
            ]:
                directory.mkdir(parents=True, exist_ok=True)

            logger.debug(f"Learn data directories setup at {self.data_dir}")

        except Exception as e:
            logger.error(f"Failed to setup data directories: {e}")
            # Fallback to temporary directory
            import tempfile

            temp_dir = Path(tempfile.gettempdir()) / "tka_learn_data"
            temp_dir.mkdir(exist_ok=True)
            self.data_dir = temp_dir
            self.progress_dir = temp_dir / "progress"
            self.results_dir = temp_dir / "results"
            self.sessions_dir = temp_dir / "sessions"

    def save_lesson_progress(
        self, session_id: str, progress_data: dict[str, Any]
    ) -> bool:
        """
        Save lesson progress to persistent storage.

        Args:
            session_id: Session to save progress for
            progress_data: Progress data to save

        Returns:
            True if save successful, False otherwise
        """
        try:
            if not session_id or not progress_data:
                logger.warning("Cannot save empty session ID or progress data")
                return False

            # Add metadata
            save_data = {
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "progress_data": progress_data,
            }

            # Save to file
            progress_file = self.progress_dir / f"{session_id}.json"
            content = json.dumps(save_data, indent=2)

            self.file_system_service.write_file(progress_file, content)

            logger.debug(f"Saved lesson progress for session {session_id}")
            return True

        except Exception as e:
            logger.error(
                f"Failed to save lesson progress for session {session_id}: {e}"
            )
            return False

    def load_lesson_progress(self, session_id: str) -> dict[str, Any] | None:
        """
        Load lesson progress from persistent storage.

        Args:
            session_id: Session to load progress for

        Returns:
            Progress data or None if not found
        """
        try:
            if not session_id:
                return None

            progress_file = self.progress_dir / f"{session_id}.json"

            if not progress_file.exists():
                logger.debug(f"No progress file found for session {session_id}")
                return None

            # Read and parse file
            content = self.file_system_service.read_file(progress_file)
            data = json.loads(content)

            # Return progress data portion
            progress_data = data.get("progress_data", {})

            logger.debug(f"Loaded lesson progress for session {session_id}")
            return progress_data

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse progress file for session {session_id}: {e}")
            return None
        except Exception as e:
            logger.error(
                f"Failed to load lesson progress for session {session_id}: {e}"
            )
            return None

    def save_lesson_results(self, results: LessonResults) -> bool:
        """
        Save lesson results to persistent storage.

        Args:
            results: Results to save

        Returns:
            True if save successful, False otherwise
        """
        try:
            if not results or not results.session_id:
                logger.warning("Cannot save empty results")
                return False

            # Convert results to dictionary
            save_data = results.to_dict()
            save_data["saved_timestamp"] = datetime.now().isoformat()
            save_data["version"] = "1.0"

            # Create filename with timestamp for uniqueness
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            results_file = self.results_dir / f"{results.session_id}_{timestamp}.json"

            # Save to file
            content = json.dumps(save_data, indent=2)
            self.file_system_service.write_file(results_file, content)

            # Also save to latest results for quick access
            latest_file = self.results_dir / f"{results.session_id}_latest.json"
            self.file_system_service.write_file(latest_file, content)

            logger.info(
                f"Saved lesson results for session {results.session_id}: "
                f"{results.correct_answers}/{results.questions_answered} correct "
                f"({results.accuracy_percentage:.1f}%)"
            )
            return True

        except Exception as e:
            logger.error(f"Failed to save lesson results: {e}")
            return False

    def get_lesson_history(
        self, lesson_type: LessonType, limit: int = 10
    ) -> list[LessonResults]:
        """
        Get lesson history for a specific lesson type.

        Args:
            lesson_type: Type of lesson to get history for
            limit: Maximum number of results to return

        Returns:
            List of lesson results ordered by completion date
        """
        try:
            if not isinstance(lesson_type, LessonType):
                logger.warning(f"Invalid lesson type: {lesson_type}")
                return []

            results = []

            # Scan results directory for matching files
            if self.results_dir.exists():
                for results_file in self.results_dir.glob("*.json"):
                    # Skip latest files to avoid duplicates
                    if "_latest.json" in results_file.name:
                        continue

                    try:
                        content = self.file_system_service.read_file(results_file)
                        data = json.loads(content)

                        # Check if lesson type matches
                        if data.get("lesson_type") == lesson_type.value:
                            lesson_results = LessonResults.from_dict(data)
                            results.append(lesson_results)

                    except Exception as e:
                        logger.warning(
                            f"Failed to parse results file {results_file}: {e}"
                        )
                        continue

            # Sort by completion date (newest first) and limit
            results.sort(key=lambda r: r.completed_at, reverse=True)
            limited_results = results[:limit]

            logger.debug(
                f"Found {len(limited_results)} results for lesson type {lesson_type.value}"
            )
            return limited_results

        except Exception as e:
            logger.error(f"Failed to get lesson history for {lesson_type}: {e}")
            return []

    def get_all_lesson_results(self, limit: int = 50) -> list[LessonResults]:
        """
        Get all lesson results across all lesson types.

        Args:
            limit: Maximum number of results to return

        Returns:
            List of all lesson results ordered by completion date
        """
        try:
            results = []

            if self.results_dir.exists():
                for results_file in self.results_dir.glob("*.json"):
                    # Skip latest files to avoid duplicates
                    if "_latest.json" in results_file.name:
                        continue

                    try:
                        content = self.file_system_service.read_file(results_file)
                        data = json.loads(content)

                        lesson_results = LessonResults.from_dict(data)
                        results.append(lesson_results)

                    except Exception as e:
                        logger.warning(
                            f"Failed to parse results file {results_file}: {e}"
                        )
                        continue

            # Sort by completion date (newest first) and limit
            results.sort(key=lambda r: r.completed_at, reverse=True)
            limited_results = results[:limit]

            logger.debug(f"Found {len(limited_results)} total lesson results")
            return limited_results

        except Exception as e:
            logger.error(f"Failed to get all lesson results: {e}")
            return []

    def delete_lesson_progress(self, session_id: str) -> bool:
        """
        Delete lesson progress for a session.

        Args:
            session_id: Session to delete progress for

        Returns:
            True if deletion successful, False otherwise
        """
        try:
            if not session_id:
                return False

            progress_file = self.progress_dir / f"{session_id}.json"

            if progress_file.exists():
                progress_file.unlink()
                logger.debug(f"Deleted lesson progress for session {session_id}")

            return True

        except Exception as e:
            logger.error(
                f"Failed to delete lesson progress for session {session_id}: {e}"
            )
            return False

    def cleanup_old_data(self, days_old: int = 30) -> int:
        """
        Clean up old lesson data files.

        Args:
            days_old: Number of days after which to clean up files

        Returns:
            Number of files cleaned up
        """
        try:
            from datetime import timedelta

            cutoff_date = datetime.now() - timedelta(days=days_old)
            cleanup_count = 0

            # Clean up old progress files
            if self.progress_dir.exists():
                for progress_file in self.progress_dir.glob("*.json"):
                    try:
                        file_time = datetime.fromtimestamp(
                            progress_file.stat().st_mtime
                        )
                        if file_time < cutoff_date:
                            progress_file.unlink()
                            cleanup_count += 1
                            logger.debug(
                                f"Cleaned up old progress file: {progress_file.name}"
                            )
                    except Exception as e:
                        logger.warning(
                            f"Failed to cleanup progress file {progress_file}: {e}"
                        )

            # Clean up old session files
            if self.sessions_dir.exists():
                for session_file in self.sessions_dir.glob("*.json"):
                    try:
                        file_time = datetime.fromtimestamp(session_file.stat().st_mtime)
                        if file_time < cutoff_date:
                            session_file.unlink()
                            cleanup_count += 1
                            logger.debug(
                                f"Cleaned up old session file: {session_file.name}"
                            )
                    except Exception as e:
                        logger.warning(
                            f"Failed to cleanup session file {session_file}: {e}"
                        )

            if cleanup_count > 0:
                logger.info(f"Cleaned up {cleanup_count} old learn data files")

            return cleanup_count

        except Exception as e:
            logger.error(f"Failed to cleanup old data: {e}")
            return 0

    def get_data_statistics(self) -> dict[str, Any]:
        """
        Get statistics about stored learn data.

        Returns:
            Dictionary with data statistics
        """
        try:
            stats = {
                "progress_files": 0,
                "results_files": 0,
                "session_files": 0,
                "total_disk_usage_mb": 0.0,
            }

            # Count files and calculate disk usage
            for directory, stat_key in [
                (self.progress_dir, "progress_files"),
                (self.results_dir, "results_files"),
                (self.sessions_dir, "session_files"),
            ]:
                if directory.exists():
                    files = list(directory.glob("*.json"))
                    stats[stat_key] = len(files)

                    # Calculate disk usage
                    for file_path in files:
                        try:
                            stats["total_disk_usage_mb"] += file_path.stat().st_size / (
                                1024 * 1024
                            )
                        except Exception:
                            pass

            return stats

        except Exception as e:
            logger.error(f"Failed to get data statistics: {e}")
            return {
                "progress_files": 0,
                "results_files": 0,
                "session_files": 0,
                "total_disk_usage_mb": 0.0,
            }
