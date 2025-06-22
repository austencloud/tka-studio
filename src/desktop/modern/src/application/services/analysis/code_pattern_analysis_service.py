"""
Code Pattern Analysis Service

Pure service for analyzing code patterns and violations.
Extracted from ImportStandardizer to follow single responsibility principle.

This service handles:
- TKA import pattern validation
- External library detection
- Violation categorization
- Pattern matching and classification

No file system dependencies, completely testable in isolation.
"""

import re
import logging
from typing import Dict, List

from desktop.modern.src.core.interfaces.organization_services import (
    ICodePatternAnalysisService,
)

logger = logging.getLogger(__name__)


class CodePatternAnalysisService(ICodePatternAnalysisService):
    """
    Pure service for analyzing code patterns and violations.

    Implements pattern recognition and classification algorithms
    without any external dependencies. Focuses solely on pattern analysis.
    """

    def __init__(self):
        """Initialize the code pattern analysis service."""

        # TKA Desktop standard import patterns
        self.standard_patterns = {
            "domain_models": r"^from domain\.models\.",
            "application_services": r"^from application\.services\.",
            "presentation_components": r"^from presentation\.components\.",
            "core_modules": r"^from core\.",
            "infrastructure": r"^from infrastructure\.",
        }

        # Patterns to avoid (violations)
        self.violation_patterns = {
            "src_prefix": r"^from src\.",
            "absolute_with_modern": r"^from modern\.",
            "deep_relative": r"^from \.\.\.\.+",  # More than 3 levels
        }

        # Internal relative imports (allowed)
        self.allowed_relative_patterns = {
            "single_level": r"^from \.",
            "parent_level": r"^from \.\.",
            "grandparent_level": r"^from \.\.\.",
        }

        # External library prefixes for recognition
        self.external_library_prefixes = [
            "typing",
            "pathlib",
            "os",
            "sys",
            "json",
            "logging",
            "dataclasses",
            "enum",
            "abc",
            "collections",
            "itertools",
            "functools",
            "operator",
            "time",
            "datetime",
            "threading",
            "asyncio",
            "concurrent",
            "multiprocessing",
            "PyQt6",
            "PySide6",
            "pytest",
            "hypothesis",
            "numpy",
            "pandas",
            "requests",
            "fastapi",
            "uvicorn",
            "pydantic",
            "sqlalchemy",
            "alembic",
        ]

    def is_standard_tka_import(self, module_name: str) -> bool:
        """
        Check if import follows standard TKA patterns.

        Args:
            module_name: Module name to check

        Returns:
            True if import follows TKA standards
        """
        # Check against standard TKA patterns
        for pattern in self.standard_patterns.values():
            if re.match(pattern, f"from {module_name}"):
                return True

        # Check if it's a relative import (also allowed)
        for pattern in self.allowed_relative_patterns.values():
            if re.match(pattern, f"from {module_name}"):
                return True

        return False

    def is_external_library(self, module_name: str) -> bool:
        """
        Check if import is from external library.

        Args:
            module_name: Module name to check

        Returns:
            True if import is from external library
        """
        return any(
            module_name.startswith(prefix) for prefix in self.external_library_prefixes
        )

    def categorize_violation(self, violation: str) -> str:
        """
        Categorize violation type for reporting.

        Args:
            violation: Violation description

        Returns:
            Violation category
        """
        if "src. prefix" in violation:
            return "src_prefix_violations"
        elif "relative import depth" in violation:
            return "excessive_relative_depth"
        elif "Non-standard TKA import" in violation:
            return "non_standard_patterns"
        elif "absolute_with_modern" in violation:
            return "modern_prefix_violations"
        else:
            return "other_violations"

    def detect_import_violations(self, import_statement: str) -> List[str]:
        """
        Detect violations in a single import statement.

        Args:
            import_statement: Import statement to analyze

        Returns:
            List of violation descriptions
        """
        violations = []

        # Check for src. prefix violations
        if re.match(self.violation_patterns["src_prefix"], import_statement):
            violations.append(f"src. prefix violation: {import_statement}")

        # Check for modern. prefix violations
        if re.match(self.violation_patterns["absolute_with_modern"], import_statement):
            violations.append(f"modern. prefix violation: {import_statement}")

        # Check for excessive relative import depth
        if re.match(self.violation_patterns["deep_relative"], import_statement):
            violations.append(f"Excessive relative import depth: {import_statement}")

        return violations

    def generate_import_recommendations(
        self, module_name: str, violation_type: str
    ) -> List[str]:
        """
        Generate specific recommendations for import violations.

        Args:
            module_name: Module name with violation
            violation_type: Type of violation detected

        Returns:
            List of specific recommendations
        """
        recommendations = []

        if violation_type == "src_prefix_violations":
            # Remove src. prefix
            fixed_import = module_name.replace("src.", "", 1)
            recommendations.append(
                f"Remove 'src.' prefix: {module_name} -> {fixed_import}"
            )

        elif violation_type == "modern_prefix_violations":
            # Remove modern. prefix
            fixed_import = module_name.replace("modern.", "", 1)
            recommendations.append(
                f"Remove 'modern.' prefix: {module_name} -> {fixed_import}"
            )

        elif violation_type == "non_standard_patterns":
            # Suggest standard TKA patterns
            if "models" in module_name:
                recommendations.append(
                    f"Use standard pattern: from domain.models.{module_name.split('.')[-1]} import ..."
                )
            elif "services" in module_name:
                recommendations.append(
                    f"Use standard pattern: from application.services.{module_name.split('.')[-1]} import ..."
                )
            elif "components" in module_name:
                recommendations.append(
                    f"Use standard pattern: from presentation.components.{module_name.split('.')[-1]} import ..."
                )
            else:
                recommendations.append(f"Use standard TKA pattern for: {module_name}")

        elif violation_type == "excessive_relative_depth":
            recommendations.append("Reduce relative import depth to maximum 3 levels")
            recommendations.append(
                "Consider using absolute imports for deep hierarchies"
            )

        return recommendations

    def calculate_pattern_compliance_score(
        self, total_imports: int, violations: int, inconsistencies: int
    ) -> float:
        """
        Calculate compliance score for import patterns.

        Args:
            total_imports: Total number of imports analyzed
            violations: Number of violations found
            inconsistencies: Number of inconsistencies found

        Returns:
            Compliance score (0-100)
        """
        if total_imports == 0:
            return 100.0

        # Deduct points for violations
        violation_penalty = (
            violations / total_imports
        ) * 50  # Up to 50% penalty for src. prefix
        inconsistency_penalty = (
            inconsistencies / total_imports
        ) * 30  # Up to 30% penalty for other issues

        score = 100.0 - violation_penalty - inconsistency_penalty
        return max(0.0, score)

    def get_standard_import_patterns(self) -> Dict[str, str]:
        """
        Get dictionary of standard TKA import patterns.

        Returns:
            Dictionary mapping pattern names to regex patterns
        """
        return self.standard_patterns.copy()

    def get_violation_patterns(self) -> Dict[str, str]:
        """
        Get dictionary of violation patterns to detect.

        Returns:
            Dictionary mapping violation names to regex patterns
        """
        return self.violation_patterns.copy()

    def validate_import_pattern(self, import_statement: str) -> dict:
        """
        Validate a single import statement against TKA patterns.

        Args:
            import_statement: Import statement to validate

        Returns:
            Dictionary with validation results
        """
        # Extract module name from import statement
        module_match = re.match(r"from\s+([^\s]+)", import_statement)
        if not module_match:
            return {
                "valid": False,
                "reason": "Could not parse import statement",
                "recommendations": ["Check import syntax"],
            }

        module_name = module_match.group(1)

        # Check if it's a standard TKA import
        if self.is_standard_tka_import(module_name):
            return {
                "valid": True,
                "pattern_type": "standard_tka",
                "recommendations": [],
            }

        # Check if it's an external library
        if self.is_external_library(module_name):
            return {
                "valid": True,
                "pattern_type": "external_library",
                "recommendations": [],
            }

        # Detect violations
        violations = self.detect_import_violations(import_statement)
        if violations:
            violation_type = self.categorize_violation(violations[0])
            recommendations = self.generate_import_recommendations(
                module_name, violation_type
            )

            return {
                "valid": False,
                "violations": violations,
                "violation_type": violation_type,
                "recommendations": recommendations,
            }

        # Unknown pattern
        return {
            "valid": False,
            "reason": "Unknown import pattern",
            "recommendations": ["Consider using standard TKA import patterns"],
        }
