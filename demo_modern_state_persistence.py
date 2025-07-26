"""
Modern State Persistence Integration Demo

This demo shows how to integrate the new modern state persistence system
into your TKA application. It demonstrates:

1. Setting up the modern settings service with dependency injection
2. Migrating from legacy settings to modern CQRS patterns
3. Using the Memento pattern for state snapshots
4. Auto-save and session restoration
5. Integration with Qt application lifecycle

Run this demo to see the modern state persistence system in action!
"""

import sys
import logging
from pathlib import Path
from typing import Optional

# Add project paths
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

# Configure logging for demo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def demo_basic_setup():
    """
    Demo 1: Basic setup of the modern settings system.
    
    Shows how to create and configure the settings service with DI.
    """
    print("🔧 Demo 1: Basic Setup of Modern Settings System")
    print("-" * 50)
    
    try:
        # Import the registration function
        from desktop.modern.core.dependency_injection.settings_service_registration import (
            create_configured_settings_container
        )
        
        # Create a fully configured container
        print("📦 Creating DI container with all settings services...")
        container = create_configured_settings_container("TKA_Demo", "DemoApp")
        
        # Resolve the main settings service
        from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
        settings_service = container.resolve(ModernSettingsService)
        
        print("✅ Modern settings service created and configured!")
        print(f"📍 Settings file location: {settings_service.settings.fileName()}")
        
        return container, settings_service
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        raise


def demo_cqrs_operations(settings_service):
    """
    Demo 2: CQRS Command/Query operations.
    
    Shows the modern command/query separation pattern.
    """
    print("\n⚡ Demo 2: CQRS Command/Query Operations")
    print("-" * 40)
    
    try:
        # Command operations (writes)
        print("📝 Executing commands (write operations)...")
        
        # Single command
        success = settings_service.execute_setting_command("demo", "user_name", "DemoUser")
        print(f"   Set user_name: {success}")
        
        # Bulk commands
        bulk_settings = {
            "demo": {
                "theme": "dark",
                "auto_save": True,
                "language": "en"
            },
            "ui": {
                "show_tooltips": True,
                "panel_width": 300
            }
        }
        
        success = settings_service.execute_bulk_setting_command(bulk_settings)
        print(f"   Bulk command execution: {success}")
        
        # Query operations (reads)
        print("🔍 Executing queries (read operations)...")
        
        user_name = settings_service.query_setting("demo", "user_name")
        theme = settings_service.query_setting("demo", "theme")
        panel_width = settings_service.query_setting("ui", "panel_width", type_hint=int)
        
        print(f"   Retrieved user_name: {user_name}")
        print(f"   Retrieved theme: {theme}")
        print(f"   Retrieved panel_width: {panel_width}")
        
        # Section query
        demo_section = settings_service.query_section("demo")
        print(f"   Demo section contains {len(demo_section)} settings")
        
        print("✅ CQRS operations completed successfully!")
        
    except Exception as e:
        print(f"❌ CQRS demo failed: {e}")
        raise


