# TKA Automated Testing Pipeline

This directory contains a comprehensive automated testing pipeline that provides immediate feedback when code changes break tests.

## 🎯 Quick Start

### 1. One-Time Setup (5 minutes)
```bash
# Run the setup script
python scripts/setup_automated_testing.py

# Or manually:
pip install pre-commit watchdog schedule pytest pytest-cov pytest-xdist pytest-qt
pre-commit install
```

### 2. Start Real-Time Testing
```bash
# Start file watcher (runs tests automatically when you save files)
python scripts/test_watcher.py

# Or run comprehensive tests manually
python scripts/run_automated_tests.py
```

### 3. VS Code Integration
- Use `Ctrl+Shift+P` → "Tasks: Run Task"
- Select "Start Test Watcher" for automatic testing
- Select "Run Automated Tests" for comprehensive testing

## 🔧 Components

### Core Scripts

- **`test_watcher.py`** - Watches files and runs relevant tests automatically
- **`run_automated_tests.py`** - Comprehensive test runner with detailed reporting
- **`notification_system.py`** - Cross-platform notifications for test failures
- **`health_monitor.py`** - Continuous monitoring (runs periodically)
- **`setup_automated_testing.py`** - One-time setup script

### Configuration Files

- **`.pre-commit-config.yaml`** - Pre-commit hooks configuration
- **`notification_config.json`** - Notification settings
- **`scripts/git-hooks/post-merge`** - Git hook for post-merge testing

### GitHub Actions

- **`.github/workflows/automated-testing.yml`** - CI/CD pipeline

## 🚀 Features

### Immediate Feedback
- Tests run automatically when you save Python files
- Desktop notifications for failures
- Sound alerts for immediate attention
- Cross-platform support (Windows, macOS, Linux)

### Smart Test Selection
- Regression tests run for any `src/` changes
- Unit tests run for service/application changes
- Related test files are automatically detected
- Critical tests run first to catch breaking changes

### Comprehensive Reporting
- Detailed test reports saved to `test_reports/`
- JSON format for integration with other tools
- Test counts, timing, and failure details
- CI/CD integration with GitHub Actions

### Multi-Level Protection
1. **File Watcher** - Real-time testing during development
2. **Pre-commit Hooks** - Prevent committing broken code
3. **Post-merge Hooks** - Verify pulled changes don't break tests
4. **CI/CD Pipeline** - Automated testing on push/PR
5. **Health Monitor** - Periodic checks to catch drift

## 📋 Test Categories

The system runs different test categories based on criticality:

### Critical Tests (Must Pass)
- **Regression Tests** (`tests/regression/bugs/`) - Prevent known bugs from returning
- **Specification Tests** (`tests/specification/`) - Core behavior verification

### Important Tests
- **Unit Tests** (`tests/unit/`) - Fast, isolated component tests
- **Integration Tests** (`tests/integration/`) - Component interaction tests

## 🔔 Notifications

Configure notifications in `scripts/notification_config.json`:

```json
{
  "desktop_notifications": true,
  "sound_alerts": true,
  "slack_webhook": "https://hooks.slack.com/...",
  "email": {
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "username": "your-email@gmail.com",
    "password": "your-app-password",
    "to_email": "developer@yourcompany.com"
  }
}
```

## 📊 Usage Examples

### Development Workflow
```bash
# 1. Start the watcher (in a separate terminal)
python scripts/test_watcher.py

# 2. Edit your code normally
# Tests run automatically when you save

# 3. Get immediate feedback
# ✅ Tests passed - continue coding
# ❌ Tests failed - fix immediately
```

### Manual Testing
```bash
# Run all automated tests
python scripts/run_automated_tests.py

# Run specific test categories
python -m pytest tests/regression/bugs/ -v
python -m pytest tests/unit/ -x --tb=short
python -m pytest tests/specification/ -v
```

### Continuous Monitoring
```bash
# Start health monitor (runs in background)
python scripts/health_monitor.py

# Monitors:
# - Every 30 minutes: Basic health check
# - Every hour: Regression tests
# - Daily at 9 AM: Comprehensive tests
```

## 🎮 VS Code Integration

The setup creates VS Code tasks accessible via `Ctrl+Shift+P` → "Tasks: Run Task":

- **Run Automated Tests** - Full test suite with reporting
- **Start Test Watcher** - Background file watching
- **Start Health Monitor** - Continuous monitoring

## 🚨 Troubleshooting

### Test Watcher Not Running
```bash
# Check if watchdog is installed
pip install watchdog

# Check file permissions
chmod +x scripts/test_watcher.py
```

### Pre-commit Hooks Not Working
```bash
# Reinstall hooks
pre-commit uninstall
pre-commit install

# Test hooks
pre-commit run --all-files
```

### Notifications Not Working
```bash
# Test notifications
python scripts/notification_system.py

# Install notification dependencies (Windows)
pip install plyer
```

### Git Hooks Not Running
```bash
# Check hook permissions
chmod +x .git/hooks/post-merge

# Test hook manually
.git/hooks/post-merge
```

## 🔧 Customization

### Adding New Test Categories
Edit `scripts/run_automated_tests.py`:

```python
# Add to critical_tests or important_tests
{
    'name': 'Your New Tests',
    'command': ['python', '-m', 'pytest', 'tests/your_category/', '-v'],
    'critical': False  # or True for critical tests
}
```

### Changing Watch Patterns
Edit `scripts/test_watcher.py`:

```python
# Modify get_test_commands() to add new patterns
if 'your_pattern/' in str(file_path):
    commands.append(['python', '-m', 'pytest', 'your/tests/', '-v'])
```

### Custom Notifications
Edit `scripts/notification_system.py` to add new notification methods.

## 📈 Performance

- **File Watcher**: ~2-second cooldown between test runs
- **Unit Tests**: Target <10 seconds total
- **Integration Tests**: Target <30 seconds total
- **Regression Tests**: Target <60 seconds total

## 🤝 Contributing

When adding new features:

1. Add appropriate tests to the correct category
2. Update the automation scripts if needed
3. Ensure the test watcher detects your changes
4. Test the notification system works

## 📚 Dependencies

Core dependencies installed by setup:
- `pre-commit` - Pre-commit hooks
- `watchdog` - File system monitoring
- `schedule` - Task scheduling
- `pytest` - Test framework
- `pytest-cov` - Coverage reporting
- `pytest-xdist` - Parallel test execution
- `pytest-qt` - Qt testing support

Optional dependencies:
- `plyer` - Cross-platform notifications (Windows)
- `requests` - Slack notifications
- `smtplib` - Email notifications (built-in)

---

**🎯 Result**: Any break in your code triggers immediate alerts across multiple channels, catching issues before they impact users!
