"""
Sequence JSON Exporter Service

Handles JSON export operations for sequences.
Follows the Single Responsibility Principle by focusing solely on
JSON serialization and formatting.
"""

from __future__ import annotations

import json
import logging
from typing import Any

from desktop.modern.core.interfaces.export_services import (
    ISequenceDataTransformer,
    ISequenceJsonExporter,
)
from desktop.modern.domain.models.sequence_data import SequenceData


logger = logging.getLogger(__name__)


class SequenceJsonExporter(ISequenceJsonExporter):
    """
    Service responsible for JSON export operations.

    Responsibilities:
    - Export sequences as JSON strings
    - Create metadata entries for JSON export
    - Format JSON output with proper indentation
    - Handle JSON serialization errors
    """

    def __init__(self, data_transformer: ISequenceDataTransformer):
        """
        Initialize the JSON exporter.

        Args:
            data_transformer: Service for transforming sequence data
        """
        self._data_transformer = data_transformer
        logger.debug("SequenceJsonExporter initialized")

    def export_to_json_string(self, sequence: SequenceData) -> tuple[bool, str]:
        """
        Export sequence as JSON string in legacy-compatible format.

        Produces JSON that matches the legacy current_sequence.json format
        for maximum compatibility with existing tools and workflows.

        Args:
            sequence: The sequence to export

        Returns:
            Tuple of (success, json_string_or_error_message)
        """
        try:
            if not sequence:
                return False, "No sequence data to export"

            # Transform sequence to legacy JSON format
            sequence_json = self._data_transformer.to_legacy_json_format(sequence)

            # Convert to formatted JSON string
            json_string = self.format_json_output(sequence_json)

            logger.info(
                f"Sequence JSON exported: {len(json_string)} characters, {len(sequence.beats)} beats"
            )
            return True, json_string

        except Exception as e:
            logger.error(f"JSON export failed: {e}")
            return False, f"JSON export failed: {e}"

    def format_json_output(self, data: list[dict[str, Any]]) -> str:
        """
        Format the data as a properly formatted JSON string.

        Args:
            data: The data to format as JSON

        Returns:
            Formatted JSON string with proper indentation
        """
        try:
            return json.dumps(data, indent=4, ensure_ascii=False)
        except Exception as e:
            logger.error(f"JSON formatting failed: {e}")
            # Fallback to basic JSON without formatting
            return json.dumps(data, ensure_ascii=False)
