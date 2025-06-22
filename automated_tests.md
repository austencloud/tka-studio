# Complete Guide to Automated Testing Implementation

## 🎯 **Overview: TKA Automated Testing Pipeline**

Automated testing means your tests run automatically when code changes, catching breaks immediately without manual intervention. TKA uses a **lifecycle-based testing approach** that prioritizes different test types based on their importance.

```
Code Change → Trigger → Tests Run → Results → Notifications
     ↓            ↓          ↓         ↓           ↓
   Git Push   Git Hook   pytest    Pass/Fail   Alert Dev
```

### **TKA Test Priority Hierarchy**

1. **🚨 CRITICAL**: Regression tests (prevent known bugs from returning)
2. **🎯 CORE**: Specification tests (enforce behavioral contracts)
3. **⚡ FAST**: Unit tests (isolated component testing)
4. **🔗 INTEGRATION**: Multi-component workflow tests
5. **🏗️ SCAFFOLDING**: Temporary debug tests (auto-expire)

## 🔧 **Level 1: Local Automation (Start Here)**

### **1. Pre-commit Hooks - Catch Issues Before Pushing**

Install pre-commit to run tests automatically before each commit:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml in your project root
```

**`.pre-commit-config.yaml`:**

```yaml
repos:
  - repo: local
    hooks:
      - id: pytest-fast
        name: Fast Tests
        entry: python -m pytest tests/unit tests/regression -x --tb=short
        language: system
        pass_filenames: false
        always_run: true

      - id: critical-tests
        name: Critical Regression Tests
        entry: python -m pytest tests/regression/bugs/ -v
        language: system
        pass_filenames: false
        always_run: true

  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

**Setup:**

```bash
# Install the hooks
pre-commit install

# Test it works
pre-commit run --all-files
```

**Result:** Now every `git commit` automatically runs your tests. If tests fail, the commit is rejected.

### **2. Git Hooks for Continuous Monitoring**

**`scripts/git-hooks/post-merge`** (runs after pulling changes):

```bash
#!/bin/bash
echo "🧪 Running tests after merge..."

# Run critical tests to ensure pulled changes didn't break anything
python -m pytest tests/regression/bugs/ tests/specification/ -x --tb=short

if [ $? -eq 0 ]; then
    echo "✅ All critical tests passed after merge"
else
    echo "❌ CRITICAL TESTS FAILED after merge!"
    echo "🚨 Your codebase may be broken!"

    # Optional: Send notification
    # python scripts/notify_dev.py "Tests failed after git merge"
fi
```

**Install:**

```bash
# Copy to git hooks directory
cp scripts/git-hooks/post-merge .git/hooks/
chmod +x .git/hooks/post-merge
```

### **3. File Watcher for Real-Time Testing**

**`scripts/test_watcher.py`:**

