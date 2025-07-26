"""
Tests for DataCacheManager interface compliance and functionality.

These tests verify that the DataCacheManager correctly implements the
IDataCacheManager interface and provides expected caching behavior.
"""

import pytest
from unittest.mock import Mock

from shared.application.services.data.cache_manager import DataCacheManager
from desktop.modern.core.interfaces.data_services import IDataCacheManager


class TestDataCacheManagerInterface:
    """Test interface compliance for DataCacheManager."""

    def test_data_cache_manager_implements_interface(self):
        """Test that DataCacheManager implements IDataCacheManager."""
        assert issubclass(DataCacheManager, IDataCacheManager)

    def test_all_interface_methods_implemented(self):
        """Test that all interface methods are implemented."""
        service = DataCacheManager()
        
        # Get all abstract methods from interface
        interface_methods = [
            method for method in dir(IDataCacheManager) 
            if not method.startswith('_') and callable(getattr(IDataCacheManager, method))
        ]
        
        # Verify all methods exist and are callable
        for method_name in interface_methods:
            assert hasattr(service, method_name), f"Missing method: {method_name}"
            assert callable(getattr(service, method_name)), f"Method not callable: {method_name}"

    def test_method_signatures_match_interface(self):
        """Test that method signatures match the interface."""
        import inspect
        
        service = DataCacheManager()
        
        # Test key methods
        key_methods = [
            'get_position_cache',
            'set_position_cache',
            'get_sequence_cache',
            'set_sequence_cache',
            'get_pictograph_cache',
            'set_pictograph_cache',
            'clear_all',
            'get_cache_stats'
        ]
        
        for method_name in key_methods:
            interface_method = getattr(IDataCacheManager, method_name)
            implementation_method = getattr(service, method_name)
            
            # Both should be callable
            assert callable(interface_method)
            assert callable(implementation_method)


