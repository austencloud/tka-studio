from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)

if TYPE_CHECKING:
    from ..sequence_card_tab import SequenceCardTab


class RegenerateImagesDialog(QDialog):
    """Dialog for selective image regeneration by sequence length."""

    def __init__(self, sequence_card_tab: "SequenceCardTab"):
        super().__init__(sequence_card_tab)
        self.sequence_card_tab = sequence_card_tab
        self.selected_length: Optional[int] = None
        self.regenerate_all = False

        self.setWindowTitle("Regenerate Sequence Images")
        self.setModal(True)
        self.setFixedSize(400, 300)

        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        """Set up the dialog UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Title
        title_label = QLabel("Select Sequence Length to Regenerate")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Description
        desc_label = QLabel(
            "Choose which sequence length to regenerate images for.\n"
            "This will use your current export settings and force regeneration."
        )
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc_label)

        # Length selection
        length_layout = QHBoxLayout()
        length_layout.addWidget(QLabel("Sequence Length:"))

        self.length_combo = QComboBox()
        self.length_combo.addItem("All Lengths", -1)
        self.length_combo.addItem("─────────────", None)  # Visual separator

        # Add common sequence lengths
        common_lengths = [2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32]
        for length in common_lengths:
            self.length_combo.addItem(f"{length} beats", length)

        length_layout.addWidget(self.length_combo)
        length_layout.addStretch()
        layout.addLayout(length_layout)

        # Options
        self.force_regenerate_cb = QCheckBox("Force regeneration (ignore cache)")
        self.force_regenerate_cb.setChecked(True)  # Default to force regeneration
        layout.addWidget(self.force_regenerate_cb)

        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status text (initially hidden)
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(80)
        self.status_text.setVisible(False)
        self.status_text.setReadOnly(True)
        layout.addWidget(self.status_text)

        # Buttons
        button_layout = QHBoxLayout()

        self.cancel_button = QPushButton("Cancel")
        self.regenerate_button = QPushButton("Regenerate Images")
        self.regenerate_button.setDefault(True)

        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.regenerate_button)

        layout.addLayout(button_layout)

    def _connect_signals(self):
        """Connect dialog signals."""
        self.cancel_button.clicked.connect(self.reject)
        self.regenerate_button.clicked.connect(self._start_regeneration)

    def _start_regeneration(self):
        """Start the regeneration process."""
        # Get selected length
        length_data = self.length_combo.currentData()
        if length_data == -1:
            self.regenerate_all = True
            self.selected_length = None
        elif length_data is None:
            # Separator selected, do nothing
            return
        else:
            self.regenerate_all = False
            self.selected_length = length_data

        # Show progress UI
        self.progress_bar.setVisible(True)
        self.status_text.setVisible(True)
        self.regenerate_button.setEnabled(False)
        self.cancel_button.setText("Close")

        # Update status
        if self.regenerate_all:
            self.status_text.append("Starting regeneration for all sequence lengths...")
        else:
            self.status_text.append(
                f"Starting regeneration for {self.selected_length}-beat sequences..."
            )

        # Start regeneration
        self._perform_regeneration()

    def _perform_regeneration(self):
        """Perform the actual regeneration."""
        try:
            # Set force regenerate flag
            force_regen = self.force_regenerate_cb.isChecked()
            self.sequence_card_tab.image_exporter.force_regenerate = force_regen

            if self.regenerate_all:
                # Regenerate all images
                self.status_text.append("Regenerating all images...")
                self.sequence_card_tab.image_exporter.export_all_images()
            else:
                # Regenerate specific length
                self.status_text.append(
                    f"Regenerating {self.selected_length}-beat sequences..."
                )
                self.sequence_card_tab.image_exporter.export_images_by_length(
                    self.selected_length
                )

            # Reset force regenerate flag
            self.sequence_card_tab.image_exporter.force_regenerate = False

            # Update progress
            self.progress_bar.setValue(100)
            self.status_text.append("✅ Regeneration completed successfully!")

            # Refresh only the affected images in the display
            self._refresh_display()

        except Exception as e:
            self.status_text.append(f"❌ Error during regeneration: {str(e)}")
            self.sequence_card_tab.image_exporter.force_regenerate = False

    def _refresh_display(self):
        """Refresh the display with newly regenerated images."""
        try:
            # Only refresh if we're currently showing the affected length
            current_length = self.sequence_card_tab.nav_sidebar.selected_length

            if (
                self.regenerate_all
                or self.selected_length == current_length
                or current_length == 0
            ):
                # Refresh the current display
                self.status_text.append("Refreshing display...")
                if hasattr(self.sequence_card_tab, "printable_displayer"):
                    self.sequence_card_tab.printable_displayer.display_sequences(
                        current_length
                    )
                    self.sequence_card_tab._sync_pages_from_displayer()
                self.status_text.append("✅ Display refreshed!")
            else:
                self.status_text.append(
                    "ℹ️ Display not refreshed (different length currently shown)"
                )

        except Exception as e:
            self.status_text.append(f"⚠️ Warning: Could not refresh display: {str(e)}")

    def get_result(self) -> tuple[bool, Optional[int]]:
        """Get the dialog result."""
        return self.regenerate_all, self.selected_length