```python
#!/usr/bin/env python3
"""
Real-time test runner that watches for file changes and runs relevant tests.
"""

import time
import subprocess
import sys
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class TestHandler(FileSystemEventHandler):
    """Handles file changes and runs appropriate tests."""

    def __init__(self):
        self.last_run = 0
        self.cooldown = 2  # Seconds between test runs

    def on_modified(self, event):
        if event.is_directory:
            return

        # Only watch Python files
        if not event.src_path.endswith('.py'):
            return

        # Avoid running tests too frequently
        current_time = time.time()
        if current_time - self.last_run < self.cooldown:
            return

        self.last_run = current_time
        self.run_relevant_tests(event.src_path)

    def run_relevant_tests(self, changed_file):
        """Run tests relevant to the changed file."""
        file_path = Path(changed_file)
        print(f"\n🔍 File changed: {file_path}")

        # Determine which tests to run based on changed file
        test_commands = self.get_test_commands(file_path)

        for command in test_commands:
            print(f"🧪 Running: {' '.join(command)}")
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print("✅ Tests passed")
            else:
                print("❌ Tests failed!")
                print(result.stdout)
                print(result.stderr)

                # Optional: Send notification
                self.notify_failure(file_path, result.stderr)

    def get_test_commands(self, file_path):
        """Determine which tests to run based on the changed file."""
        commands = []

        # Always run regression tests for any core changes
        if 'src/' in str(file_path):
            commands.append([
                'python', '-m', 'pytest',
                'tests/regression/bugs/',
                '-x', '--tb=short'
            ])

        # Run specific test files if they exist
        if 'services/' in str(file_path):
            # Find related test file
            test_file = self.find_related_test_file(file_path)
            if test_file and test_file.exists():
                commands.append([
                    'python', '-m', 'pytest',
                    str(test_file),
                    '-v'
                ])

        # Run unit tests for any src changes
        if 'src/' in str(file_path):
            commands.append([
                'python', '-m', 'pytest',
                'tests/unit/',
                '-x', '--tb=short'
            ])

        return commands

    def find_related_test_file(self, source_file):
        """Find the test file that corresponds to a source file."""
        # Convert src/application/services/data/csv_data_service.py
        # to tests/unit/application/services/data/test_csv_data_service.py

        parts = source_file.parts
        if 'src' in parts:
            src_index = parts.index('src')
            rel_parts = parts[src_index + 1:]  # Remove 'src'

            # Build test path
            test_parts = ['tests', 'unit'] + list(rel_parts[:-1])
            test_file = test_parts + [f"test_{rel_parts[-1]}"]

            return Path('/'.join(test_file))

        return None

    def notify_failure(self, file_path, error_output):
        """Send notification when tests fail."""
        # You can implement various notification methods here
        print(f"\n🚨 ALERT: Tests failed for {file_path}")
        print("Consider implementing notifications via:")
        print("- Desktop notification")
        print("- Slack/Discord webhook")
        print("- Email alert")
        print("- Sound alert")


def main():
    """Start the file watcher."""
    print("🚀 Starting TKA Test Watcher...")
    print("👁️  Watching for file changes...")
    print("⏹️  Press Ctrl+C to stop")

    event_handler = TestHandler()
    observer = Observer()

    # Watch source code directories
    watch_dirs = ['src/', 'tests/']
    for watch_dir in watch_dirs:
        if Path(watch_dir).exists():
            observer.schedule(event_handler, watch_dir, recursive=True)
            print(f"📁 Watching: {watch_dir}")

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n🛑 Test watcher stopped")

    observer.join()


if __name__ == "__main__":
    main()
```

**Install dependencies and run:**

```bash
pip install watchdog
python scripts/test_watcher.py
```

**Result:** Now tests run automatically whenever you save a file!

## 🚀 **Level 2: Continuous Integration (CI/CD)**

### **1. GitHub Actions Workflow**

**`.github/workflows/automated-testing.yml`:**

```yaml
name: Automated Testing

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]
  schedule:
    # Run tests every day at 9 AM UTC
    - cron: "0 9 * * *"

jobs:
  test:
    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: [3.11, 3.12]

    steps:
      - uses: actions/checkout@v4

      - name: Set up Python ${{ matrix.python-version }}
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Cache dependencies
        uses: actions/cache@v3
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-xdist

      - name: Run regression tests (CRITICAL)
        run: |
          python -m pytest tests/regression/bugs/ -v --tb=short

      - name: Run specification tests (CORE BEHAVIOR)
        run: |
          python -m pytest tests/specification/ -v --tb=short

      - name: Run unit tests
        run: |
          python -m pytest tests/unit/ -x --tb=short --cov=src/

      - name: Run integration tests
        run: |
          python -m pytest tests/integration/ -x --tb=short

      - name: Upload coverage reports
        uses: codecov/codecov-action@v3
        if: matrix.python-version == '3.12'

      - name: Notify on failure
        if: failure()
        uses: 8398a7/action-slack@v3
        with:
          status: failure
          text: "🚨 TKA Tests Failed! Check the logs."
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### **2. Automated Testing Script for Local CI**

**`scripts/run_automated_tests.py`:**

```python
#!/usr/bin/env python3
"""
Comprehensive automated testing script that runs different test suites
and provides detailed reporting.
"""

