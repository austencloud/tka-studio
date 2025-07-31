#!/usr/bin/env python3
"""
Visual debugging script to test if pictographs are actually visible in the Learn Tab.
This script opens the actual application and checks visual properties.
"""

import os
import sys
import time

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QWidget


def debug_visual_pictographs():
    """Debug visual pictograph rendering in Learn Tab."""

    app = QApplication([])

    try:
        print("🔍 Starting visual pictograph debugging...")

        # Initialize the main application
        from desktop.modern.main import create_application

        result = create_application()

        # Handle tuple return (app, main_window) or just main_window
        if isinstance(result, tuple):
            app_instance, main_window = result
        else:
            main_window = result

        print("✅ Application created successfully")

        # Show the main window
        main_window.show()
        main_window.resize(1200, 800)

        print("✅ Main window shown")

        # Navigate to Learn Tab
        # Find the Learn Tab - it could be in different places depending on the architecture
        learn_tab = None

        # Try modern architecture first
        if hasattr(main_window, "tab_widget"):
            tab_widget = main_window.tab_widget
            # Look for Learn Tab by iterating through tabs
            for i in range(tab_widget.count()):
                widget = tab_widget.widget(i)
                if widget and (
                    "Learn" in str(type(widget).__name__)
                    or hasattr(widget, "lesson_selector")
                ):
                    learn_tab = widget
                    tab_widget.setCurrentIndex(i)
                    break

        # Try legacy architecture
        if not learn_tab and hasattr(main_window, "main_widget"):
            if hasattr(main_window.main_widget, "learn_tab"):
                learn_tab = main_window.main_widget.learn_tab
                # Navigate to learn tab in legacy architecture
                if hasattr(main_window.main_widget, "tab_widget"):
                    main_window.main_widget.tab_widget.setCurrentWidget(learn_tab)

        if not learn_tab:
            print("❌ Could not find Learn Tab")
            return

        print("✅ Navigated to Learn Tab")

        # Wait for UI to settle
        app.processEvents()
        time.sleep(1)

        # Check if Learn Tab is visible
        print(f"📋 Learn Tab visible: {learn_tab.isVisible()}")
        print(f"📋 Learn Tab size: {learn_tab.size()}")

        # Try to start a lesson
        lesson_selector = learn_tab.lesson_selector
        if lesson_selector and lesson_selector.isVisible():
            print("✅ Lesson selector found and visible")

            # Look for lesson buttons - need to find actual clickable buttons
            from PyQt6.QtWidgets import QAbstractButton

            lesson_buttons = lesson_selector.findChildren(QAbstractButton)
            lesson_buttons = [
                btn
                for btn in lesson_buttons
                if hasattr(btn, "text") and "Lesson" in str(btn.text())
            ]

            print(f"📚 Found {len(lesson_buttons)} lesson buttons")

            if lesson_buttons:
                # Click first lesson button
                first_lesson = lesson_buttons[0]
                print(f"🎯 Clicking lesson: {first_lesson.text()}")

                # Simulate click
                first_lesson.click()

                # Wait for lesson to load
                app.processEvents()
                time.sleep(2)

                # Check if lesson widget is now visible
                lesson_widget = learn_tab.lesson_widget
                print(f"📚 Lesson widget visible: {lesson_widget.isVisible()}")
                print(f"📚 Lesson widget size: {lesson_widget.size()}")

                # Check if question display exists
                if hasattr(lesson_widget, "question_display"):
                    question_display = lesson_widget.question_display
                    print(
                        f"❓ Question display visible: {question_display.isVisible()}"
                    )
                    print(f"❓ Question display size: {question_display.size()}")

                    # Try to force question display visible
                    print("🔧 Forcing question display visible...")
                    question_display.setVisible(True)
                    question_display.show()
                    app.processEvents()
                    print(f"❓ After forcing: {question_display.isVisible()}")

                    # Check if content widget exists
                    if (
                        hasattr(question_display, "content_widget")
                        and question_display.content_widget
                    ):
                        content_widget = question_display.content_widget
                        print(
                            f"📄 Content widget type: {type(content_widget).__name__}"
                        )
                        print(
                            f"📄 Content widget visible: {content_widget.isVisible()}"
                        )
                        print(f"📄 Content widget size: {content_widget.size()}")
                        print(f"📄 Content widget parent: {content_widget.parent()}")
                        print(
                            f"📄 Content widget window flags: {content_widget.windowFlags()}"
                        )

                        # Try to force content widget visible
                        print("🔧 Forcing content widget visible...")
                        content_widget.setVisible(True)
                        content_widget.show()
                        app.processEvents()
                        print(f"📄 After forcing: {content_widget.isVisible()}")

                        # Check if it has scene content
                        if hasattr(content_widget, "scene") and content_widget.scene:
                            scene = content_widget.scene
                            items = scene.items()
                            print(f"📄 Scene items: {len(items)}")
                            for i, item in enumerate(items[:3]):
                                print(f"    Item {i + 1}: {type(item).__name__}")

                        # Check and fix window flags if problematic
                        from PyQt6.QtCore import Qt

                        current_flags = content_widget.windowFlags()
                        print(f"📄 Current window flags: {current_flags}")

                        # Check if it has window flags that make it a separate window
                        if current_flags & Qt.WindowType.Window:
                            print("🔧 Widget has Window flag - removing it...")
                            # Remove window flags and set as widget
                            content_widget.setWindowFlags(Qt.WindowType.Widget)
                            content_widget.setParent(question_display)
                            app.processEvents()
                            print(
                                f"📄 New window flags: {content_widget.windowFlags()}"
                            )
                    else:
                        print("❌ No content widget found in question display")

                # Check if answer options exist
                if hasattr(lesson_widget, "answer_options"):
                    answer_options = lesson_widget.answer_options
                    print(f"🎯 Answer options visible: {answer_options.isVisible()}")
                    print(f"🎯 Answer options size: {answer_options.size()}")

                    # Try to force answer options visible
                    print("🔧 Forcing answer options visible...")
                    answer_options.setVisible(True)
                    answer_options.show()
                    app.processEvents()
                    print(f"🎯 After forcing: {answer_options.isVisible()}")

                    # Check for answer option widgets
                    answer_widgets = answer_options.findChildren(QWidget)
                    answer_pictographs = [
                        w
                        for w in answer_widgets
                        if "pictograph" in w.__class__.__name__.lower()
                    ]
                    print(
                        f"🎯 Found {len(answer_pictographs)} answer pictograph widgets"
                    )

                    for i, widget in enumerate(answer_pictographs[:3]):
                        print(
                            f"  Answer {i + 1}: {widget.__class__.__name__} - Visible: {widget.isVisible()}"
                        )

                        # Try to force answer widget visible
                        if not widget.isVisible():
                            print(f"🔧 Forcing answer widget {i + 1} visible...")
                            widget.setVisible(True)
                            widget.show()
                            app.processEvents()
                            print(f"  After forcing: {widget.isVisible()}")
                else:
                    print("❌ No answer options found")

                # Check for pictograph widgets
                print("🔍 Searching for pictograph widgets...")

                # Find all pictograph-related widgets
                all_widgets = main_window.findChildren(QWidget)
                pictograph_widgets = []
                learn_pictograph_widgets = []

                for widget in all_widgets:
                    widget_name = widget.__class__.__name__
                    if any(
                        term in widget_name.lower() for term in ["pictograph", "learn"]
                    ):
                        pictograph_widgets.append(widget)
                        if "learn" in widget_name.lower():
                            learn_pictograph_widgets.append(widget)

                print(f"🎨 Found {len(pictograph_widgets)} pictograph-related widgets")
                print(
                    f"🧠 Found {len(learn_pictograph_widgets)} Learn pictograph widgets"
                )

                for i, widget in enumerate(
                    pictograph_widgets[:10]
                ):  # Limit to first 10
                    print(f"  Widget {i + 1}: {widget.__class__.__name__}")
                    print(f"    Visible: {widget.isVisible()}")
                    print(f"    Size: {widget.size()}")
                    print(f"    Position: {widget.pos()}")
                    print(
                        f"    Parent: {widget.parent().__class__.__name__ if widget.parent() else 'None'}"
                    )

                    # Try to force visibility
                    if not widget.isVisible():
                        print("    🔧 Forcing widget visible...")
                        widget.setVisible(True)
                        widget.show()
                        widget.raise_()
                        app.processEvents()
                        print(f"    After forcing visible: {widget.isVisible()}")

                        # Check parent visibility chain
                        parent = widget.parent()
                        level = 1
                        while parent and level <= 5:
                            print(
                                f"    Parent {level}: {parent.__class__.__name__} - Visible: {parent.isVisible()}"
                            )
                            if not parent.isVisible():
                                print(f"    🔧 Making parent {level} visible...")
                                parent.setVisible(True)
                                parent.show()
                            parent = parent.parent()
                            level += 1

                    # Check if widget has content
                    if hasattr(widget, "scene"):
                        try:
                            scene = widget.scene()
                            if scene:
                                items = scene.items()
                                print(f"    Scene items: {len(items)}")
                                if items:
                                    print(
                                        f"    First item type: {type(items[0]).__name__}"
                                    )
                        except:
                            pass

                    # Try to capture widget as image to see if it has visual content
                    if (
                        widget.isVisible()
                        and widget.size().width() > 0
                        and widget.size().height() > 0
                    ):
                        try:
                            pixmap = widget.grab()
                            if not pixmap.isNull():
                                # Check if pixmap has non-transparent content
                                image = pixmap.toImage()
                                has_content = False

                                # Sample a few pixels to see if there's content
                                width, height = image.width(), image.height()
                                if width > 10 and height > 10:
                                    for x in range(5, width - 5, max(1, width // 10)):
                                        for y in range(
                                            5, height - 5, max(1, height // 10)
                                        ):
                                            pixel = image.pixelColor(x, y)
                                            if pixel.alpha() > 0:  # Has some opacity
                                                has_content = True
                                                break
                                        if has_content:
                                            break

                                print(f"    Has visual content: {has_content}")

                                # Save a screenshot for manual inspection
                                if has_content:
                                    filename = f"debug_widget_{i + 1}_{widget.__class__.__name__}.png"
                                    pixmap.save(filename)
                                    print(f"    Screenshot saved: {filename}")
                        except Exception as e:
                            print(f"    Screenshot failed: {e}")

                    print()

        else:
            print("❌ Lesson selector not found or not visible")

        # Show Learn pictograph widgets specifically if we found any
        if "learn_pictograph_widgets" in locals() and learn_pictograph_widgets:
            print("\n🧠 Learn Pictograph Widgets Details:")
            for i, widget in enumerate(learn_pictograph_widgets):
                print(f"  Learn Widget {i + 1}: {widget.__class__.__name__}")
                print(f"    Visible: {widget.isVisible()}")
                print(f"    Size: {widget.size()}")
                print(f"    Position: {widget.pos()}")
                if hasattr(widget, "scene"):
                    try:
                        scene = widget.scene()
                        if scene:
                            items = scene.items()
                            print(f"    Scene items: {len(items)}")
                            for j, item in enumerate(items[:5]):
                                print(f"      Item {j + 1}: {type(item).__name__}")
                    except Exception as e:
                        print(f"    Scene error: {e}")

        # Keep window open for manual inspection
        print("🔍 Window will stay open for 10 seconds for manual inspection...")

        # Set up timer to close after 10 seconds
        timer = QTimer()
        timer.timeout.connect(app.quit)
        timer.start(10000)  # 10 seconds

        # Run the application
        app.exec()

    except Exception as e:
        print(f"❌ Error during visual debugging: {e}")
        import traceback

        traceback.print_exc()

    print("🔍 Visual debugging completed")


if __name__ == "__main__":
    debug_visual_pictographs()
