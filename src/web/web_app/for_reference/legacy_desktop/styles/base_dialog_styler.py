from __future__ import annotations
# base_dialog_styler.py
from PyQt6.QtWidgets import QComboBox, QFrame, QLabel, QPushButton, QSpinBox, QWidget

from .dark_theme_styler import DarkThemeStyler  # your existing dark theme


class BaseDialogStyler:
    """
    Generic styling that can be applied to ANY QDialog
    without referencing .ui.sidebar or any custom stuff.
    """

    @staticmethod
    def apply_styles(dialog: QWidget) -> None:
        """
        Apply the dark mode & style each child widget (buttons, combos, etc.).
        """
        # 1) apply dark mode background + text color
        DarkThemeStyler.apply_dark_mode(dialog)

        # 2) define which widget types to style
        widget_types = {
            QPushButton: DarkThemeStyler.style_button,
            QLabel: DarkThemeStyler.style_label,
            QComboBox: DarkThemeStyler.style_combo_box,
            QSpinBox: DarkThemeStyler.style_spinbox,
            QFrame: DarkThemeStyler.style_frame,
        }

        # 3) for each widget type, apply the style function to all children
        for wtype, style_func in widget_types.items():
            for child in dialog.findChildren(wtype):
                style_func(child)
