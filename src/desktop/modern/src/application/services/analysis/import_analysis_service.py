"""
Import Analysis Service

Pure service for analyzing import patterns in Python files.
Extracted from ImportStandardizer to follow single responsibility principle.

This service handles:
- AST parsing and import extraction
- Import pattern analysis
- Compliance score calculation
- Codebase-wide analysis coordination

Uses dependency injection for file system and pattern analysis services.
"""

import ast
import logging
from pathlib import Path
from typing import List
from collections import defaultdict

from desktop.modern.src.core.interfaces.organization_services import (
    IImportAnalysisService,
    IFileSystemService,
    ICodePatternAnalysisService,
    ImportAnalysis,
    ImportStandardizationReport,
)

logger = logging.getLogger(__name__)


class ImportAnalysisService(IImportAnalysisService):
    """
    Pure service for analyzing import patterns in Python files.

    Coordinates AST parsing, pattern analysis, and reporting.
    Uses dependency injection for file system and pattern analysis.
    """

    def __init__(
        self,
        file_system_service: IFileSystemService,
        pattern_analysis_service: ICodePatternAnalysisService,
        project_root: Path,
    ):
        """
        Initialize the import analysis service.

        Args:
            file_system_service: Service for file system operations
            pattern_analysis_service: Service for pattern analysis
            project_root: Root directory of the project
        """
        self.file_system_service = file_system_service
        self.pattern_analysis_service = pattern_analysis_service
        self.project_root = project_root
        self.src_root = project_root / "src"

    def analyze_file(self, file_path: Path) -> ImportAnalysis:
        """
        Analyze import patterns in a single Python file.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            ImportAnalysis with detailed import pattern analysis
        """
        try:
            content = self.file_system_service.read_file(file_path)
            tree = ast.parse(content)

            total_imports = 0
            relative_imports = 0
            absolute_imports = 0
            src_prefix_imports = 0
            inconsistent_imports = []
            recommendations = []

            for node in ast.walk(tree):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    total_imports += 1

                    if isinstance(node, ast.ImportFrom):
                        module_name = node.module or ""

                        # Check for relative imports
                        if node.level > 0:
                            relative_imports += 1

                            # Check for excessive relative import depth
                            if node.level > 3:
                                inconsistent_imports.append(
                                    f"Excessive relative import depth: {'.' * node.level}{module_name}"
                                )
                                recommendations.append(
                                    "Reduce relative import depth to maximum 3 levels"
                                )

                        else:
                            absolute_imports += 1

                            # Check for src. prefix violations
                            if module_name.startswith("src."):
                                src_prefix_imports += 1
                                inconsistent_imports.append(
                                    f"src. prefix violation: {module_name}"
                                )
                                recommendations.append(
                                    f"Remove 'src.' prefix: {module_name} -> {module_name[4:]}"
                                )

                            # Check for standard TKA patterns
                            elif not self.pattern_analysis_service.is_standard_tka_import(
                                module_name
                            ):
                                if not self.pattern_analysis_service.is_external_library(
                                    module_name
                                ):
                                    inconsistent_imports.append(
                                        f"Non-standard TKA import: {module_name}"
                                    )
                                    recommendations.append(
                                        f"Use standard TKA pattern for: {module_name}"
                                    )

            # Calculate compliance score
            compliance_score = (
                self.pattern_analysis_service.calculate_pattern_compliance_score(
                    total_imports, src_prefix_imports, len(inconsistent_imports)
                )
            )

            return ImportAnalysis(
                file_path=file_path,
                total_imports=total_imports,
                relative_imports=relative_imports,
                absolute_imports=absolute_imports,
                src_prefix_imports=src_prefix_imports,
                inconsistent_imports=inconsistent_imports,
                recommendations=list(set(recommendations)),  # Remove duplicates
                compliance_score=compliance_score,
            )

        except Exception as e:
            logger.error(f"Error analyzing file {file_path}: {e}")
            return ImportAnalysis(
                file_path=file_path,
                total_imports=0,
                relative_imports=0,
                absolute_imports=0,
                src_prefix_imports=0,
                inconsistent_imports=[f"Analysis failed: {e}"],
                recommendations=["Fix syntax errors before import analysis"],
                compliance_score=0.0,
            )

    def analyze_codebase(self) -> ImportStandardizationReport:
        """
        Analyze import patterns across the entire codebase.

        Returns:
            ImportStandardizationReport with comprehensive analysis
        """
        python_files = self.file_system_service.find_python_files(self.src_root)
        file_analyses = []

        logger.info(f"Analyzing {len(python_files)} Python files...")

        for file_path in python_files:
            analysis = self.analyze_file(file_path)
            file_analyses.append(analysis)

        # Generate comprehensive report
        total_files = len(file_analyses)
        total_imports = sum(analysis.total_imports for analysis in file_analyses)
        compliant_files = sum(
            1 for analysis in file_analyses if analysis.compliance_score >= 95.0
        )
        non_compliant_files = total_files - compliant_files

        average_compliance = (
            sum(analysis.compliance_score for analysis in file_analyses) / total_files
            if total_files > 0
            else 0.0
        )

        # Collect common violations
        common_violations = defaultdict(int)
        files_needing_fixes = []

        for analysis in file_analyses:
            if analysis.compliance_score < 95.0:
                files_needing_fixes.append(analysis.file_path)

            for violation in analysis.inconsistent_imports:
                violation_type = self.pattern_analysis_service.categorize_violation(
                    violation
                )
                common_violations[violation_type] += 1

        # Generate standardization recommendations
        recommendations = self._generate_standardization_recommendations(file_analyses)

        return ImportStandardizationReport(
            total_files_analyzed=total_files,
            total_imports_found=total_imports,
            compliant_files=compliant_files,
            non_compliant_files=non_compliant_files,
            average_compliance_score=average_compliance,
            common_violations=dict(common_violations),
            files_needing_fixes=files_needing_fixes,
            standardization_recommendations=recommendations,
        )

    def _generate_standardization_recommendations(
        self, analyses: List[ImportAnalysis]
    ) -> List[str]:
        """Generate actionable recommendations for import standardization."""
        recommendations = []

        # Count violation types
        src_prefix_count = sum(analysis.src_prefix_imports for analysis in analyses)
        non_compliant_count = sum(
            1 for analysis in analyses if analysis.compliance_score < 95.0
        )

        if src_prefix_count > 0:
            recommendations.append(
                f"Remove 'src.' prefix from {src_prefix_count} import statements across codebase"
            )

        if non_compliant_count > 0:
            recommendations.append(
                f"Standardize imports in {non_compliant_count} files to follow TKA conventions"
            )

        # Add specific pattern recommendations
        recommendations.extend(
            [
                "Use 'from domain.models.core_models import ...' for domain models",
                "Use 'from application.services import ...' for application services",
                "Use 'from presentation.components import ...' for UI components",
                "Use 'from core.interfaces import ...' for core interfaces",
                "Limit relative imports to maximum 3 levels (../../..)",
                "Use relative imports only within the same module hierarchy",
            ]
        )

        return recommendations

    def get_analysis_summary(self, file_path: Path) -> dict:
        """
        Get a summary of analysis results for a specific file.

        Args:
            file_path: Path to analyze

        Returns:
            Dictionary with analysis summary
        """
        analysis = self.analyze_file(file_path)

        return {
            "file_path": str(analysis.file_path),
            "total_imports": analysis.total_imports,
            "compliance_score": analysis.compliance_score,
            "violations_count": len(analysis.inconsistent_imports),
            "src_prefix_violations": analysis.src_prefix_imports,
            "relative_imports": analysis.relative_imports,
            "absolute_imports": analysis.absolute_imports,
            "needs_fixes": analysis.compliance_score < 95.0,
            "top_recommendations": analysis.recommendations[
                :3
            ],  # Top 3 recommendations
        }

    def validate_project_structure(self) -> dict:
        """
        Validate that the project has the expected structure for analysis.

        Returns:
            Dictionary with validation results
        """
        validation_results = {"valid": True, "issues": [], "recommendations": []}

        # Check if src directory exists
        if not self.src_root.exists():
            validation_results["valid"] = False
            validation_results["issues"].append(
                f"src directory not found: {self.src_root}"
            )
            validation_results["recommendations"].append(
                "Ensure project follows standard src/ layout"
            )

        # Check for expected TKA directories
        expected_dirs = [
            "domain",
            "application",
            "presentation",
            "core",
            "infrastructure",
        ]
        for dir_name in expected_dirs:
            dir_path = self.src_root / dir_name
            if not dir_path.exists():
                validation_results["issues"].append(
                    f"Expected directory not found: {dir_path}"
                )
                validation_results["recommendations"].append(
                    f"Create {dir_name}/ directory for TKA architecture"
                )

        return validation_results
