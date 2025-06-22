"""
Import Standardization Tool for TKA Desktop

REFACTORED: Thin orchestration layer that coordinates specialized services.
Replaces the monolithic ImportStandardizer with clean architecture.

PROVIDES:
- Complete import analysis and standardization pipeline
- Immutable analysis result data
- Clean separation of concerns
- Dependency injection for all operations
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Union

from core.interfaces.organization_services import (
    ComponentHierarchyAnalysis,
    ICodePatternAnalysisService,
    IComponentHierarchyAnalysisService,
    IFileSystemService,
    IImportAnalysisService,
    IImportStandardizationService,
    ImportAnalysis,
    ImportStandardizationReport,
)

logger = logging.getLogger(__name__)


class ImportStandardizer:
    """
    Orchestrates the complete import analysis and standardization pipeline.

    REFACTORED: Thin coordination layer that delegates to specialized services.
    Follows TKA's clean architecture and dependency injection patterns.
    """

    def __init__(
        self,
        project_root: Path,
        file_system_service: Optional[IFileSystemService] = None,
        pattern_analysis_service: Optional[ICodePatternAnalysisService] = None,
        import_analysis_service: Optional[IImportAnalysisService] = None,
        standardization_service: Optional[IImportStandardizationService] = None,
    ):
        """
        Initialize import standardizer with dependency injection.

        Args:
            project_root: Root directory of the TKA Desktop project
            file_system_service: Service for file system operations
            pattern_analysis_service: Service for pattern analysis
            import_analysis_service: Service for import analysis
            standardization_service: Service for import standardization
        """
        self.project_root = project_root

        # Initialize services with dependency injection
        if file_system_service is None:
            from infrastructure.file_system.file_system_service import FileSystemService

            file_system_service = FileSystemService()

        if pattern_analysis_service is None:
            from application.services.analysis.code_pattern_analysis_service import (
                CodePatternAnalysisService,
            )

            pattern_analysis_service = CodePatternAnalysisService()

        if import_analysis_service is None:
            from application.services.analysis.import_analysis_service import (
                ImportAnalysisService,
            )

            import_analysis_service = ImportAnalysisService(
                file_system_service, pattern_analysis_service, project_root
            )

        if standardization_service is None:
            from application.services.analysis.import_standardization_service import (
                ImportStandardizationService,
            )

            standardization_service = ImportStandardizationService(
                file_system_service, import_analysis_service
            )

        self.file_system_service = file_system_service
        self.pattern_analysis_service = pattern_analysis_service
        self.import_analysis_service = import_analysis_service
        self.standardization_service = standardization_service

        logger.info(f"Import standardizer initialized for project: {project_root}")

    def analyze_file(self, file_path: Path) -> ImportAnalysis:
        """
        Analyze import patterns in a single Python file using analysis service.

        Args:
            file_path: Path to the Python file to analyze

        Returns:
            ImportAnalysis with detailed import pattern analysis
        """
        return self.import_analysis_service.analyze_file(file_path)

    def analyze_codebase(self) -> ImportStandardizationReport:
        """
        Analyze import patterns across the entire codebase using analysis service.

        Returns:
            ImportStandardizationReport with comprehensive analysis
        """
        return self.import_analysis_service.analyze_codebase()

    def fix_file_imports(self, file_path: Path, dry_run: bool = True) -> bool:
        """
        Fix import patterns in a single file using standardization service.

        Args:
            file_path: Path to the file to fix
            dry_run: If True, only show what would be changed

        Returns:
            True if fixes were applied (or would be applied in dry_run)
        """
        return self.standardization_service.fix_file_imports(file_path, dry_run)

    def standardize_codebase(
        self, dry_run: bool = True
    ) -> Dict[str, Union[int, float]]:
        """
        Standardize imports across the entire codebase using standardization service.

        Args:
            dry_run: If True, only show what would be changed

        Returns:
            Dictionary with fix statistics
        """
        return self.standardization_service.standardize_codebase(dry_run)


# ============================================================================
# COMPONENT HIERARCHY OPTIMIZER - REFACTORED
# ============================================================================


class ComponentHierarchyOptimizer:
    """
    Orchestrates the complete component hierarchy analysis pipeline.

    REFACTORED: Thin coordination layer that delegates to specialized services.
    Follows TKA's clean architecture and dependency injection patterns.
    """

    def __init__(
        self,
        project_root: Path,
        file_system_service: Optional[IFileSystemService] = None,
        hierarchy_analysis_service: Optional[IComponentHierarchyAnalysisService] = None,
    ):
        """
        Initialize component hierarchy optimizer with dependency injection.

        Args:
            project_root: Root directory of the project
            file_system_service: Service for file system operations
            hierarchy_analysis_service: Service for hierarchy analysis
        """
        self.project_root = project_root

        # Initialize services with dependency injection
        if file_system_service is None:
            from infrastructure.file_system.file_system_service import FileSystemService

            file_system_service = FileSystemService()

        if hierarchy_analysis_service is None:
            from application.services.analysis.component_hierarchy_analysis_service import (
                ComponentHierarchyAnalysisService,
            )

            hierarchy_analysis_service = ComponentHierarchyAnalysisService(
                file_system_service, project_root
            )

        self.file_system_service = file_system_service
        self.hierarchy_analysis_service = hierarchy_analysis_service

        logger.info(f"Component hierarchy optimizer initialized for: {project_root}")

    def analyze_component_hierarchy(self) -> List[ComponentHierarchyAnalysis]:
        """
        Analyze component hierarchy across presentation layer using analysis service.

        Returns:
            List of ComponentHierarchyAnalysis for each component
        """
        return self.hierarchy_analysis_service.analyze_component_hierarchy()

    def generate_optimization_recommendations(self) -> List[str]:
        """
        Generate optimization recommendations for component hierarchy using analysis service.

        Returns:
            List of actionable optimization recommendations
        """
        return self.hierarchy_analysis_service.generate_optimization_recommendations()
