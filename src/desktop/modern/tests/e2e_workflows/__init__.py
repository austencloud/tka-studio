"""
Optimized E2E Workflows Package
===============================

Clean, efficient end-to-end testing with zero duplication.

Usage:
    # Run all tab workflow tests
    from tests.e2e_workflows import run_optimized_e2e_tests
    results = run_optimized_e2e_tests()

    # Run specific tab test  
    from tests.e2e_workflows import run_tab_test
    results = run_tab_test('construct')

    # Custom test infrastructure usage
    from tests.e2e_workflows import get_test_infrastructure
    infra = get_test_infrastructure()
    service = infra.get_service('start_position_data')
"""

from .test_infrastructure import get_test_infrastructure, TestInfrastructure
from .test_runner import run_optimized_e2e_tests, run_tab_test, OptimizedTestRunner
from .base_tab_test import BaseTabTest, TabTestPlan, TabType, TestAction

# Convenience imports for test creation
from .base_tab_test import setup_action, workflow_action, validation_action, cleanup_action

__all__ = [
    # Main entry points
    'run_optimized_e2e_tests',
    'run_tab_test',
    
    # Infrastructure
    'get_test_infrastructure', 
    'TestInfrastructure',
    'OptimizedTestRunner',
    
    # Base classes for creating new tests
    'BaseTabTest',
    'TabTestPlan', 
    'TabType',
    'TestAction',
    
    # Helper functions
    'setup_action',
    'workflow_action', 
    'validation_action',
    'cleanup_action',
]
