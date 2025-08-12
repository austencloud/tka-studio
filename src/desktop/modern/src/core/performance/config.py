"""
Performance Configuration Management

Provides configuration management for the TKA performance framework.
Integrates with existing configuration patterns and supports environment-based settings.
"""
from __future__ import annotations

from dataclasses import dataclass
import logging
import os


# Result pattern removed - using simple exceptions

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProfilingConfig:
    """Configuration for profiling operations."""

    enabled: bool = True
    overhead_threshold_percent: float = 1.0
    bottleneck_threshold_ms: float = 50.0
    memory_threshold_mb: float = 200.0
    cache_enabled: bool = True
    cache_size: int = 1000
    session_timeout_minutes: int = 60


@dataclass(frozen=True)
class MonitoringConfig:
    """Configuration for real-time monitoring."""

    enabled: bool = True
    interval_ms: int = 1000
    system_metrics: bool = True
    qt_metrics: bool = True
    memory_tracking: bool = True
    alert_thresholds: dict[str, float] = None

    def __post_init__(self):
        if self.alert_thresholds is None:
            object.__setattr__(
                self,
                "alert_thresholds",
                {"cpu_percent": 80.0, "memory_mb": 500.0, "function_time_ms": 100.0},
            )


@dataclass(frozen=True)
class RegressionConfig:
    """Configuration for regression detection."""

    enabled: bool = True
    threshold_percent: float = 5.0
    baseline_days: int = 7
    auto_baseline_update: bool = True
    critical_functions: list[str] = None

    def __post_init__(self):
        if self.critical_functions is None:
            object.__setattr__(
                self,
                "critical_functions",
                [
                    "ArrowRenderer._load_svg_file_cached",
                    "ConstructorResolver._get_cached_signature",
                    "PictographScene.render",
                    "SpecialPlacementService.__init__",
                ],
            )


@dataclass(frozen=True)
class StorageConfig:
    """Configuration for performance data storage."""

    data_dir: str = "data/performance"
    database_path: str = "data/performance/performance.db"
    max_sessions: int = 1000
    retention_days: int = 30
    backup_enabled: bool = True

    def with_database_path(self, new_path: str) -> StorageConfig:
        """Create a new StorageConfig with a different database path."""
        return StorageConfig(
            data_dir=self.data_dir,
            database_path=new_path,
            max_sessions=self.max_sessions,
            retention_days=self.retention_days,
            backup_enabled=self.backup_enabled,
        )