import subprocess
import sys
import time
import json
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Optional


@dataclass
class TestResult:
    name: str
    passed: bool
    duration: float
    output: str
    error_output: str
    test_count: int = 0
    failure_count: int = 0


class AutomatedTestRunner:
    """Runs automated tests with comprehensive reporting."""

    def __init__(self):
        self.results: List[TestResult] = []
        self.start_time = datetime.now()

    def run_test_suite(self, name: str, command: List[str], critical: bool = False) -> TestResult:
        """Run a test suite and capture results."""
        print(f"\n🧪 Running {name}...")
        print(f"   Command: {' '.join(command)}")

        start_time = time.time()
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=Path.cwd()
        )
        duration = time.time() - start_time

        test_result = TestResult(
            name=name,
            passed=result.returncode == 0,
            duration=duration,
            output=result.stdout,
            error_output=result.stderr
        )

        # Extract test counts from pytest output
        if 'pytest' in command[0] or 'pytest' in command[1]:
            test_result.test_count, test_result.failure_count = self.parse_pytest_output(result.stdout)

        self.results.append(test_result)

        if test_result.passed:
            print(f"   ✅ {name} passed ({duration:.1f}s)")
            if test_result.test_count > 0:
                print(f"      Tests: {test_result.test_count}, Failures: {test_result.failure_count}")
        else:
            print(f"   ❌ {name} failed ({duration:.1f}s)")
            if critical:
                print(f"   🚨 CRITICAL TEST FAILURE!")
            if test_result.error_output:
                print(f"      Error: {test_result.error_output[:200]}...")

        return test_result

    def parse_pytest_output(self, output: str) -> tuple[int, int]:
        """Parse pytest output to extract test counts."""
        lines = output.split('\n')
        for line in lines:
            if 'passed' in line and ('failed' in line or 'error' in line):
                # Look for lines like "5 passed, 2 failed in 1.23s"
                parts = line.split()
                passed_count = 0
                failed_count = 0

                for i, part in enumerate(parts):
                    if part == 'passed' and i > 0:
                        try:
                            passed_count = int(parts[i-1])
                        except ValueError:
                            pass
                    elif part == 'failed' and i > 0:
                        try:
                            failed_count = int(parts[i-1])
                        except ValueError:
                            pass

                return passed_count + failed_count, failed_count
            elif 'passed in' in line:
                # Look for lines like "5 passed in 1.23s"
                parts = line.split()
                for i, part in enumerate(parts):
                    if part == 'passed' and i > 0:
                        try:
                            return int(parts[i-1]), 0
                        except ValueError:
                            pass

        return 0, 0

    def run_all_tests(self):
        """Run all automated test suites."""
        print("🚀 Starting Automated Test Suite")
        print("=" * 50)

        # Critical tests that must always pass
        critical_tests = [
            {
                'name': 'Regression Tests (Critical)',
                'command': ['python', '-m', 'pytest', 'tests/regression/bugs/', '-v', '--tb=short'],
                'critical': True
            },
            {
                'name': 'Specification Tests (Core Behavior)',
                'command': ['python', '-m', 'pytest', 'tests/specification/', '-v', '--tb=short'],
                'critical': True
            }
        ]

        # Important but not critical tests
        important_tests = [
            {
                'name': 'Unit Tests',
                'command': ['python', '-m', 'pytest', 'tests/unit/', '-x', '--tb=short'],
                'critical': False
            },
            {
                'name': 'Integration Tests',
                'command': ['python', '-m', 'pytest', 'tests/integration/', '-x', '--tb=short'],
                'critical': False
            }
        ]

        # Run critical tests first
        critical_failures = 0
        for test_config in critical_tests:
            result = self.run_test_suite(**test_config)
            if not result.passed:
                critical_failures += 1

        # If critical tests fail, stop here
        if critical_failures > 0:
            print(f"\n🚨 {critical_failures} CRITICAL TEST SUITES FAILED!")
            print("🛑 Stopping execution - fix critical issues first")
            self.generate_report()
            return False

        # Run important tests
        for test_config in important_tests:
            self.run_test_suite(**test_config)

        # Generate final report
        self.generate_report()
        return self.all_tests_passed()

    def all_tests_passed(self) -> bool:
        """Check if all tests passed."""
        return all(result.passed for result in self.results)

    def generate_report(self):
        """Generate a comprehensive test report."""
        total_duration = (datetime.now() - self.start_time).total_seconds()
        total_tests = sum(r.test_count for r in self.results)
        total_failures = sum(r.failure_count for r in self.results)
        passed_suites = sum(1 for r in self.results if r.passed)

        print("\n" + "=" * 60)
        print("📊 AUTOMATED TEST REPORT")
        print("=" * 60)
        print(f"🕐 Total Duration: {total_duration:.1f}s")
        print(f"📋 Test Suites: {len(self.results)}")
        print(f"✅ Passed Suites: {passed_suites}/{len(self.results)}")
        print(f"🧪 Total Tests: {total_tests}")
        print(f"❌ Total Failures: {total_failures}")

        print(f"\n📈 Suite Results:")
        for result in self.results:
            status = "✅" if result.passed else "❌"
            print(f"  {status} {result.name}: {result.test_count} tests, {result.failure_count} failures ({result.duration:.1f}s)")

        if not self.all_tests_passed():
            print(f"\n🚨 FAILURES DETECTED:")
            for result in self.results:
                if not result.passed:
                    print(f"\n❌ {result.name}:")
                    if result.error_output:
                        print(f"   Error: {result.error_output[:300]}...")
                    if "FAILED" in result.output:
                        # Extract failed test names
                        failed_tests = [line for line in result.output.split('\n') if 'FAILED' in line]
                        for failed_test in failed_tests[:5]:  # Show first 5 failures
                            print(f"   {failed_test}")

        # Save detailed report to file
        self.save_detailed_report()

        print(f"\n🎯 Overall Status: {'✅ ALL TESTS PASSED' if self.all_tests_passed() else '❌ SOME TESTS FAILED'}")

    def save_detailed_report(self):
        """Save detailed report to JSON file."""
        report_data = {
            'timestamp': self.start_time.isoformat(),
            'total_duration': (datetime.now() - self.start_time).total_seconds(),
            'overall_passed': self.all_tests_passed(),
            'results': [
                {
                    'name': r.name,
                    'passed': r.passed,
                    'duration': r.duration,
                    'test_count': r.test_count,
                    'failure_count': r.failure_count,
                    'output': r.output,
                    'error_output': r.error_output
                }
                for r in self.results
            ]
        }

        reports_dir = Path('test_reports')
        reports_dir.mkdir(exist_ok=True)

        report_file = reports_dir / f"test_report_{self.start_time.strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)

        print(f"📄 Detailed report saved: {report_file}")


