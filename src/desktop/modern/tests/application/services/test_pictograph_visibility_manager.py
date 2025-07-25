"""
Tests for PictographVisibilityManager.

Tests the visibility manager that replaces the visibility flags
previously stored in GlyphData.
"""

import pytest
from application.services.pictograph.pictograph_visibility_manager import (
    PictographVisibilityManager,
    PictographVisibilityState,
    get_pictograph_visibility_manager,
    reset_pictograph_visibility_manager,
)
from domain.models.enums import LetterType


class TestPictographVisibilityState:
    """Test PictographVisibilityState functionality."""

    def test_default_state(self):
        """Test default visibility state."""
        state = PictographVisibilityState()
        assert state.show_elemental is True
        assert state.show_vtg is True
        assert state.show_tka is True
        assert state.show_positions is True

    def test_custom_state(self):
        """Test custom visibility state."""
        state = PictographVisibilityState(
            show_elemental=False,
            show_vtg=True,
            show_tka=False,
            show_positions=True,
        )
        assert state.show_elemental is False
        assert state.show_vtg is True
        assert state.show_tka is False
        assert state.show_positions is True

    def test_to_dict(self):
        """Test conversion to dictionary."""
        state = PictographVisibilityState(
            show_elemental=False,
            show_vtg=True,
            show_tka=False,
            show_positions=True,
        )
        data = state.to_dict()
        expected = {
            "show_elemental": False,
            "show_vtg": True,
            "show_tka": False,
            "show_positions": True,
        }
        assert data == expected

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "show_elemental": False,
            "show_vtg": True,
            "show_tka": False,
            "show_positions": True,
        }
        state = PictographVisibilityState.from_dict(data)
        assert state.show_elemental is False
        assert state.show_vtg is True
        assert state.show_tka is False
        assert state.show_positions is True

    def test_from_letter_type_type1(self):
        """Test creation from Type1 letter type."""
        state = PictographVisibilityState.from_letter_type(LetterType.TYPE1)
        assert state.show_elemental is True  # Type1 shows elemental
        assert state.show_vtg is True  # Type1 shows VTG
        assert state.show_tka is True  # Always show TKA
        assert state.show_positions is True  # Type1 shows positions

    def test_from_letter_type_type6(self):
        """Test creation from Type6 letter type."""
        state = PictographVisibilityState.from_letter_type(LetterType.TYPE6)
        assert state.show_elemental is False  # Type6 doesn't show elemental
        assert state.show_vtg is False  # Type6 doesn't show VTG
        assert state.show_tka is True  # Always show TKA
        assert state.show_positions is False  # Type6 doesn't show positions


class TestPictographVisibilityManager:
    """Test PictographVisibilityManager functionality."""

    def setup_method(self):
        """Set up test environment."""
        self.manager = PictographVisibilityManager()

    def test_default_visibility_state(self):
        """Test getting default visibility state."""
        state = self.manager.get_visibility_state("test_id")
        assert isinstance(state, PictographVisibilityState)
        assert state.show_elemental is True
        assert state.show_vtg is True
        assert state.show_tka is True
        assert state.show_positions is True

    def test_set_visibility_state(self):
        """Test setting visibility state."""
        custom_state = PictographVisibilityState(
            show_elemental=False,
            show_vtg=True,
            show_tka=False,
            show_positions=True,
        )
        self.manager.set_visibility_state("test_id", custom_state)
        
        retrieved_state = self.manager.get_visibility_state("test_id")
        assert retrieved_state.show_elemental is False
        assert retrieved_state.show_vtg is True
        assert retrieved_state.show_tka is False
        assert retrieved_state.show_positions is True

    def test_set_pictograph_visibility(self):
        """Test setting individual glyph visibility."""
        self.manager.set_pictograph_visibility("test_id", "elemental", False)
        self.manager.set_pictograph_visibility("test_id", "vtg", True)
        self.manager.set_pictograph_visibility("test_id", "tka", False)
        self.manager.set_pictograph_visibility("test_id", "positions", True)
        
        state = self.manager.get_visibility_state("test_id")
        assert state.show_elemental is False
        assert state.show_vtg is True
        assert state.show_tka is False
        assert state.show_positions is True

    def test_get_pictograph_visibility(self):
        """Test getting individual glyph visibility."""
        self.manager.set_pictograph_visibility("test_id", "elemental", False)
        
        assert self.manager.get_pictograph_visibility("test_id", "elemental") is False
        assert self.manager.get_pictograph_visibility("test_id", "vtg") is True

    def test_global_visibility_override(self):
        """Test global visibility overrides."""
        # Set pictograph-specific visibility to True
        self.manager.set_pictograph_visibility("test_id", "elemental", True)
        
        # Set global visibility to False
        self.manager.set_global_visibility("elemental", False)
        
        # Should return False due to global override
        assert self.manager.get_pictograph_visibility("test_id", "elemental") is False

    def test_initialize_pictograph_visibility(self):
        """Test initializing pictograph visibility from letter type."""
        self.manager.initialize_pictograph_visibility("test_id", LetterType.TYPE6)
        
        state = self.manager.get_visibility_state("test_id")
        assert state.show_elemental is False  # Type6 doesn't show elemental
        assert state.show_vtg is False  # Type6 doesn't show VTG
        assert state.show_tka is True  # Always show TKA
        assert state.show_positions is False  # Type6 doesn't show positions

    def test_remove_pictograph_visibility(self):
        """Test removing pictograph visibility."""
        self.manager.set_pictograph_visibility("test_id", "elemental", False)
        assert self.manager.get_pictograph_visibility("test_id", "elemental") is False
        
        self.manager.remove_pictograph_visibility("test_id")
        # Should return to default state
        assert self.manager.get_pictograph_visibility("test_id", "elemental") is True

    def test_clear_all_visibility(self):
        """Test clearing all visibility states."""
        self.manager.set_pictograph_visibility("test_id1", "elemental", False)
        self.manager.set_pictograph_visibility("test_id2", "vtg", False)
        
        self.manager.clear_all_visibility()
        
        # Should return to default states
        assert self.manager.get_pictograph_visibility("test_id1", "elemental") is True
        assert self.manager.get_pictograph_visibility("test_id2", "vtg") is True

    def test_invalid_glyph_type(self):
        """Test handling of invalid glyph types."""
        with pytest.raises(ValueError, match="Unknown glyph type"):
            self.manager.set_pictograph_visibility("test_id", "invalid", True)
        
        with pytest.raises(ValueError, match="Unknown glyph type"):
            self.manager.get_pictograph_visibility("test_id", "invalid")
        
        with pytest.raises(ValueError, match="Unknown glyph type"):
            self.manager.set_global_visibility("invalid", True)


class TestGlobalVisibilityManager:
    """Test global visibility manager functions."""

    def setup_method(self):
        """Set up test environment."""
        reset_pictograph_visibility_manager()

    def test_singleton_behavior(self):
        """Test that global manager returns same instance."""
        manager1 = get_pictograph_visibility_manager()
        manager2 = get_pictograph_visibility_manager()
        assert manager1 is manager2

    def test_reset_manager(self):
        """Test resetting the global manager."""
        manager1 = get_pictograph_visibility_manager()
        manager1.set_pictograph_visibility("test_id", "elemental", False)
        
        reset_pictograph_visibility_manager()
        manager2 = get_pictograph_visibility_manager()
        
        # Should be a new instance with default state
        assert manager2 is not manager1
        assert manager2.get_pictograph_visibility("test_id", "elemental") is True
