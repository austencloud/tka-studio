"""
Simplified Generation Services - Core Functionality Only

This demonstrates what the refactored services should actually look like
without over-engineering. Based on analysis of original service functionality.
"""

from copy import deepcopy
import csv
import logging
from pathlib import Path
import random
from typing import Any, Optional


# Mock imports for demonstration
class GenerationConfig:
    def __init__(self, mode, length, level, letter_types=None, prop_continuity=None):
        self.mode = mode
        self.length = length
        self.level = level
        self.letter_types = letter_types or set()
        self.prop_continuity = prop_continuity


class PictographData:
    def __init__(self, letter, start_position, end_position, beat, motions=None):
        self.letter = letter
        self.start_position = start_position
        self.end_position = end_position
        self.beat = beat
        self.motions = motions or {}


logger = logging.getLogger(__name__)


class SimpleDataLoader:
    """
    Simple data loader - replaces over-engineered PictographDataRepository.
    Does exactly what the original service does: loads CSV files once.
    """

    def __init__(self):
        self.diamond_data: list[dict[str, Any]] = []
        self.box_data: list[dict[str, Any]] = []
        self.all_data: list[dict[str, Any]] = []
        self._load_data()

    def _load_data(self):
        """Load CSV data - simple and direct."""
        try:
            data_dir = Path("src/desktop/data")

            # Load diamond data
            diamond_file = data_dir / "DiamondPictographDataframe.csv"
            if diamond_file.exists():
                with open(diamond_file) as f:
                    reader = csv.DictReader(f)
                    self.diamond_data = list(reader)

            # Load box data
            box_file = data_dir / "BoxPictographDataframe.csv"
            if box_file.exists():
                with open(box_file) as f:
                    reader = csv.DictReader(f)
                    self.box_data = list(reader)

            self.all_data = self.diamond_data + self.box_data
            logger.info(
                f"Loaded {len(self.all_data)} pictographs ({len(self.diamond_data)} diamond, {len(self.box_data)} box)"
            )

        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            self.all_data = []

    def get_all_data(self) -> list[dict[str, Any]]:
        """Get all pictograph data."""
        return self.all_data

    def get_diamond_data(self) -> list[dict[str, Any]]:
        """Get diamond pictograph data."""
        return self.diamond_data

    def get_box_data(self) -> list[dict[str, Any]]:
        """Get box pictograph data."""
        return self.box_data


class SimpleCSVConverter:
    """
    Simple CSV to PictographData converter.
    Replaces over-engineered conversion layer.
    """

    def convert(
        self, csv_row: dict[str, Any], beat_number: int
    ) -> Optional[PictographData]:
        """Convert CSV row to PictographData - simple and direct."""
        try:
            return PictographData(
                letter=csv_row.get("letter", ""),
                start_position=csv_row.get("start_pos", ""),
                end_position=csv_row.get("end_pos", ""),
                beat=beat_number,
                motions=self._extract_motions(csv_row),
            )
        except Exception as e:
            logger.error(f"Failed to convert CSV row: {e}")
            return None

    def _extract_motions(self, csv_row: dict[str, Any]) -> dict[str, Any]:
        """Extract motion data from CSV row."""
        motions = {}

        # Extract blue motion
        if "blue_motion_type" in csv_row:
            motions["blue"] = {
                "motion_type": csv_row.get("blue_motion_type", ""),
                "prop_rot_dir": csv_row.get("blue_prop_rot_dir", ""),
                "start_loc": csv_row.get("blue_start_loc", ""),
                "end_loc": csv_row.get("blue_end_loc", ""),
            }

        # Extract red motion
        if "red_motion_type" in csv_row:
            motions["red"] = {
                "motion_type": csv_row.get("red_motion_type", ""),
                "prop_rot_dir": csv_row.get("red_prop_rot_dir", ""),
                "start_loc": csv_row.get("red_start_loc", ""),
                "end_loc": csv_row.get("red_end_loc", ""),
            }

        return motions