def main():
    """Main entry point."""
    runner = AutomatedTestRunner()
    success = runner.run_all_tests()

    # Exit with appropriate code for CI/CD systems
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
```

**Usage:**

```bash
# Run comprehensive automated tests
python scripts/run_automated_tests.py

# Run specific test suite
python -m pytest tests/regression/bugs/ -v --tb=short
```

## 📱 **Level 3: Advanced Monitoring & Notifications**

### **1. Real-time Notifications**

**`scripts/notification_system.py`:**

````python
#!/usr/bin/env python3
"""
Notification system for test failures.
"""

import requests
import smtplib
import subprocess
import sys
from email.mime.text import MimeText
from pathlib import Path


class NotificationSystem:
    """Handles various notification methods for test failures."""

    def __init__(self, config_file='scripts/notification_config.json'):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """Load notification configuration."""
        import json
        try:
            with open(config_file) as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                'slack_webhook': None,
                'email': {
                    'smtp_server': 'smtp.gmail.com',
                    'smtp_port': 587,
                    'username': None,
                    'password': None,
                    'to_email': None
                },
                'desktop_notifications': True,
                'sound_alerts': True
            }

    def notify_test_failure(self, test_name, error_details):
        """Send notifications for test failures."""
        message = f"🚨 TKA Test Failure: {test_name}\n\nDetails:\n{error_details[:500]}..."

        if self.config.get('desktop_notifications'):
            self.send_desktop_notification(test_name, error_details)

        if self.config.get('sound_alerts'):
            self.play_alert_sound()

        if self.config.get('slack_webhook'):
            self.send_slack_notification(test_name, error_details)

        if self.config['email'].get('to_email'):
            self.send_email_notification(test_name, error_details)

    def send_desktop_notification(self, test_name, error_details):
        """Send desktop notification (cross-platform)."""
        title = f"TKA Test Failed: {test_name}"
        message = error_details[:100] + "..." if len(error_details) > 100 else error_details

        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run([
                    'osascript', '-e',
                    f'display notification "{message}" with title "{title}"'
                ])
            elif sys.platform == "win32":  # Windows
                import plyer
                plyer.notification.notify(
                    title=title,
                    message=message,
                    timeout=10
                )
            else:  # Linux
                subprocess.run(['notify-send', title, message])
        except Exception as e:
            print(f"Failed to send desktop notification: {e}")

    def play_alert_sound(self):
        """Play alert sound."""
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(['afplay', '/System/Library/Sounds/Sosumi.aiff'])
            elif sys.platform == "win32":  # Windows
                import winsound
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            else:  # Linux
                subprocess.run(['paplay', '/usr/share/sounds/alsa/Front_Left.wav'])
        except Exception:
            # Fallback: terminal bell
            print('\a')

    def send_slack_notification(self, test_name, error_details):
        """Send Slack notification via webhook."""
        webhook_url = self.config.get('slack_webhook')
        if not webhook_url:
            return

        payload = {
            "text": f"🚨 TKA Test Failure",
            "attachments": [
                {
                    "color": "danger",
                    "fields": [
                        {
                            "title": "Failed Test",
                            "value": test_name,
                            "short": True
                        },
                        {
                            "title": "Error Details",
                            "value": f"```{error_details[:800]}```",
                            "short": False
                        }
                    ]
                }
            ]
        }

        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            print(f"Failed to send Slack notification: {e}")

    def send_email_notification(self, test_name, error_details):
        """Send email notification."""
        email_config = self.config.get('email', {})

        if not all([email_config.get('username'), email_config.get('password'), email_config.get('to_email')]):
            return

        subject = f"TKA Test Failure: {test_name}"
        body = f"""
TKA Automated Test Failure Report

Failed Test: {test_name}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Error Details:
{error_details}

Please check the test logs and fix the issue.
        """

        try:
            msg = MimeText(body)
            msg['Subject'] = subject
            msg['From'] = email_config['username']
            msg['To'] = email_config['to_email']

            with smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port']) as server:
                server.starttls()
                server.login(email_config['username'], email_config['password'])
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email notification: {e}")


# Usage in your test scripts:
def notify_if_tests_fail():
    """Example integration with your test runner."""
    notifier = NotificationSystem()

    # Run tests
    result = subprocess.run(['python', '-m', 'pytest', 'tests/regression/'], capture_output=True, text=True)

    if result.returncode != 0:
        notifier.notify_test_failure("Regression Tests", result.stderr)
````

### **2. Health Check Monitoring**

**`scripts/health_monitor.py`:**

```python
#!/usr/bin/env python3
"""
Continuous health monitoring for TKA application.
"""

