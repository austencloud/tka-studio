from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .image_export_manager import ImageExportManager


class ImageExportLayoutHandler:
    def __init__(self, image_export_manager: "ImageExportManager"):
        self.image_export_manager = image_export_manager
        self.beat_frame = image_export_manager.beat_frame

    @property
    def include_start_pos(self):
        # Dynamically fetch the current setting from the export manager
        return self.image_export_manager.include_start_pos

    def get_current_beat_frame_layout(self, beat_count: int) -> tuple[int, int]:
        """
        Get the current layout from the beat frame's layout manager.
        This ensures the exported image matches the current beat frame layout.

        Returns a tuple of (rows, columns) to match the format used in the beat frame layout.
        """
        return self.beat_frame.layout_manager.calculate_layout(beat_count)

    def calculate_layout(
        self, filled_beat_count: int, include_start_pos: bool
    ) -> tuple[int, int]:
        """
        Determine the layout based on the current beat frame layout and adjust for start position if needed.

        Returns a tuple of (columns, rows) for the image layout.
        """
        # Get the current layout from the beat frame
        # Note: beat_frame_layout_manager.calculate_layout returns (rows, columns)
        # So we need to assign them correctly to swap for image creator
        rows, columns = self.get_current_beat_frame_layout(filled_beat_count)

        # If including start position and it's not already accounted for in the layout,
        # adjust the layout to accommodate it
        if include_start_pos:
            # Add an extra column for the start position if needed
            # Beat frame gives us (rows, columns), image creator expects (columns, rows)
            # So we need to swap: return (columns, rows)
            return (columns + 1, rows) if filled_beat_count > 0 else (1, 1)

        # Return in (columns, rows) format for the image creator
        # Beat frame returns (rows, columns), image creator expects (columns, rows)
        # So we swap: return (columns, rows) to get wide layouts for wide sequences
        result = (columns, rows)

        return result

    def calculate_layout_with_start(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Calculate layout considering an additional column for the start position.
        """
        # For backward compatibility, keep this method but use the new approach
        return self.calculate_layout(filled_beat_count, True)

    def calculate_layout_without_start(self, filled_beat_count: int) -> tuple[int, int]:
        """
        Calculate layout without the start position affecting the column count.
        """
        # For backward compatibility, keep this method but use the new approach
        return self.calculate_layout(filled_beat_count, False)

    def calculate_optimal_layout(
        self, beat_count: int, layout_options: dict
    ) -> tuple[int, int]:
        """
        Shared logic for calculating layout which can be customized further using provided layout options.
        """
        # For backward compatibility, keep this method
        if beat_count in layout_options:
            return layout_options[beat_count]
        return self.get_fallback_layout(beat_count)

    def get_fallback_layout(self, beat_count: int) -> tuple[int, int]:
        """
        Provide a fallback layout when beat_count is not in layout_options.
        """
        # Simple fallback: try to make a roughly square layout
        if beat_count <= 4:
            return (1, beat_count)
        elif beat_count <= 16:
            rows = int(beat_count**0.5)
            cols = (beat_count + rows - 1) // rows
            return (rows, cols)
        else:
            # For larger counts, use a 4-column layout
            rows = (beat_count + 3) // 4
            return (rows, 4)

    def get_layout_options_with_start(self) -> dict[int, tuple[int, int]]:
        """
        Layout options when including the start position in the layout.
        """
        return {
            0: (1, 1),
            1: (2, 1),
            2: (3, 1),
            3: (4, 1),
            4: (5, 1),
            5: (4, 2),
            6: (4, 2),
            7: (5, 2),
            8: (5, 2),
            9: (4, 3),
            10: (6, 2),
            11: (5, 3),
            12: (4, 4),
            13: (5, 4),
            14: (5, 4),
            15: (5, 4),
            16: (5, 4),
            17: (5, 5),
            18: (5, 5),
            19: (5, 5),
            20: (6, 4),
            21: (5, 6),
            22: (5, 6),
            23: (5, 6),
            24: (7, 4),
            25: (5, 7),
            26: (5, 7),
            27: (5, 7),
            28: (5, 7),
            29: (5, 8),
            30: (8, 4),
            31: (5, 8),
            32: (9, 4),
            33: (5, 9),
            34: (5, 9),
            35: (5, 9),
            36: (10, 4),
            37: (5, 10),
            38: (5, 10),
            39: (5, 10),
            40: (11, 4),
            41: (5, 11),
            42: (5, 11),
            43: (5, 11),
            44: (5, 11),
            45: (5, 12),
            46: (5, 12),
            47: (5, 12),
            48: (5, 12),
            49: (5, 13),
            50: (5, 13),
            51: (5, 13),
            52: (5, 13),
            53: (5, 14),
            54: (5, 14),
            55: (5, 14),
            56: (5, 14),
            57: (5, 15),
            58: (5, 15),
            59: (5, 15),
            60: (5, 15),
            61: (5, 16),
            62: (5, 16),
            63: (5, 16),
            64: (5, 16),
        }

    def get_layout_options_without_start(self) -> dict[int, tuple[int, int]]:
        """
        Use the same layout source as TempBeatFrameLayoutManager for consistency.
        This ensures there's only ONE source of truth for layouts.
        """
        from data.beat_frame_layouts import sequence_workbench_BEAT_FRAME_LAYOUTS

        return sequence_workbench_BEAT_FRAME_LAYOUTS