def demo_individual_managers(container):
    """
    Demo 3: Individual settings managers.
    
    Shows how specialized managers handle specific setting types.
    """
    print("\n🎛️ Demo 3: Individual Settings Managers")
    print("-" * 38)
    
    try:
        # Get managers from container
        from desktop.modern.core.interfaces.settings_services import (
            IBackgroundSettingsManager,
            IVisibilitySettingsManager,
            IPropTypeSettingsManager,
            PropType
        )
        
        background_manager = container.resolve(IBackgroundSettingsManager)
        visibility_manager = container.resolve(IVisibilitySettingsManager)
        prop_manager = container.resolve(IPropTypeSettingsManager)
        
        # Background manager demo
        print("🌅 Background Manager:")
        available_backgrounds = background_manager.get_available_backgrounds()
        print(f"   Available backgrounds: {', '.join(available_backgrounds[:3])}...")
        
        current_bg = background_manager.get_current_background()
        print(f"   Current background: {current_bg}")
        
        # Change background
        background_manager.set_background("Starfield")
        new_bg = background_manager.get_current_background()
        print(f"   Changed to: {new_bg}")
        
        # Font color computation
        font_color = background_manager.get_current_font_color()
        print(f"   Recommended font color: {font_color}")
        
        # Visibility manager demo
        print("\n👁️ Visibility Manager:")
        letter_visible = visibility_manager.get_glyph_visibility("letter")
        print(f"   Letter glyphs visible: {letter_visible}")
        
        # Toggle visibility
        new_state = visibility_manager.toggle_glyph_visibility("vtg")
        print(f"   Toggled VTG glyphs to: {new_state}")
        
        # Get all visibility settings
        all_visibility = visibility_manager.get_all_visibility_settings()
        print(f"   Managing {len(all_visibility)} visibility settings")
        
        # Prop manager demo
        print("\n🎪 Prop Manager:")
        current_prop = prop_manager.get_current_prop_type()
        print(f"   Current prop type: {current_prop.value}")
        
        available_props = prop_manager.get_available_prop_types()
        prop_names = [prop.value for prop in available_props]
        print(f"   Available props: {', '.join(prop_names)}")
        
        # Cycle prop type
        next_prop = prop_manager.cycle_prop_type()
        print(f"   Cycled to: {next_prop.value}")
        
        print("✅ Individual managers working correctly!")
        
    except Exception as e:
        print(f"❌ Managers demo failed: {e}")
        raise


def demo_memento_pattern(settings_service):
    """
    Demo 4: Memento pattern for state snapshots.
    
    Shows how to create and restore complete application state.
    """
    print("\n💾 Demo 4: Memento Pattern State Snapshots")
    print("-" * 42)
    
    try:
        # Create some application state
        print("🏗️ Setting up application state...")
        settings_service.execute_setting_command("app", "current_tab", "sequence")
        settings_service.execute_setting_command("app", "zoom_level", 1.5)
        settings_service.execute_setting_command("workbench", "beat_count", 16)
        
        # Create state memento
        print("📸 Creating state snapshot (Memento)...")
        memento = settings_service.create_state_memento(
            current_tab="sequence",
            session_data={"demo": "session_data"}
        )
        
        print(f"   Snapshot created at: {memento.timestamp}")
        print(f"   Current tab: {memento.current_tab}")
        print(f"   Settings captured: {len(memento.settings_snapshot)} groups")
        
        # Serialize memento
        print("💾 Serializing memento to JSON...")
        memento_dict = memento.to_dict()
        print(f"   Serialized size: {len(str(memento_dict))} chars")
        
        # Save memento to file
        print("💿 Saving memento to file...")
        temp_file = Path("demo_state_snapshot.json")
        success = settings_service.save_state_memento(memento, temp_file)
        print(f"   Save success: {success}")
        
        # Load memento from file
        print("📂 Loading memento from file...")
        loaded_memento = settings_service.load_state_memento(temp_file)
        if loaded_memento:
            print(f"   Loaded memento with tab: {loaded_memento.current_tab}")
            print(f"   Timestamp: {loaded_memento.timestamp}")
        
        # Restore from memento
        print("♻️ Restoring state from memento...")
        success = settings_service.restore_from_memento(loaded_memento)
        print(f"   Restoration success: {success}")
        
        # Cleanup
        if temp_file.exists():
            temp_file.unlink()
            print("🧹 Cleaned up demo file")
        
        print("✅ Memento pattern demo completed!")
        
    except Exception as e:
        print(f"❌ Memento demo failed: {e}")
        raise


