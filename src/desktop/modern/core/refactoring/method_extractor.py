"""
Method Extraction Utility for TKA Code Refactoring

Helps break down long methods into smaller, focused methods following
single responsibility principle.

PROVIDES:
- Method extraction guidelines
- Common patterns for method breakdown
- Validation helpers for method length
"""

from dataclasses import dataclass
import inspect
from typing import Callable, Dict, List


@dataclass
class MethodAnalysis:
    """Analysis results for a method."""

    name: str
    line_count: int
    complexity_score: int
    responsibilities: List[str]
    suggested_extractions: List[str]
    is_too_long: bool


class MethodExtractor:
    """
    Utility for analyzing and suggesting method extractions.

    Helps identify long methods and suggests how to break them down.
    """

    # Constants for method analysis
    MAX_METHOD_LENGTH = 25  # Lines
    MAX_COMPLEXITY_SCORE = 10

    @staticmethod
    def analyze_method(method_func: Callable) -> MethodAnalysis:
        """
        Analyze a method and suggest extractions if needed.

        Args:
            method_func: The method to analyze

        Returns:
            MethodAnalysis with suggestions for improvement
        """
        try:
            source_lines = inspect.getsourcelines(method_func)[0]
            line_count = len(source_lines)

            # Calculate basic complexity score
            complexity_score = MethodExtractor._calculate_complexity(source_lines)

            # Identify responsibilities
            responsibilities = MethodExtractor._identify_responsibilities(source_lines)

            # Suggest extractions if method is too long
            suggested_extractions = []
            is_too_long = line_count > MethodExtractor.MAX_METHOD_LENGTH

            if is_too_long:
                suggested_extractions = MethodExtractor._suggest_extractions(
                    source_lines, responsibilities
                )

            return MethodAnalysis(
                name=method_func.__name__,
                line_count=line_count,
                complexity_score=complexity_score,
                responsibilities=responsibilities,
                suggested_extractions=suggested_extractions,
                is_too_long=is_too_long,
            )

        except Exception:
            # Return basic analysis if source inspection fails
            return MethodAnalysis(
                name=getattr(method_func, "__name__", "unknown"),
                line_count=0,
                complexity_score=0,
                responsibilities=[],
                suggested_extractions=[],
                is_too_long=False,
            )

    @staticmethod
    def _calculate_complexity(source_lines: List[str]) -> int:
        """Calculate basic complexity score based on control structures."""
        complexity = 1  # Base complexity

        for line in source_lines:
            line = line.strip().lower()

            # Add complexity for control structures
            if any(
                keyword in line
                for keyword in [
                    "if ",
                    "elif ",
                    "else:",
                    "for ",
                    "while ",
                    "try:",
                    "except",
                ]
            ):
                complexity += 1

            # Add complexity for nested structures
            if line.startswith("    "):  # Nested (4+ spaces)
                complexity += 0.5

        return int(complexity)

    @staticmethod
    def _identify_responsibilities(source_lines: List[str]) -> List[str]:
        """Identify different responsibilities in the method."""
        responsibilities = []

        # Look for common patterns that indicate different responsibilities
        patterns = {
            "validation": ["validate", "check", "verify", "assert"],
            "initialization": ["init", "setup", "create", "configure"],
            "data_processing": ["process", "transform", "convert", "parse"],
            "error_handling": ["try:", "except", "error", "handle"],
            "ui_creation": ["widget", "layout", "button", "label"],
            "service_registration": ["register", "resolve", "container"],
            "file_operations": ["read", "write", "file", "path"],
            "cleanup": ["cleanup", "dispose", "close", "reset"],
        }

        for line in source_lines:
            line_lower = line.lower()
            for responsibility, keywords in patterns.items():
                if any(keyword in line_lower for keyword in keywords):
                    if responsibility not in responsibilities:
                        responsibilities.append(responsibility)

        return responsibilities

    @staticmethod
    def _suggest_extractions(
        source_lines: List[str], responsibilities: List[str]
    ) -> List[str]:
        """Suggest method extractions based on identified responsibilities."""
        suggestions = []

        # Suggest extractions based on responsibilities
        if "validation" in responsibilities:
            suggestions.append(
                "Extract validation logic into _validate_inputs() method"
            )

        if "initialization" in responsibilities:
            suggestions.append(
                "Extract initialization logic into _initialize_components() method"
            )

        if "error_handling" in responsibilities:
            suggestions.append("Extract error handling into _handle_errors() method")

        if "ui_creation" in responsibilities:
            suggestions.append(
                "Extract UI creation into _create_ui_components() method"
            )

        if "service_registration" in responsibilities:
            suggestions.append(
                "Extract service registration into _register_services() method"
            )

        if len(responsibilities) > 3:
            suggestions.append(
                f"Method has {len(responsibilities)} responsibilities - consider splitting into {len(responsibilities)} smaller methods"
            )

        # Look for comment-based sections
        comment_sections = []
        for i, line in enumerate(source_lines):
            if line.strip().startswith("#") and "step" in line.lower():
                comment_sections.append(f"Line {i + 1}: {line.strip()}")

        if comment_sections:
            suggestions.append(
                "Consider extracting each commented step into its own method"
            )

        return suggestions


