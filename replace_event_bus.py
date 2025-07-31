#!/usr/bin/env python3
"""
Script to replace all event bus usage in UIStateManager with Qt signals
"""

import re


def replace_event_bus_with_signals(file_path):
    with open(file_path) as f:
        content = f.read()

    # Remove the _setup_event_subscriptions method call
    content = re.sub(
        r"\s*# Subscribe to UI events\s*self\._setup_event_subscriptions\(\)",
        "",
        content,
    )

    # Pattern to match event bus publish calls
    pattern = r'(\s*)# Publish .* event\s*event = UIEvent\(\s*component="([^"]*)",\s*action="([^"]*)",\s*state_data=\{([^}]*)\},\s*source="[^"]*",?\s*\)\s*self\._event_bus\.publish\(event\)'

    def replace_with_signal(match):
        indent = match.group(1)
        component = match.group(2)
        action = match.group(3)
        state_data = match.group(4)

        # Map different event types to appropriate signals
        if component == "settings":
            return f"{indent}# Emit Qt signal for setting change\n{indent}self.setting_changed.emit(key, value)"
        elif component == "tab":
            return f"{indent}# Emit Qt signal for tab state change\n{indent}self.tab_state_changed.emit(tab_name, state)"
        elif "visibility" in action or "visible" in action:
            return f"{indent}# Emit Qt signal for visibility change\n{indent}self.component_visibility_changed.emit(component_name, visible)"
        elif "hotkey" in action:
            return f"{indent}# Emit Qt signal for hotkey\n{indent}self.hotkey_triggered.emit(hotkey_name)"
        else:
            return f'{indent}# Emit Qt signal for UI state change\n{indent}self.ui_state_changed.emit("{component}", state_data)'

    # Apply the replacement
    content = re.sub(
        pattern, replace_with_signal, content, flags=re.MULTILINE | re.DOTALL
    )

    # Remove any remaining _event_bus references
    content = re.sub(r"self\._event_bus[^=]*=.*\n", "", content)

    # Remove _setup_event_subscriptions method if it exists
    content = re.sub(
        r"def _setup_event_subscriptions\(self\).*?(?=def|\Z)",
        "",
        content,
        flags=re.DOTALL,
    )

    with open(file_path, "w") as f:
        f.write(content)


if __name__ == "__main__":
    replace_event_bus_with_signals(
        "src/shared/application/services/ui/ui_state_manager.py"
    )
    print("✅ Replaced event bus usage with Qt signals in UIStateManager")
