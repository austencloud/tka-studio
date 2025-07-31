#!/usr/bin/env python3
"""
Bulk Function Remover

Programmatically removes unused functions from the TKA codebase.
Uses the output from unused_function_detector.py to systematically clean up dead code.
"""

# List of safe method functions to remove (🔹 from detector output - getters/setters/utilities)
SAFE_METHODS_TO_REMOVE = [
    ("src/shared/application/services/core/types.py", "area", 29),
    ("src/shared/application/services/core/types.py", "distance_to", 59),
    ("src/shared/application/services/core/types.py", "top_left", 74),
    ("src/shared/application/services/core/types.py", "to_rgba_tuple", 139),
    (
        "src/shared/application/services/backgrounds/aurora/blob_animation.py",
        "reset",
        57,
    ),
    (
        "src/shared/application/services/backgrounds/aurora/sparkle_animation.py",
        "reset",
        36,
    ),
    (
        "src/shared/application/services/backgrounds/aurora/wave_effects.py",
        "get_current_state",
        28,
    ),
    ("src/shared/application/services/backgrounds/aurora/wave_effects.py", "reset", 36),
    (
        "src/shared/application/services/backgrounds/bubbles/bubble_physics.py",
        "reset",
        40,
    ),
    (
        "src/shared/application/services/backgrounds/bubbles/fish_movement.py",
        "is_fish_offscreen",
        16,
    ),
    (
        "src/shared/application/services/backgrounds/bubbles/fish_spawning.py",
        "reset",
        61,
    ),
    (
        "src/shared/application/services/backgrounds/snowfall/santa_movement.py",
        "reset",
        50,
    ),
    (
        "src/shared/application/services/backgrounds/snowfall/shooting_star.py",
        "reset",
        94,
    ),
    (
        "src/shared/application/services/backgrounds/snowfall/snowflake_physics.py",
        "reset",
        53,
    ),
    (
        "src/shared/application/services/backgrounds/starfield/comet_trajectory.py",
        "reset",
        114,
    ),
    (
        "src/shared/application/services/backgrounds/starfield/star_twinkling.py",
        "reset",
        55,
    ),
    ("src/shared/application/services/data/cache_manager.py", "get_position_cache", 45),
    ("src/shared/application/services/data/cache_manager.py", "set_position_cache", 51),
    ("src/shared/application/services/data/cache_manager.py", "get_sequence_cache", 57),
    ("src/shared/application/services/data/cache_manager.py", "set_sequence_cache", 63),
    (
        "src/shared/application/services/data/cache_manager.py",
        "get_conversion_cache",
        85,
    ),
    (
        "src/shared/application/services/data/cache_manager.py",
        "set_conversion_cache",
        91,
    ),
    ("src/shared/application/services/data/cache_manager.py", "clear_all", 101),
    (
        "src/shared/application/services/data/cache_manager.py",
        "clear_position_cache",
        115,
    ),
    (
        "src/shared/application/services/data/cache_manager.py",
        "clear_sequence_cache",
        121,
    ),
    (
        "src/shared/application/services/data/cache_manager.py",
        "clear_conversion_cache",
        133,
    ),
]

