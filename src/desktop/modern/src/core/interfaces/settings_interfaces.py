from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from core.interfaces.core_services import ISettingsService


class ISettingsDialogService(ABC):
    @abstractmethod
    def show_settings_dialog(self) -> None:
        pass

    @abstractmethod
    def close_settings_dialog(self) -> None:
        pass
