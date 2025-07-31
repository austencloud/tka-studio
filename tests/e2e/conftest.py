"""
Pytest configuration and fixtures for modern E2E tests.

This module provides shared fixtures for:
- QApplication lifecycle management
- TKA application setup and teardown
- Page object creation and initialization
- Common test data and utilities
"""

import logging
from pathlib import Path
import sys
import time
import warnings

import pytest

# Add src to path for imports (same as legacy setup)
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

# Configure logging for modern E2E tests
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

# Performance tracking
_test_performance = {}


@pytest.fixture(scope="session")
def qapp():
    """
    Create QApplication for the test session.

    This fixture ensures a single QApplication instance is shared
    across all tests in the session, preventing Qt initialization issues.
    """
    logger.info("FIXTURE: Creating QApplication for test session")

    app = QApplication.instance()
    if app is None:
        app = QApplication([])

    # Configure application for testing
    app.setQuitOnLastWindowClosed(False)

    yield app

    logger.info("FIXTURE: Cleaning up QApplication")
    app.quit()


@pytest.fixture(scope="function")
def tka_app(qapp):
    """
    Create TKA application instance for each test.

    This fixture provides a fresh TKA application instance for each test,
    ensuring test isolation and clean state.

    Returns:
        Tuple[Any, Any]: (app_instance, main_window)
    """
    logger.info("FIXTURE: Creating TKA application instance")

    try:
        # Use the proven application creation method from legacy tests
        from desktop.modern.main import create_application

        app, main_window = create_application()
        main_window.show()

        # Wait for full initialization (same as legacy tests)
        QTest.qWait(3000)

        logger.info("FIXTURE: TKA application ready")
        yield app, main_window

    except Exception as e:
        logger.error(f"FIXTURE: Failed to create TKA application: {e}")
        raise
    finally:
        # Cleanup
        logger.info("FIXTURE: Cleaning up TKA application")
        if "main_window" in locals() and main_window:
            main_window.close()
            QTest.qWait(500)


@pytest.fixture(scope="function")
def tka_pages(tka_app):
    """
    Create all page objects for the TKA application.

    This fixture provides a dictionary of initialized page objects
    for common TKA components, ready for use in tests.

    Returns:
        Dict[str, Any]: Dictionary of page objects
    """
    logger.info("FIXTURE: Creating page objects")

    app, main_window = tka_app

    # Import page objects
    from tests.e2e.framework.page_objects.construct_tab import ConstructTabPage

    # Create and initialize construct tab page object
    construct_tab = ConstructTabPage(main_window)

    # Navigate to construct tab to ensure it's active
    if not construct_tab.navigate_to_tab():
        logger.warning("FIXTURE: Failed to navigate to construct tab")

    # Create component page objects
    pages = {
        "construct_tab": construct_tab,
        "start_position_picker": construct_tab.get_start_position_picker(),
        "option_picker": construct_tab.get_option_picker(),
        "sequence_workbench": construct_tab.get_sequence_workbench(),
    }

    logger.info("FIXTURE: Page objects created successfully")
    return pages


@pytest.fixture(scope="function")
def workflow_steps(tka_pages):
    """
    Create step objects for common workflows.

    This fixture provides pre-configured step objects that encapsulate
    common workflow operations, making tests more readable and maintainable.

    Returns:
        Dict[str, Any]: Dictionary of step objects
    """
    logger.info("FIXTURE: Creating workflow step objects")

    # Import step definitions
    from tests.e2e.framework.steps.navigation_steps import NavigationSteps
    from tests.e2e.framework.steps.sequence_steps import SequenceSteps
    from tests.e2e.framework.steps.validation_steps import ValidationSteps

    pages = tka_pages

    # Get the main window from the construct tab page object
    main_window = pages["construct_tab"].parent

    steps = {
        "navigation": NavigationSteps(main_window),
        "sequence": SequenceSteps(pages["sequence_workbench"], pages["option_picker"]),
        "validation": ValidationSteps(pages["sequence_workbench"]),
    }

    logger.info("FIXTURE: Workflow step objects created")
    return steps


