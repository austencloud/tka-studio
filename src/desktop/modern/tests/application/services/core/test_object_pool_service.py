"""
Tests for Object Pool Service

This module tests the extracted object pool business logic service
to ensure it correctly handles object pool management and lifecycle.
"""

import pytest
from unittest.mock import Mock

from application.services.core.object_pool_service import ObjectPoolService


class TestObjectPoolService:
    """Test cases for ObjectPoolService."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = ObjectPoolService()

    def test_initialization(self):
        """Test service initialization."""
        assert self.service is not None
        assert hasattr(self.service, '_pools')
        assert hasattr(self.service, '_pool_states')
        assert len(self.service._pools) == 0
        assert len(self.service._pool_states) == 0

    def test_initialize_pool_success(self):
        """Test successful pool initialization."""
        mock_objects = ["obj1", "obj2", "obj3"]
        object_index = 0
        
        def mock_factory():
            nonlocal object_index
            if object_index < len(mock_objects):
                obj = mock_objects[object_index]
                object_index += 1
                return obj
            return None
        
        progress_calls = []
        def progress_callback(message, progress):
            progress_calls.append((message, progress))
        
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=3,
            object_factory=mock_factory,
            progress_callback=progress_callback
        )
        
        # Verify pool was created
        assert "test_pool" in self.service._pools
        assert len(self.service._pools["test_pool"]) == 3
        assert self.service._pools["test_pool"] == mock_objects
        
        # Verify pool state
        state = self.service._pool_states["test_pool"]
        assert state["initialized"] is True
        assert state["max_objects"] == 3
        assert state["created_objects"] == 3
        
        # Verify progress callbacks were called
        assert len(progress_calls) > 0
        assert progress_calls[0][0] == "Starting test_pool pool initialization"
        assert progress_calls[-1][0] == "test_pool pool initialization complete"

    def test_initialize_pool_already_initialized(self):
        """Test initializing a pool that's already initialized."""
        # First initialization
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=2,
            object_factory=lambda: "obj"
        )
        
        original_pool = self.service._pools["test_pool"].copy()
        
        # Second initialization should be skipped
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=5,
            object_factory=lambda: "new_obj"
        )
        
        # Pool should remain unchanged
        assert self.service._pools["test_pool"] == original_pool
        assert len(self.service._pools["test_pool"]) == 2

    def test_initialize_pool_factory_returns_none(self):
        """Test pool initialization when factory returns None."""
        def failing_factory():
            return None
        
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=3,
            object_factory=failing_factory
        )
        
        # Pool should be created but empty
        assert "test_pool" in self.service._pools
        assert len(self.service._pools["test_pool"]) == 0
        assert self.service._pool_states["test_pool"]["created_objects"] == 0

    def test_initialize_pool_factory_raises_exception(self):
        """Test pool initialization when factory raises exceptions."""
        call_count = 0
        def failing_factory():
            nonlocal call_count
            call_count += 1
            if call_count <= 2:
                return f"obj{call_count}"
            raise Exception("Factory failed")
        
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=5,
            object_factory=failing_factory
        )
        
        # Should have created 2 objects before failing
        assert "test_pool" in self.service._pools
        assert len(self.service._pools["test_pool"]) == 2
        assert self.service._pool_states["test_pool"]["created_objects"] == 2

    def test_get_pooled_object_success(self):
        """Test successfully getting an object from the pool."""
        objects = ["obj1", "obj2", "obj3"]
        self.service._pools["test_pool"] = objects
        
        result = self.service.get_pooled_object("test_pool", 1)
        assert result == "obj2"

    def test_get_pooled_object_pool_not_exists(self):
        """Test getting object from non-existent pool."""
        result = self.service.get_pooled_object("nonexistent_pool", 0)
        assert result is None

    def test_get_pooled_object_index_out_of_range(self):
        """Test getting object with index out of range."""
        self.service._pools["test_pool"] = ["obj1", "obj2"]
        
        # Test negative index
        result = self.service.get_pooled_object("test_pool", -1)
        assert result is None
        
        # Test index too large
        result = self.service.get_pooled_object("test_pool", 5)
        assert result is None

    def test_reset_pool_success(self):
        """Test successfully resetting a pool."""
        # Setup pool
        self.service._pools["test_pool"] = ["obj1", "obj2"]
        self.service._pool_states["test_pool"] = {
            "initialized": True,
            "max_objects": 2,
            "created_objects": 2
        }
        
        self.service.reset_pool("test_pool")
        
        # Verify pool was reset
        assert len(self.service._pools["test_pool"]) == 0
        assert self.service._pool_states["test_pool"]["initialized"] is False
        assert self.service._pool_states["test_pool"]["created_objects"] == 0

    def test_reset_pool_nonexistent(self):
        """Test resetting a non-existent pool."""
        # Should not raise an exception
        self.service.reset_pool("nonexistent_pool")

    def test_get_pool_info_existing_pool(self):
        """Test getting info for an existing pool."""
        self.service._pools["test_pool"] = ["obj1", "obj2"]
        self.service._pool_states["test_pool"] = {
            "initialized": True,
            "max_objects": 3,
            "created_objects": 2
        }
        
        info = self.service.get_pool_info("test_pool")
        
        assert info["exists"] is True
        assert info["initialized"] is True
        assert info["size"] == 2
        assert info["max_objects"] == 3
        assert info["created_objects"] == 2

    def test_get_pool_info_nonexistent_pool(self):
        """Test getting info for a non-existent pool."""
        info = self.service.get_pool_info("nonexistent_pool")
        
        assert info["exists"] is False
        assert info["initialized"] is False
        assert info["size"] == 0
        assert info["max_objects"] == 0
        assert info["created_objects"] == 0

    def test_list_pools(self):
        """Test listing all pools."""
        self.service._pools["pool1"] = []
        self.service._pools["pool2"] = []
        
        pools = self.service.list_pools()
        
        assert "pool1" in pools
        assert "pool2" in pools
        assert len(pools) == 2

    def test_list_pools_empty(self):
        """Test listing pools when no pools exist."""
        pools = self.service.list_pools()
        assert pools == []

    def test_cleanup_all_pools(self):
        """Test cleaning up all pools."""
        # Setup multiple pools
        self.service._pools["pool1"] = ["obj1"]
        self.service._pools["pool2"] = ["obj2"]
        self.service._pool_states["pool1"] = {"initialized": True}
        self.service._pool_states["pool2"] = {"initialized": True}
        
        self.service.cleanup_all_pools()
        
        # Verify all pools were cleaned up
        assert len(self.service._pools) == 0
        assert len(self.service._pool_states) == 0

    def test_get_pool_statistics(self):
        """Test getting pool statistics."""
        # Setup pools
        self.service._pools["pool1"] = ["obj1", "obj2"]
        self.service._pool_states["pool1"] = {"initialized": True}
        
        self.service._pools["pool2"] = ["obj3"]
        self.service._pool_states["pool2"] = {"initialized": False}
        
        stats = self.service.get_pool_statistics()
        
        assert stats["total_pools"] == 2
        assert stats["initialized_pools"] == 1
        assert stats["total_objects"] == 3
        assert "pool1" in stats["pools"]
        assert "pool2" in stats["pools"]

    def test_get_pool_statistics_empty(self):
        """Test getting statistics when no pools exist."""
        stats = self.service.get_pool_statistics()
        
        assert stats["total_pools"] == 0
        assert stats["initialized_pools"] == 0
        assert stats["total_objects"] == 0
        assert stats["pools"] == {}

    def test_error_handling_in_initialize_pool(self):
        """Test error handling in initialize_pool method."""
        def failing_factory():
            raise Exception("Critical factory failure")
        
        # Should not raise exception
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=1,
            object_factory=failing_factory
        )
        
        # Pool should exist but be empty
        assert "test_pool" in self.service._pools
        assert len(self.service._pools["test_pool"]) == 0

    def test_error_handling_in_get_pooled_object(self):
        """Test error handling in get_pooled_object method."""
        # Setup pool with problematic data
        self.service._pools["test_pool"] = None  # Invalid pool data
        
        result = self.service.get_pooled_object("test_pool", 0)
        assert result is None

    def test_progress_callback_frequency(self):
        """Test that progress callbacks are called at appropriate intervals."""
        progress_calls = []
        def progress_callback(message, progress):
            progress_calls.append((message, progress))
        
        # Create pool with enough objects to trigger multiple progress updates
        self.service.initialize_pool(
            pool_name="test_pool",
            max_objects=20,
            object_factory=lambda: "obj",
            progress_callback=progress_callback
        )
        
        # Should have multiple progress updates
        assert len(progress_calls) >= 3  # Start, at least one middle, end
        
        # Progress should be between 0 and 1
        for message, progress in progress_calls:
            assert 0.0 <= progress <= 1.0


if __name__ == "__main__":
    pytest.main([__file__])
