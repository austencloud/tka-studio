"""
Configuration Manager for TKA Application

Handles all configuration loading, validation, environment setup, and argument parsing.
Extracted from main.py to follow Single Responsibility Principle.

This class centralizes all configuration concerns including:
- Command line argument parsing
- Environment variable detection
- Application mode determination
- Logging configuration
- Parallel testing configuration
"""

import argparse
import logging
import os
import sys
from dataclasses import dataclass
from typing import Optional, Tuple

from desktop.modern.core.application.application_factory import ApplicationMode
from desktop.modern.core.error_handling import StandardErrorHandler


@dataclass
class ApplicationConfiguration:
    """Immutable configuration object for the TKA application."""

    mode: str
    parallel_testing: bool
    monitor: Optional[str]
    geometry: Optional[str]
    test_generation: bool


class ConfigurationManager:
    """
    Manages all application configuration concerns.

    Provides centralized configuration loading, validation, and environment setup
    to replace scattered configuration patterns throughout main.py.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._config: Optional[ApplicationConfiguration] = None

    def load_configuration(self) -> ApplicationConfiguration:
        """
        Load and validate complete application configuration.

        Returns:
            ApplicationConfiguration: Immutable configuration object

        Raises:
            ConfigurationError: If configuration is invalid or incomplete
        """
        try:
            # Parse command line arguments
            app_mode = self._determine_application_mode()

            # Detect parallel testing configuration
            parallel_mode, monitor, geometry = self._detect_parallel_testing_mode()

            # Check for test generation flag
            test_generation = "--test-generation" in sys.argv

            # Set up logging configuration
            self._configure_logging()

            # Create immutable configuration
            config = ApplicationConfiguration(
                mode=app_mode,
                parallel_testing=parallel_mode,
                monitor=monitor,
                geometry=geometry,
                test_generation=test_generation,
            )

            self.logger.info(f"🔧 Application Mode: {config.mode}")
            return config

        except Exception as e:
            StandardErrorHandler.handle_initialization_error(
                "Configuration loading", e, self.logger, is_critical=True
            )
            raise

    def _determine_application_mode(self) -> str:
        """
        Determine application mode from command line arguments.

        Returns:
            str: Application mode constant
        """
        if "--test" in sys.argv:
            return ApplicationMode.TEST
        else:
            return ApplicationMode.PRODUCTION

    def _detect_parallel_testing_mode(
        self,
    ) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Detect parallel testing configuration from arguments and environment.

        Returns:
            Tuple of (parallel_mode, monitor, geometry)
        """
        try:
            parser = argparse.ArgumentParser(add_help=False)
            parser.add_argument("--parallel-testing", action="store_true")
            parser.add_argument(
                "--monitor", choices=["primary", "secondary", "left", "right"]
            )
            args, _ = parser.parse_known_args()

            # Check environment variables
            env_parallel = os.environ.get("TKA_PARALLEL_TESTING", "").lower() == "true"
            env_monitor = os.environ.get("TKA_PARALLEL_MONITOR", "")
            env_geometry = os.environ.get("TKA_PARALLEL_GEOMETRY", "")

            parallel_mode = args.parallel_testing or env_parallel
            monitor = args.monitor or env_monitor or None
            geometry = env_geometry or None

            return parallel_mode, monitor, geometry

        except Exception as e:
            self.logger.warning(f"Failed to detect parallel testing mode: {e}")
            return False, None, None

    def _configure_logging(self) -> None:
        """Configure application logging for quiet startup."""
        try:
            from desktop.modern.core.logging.instant_fix import apply_instant_fix

            apply_instant_fix("quiet")
        except Exception as e:
            self.logger.warning(f"⚠️ Could not apply logging fix: {e}")
