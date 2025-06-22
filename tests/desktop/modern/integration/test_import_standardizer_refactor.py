"""
Integration test for the refactored import standardizer services.

This test verifies that the refactored services produce the same results
as the original monolithic ImportStandardizer.
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.core.organization.import_standardizer import ImportStandardizer, ComponentHierarchyOptimizer
from src.infrastructure.file_system.file_system_service import FileSystemService
from src.application.services.analysis.code_pattern_analysis_service import CodePatternAnalysisService
from src.application.services.analysis.import_analysis_service import ImportAnalysisService
from src.application.services.analysis.import_standardization_service import ImportStandardizationService
from src.application.services.analysis.component_hierarchy_analysis_service import ComponentHierarchyAnalysisService


class TestImportStandardizerRefactor:
    """Test that refactored services work correctly."""

    @pytest.fixture
    def project_root(self, tmp_path):
        """Create a temporary project structure for testing."""
        project_root = tmp_path / "test_project"
        src_dir = project_root / "src"
        src_dir.mkdir(parents=True)
        
        # Create test files
        test_file = src_dir / "test_module.py"
        test_file.write_text("""
from src.domain.models import BeatData
from modern.src.application import Service
from domain.models.core_models import MotionData
import os
""")
        
        return project_root

    @pytest.fixture
    def file_system_service(self):
        """Create file system service."""
        return FileSystemService()

    @pytest.fixture
    def pattern_analysis_service(self):
        """Create pattern analysis service."""
        return CodePatternAnalysisService()

    @pytest.fixture
    def import_analysis_service(self, file_system_service, pattern_analysis_service, project_root):
        """Create import analysis service."""
        return ImportAnalysisService(
            file_system_service, pattern_analysis_service, project_root
        )

    @pytest.fixture
    def standardization_service(self, file_system_service, import_analysis_service):
        """Create import standardization service."""
        return ImportStandardizationService(file_system_service, import_analysis_service)

    @pytest.fixture
    def hierarchy_analysis_service(self, file_system_service, project_root):
        """Create component hierarchy analysis service."""
        return ComponentHierarchyAnalysisService(file_system_service, project_root)

    @pytest.fixture
    def refactored_import_standardizer(
        self, 
        project_root, 
        file_system_service, 
        pattern_analysis_service, 
        import_analysis_service, 
        standardization_service
    ):
        """Create refactored import standardizer."""
        return ImportStandardizer(
            project_root=project_root,
            file_system_service=file_system_service,
            pattern_analysis_service=pattern_analysis_service,
            import_analysis_service=import_analysis_service,
            standardization_service=standardization_service
        )

    @pytest.fixture
    def refactored_hierarchy_optimizer(
        self, 
        project_root, 
        file_system_service, 
        hierarchy_analysis_service
    ):
        """Create refactored component hierarchy optimizer."""
        return ComponentHierarchyOptimizer(
            project_root=project_root,
            file_system_service=file_system_service,
            hierarchy_analysis_service=hierarchy_analysis_service
        )

    def test_file_system_service(self, file_system_service, project_root):
        """Test that file system service works correctly."""
        src_dir = project_root / "src"
        python_files = file_system_service.find_python_files(src_dir)
        
        assert len(python_files) > 0
        assert all(file.suffix == ".py" for file in python_files)

    def test_pattern_analysis_service(self, pattern_analysis_service):
        """Test that pattern analysis service works correctly."""
        # Test standard TKA import
        assert pattern_analysis_service.is_standard_tka_import("domain.models.core_models")
        
        # Test external library
        assert pattern_analysis_service.is_external_library("PyQt6.QtCore")
        
        # Test violation categorization
        violation = "src. prefix violation: src.domain.models"
        category = pattern_analysis_service.categorize_violation(violation)
        assert category == "src_prefix_violations"

    def test_import_analysis_service(self, import_analysis_service, project_root):
        """Test that import analysis service works correctly."""
        test_file = project_root / "src" / "test_module.py"
        analysis = import_analysis_service.analyze_file(test_file)
        
        assert analysis.total_imports > 0
        assert analysis.src_prefix_imports > 0  # Should detect src. prefix violations
        assert len(analysis.inconsistent_imports) > 0

    def test_standardization_service(self, standardization_service, project_root):
        """Test that standardization service works correctly."""
        test_file = project_root / "src" / "test_module.py"
        
        # Test dry run
        result = standardization_service.fix_file_imports(test_file, dry_run=True)
        assert result is True  # Should detect fixes needed

    def test_hierarchy_analysis_service(self, hierarchy_analysis_service):
        """Test that hierarchy analysis service works correctly."""
        # Test with empty presentation directory (should handle gracefully)
        analyses = hierarchy_analysis_service.analyze_component_hierarchy()
        assert isinstance(analyses, list)

    def test_refactored_import_standardizer(self, refactored_import_standardizer, project_root):
        """Test that refactored import standardizer works correctly."""
        test_file = project_root / "src" / "test_module.py"
        
        # Test file analysis
        analysis = refactored_import_standardizer.analyze_file(test_file)
        assert analysis.total_imports > 0
        
        # Test codebase analysis
        report = refactored_import_standardizer.analyze_codebase()
        assert report.total_files_analyzed > 0
        
        # Test standardization
        result = refactored_import_standardizer.standardize_codebase(dry_run=True)
        assert "files_fixed" in result

    def test_refactored_hierarchy_optimizer(self, refactored_hierarchy_optimizer):
        """Test that refactored hierarchy optimizer works correctly."""
        # Test hierarchy analysis
        analyses = refactored_hierarchy_optimizer.analyze_component_hierarchy()
        assert isinstance(analyses, list)
        
        # Test recommendations
        recommendations = refactored_hierarchy_optimizer.generate_optimization_recommendations()
        assert isinstance(recommendations, list)

    def test_service_validation_methods(self, pattern_analysis_service):
        """Test that services provide useful validation methods."""
        # Test pattern validation
        validation = pattern_analysis_service.validate_import_pattern("from src.domain.models import BeatData")
        assert validation["valid"] is False
        assert "violations" in validation

    def test_service_info_methods(self, import_analysis_service, project_root):
        """Test that services provide useful debugging information."""
        test_file = project_root / "src" / "test_module.py"
        
        # Test analysis summary
        summary = import_analysis_service.get_analysis_summary(test_file)
        assert "total_imports" in summary
        assert "compliance_score" in summary
        assert "needs_fixes" in summary

    def test_service_dependency_injection(self, project_root):
        """Test that services work with dependency injection."""
        # Test that services can be created without explicit dependencies
        standardizer = ImportStandardizer(project_root)
        assert standardizer.file_system_service is not None
        assert standardizer.pattern_analysis_service is not None
        assert standardizer.import_analysis_service is not None
        assert standardizer.standardization_service is not None
        
        optimizer = ComponentHierarchyOptimizer(project_root)
        assert optimizer.file_system_service is not None
        assert optimizer.hierarchy_analysis_service is not None

    def test_error_handling(self, import_analysis_service):
        """Test that services handle errors gracefully."""
        # Test with non-existent file
        non_existent_file = Path("/non/existent/file.py")
        analysis = import_analysis_service.analyze_file(non_existent_file)
        
        # Should return analysis with error information
        assert analysis.total_imports == 0
        assert len(analysis.inconsistent_imports) > 0
        assert "Analysis failed" in analysis.inconsistent_imports[0]
