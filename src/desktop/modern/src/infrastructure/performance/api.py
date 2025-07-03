"""
Performance API Endpoints

Provides REST API endpoints for accessing performance data.
Integrates with existing FastAPI infrastructure and follows TKA patterns.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import logging

try:
    from fastapi import APIRouter, HTTPException, Query
    from pydantic import BaseModel
    FASTAPI_AVAILABLE = True
except ImportError:
    # Fallback for environments without FastAPI
    FASTAPI_AVAILABLE = False
    class APIRouter:
        """Fallback APIRouter for when FastAPI is not available."""
        def __init__(self, prefix="", tags=None, **kwargs):
            self.prefix = prefix
            self.tags = tags or []
            
        def get(self, path, **kwargs):
            def decorator(func):
                return func
            return decorator
            
        def post(self, path, **kwargs):
            def decorator(func):
                return func
            return decorator
    
    def Query(default=None, **kwargs):
        """Fallback Query for when FastAPI is not available."""
        return default
    
    class HTTPException(Exception):
        """Fallback HTTPException for when FastAPI is not available."""
        def __init__(self, status_code=500, detail="Internal Server Error", **kwargs):
            self.status_code = status_code
            self.detail = detail
            super().__init__(detail)
    BaseModel = object

from core.performance import get_profiler, get_qt_profiler, get_memory_tracker
from .storage import get_performance_storage

logger = logging.getLogger(__name__)


if FASTAPI_AVAILABLE:
    class SessionResponse(BaseModel):
        """Response model for session data."""
        session_id: str
        start_time: datetime
        end_time: Optional[datetime]
        metadata: Dict[str, Any]
        function_count: int
        system_metrics_count: int

    class FunctionMetricsResponse(BaseModel):
        """Response model for function metrics."""
        function_name: str
        call_count: int
        total_time: float
        avg_time: float
        min_time: float
        max_time: float
        memory_total: float
        memory_avg: float
        efficiency_score: float

    class PerformanceSummaryResponse(BaseModel):
        """Response model for performance summary."""
        total_functions: int
        active_sessions: int
        top_bottlenecks: List[Dict[str, Any]]
        memory_usage: Dict[str, Any]
        qt_performance: Dict[str, Any]
        recommendations: List[Dict[str, str]]


class PerformanceAPI:
    """
    Performance API providing REST endpoints for performance data access.
    
    Features:
    - Session management endpoints
    - Real-time performance metrics
    - Historical data access
    - Performance summaries and reports
    """

    def __init__(self):
        self.storage = get_performance_storage()
        self.profiler = get_profiler()
        self.qt_profiler = get_qt_profiler()
        self.memory_tracker = get_memory_tracker()
         
        if FASTAPI_AVAILABLE:
            self.router = APIRouter(prefix="/api/performance", tags=["performance"])
            self._setup_routes()
        else:
            logger.warning("FastAPI not available - Performance API disabled")

    def _setup_routes(self):
        """Setup API routes."""
        if not FASTAPI_AVAILABLE:
            return

        @self.router.get("/status")
        async def get_status():
            """Get performance monitoring status."""
            return {
                "profiling_active": self.profiler.is_profiling,
                "qt_profiling_active": self.qt_profiler.is_profiling if hasattr(self.qt_profiler, 'is_profiling') else False,
                "memory_tracking_active": self.memory_tracker.is_tracking if hasattr(self.memory_tracker, 'is_tracking') else False,
                "timestamp": datetime.now().isoformat()
            }

        @self.router.post("/sessions/start")
        async def start_session(session_name: Optional[str] = None):
            """Start a new profiling session."""
            result = self.profiler.start_session(session_name)
            if result.is_failure():
                raise HTTPException(status_code=400, detail=str(result.error))
            
            return {"session_id": result.value, "status": "started"}

        @self.router.post("/sessions/{session_id}/stop")
        async def stop_session(session_id: str):
            """Stop a profiling session."""
            result = self.profiler.stop_session()
            if result.is_failure():
                raise HTTPException(status_code=400, detail=str(result.error))
            
            session = result.value
            if session and session.session_id == session_id:
                # Save session to storage
                save_result = self.storage.save_session(session)
                if save_result.is_failure():
                    logger.warning(f"Failed to save session: {save_result.error}")
                
                return {"session_id": session_id, "status": "stopped", "saved": save_result.is_success()}
            
            return {"session_id": session_id, "status": "not_found"}

        @self.router.get("/sessions", response_model=List[SessionResponse] if FASTAPI_AVAILABLE else List)
        async def get_sessions(limit: int = Query(10, ge=1, le=100)):
            """Get recent profiling sessions."""
            result = self.storage.get_recent_sessions(limit)
            if result.is_failure():
                raise HTTPException(status_code=500, detail=str(result.error))
            
            sessions = []
            for session_data in result.value:
                sessions.append(SessionResponse(
                    session_id=session_data["session_id"],
                    start_time=datetime.fromisoformat(session_data["start_time"]),
                    end_time=datetime.fromisoformat(session_data["end_time"]) if session_data["end_time"] else None,
                    metadata=session_data["metadata"],
                    function_count=len(session_data.get("function_metrics", [])),
                    system_metrics_count=len(session_data.get("system_metrics", []))
                ))
            
            return sessions

        @self.router.get("/sessions/{session_id}")
        async def get_session(session_id: str):
            """Get detailed session data."""
            result = self.storage.get_session(session_id)
            if result.is_failure():
                raise HTTPException(status_code=500, detail=str(result.error))
            
            if result.value is None:
                raise HTTPException(status_code=404, detail="Session not found")
            
            return result.value

        @self.router.get("/summary", response_model=PerformanceSummaryResponse if FASTAPI_AVAILABLE else Dict)
        async def get_performance_summary():
            """Get comprehensive performance summary."""
            try:
                # Get current profiler summary
                profiler_summary = self.profiler.get_performance_summary()
                
                # Get Qt performance data
                qt_summary = {}
                if hasattr(self.qt_profiler, 'get_qt_performance_summary'):
                    qt_summary = self.qt_profiler.get_qt_performance_summary()
                
                # Get memory data
                memory_summary = {}
                if hasattr(self.memory_tracker, 'get_memory_summary'):
                    memory_summary = self.memory_tracker.get_memory_summary()
                
                summary = {
                    "total_functions": len(self.profiler._function_stats),
                    "active_sessions": 1 if self.profiler.is_profiling else 0,
                    "top_bottlenecks": self._format_bottlenecks(self.profiler.get_top_bottlenecks(5)),
                    "memory_usage": memory_summary,
                    "qt_performance": qt_summary,
                    "recommendations": self._generate_recommendations()
                }
                
                if FASTAPI_AVAILABLE:
                    return PerformanceSummaryResponse(**summary)
                else:
                    return summary
                    
            except Exception as e:
                logger.error(f"Failed to generate performance summary: {e}")
                raise HTTPException(status_code=500, detail=str(e))

        @self.router.get("/functions/{function_name}/history")
        async def get_function_history(
            function_name: str, 
            days: int = Query(7, ge=1, le=30)
        ):
            """Get performance history for a specific function."""
            result = self.storage.get_function_performance_history(function_name, days)
            if result.is_failure():
                raise HTTPException(status_code=500, detail=str(result.error))
            
            return {"function_name": function_name, "history": result.value}

        @self.router.post("/cleanup")
        async def cleanup_old_data():
            """Clean up old performance data."""
            result = self.storage.cleanup_old_data()
            if result.is_failure():
                raise HTTPException(status_code=500, detail=str(result.error))
            
            return {"deleted_records": result.value}

        @self.router.get("/metrics/live")
        async def get_live_metrics():
            """Get live performance metrics."""
            try:
                current_memory = self.memory_tracker.get_current_usage()
                
                return {
                    "timestamp": datetime.now().isoformat(),
                    "memory_mb": current_memory,
                    "profiling_active": self.profiler.is_profiling,
                    "function_count": len(self.profiler._function_stats),
                    "qt_events": len(self.qt_profiler.event_metrics) if hasattr(self.qt_profiler, 'event_metrics') else 0
                }
            except Exception as e:
                logger.error(f"Failed to get live metrics: {e}")
                raise HTTPException(status_code=500, detail=str(e))

    def _format_bottlenecks(self, bottlenecks) -> List[Dict[str, Any]]:
        """Format bottleneck data for API response."""
        formatted = []
        for bottleneck in bottlenecks:
            formatted.append({
                "function": bottleneck.name,
                "total_time": bottleneck.total_time,
                "avg_time": bottleneck.avg_time,
                "call_count": bottleneck.call_count,
                "efficiency_score": bottleneck.efficiency_score
            })
        return formatted

    def _generate_recommendations(self) -> List[Dict[str, str]]:
        """Generate performance recommendations."""
        recommendations = []
        
        # Get recommendations from profiler
        try:
            profiler_summary = self.profiler.get_performance_summary()
            if "optimization_recommendations" in profiler_summary:
                recommendations.extend(profiler_summary["optimization_recommendations"])
        except Exception as e:
            logger.warning(f"Failed to get profiler recommendations: {e}")
        
        # Get Qt recommendations
        try:
            if hasattr(self.qt_profiler, '_generate_qt_recommendations'):
                qt_recommendations = self.qt_profiler._generate_qt_recommendations()
                recommendations.extend(qt_recommendations)
        except Exception as e:
            logger.warning(f"Failed to get Qt recommendations: {e}")
        
        # Get memory recommendations
        try:
            if hasattr(self.memory_tracker, '_generate_memory_recommendations'):
                memory_recommendations = self.memory_tracker._generate_memory_recommendations()
                recommendations.extend(memory_recommendations)
        except Exception as e:
            logger.warning(f"Failed to get memory recommendations: {e}")
        
        return recommendations

    def get_router(self):
        """Get the FastAPI router for integration."""
        if FASTAPI_AVAILABLE:
            return self.router
        else:
            raise RuntimeError("FastAPI not available")


# Global API instance
_global_api: Optional[PerformanceAPI] = None


def get_performance_api() -> PerformanceAPI:
    """Get the global performance API instance."""
    global _global_api
    if _global_api is None:
        _global_api = PerformanceAPI()
    return _global_api


def reset_performance_api():
    """Reset the global API instance (mainly for testing)."""
    global _global_api
    _global_api = None
