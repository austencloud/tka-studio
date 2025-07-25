"""
Integration Test: Letter Determination with Sequence Generator

Tests that letter determination works properly in the context of the sequence
generator tab, ensuring it integrates correctly with the actual program flow.
"""

import sys
from dataclasses import replace
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestLetterDeterminationIntegration:
    """Test letter determination integration with sequence generation."""

    def test_letter_determination_service_resolution(self):
        """Test that letter determination service can be resolved from DI container."""
        from core.dependency_injection.di_container import DIContainer
        from core.dependency_injection.letter_determination_service_registration import (
            register_letter_determination_services,
        )
        from core.interfaces.letter_determination.letter_determination_services import (
            ILetterDeterminationService,
        )

        # Setup container with all dependencies
        container = DIContainer()

        # Register required dependencies
        from application.services.data.dataset_query import DatasetQuery
        from application.services.pictograph.pictograph_csv_manager import (
            PictographCSVManager,
        )

        container.register_singleton(PictographCSVManager, PictographCSVManager)
        container.register_singleton(DatasetQuery, DatasetQuery)

        # Register letter determination services
        register_letter_determination_services(container)

        # Test service resolution
        letter_service = container.resolve(ILetterDeterminationService)
        assert letter_service is not None
        assert hasattr(letter_service, "determine_letter")

    def test_pictograph_data_with_letter_fields(self):
        """Test that PictographData properly supports letter determination fields."""
        from domain.models import (
            GridData,
            Location,
            MotionData,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.enums import (
            Direction,
            GridPosition,
            Letter,
            LetterType,
            Timing,
        )
        from domain.models.pictograph_data import PictographData

        # Create a PictographData with letter determination fields
        pictograph = PictographData(
            grid_data=GridData(),
            motions={
                "blue": MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                ),
                "red": MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                ),
            },
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.ALPHA3,
            # Letter determination fields
            beat=1,
            letter=Letter.A.value,
            timing=Timing.SPLIT,
            direction=Direction.SAME,
            duration=1,
            letter_type=LetterType.TYPE1,
        )

        # Verify all fields are accessible
        assert pictograph.beat == 1
        assert pictograph.letter == Letter.A.value
        assert pictograph.timing == Timing.SPLIT
        assert pictograph.direction == Direction.SAME
        assert pictograph.duration == 1
        assert pictograph.letter_type == LetterType.TYPE1

        # Verify motions are accessible
        assert pictograph.motions["blue"].motion_type == MotionType.PRO
        assert pictograph.motions["red"].motion_type == MotionType.PRO

    def test_motion_data_with_prefloat_fields(self):
        """Test that MotionData properly supports prefloat fields."""
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion_data import MotionData

        # Create MotionData with prefloat fields
        motion = MotionData(
            motion_type=MotionType.FLOAT,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
            # Prefloat fields for letter determination
            prefloat_motion_type=MotionType.PRO,
            prefloat_prop_rot_dir=RotationDirection.CLOCKWISE,
        )

        # Verify prefloat fields are accessible
        assert motion.prefloat_motion_type == MotionType.PRO
        assert motion.prefloat_prop_rot_dir == RotationDirection.CLOCKWISE

        # Verify regular fields still work
        assert motion.motion_type == MotionType.FLOAT
        assert motion.prop_rot_dir == RotationDirection.NO_ROTATION

    def test_end_to_end_letter_determination(self):
        """Test complete end-to-end letter determination flow."""
        from core.dependency_injection.di_container import DIContainer
        from core.dependency_injection.letter_determination_service_registration import (
            register_letter_determination_services,
        )
        from core.interfaces.letter_determination.letter_determination_services import (
            ILetterDeterminationService,
        )
        from domain.models import (
            GridData,
            Location,
            MotionData,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.enums import GridPosition, Letter
        from domain.models.pictograph_data import PictographData

        # Setup container
        container = DIContainer()

        # Register dependencies
        from application.services.data.dataset_query import DatasetQuery
        from application.services.pictograph.pictograph_csv_manager import (
            PictographCSVManager,
        )

        container.register_singleton(PictographCSVManager, PictographCSVManager)
        container.register_singleton(DatasetQuery, DatasetQuery)

        # Register letter determination services
        register_letter_determination_services(container)

        # Get service
        letter_service = container.resolve(ILetterDeterminationService)

        # Create test pictograph (dual float - should match dual float strategy)
        test_pictograph = PictographData(
            grid_data=GridData(),
            motions={
                "blue": MotionData(
                    motion_type=MotionType.FLOAT,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                    prefloat_motion_type=MotionType.PRO,
                    prefloat_prop_rot_dir=RotationDirection.CLOCKWISE,
                ),
                "red": MotionData(
                    motion_type=MotionType.FLOAT,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                    prefloat_motion_type=MotionType.PRO,
                    prefloat_prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
                ),
            },
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.ALPHA3,
            beat=1,
            timing="split",
            direction="same",
        )

        # Test letter determination
        result = letter_service.determine_letter(test_pictograph)

        # Verify result structure
        assert result is not None
        assert hasattr(result, "is_successful")
        assert hasattr(result, "letter")
        assert hasattr(result, "confidence")
        assert hasattr(result, "strategy_used")

        # The result should be valid (even if no exact match found)
        assert isinstance(result.is_successful, bool)

        # If successful, should have a letter
        if result.is_successful:
            assert result.letter is not None
            assert result.confidence > 0.0
            assert result.strategy_used is not None

    def test_strategy_application(self):
        """Test that strategies apply correctly to different motion types."""
        from application.services.letter_determination.strategies.dual_float_strategy import (
            DualFloatStrategy,
        )
        from application.services.letter_determination.strategies.non_hybrid_shift_strategy import (
            NonHybridShiftStrategy,
        )
        from domain.models import (
            GridData,
            Location,
            MotionData,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.enums import GridPosition
        from domain.models.pictograph_data import PictographData

        # Mock comparison service
        class MockComparisonService:
            def compare_motions(self, motion1, motion2, context=None):
                return 0.8

        mock_service = MockComparisonService()

        # Test dual float strategy
        dual_float_strategy = DualFloatStrategy(mock_service)

        # Create dual float pictograph
        dual_float_pictograph = PictographData(
            grid_data=GridData(),
            motions={
                "blue": MotionData(
                    motion_type=MotionType.FLOAT,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                ),
                "red": MotionData(
                    motion_type=MotionType.FLOAT,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                ),
            },
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.ALPHA3,
        )

        # Test strategy application
        assert dual_float_strategy.applies_to(dual_float_pictograph) == True
        assert dual_float_strategy.get_strategy_name() == "dual_float"

        # Test non-hybrid shift strategy
        non_hybrid_strategy = NonHybridShiftStrategy(mock_service)

        # Create hybrid pictograph (one float, one shift)
        hybrid_pictograph = PictographData(
            grid_data=GridData(),
            motions={
                "blue": MotionData(
                    motion_type=MotionType.FLOAT,
                    prop_rot_dir=RotationDirection.NO_ROTATION,
                    start_loc=Location.NORTH,
                    end_loc=Location.SOUTH,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                ),
                "red": MotionData(
                    motion_type=MotionType.PRO,
                    prop_rot_dir=RotationDirection.CLOCKWISE,
                    start_loc=Location.EAST,
                    end_loc=Location.WEST,
                    start_ori=Orientation.IN,
                    end_ori=Orientation.OUT,
                ),
            },
            start_position=GridPosition.ALPHA1,
            end_position=GridPosition.ALPHA3,
        )

        # Test strategy application
        assert non_hybrid_strategy.applies_to(hybrid_pictograph) == True
        assert non_hybrid_strategy.get_strategy_name() == "non_hybrid_shift"

        # Dual float strategy should not apply to hybrid
        assert dual_float_strategy.applies_to(hybrid_pictograph) == False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
