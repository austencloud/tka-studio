#!/usr/bin/env python3
"""
Continuous health monitoring for TKA application.
"""

import time
import schedule
import subprocess
from datetime import datetime

# Try to import our notification system
try:
    from .notification_system import NotificationSystem
except ImportError:
    # Fallback if running as script
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).parent))
    from notification_system import NotificationSystem


class HealthMonitor:
    """Monitors application health and runs tests periodically."""

    def __init__(self):
        self.notifier = NotificationSystem()
        self.last_failure_time = None

    def run_health_check(self):
        """Run a basic health check."""
        print(f"Running health check at {datetime.now().strftime('%H:%M:%S')}")

        # Run critical regression tests
        result = subprocess.run(
            ["python", "-m", "pytest", "tests/regression/bugs/", "-x", "--tb=short"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            print("[PASS] Health check passed")
            if self.last_failure_time:
                # Recovery notification
                self.notifier.notify_recovery()
                self.last_failure_time = None
        else:
            print("[FAIL] Health check failed")
            self.last_failure_time = datetime.now()
            self.notifier.notify_test_failure("Health Check", result.stderr)

    def start_monitoring(self):
        """Start continuous monitoring."""
        print("Starting TKA Health Monitor")

        # Schedule health checks
        schedule.every(30).minutes.do(self.run_health_check)  # Every 30 minutes
        schedule.every().hour.at(":00").do(self.run_health_check)  # Every hour
        schedule.every().day.at("09:00").do(
            self.run_comprehensive_tests
        )  # Daily comprehensive tests

        print("Scheduled health checks:")
        print("   - Every 30 minutes: Basic health check")
        print("   - Every hour: Health check")
        print("   - Daily at 9 AM: Comprehensive tests")

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def run_comprehensive_tests(self):
        """Run comprehensive test suite daily."""
        print("Running daily comprehensive tests")

        result = subprocess.run(
            ["python", "scripts/simple_test_runner.py"],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode != 0:
            self.notifier.notify_test_failure(
                "Daily Comprehensive Tests", result.stderr
            )


if __name__ == "__main__":
    monitor = HealthMonitor()
    monitor.start_monitoring()
