"""
Component Hierarchy Analysis Service

Pure service for analyzing component hierarchy structure and complexity.
Extracted from ComponentHierarchyOptimizer to follow single responsibility principle.

This service handles:
- Component hierarchy depth analysis
- Class and method complexity analysis
- Responsibility extraction from method names
- Optimization recommendations generation

Uses dependency injection for file system operations.
"""

import ast
import logging
from pathlib import Path
from typing import List, Optional

from desktop.modern.src.core.interfaces.organization_services import (
    IComponentHierarchyAnalysisService,
    IFileSystemService,
    ComponentHierarchyAnalysis,
)

logger = logging.getLogger(__name__)


class ComponentHierarchyAnalysisService(IComponentHierarchyAnalysisService):
    """
    Pure service for analyzing component hierarchy structure and complexity.

    Analyzes presentation layer components to identify architectural issues
    and optimization opportunities. Uses AST parsing for code analysis.
    """

    def __init__(self, file_system_service: IFileSystemService, project_root: Path):
        """
        Initialize the component hierarchy analysis service.

        Args:
            file_system_service: Service for file system operations
            project_root: Root directory of the project
        """
        self.file_system_service = file_system_service
        self.project_root = project_root
        self.presentation_root = project_root / "src" / "presentation" / "components"

        # Configuration thresholds
        self.max_hierarchy_depth = 3
        self.max_methods_per_class = 15
        self.max_lines_per_method = 50
        self.max_classes_per_file = 3

    def analyze_component_hierarchy(self) -> List[ComponentHierarchyAnalysis]:
        """
        Analyze component hierarchy across presentation layer.

        Returns:
            List of ComponentHierarchyAnalysis for each component
        """
        if not self.presentation_root.exists():
            logger.warning(
                f"Presentation components directory not found: {self.presentation_root}"
            )
            return []

        analyses = []
        component_files = self.file_system_service.find_python_files(
            self.presentation_root
        )

        logger.info(f"Analyzing {len(component_files)} component files...")

        for component_file in component_files:
            analysis = self._analyze_single_component(component_file)
            if analysis:
                analyses.append(analysis)

        return analyses

    def generate_optimization_recommendations(self) -> List[str]:
        """
        Generate optimization recommendations for component hierarchy.

        Returns:
            List of actionable optimization recommendations
        """
        analyses = self.analyze_component_hierarchy()
        recommendations = []

        # Find components with excessive depth
        deep_components = [
            a for a in analyses if a.hierarchy_depth > self.max_hierarchy_depth
        ]
        if deep_components:
            recommendations.append(
                f"Flatten {len(deep_components)} components with excessive hierarchy depth"
            )

        # Find components with multiple responsibilities
        complex_components = [a for a in analyses if len(a.responsibilities) > 3]
        if complex_components:
            recommendations.append(
                f"Decompose {len(complex_components)} components with multiple responsibilities"
            )

        # Find components with low complexity scores
        low_score_components = [a for a in analyses if a.complexity_score < 70]
        if low_score_components:
            recommendations.append(
                f"Refactor {len(low_score_components)} components with high complexity"
            )

        # Find components with too many methods
        method_heavy_components = [
            a for a in analyses if a.method_count > self.max_methods_per_class
        ]
        if method_heavy_components:
            recommendations.append(
                f"Split {len(method_heavy_components)} components with excessive methods"
            )

        # Find components with too many classes
        class_heavy_components = [
            a for a in analyses if a.class_count > self.max_classes_per_file
        ]
        if class_heavy_components:
            recommendations.append(
                f"Separate {len(class_heavy_components)} files with multiple classes"
            )

        return recommendations

    def _analyze_single_component(
        self, component_path: Path
    ) -> Optional[ComponentHierarchyAnalysis]:
        """
        Analyze a single component file.

        Args:
            component_path: Path to the component file

        Returns:
            ComponentHierarchyAnalysis or None if analysis failed
        """
        try:
            # Calculate hierarchy depth from path
            relative_path = component_path.relative_to(self.presentation_root)
            hierarchy_depth = len(relative_path.parts) - 1  # Subtract filename

            content = self.file_system_service.read_file(component_path)
            tree = ast.parse(content)

            class_count = 0
            method_count = 0
            responsibilities = []
            recommendations = []

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_count += 1

                    # Analyze class methods
                    class_methods = [
                        n for n in node.body if isinstance(n, ast.FunctionDef)
                    ]
                    method_count += len(class_methods)

                    # Check for excessive methods
                    if len(class_methods) > self.max_methods_per_class:
                        recommendations.append(
                            f"Class {node.name} has {len(class_methods)} methods "
                            f"(max: {self.max_methods_per_class}) - consider decomposition"
                        )

                    # Identify responsibilities from method names
                    responsibilities.extend(
                        self._extract_responsibilities(class_methods)
                    )

            # Check hierarchy depth
            if hierarchy_depth > self.max_hierarchy_depth:
                recommendations.append(
                    f"Hierarchy depth {hierarchy_depth} exceeds maximum {self.max_hierarchy_depth} "
                    f"- consider flattening structure"
                )

            # Check for too many classes in one file
            if class_count > self.max_classes_per_file:
                recommendations.append(
                    f"File contains {class_count} classes (max: {self.max_classes_per_file}) "
                    f"- consider splitting into separate files"
                )

            # Calculate complexity score
            complexity_score = self._calculate_complexity_score(
                hierarchy_depth, class_count, method_count
            )

            return ComponentHierarchyAnalysis(
                component_path=component_path,
                hierarchy_depth=hierarchy_depth,
                class_count=class_count,
                method_count=method_count,
                complexity_score=complexity_score,
                responsibilities=list(set(responsibilities)),
                recommendations=recommendations,
            )

        except Exception as e:
            logger.error(f"Error analyzing component {component_path}: {e}")
            return None

    def _extract_responsibilities(self, methods: List[ast.FunctionDef]) -> List[str]:
        """
        Extract responsibilities from method names.

        Args:
            methods: List of method AST nodes

        Returns:
            List of identified responsibilities
        """
        responsibilities = []

        for method in methods:
            method_name = method.name

            # Skip special methods
            if method_name.startswith("__"):
                continue

            # Categorize by method name patterns
            if any(
                pattern in method_name.lower() for pattern in ["load", "fetch", "get"]
            ):
                responsibilities.append("data_loading")
            elif any(
                pattern in method_name.lower()
                for pattern in ["save", "store", "persist"]
            ):
                responsibilities.append("data_persistence")
            elif any(
                pattern in method_name.lower()
                for pattern in ["render", "draw", "paint"]
            ):
                responsibilities.append("rendering")
            elif any(
                pattern in method_name.lower()
                for pattern in ["handle", "on_", "process"]
            ):
                responsibilities.append("event_handling")
            elif any(
                pattern in method_name.lower()
                for pattern in ["validate", "check", "verify"]
            ):
                responsibilities.append("validation")
            elif any(
                pattern in method_name.lower()
                for pattern in ["update", "refresh", "sync"]
            ):
                responsibilities.append("state_management")
            elif any(
                pattern in method_name.lower()
                for pattern in ["create", "build", "make"]
            ):
                responsibilities.append("object_creation")
            elif any(
                pattern in method_name.lower()
                for pattern in ["calculate", "compute", "process"]
            ):
                responsibilities.append("computation")
            else:
                responsibilities.append("business_logic")

        return responsibilities

    def _calculate_complexity_score(
        self, depth: int, classes: int, methods: int
    ) -> float:
        """
        Calculate component complexity score.

        Args:
            depth: Hierarchy depth
            classes: Number of classes
            methods: Number of methods

        Returns:
            Complexity score (0-100, higher is better)
        """
        # Base score starts at 100
        score = 100.0

        # Deduct for excessive depth
        if depth > self.max_hierarchy_depth:
            score -= (depth - self.max_hierarchy_depth) * 15

        # Deduct for too many classes in one file
        if classes > self.max_classes_per_file:
            score -= (classes - self.max_classes_per_file) * 10

        # Deduct for too many methods
        if methods > 20:
            score -= (methods - 20) * 2

        return max(0.0, score)

    def get_component_summary(self, component_path: Path) -> dict:
        """
        Get a summary of analysis results for a specific component.

        Args:
            component_path: Path to analyze

        Returns:
            Dictionary with component summary
        """
        analysis = self._analyze_single_component(component_path)

        if not analysis:
            return {"error": "Analysis failed"}

        return {
            "component_path": str(analysis.component_path),
            "hierarchy_depth": analysis.hierarchy_depth,
            "class_count": analysis.class_count,
            "method_count": analysis.method_count,
            "complexity_score": analysis.complexity_score,
            "responsibilities": analysis.responsibilities,
            "recommendations_count": len(analysis.recommendations),
            "needs_refactoring": analysis.complexity_score < 70,
            "top_recommendations": analysis.recommendations[
                :3
            ],  # Top 3 recommendations
        }

    def validate_component_structure(self) -> dict:
        """
        Validate that the component structure follows TKA conventions.

        Returns:
            Dictionary with validation results
        """
        validation_results = {"valid": True, "issues": [], "recommendations": []}

        # Check if presentation directory exists
        if not self.presentation_root.exists():
            validation_results["valid"] = False
            validation_results["issues"].append(
                f"Presentation directory not found: {self.presentation_root}"
            )
            validation_results["recommendations"].append(
                "Create presentation/components/ directory structure"
            )

        # Check for expected component subdirectories
        if self.presentation_root.exists():
            expected_subdirs = ["workbench", "option_picker", "sequence_widget"]
            for subdir in expected_subdirs:
                subdir_path = self.presentation_root / subdir
                if not subdir_path.exists():
                    validation_results["issues"].append(
                        f"Expected component directory not found: {subdir_path}"
                    )
                    validation_results["recommendations"].append(
                        f"Consider organizing components in {subdir}/ directory"
                    )

        return validation_results