def demo_application_state_manager(container):
    """
    Demo 5: High-level Application State Manager.
    
    Shows the complete application state management orchestration.
    """
    print("\n🏗️ Demo 5: Application State Manager")
    print("-" * 35)
    
    try:
        # Create application state manager
        from desktop.modern.application.services.core.application_state_manager import (
            create_application_state_manager
        )
        
        print("🎯 Creating Application State Manager...")
        state_manager = create_application_state_manager(container)
        
        # Test state management features
        print("🖱️ Simulating user interactions...")
        state_manager.mark_user_interaction("button_click")
        state_manager.mark_user_interaction("menu_selection")
        state_manager.mark_user_interaction("tab_switch")
        
        # Get state statistics
        print("📊 Getting state statistics...")
        stats = state_manager.get_state_statistics()
        print(f"   Auto-save enabled: {stats.get('auto_save_enabled')}")
        print(f"   Settings service active: {stats.get('settings_service_active')}")
        print(f"   Session ID: {stats.get('session_id', 'None')[:8]}..." if stats.get('session_id') else "   Session ID: None")
        
        # Force state save
        print("💾 Force saving application state...")
        success = state_manager.force_save_state()
        print(f"   Save success: {success}")
        
        # Test state export/import
        print("📤 Testing state export...")
        export_file = Path("demo_app_state.json")
        success = state_manager.export_application_state(export_file)
        print(f"   Export success: {success}")
        
        if export_file.exists():
            print("📥 Testing state import...")
            success = state_manager.import_application_state(export_file)
            print(f"   Import success: {success}")
            
            # Cleanup
            export_file.unlink()
            print("🧹 Cleaned up demo file")
        
        print("✅ Application State Manager demo completed!")
        
    except Exception as e:
        print(f"❌ State manager demo failed: {e}")
        raise


def demo_migration_from_legacy():
    """
    Demo 6: Migration from legacy settings system.
    
    Shows how to migrate existing settings to the modern system.
    """
    print("\n🔄 Demo 6: Migration from Legacy Settings")
    print("-" * 40)
    
    try:
        # Simulate legacy settings data
        print("📦 Simulating legacy settings data...")
        legacy_settings = {
            "global/prop_type": "Staff",
            "global/background_type": "Snowfall", 
            "global/current_tab": "construct",
            "global/grid_mode": "diamond",
            "visibility/letter": True,
            "visibility/elemental": True,
            "visibility/vtg": False,
            "layout/default_sequence_length": 16,
        }
        
        print(f"   Legacy settings: {len(legacy_settings)} items")
        
        # Create modern settings service
        from desktop.modern.core.dependency_injection.settings_service_registration import (
            create_configured_settings_container
        )
        
        container = create_configured_settings_container("TKA_Migration", "MigrationDemo")
        from desktop.modern.application.services.settings.modern_settings_service import ModernSettingsService
        settings_service = container.resolve(ModernSettingsService)
        
        # Migrate legacy settings to modern format
        print("⚡ Migrating to modern CQRS format...")
        migration_map = {
            "global": {
                "prop_type": legacy_settings["global/prop_type"],
                "background_type": legacy_settings["global/background_type"],
                "current_tab": legacy_settings["global/current_tab"],
                "grid_mode": legacy_settings["global/grid_mode"],
            },
            "visibility": {
                "glyph_letter": legacy_settings["visibility/letter"],
                "glyph_elemental": legacy_settings["visibility/elemental"], 
                "glyph_vtg": legacy_settings["visibility/vtg"],
            },
            "layout": {
                "default_sequence_length": legacy_settings["layout/default_sequence_length"],
            }
        }
        
        success = settings_service.execute_bulk_setting_command(migration_map)
        print(f"   Migration success: {success}")
        
        # Verify migration with modern managers
        print("✅ Verifying migration with modern managers...")
        from desktop.modern.core.interfaces.settings_services import (
            IBackgroundSettingsManager,
            IVisibilitySettingsManager,
            IPropTypeSettingsManager
        )
        
        background_manager = container.resolve(IBackgroundSettingsManager)
        visibility_manager = container.resolve(IVisibilitySettingsManager)
        prop_manager = container.resolve(IPropTypeSettingsManager)
        
        # Check migrated values
        current_bg = background_manager.get_current_background()
        letter_visible = visibility_manager.get_glyph_visibility("letter")
        current_prop = prop_manager.get_current_prop_type()
        
        print(f"   Background: {current_bg} (expected: Snowfall)")
        print(f"   Letter visible: {letter_visible} (expected: True)")
        print(f"   Prop type: {current_prop.value} (expected: Staff)")
        
        # Test legacy compatibility methods
        print("🔗 Testing legacy compatibility methods...")
        current_tab = settings_service.get_current_tab()  # Legacy method
        print(f"   Current tab (legacy method): {current_tab}")
        
        settings_service.set_setting("legacy_test", "test_key", "test_value")  # Legacy method
        test_value = settings_service.get_setting("legacy_test", "test_key")  # Legacy method
        print(f"   Legacy get/set test: {test_value}")
        
        print("✅ Migration demo completed successfully!")
        
    except Exception as e:
        print(f"❌ Migration demo failed: {e}")
        raise