class TestDataCacheManagerBehavior:
    """Test behavior of DataCacheManager."""

    def setup_method(self):
        """Set up test fixtures."""
        self.service = DataCacheManager(max_size=5)  # Small size for testing

    def test_initial_cache_is_empty(self):
        """Test that initial cache is empty."""
        stats = self.service.get_cache_stats()
        
        assert stats['position_cache_size'] == 0
        assert stats['sequence_cache_size'] == 0
        assert stats['pictograph_cache_size'] == 0
        assert stats['conversion_cache_size'] == 0
        assert stats['total_items'] == 0

    def test_position_cache_operations(self):
        """Test position cache get/set operations."""
        # Initially empty
        assert self.service.get_position_cache('key1') is None
        
        # Set value
        test_value = {'position': 'A'}
        self.service.set_position_cache('key1', test_value)
        
        # Get value
        result = self.service.get_position_cache('key1')
        assert result == test_value
        
        # Check stats
        stats = self.service.get_cache_stats()
        assert stats['position_cache_size'] == 1
        assert 'key1' in stats['position_keys']

    def test_sequence_cache_operations(self):
        """Test sequence cache get/set operations."""
        # Initially empty
        assert self.service.get_sequence_cache('seq1') is None
        
        # Set value
        test_sequence = {'name': 'Test Sequence', 'length': 10}
        self.service.set_sequence_cache('seq1', test_sequence)
        
        # Get value
        result = self.service.get_sequence_cache('seq1')
        assert result == test_sequence
        
        # Check stats
        stats = self.service.get_cache_stats()
        assert stats['sequence_cache_size'] == 1
        assert 'seq1' in stats['sequence_keys']

    def test_pictograph_cache_operations(self):
        """Test pictograph cache get/set operations."""
        # Initially empty
        assert self.service.get_pictograph_cache('pic1') is None
        
        # Set value
        test_pictograph = {'letter': 'A', 'grid_mode': 'diamond'}
        self.service.set_pictograph_cache('pic1', test_pictograph)
        
        # Get value
        result = self.service.get_pictograph_cache('pic1')
        assert result == test_pictograph
        
        # Check stats
        stats = self.service.get_cache_stats()
        assert stats['pictograph_cache_size'] == 1
        assert 'pic1' in stats['pictograph_keys']

    def test_conversion_cache_operations(self):
        """Test conversion cache get/set operations."""
        # Initially empty
        assert self.service.get_conversion_cache('conv1') is None
        
        # Set value
        test_conversion = {'from': 'legacy', 'to': 'modern'}
        self.service.set_conversion_cache('conv1', test_conversion)
        
        # Get value
        result = self.service.get_conversion_cache('conv1')
        assert result == test_conversion
        
        # Check stats
        stats = self.service.get_cache_stats()
        assert stats['conversion_cache_size'] == 1
        assert 'conv1' in stats['conversion_keys']

    def test_lru_eviction(self):
        """Test LRU eviction when cache is full."""
        # Fill cache to max size
        for i in range(6):  # max_size is 5
            self.service.set_position_cache(f'key{i}', f'value{i}')
        
        # Check that cache size is still max_size
        stats = self.service.get_cache_stats()
        assert stats['position_cache_size'] == 5
        
        # First key should have been evicted
        assert self.service.get_position_cache('key0') is None
        
        # Last key should still be there
        assert self.service.get_position_cache('key5') == 'value5'

    def test_lru_access_order(self):
        """Test that accessing items updates LRU order."""
        # Add items
        self.service.set_position_cache('key1', 'value1')
        self.service.set_position_cache('key2', 'value2')
        
        # Access key1 to make it most recently used
        self.service.get_position_cache('key1')
        
        # Fill cache to trigger eviction
        for i in range(3, 7):  # Fill remaining slots
            self.service.set_position_cache(f'key{i}', f'value{i}')
        
        # key1 should still be there (recently accessed)
        assert self.service.get_position_cache('key1') == 'value1'
        
        # key2 should have been evicted (least recently used)
        assert self.service.get_position_cache('key2') is None

    def test_clear_individual_caches(self):
        """Test clearing individual caches."""
        # Add items to all caches
        self.service.set_position_cache('pos1', 'pos_value')
        self.service.set_sequence_cache('seq1', 'seq_value')
        self.service.set_pictograph_cache('pic1', 'pic_value')
        self.service.set_conversion_cache('conv1', 'conv_value')
        
        # Clear position cache
        self.service.clear_position_cache()
        
        # Position cache should be empty
        assert self.service.get_position_cache('pos1') is None
        
        # Other caches should still have data
        assert self.service.get_sequence_cache('seq1') == 'seq_value'
        assert self.service.get_pictograph_cache('pic1') == 'pic_value'
        assert self.service.get_conversion_cache('conv1') == 'conv_value'

    def test_clear_all_caches(self):
        """Test clearing all caches."""
        # Add items to all caches
        self.service.set_position_cache('pos1', 'pos_value')
        self.service.set_sequence_cache('seq1', 'seq_value')
        self.service.set_pictograph_cache('pic1', 'pic_value')
        self.service.set_conversion_cache('conv1', 'conv_value')
        
        # Clear all
        self.service.clear_all()
        
        # All caches should be empty
        assert self.service.get_position_cache('pos1') is None
        assert self.service.get_sequence_cache('seq1') is None
        assert self.service.get_pictograph_cache('pic1') is None
        assert self.service.get_conversion_cache('conv1') is None
        
        # Stats should show empty caches
        stats = self.service.get_cache_stats()
        assert stats['total_items'] == 0

    def test_cache_stats_comprehensive(self):
        """Test comprehensive cache statistics."""
        # Add various items
        self.service.set_position_cache('pos1', 'pos_value')
        self.service.set_position_cache('pos2', 'pos_value2')
        self.service.set_sequence_cache('seq1', 'seq_value')
        self.service.set_pictograph_cache('pic1', 'pic_value')
        
        stats = self.service.get_cache_stats()
        
        # Check all required fields
        assert stats['position_cache_size'] == 2
        assert stats['sequence_cache_size'] == 1
        assert stats['pictograph_cache_size'] == 1
        assert stats['conversion_cache_size'] == 0
        assert stats['total_items'] == 4
        assert stats['max_size_per_cache'] == 5
        
        # Check keys are listed
        assert 'pos1' in stats['position_keys']
        assert 'pos2' in stats['position_keys']
        assert 'seq1' in stats['sequence_keys']
        assert 'pic1' in stats['pictograph_keys']

    def test_cache_with_none_values(self):
        """Test caching None values."""
        # Set None value
        self.service.set_position_cache('null_key', None)
        
        # Should be able to retrieve None
        result = self.service.get_position_cache('null_key')
        assert result is None
        
        # Should be in cache (different from missing key)
        stats = self.service.get_cache_stats()
        assert stats['position_cache_size'] == 1
        assert 'null_key' in stats['position_keys']

    def test_cache_with_complex_objects(self):
        """Test caching complex objects."""
        # Complex object
        complex_obj = {
            'nested': {
                'list': [1, 2, 3],
                'dict': {'a': 1, 'b': 2}
            },
            'function': lambda x: x * 2
        }
        
        self.service.set_position_cache('complex', complex_obj)
        
        # Should retrieve the same object
        result = self.service.get_position_cache('complex')
        assert result == complex_obj
        assert result['nested']['list'] == [1, 2, 3]


