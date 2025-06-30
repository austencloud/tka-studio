#!/usr/bin/env python3
"""
TKA Application Factory Interactive Demo

This script demonstrates all application modes with practical examples,
showing how services behave differently in each mode.
"""

import sys
import time
import os
from pathlib import Path
from typing import Dict, Any

# Set UTF-8 encoding for Windows console
if sys.platform == "win32":
    os.environ["PYTHONIOENCODING"] = "utf-8"

# Add TKA modern src to path
tka_src_path = Path(__file__).parent.parent / "src" / "desktop" / "modern" / "src"
sys.path.insert(0, str(tka_src_path))

from core.application.application_factory import ApplicationFactory, ApplicationMode
from core.interfaces.core_services import (
    ISequenceDataService,
    ILayoutService,
    ISettingsService,
    IValidationService,
    ISequenceManagementService,
    IPictographManagementService,
    IUIStateManagementService,
)


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n--- {title} ---")


def demonstrate_mode(mode: str, description: str):
    """Demonstrate a specific application mode."""
    print_header(f"{mode.upper()} MODE DEMONSTRATION")
    print(f"Description: {description}")

    try:
        # Create application container
        print_section("Creating Application Container")
        start_time = time.time()
        container = ApplicationFactory.create_app(mode)
        creation_time = time.time() - start_time
        print(f"[OK] Container created in {creation_time:.4f} seconds")

        # Show available services
        services = container.get_registrations()
        print(f"Available services: {len(services)}")
        for service_interface in services.keys():
            print(f"   - {service_interface.__name__}")

        # Demonstrate service resolution and usage
        demonstrate_services(container, mode)

        return container

    except Exception as e:
        print(f"[ERROR] Failed to create {mode} application: {e}")
        import traceback

        traceback.print_exc()
        return None


def demonstrate_services(container, mode: str):
    """Demonstrate service usage for a given container."""

    # Test Sequence Data Service
    print_section("Sequence Data Service Demo")
    try:
        seq_service = container.resolve(ISequenceDataService)
        print(f"[OK] Resolved ISequenceDataService: {type(seq_service).__name__}")

        # Create a sequence
        sequence = seq_service.create_new_sequence("Demo Sequence")
        print(f"Created sequence: {sequence}")

        # Save and retrieve
        saved = seq_service.save_sequence(sequence)
        print(f"Sequence saved: {saved}")

        retrieved = seq_service.get_sequence_by_id(sequence["id"])
        print(f"Retrieved sequence: {retrieved is not None}")

        all_sequences = seq_service.get_all_sequences()
        print(f"Total sequences in storage: {len(all_sequences)}")

    except Exception as e:
        print(f"[ERROR] Sequence service error: {e}")

    # Test Layout Service
    print_section("Layout Service Demo")
    try:
        layout_service = container.resolve(ILayoutService)
        print(f"[OK] Resolved ILayoutService: {type(layout_service).__name__}")

        # Get window dimensions
        window_size = layout_service.get_main_window_size()
        workbench_size = layout_service.get_workbench_size()
        picker_size = layout_service.get_picker_size()

        print(f"[DISPLAY] Main window size: {window_size.width}x{window_size.height}")
        print(f"[TOOL] Workbench size: {workbench_size.width}x{workbench_size.height}")
        print(f"[TARGET] Picker size: {picker_size.width}x{picker_size.height}")

        # Test layout calculations
        layout_ratio = layout_service.get_layout_ratio()
        print(f"[RULER] Layout ratio: {layout_ratio}")

        # Calculate component sizes
        beat_size = layout_service.calculate_component_size("beat_frame", window_size)
        pictograph_size = layout_service.calculate_component_size(
            "pictograph", window_size
        )

        print(f"[MUSIC] Beat frame size: {beat_size.width}x{beat_size.height}")
        print(f"[ART] Pictograph size: {pictograph_size.width}x{pictograph_size.height}")

        # Test grid layout calculation
        grid_layout = layout_service.get_optimal_grid_layout(16, (1200, 800))
        print(
            f"[CHART] Optimal grid for 16 items: {grid_layout[0]} rows x {grid_layout[1]} cols"
        )

    except Exception as e:
        print(f"[ERROR] Layout service error: {e}")

    # Test Settings Service
    print_section("Settings Service Demo")
    try:
        settings_service = container.resolve(ISettingsService)
        print(f"[OK] Resolved ISettingsService: {type(settings_service).__name__}")

        # Test setting and getting values
        settings_service.set_setting("demo_setting", f"value_from_{mode}_mode")
        settings_service.set_setting("demo_number", 42)
        settings_service.set_setting("demo_list", [1, 2, 3])

        demo_setting = settings_service.get_setting("demo_setting")
        demo_number = settings_service.get_setting("demo_number")
        demo_list = settings_service.get_setting("demo_list")
        nonexistent = settings_service.get_setting("nonexistent", "default_value")

        print(f"[SETTINGS] Demo setting: {demo_setting}")
        print(f"[NUMBER] Demo number: {demo_number}")
        print(f"[LIST] Demo list: {demo_list}")
        print(f"[QUESTION] Nonexistent setting (with default): {nonexistent}")

        # Test save/load operations
        print("[SAVE] Testing save/load operations...")
        settings_service.save_settings()
        settings_service.load_settings()
        print("[OK] Save/load completed without errors")

    except Exception as e:
        print(f"[ERROR] Settings service error: {e}")