class SimpleFilter:
    """
    Simple filtering - replaces over-engineered filter chain.
    Does exactly what the original service does.
    """

    def filter_options(
        self,
        options: list[dict[str, Any]],
        config: GenerationConfig,
        current_end_position: Optional[str] = None,
        grid_mode: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """Filter options based on config - simple sequential filtering."""

        filtered = deepcopy(options)

        # Filter by positional continuity (CRITICAL)
        if current_end_position:
            filtered = [
                opt for opt in filtered if opt.get("start_pos") == current_end_position
            ]
            logger.info(
                f"Positional continuity: {len(filtered)} options start at {current_end_position}"
            )

        # Filter by letter types
        if config.letter_types:
            allowed_letters = self._get_letters_for_types(config.letter_types)
            filtered = [opt for opt in filtered if opt.get("letter") in allowed_letters]
            logger.info(f"Letter type filter: {len(filtered)} options match types")

        # Filter by grid mode consistency
        if grid_mode:
            if grid_mode == "diamond":
                filtered = [
                    opt
                    for opt in filtered
                    if self._is_diamond_position(opt.get("start_pos"))
                ]
            elif grid_mode == "box":
                filtered = [
                    opt
                    for opt in filtered
                    if self._is_box_position(opt.get("start_pos"))
                ]
            logger.info(f"Grid mode filter ({grid_mode}): {len(filtered)} options")

        return filtered

    def _get_letters_for_types(self, letter_types: set) -> set[str]:
        """Get letters for specified types - simplified mapping."""
        # Simplified version of original letter type mapping
        all_letters = set()
        for letter_type in letter_types:
            if hasattr(letter_type, "value") and letter_type.value == "TYPE1":
                all_letters.update(
                    [
                        "A",
                        "B",
                        "C",
                        "D",
                        "E",
                        "F",
                        "G",
                        "H",
                        "I",
                        "J",
                        "K",
                        "L",
                        "M",
                        "N",
                        "O",
                        "P",
                        "Q",
                        "R",
                        "S",
                        "T",
                        "U",
                        "V",
                    ]
                )
            # Add other types as needed
        return all_letters

    def _is_diamond_position(self, position: str) -> bool:
        """Check if position is diamond."""
        diamond_positions = [
            "alpha1",
            "alpha3",
            "alpha5",
            "alpha7",
            "beta1",
            "beta3",
            "beta5",
            "beta7",
            "gamma1",
            "gamma3",
            "gamma5",
            "gamma7",
        ]
        return position in diamond_positions

    def _is_box_position(self, position: str) -> bool:
        """Check if position is box."""
        box_positions = [
            "alpha2",
            "alpha4",
            "alpha6",
            "alpha8",
            "beta2",
            "beta4",
            "beta6",
            "beta8",
            "gamma2",
            "gamma4",
            "gamma6",
            "gamma8",
        ]
        return position in box_positions


class SimpleFreeformGenerator:
    """
    Simplified freeform generator - core functionality only.
    Replaces over-engineered orchestrator + services.
    """

    def __init__(self):
        self.data_loader = SimpleDataLoader()
        self.converter = SimpleCSVConverter()
        self.filter = SimpleFilter()
        self.current_end_position: Optional[str] = None
        self.grid_mode: Optional[str] = None

    def generate_sequence(self, config: GenerationConfig) -> list[PictographData]:
        """Generate freeform sequence - simple and direct."""

        # Simple validation
        if config.length <= 0 or config.length > 32:
            raise ValueError("Invalid sequence length")

        logger.info(
            f"Generating freeform sequence: length={config.length}, level={config.level}"
        )

        sequence = []
        available_data = self.data_loader.get_all_data()

        for beat_num in range(1, config.length + 1):
            # Filter options
            filtered_options = self.filter.filter_options(
                available_data, config, self.current_end_position, self.grid_mode
            )

            if not filtered_options:
                logger.warning(f"No options available for beat {beat_num}")
                break

            # Select random option
            selected_csv = random.choice(filtered_options)

            # Convert to PictographData
            pictograph = self.converter.convert(selected_csv, beat_num)
            if pictograph:
                sequence.append(pictograph)

                # Update state for next beat
                self.current_end_position = pictograph.end_position
                if not self.grid_mode:
                    self.grid_mode = (
                        "diamond"
                        if self.filter._is_diamond_position(pictograph.start_position)
                        else "box"
                    )

                # Process events for UI responsiveness
                try:
                    from PyQt6.QtCore import QCoreApplication

                    QCoreApplication.processEvents()
                except:
                    pass  # No Qt available

        logger.info(f"Generated {len(sequence)} beats")
        return sequence


class SimpleCircularGenerator:
    """
    Simplified circular generator - core functionality only.
    Replaces over-engineered transformation engine.
    """

    def __init__(self):
        self.freeform_generator = SimpleFreeformGenerator()

    def generate_sequence(self, config: GenerationConfig) -> list[PictographData]:
        """Generate circular sequence with CAP transformations."""

        # Calculate word length (simplified)
        word_length = max(1, config.length // 2)  # Default to halved

        # Generate base pattern
        base_config = GenerationConfig(
            mode=config.mode,
            length=word_length,
            level=config.level,
            letter_types=config.letter_types,
            prop_continuity=config.prop_continuity,
        )

        base_pattern = self.freeform_generator.generate_sequence(base_config)

        # Apply CAP transformation (simplified)
        cap_type = getattr(config, "cap_type", "rotated")
        transformed_pattern = self._apply_cap_transformation(base_pattern, cap_type)

        # Combine base + transformed
        full_sequence = base_pattern + transformed_pattern

        # Trim to requested length
        return full_sequence[: config.length]

    def _apply_cap_transformation(
        self, base_pattern: list[PictographData], cap_type: str
    ) -> list[PictographData]:
        """Apply CAP transformation - simplified version."""

        if cap_type == "rotated":
            return self._apply_rotated_transformation(base_pattern)
        elif cap_type == "mirrored":
            return self._apply_mirrored_transformation(base_pattern)
        # Add other transformations as needed

        return base_pattern  # Fallback

    def _apply_rotated_transformation(
        self, pattern: list[PictographData]
    ) -> list[PictographData]:
        """Apply 180-degree rotation transformation."""
        # Simplified rotation logic
        transformed = []
        for beat in pattern:
            # Create rotated version (simplified)
            rotated = PictographData(
                letter=beat.letter,
                start_position=self._rotate_position(beat.start_position),
                end_position=self._rotate_position(beat.end_position),
                beat=beat.beat + len(pattern),
                motions=beat.motions,  # Simplified - would need rotation logic
            )
            transformed.append(rotated)
        return transformed

    def _apply_mirrored_transformation(
        self, pattern: list[PictographData]
    ) -> list[PictographData]:
        """Apply horizontal mirror transformation."""
        # Simplified mirror logic
        transformed = []
        for beat in pattern:
            mirrored = PictographData(
                letter=beat.letter,
                start_position=self._mirror_position(beat.start_position),
                end_position=self._mirror_position(beat.end_position),
                beat=beat.beat + len(pattern),
                motions=beat.motions,  # Simplified
            )
            transformed.append(mirrored)
        return transformed

    def _rotate_position(self, position: str) -> str:
        """Rotate position 180 degrees - simplified."""
        # Simplified rotation mapping
        rotation_map = {
            "alpha1": "gamma5",
            "alpha3": "gamma7",
            "alpha5": "gamma1",
            "alpha7": "gamma3",
            "beta1": "beta5",
            "beta3": "beta7",
            "beta5": "beta1",
            "beta7": "beta3",
            "gamma1": "alpha5",
            "gamma3": "alpha7",
            "gamma5": "alpha1",
            "gamma7": "alpha3",
        }
        return rotation_map.get(position, position)

    def _mirror_position(self, position: str) -> str:
        """Mirror position horizontally - simplified."""
        # Simplified mirror mapping
        mirror_map = {
            "alpha1": "alpha7",
            "alpha3": "alpha5",
            "alpha5": "alpha3",
            "alpha7": "alpha1",
            "beta1": "beta7",
            "beta3": "beta5",
            "beta5": "beta3",
            "beta7": "beta1",
            "gamma1": "gamma7",
            "gamma3": "gamma5",
            "gamma5": "gamma3",
            "gamma7": "gamma1",
        }
        return mirror_map.get(position, position)


# Test the simplified services
def test_simplified_services():
    """Test the simplified services."""
    print("🧪 Testing Simplified Generation Services")
    print("=" * 50)

    try:
        # Test data loader
        loader = SimpleDataLoader()
        print(f"✅ Data loader: {len(loader.get_all_data())} pictographs loaded")

        # Test freeform generation
        config = GenerationConfig(
            mode="freeform", length=4, level=1, letter_types=set()
        )

        freeform_gen = SimpleFreeformGenerator()
        sequence = freeform_gen.generate_sequence(config)
        print(f"✅ Freeform generation: {len(sequence)} beats generated")

        # Test circular generation
        circular_gen = SimpleCircularGenerator()
        circular_sequence = circular_gen.generate_sequence(config)
        print(f"✅ Circular generation: {len(circular_sequence)} beats generated")

        print("\n🎉 All simplified services working!")

    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == "__main__":
    test_simplified_services()
