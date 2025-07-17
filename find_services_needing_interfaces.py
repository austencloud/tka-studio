import os
import re

# Find all service files
service_files = []
for root, dirs, files in os.walk("src/desktop/modern/src/application/services"):
    for file in files:
        if file.endswith(".py") and not file.startswith("__"):
            service_files.append(os.path.join(root, file))

# Check each service file for classes that don't have interfaces
services_needing_interfaces = []
for filepath in service_files:
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Find all class definitions
        class_matches = re.findall(
            r"^class\s+(\w+)(?:\([^)]*\))?:", content, re.MULTILINE
        )

        for class_name in class_matches:
            if (
                class_name.startswith("I")
                or class_name.endswith("Error")
                or class_name.endswith("Exception")
            ):
                continue

            # Check if there's a corresponding interface
            interface_name = f"I{class_name}"
            if interface_name not in content:
                services_needing_interfaces.append((filepath, class_name))
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print(f"Found {len(services_needing_interfaces)} services needing interfaces:")
for filepath, class_name in services_needing_interfaces:
    print(f"  {class_name} in {filepath}")
