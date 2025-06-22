#!/usr/bin/env python3
"""
Notification system for test failures.
"""

import subprocess
import sys
import json
from pathlib import Path


class NotificationSystem:
    """Handles various notification methods for test failures."""

    def __init__(self, config_file="scripts/notification_config.json"):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """Load notification configuration."""
        try:
            with open(config_file, encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"desktop_notifications": True, "sound_alerts": True}

    def notify_test_failure(self, test_name, error_details):
        """Send notifications for test failures."""
        if self.config.get("desktop_notifications"):
            self.send_desktop_notification(test_name, error_details)

        if self.config.get("sound_alerts"):
            self.play_alert_sound()

    def send_desktop_notification(self, test_name, error_details):
        """Send desktop notification (cross-platform)."""
        title = f"TKA Test Failed: {test_name}"
        message = (
            error_details[:100] + "..." if len(error_details) > 100 else error_details
        )

        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(
                    [
                        "osascript",
                        "-e",
                        f'display notification "{message}" with title "{title}"',
                    ],
                    check=False,
                )
            elif sys.platform == "win32":  # Windows
                try:
                    import plyer

                    plyer.notification.notify(title=title, message=message, timeout=10)
                except ImportError:
                    print(f"Desktop notification: {title} - {message}")
            else:  # Linux
                subprocess.run(["notify-send", title, message], check=False)
        except Exception as e:
            print(f"Failed to send desktop notification: {e}")

    def play_alert_sound(self):
        """Play alert sound."""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(
                    ["afplay", "/System/Library/Sounds/Sosumi.aiff"], check=False
                )
            elif sys.platform == "win32":  # Windows
                try:
                    import winsound

                    winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                except ImportError:
                    print("\a")  # Terminal bell
            else:  # Linux
                subprocess.run(
                    ["paplay", "/usr/share/sounds/alsa/Front_Left.wav"], check=False
                )
        except Exception:
            # Fallback: terminal bell
            print("\a")

    def notify_recovery(self):
        """Send notification when tests recover from failure."""
        if self.config.get("desktop_notifications"):
            self.send_desktop_notification("TKA Tests", "Tests are now passing again!")


def notify_if_tests_fail():
    """Example integration with your test runner."""
    notifier = NotificationSystem()

    # Run tests
    result = subprocess.run(
        ["python", "-m", "pytest", "tests/regression/"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        notifier.notify_test_failure("Regression Tests", result.stderr)


if __name__ == "__main__":
    # Test the notification system
    notifier = NotificationSystem()
    notifier.notify_test_failure(
        "Test Notification", "This is a test notification to verify the system works."
    )
    print("Test notification sent!")