# Test data fixtures
@pytest.fixture(scope="session")
def test_positions():
    """Provide common test start positions."""
    return ["alpha1_alpha1", "beta5_beta5", "gamma11_gamma11"]


@pytest.fixture(scope="session")
def test_sequence_lengths():
    """Provide common test sequence lengths."""
    return [1, 2, 3, 5]


@pytest.fixture(scope="function")
def qtbot_enhanced(qtbot, tka_app):
    """
    Enhanced qtbot with TKA-specific setup and monitoring.

    This fixture combines pytest-qt's qtbot with TKA application setup,
    providing enhanced debugging and interaction capabilities.

    Returns:
        qtbot: Enhanced qtbot instance with TKA integration
    """
    logger.info("FIXTURE: Creating enhanced qtbot")

    app, main_window = tka_app

    # Register main window with qtbot for proper cleanup
    qtbot.addWidget(main_window)

    # Add TKA-specific helper methods to qtbot
    def wait_for_tka_component(component_name, timeout=5000):
        """Wait for a specific TKA component to be ready."""
        start_time = 0
        while start_time < timeout:
            # This would be customized based on your component discovery
            if main_window.findChild(object, component_name):
                return True
            qtbot.wait(100)
            start_time += 100
        return False

    def screenshot_on_failure(test_name):
        """Take screenshot for debugging failed tests."""
        try:
            screenshot_path = Path(f"test_screenshots/{test_name}_failure.png")
            screenshot_path.parent.mkdir(exist_ok=True)
            main_window.grab().save(str(screenshot_path))
            logger.info(f"Screenshot saved: {screenshot_path}")
        except Exception as e:
            logger.warning(f"Failed to save screenshot: {e}")

    # Attach helper methods to qtbot
    qtbot.wait_for_tka_component = wait_for_tka_component
    qtbot.screenshot_on_failure = screenshot_on_failure

    logger.info("FIXTURE: Enhanced qtbot ready")
    return qtbot


@pytest.fixture(autouse=True)
def performance_monitor(request):
    """
    Monitor test performance and flag slow tests.

    This fixture automatically tracks execution time for all tests
    and provides warnings for tests that exceed reasonable thresholds.
    """
    test_name = request.node.name
    start_time = time.time()

    logger.debug(f"Starting performance monitoring for: {test_name}")

    yield

    duration = time.time() - start_time
    _test_performance[test_name] = duration

    # Flag slow tests
    if duration > 30:
        warnings.warn(
            f"Slow test detected: {test_name} took {duration:.2f}s", UserWarning
        )
        logger.warning(f"PERFORMANCE: Slow test {test_name}: {duration:.2f}s")
    elif duration > 10:
        logger.info(f"PERFORMANCE: Test {test_name}: {duration:.2f}s")
    else:
        logger.debug(f"PERFORMANCE: Test {test_name}: {duration:.2f}s")


@pytest.fixture(scope="session")
def performance_report():
    """Generate performance report at end of session."""
    yield

    if _test_performance:
        logger.info("=== PERFORMANCE REPORT ===")
        sorted_tests = sorted(
            _test_performance.items(), key=lambda x: x[1], reverse=True
        )

        logger.info("Slowest tests:")
        for test_name, duration in sorted_tests[:5]:
            logger.info(f"  {test_name}: {duration:.2f}s")

        total_time = sum(_test_performance.values())
        avg_time = total_time / len(_test_performance)

        logger.info(f"Total test time: {total_time:.2f}s")
        logger.info(f"Average test time: {avg_time:.2f}s")
        logger.info(f"Total tests: {len(_test_performance)}")
        logger.info("=== END PERFORMANCE REPORT ===")