import time
import schedule
import subprocess
from datetime import datetime
from notification_system import NotificationSystem


class HealthMonitor:
    """Monitors application health and runs tests periodically."""

    def __init__(self):
        self.notifier = NotificationSystem()
        self.last_failure_time = None

    def run_health_check(self):
        """Run a basic health check."""
        print(f"🏥 Running health check at {datetime.now().strftime('%H:%M:%S')}")

        # Run critical regression tests
        result = subprocess.run([
            'python', '-m', 'pytest',
            'tests/regression/bugs/',
            '-x', '--tb=short'
        ], capture_output=True, text=True)

        if result.returncode == 0:
            print("✅ Health check passed")
            if self.last_failure_time:
                # Recovery notification
                self.notifier.notify_recovery()
                self.last_failure_time = None
        else:
            print("❌ Health check failed")
            self.last_failure_time = datetime.now()
            self.notifier.notify_test_failure("Health Check", result.stderr)

    def start_monitoring(self):
        """Start continuous monitoring."""
        print("🚀 Starting TKA Health Monitor")

        # Schedule health checks
        schedule.every(30).minutes.do(self.run_health_check)  # Every 30 minutes
        schedule.every().hour.at(":00").do(self.run_health_check)  # Every hour
        schedule.every().day.at("09:00").do(self.run_comprehensive_tests)  # Daily comprehensive tests

        print("⏰ Scheduled health checks:")
        print("   - Every 30 minutes: Basic health check")
        print("   - Every hour: Health check")
        print("   - Daily at 9 AM: Comprehensive tests")

        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute

    def run_comprehensive_tests(self):
        """Run comprehensive test suite daily."""
        print("🧪 Running daily comprehensive tests")

        result = subprocess.run([
            'python', 'scripts/run_automated_tests.py'
        ], capture_output=True, text=True)

        if result.returncode != 0:
            self.notifier.notify_test_failure("Daily Comprehensive Tests", result.stderr)