@dataclass(frozen=True)
class PerformanceConfig:
    """
    Comprehensive performance configuration.

    Integrates with existing TKA configuration patterns and provides
    environment-based configuration support.
    """

    profiling: ProfilingConfig
    monitoring: MonitoringConfig
    regression: RegressionConfig
    storage: StorageConfig
    environment: str = "development"

    @classmethod
    def create_default(cls) -> PerformanceConfig:
        """Create default performance configuration."""
        return cls(
            profiling=ProfilingConfig(),
            monitoring=MonitoringConfig(),
            regression=RegressionConfig(),
            storage=StorageConfig(),
            environment=os.getenv("TKA_ENV", "development"),
        )

    @classmethod
    def from_environment(cls) -> PerformanceConfig:
        """
        Create configuration from environment variables.

        Returns:
            PerformanceConfig instance
        """
        try:
            # Profiling configuration
            profiling = ProfilingConfig(
                enabled=os.getenv("TKA_PROFILING_ENABLED", "true").lower() == "true",
                overhead_threshold_percent=float(
                    os.getenv("TKA_PROFILING_OVERHEAD_THRESHOLD", "1.0")
                ),
                bottleneck_threshold_ms=float(
                    os.getenv("TKA_PROFILING_BOTTLENECK_THRESHOLD", "50.0")
                ),
                memory_threshold_mb=float(
                    os.getenv("TKA_PROFILING_MEMORY_THRESHOLD", "200.0")
                ),
                cache_enabled=os.getenv("TKA_PROFILING_CACHE_ENABLED", "true").lower()
                == "true",
                cache_size=int(os.getenv("TKA_PROFILING_CACHE_SIZE", "1000")),
                session_timeout_minutes=int(
                    os.getenv("TKA_PROFILING_SESSION_TIMEOUT", "60")
                ),
            )

            # Monitoring configuration
            monitoring = MonitoringConfig(
                enabled=os.getenv("TKA_MONITORING_ENABLED", "true").lower() == "true",
                interval_ms=int(os.getenv("TKA_MONITORING_INTERVAL", "1000")),
                system_metrics=os.getenv(
                    "TKA_MONITORING_SYSTEM_METRICS", "true"
                ).lower()
                == "true",
                qt_metrics=os.getenv("TKA_MONITORING_QT_METRICS", "true").lower()
                == "true",
                memory_tracking=os.getenv(
                    "TKA_MONITORING_MEMORY_TRACKING", "true"
                ).lower()
                == "true",
            )

            # Regression configuration
            regression = RegressionConfig(
                enabled=os.getenv("TKA_REGRESSION_ENABLED", "true").lower() == "true",
                threshold_percent=float(os.getenv("TKA_REGRESSION_THRESHOLD", "5.0")),
                baseline_days=int(os.getenv("TKA_REGRESSION_BASELINE_DAYS", "7")),
                auto_baseline_update=os.getenv(
                    "TKA_REGRESSION_AUTO_BASELINE", "true"
                ).lower()
                == "true",
            )

            # Storage configuration
            storage = StorageConfig(
                data_dir=os.getenv("TKA_PERFORMANCE_DATA_DIR", "data/performance"),
                database_path=os.getenv(
                    "TKA_PERFORMANCE_DB_PATH", "data/performance/performance.db"
                ),
                max_sessions=int(os.getenv("TKA_PERFORMANCE_MAX_SESSIONS", "1000")),
                retention_days=int(os.getenv("TKA_PERFORMANCE_RETENTION_DAYS", "30")),
                backup_enabled=os.getenv(
                    "TKA_PERFORMANCE_BACKUP_ENABLED", "true"
                ).lower()
                == "true",
            )

            config = cls(
                profiling=profiling,
                monitoring=monitoring,
                regression=regression,
                storage=storage,
                environment=os.getenv("TKA_ENV", "development"),
            )

            return config

        except Exception as e:
            logger.exception(
                f"Failed to create performance configuration from environment: {e}"
            )
            return cls.create_default()

    def validate(self) -> bool:
        """
        Validate configuration settings.

        Returns:
            True if valid, False otherwise
        """
        try:
            # Validate profiling settings
            if (
                self.profiling.overhead_threshold_percent < 0
                or self.profiling.overhead_threshold_percent > 10
            ):
                logger.error(
                    "Profiling overhead threshold must be between 0 and 10 percent"
                )
                return False

            if self.profiling.cache_size < 1:
                logger.error("Profiling cache size must be at least 1")
                return False

            # Validate monitoring settings
            if self.monitoring.interval_ms < 100:
                logger.error("Monitoring interval must be at least 100ms")
                return False

            # Validate regression settings
            if self.regression.threshold_percent < 0:
                logger.error("Regression threshold must be non-negative")
                return False

            # Validate storage settings
            if self.storage.retention_days < 1:
                logger.error("Storage retention must be at least 1 day")
                return False

            return True

        except Exception as e:
            logger.exception(f"Configuration validation failed: {e}")
            return False


# Global configuration instance
_global_config: PerformanceConfig | None = None


def get_performance_config() -> PerformanceConfig:
    """
    Get the global performance configuration instance.

    Returns:
        Performance configuration instance
    """
    global _global_config
    if _global_config is None:
        # Try to load from environment first
        try:
            _global_config = PerformanceConfig.from_environment()
        except Exception as e:
            logger.warning(f"Failed to load config from environment: {e}")
            _global_config = PerformanceConfig.create_default()

        # Validate configuration
        if not _global_config.validate():
            logger.error("Configuration validation failed, using default")
            _global_config = PerformanceConfig.create_default()

    return _global_config


def reset_performance_config():
    """Reset the global configuration instance (mainly for testing)."""
    global _global_config
    _global_config = None
