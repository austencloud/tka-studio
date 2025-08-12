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

from __future__ import annotations

from dataclasses import dataclass
import logging
import sys

from desktop.modern.core.application.application_factory import ApplicationMode
from desktop.modern.core.error_handling import StandardErrorHandler


@dataclass
class ApplicationConfiguration:
    """Immutable configuration object for the TKA application."""

    mode: str


class ConfigurationManager:
    """
    Manages all application configuration concerns.

    Provides centralized configuration loading, validation, and environment setup
    to replace scattered configuration patterns throughout main.py.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._config: ApplicationConfiguration | None = None

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



            # Create immutable configuration
            config = ApplicationConfiguration(mode=app_mode)

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
        return ApplicationMode.PRODUCTION

