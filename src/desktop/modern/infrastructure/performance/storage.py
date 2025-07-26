"""
Performance Data Storage

Provides persistent storage for performance metrics, session data,
and historical performance information. Uses SQLite for local storage
with proper schema management and data retention policies.
"""

import json
import logging
import sqlite3
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

# Result pattern removed - using simple exceptions
from core.performance.config import PerformanceConfig, get_performance_config
from core.performance.profiler import ProfilerSession

logger = logging.getLogger(__name__)


class PerformanceStorage:
    """
    Performance data storage with SQLite backend.

    Features:
    - Session data persistence
    - Function metrics storage
    - System metrics tracking
    - Data retention management
    - Thread-safe operations
    """

    def __init__(self, config: Optional[PerformanceConfig] = None):
        self.config = config or get_performance_config()
        self._lock = threading.RLock()

        # Database setup
        if self.config.storage.database_path == ":memory:":
            self.db_path = ":memory:"
        else:
            self.db_path = Path(self.config.storage.database_path)
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database
        self._init_database()

    def _init_database(self):
        """Initialize SQLite database with proper schema."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("PRAGMA foreign_keys = ON")

                # Sessions table
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        start_time TIMESTAMP NOT NULL,
                        end_time TIMESTAMP,
                        metadata TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """
                )

                # Function metrics table
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS function_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        function_name TEXT NOT NULL,
                        call_count INTEGER NOT NULL,
                        total_time REAL NOT NULL,
                        avg_time REAL NOT NULL,
                        min_time REAL NOT NULL,
                        max_time REAL NOT NULL,
                        memory_total REAL NOT NULL,
                        memory_avg REAL NOT NULL,
                        cache_hits INTEGER DEFAULT 0,
                        cache_misses INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                """
                )

                # System metrics table
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS system_metrics (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT,
                        timestamp TIMESTAMP NOT NULL,
                        cpu_percent REAL NOT NULL,
                        memory_mb REAL NOT NULL,
                        memory_percent REAL NOT NULL,
                        thread_count INTEGER DEFAULT 0,
                        open_files INTEGER DEFAULT 0,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                    )
                """
                )

                # Performance baselines table
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS performance_baselines (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        function_name TEXT NOT NULL UNIQUE,
                        baseline_time REAL NOT NULL,
                        baseline_memory REAL NOT NULL,
                        established_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        sample_count INTEGER DEFAULT 1
                    )
                """
                )

                # Create indexes for better query performance
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_function_metrics_session ON function_metrics(session_id)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_function_metrics_name ON function_metrics(function_name)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_system_metrics_session ON system_metrics(session_id)"
                )
                conn.execute(
                    "CREATE INDEX IF NOT EXISTS idx_system_metrics_timestamp ON system_metrics(timestamp)"
                )

                conn.commit()
                logger.info("Performance database initialized successfully")

        except Exception as e:
            logger.error(f"Failed to initialize performance database: {e}")
            raise

    def save_session(self, session: ProfilerSession) -> Result[bool, AppError]:
        """
        Save a profiling session to the database.

        Args:
            session: ProfilerSession to save

        Returns:
            Result indicating success or failure
        """
        try:
            with self._lock:
                with sqlite3.connect(self.db_path) as conn:
                    # Save session metadata
                    conn.execute(
                        "INSERT OR REPLACE INTO sessions (session_id, start_time, end_time, metadata) VALUES (?, ?, ?, ?)",
                        (
                            session.session_id,
                            session.start_time,
                            session.end_time,
                            json.dumps(session.metadata),
                        ),
                    )

                    # Save function metrics
                    for func_name, metrics in session.function_metrics.items():
                        conn.execute(
                            """INSERT INTO function_metrics
                               (session_id, function_name, call_count, total_time, avg_time, min_time, max_time, 
                                memory_total, memory_avg, cache_hits, cache_misses)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (
                                session.session_id,
                                func_name,
                                metrics.call_count,
                                metrics.total_time,
                                metrics.avg_time,
                                metrics.min_time,
                                metrics.max_time,
                                metrics.memory_total,
                                metrics.memory_avg,
                                metrics.cache_hits,
                                metrics.cache_misses,
                            ),
                        )

                    # Save system metrics
                    for metric in session.system_metrics:
                        conn.execute(
                            """INSERT INTO system_metrics
                               (session_id, timestamp, cpu_percent, memory_mb, memory_percent, thread_count, open_files)
                               VALUES (?, ?, ?, ?, ?, ?, ?)""",
                            (
                                session.session_id,
                                metric.timestamp,
                                metric.cpu_percent,
                                metric.memory_mb,
                                metric.memory_percent,
                                metric.thread_count,
                                metric.open_files,
                            ),
                        )

                    conn.commit()

            logger.info(f"Saved session {session.session_id} to database")
            return success(True)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.STORAGE_ERROR,
                    f"Failed to save session {session.session_id}: {e}",
                    cause=e,
                )
            )

    def get_session(
        self, session_id: str
    ) -> Result[Optional[Dict[str, Any]], AppError]:
        """
        Retrieve a session from the database.

        Args:
            session_id: ID of the session to retrieve

        Returns:
            Result containing session data or None if not found
        """
        try:
            with self._lock:
                with sqlite3.connect(self.db_path) as conn:
                    conn.row_factory = sqlite3.Row

                    # Get session metadata
                    session_row = conn.execute(
                        "SELECT * FROM sessions WHERE session_id = ?", (session_id,)
                    ).fetchone()

                    if not session_row:
                        return success(None)

                    # Get function metrics
                    function_metrics = conn.execute(
                        "SELECT * FROM function_metrics WHERE session_id = ?",
                        (session_id,),
                    ).fetchall()

                    # Get system metrics
                    system_metrics = conn.execute(
                        "SELECT * FROM system_metrics WHERE session_id = ? ORDER BY timestamp",
                        (session_id,),
                    ).fetchall()

                    session_data = {
                        "session_id": session_row["session_id"],
                        "start_time": session_row["start_time"],
                        "end_time": session_row["end_time"],
                        "metadata": (
                            json.loads(session_row["metadata"])
                            if session_row["metadata"]
                            else {}
                        ),
                        "function_metrics": [dict(row) for row in function_metrics],
                        "system_metrics": [dict(row) for row in system_metrics],
                    }

                    return success(session_data)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.STORAGE_ERROR,
                    f"Failed to retrieve session {session_id}: {e}",
                    cause=e,
                )
            )

    def get_recent_sessions(
        self, limit: int = 10
    ) -> Result[List[Dict[str, Any]], AppError]:
        """
        Get recent profiling sessions.

        Args:
            limit: Maximum number of sessions to return

        Returns:
            Result containing list of recent sessions
        """
        try:
            with self._lock:
                with sqlite3.connect(self.db_path) as conn:
                    conn.row_factory = sqlite3.Row

                    rows = conn.execute(
                        "SELECT * FROM sessions ORDER BY start_time DESC LIMIT ?",
                        (limit,),
                    ).fetchall()

                    sessions = []
                    for row in rows:
                        sessions.append(
                            {
                                "session_id": row["session_id"],
                                "start_time": row["start_time"],
                                "end_time": row["end_time"],
                                "metadata": (
                                    json.loads(row["metadata"])
                                    if row["metadata"]
                                    else {}
                                ),
                            }
                        )

                    return success(sessions)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.STORAGE_ERROR,
                    f"Failed to retrieve recent sessions: {e}",
                    cause=e,
                )
            )

    def get_function_performance_history(
        self, function_name: str, days: int = 7
    ) -> Result[List[Dict[str, Any]], AppError]:
        """
        Get performance history for a specific function.

        Args:
            function_name: Name of the function
            days: Number of days of history to retrieve

        Returns:
            Result containing function performance history
        """
        try:
            cutoff_date = datetime.now() - timedelta(days=days)

            with self._lock:
                with sqlite3.connect(self.db_path) as conn:
                    conn.row_factory = sqlite3.Row

                    rows = conn.execute(
                        """SELECT fm.*, s.start_time 
                           FROM function_metrics fm
                           JOIN sessions s ON fm.session_id = s.session_id
                           WHERE fm.function_name = ? AND s.start_time >= ?
                           ORDER BY s.start_time""",
                        (function_name, cutoff_date),
                    ).fetchall()

                    history = [dict(row) for row in rows]
                    return success(history)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.STORAGE_ERROR,
                    f"Failed to retrieve function history for {function_name}: {e}",
                    cause=e,
                )
            )

    def cleanup_old_data(self) -> Result[int, AppError]:
        """
        Clean up old performance data based on retention policy.

        Returns:
            Result containing number of records deleted
        """
        try:
            cutoff_date = datetime.now() - timedelta(
                days=self.config.storage.retention_days
            )

            with self._lock:
                with sqlite3.connect(self.db_path) as conn:
                    # Delete old sessions and related data (cascading)
                    cursor = conn.execute(
                        "DELETE FROM sessions WHERE start_time < ?", (cutoff_date,)
                    )
                    deleted_count = cursor.rowcount

                    # Clean up orphaned records
                    conn.execute(
                        "DELETE FROM function_metrics WHERE session_id NOT IN (SELECT session_id FROM sessions)"
                    )
                    conn.execute(
                        "DELETE FROM system_metrics WHERE session_id NOT IN (SELECT session_id FROM sessions)"
                    )

                    conn.commit()

            logger.info(f"Cleaned up {deleted_count} old performance records")
            return success(deleted_count)

        except Exception as e:
            return failure(
                app_error(
                    ErrorType.STORAGE_ERROR, f"Failed to cleanup old data: {e}", cause=e
                )
            )


# Global storage instance
_global_storage: Optional[PerformanceStorage] = None


def get_performance_storage() -> PerformanceStorage:
    """Get the global performance storage instance."""
    global _global_storage
    if _global_storage is None:
        _global_storage = PerformanceStorage()
    return _global_storage


def reset_performance_storage():
    """Reset the global storage instance (mainly for testing)."""
    global _global_storage
    _global_storage = None
