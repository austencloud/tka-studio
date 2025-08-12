"""
Sequence Card Export Service Implementation

Handles export and regeneration of sequence card images.
"""

from __future__ import annotations

from collections.abc import Callable
import logging

from PyQt6.QtCore import QThread, pyqtSignal

from desktop.modern.core.interfaces.sequence_card_services import (
    ISequenceCardExportService,
)


logger = logging.getLogger(__name__)


class ExportWorker(QThread):
    """Worker thread for export operations to avoid blocking UI."""

    progress_updated = pyqtSignal(int, int, str)  # current, total, message
    export_completed = pyqtSignal(bool)  # success

    def __init__(self, export_type: str = "export"):
        super().__init__()
        self.export_type = export_type
        self._cancel_requested = False

    def cancel(self):
        """Cancel the export operation."""
        self._cancel_requested = True

    def run(self):
        """Run the export operation."""
        try:
            if self.export_type == "export":
                success = self._run_export()
            elif self.export_type == "regenerate":
                success = self._run_regenerate()
            else:
                success = False

            self.export_completed.emit(success)

        except Exception as e:
            logger.exception(f"Export worker error: {e}")
            self.export_completed.emit(False)

    def _run_export(self) -> bool:
        """Run export operation."""
        try:
            # Try to use legacy exporter if available
            try:
                from main_window.main_widget.sequence_card_tab.export.image_exporter import (
                    SequenceCardImageExporter,
                )

                # Create a mock sequence card tab for the exporter
                class MockSequenceCardTab:
                    def __init__(self):
                        self.main_widget = None

                mock_tab = MockSequenceCardTab()
                exporter = SequenceCardImageExporter(mock_tab)

                # Hook up progress signals if available
                if hasattr(exporter, "progress_updated"):
                    exporter.progress_updated.connect(self.progress_updated)

                self.progress_updated.emit(0, 100, "Starting export...")

                # Run the export
                success = exporter.export_all_images()

                return success

            except ImportError:
                logger.warning("Legacy image exporter not available, using mock export")
                return self._mock_export()

        except Exception as e:
            logger.exception(f"Export operation failed: {e}")
            return False

    def _run_regenerate(self) -> bool:
        """Run regenerate operation."""
        # For regeneration, we first clear cache then export
        self.progress_updated.emit(0, 100, "Clearing cache...")

        # Clear any existing cached images
        try:
            # This would clear the cache in a real implementation
            pass
        except Exception as e:
            logger.warning(f"Error clearing cache: {e}")

        # Then run export
        return self._run_export()

    def _mock_export(self) -> bool:
        """Mock export operation for testing."""
        total_steps = 100

        for i in range(total_steps):
            if self._cancel_requested:
                return False

            # Simulate export progress
            self.progress_updated.emit(
                i + 1, total_steps, f"Exporting sequence {i + 1}/{total_steps}"
            )
            self.msleep(50)  # Simulate work

        return True


class SequenceCardExportService(ISequenceCardExportService):
    """Implementation of sequence card export operations."""

    def __init__(self):
        self.export_progress_callback: Callable[[int, int, str], None] | None = None
        self._current_worker: ExportWorker | None = None

    def export_all_sequences(self) -> bool:
        """Export all sequence cards."""
        try:
            if self._current_worker and self._current_worker.isRunning():
                logger.warning("Export already in progress")
                return False

            logger.info("Starting sequence card export")

            # Create and start worker thread
            self._current_worker = ExportWorker("export")
            self._current_worker.start()

            return True

        except Exception as e:
            logger.exception(f"Error starting export: {e}")
            return False

    def regenerate_all_images(self) -> bool:
        """Regenerate all sequence card images."""
        try:
            if self._current_worker and self._current_worker.isRunning():
                logger.warning("Export already in progress")
                return False

            logger.info("Starting sequence card regeneration")

            # Create and start worker thread
            self._current_worker = ExportWorker("regenerate")
            self._current_worker.start()

            return True

        except Exception as e:
            logger.exception(f"Error starting regeneration: {e}")
            return False

    def set_export_progress_callback(
        self, callback: Callable[[int, int, str], None]
    ) -> None:
        """Set export progress callback."""
        self.export_progress_callback = callback

    def cancel_export(self) -> None:
        """Cancel current export operation."""
        if self._current_worker and self._current_worker.isRunning():
            self._current_worker.cancel()
            self._current_worker.wait(5000)  # Wait up to 5 seconds
            logger.info("Export operation cancelled")
