from __future__ import annotations
from collections.abc import Callable
from typing import TYPE_CHECKING

from base_widgets.pictograph.elements.views.option_view import OptionView
from base_widgets.pictograph.legacy_pictograph import LegacyPictograph
from PyQt6.QtCore import QSize

if TYPE_CHECKING:
    from main_window.main_widget.construct_tab.option_picker.widgets.legacy_option_picker import (
        LegacyOptionPicker,
    )


class OptionFactory:
    MAX_PICTOGRAPHS = 36

    def __init__(
        self, option_picker: "LegacyOptionPicker", mw_size_provider: Callable[[], QSize]
    ) -> None:
        self.option_picker = option_picker
        self.mw_size_provider = mw_size_provider
        # Build the option pool upon instantiation.
        self.option_picker.option_pool = self.create_options()

    def create_options(self) -> list[LegacyPictograph]:
        options: list[LegacyPictograph] = []
        for _ in range(self.MAX_PICTOGRAPHS):
            opt = LegacyPictograph()
            # Construct the view using OptionView, passing the picker and size provider.
            opt.elements.view = OptionView(
                self.option_picker, opt, self.mw_size_provider
            )
            options.append(opt)
        return options
