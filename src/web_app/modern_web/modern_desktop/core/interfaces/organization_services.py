"""
Interface definitions for code organization services.

These interfaces define the contracts for services that analyze and optimize
code organization, following TKA's clean architecture principles.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path


@dataclass
class ImportAnalysis:
    """Analysis results for import patterns in a file."""

    file_path: Path
    total_imports: int
    relative_imports: int
    absolute_imports: int
    src_prefix_imports: int
    inconsistent_imports: list[str]
    recommendations: list[str]
    compliance_score: float


@dataclass
class ImportStandardizationReport:
    """Comprehensive report of import standardization across codebase."""

    total_files_analyzed: int
    total_imports_found: int
    compliant_files: int
    non_compliant_files: int
    average_compliance_score: float
    common_violations: dict[str, int]
    files_needing_fixes: list[Path]
    standardization_recommendations: list[str]


@dataclass
class ComponentHierarchyAnalysis:
    """Analysis of component hierarchy depth and structure."""

    component_path: Path
    hierarchy_depth: int
    class_count: int
    method_count: int
    complexity_score: float
    responsibilities: list[str]
    recommendations: list[str]


class IImportAnalysisService(ABC):
    """Interface for analyzing import patterns in Python files."""

    @abstractmethod
    def analyze_file(self, file_path: Path) -> ImportAnalysis:
        """
        Analyze import patterns in a single Python file.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            ImportAnalysis with detailed import pattern analysis
        """

    @abstractmethod
    def analyze_codebase(self) -> ImportStandardizationReport:
        """
        Analyze import patterns across the entire codebase.

        Returns:
            ImportStandardizationReport with comprehensive analysis
        """


class IImportStandardizationService(ABC):
    """Interface for standardizing import patterns in Python files."""

    @abstractmethod
    def fix_file_imports(self, file_path: Path, dry_run: bool = True) -> bool:
        """
        Fix import patterns in a single file.

        Args:
            file_path: Path to the file to fix
            dry_run: If True, only show what would be changed

        Returns:
            True if fixes were applied (or would be applied in dry_run)
        """

    @abstractmethod
    def standardize_codebase(self, dry_run: bool = True) -> dict[str, int | float]:
        """
        Standardize imports across the entire codebase.

        Args:
            dry_run: If True, only show what would be changed

        Returns:
            Dictionary with fix statistics
        """


class IComponentHierarchyAnalysisService(ABC):
    """Interface for analyzing component hierarchy structure."""

    @abstractmethod
    def analyze_component_hierarchy(self) -> list[ComponentHierarchyAnalysis]:
        """
        Analyze component hierarchy across presentation layer.

        Returns:
            List of ComponentHierarchyAnalysis for each component
        """

    @abstractmethod
    def generate_optimization_recommendations(self) -> list[str]:
        """
        Generate optimization recommendations for component hierarchy.

        Returns:
            List of actionable optimization recommendations
        """


class IFileSystemService(ABC):
    """Interface for file system operations used by organization services."""

    @abstractmethod
    def read_file(self, file_path: Path) -> str:
        """
        Read content from a file.

        Args:
            file_path: Path to the file to read

        Returns:
            File content as string
        """

    @abstractmethod
    def write_file(self, file_path: Path, content: str) -> None:
        """
        Write content to a file.

        Args:
            file_path: Path to the file to write
            content: Content to write
        """

    @abstractmethod
    def find_python_files(self, root_path: Path) -> list[Path]:
        """
        Find all Python files in a directory tree.

        Args:
            root_path: Root directory to search

        Returns:
            List of Python file paths
        """


class ICodePatternAnalysisService(ABC):
    """Interface for analyzing code patterns and violations."""

    @abstractmethod
    def is_standard_tka_import(self, module_name: str) -> bool:
        """
        Check if import follows standard TKA patterns.

        Args:
            module_name: Module name to check

        Returns:
            True if import follows TKA standards
        """

    @abstractmethod
    def is_external_library(self, module_name: str) -> bool:
        """
        Check if import is from external library.

        Args:
            module_name: Module name to check

        Returns:
            True if import is from external library
        """

    @abstractmethod
    def categorize_violation(self, violation: str) -> str:
        """
        Categorize violation type for reporting.

        Args:
            violation: Violation description

        Returns:
            Violation category
        """
