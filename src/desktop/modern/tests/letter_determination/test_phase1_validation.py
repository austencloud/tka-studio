"""
Phase 1: Letter Determination Migration Validation Tests

Tests import compatibility, model extensions, and legacy compatibility
to ensure the foundation is solid before proceeding with implementation.
"""

import sys
from pathlib import Path

import pytest

# Add src to path for imports
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))


class TestImportCompatibility:
    """Test that all imports resolve correctly."""

    def test_extended_motion_data_import(self):
        """Test ExtendedMotionData import."""
        try:
            from domain.models.motion.extended_motion_data import ExtendedMotionData

            assert ExtendedMotionData is not None
        except ImportError as e:
            pytest.fail(f"Failed to import ExtendedMotionData: {e}")

    def test_letter_determination_pictograph_data_import(self):
        """Test LetterDeterminationPictographData import."""
        try:
            from domain.models.motion.letter_determination_pictograph_data import (
                LetterDeterminationPictographData,
            )

            assert LetterDeterminationPictographData is not None
        except ImportError as e:
            pytest.fail(f"Failed to import LetterDeterminationPictographData: {e}")

    def test_letter_determination_service_import(self):
        """Test ILetterDeterminationService import."""
        try:
            from core.interfaces.letter_determination.letter_determination_services import (
                ILetterDeterminationService,
            )

            assert ILetterDeterminationService is not None
        except ImportError as e:
            pytest.fail(f"Failed to import ILetterDeterminationService: {e}")

    def test_core_domain_imports(self):
        """Test core domain model imports."""
        try:
            from domain.models.enums import (
                Location,
                MotionType,
                Orientation,
                RotationDirection,
            )
            from domain.models.motion_data import MotionData

            assert all(
                [MotionData, MotionType, RotationDirection, Location, Orientation]
            )
        except ImportError as e:
            pytest.fail(f"Failed to import core domain models: {e}")


