from __future__ import annotations

from abc import ABC, abstractmethod


class ISettingsDialogService(ABC):
    @abstractmethod
    def show_settings_dialog(self) -> None:
        pass

    @abstractmethod
    def close_settings_dialog(self) -> None:
        pass
