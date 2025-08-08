"""
Glassmorphism styling for the settings dialog components.

This module contains all the CSS styling for the modern settings dialog,
implementing a beautiful glassmorphism design with translucent backgrounds,
proper borders, and smooth hover effects.
"""

from __future__ import annotations


class GlassmorphismStyles:
    """Central repository for all glassmorphism styling used in the settings dialog."""

    @staticmethod
    def get_dialog_styles() -> str:
        """Get the complete stylesheet for the settings dialog."""
        return """
            QDialog {
                background: transparent;
            }
              #glassmorphism_container {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 rgba(255, 255, 255, 0.25),
                    stop:0.5 rgba(255, 255, 255, 0.20),
                    stop:1 rgba(255, 255, 255, 0.18));
                border: 1px solid rgba(255, 255, 255, 0.35);
                border-radius: 24px;
            }

            #header_frame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 16px;
                margin-bottom: 8px;
                padding: 6px;
            }

            #dialog_title {
                color: rgba(255, 255, 255, 0.98);
                background: transparent;
                padding: 8px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 700;
                letter-spacing: -0.5px;
            }

            #close_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 22px;
                color: rgba(255, 255, 255, 0.90);
                font-size: 18px;
                font-weight: 600;
                font-family: "Inter", sans-serif;
            }

            #close_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 100, 100, 0.4),
                    stop:1 rgba(255, 80, 80, 0.3));
                border-color: rgba(255, 150, 150, 0.6);
                color: white;
            }

            #close_button:pressed {
                background: rgba(255, 60, 60, 0.5);
            }

            #settings_sidebar {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 16px;
                outline: none;
                selection-background-color: transparent;
                padding: 4px;
            }

            #settings_sidebar::item {
                background: transparent;
                border: none;
                padding: 12px 16px;
                margin: 1px 0px;
                border-radius: 12px;
                color: rgba(255, 255, 255, 0.80);
                font-weight: 500;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.2px;
            }

            #settings_sidebar::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(42, 130, 218, 0.45),
                    stop:1 rgba(42, 130, 218, 0.30));
                border: 1px solid rgba(42, 130, 218, 0.7);
                color: white;
                font-weight: 600;
            }

            #settings_sidebar::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.10));
                color: rgba(255, 255, 255, 0.95);
            }

            QStackedWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 16px;
                padding: 4px;
            }

            #button_frame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 16px;
                margin-top: 8px;
                padding: 6px;
            }

            #primary_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 0.9),
                    stop:0.5 rgba(42, 130, 218, 0.8),
                    stop:1 rgba(42, 130, 218, 0.7));
                border: 1px solid rgba(42, 130, 218, 1.0);
                border-radius: 14px;
                color: white;
                font-weight: 600;
                padding: 11px 24px;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.3px;
            }

            #primary_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 1.0),
                    stop:0.5 rgba(42, 130, 218, 0.9),
                    stop:1 rgba(42, 130, 218, 0.8));
            }

            #primary_button:pressed {
                background: rgba(42, 130, 218, 0.95);
            }

            #secondary_button {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 14px;
                color: rgba(255, 255, 255, 0.90);
                font-weight: 500;
                padding: 11px 20px;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                letter-spacing: 0.2px;
                margin-right: 8px;
            }

            #secondary_button:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.25),
                    stop:1 rgba(255, 255, 255, 0.15));
                color: white;
            }

            #secondary_button:pressed {
                background: rgba(255, 255, 255, 0.12);
            }

            /* Settings group styling with reduced spacing */
            QGroupBox {
                font-weight: 600;
                color: rgba(255, 255, 255, 0.95);
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 12px;
                margin-top: 8px;
                padding-top: 12px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 15px;
                letter-spacing: 0.3px;
            }

            QGroupBox::title {
                subcontrol-origin: margin;
                left: 16px;
                padding: 4px 12px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.18),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.25);
                border-radius: 8px;
            }

            /* Enhanced setting controls styling */
            QLabel[objectName="setting_label"] {
                color: rgba(255, 255, 255, 0.90);
                font-weight: 500;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 14px;
                letter-spacing: 0.2px;
            }

            QSpinBox, QDoubleSpinBox, QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.10));
                border: 1px solid rgba(255, 255, 255, 0.30);
                border-radius: 10px;
                padding: 10px 14px;
                color: white;
                font-size: 14px;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-weight: 500;
            }

            QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {
                border-color: rgba(42, 130, 218, 0.8);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.22),
                    stop:1 rgba(255, 255, 255, 0.15));
            }

            QCheckBox {
                color: rgba(255, 255, 255, 0.90);
                font-weight: 500;
                font-family: "Inter", "Segoe UI", sans-serif;
                font-size: 14px;
                letter-spacing: 0.2px;
            }

            QCheckBox::indicator {
                width: 20px;
                height: 20px;
                border: 2px solid rgba(255, 255, 255, 0.40);
                border-radius: 6px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.15),
                    stop:1 rgba(255, 255, 255, 0.08));
            }

            QCheckBox::indicator:checked {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(42, 130, 218, 0.8),
                    stop:1 rgba(42, 130, 218, 0.6));
                border-color: rgba(42, 130, 218, 1.0);
            }

            QCheckBox::indicator:hover {
                border-color: rgba(255, 255, 255, 0.6);
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(255, 255, 255, 0.22),
                    stop:1 rgba(255, 255, 255, 0.12));
            }
        """