class TestModelExtensions:
    """Test that ExtendedMotionData properly extends MotionData."""

    def test_extended_motion_data_creation(self):
        """Test creating ExtendedMotionData from MotionData."""
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion.extended_motion_data import ExtendedMotionData
        from domain.models.motion_data import MotionData

        # Create base motion
        base_motion = MotionData(
            motion_type=MotionType.FLOAT,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )

        # Create extended motion
        extended_motion = ExtendedMotionData.from_motion_data(
            base_motion,
            prefloat_motion_type=MotionType.PRO,
            prefloat_prop_rot_dir=RotationDirection.COUNTER_CLOCKWISE,
        )

        # Verify properties
        assert extended_motion.is_float == True
        assert extended_motion.effective_motion_type == MotionType.PRO
        assert extended_motion.prefloat_motion_type == MotionType.PRO
        assert (
            extended_motion.prefloat_prop_rot_dir == RotationDirection.COUNTER_CLOCKWISE
        )

        # Verify base properties are preserved
        assert extended_motion.motion_type == MotionType.FLOAT
        assert extended_motion.prop_rot_dir == RotationDirection.CLOCKWISE
        assert extended_motion.start_loc == Location.NORTH
        assert extended_motion.end_loc == Location.SOUTH

    def test_extended_motion_data_properties(self):
        """Test ExtendedMotionData specific properties."""
        from domain.models.enums import (
            Location,
            MotionType,
            Orientation,
            RotationDirection,
        )
        from domain.models.motion.extended_motion_data import ExtendedMotionData
        from domain.models.motion_data import MotionData

        # Test float motion
        float_motion = ExtendedMotionData(
            motion_type=MotionType.FLOAT,
            prop_rot_dir=RotationDirection.NO_ROTATION,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        assert float_motion.is_float == True
        assert float_motion.is_shift == False

        # Test shift motion
        shift_motion = ExtendedMotionData(
            motion_type=MotionType.PRO,
            prop_rot_dir=RotationDirection.CLOCKWISE,
            start_loc=Location.NORTH,
            end_loc=Location.SOUTH,
            start_ori=Orientation.IN,
            end_ori=Orientation.OUT,
        )
        assert shift_motion.is_float == False
        assert shift_motion.is_shift == True


class TestLegacyCompatibility:
    """Test conversion between legacy dict format and new models."""

    def test_legacy_dict_conversion(self):
        """Test conversion from legacy dict to modern model and back."""
        from domain.models.motion.letter_determination_pictograph_data import (
            LetterDeterminationPictographData,
        )

        # Legacy dict format
        legacy_dict = {
            "beat": 1,
            "letter": "A",
            "start_pos": "alpha1",
            "end_pos": "alpha3",
            "timing": "split",
            "direction": "same",
            "blue_attributes": {
                "motion_type": "pro",
                "start_ori": "in",
                "end_ori": "in",
                "start_loc": "s",
                "end_loc": "w",
                "prop_rot_dir": "cw",
                "turns": 0,
            },
            "red_attributes": {
                "motion_type": "pro",
                "start_ori": "in",
                "end_ori": "in",
                "start_loc": "n",
                "end_loc": "e",
                "prop_rot_dir": "cw",
                "turns": 0,
            },
        }

        # Convert to modern model
        try:
            modern_data = LetterDeterminationPictographData.from_legacy_dict(
                legacy_dict
            )
            assert modern_data is not None
            assert modern_data.beat == 1

            # Convert back to legacy format
            converted_back = modern_data.to_legacy_dict()

            # Verify round-trip conversion
            assert converted_back["beat"] == legacy_dict["beat"]
            assert converted_back["letter"] == legacy_dict["letter"]

        except Exception as e:
            pytest.fail(f"Legacy conversion failed: {e}")


class TestPhase2Implementation:
    """Test Phase 2: Complete Missing Implementation."""

    def test_dataset_provider_creation(self):
        """Test that PictographDatasetProvider can be created."""
        try:
            from application.services.letter_determination.pictograph_dataset_provider import (
                PictographDatasetProvider,
            )

            provider = PictographDatasetProvider()
            assert provider is not None
        except Exception as e:
            pytest.fail(f"Failed to create PictographDatasetProvider: {e}")

    def test_service_registration(self):
        """Test that letter determination services can be registered."""
        try:
            from core.dependency_injection.di_container import DIContainer
            from core.dependency_injection.letter_determination_service_registration import (
                register_letter_determination_services,
            )
            from core.interfaces.letter_determination.letter_determination_services import (
                ILetterDeterminationService,
            )

            container = DIContainer()

            # Register required dependencies first
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

        except Exception as e:
            pytest.fail(f"Service registration failed: {e}")

    def test_generation_services_compatibility(self):
        """Test that generation services work with existing models."""
        try:
            from application.services.generation.freeform_generation_service import (
                RotationDeterminer,
            )
            from application.services.generation.turn_intensity_manager import (
                TurnIntensityManager,
            )

            # Test that these can be imported and basic functionality works
            turn_manager = TurnIntensityManager(
                word_length=5, level=2, max_turn_intensity=2.0
            )
            blue_turns, red_turns = turn_manager.allocate_turns_for_blue_and_red()

            assert len(blue_turns) == 5
            assert len(red_turns) == 5

            # Test rotation determiner
            rotation_determiner = RotationDeterminer()
            blue_rot, red_rot = rotation_determiner.get_rotation_dirs("continuous")
            assert (
                blue_rot is not None or red_rot is not None
            )  # Should return some rotation

        except Exception as e:
            pytest.fail(f"Generation services compatibility test failed: {e}")


class TestPhase3Integration:
    """Test Phase 3: Integration Testing."""

    def test_letter_determination_pipeline(self):
        """Test that the complete letter determination works end-to-end."""
        try:
            from core.dependency_injection.di_container import DIContainer
            from core.dependency_injection.letter_determination_service_registration import (
                register_letter_determination_services,
            )
            from core.interfaces.letter_determination.letter_determination_services import (
                ILetterDeterminationService,
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

            # Create test pictograph data (minimal valid data)
            from domain.models import (
                GridData,
                Location,
                MotionData,
                MotionType,
                Orientation,
                RotationDirection,
            )

            test_pictograph = PictographData(
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

            # Set letter determination fields directly on PictographData
            from dataclasses import replace

            from domain.models.enums import Direction, Timing

            letter_data = replace(
                test_pictograph,
                beat=1,
                letter=Letter.A.value,
                timing=Timing.SPLIT,
                direction=Direction.SAME,
            )

            # Test letter determination
            result = letter_service.determine_letter(letter_data)

            # Verify result structure (may not find exact match but should return valid result)
            assert result is not None
            assert hasattr(result, "is_successful")
            assert hasattr(result, "letter")

        except Exception as e:
            pytest.fail(f"Letter determination pipeline test failed: {e}")

    def test_strategy_coverage(self):
        """Test that strategies are available and can be applied."""
        try:
            from application.services.letter_determination.strategies.dual_float_strategy import (
                DualFloatStrategy,
            )
            from application.services.letter_determination.strategies.non_hybrid_shift_strategy import (
                NonHybridShiftStrategy,
            )
            from core.interfaces.letter_determination.letter_determination_services import (
                IMotionComparisonService,
            )

            # Create mock comparison service for strategy testing
            class MockComparisonService(IMotionComparisonService):
                def compare_motions(self, motion1, motion2, context=None):
                    return 0.8

                def compare_attributes(self, attrs1, attrs2, context=None):
                    from domain.models.letter_determination.determination_models import (
                        AttributeComparisonResult,
                    )

                    return AttributeComparisonResult(is_match=True, confidence=0.8)

                def reverse_prop_rot_dir(self, prop_rot_dir):
                    return "ccw" if prop_rot_dir == "cw" else "cw"

                def apply_direction_inversion(self, direction, prop_rot_dir):
                    return prop_rot_dir

                def find_matching_pictographs(self, target_data, dataset, context=None):
                    return []

            mock_service = MockComparisonService()

            # Test strategy creation
            dual_float = DualFloatStrategy(mock_service)
            non_hybrid_shift = NonHybridShiftStrategy(mock_service)

            assert dual_float.get_strategy_name() == "dual_float"
            assert non_hybrid_shift.get_strategy_name() == "non_hybrid_shift"

        except Exception as e:
            pytest.fail(f"Strategy coverage test failed: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
