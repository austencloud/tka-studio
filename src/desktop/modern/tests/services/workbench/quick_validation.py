"""
Quick validation script for workbench services

This script provides a fast way to validate that the new workbench services
are working correctly without running the full test suite.
"""

import sys
from pathlib import Path

def main():
    """Quick validation of workbench services."""
    print("🚀 Quick Workbench Service Validation")
    print("=" * 40)
    
    try:
        # Add src to Python path
        project_root = Path(__file__).parent.parent.parent.parent
        project_src = project_root / "src"
        
        if str(project_src) not in sys.path:
            sys.path.insert(0, str(project_src))
        
        print("📦 Testing imports...")
        
        # Test export service
        print("  🔧 WorkbenchExportService...", end=" ")
        from desktop.modern.application.services.workbench.workbench_export_service import WorkbenchExportService
        export_service = WorkbenchExportService()
        assert export_service.validate_export_directory()
        print("✅")
        
        # Test clipboard service
        print("  📋 WorkbenchClipboardService...", end=" ")
        from desktop.modern.application.services.workbench.workbench_clipboard_service import (
            WorkbenchClipboardService, MockClipboardAdapter
        )
        clipboard_service = WorkbenchClipboardService(MockClipboardAdapter())
        success, _ = clipboard_service.copy_text_to_clipboard("test")
        assert success
        print("✅")
        
        # Test coordinator
        print("  🎛️ EnhancedWorkbenchOperationCoordinator...", end=" ")
        from shared.application.services.workbench.enhanced_workbench_operation_coordinator import (
            EnhancedWorkbenchOperationCoordinator
        )
        coordinator = EnhancedWorkbenchOperationCoordinator()
        status = coordinator.get_operation_status_summary()
        assert isinstance(status, dict)
        print("✅")
        
        # Test interfaces
        print("  📄 Service interfaces...", end=" ")
        from desktop.modern.core.interfaces.workbench_export_services import IWorkbenchExportService
        print("✅")
        
        print("\n🎉 All validations passed!")
        print("✅ New workbench services are ready for use.")
        return True
        
    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
