"""
Diagnostic test for pictograph scaling inconsistencies.

This test measures actual dimensions vs expected dimensions across all
pictograph contexts to identify scaling issues.
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont


def create_scaling_diagnostic():
    """Create diagnostic test for pictograph scaling."""

    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("TKA Pictograph Scaling Diagnostic")
    window.setGeometry(100, 100, 1200, 800)

    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    window.setCentralWidget(central_widget)

    # Title
    title = QLabel("🔍 TKA Pictograph Scaling Diagnostic Test")
    title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
    layout.addWidget(title)

    # Results container
    results_widget = QWidget()
    results_layout = QVBoxLayout(results_widget)
    layout.addWidget(results_widget)

    def run_diagnostic_tests():
        """Run all diagnostic tests and display results."""
        print("=" * 80)
        print("🔍 STARTING PICTOGRAPH SCALING DIAGNOSTIC")
        print("=" * 80)

        test_results = []

        # Test 1: Start Position Picker Scaling
        print("\n📍 TEST 1: START POSITION PICKER SCALING")
        print("-" * 50)
        start_pos_results = test_start_position_scaling(window)
        test_results.extend(start_pos_results)

        # Test 2: Option Picker Scaling
        print("\n🎯 TEST 2: OPTION PICKER SCALING")
        print("-" * 50)
        option_picker_results = test_option_picker_scaling(window)
        test_results.extend(option_picker_results)

        # Test 3: Learn Tab Scaling
        print("\n📚 TEST 3: LEARN TAB SCALING")
        print("-" * 50)
        learn_tab_results = test_learn_tab_scaling(window)
        test_results.extend(learn_tab_results)

        # Display summary
        print("\n" + "=" * 80)
        print("📊 DIAGNOSTIC SUMMARY")
        print("=" * 80)

        passed = sum(1 for r in test_results if r["status"] == "PASS")
        failed = sum(1 for r in test_results if r["status"] == "FAIL")

        print(f"✅ Tests Passed: {passed}")
        print(f"❌ Tests Failed: {failed}")
        print(f"📊 Total Tests: {len(test_results)}")

        # Show detailed results
        for result in test_results:
            status_icon = "✅" if result["status"] == "PASS" else "❌"
            print(f"{status_icon} {result['test_name']}: {result['message']}")

        # Update UI with results
        update_results_ui(results_layout, test_results)

        return test_results

    # Run tests after a short delay to ensure UI is ready
    QTimer.singleShot(500, run_diagnostic_tests)

    window.show()
    return window, app


def test_start_position_scaling(main_window):
    """Test start position picker scaling with direct views."""
    results = []

    try:
        from presentation.components.pictograph.views import create_start_position_view

        # Test different container sizes
        test_sizes = [120, 100, 80]

        for size in test_sizes:
            try:
                # Create direct start position view
                view = create_start_position_view(is_advanced=False)

                # Set container size
                view.setFixedSize(size, size)

                # Measure actual dimensions
                widget_size = view.size()
                actual_width = widget_size.width()
                actual_height = widget_size.height()

                # Check if square
                is_square = actual_width == actual_height == size

                result = {
                    "test_name": f"StartPositionView_{size}px",
                    "expected_size": f"{size}x{size}",
                    "actual_size": f"{actual_width}x{actual_height}",
                    "status": "PASS" if is_square else "FAIL",
                    "message": f"Expected {size}x{size}, got {actual_width}x{actual_height}",
                }
                results.append(result)

                print(
                    f"  📏 Direct View {size}px: {actual_width}x{actual_height} {'✅' if is_square else '❌'}"
                )

            except Exception as e:
                results.append(
                    {
                        "test_name": f"StartPositionView_{size}px",
                        "expected_size": f"{size}x{size}",
                        "actual_size": "ERROR",
                        "status": "FAIL",
                        "message": f"Error: {str(e)}",
                    }
                )
                print(f"  ❌ Direct View {size}px: Error - {e}")

    except Exception as e:
        results.append(
            {
                "test_name": "StartPositionView_Import",
                "expected_size": "N/A",
                "actual_size": "N/A",
                "status": "FAIL",
                "message": f"Import error: {str(e)}",
            }
        )
        print(f"❌ Start position view import error: {e}")

    return results


def test_option_picker_scaling(main_window):
    """Test option picker scaling."""
    results = []

    try:
        from presentation.components.option_picker.components.option_pictograph import (
            OptionPictograph,
        )

        # Test option picker scaling
        main_window_width = main_window.width()
        option_picker_width = 800  # Typical width

        # Calculate expected size using legacy formula
        size_option_1 = main_window_width // 16
        size_option_2 = option_picker_width // 8
        expected_size = max(size_option_1, size_option_2)

        # Apply border calculation
        border_width = max(1, int(expected_size * 0.015))
        expected_size = expected_size - (2 * border_width)
        expected_size = max(expected_size, 100)

        try:
            # Create option pictograph
            option = OptionPictograph()

            # Simulate the sizing that should happen
            option.setFixedSize(expected_size, expected_size)

            # Measure actual dimensions
            widget_size = option.size()
            actual_width = widget_size.width()
            actual_height = widget_size.height()

            # Check if matches expected
            is_correct = actual_width == actual_height == expected_size

            result = {
                "test_name": "OptionPicker_Sizing",
                "expected_size": f"{expected_size}x{expected_size}",
                "actual_size": f"{actual_width}x{actual_height}",
                "status": "PASS" if is_correct else "FAIL",
                "message": f"Expected {expected_size}x{expected_size}, got {actual_width}x{actual_height}",
            }
            results.append(result)

            print(
                f"  📏 Option Picker: Expected {expected_size}x{expected_size}, got {actual_width}x{actual_height} {'✅' if is_correct else '❌'}"
            )

        except Exception as e:
            results.append(
                {
                    "test_name": "OptionPicker_Sizing",
                    "expected_size": f"{expected_size}x{expected_size}",
                    "actual_size": "ERROR",
                    "status": "FAIL",
                    "message": f"Error: {str(e)}",
                }
            )
            print(f"  ❌ Option Picker: Error - {e}")

    except Exception as e:
        results.append(
            {
                "test_name": "OptionPicker_Import",
                "expected_size": "N/A",
                "actual_size": "N/A",
                "status": "FAIL",
                "message": f"Import error: {str(e)}",
            }
        )
        print(f"❌ Option picker import error: {e}")

    return results


def test_learn_tab_scaling(main_window):
    """Test learn tab scaling."""
    results = []

    try:
        from presentation.components.pictograph.pictograph_widget import (
            PictographWidget,
        )

        # Test learn tab pictograph scaling
        container_sizes = [200, 400, 600]  # Typical learn tab sizes

        for container_size in container_sizes:
            try:
                # Create pictograph widget
                widget = PictographWidget()

                # Set container size
                widget.setFixedSize(container_size, container_size)

                # Measure actual dimensions
                widget_size = widget.size()
                actual_width = widget_size.width()
                actual_height = widget_size.height()

                # Check if matches container
                is_correct = actual_width == actual_height == container_size

                result = {
                    "test_name": f"LearnTab_{container_size}px",
                    "expected_size": f"{container_size}x{container_size}",
                    "actual_size": f"{actual_width}x{actual_height}",
                    "status": "PASS" if is_correct else "FAIL",
                    "message": f"Expected {container_size}x{container_size}, got {actual_width}x{actual_height}",
                }
                results.append(result)

                print(
                    f"  📏 Learn Tab {container_size}px: {actual_width}x{actual_height} {'✅' if is_correct else '❌'}"
                )

            except Exception as e:
                results.append(
                    {
                        "test_name": f"LearnTab_{container_size}px",
                        "expected_size": f"{container_size}x{container_size}",
                        "actual_size": "ERROR",
                        "status": "FAIL",
                        "message": f"Error: {str(e)}",
                    }
                )
                print(f"  ❌ Learn Tab {container_size}px: Error - {e}")

    except Exception as e:
        results.append(
            {
                "test_name": "LearnTab_Import",
                "expected_size": "N/A",
                "actual_size": "N/A",
                "status": "FAIL",
                "message": f"Import error: {str(e)}",
            }
        )
        print(f"❌ Learn tab import error: {e}")

    return results


def update_results_ui(layout, results):
    """Update the UI with test results."""

    # Clear existing widgets
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)

    # Add results
    for result in results:
        status_color = "green" if result["status"] == "PASS" else "red"
        status_icon = "✅" if result["status"] == "PASS" else "❌"

        label = QLabel(f"{status_icon} {result['test_name']}: {result['message']}")
        label.setStyleSheet(f"color: {status_color}; padding: 2px;")
        layout.addWidget(label)


if __name__ == "__main__":
    window, app = create_scaling_diagnostic()
    sys.exit(app.exec())
