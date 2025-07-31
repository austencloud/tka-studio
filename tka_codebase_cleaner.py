#!/usr/bin/env python3
"""
TKA Codebase Cleanup Analyzer
=============================

Identifies cleanup opportunities in the TKA codebase:
- Unused imports
- Over-engineered systems (like event bus)
- Dead code patterns
- AI-generated bloat
- Incomplete implementations

Usage:
    python tka_codebase_cleaner.py
    python tka_codebase_cleaner.py --focus event-bus
    python tka_codebase_cleaner.py --focus imports
    python tka_codebase_cleaner.py --comprehensive
"""

import argparse
import ast
from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Dict, List, NamedTuple, Set, Tuple


class CleanupOpportunity(NamedTuple):
    """Represents a cleanup opportunity."""

    category: str
    severity: str  # 'high', 'medium', 'low'
    file_path: str
    line_number: int
    description: str
    suggestion: str


class TKACodebaseAnalyzer:
    """Analyzes TKA codebase for cleanup opportunities."""

    def __init__(self, root_directory: str):
        self.root_dir = Path(root_directory)
        self.opportunities: List[CleanupOpportunity] = []
        self.files_analyzed = 0

        # Track various code patterns
        self.imports_by_file: Dict[str, Set[str]] = defaultdict(set)
        self.function_calls_by_file: Dict[str, Set[str]] = defaultdict(set)
        self.class_definitions: Dict[str, List[str]] = defaultdict(list)
        self.event_bus_usage: List[Tuple[str, str]] = []
        self.signal_usage: List[Tuple[str, str]] = []
        self.todo_comments: List[Tuple[str, int, str]] = []
        self.large_functions: List[Tuple[str, str, int]] = []

    def analyze_codebase(self, focus_areas: List[str] = None) -> None:
        """Analyze the entire codebase for cleanup opportunities."""
        print(f"🔍 Analyzing TKA codebase in {self.root_dir}")

        focus_areas = focus_areas or ["all"]

        python_files = list(self.root_dir.rglob("*.py"))
        excluded_patterns = ["__pycache__", ".pytest_cache", "node_modules"]

        for file_path in python_files:
            if any(pattern in str(file_path) for pattern in excluded_patterns):
                continue

            self._analyze_file(file_path, focus_areas)
            self.files_analyzed += 1

        # Run specific analyses
        if "all" in focus_areas or "imports" in focus_areas:
            self._analyze_unused_imports()

        if "all" in focus_areas or "event-bus" in focus_areas:
            self._analyze_event_bus_usage()

        if "all" in focus_areas or "complexity" in focus_areas:
            self._analyze_complexity_issues()

        if "all" in focus_areas or "ai-bloat" in focus_areas:
            self._analyze_ai_generated_bloat()

        print(f"✅ Analyzed {self.files_analyzed} files")

    def _analyze_file(self, file_path: Path, focus_areas: List[str]) -> None:
        """Analyze a single Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            # Extract various patterns
            visitor = CodePatternVisitor(str(file_path))
            visitor.visit(tree)

            # Store results
            self.imports_by_file[str(file_path)] = visitor.imports
            self.function_calls_by_file[str(file_path)] = visitor.function_calls
            self.class_definitions[str(file_path)] = visitor.class_names

            # Look for specific patterns
            if "event-bus" in focus_areas or "all" in focus_areas:
                self._find_event_bus_patterns(file_path, content, visitor)

            if "complexity" in focus_areas or "all" in focus_areas:
                self._find_complexity_issues(file_path, content, visitor)

            # Find TODO/FIXME comments
            self._find_todo_comments(file_path, content)

        except (SyntaxError, UnicodeDecodeError) as e:
            print(f"Warning: Could not parse {file_path}: {e}")

    def _find_event_bus_patterns(self, file_path: Path, content: str, visitor) -> None:
        """Find event bus and signal usage patterns."""
        file_str = str(file_path)

        # Event bus patterns
        event_patterns = [
            r"\.emit\s*\(",
            r"\.subscribe\s*\(",
            r"\.publish\s*\(",
            r"EventBus",
            r"event_bus",
        ]

        for pattern in event_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[: match.start()].count("\n") + 1
                self.event_bus_usage.append(
                    (file_str, f"Line {line_num}: {match.group()}")
                )

        # Qt signal patterns
        signal_patterns = [
            r"\.connect\s*\(",
            r"\.disconnect\s*\(",
            r"Signal\s*\(",
            r"pyqtSignal",
            r"\.emit\s*\(",
        ]

        for pattern in signal_patterns:
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                line_num = content[: match.start()].count("\n") + 1
                self.signal_usage.append(
                    (file_str, f"Line {line_num}: {match.group()}")
                )

    def _find_complexity_issues(self, file_path: Path, content: str, visitor) -> None:
        """Find complexity and code smell issues."""
        lines = content.split("\n")

        # Find large functions
        for func_name, line_count in visitor.function_line_counts.items():
            if line_count > 50:  # Functions longer than 50 lines
                self.large_functions.append((str(file_path), func_name, line_count))

        # Find deeply nested code
        for i, line in enumerate(lines):
            indent_level = len(line) - len(line.lstrip())
            if indent_level > 20:  # Very deep nesting
                self.opportunities.append(
                    CleanupOpportunity(
                        category="complexity",
                        severity="medium",
                        file_path=str(file_path),
                        line_number=i + 1,
                        description=f"Very deep nesting (indent level {indent_level})",
                        suggestion="Consider extracting nested logic into separate functions",
                    )
                )

    def _find_todo_comments(self, file_path: Path, content: str) -> None:
        """Find TODO, FIXME, and similar comments."""
        lines = content.split("\n")
        todo_patterns = [
            r"#.*TODO",
            r"#.*FIXME",
            r"#.*HACK",
            r"#.*XXX",
            r"#.*BUG",
            r"#.*NOTE.*remove",
            r"#.*temporary",
            r"#.*delete.*later",
        ]

        for i, line in enumerate(lines):
            for pattern in todo_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    self.todo_comments.append((str(file_path), i + 1, line.strip()))

    def _analyze_unused_imports(self) -> None:
        """Analyze for unused imports."""
        for file_path, imports in self.imports_by_file.items():
            function_calls = self.function_calls_by_file.get(file_path, set())

            # Read file content to check for string usage
            try:
                with open(file_path, encoding="utf-8") as f:
                    content = f.read()
            except:
                continue

            for import_name in imports:
                # Skip certain imports that might be used dynamically
                if self._is_likely_dynamic_import(import_name):
                    continue

                # Check if import is used
                is_used = (
                    import_name in function_calls
                    or import_name in content
                    or any(import_name in call for call in function_calls)
                )

                if not is_used:
                    self.opportunities.append(
                        CleanupOpportunity(
                            category="unused_imports",
                            severity="low",
                            file_path=file_path,
                            line_number=1,  # Would need more parsing to get exact line
                            description=f"Potentially unused import: {import_name}",
                            suggestion=f"Remove unused import: {import_name}",
                        )
                    )

    def _is_likely_dynamic_import(self, import_name: str) -> bool:
        """Check if an import is likely used dynamically."""
        # Common dynamic usage patterns
        dynamic_patterns = [
            "pytest",
            "unittest",
            "mock",  # Testing frameworks
            "logging",
            "sys",
            "os",
            "Path",  # Common utilities
            "Qt",
            "PyQt",  # Qt might be used in string form
            "typing",  # Type hints
        ]

        return any(pattern in import_name for pattern in dynamic_patterns)

    def _analyze_event_bus_usage(self) -> None:
        """Analyze event bus vs signal usage patterns."""
        event_files = set(file for file, _ in self.event_bus_usage)
        signal_files = set(file for file, _ in self.signal_usage)

        # Find files using both patterns (potential inconsistency)
        both_patterns = event_files.intersection(signal_files)

        for file_path in both_patterns:
            self.opportunities.append(
                CleanupOpportunity(
                    category="event_system",
                    severity="medium",
                    file_path=file_path,
                    line_number=1,
                    description="File uses both event bus and Qt signals",
                    suggestion="Standardize on one event system (prefer Qt signals for UI)",
                )
            )

        # If event bus is barely used, suggest removal
        if len(self.event_bus_usage) < 5 and len(self.signal_usage) > 20:
            self.opportunities.append(
                CleanupOpportunity(
                    category="event_system",
                    severity="high",
                    file_path="(multiple)",
                    line_number=1,
                    description=f"Event bus used in {len(self.event_bus_usage)} places vs Qt signals in {len(self.signal_usage)} places",
                    suggestion="Consider removing event bus system and using Qt signals consistently",
                )
            )

    def _analyze_ai_generated_bloat(self) -> None:
        """Look for patterns that suggest AI-generated code bloat."""

        # Look for comprehensive but unused systems
        for file_path, classes in self.class_definitions.items():
            # Look for manager/service classes that might be over-engineered
            manager_classes = [
                cls for cls in classes if "Manager" in cls or "Service" in cls
            ]

            if len(manager_classes) > 3:  # Many manager classes in one file
                self.opportunities.append(
                    CleanupOpportunity(
                        category="ai_bloat",
                        severity="medium",
                        file_path=file_path,
                        line_number=1,
                        description=f"File has {len(manager_classes)} manager/service classes",
                        suggestion="Consider if all these classes are necessary or if some can be simplified",
                    )
                )

        # Look for TODO comments suggesting incomplete AI implementation
        for file_path, line_num, comment in self.todo_comments:
            ai_indicators = [
                "implement",
                "placeholder",
                "stub",
                "todo",
                "fixme",
                "add logic here",
                "complete this",
                "finish implementation",
            ]

            if any(indicator in comment.lower() for indicator in ai_indicators):
                self.opportunities.append(
                    CleanupOpportunity(
                        category="incomplete_implementation",
                        severity="medium",
                        file_path=file_path,
                        line_number=line_num,
                        description=f"Incomplete implementation: {comment}",
                        suggestion="Complete implementation or remove placeholder code",
                    )
                )

    def _analyze_complexity_issues(self) -> None:
        """Analyze for complexity issues."""
        # Report large functions
        for file_path, func_name, line_count in self.large_functions:
            severity = "high" if line_count > 100 else "medium"
            self.opportunities.append(
                CleanupOpportunity(
                    category="complexity",
                    severity=severity,
                    file_path=file_path,
                    line_number=1,
                    description=f"Large function '{func_name}' has {line_count} lines",
                    suggestion=f"Consider breaking down '{func_name}' into smaller functions",
                )
            )

    def generate_report(self, output_file: str = None) -> str:
        """Generate cleanup report."""
        if not self.opportunities:
            report = "🎉 No major cleanup opportunities found!"
            print(report)
            return report

        # Group opportunities by category
        by_category = defaultdict(list)
        for opp in self.opportunities:
            by_category[opp.category].append(opp)

        report_lines = [
            "🧹 TKA Codebase Cleanup Analysis",
            "=" * 50,
            f"📊 Found {len(self.opportunities)} cleanup opportunities",
            f"📁 Across {len(set(opp.file_path for opp in self.opportunities))} files",
            "",
        ]

        # Summary by category and severity
        severity_counts = Counter(opp.severity for opp in self.opportunities)
        category_counts = Counter(opp.category for opp in self.opportunities)

        report_lines.extend(
            [
                "🎯 Priority Summary:",
                f"  🔴 High priority: {severity_counts['high']} issues",
                f"  🟡 Medium priority: {severity_counts['medium']} issues",
                f"  🟢 Low priority: {severity_counts['low']} issues",
                "",
                "📋 Category Breakdown:",
            ]
        )

        for category, count in category_counts.most_common():
            report_lines.append(
                f"  📁 {category.replace('_', ' ').title()}: {count} issues"
            )

        report_lines.extend(["", "🔍 Detailed Issues:", ""])

        # Sort by severity then category
        severity_order = {"high": 0, "medium": 1, "low": 2}
        sorted_opportunities = sorted(
            self.opportunities,
            key=lambda x: (severity_order[x.severity], x.category, x.file_path),
        )

        current_category = None
        for opp in sorted_opportunities:
            if opp.category != current_category:
                current_category = opp.category
                report_lines.append(
                    f"\n📂 {current_category.replace('_', ' ').title()}"
                )
                report_lines.append("-" * 30)

            severity_icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}[opp.severity]
            file_short = (
                Path(opp.file_path).name
                if opp.file_path != "(multiple)"
                else opp.file_path
            )

            report_lines.append(f"{severity_icon} {file_short}:{opp.line_number}")
            report_lines.append(f"   Issue: {opp.description}")
            report_lines.append(f"   Fix: {opp.suggestion}")
            report_lines.append("")

        # Special sections for major findings
        if self.event_bus_usage or self.signal_usage:
            report_lines.extend(
                [
                    "\n🔌 Event System Analysis:",
                    f"  Event Bus Usage: {len(self.event_bus_usage)} occurrences",
                    f"  Qt Signal Usage: {len(self.signal_usage)} occurrences",
                ]
            )

            if len(self.event_bus_usage) < len(self.signal_usage) / 4:
                report_lines.append(
                    "  💡 Recommendation: Consider removing event bus and standardizing on Qt signals"
                )

        if self.large_functions:
            report_lines.extend(
                [
                    f"\n📏 Large Functions Found: {len(self.large_functions)}",
                    "  Top 5 largest functions:",
                ]
            )

            sorted_funcs = sorted(
                self.large_functions, key=lambda x: x[2], reverse=True
            )[:5]
            for file_path, func_name, line_count in sorted_funcs:
                file_short = Path(file_path).name
                report_lines.append(
                    f"    📄 {file_short}: {func_name}() - {line_count} lines"
                )

        if self.todo_comments:
            report_lines.extend(
                [
                    f"\n📝 TODO Comments Found: {len(self.todo_comments)}",
                    "  Categories of incomplete work:",
                ]
            )

            # Categorize TODOs
            todo_categories = defaultdict(int)
            for _, _, comment in self.todo_comments:
                if "implement" in comment.lower():
                    todo_categories["Implementation needed"] += 1
                elif "remove" in comment.lower() or "delete" in comment.lower():
                    todo_categories["Scheduled for removal"] += 1
                elif "fix" in comment.lower():
                    todo_categories["Bug fixes needed"] += 1
                else:
                    todo_categories["Other TODOs"] += 1

            for category, count in todo_categories.items():
                report_lines.append(f"    📌 {category}: {count}")

        report_lines.extend(
            [
                "\n💡 Quick Wins (Start Here):",
                "1. 🗑️  Remove unused imports (low risk, immediate benefit)",
                "2. 🔧 Complete or remove TODO items (prevents technical debt)",
                "3. 📱 Standardize event system (Qt signals vs event bus)",
                "4. ✂️  Break down large functions (improves maintainability)",
                "5. 🧹 Remove AI-generated code that wasn't needed",
            ]
        )

        report = "\n".join(report_lines)

        if output_file:
            with open(output_file, "w") as f:
                f.write(report)
            print(f"📝 Report saved to {output_file}")

        return report


class CodePatternVisitor(ast.NodeVisitor):
    """AST visitor to extract code patterns."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.imports: Set[str] = set()
        self.function_calls: Set[str] = set()
        self.class_names: List[str] = []
        self.function_line_counts: Dict[str, int] = {}
        self.current_function_start = None

    def visit_Import(self, node):
        """Visit import statement."""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        """Visit from import statement."""
        for alias in node.names:
            self.imports.add(alias.name)
        self.generic_visit(node)

    def visit_ClassDef(self, node):
        """Visit class definition."""
        self.class_names.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        """Visit function definition."""
        # Calculate function length
        if hasattr(node, "end_lineno") and node.end_lineno:
            line_count = node.end_lineno - node.lineno
            self.function_line_counts[node.name] = line_count

        self.generic_visit(node)

    def visit_Call(self, node):
        """Visit function call."""
        if isinstance(node.func, ast.Name):
            self.function_calls.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            self.function_calls.add(node.func.attr)

        self.generic_visit(node)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Analyze TKA codebase for cleanup opportunities"
    )
    parser.add_argument(
        "--directory",
        "-d",
        default="src",
        help="Root directory to analyze (default: src)",
    )
    parser.add_argument(
        "--focus",
        choices=["imports", "event-bus", "complexity", "ai-bloat", "all"],
        nargs="+",
        default=["all"],
        help="Focus areas for analysis",
    )
    parser.add_argument("--output", "-o", help="Output file for report")
    parser.add_argument(
        "--comprehensive",
        action="store_true",
        help="Run comprehensive analysis (slower but more thorough)",
    )

    args = parser.parse_args()

    # Initialize analyzer
    analyzer = TKACodebaseAnalyzer(args.directory)

    # Run analysis
    analyzer.analyze_codebase(args.focus)

    # Generate report
    report = analyzer.generate_report(args.output)

    if not args.output:
        print("\n" + report)

    # Provide actionable summary
    total_issues = len(analyzer.opportunities)
    if total_issues > 0:
        high_priority = sum(
            1 for opp in analyzer.opportunities if opp.severity == "high"
        )
        print(
            f"\n🎯 Action Items: {high_priority} high priority issues to address first"
        )
        print("💡 Run with --output report.txt to save detailed analysis")


if __name__ == "__main__":
    main()
