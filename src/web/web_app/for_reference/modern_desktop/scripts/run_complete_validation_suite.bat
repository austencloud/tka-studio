@echo off
echo === RUNNING COMPLETE VALIDATION SUITE ===
echo.

echo [1/6] Basic Structure Validation...
F:\CODE\TKA\.venv\Scripts\python.exe basic_validation.py
if %errorlevel% neq 0 (
    echo ❌ Basic validation failed!
    exit /b 1
)
echo.

echo [2/6] Comprehensive Service Validation...
F:\CODE\TKA\.venv\Scripts\python.exe validate_start_position_services.py
if %errorlevel% neq 0 (
    echo ❌ Service validation failed!
    exit /b 1
)
echo.

echo [3/6] Integration Validation...
F:\CODE\TKA\.venv\Scripts\python.exe validate_integration_nogui.py
if %errorlevel% neq 0 (
    echo ❌ Integration validation failed!
    exit /b 1
)
echo.

echo [4/6] Service Functionality Tests...
F:\CODE\TKA\.venv\Scripts\python.exe test_service_functionality.py
if %errorlevel% neq 0 (
    echo ❌ Service functionality tests failed!
    exit /b 1
)
echo.

echo [5/6] Component Service Usage Verification...
F:\CODE\TKA\.venv\Scripts\python.exe verify_component_service_usage_signatures.py
if %errorlevel% neq 0 (
    echo ❌ Component service usage verification failed!
    exit /b 1
)
echo.

echo [6/6] Backward Compatibility Verification...
F:\CODE\TKA\.venv\Scripts\python.exe verify_backward_compatibility.py
if %errorlevel% neq 0 (
    echo ❌ Backward compatibility verification failed!
    exit /b 1
)
echo.

echo === ALL VALIDATIONS COMPLETE ===
echo ✅ ALL TESTS PASSED - START POSITION SERVICE REFACTORING COMPLETE!