if __name__ == "__main__":
    monitor = HealthMonitor()
    monitor.start_monitoring()
```

## 🎯 **Quick Setup Guide**

### **1. Immediate Setup (5 minutes):**

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Start file watcher
pip install watchdog
python scripts/test_watcher.py
```

### **2. Advanced Setup (30 minutes):**

```bash
# Set up GitHub Actions (copy .github/workflows/automated-testing.yml)
# Configure notifications (copy scripts/notification_system.py)
# Set up health monitoring (copy scripts/health_monitor.py)
```

### **3. Configuration:**

**`scripts/notification_config.json`:**

```json
{
  "slack_webhook": "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK",
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password",
    "to_email": "developer@yourcompany.com"
  },
  "desktop_notifications": true,
  "sound_alerts": true
}
```

## 🚨 **What This Achieves**

With this setup, you get:

1. **Immediate Feedback:** Tests run automatically when you save files
2. **Pre-commit Protection:** Can't commit broken code
3. **Continuous Integration:** Tests run on every push/pull request
4. **Health Monitoring:** Periodic checks ensure your app stays healthy
5. **Multiple Notifications:** Desktop, Slack, email, sound alerts
6. **Comprehensive Reporting:** Detailed test reports and history

**Result:** Any break in your code triggers immediate alerts across multiple channels, catching issues before they impact users!

## 🎯 **Best Practices**

1. **Start Simple:** Begin with pre-commit hooks and file watching
2. **Test the Tests:** Make sure your test suite actually catches real issues
3. **Keep Tests Fast:** Slow tests won't be run frequently
4. **Monitor What Matters:** Focus on regression and specification tests for automated monitoring
5. **Don't Over-Notify:** Too many alerts lead to alert fatigue

This creates a robust safety net that automatically catches breaks as soon as they happen!