def compare_modes():
    """Compare behavior across different modes."""
    print_header("MODE COMPARISON DEMONSTRATION")

    modes_to_test = [
        (ApplicationMode.TEST, "Fast in-memory testing with mock services"),
        (ApplicationMode.HEADLESS, "Real business logic without UI components"),
        (ApplicationMode.PRODUCTION, "Full application with real services"),
    ]

    containers = {}

    # Create containers for each mode
    for mode, description in modes_to_test:
        try:
            print(f"\n[LAUNCH] Creating {mode} container...")
            start_time = time.time()
            container = ApplicationFactory.create_app(mode)
            creation_time = time.time() - start_time
            containers[mode] = container
            print(f"[OK] {mode} container created in {creation_time:.4f}s")
        except Exception as e:
            print(f"[ERROR] Failed to create {mode} container: {e}")
            containers[mode] = None

    # Compare sequence operations across modes
    print_section("Sequence Operations Comparison")
    for mode, container in containers.items():
        if container is None:
            continue

        try:
            seq_service = container.resolve(ISequenceDataService)

            # Time sequence creation
            start_time = time.time()
            sequence = seq_service.create_new_sequence(f"Test_{mode}")
            creation_time = time.time() - start_time

            # Time sequence save
            start_time = time.time()
            seq_service.save_sequence(sequence)
            save_time = time.time() - start_time

            print(
                f"{mode:12} | Create: {creation_time:.6f}s | Save: {save_time:.6f}s | ID: {sequence['id']}"
            )

        except Exception as e:
            print(f"{mode:12} | ERROR: {e}")

    # Compare layout calculations
    print_section("Layout Calculations Comparison")
    test_container_size = (1920, 1080)

    for mode, container in containers.items():
        if container is None:
            continue

        try:
            layout_service = container.resolve(ILayoutService)

            # Time layout calculation
            start_time = time.time()
            grid_layout = layout_service.get_optimal_grid_layout(
                16, test_container_size
            )
            calc_time = time.time() - start_time

            window_size = layout_service.get_main_window_size()

            print(
                f"{mode:12} | Grid: {grid_layout} | Window: {window_size.width}x{window_size.height} | Time: {calc_time:.6f}s"
            )

        except Exception as e:
            print(f"{mode:12} | ERROR: {e}")


def main():
    """Main demonstration function."""
    print_header("TKA APPLICATION FACTORY INTERACTIVE DEMO")
    print("This demo shows how different application modes work in practice.")
    print("Each mode uses different service implementations for different use cases.")

    # Demonstrate each mode individually
    test_container = demonstrate_mode(
        ApplicationMode.TEST,
        "Fast in-memory testing with mock services - perfect for AI agents",
    )

    headless_container = demonstrate_mode(
        ApplicationMode.HEADLESS,
        "Real business logic without UI - ideal for server-side processing",
    )

    production_container = demonstrate_mode(
        ApplicationMode.PRODUCTION,
        "Full application with real services - complete desktop experience",
    )

    # Compare modes side by side
    compare_modes()

    # Summary
    print_header("DEMONSTRATION SUMMARY")
    print("[OK] TEST MODE: Fast, predictable, isolated - perfect for automated testing")
    print("[OK] HEADLESS MODE: Real logic, no UI - ideal for batch processing")
    print("[OK] PRODUCTION MODE: Complete application - full desktop experience")
    print("\n[TARGET] The Application Factory enables easy switching between these modes")
    print("   based on your specific use case and environment requirements.")

    return {
        "test": test_container,
        "headless": headless_container,
        "production": production_container,
    }


if __name__ == "__main__":
    containers = main()
