"""
TKA Complete Interface Coverage Analysis

This script analyzes all services in the TKA application to identify
which services need interfaces for complete cross-platform coverage.
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
import os
from pathlib import Path
import re


@dataclass
class ServiceInfo:
    """Information about a service class."""

    name: str
    file_path: str
    category: str
    methods: list[str]
    dependencies: list[str]
    priority: str = "Unknown"
    has_interface: bool = False
    interface_file: str = ""


class ServiceAnalyzer:
    """Analyzes TKA services to identify interface requirements."""

    def __init__(self, src_path: str):
        self.src_path = Path(src_path)
        self.services: dict[str, ServiceInfo] = {}
        self.existing_interfaces: set[str] = set()
        self.service_categories = {
            "settings": ["settings"],
            "workbench": ["workbench"],
            "sequence": ["sequence"],
            "pictograph": ["pictograph"],
            "option_picker": ["option_picker"],
            "start_position": ["start_position"],
            "positioning": ["positioning"],
            "ui": ["ui"],
            "layout": ["layout"],
            "motion": ["motion"],
            "generation": ["generation"],
            "graph_editor": ["graph_editor"],
            "glyphs": ["glyphs"],
            "animation": ["animation"],
            "export": ["export"],
            "data": ["data"],
            "core": ["core"],
        }

    def analyze_all_services(self) -> dict[str, list[ServiceInfo]]:
        """Analyze all services and categorize them."""
        # First, identify existing interfaces
        self._identify_existing_interfaces()

        # Then scan all services
        self._scan_services()

        # Categorize by priority and interface status
        return self._categorize_services()

    def _identify_existing_interfaces(self) -> None:
        """Identify existing interfaces."""
        interfaces_path = self.src_path / "core" / "interfaces"
        if interfaces_path.exists():
            for file_path in interfaces_path.glob("*.py"):
                if file_path.name == "__init__.py":
                    continue

                try:
                    with open(file_path, encoding="utf-8") as f:
                        content = f.read()

                    # Find interface definitions
                    interface_matches = re.findall(
                        r"class\s+(I[A-Z][a-zA-Z]*)\s*\(", content
                    )
                    for interface_name in interface_matches:
                        self.existing_interfaces.add(interface_name)

                except Exception:
                    continue

    def _scan_services(self) -> None:
        """Scan all service files."""
        services_path = self.src_path / "application" / "services"

        for file_path in services_path.rglob("*.py"):
            if file_path.name == "__init__.py":
                continue

            try:
                self._analyze_service_file(file_path)
            except Exception:
                continue

    def _analyze_service_file(self, file_path: Path) -> None:
        """Analyze a single service file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            # Parse AST to find classes
            tree = ast.parse(content)

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    if self._is_service_class(node.name):
                        service_info = self._extract_service_info(
                            node, file_path, content
                        )
                        if service_info:
                            self.services[service_info.name] = service_info

        except Exception:
            pass

    def _is_service_class(self, class_name: str) -> bool:
        """Check if a class is a service class."""
        service_indicators = [
            "Service",
            "Manager",
            "Calculator",
            "Handler",
            "Coordinator",
            "Provider",
            "Factory",
            "Generator",
            "Validator",
            "Analyzer",
            "Processor",
            "Controller",
            "Orchestrator",
            "Registry",
            "Repository",
            "Persister",
            "Loader",
            "Transformer",
            "Adapter",
            "Mapper",
            "Matcher",
            "Selector",
            "Updater",
        ]

        return any(indicator in class_name for indicator in service_indicators)

    def _extract_service_info(
        self, class_node: ast.ClassDef, file_path: Path, content: str
    ) -> ServiceInfo:
        """Extract information about a service class."""
        # Get methods
        methods = []
        for node in class_node.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                methods.append(node.name)

        # Determine category
        category = self._determine_category(file_path)

        # Check if interface exists
        interface_name = f"I{class_node.name}"
        has_interface = interface_name in self.existing_interfaces

        # Determine priority
        priority = self._determine_priority(class_node.name, category, methods)

        return ServiceInfo(
            name=class_node.name,
            file_path=str(file_path),
            category=category,
            methods=methods,
            dependencies=self._extract_dependencies(content),
            priority=priority,
            has_interface=has_interface,
            interface_file=(
                f"{category}_services.py" if not has_interface else "existing"
            ),
        )

    def _determine_category(self, file_path: Path) -> str:
        """Determine the category of a service based on its path."""
        path_parts = file_path.parts

        for category, keywords in self.service_categories.items():
            if any(keyword in str(file_path).lower() for keyword in keywords):
                return category

        return "misc"

    def _determine_priority(
        self, class_name: str, category: str, methods: list[str]
    ) -> str:
        """Determine the priority level for interfacing this service."""
        # High priority services
        high_priority_patterns = [
            "State",
            "Session",
            "Export",
            "Import",
            "Clipboard",
            "Storage",
            "Persistence",
            "Cache",
            "Repository",
            "Data",
            "CSV",
            "JSON",
            "Thumbnail",
            "Image",
            "Render",
            "Scale",
            "Transform",
        ]

        # Medium priority services
        medium_priority_patterns = [
            "Layout",
            "Position",
            "Size",
            "Dimension",
            "Calculation",
            "Math",
            "Validation",
            "Analysis",
            "Detection",
            "Matching",
            "Selection",
        ]

        # Low priority services
        low_priority_patterns = [
            "Animation",
            "Effect",
            "Visual",
            "Display",
            "UI",
            "Widget",
            "Event",
            "Handler",
            "Registry",
            "Pool",
            "Factory",
        ]

        class_lower = class_name.lower()

        if any(pattern.lower() in class_lower for pattern in high_priority_patterns):
            return "HIGH"
        if any(pattern.lower() in class_lower for pattern in medium_priority_patterns):
            return "MEDIUM"
        if any(pattern.lower() in class_lower for pattern in low_priority_patterns):
            return "LOW"
        return "MEDIUM"  # Default to medium

    def _extract_dependencies(self, content: str) -> list[str]:
        """Extract dependencies from service content."""
        dependencies = []

        # Look for constructor dependencies
        constructor_match = re.search(r"def __init__\(self[^)]*\):", content)
        if constructor_match:
            # Extract parameter names
            params = re.findall(r"(\w+):\s*I?[A-Z]\w*", constructor_match.group(0))
            dependencies.extend(params)

        return dependencies

    def _categorize_services(self) -> dict[str, list[ServiceInfo]]:
        """Categorize services by interface status and priority."""
        result = {
            "needs_interface_high": [],
            "needs_interface_medium": [],
            "needs_interface_low": [],
            "has_interface": [],
            "by_category": {},
        }

        for service in self.services.values():
            # By interface status and priority
            if service.has_interface:
                result["has_interface"].append(service)
            elif service.priority == "HIGH":
                result["needs_interface_high"].append(service)
            elif service.priority == "MEDIUM":
                result["needs_interface_medium"].append(service)
            else:
                result["needs_interface_low"].append(service)

            # By category
            if service.category not in result["by_category"]:
                result["by_category"][service.category] = []
            result["by_category"][service.category].append(service)

        return result

    def generate_report(self) -> str:
        """Generate a comprehensive report."""
        categorized = self.analyze_all_services()

        report = []
        report.append("# TKA Complete Interface Coverage Analysis")
        report.append("=" * 50)

        # Summary
        total_services = len(self.services)
        has_interface = len(categorized["has_interface"])
        needs_interface = total_services - has_interface

        report.append("\n## 📊 Summary")
        report.append(f"- **Total Services Found**: {total_services}")
        report.append(f"- **Services with Interfaces**: {has_interface}")
        report.append(f"- **Services Needing Interfaces**: {needs_interface}")
        report.append(f"- **Coverage**: {(has_interface / total_services) * 100:.1f}%")

        # Priority breakdown
        high_priority = len(categorized["needs_interface_high"])
        medium_priority = len(categorized["needs_interface_medium"])
        low_priority = len(categorized["needs_interface_low"])

        report.append("\n## 🎯 Priority Breakdown")
        report.append(f"- **High Priority**: {high_priority} services")
        report.append(f"- **Medium Priority**: {medium_priority} services")
        report.append(f"- **Low Priority**: {low_priority} services")

        # Services needing interfaces (HIGH PRIORITY)
        report.append(
            f"\n## 🚨 HIGH PRIORITY - Needs Interfaces ({high_priority} services)"
        )
        for service in sorted(
            categorized["needs_interface_high"], key=lambda s: s.category
        ):
            report.append(f"- **{service.name}** ({service.category})")
            report.append(f"  - File: `{service.file_path}`")
            report.append(f"  - Methods: {len(service.methods)} public methods")
            report.append(f"  - Interface File: `{service.interface_file}`")

        # Services needing interfaces (MEDIUM PRIORITY)
        report.append(
            f"\n## ⚠️ MEDIUM PRIORITY - Needs Interfaces ({medium_priority} services)"
        )
        for service in sorted(
            categorized["needs_interface_medium"], key=lambda s: s.category
        ):
            report.append(f"- **{service.name}** ({service.category})")
            report.append(f"  - File: `{service.file_path}`")
            report.append(f"  - Methods: {len(service.methods)} public methods")
            report.append(f"  - Interface File: `{service.interface_file}`")

        # Category breakdown
        report.append("\n## 📂 By Category")
        for category, services in sorted(categorized["by_category"].items()):
            with_interface = sum(1 for s in services if s.has_interface)
            without_interface = len(services) - with_interface

            report.append(f"### {category.title()} ({len(services)} services)")
            report.append(f"- With Interface: {with_interface}")
            report.append(f"- Need Interface: {without_interface}")

            if without_interface > 0:
                report.append("- **Services needing interfaces:**")
                for service in sorted(services, key=lambda s: s.priority):
                    if not service.has_interface:
                        report.append(f"  - {service.name} ({service.priority})")

        # Existing interfaces
        report.append(f"\n## ✅ Existing Interfaces ({len(self.existing_interfaces)})")
        for interface in sorted(self.existing_interfaces):
            report.append(f"- {interface}")

        return "\\n".join(report)


def main():
    """Main function to run the analysis."""
    src_path = os.path.join(os.path.dirname(__file__))

    analyzer = ServiceAnalyzer(src_path)
    report = analyzer.generate_report()

    print(report)

    # Save report to file
    with open("COMPLETE_INTERFACE_COVERAGE_ANALYSIS.md", "w", encoding="utf-8") as f:
        f.write(report)

    print("\\n" + "=" * 50)
    print(
        "📝 Analysis complete! Report saved to COMPLETE_INTERFACE_COVERAGE_ANALYSIS.md"
    )


if __name__ == "__main__":
    main()
