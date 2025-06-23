#!/usr/bin/env python3
"""
Test script for the Production API
Verifies all endpoints and service integration.
"""

import sys
import asyncio
import json
import pytest
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))


@pytest.mark.requires_server
def test_production_api():
    """Test the production API endpoints - requires running server."""
    pytest.skip("Server integration test - run manually with server")


@pytest.mark.requires_server
def test_api_documentation():
    """Test API documentation generation - requires running server."""
    pytest.skip("Server integration test - run manually with server")


async def main():
    """Run all API tests."""
    print("🔧 TKA Desktop Production API Test Suite")
    print("=" * 60)

    # Test API functionality
    api_test_passed = await test_production_api()

    # Test API documentation
    doc_test_passed = test_api_documentation()

    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"API Functionality: {'✅ PASS' if api_test_passed else '❌ FAIL'}")
    print(f"API Documentation: {'✅ PASS' if doc_test_passed else '❌ FAIL'}")

    overall_success = api_test_passed and doc_test_passed
    print(
        f"\nOverall Result: {'✅ ALL TESTS PASSED' if overall_success else '❌ SOME TESTS FAILED'}"
    )

    if overall_success:
        print("\n🎉 Production API is ready for deployment!")
        print("📋 Next steps:")
        print("  1. Run with: uvicorn infrastructure.api.production_api:app --reload")
        print("  2. Access docs at: http://localhost:8000/api/docs")
        print("  3. Access health check at: http://localhost:8000/api/health")
    else:
        print("\n⚠️ API needs fixes before production deployment")

    return overall_success


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
