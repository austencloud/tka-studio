from __future__ import annotations
from abc import abstractmethod
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ISettingsManager(Protocol):
    @abstractmethod
    def get_setting(self, section: str, key: str, default_value: Any = None) -> Any:
        pass

    @abstractmethod
    def set_setting(self, section: str, key: str, value: Any) -> None:
        pass

    @abstractmethod
    def save_settings(self) -> bool:
        pass

    @abstractmethod
    def load_settings(self) -> bool:
        pass

    @property
    @abstractmethod
    def global_settings(self) -> "IGlobalSettings":
        pass

    @property
    @abstractmethod
    def construct_tab_settings(self) -> "IConstructTabSettings":
        pass

    @property
    @abstractmethod
    def generate_tab_settings(self) -> "IGenerateTabSettings":
        pass

    @property
    @abstractmethod
    def browse_tab_settings(self) -> "IBrowseTabSettings":
        pass

    @property
    @abstractmethod
    def write_tab_settings(self) -> "IWriteTabSettings":
        pass

    @property
    @abstractmethod
    def image_export_settings(self) -> "IImageExportSettings":
        pass

    @property
    @abstractmethod
    def sequence_card_tab_settings(self) -> "ISequenceCardTabSettings":
        pass

    @property
    @abstractmethod
    def user_profile_settings(self) -> "IUserProfileSettings":
        pass

    @property
    @abstractmethod
    def users(self) -> "IUserProfileSettings":
        pass

    @property
    @abstractmethod
    def visibility_settings(self) -> "IVisibilitySettings":
        pass


@runtime_checkable
class IGlobalSettings(Protocol):
    @abstractmethod
    def get_current_tab(self) -> str:
        pass

    @abstractmethod
    def set_current_tab(self, tab_name: str) -> None:
        pass

    @abstractmethod
    def get_grid_mode(self) -> str:
        pass

    @abstractmethod
    def set_grid_mode(self, mode: str) -> None:
        pass

    @abstractmethod
    def get_prop_type(self) -> str:
        pass

    @abstractmethod
    def set_prop_type(self, prop_type: str) -> None:
        pass


@runtime_checkable
class IConstructTabSettings(Protocol):
    @abstractmethod
    def get_level(self) -> int:
        pass


@runtime_checkable
class IGenerateTabSettings(Protocol):
    @abstractmethod
    def get_level(self) -> int:
        pass

    @abstractmethod
    def set_level(self, level: int) -> None:
        pass

    @abstractmethod
    def get_length(self) -> int:
        pass

    @abstractmethod
    def set_length(self, length: int) -> None:
        pass


@runtime_checkable
class IBrowseTabSettings(Protocol):
    @abstractmethod
    def get_sort_method(self) -> str:
        pass

    @abstractmethod
    def set_sort_method(self, method: str) -> None:
        pass


@runtime_checkable
class IWriteTabSettings(Protocol):
    @abstractmethod
    @abstractmethod
    def set_auto_save_enabled(self, enabled: bool) -> None:
        pass


@runtime_checkable
class IImageExportSettings(Protocol):
    @abstractmethod
    def get_include_start_position(self) -> bool:
        pass

    @abstractmethod
    def set_include_start_position(self, include: bool) -> None:
        pass


@runtime_checkable
class ISequenceCardTabSettings(Protocol):
    @abstractmethod
    def get_columns_per_row(self) -> int:
        pass

    @abstractmethod
    def set_columns_per_row(self, columns: int) -> None:
        pass


@runtime_checkable
class IUserProfileSettings(Protocol):
    @abstractmethod
    def get_username(self) -> str:
        pass

    @abstractmethod
    def set_username(self, username: str) -> None:
        pass

    @abstractmethod
    def get_current_user(self) -> str:
        pass


@runtime_checkable
class IVisibilitySettings(Protocol):
    @abstractmethod
    def get_show_grid(self) -> bool:
        pass

    @abstractmethod
    def set_show_grid(self, show: bool) -> None:
        pass
