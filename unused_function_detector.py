#!/usr/bin/env python3
"""
TKA Unused Function Detector
============================

Analyzes the TKA codebase to identify functions that are defined but never called.
Perfect for cleaning up AI-generated code that includes unnecessary functions.

Usage:
    python unused_function_detector.py
    python unused_function_detector.py --directory src/desktop/modern/src
    python unused_function_detector.py --exclude-tests --exclude-patterns "__*,*_test.py"
"""

import argparse
import ast
from collections import defaultdict
import json
from pathlib import Path
from typing import Dict, List, NamedTuple, Set


class FunctionInfo(NamedTuple):
    """Information about a function definition."""

    name: str
    file_path: str
    line_number: int
    class_name: str = None
    is_method: bool = False
    is_private: bool = False
    is_dunder: bool = False


class UnusedFunctionDetector:
    """Detects functions that are defined but never called."""

    def __init__(
        self,
        root_directory: str,
        exclude_patterns: List[str] = None,
        exclude_tests: bool = True,
        exclude_migrations: bool = True,
    ):
        self.root_dir = Path(root_directory)
        self.exclude_patterns = exclude_patterns or []
        self.exclude_tests = exclude_tests
        self.exclude_migrations = exclude_migrations

        # Storage for analysis results
        self.function_definitions: Dict[str, List[FunctionInfo]] = defaultdict(list)
        self.function_calls: Set[str] = set()
        self.method_calls: Set[str] = set()
        self.files_analyzed = 0
        self.files_skipped = 0

        # Common patterns to exclude
        self.default_exclude_patterns = [
            "__pycache__",
            ".git",
            ".pytest_cache",
            "node_modules",
            ".vscode",
            "*.pyc",
            "migrations/",
        ]

        if exclude_tests:
            self.default_exclude_patterns.extend(
                ["test_*.py", "*_test.py", "tests/", "conftest.py"]
            )

        if exclude_migrations:
            self.default_exclude_patterns.extend(["*migration*", "MIGRATION_GUIDE*"])

    def should_exclude_file(self, file_path: Path) -> bool:
        """Check if a file should be excluded from analysis."""
        file_str = str(file_path)

        # Check all exclude patterns
        all_patterns = self.default_exclude_patterns + self.exclude_patterns

        for pattern in all_patterns:
            if pattern.endswith("/"):
                # Directory pattern
                if f"/{pattern}" in file_str or file_str.endswith(pattern[:-1]):
                    return True
            elif "*" in pattern:
                # Glob pattern
                import fnmatch

                if fnmatch.fnmatch(file_path.name, pattern):
                    return True
            else:
                # Simple substring match
                if pattern in file_str:
                    return True

        return False

    def extract_functions_from_file(self, file_path: Path) -> None:
        """Extract function definitions and calls from a Python file."""
        try:
            with open(file_path, encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=str(file_path))

            # Extract function definitions and calls
            visitor = FunctionVisitor(file_path)
            visitor.visit(tree)

            # Store results
            for func_info in visitor.function_definitions:
                self.function_definitions[func_info.name].append(func_info)

            self.function_calls.update(visitor.function_calls)
            self.method_calls.update(visitor.method_calls)

            self.files_analyzed += 1

        except (SyntaxError, UnicodeDecodeError, Exception) as e:
            print(f"Warning: Could not parse {file_path}: {e}")
            self.files_skipped += 1

    def analyze_directory(self) -> None:
        """Analyze all Python files in the directory tree."""
        print(f"🔍 Analyzing Python files in {self.root_dir}")
        print(
            f"📁 Excluding: {', '.join(self.default_exclude_patterns + self.exclude_patterns)}"
        )

        python_files = list(self.root_dir.rglob("*.py"))

        for file_path in python_files:
            if self.should_exclude_file(file_path):
                continue

            self.extract_functions_from_file(file_path)

        print(f"✅ Analyzed {self.files_analyzed} files, skipped {self.files_skipped}")

    def find_unused_functions(self) -> List[FunctionInfo]:
        """Find functions that are defined but never called."""
        unused_functions = []

        for func_name, definitions in self.function_definitions.items():
            for func_info in definitions:
                # Skip special methods and private functions unless explicitly requested
                if self._should_skip_function(func_info):
                    continue

                # Check if function is called anywhere
                is_called = (
                    func_name in self.function_calls
                    or func_name in self.method_calls
                    or self._check_dynamic_usage(func_name)
                )

                if not is_called:
                    unused_functions.append(func_info)

        return sorted(unused_functions, key=lambda x: (x.file_path, x.line_number))

    def _should_skip_function(self, func_info: FunctionInfo) -> bool:
        """Determine if a function should be skipped from unused analysis."""
        # Skip dunder methods (they're called by Python runtime)
        if func_info.is_dunder:
            return True

        # Skip common lifecycle methods that might be called by frameworks
        lifecycle_methods = {
            "setup_method",
            "teardown_method",
            "setup_class",
            "teardown_class",
            "setUp",
            "tearDown",
            "setUpClass",
            "tearDownClass",
            "run",
            "main",
            "execute",
            "process",
            "handle",
            "get",
            "post",
            "put",
            "delete",  # HTTP methods
            "mousePressEvent",
            "mouseReleaseEvent",
            "paintEvent",  # Qt events
            "closeEvent",
            "showEvent",
            "hideEvent",
            "resizeEvent",
        }

        if func_info.name in lifecycle_methods:
            return True

        # Skip property getters/setters
        if func_info.name.startswith(("get_", "set_", "is_", "has_")):
            # These might be used dynamically or by property decorators
            return False  # Actually, let's check these - they might be unused

        return False

    def _check_dynamic_usage(self, func_name: str) -> bool:
        """Check for dynamic usage patterns that AST parsing might miss."""
        # These patterns suggest the function might be used dynamically
        dynamic_patterns = [
            "getattr",
            "setattr",
            "hasattr",
            f'"{func_name}"',
            f"'{func_name}'",
        ]

        # This is a simplified check - in practice you'd search file contents
        # For now, assume functions with common dynamic usage patterns are used
        common_dynamic_names = {
            "serialize",
            "deserialize",
            "to_dict",
            "from_dict",
            "validate",
            "clean",
            "save",
            "delete",
            "create",
            "encode",
            "decode",
            "parse",
            "format",
        }

        return func_name in common_dynamic_names

    def generate_report(
        self, unused_functions: List[FunctionInfo], output_file: str = None
    ) -> str:
        """Generate a detailed report of unused functions."""
        if not unused_functions:
            report = "🎉 No unused functions found!"
            print(report)
            return report

        # Group by file for better readability
        by_file = defaultdict(list)
        for func in unused_functions:
            by_file[func.file_path].append(func)

        report_lines = [
            "🧹 TKA Unused Function Analysis Report",
            "=" * 50,
            f"📊 Found {len(unused_functions)} potentially unused functions",
            f"📁 Across {len(by_file)} files",
            "",
        ]

        # Summary by category
        categories = {
            "Public Functions": [
                f for f in unused_functions if not f.is_private and not f.is_method
            ],
            "Private Functions": [
                f for f in unused_functions if f.is_private and not f.is_method
            ],
            "Methods": [f for f in unused_functions if f.is_method],
        }

        for category, funcs in categories.items():
            if funcs:
                report_lines.append(f"🏷️  {category}: {len(funcs)} functions")

        report_lines.extend(["", "📋 Detailed Breakdown:", ""])

        for file_path in sorted(by_file.keys()):
            funcs = by_file[file_path]
            report_lines.append(f"📄 {file_path}")

            for func in sorted(funcs, key=lambda x: x.line_number):
                prefix = "  🔸"
                if func.is_method:
                    prefix = "  🔹 (method)"
                elif func.is_private:
                    prefix = "  🔸 (private)"

                class_info = f" in {func.class_name}" if func.class_name else ""
                report_lines.append(
                    f"{prefix} {func.name}(){class_info} (line {func.line_number})"
                )

            report_lines.append("")

        # Action recommendations
        report_lines.extend(
            [
                "💡 Recommendations:",
                "",
                "1. 🗑️  Safe to delete:",
                "   - Private functions that aren't called",
                "   - Helper functions with no usage",
                "   - AI-generated functions that weren't needed",
                "",
                "2. ⚠️  Check carefully:",
                "   - Public functions (might be part of API)",
                "   - Methods (might be called by framework/inheritance)",
                "   - Functions with generic names (might be used dynamically)",
                "",
                "3. 🔍 Search for dynamic usage:",
                "   - String-based function calls (getattr, etc.)",
                "   - Import patterns (from module import function)",
                "   - Configuration-based calling",
                "",
            ]
        )

        report = "\n".join(report_lines)

        # Save to file if requested
        if output_file:
            with open(output_file, "w") as f:
                f.write(report)
            print(f"📝 Report saved to {output_file}")

        return report

    def export_json(
        self, unused_functions: List[FunctionInfo], output_file: str
    ) -> None:
        """Export results as JSON for programmatic processing."""
        data = {
            "analysis_summary": {
                "total_unused_functions": len(unused_functions),
                "files_analyzed": self.files_analyzed,
                "files_skipped": self.files_skipped,
                "root_directory": str(self.root_dir),
            },
            "unused_functions": [
                {
                    "name": func.name,
                    "file_path": func.file_path,
                    "line_number": func.line_number,
                    "class_name": func.class_name,
                    "is_method": func.is_method,
                    "is_private": func.is_private,
                    "is_dunder": func.is_dunder,
                }
                for func in unused_functions
            ],
        }

        with open(output_file, "w") as f:
            json.dump(data, f, indent=2)

        print(f"💾 JSON export saved to {output_file}")