class MockDataCacheManager(IDataCacheManager):
    """Mock implementation for testing interface compliance."""
    
    def __init__(self):
        self.caches = {
            'position': {},
            'sequence': {},
            'pictograph': {},
            'conversion': {}
        }
    
    def get_position_cache(self, key):
        return self.caches['position'].get(key)
    
    def set_position_cache(self, key, value):
        self.caches['position'][key] = value
    
    def get_sequence_cache(self, key):
        return self.caches['sequence'].get(key)
    
    def set_sequence_cache(self, key, value):
        self.caches['sequence'][key] = value
    
    def get_pictograph_cache(self, key):
        return self.caches['pictograph'].get(key)
    
    def set_pictograph_cache(self, key, value):
        self.caches['pictograph'][key] = value
    
    def get_conversion_cache(self, key):
        return self.caches['conversion'].get(key)
    
    def set_conversion_cache(self, key, value):
        self.caches['conversion'][key] = value
    
    def clear_all(self):
        for cache in self.caches.values():
            cache.clear()
    
    def clear_position_cache(self):
        self.caches['position'].clear()
    
    def clear_sequence_cache(self):
        self.caches['sequence'].clear()
    
    def clear_pictograph_cache(self):
        self.caches['pictograph'].clear()
    
    def clear_conversion_cache(self):
        self.caches['conversion'].clear()
    
    def get_cache_stats(self):
        return {
            'position_cache_size': len(self.caches['position']),
            'sequence_cache_size': len(self.caches['sequence']),
            'pictograph_cache_size': len(self.caches['pictograph']),
            'conversion_cache_size': len(self.caches['conversion']),
            'total_items': sum(len(cache) for cache in self.caches.values()),
            'max_size_per_cache': 100,
            'position_keys': list(self.caches['position'].keys()),
            'sequence_keys': list(self.caches['sequence'].keys()),
            'pictograph_keys': list(self.caches['pictograph'].keys()),
            'conversion_keys': list(self.caches['conversion'].keys())
        }


class TestMockDataCacheManager:
    """Test mock implementation."""

    def test_mock_implements_interface(self):
        """Test that mock implements interface."""
        mock_service = MockDataCacheManager()
        assert isinstance(mock_service, IDataCacheManager)

    def test_mock_basic_functionality(self):
        """Test basic mock functionality."""
        mock_service = MockDataCacheManager()
        
        # Initially empty
        assert mock_service.get_position_cache('key1') is None
        
        # Set and get
        mock_service.set_position_cache('key1', 'value1')
        assert mock_service.get_position_cache('key1') == 'value1'
        
        # Stats
        stats = mock_service.get_cache_stats()
        assert stats['position_cache_size'] == 1
        assert stats['total_items'] == 1

    def test_mock_clear_functionality(self):
        """Test mock clear functionality."""
        mock_service = MockDataCacheManager()
        
        # Add some data
        mock_service.set_position_cache('key1', 'value1')
        mock_service.set_sequence_cache('key2', 'value2')
        
        # Clear all
        mock_service.clear_all()
        
        # Should be empty
        assert mock_service.get_position_cache('key1') is None
        assert mock_service.get_sequence_cache('key2') is None
        
        stats = mock_service.get_cache_stats()
        assert stats['total_items'] == 0
