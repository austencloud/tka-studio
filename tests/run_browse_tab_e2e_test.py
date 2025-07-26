#!/usr/bin/env python3
"""
Browse Tab E2E Test Runner

Simple script to run the Browse tab end-to-end test.
Based on the existing test runner patterns.
"""

import logging
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tests.e2e.test_browse_tab_workflow import BrowseTabWorkflowTest

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("browse_tab_e2e_test.log"),
    ],
)

logger = logging.getLogger(__name__)


def main():
    """Run the Browse tab E2E test."""
    logger.info("🚀 Starting Browse Tab E2E Test...")

    try:
        # Create and run the test
        test = BrowseTabWorkflowTest()
        success = test.run_test()

        if success:
            logger.info("🎉 Browse Tab E2E Test completed successfully!")
            return 0
        else:
            logger.error("❌ Browse Tab E2E Test failed!")
            return 1

    except Exception as e:
        logger.error(f"❌ Test runner failed: {e}")
        import traceback

        traceback.print_exc()
        return 1
    finally:
        logger.info("🏁 Browse Tab E2E Test finished")


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