class RefactoredMethodPatterns:
    """
    Common patterns for refactored methods that follow best practices.

    Provides templates and examples for properly structured methods.
    """

    @staticmethod
    def initialization_pattern(self, *args, **kwargs):
        """
        Template for initialization methods.

        Pattern: Validate -> Configure -> Initialize -> Verify
        """
        # Step 1: Validate inputs
        self._validate_initialization_inputs(*args, **kwargs)

        # Step 2: Configure components
        self._configure_components(**kwargs)

        # Step 3: Initialize services
        self._initialize_services()

        # Step 4: Verify initialization
        self._verify_initialization_success()

    @staticmethod
    def ui_setup_pattern(self, parent_widget, container, progress_callback=None):
        """
        Template for UI setup methods.

        Pattern: Create Structure -> Load Components -> Connect Signals -> Finalize
        """
        try:
            # Step 1: Create basic structure
            main_widget = self._create_main_structure(parent_widget)

            # Step 2: Load components
            components = self._load_ui_components(container, progress_callback)

            # Step 3: Connect signals
            self._connect_component_signals(components)

            # Step 4: Finalize setup
            self._finalize_ui_setup(main_widget, progress_callback)

            return main_widget

        except Exception as e:
            return self._handle_ui_setup_failure(e, parent_widget)

    @staticmethod
    def service_registration_pattern(self, container):
        """
        Template for service registration methods.

        Pattern: Register Core -> Register Optional -> Verify -> Handle Failures
        """
        registration_results = {}

        # Step 1: Register core services (required)
        registration_results["core"] = self._register_core_services(container)

        # Step 2: Register optional services (graceful failure)
        registration_results["optional"] = self._register_optional_services(container)

        # Step 3: Verify critical registrations
        self._verify_critical_services(container, registration_results["core"])

        # Step 4: Report registration status
        self._report_registration_status(registration_results)

        return registration_results

    @staticmethod
    def error_recovery_pattern(
        self, operation_name, primary_action, fallback_action=None
    ):
        """
        Template for error recovery methods.

        Pattern: Attempt Primary -> Log Error -> Execute Fallback -> Verify Result
        """
        try:
            # Step 1: Attempt primary operation
            result = primary_action()

            # Step 2: Verify success
            if result is not None:
                return result

        except Exception as e:
            # Step 3: Log error with context
            self._log_operation_failure(operation_name, e)

        # Step 4: Execute fallback if available
        if fallback_action:
            try:
                fallback_result = fallback_action()
                self._log_fallback_success(operation_name)
                return fallback_result
            except Exception as fallback_error:
                self._log_fallback_failure(operation_name, fallback_error)

        # Step 5: Return safe default or raise
        return self._get_safe_default_for_operation(operation_name)


def extract_method_suggestions(class_obj) -> Dict[str, MethodAnalysis]:
    """
    Analyze all methods in a class and provide extraction suggestions.

    Args:
        class_obj: The class to analyze

    Returns:
        Dictionary mapping method names to their analysis
    """
    results = {}

    for method_name in dir(class_obj):
        if not method_name.startswith("_") or method_name.startswith("__"):
            continue

        method = getattr(class_obj, method_name)
        if callable(method) and hasattr(method, "__code__"):
            analysis = MethodExtractor.analyze_method(method)
            if analysis.is_too_long:
                results[method_name] = analysis

    return results


def generate_refactoring_report(class_obj, class_name: str) -> str:
    """
    Generate a comprehensive refactoring report for a class.

    Args:
        class_obj: The class to analyze
        class_name: Name of the class for the report

    Returns:
        Formatted report with refactoring suggestions
    """
    analyses = extract_method_suggestions(class_obj)

    if not analyses:
        return f"✅ {class_name}: All methods are appropriately sized (≤{MethodExtractor.MAX_METHOD_LENGTH} lines)"

    report = [f"📊 Refactoring Report for {class_name}"]
    report.append("=" * 50)

    for method_name, analysis in analyses.items():
        report.append(f"\n🔍 Method: {method_name}")
        report.append(
            f"   Lines: {analysis.line_count} (max: {MethodExtractor.MAX_METHOD_LENGTH})"
        )
        report.append(f"   Complexity: {analysis.complexity_score}/10")
        report.append(f"   Responsibilities: {', '.join(analysis.responsibilities)}")

        if analysis.suggested_extractions:
            report.append("   💡 Suggestions:")
            for suggestion in analysis.suggested_extractions:
                report.append(f"      • {suggestion}")

    return "\n".join(report)