def demo_qt_integration():
    """
    Demo 7: Qt Application Integration.
    
    Shows how to integrate with Qt application lifecycle.
    """
    print("\n🖼️ Demo 7: Qt Application Integration")
    print("-" * 35)
    
    try:
        print("⚙️ Setting up Qt integration example...")
        
        # This would typically be done in your main application
        integration_code = '''
        # In your main.py or application startup:
        
        from PyQt6.QtWidgets import QApplication, QMainWindow
        from desktop.modern.application.services.core.application_state_manager import (
            integrate_with_application_startup
        )
        from desktop.modern.core.dependency_injection.settings_service_registration import (
            create_configured_settings_container
        )
        
        def main():
            app = QApplication(sys.argv)
            
            # Create main window
            main_window = QMainWindow()
            main_window.setWindowTitle("TKA - Kinetic Constructor")
            
            # Set up dependency injection
            container = create_configured_settings_container("TKA", "KineticConstructor")
            
            # Integrate state persistence
            state_manager = integrate_with_application_startup(container, main_window, app)
            
            # Your application will now automatically:
            # - Restore window position and state on startup
            # - Save state when user interacts with the app
            # - Persist state when the application closes
            
            main_window.show()
            return app.exec()
        '''
        
        print("📝 Integration code pattern:")
        print(integration_code)
        
        # Demonstrate key concepts
        print("🔑 Key integration points:")
        print("   1. Create DI container with settings services")
        print("   2. Set up ApplicationStateManager with main window")
        print("   3. Connect to Qt application lifecycle events")
        print("   4. Auto-save triggers on user interactions")
        print("   5. State persistence on application exit")
        
        # Show event connection pattern
        print("\n🔗 Event connection pattern:")
        event_code = '''
        # Connect state manager to your widgets
        def on_tab_changed(index):
            state_manager.mark_user_interaction("tab_change")
            
        def on_setting_changed():
            state_manager.mark_user_interaction("setting_change")
            
        # Connect to Qt signals
        tab_widget.currentChanged.connect(on_tab_changed)
        settings_dialog.accepted.connect(on_setting_changed)
        '''
        
        print(event_code)
        
        print("✅ Qt integration demo completed!")
        
    except Exception as e:
        print(f"❌ Qt integration demo failed: {e}")
        raise


def run_complete_demo():
    """Run the complete demonstration of the modern state persistence system."""
    
    print("🚀 Modern State Persistence System - Complete Demo")
    print("=" * 55)
    print("This demo shows how to use the new modern state persistence")
    print("system in your TKA application with clean architecture patterns.")
    print()
    
    try:
        # Demo 1: Basic setup
        container, settings_service = demo_basic_setup()
        
        # Demo 2: CQRS operations
        demo_cqrs_operations(settings_service)
        
        # Demo 3: Individual managers
        demo_individual_managers(container)
        
        # Demo 4: Memento pattern
        demo_memento_pattern(settings_service)
        
        # Demo 5: Application state manager
        demo_application_state_manager(container)
        
        # Demo 6: Migration from legacy
        demo_migration_from_legacy()
        
        # Demo 7: Qt integration
        demo_qt_integration()
        
        # Summary
        print("\n🎉 Demo Complete!")
        print("=" * 20)
        print("✅ All features demonstrated successfully!")
        print("\n📖 Next steps:")
        print("   1. Review the integration examples above")
        print("   2. Add settings service registration to your DI container")
        print("   3. Replace legacy settings calls with modern CQRS operations")
        print("   4. Set up ApplicationStateManager in your main window")
        print("   5. Connect user interactions to state management")
        print("\n📚 For more information, see:")
        print("   - desktop/modern/application/services/settings/ (implementations)")
        print("   - desktop/modern/core/interfaces/settings_services.py (interfaces)")
        print("   - desktop/modern/tests/services/test_modern_settings_service.py (tests)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_complete_demo()
    sys.exit(0 if success else 1)
