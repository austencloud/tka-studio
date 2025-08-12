"""
File-based Sequence Data Service for TKA

Provides persistent sequence data storage using JSON files.
"""
from __future__ import annotations

from datetime import datetime
import json
import logging
from pathlib import Path
from typing import Any

from desktop.modern.core.interfaces.core_services import ISequenceDataService


logger = logging.getLogger(__name__)


class FileBasedSequenceDataService(ISequenceDataService):
    """
    File-based implementation of ISequenceDataService.

    Stores sequences as JSON files in a data directory.
    Suitable for production and headless modes.
    """

    def __init__(self, data_dir: str = "data/sequences"):
        """
        Initialize with data directory.

        Args:
            data_dir: Directory to store sequence files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self._id_counter = self._get_next_id()
        logger.info(f"FileBasedSequenceDataService initialized with data_dir: {self.data_dir}")

    def _get_next_id(self) -> int:
        """Get the next available sequence ID."""
        existing_files = list(self.data_dir.glob("seq_*.json"))
        if not existing_files:
            return 0

        # Extract IDs from filenames
        ids = []
        for file_path in existing_files:
            try:
                id_str = file_path.stem.split("_")[1]
                ids.append(int(id_str))
            except (IndexError, ValueError):
                continue

        return max(ids, default=-1) + 1

    def _get_file_path(self, sequence_id: str) -> Path:
        """Get file path for a sequence ID."""
        return self.data_dir / f"{sequence_id}.json"

    def get_all_sequences(self) -> list[dict[str, Any]]:
        """Get all sequences from files."""
        sequences = []

        try:
            for file_path in self.data_dir.glob("*.json"):
                try:
                    with open(file_path, encoding='utf-8') as f:
                        sequence_data = json.load(f)
                        sequences.append(sequence_data)
                except (OSError, json.JSONDecodeError) as e:
                    logger.warning(f"Failed to load sequence from {file_path}: {e}")
                    continue
        except Exception as e:
            logger.exception(f"Error reading sequences directory: {e}")

        logger.debug(f"Loaded {len(sequences)} sequences from {self.data_dir}")
        return sequences

    def get_sequence_by_id(self, sequence_id: str) -> dict[str, Any] | None:
        """Get sequence by ID from file."""
        file_path = self._get_file_path(sequence_id)

        if not file_path.exists():
            logger.debug(f"Sequence file not found: {file_path}")
            return None

        try:
            with open(file_path, encoding='utf-8') as f:
                sequence_data = json.load(f)
            logger.debug(f"Loaded sequence {sequence_id} from {file_path}")
            return sequence_data
        except (OSError, json.JSONDecodeError) as e:
            logger.exception(f"Failed to load sequence {sequence_id}: {e}")
            return None

    def save_sequence(self, sequence_data: dict[str, Any]) -> bool:
        """Save sequence to file."""
        try:
            # Ensure sequence has an ID
            if "id" not in sequence_data:
                sequence_data["id"] = f"seq_{self._id_counter}"
                self._id_counter += 1

            # Add timestamp
            sequence_data["last_modified"] = datetime.now().isoformat()

            file_path = self._get_file_path(sequence_data["id"])

            # Write to temporary file first, then rename for atomic operation
            temp_path = file_path.with_suffix('.tmp')
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(sequence_data, f, indent=2, ensure_ascii=False)

            # Atomic rename
            temp_path.replace(file_path)

            logger.debug(f"Saved sequence {sequence_data['id']} to {file_path}")
            return True

        except Exception as e:
            logger.exception(f"Failed to save sequence: {e}")
            return False

    def delete_sequence(self, sequence_id: str) -> bool:
        """Delete sequence file."""
        file_path = self._get_file_path(sequence_id)

        if not file_path.exists():
            logger.warning(f"Cannot delete non-existent sequence: {sequence_id}")
            return False

        try:
            file_path.unlink()
            logger.debug(f"Deleted sequence {sequence_id} file: {file_path}")
            return True
        except Exception as e:
            logger.exception(f"Failed to delete sequence {sequence_id}: {e}")
            return False

    def create_new_sequence(self, name: str) -> dict[str, Any]:
        """Create new empty sequence."""
        sequence = {
            "id": f"seq_{self._id_counter}",
            "name": name,
            "beats": [],
            "length": 16,
            "created_at": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
        }
        self._id_counter += 1

        # Save immediately
        if self.save_sequence(sequence):
            logger.info(f"Created new sequence: {sequence['id']} - {name}")
            return sequence
        logger.error(f"Failed to save new sequence: {name}")
        return sequence