class FunctionVisitor(ast.NodeVisitor):
    """AST visitor to extract function definitions and calls."""

    def __init__(self, file_path: Path):
        self.file_path = str(file_path)
        self.function_definitions: List[FunctionInfo] = []
        self.function_calls: Set[str] = set()
        self.method_calls: Set[str] = set()
        self.current_class = None

    def visit_ClassDef(self, node):
        """Visit class definition."""
        old_class = self.current_class
        self.current_class = node.name
        self.generic_visit(node)
        self.current_class = old_class

    def visit_FunctionDef(self, node):
        """Visit function definition."""
        func_info = FunctionInfo(
            name=node.name,
            file_path=self.file_path,
            line_number=node.lineno,
            class_name=self.current_class,
            is_method=self.current_class is not None,
            is_private=node.name.startswith("_") and not node.name.startswith("__"),
            is_dunder=node.name.startswith("__") and node.name.endswith("__"),
        )

        self.function_definitions.append(func_info)
        self.generic_visit(node)

    def visit_Call(self, node):
        """Visit function call."""
        # Direct function calls
        if isinstance(node.func, ast.Name):
            self.function_calls.add(node.func.id)

        # Method calls (obj.method)
        elif isinstance(node.func, ast.Attribute):
            self.method_calls.add(node.func.attr)

        # Chained calls (obj.method().other_method)
        elif isinstance(node.func, ast.Call) and isinstance(
            node.func.func, ast.Attribute
        ):
            self.method_calls.add(node.func.func.attr)

        self.generic_visit(node)

    def visit_Attribute(self, node):
        """Visit attribute access (might be function reference)."""
        # This catches cases like: callback = obj.method_name
        if isinstance(node.ctx, ast.Load):
            self.method_calls.add(node.attr)

        self.generic_visit(node)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Detect unused functions in TKA codebase"
    )
    parser.add_argument(
        "--directory",
        "-d",
        default="src",
        help="Root directory to analyze (default: src)",
    )
    parser.add_argument(
        "--exclude-patterns",
        nargs="+",
        default=[],
        help="Additional patterns to exclude",
    )
    parser.add_argument(
        "--include-tests", action="store_true", help="Include test files in analysis"
    )
    parser.add_argument(
        "--include-private",
        action="store_true",
        help="Include private functions in report",
    )
    parser.add_argument("--output", "-o", help="Output file for report")
    parser.add_argument("--json", help="Export results as JSON")
    parser.add_argument(
        "--quick", action="store_true", help="Quick analysis (excludes more patterns)"
    )

    args = parser.parse_args()

    # Adjust exclude patterns for quick mode
    if args.quick:
        args.exclude_patterns.extend(
            ["legacy/", "debug*", "temp*", "*_backup*", "examples/"]
        )

    # Initialize detector
    detector = UnusedFunctionDetector(
        root_directory=args.directory,
        exclude_patterns=args.exclude_patterns,
        exclude_tests=not args.include_tests,
    )

    # Run analysis
    detector.analyze_directory()
    unused_functions = detector.find_unused_functions()

    # Filter out private functions if not requested
    if not args.include_private:
        unused_functions = [f for f in unused_functions if not f.is_private]

    # Generate report
    report = detector.generate_report(unused_functions, args.output)

    # Export JSON if requested
    if args.json:
        detector.export_json(unused_functions, args.json)

    # Print summary
    print(f"\n📊 Analysis complete: {len(unused_functions)} unused functions found")

    if not args.output:
        print("\n" + report)


if __name__ == "__main__":
    main()