# List of standalone functions to remove (🔸 from detector output)
STANDALONE_FUNCTIONS_TO_REMOVE = [
    (
        "src/desktop/modern/presentation/components/shared/picker_title_section.py",
        "create_picker_title_section",
        13,
    ),
    (
        "src/desktop/modern/presentation/components/shared/picker_title_section.py",
        "update_picker_title_section",
        71,
    ),
    (
        "src/desktop/modern/presentation/components/start_position_picker/start_text_overlay.py",
        "add_start_text_to_pictograph",
        96,
    ),
    (
        "src/desktop/modern/presentation/components/start_position_picker/start_text_overlay.py",
        "remove_start_text_from_pictograph",
        116,
    ),
    (
        "src/desktop/modern/presentation/controllers/construct/infrastructure/event_integration.py",
        "create_event_integration",
        402,
    ),
    (
        "src/desktop/modern/presentation/controllers/construct/infrastructure/initialization_saga.py",
        "create_construct_tab_initialization_saga",
        514,
    ),
    (
        "src/desktop/modern/presentation/controllers/construct/infrastructure/service_mesh.py",
        "create_service_mesh_for_construct_tab",
        346,
    ),
    (
        "src/desktop/modern/presentation/controllers/construct/infrastructure/signal_integration_adapter.py",
        "create_signal_integration",
        255,
    ),
    (
        "src/desktop/modern/presentation/controllers/construct/qt_signal_coordinator.py",
        "create_signal_coordinator",
        191,
    ),
    (
        "src/desktop/modern/presentation/qt_integration/qt_compatibility.py",
        "qt_compat",
        363,
    ),
    (
        "src/desktop/modern/presentation/qt_integration/resource_management.py",
        "pooled_pen",
        438,
    ),
    (
        "src/desktop/modern/presentation/qt_integration/resource_management.py",
        "pooled_brush",
        446,
    ),
    (
        "src/desktop/modern/presentation/qt_integration/resource_management.py",
        "pooled_font",
        454,
    ),
    (
        "src/desktop/modern/presentation/qt_integration/threading_integration.py",
        "qt_thread_manager",
        480,
    ),
    (
        "src/desktop/modern/presentation/styles/design_system.py",
        "reset_design_system",
        407,
    ),
    (
        "src/desktop/modern/presentation/styles/design_system.py",
        "get_button_style",
        420,
    ),
    ("src/desktop/modern/presentation/styles/design_system.py", "get_panel_style", 427),
    ("src/desktop/modern/presentation/styles/design_system.py", "get_label_style", 434),
    (
        "src/desktop/modern/presentation/styles/mixins.py",
        "apply_button_style_to_widget",
        102,
    ),
    (
        "src/desktop/modern/presentation/styles/mixins.py",
        "apply_menu_bar_style_to_widget",
        112,
    ),
    (
        "src/desktop/modern/presentation/styles/mixins.py",
        "apply_dialog_style_to_widget",
        117,
    ),
    ("src/desktop/modern/ui/adapters/qt_geometry_adapter.py", "to_qsize", 151),
    ("src/desktop/modern/ui/adapters/qt_geometry_adapter.py", "from_qsize", 156),
    ("src/desktop/modern/ui/adapters/qt_geometry_adapter.py", "to_qpointf", 161),
    ("src/desktop/modern/ui/adapters/qt_geometry_adapter.py", "from_qpointf", 166),
    ("src/shared/application/services/core/types.py", "scale_size_to_fit", 335),
    ("src/shared/application/services/core/types.py", "calculate_center_position", 340),
    (
        "src/shared/application/services/layout/component_position_calculator.py",
        "decorator",
        21,
    ),
    (
        "src/shared/application/services/layout/component_position_calculator.py",
        "decorator",
        27,
    ),
    ("src/shared/application/services/layout/layout_types.py", "decorator", 33),
    ("src/shared/application/services/layout/layout_types.py", "decorator", 39),
    (
        "src/shared/application/services/layout/responsive_scaling_calculator.py",
        "decorator",
        19,
    ),
    (
        "src/shared/application/services/layout/responsive_scaling_calculator.py",
        "decorator",
        25,
    ),
    (
        "src/shared/application/services/pictograph/context_detection_service.py",
        "create_context_aware_scene",
        203,
    ),
    (
        "src/shared/application/services/ui/animation/modern_service_registration.py",
        "create_simple_animation_orchestrator",
        73,
    ),
    (
        "src/shared/application/services/ui/animation/modern_service_registration.py",
        "create_legacy_adapter",
        81,
    ),
    (
        "src/shared/application/services/ui/animation/service_registration.py",
        "setup_animation_services",
        58,
    ),
    (
        "src/shared/application/services/ui/animation/service_registration.py",
        "create_fade_orchestrator_for_testing",
        68,
    ),
    (
        "src/web/services/web_pictograph_service.py",
        "create_fastapi_pictograph_endpoints",
        449,
    ),
]


def find_function_in_file(
    file_path: str, function_name: str, line_number: int
) -> tuple[int, int] | None:
    """Find the start and end lines of a function in a file."""
    try:
        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Start searching around the given line number
        start_idx = max(0, line_number - 10)
        end_idx = min(len(lines), line_number + 50)

        function_start = None
        function_end = None

        # Look for the function definition
        for i in range(start_idx, end_idx):
            line = lines[i].strip()
            if f"def {function_name}(" in line:
                function_start = i
                break

        if function_start is None:
            return None

        # Find the end of the function by tracking indentation
        base_indent = len(lines[function_start]) - len(lines[function_start].lstrip())

        for i in range(function_start + 1, len(lines)):
            line = lines[i]
            if line.strip() == "":  # Skip empty lines
                continue

            current_indent = len(line) - len(line.lstrip())
            if current_indent <= base_indent and line.strip():
                function_end = i - 1
                break

        if function_end is None:
            function_end = len(lines) - 1

        return (function_start + 1, function_end + 1)  # Convert to 1-based

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None


def remove_function_from_file(
    file_path: str, function_name: str, line_number: int
) -> bool:
    """Remove a function from a file."""
    try:
        bounds = find_function_in_file(file_path, function_name, line_number)
        if not bounds:
            print(f"Could not find function {function_name} in {file_path}")
            return False

        start_line, end_line = bounds

        with open(file_path, encoding="utf-8") as f:
            lines = f.readlines()

        # Remove the function lines
        new_lines = lines[: start_line - 1] + lines[end_line:]

        with open(file_path, "w", encoding="utf-8") as f:
            f.writelines(new_lines)

        print(
            f"✅ Removed {function_name} from {file_path} (lines {start_line}-{end_line})"
        )
        return True

    except Exception as e:
        print(f"❌ Error removing {function_name} from {file_path}: {e}")
        return False


def main():
    """Remove all functions in both lists."""
    print("🚀 Starting bulk function removal...")

    removed_count = 0
    failed_count = 0

    # Process safe methods first
    print("🔹 Processing safe methods...")
    for file_path, function_name, line_number in SAFE_METHODS_TO_REMOVE:
        if remove_function_from_file(file_path, function_name, line_number):
            removed_count += 1
        else:
            failed_count += 1

    total_functions = len(SAFE_METHODS_TO_REMOVE)

    print("\n📊 Summary:")
    print(f"✅ Successfully removed: {removed_count} functions")
    print(f"❌ Failed to remove: {failed_count} functions")
    print(f"🎯 Total processed: {total_functions} functions")


if __name__ == "__main__":
    main()
