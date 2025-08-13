"""
Modern Path Service for Sequence Cards

Provides path resolution for sequence card resources without legacy dependencies.
Replaces legacy utils.path_helpers for sequence card functionality.
"""

import logging
import os
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)


class SequenceCardPathService:
    """Modern service for resolving sequence card related paths."""

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._dictionary_path: Optional[Path] = None
        self._cache_path: Optional[Path] = None

    def get_dictionary_path(self) -> Path:
        """
        Get the path to the sequence dictionary.

        Returns:
            Path to the dictionary directory
        """
        if self._dictionary_path is not None:
            return self._dictionary_path

        # Try multiple possible locations for the dictionary
        possible_paths = [
            # Development environment
            Path.cwd() / "data" / "dictionary",
            Path(__file__).parent.parent.parent.parent.parent / "data" / "dictionary",
            # Legacy locations
            Path.cwd() / "src" / "data" / "dictionary",
            Path(__file__).parent.parent.parent.parent.parent.parent
            / "data"
            / "dictionary",
            # User data locations
            Path.home() / "Documents" / "The Kinetic Alphabet" / "dictionary",
            (
                Path(os.getenv("APPDATA", "")) / "The Kinetic Alphabet" / "dictionary"
                if os.getenv("APPDATA")
                else None
            ),
        ]

        # Filter out None values
        possible_paths = [p for p in possible_paths if p is not None]

        for path in possible_paths:
            if path.exists() and path.is_dir():
                self.logger.info(f"Found dictionary at: {path}")
                self._dictionary_path = path
                return path

        # If no existing dictionary found, create default location
        default_path = Path.cwd() / "data" / "dictionary"
        default_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created default dictionary at: {default_path}")
        self._dictionary_path = default_path
        return default_path

    def set_dictionary_path(self, path: Path) -> None:
        """
        Set a custom dictionary path.

        Args:
            path: Custom path to use for dictionary
        """
        self._dictionary_path = path
        self.logger.info(f"Dictionary path set to: {path}")

    def get_cache_path(self) -> Path:
        """
        Get the path to the sequence card cache directory.

        Returns:
            Path to the cache directory
        """
        if self._cache_path is not None:
            return self._cache_path

        # Use platform-appropriate cache location
        if os.name == "nt":  # Windows
            cache_base = Path(
                os.getenv("LOCALAPPDATA", Path.home() / "AppData" / "Local")
            )
        else:  # Unix-like
            cache_base = Path.home() / ".cache"

        cache_path = cache_base / "The Kinetic Alphabet" / "sequence_cards"
        cache_path.mkdir(parents=True, exist_ok=True)

        self._cache_path = cache_path
        self.logger.info(f"Cache path: {cache_path}")
        return cache_path

    def set_cache_path(self, path: Path) -> None:
        """
        Set a custom cache path.

        Args:
            path: Custom path to use for cache
        """
        self._cache_path = path
        self.logger.info(f"Cache path set to: {path}")

    def get_export_path(self) -> Path:
        """
        Get the path for exporting sequence card images.

        Returns:
            Path to the export directory
        """
        # Use user's Pictures directory for exports
        if os.name == "nt":  # Windows
            try:
                # Try to get Pictures folder from environment first
                pictures_env = os.getenv("USERPROFILE")
                if pictures_env:
                    export_path = (
                        Path(pictures_env)
                        / "Pictures"
                        / "The Kinetic Alphabet"
                        / "sequence_card_images"
                    )
                else:
                    # Fallback to home directory
                    export_path = (
                        Path.home()
                        / "Pictures"
                        / "The Kinetic Alphabet"
                        / "sequence_card_images"
                    )
            except Exception:
                # Final fallback
                export_path = (
                    Path.home()
                    / "Pictures"
                    / "The Kinetic Alphabet"
                    / "sequence_card_images"
                )
        else:  # Unix-like
            export_path = (
                Path.home()
                / "Pictures"
                / "The Kinetic Alphabet"
                / "sequence_card_images"
            )

        try:
            export_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.logger.warning(f"Could not create export directory {export_path}: {e}")
            # Use temp directory as fallback
            export_path = self.get_temp_path() / "exports"
            export_path.mkdir(parents=True, exist_ok=True)

        return export_path

    def get_temp_path(self) -> Path:
        """
        Get a temporary directory for sequence card operations.

        Returns:
            Path to temporary directory
        """
        import tempfile

        temp_base = Path(tempfile.gettempdir())
        temp_path = temp_base / "tka_sequence_cards"
        temp_path.mkdir(parents=True, exist_ok=True)
        return temp_path

    def validate_dictionary_structure(
        self, dictionary_path: Optional[Path] = None
    ) -> bool:
        """
        Validate that the dictionary has the expected structure.

        Args:
            dictionary_path: Path to validate, or None to use default

        Returns:
            True if structure is valid, False otherwise
        """
        if dictionary_path is None:
            dictionary_path = self.get_dictionary_path()

        if not dictionary_path.exists() or not dictionary_path.is_dir():
            return False

        # Check for at least one word directory with PNG files
        word_dirs = [
            d
            for d in dictionary_path.iterdir()
            if d.is_dir() and not d.name.startswith(".")
        ]

        if not word_dirs:
            self.logger.warning(f"No word directories found in {dictionary_path}")
            return False

        # Check that at least one word directory has PNG files
        for word_dir in word_dirs[:5]:  # Check first 5 directories
            png_files = list(word_dir.glob("*.png"))
            if png_files:
                self.logger.info(
                    f"Dictionary structure validated: {len(word_dirs)} word directories found"
                )
                return True

        self.logger.warning(
            f"No PNG files found in word directories in {dictionary_path}"
        )
        return False

    def find_sequence_files(
        self, word: str, dictionary_path: Optional[Path] = None
    ) -> list[Path]:
        """
        Find all sequence files for a given word.

        Args:
            word: Word to search for
            dictionary_path: Dictionary path to search in

        Returns:
            List of paths to sequence files for the word
        """
        if dictionary_path is None:
            dictionary_path = self.get_dictionary_path()

        word_dir = dictionary_path / word
        if not word_dir.exists() or not word_dir.is_dir():
            return []

        # Find all PNG files that aren't thumbnails or temp files
        sequence_files = []
        for png_file in word_dir.glob("*.png"):
            if not png_file.name.startswith((".", "_", "thumb")):
                sequence_files.append(png_file)

        return sorted(sequence_files)

    def get_all_words(self, dictionary_path: Optional[Path] = None) -> list[str]:
        """
        Get all words available in the dictionary.

        Args:
            dictionary_path: Dictionary path to search in

        Returns:
            List of word names
        """
        if dictionary_path is None:
            dictionary_path = self.get_dictionary_path()

        if not dictionary_path.exists():
            return []

        words = []
        for item in dictionary_path.iterdir():
            if (
                item.is_dir()
                and not item.name.startswith(".")
                and item.name != "__pycache__"
            ):
                # Verify the directory has sequence files
                if any(item.glob("*.png")):
                    words.append(item.name)

        return sorted(words)

    def ensure_directory_exists(self, path: Path) -> bool:
        """
        Ensure a directory exists, creating it if necessary.

        Args:
            path: Directory path to ensure exists

        Returns:
            True if directory exists or was created successfully
        """
        try:
            path.mkdir(parents=True, exist_ok=True)
            return True
        except Exception as e:
            self.logger.error(f"Failed to create directory {path}: {e}")
            return False
