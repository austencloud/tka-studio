#!/usr/bin/env python3
"""
Aggressive Function Remover

Removes large batches of unused functions from the TKA codebase.
Targets the safest categories first: standalone functions, getters/setters, utilities.
"""

# Standalone functions to remove (🔸 from detector output) - SAFEST
STANDALONE_FUNCTIONS = [
    ("src/desktop/legacy/core/application_context.py", "create_legacy_adapter", 119),
    ("src/desktop/legacy/core/dependency_container.py", "create_json_manager", 248),
    (
        "src/desktop/legacy/core/dependency_container.py",
        "create_dictionary_data_manager",
        280,
    ),
    (
        "src/desktop/legacy/core/dependency_container.py",
        "create_pictograph_data_loader",
        307,
    ),
    (
        "src/desktop/legacy/core/dependency_container.py",
        "create_letter_determiner",
        321,
    ),
    (
        "src/desktop/legacy/core/dependency_container.py",
        "register_additional_service",
        346,
    ),
    ("src/desktop/legacy/core_import_hook.py", "uninstall_core_import_hook", 119),
    ("src/desktop/legacy/core_imports.py", "enable_core_imports", 42),
    (
        "src/desktop/legacy/legacy_settings_manager/settings_logger.py",
        "log_settings_load",
        46,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/settings_logger.py",
        "log_settings_save",
        61,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/sequence_workbench/add_to_dictionary_manager/structural_variation_checker.py",
        "hash_sequence",
        16,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/main_background_widget/main_background_widget.py",
        "use_painter",
        22,
    ),
]

# Safe getter/setter methods - Very likely unused
SAFE_GETTERS_SETTERS = [
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "get_auto_builder_enabled",
        104,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "set_auto_builder_enabled",
        108,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "get_auto_save_enabled",
        145,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "get_include_start_position",
        156,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "set_include_start_position",
        160,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "get_columns_per_row",
        167,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "get_username",
        178,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "set_username",
        182,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "get_show_grid",
        193,
    ),
    (
        "src/desktop/legacy/interfaces/settings_manager_interface.py",
        "set_show_grid",
        197,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "get_date_sub_sort_method",
        29,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "set_date_sub_sort_method",
        33,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "get_browse_left_stack_index",
        91,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "set_browse_left_stack_index",
        94,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "get_browse_right_stack_index",
        97,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "set_browse_right_stack_index",
        100,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/browse_tab_settings.py",
        "set_browse_ratio",
        118,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/generate_tab_settings.py",
        "get_current_mode",
        29,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/generate_tab_settings.py",
        "set_current_mode",
        32,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "get_last_length",
        41,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "set_last_length",
        49,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "get_auto_cache",
        53,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "set_auto_cache",
        61,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "get_cache_max_size_mb",
        65,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "get_cache_max_age_days",
        78,
    ),
    (
        "src/desktop/legacy/legacy_settings_manager/sequence_card_tab_settings.py",
        "set_cache_max_age_days",
        87,
    ),
]

# Safe utility/validation methods - Usually helper functions
SAFE_UTILITIES = [
    (
        "src/desktop/legacy/main_window/main_widget/browse_tab/thumbnail_box/core/thumbnail_size_calculator.py",
        "calculate_display_size",
        83,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/browse_tab/thumbnail_box/core/thumbnail_size_calculator.py",
        "calculate_aspect_ratio_size",
        112,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/browse_tab/thumbnail_box/core/thumbnail_size_calculator.py",
        "get_size_for_zoom_level",
        198,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/browse_tab/thumbnail_box/thumbnail_image_label.py",
        "aspect_ratio",
        59,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/sequence_card_tab/components/display/scaling/aspect_ratio_manager.py",
        "validate_aspect_ratio",
        67,
    ),
    (
        "src/desktop/legacy/main_window/main_widget/sequence_card_tab/components/display/scaling/aspect_ratio_manager.py",
        "constrain_aspect_ratio",
        87,
    ),
    (
        "src/shared/application/services/data/conversion_utils.py",
        "convert_coordinates",
        35,
    ),
    (
        "src/shared/application/services/data/conversion_utils.py",
        "convert_color_format",
        71,
    ),
    ("src/shared/application/services/data/conversion_utils.py", "convert_units", 110),
    (
        "src/shared/application/services/layout/component_sizer.py",
        "calculate_responsive_dimensions",
        104,
    ),
    (
        "src/shared/application/services/layout/component_sizer.py",
        "calculate_container_based_size",
        154,
    ),
    (
        "src/shared/application/services/layout/component_sizer.py",
        "calculate_final_size_with_spacing",
        182,
    ),
    (
        "src/shared/application/services/layout/component_sizer.py",
        "get_size_constraints",
        216,
    ),
    (
        "src/shared/application/services/layout/component_sizer.py",
        "apply_responsive_sizing",
        228,
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
            if f"def {function_name}(" in line or f"def {function_name}(" in lines[i]:
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
            print(f"❌ Could not find function {function_name} in {file_path}")
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


def process_function_list(function_list: list, category_name: str) -> tuple[int, int]:
    """Process a list of functions and return success/failure counts."""
    print(f"\n🔹 Processing {category_name}...")
    removed_count = 0
    failed_count = 0

    for file_path, function_name, line_number in function_list:
        if remove_function_from_file(file_path, function_name, line_number):
            removed_count += 1
        else:
            failed_count += 1

    return removed_count, failed_count


def main():
    """Remove all functions in aggressive batches."""
    print("🚀 Starting AGGRESSIVE function removal...")
    print(
        f"📊 Target: {len(STANDALONE_FUNCTIONS) + len(SAFE_GETTERS_SETTERS) + len(SAFE_UTILITIES)} functions"
    )

    total_removed = 0
    total_failed = 0

    # Process standalone functions first (safest)
    removed, failed = process_function_list(
        STANDALONE_FUNCTIONS, "Standalone Functions"
    )
    total_removed += removed
    total_failed += failed

    # Process getters/setters
    removed, failed = process_function_list(SAFE_GETTERS_SETTERS, "Getters/Setters")
    total_removed += removed
    total_failed += failed

    # Process utilities
    removed, failed = process_function_list(SAFE_UTILITIES, "Utility Functions")
    total_removed += removed
    total_failed += failed

    print("\n🎯 AGGRESSIVE REMOVAL COMPLETE!")
    print(f"✅ Successfully removed: {total_removed} functions")
    print(f"❌ Failed to remove: {total_failed} functions")
    print(
        f"📊 Total processed: {len(STANDALONE_FUNCTIONS) + len(SAFE_GETTERS_SETTERS) + len(SAFE_UTILITIES)} functions"
    )
    print(
        f"🔥 Success rate: {(total_removed / (total_removed + total_failed) * 100):.1f}%"
    )


if __name__ == "__main__":
    main()
