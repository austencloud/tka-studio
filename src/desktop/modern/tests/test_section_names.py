"""
Test to verify section names are correct and header clicking works.
"""

from application.services.pictograph_pool_manager import initialize_pictograph_pool
from core.application.application_factory import ApplicationFactory
from presentation.tabs.construct.modern_construct_tab import ConstructTabWidget
from PyQt6.QtWidgets import QApplication


def test_section_names():
    """Test that section names are correct."""
    print("🧪 Testing Section Names and Header Functionality")
    print("=" * 60)

    # Create application
    app = QApplication.instance() or QApplication(sys.argv)

    try:
        # Create fresh container and construct tab
        container = ApplicationFactory.create_production_app()

        # Initialize pictograph pool
        try:
            initialize_pictograph_pool(container)
            print("✅ Pictograph pool initialized")
        except Exception as e:
            print(f"⚠️ Pool initialization failed: {e}")

        construct_tab = ConstructTabWidget(container)

        # Get option picker through layout manager
        option_picker = construct_tab.layout_manager.option_picker
        option_picker_widget = option_picker.option_picker_widget
        scroll_widget = (
            option_picker_widget.option_picker_scroll
        )  # This is the OptionPickerScroll

        print(f"🔍 Found {len(scroll_widget.sections)} sections")

        # Load some options first to make sections visible
        print("🔄 Loading options to make sections visible...")
        try:
            # Simulate start position selection to load options
            from domain.models.beat_data import BeatData
            from domain.models.pictograph_data import PictographData

            # Create a simple start position
            start_position = PictographData(
                letter="α", start_position="alpha1", end_position="alpha1"
            )
            start_beat = BeatData(
                beat_number=0, duration=0, pictograph_data=start_position
            )

            # Load options for this start position
            scroll_widget.load_options_from_sequence([start_beat])
            print("✅ Options loaded")
        except Exception as e:
            print(f"⚠️ Failed to load options: {e}")

        # Check section names
        for letter_type, section in scroll_widget.sections.items():
            header_text = section.header.type_button.label.text()
            print(f"📝 {letter_type}: '{header_text}'")

            # Check if section has pictographs
            pictograph_count = len(section.pictographs)
            print(f"   Pictographs loaded: {pictograph_count}")

            # Test header clicking
            print(f"🖱️ Testing header click for {letter_type}...")
            initial_visible = section.pictograph_frame.isVisible()
            print(f"   Initial visibility: {initial_visible}")

            # If section has pictographs, make it visible first
            if pictograph_count > 0 and not initial_visible:
                section.pictograph_frame.setVisible(True)
                print(f"   Made section visible for testing")
                initial_visible = True

            # Click the header
            section.header.type_button.clicked.emit()

            after_click_visible = section.pictograph_frame.isVisible()
            print(f"   After click visibility: {after_click_visible}")

            if initial_visible != after_click_visible:
                print(f"   ✅ Header click works - visibility toggled")
            else:
                print(f"   ❌ Header click failed - visibility unchanged")

            print()

        print("🎉 Section name and header test completed!")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    test_section_names()
