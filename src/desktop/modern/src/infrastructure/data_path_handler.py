from __future__ import annotations

from pathlib import Path

import pandas as pd


class DataPathHandler:
    """Centralized handler for data file paths and loading operations."""

    _instance: DataPathHandler | None = None
    _data_dir: Path | None = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._data_dir = cls._instance._resolve_data_directory()
        return cls._instance

    def __init__(self):
        pass

    def _resolve_data_directory(self) -> Path:
        """Resolve the root data directory path."""
        current_file = Path(__file__).resolve()  # Use .resolve() for absolute path
        # Go up to project root and find data directory
        # From: src/infrastructure/data_path_handler.py
        # To: data/
        project_root = current_file.parent.parent.parent.parent
        data_dir = project_root / "data"

        # Fallback: if data dir doesn't exist, look for it by searching upwards
        if not data_dir.exists():
            # Search upwards from current file to find the data directory
            search_path = current_file.parent
            while search_path.parent != search_path:  # Not at filesystem root
                potential_data = search_path / "data"
                if potential_data.exists() and (potential_data / "DiamondPictographDataframe.csv").exists():
                    return potential_data
                search_path = search_path.parent

            # Last resort: look for TKA directory structure
            search_path = current_file.parent
            while search_path.parent != search_path:
                if search_path.name == "TKA":
                    return search_path / "data"
                search_path = search_path.parent

        return data_dir

    @property
    def data_dir(self) -> Path:
        """Get the data directory path."""
        if self._data_dir is None:
            self._data_dir = self._resolve_data_directory()
        return self._data_dir

    @property
    def diamond_csv_path(self) -> Path:
        """Get the diamond pictograph CSV file path."""
        return self.data_dir / "DiamondPictographDataframe.csv"

    @property
    def box_csv_path(self) -> Path:
        """Get the box pictograph CSV file path."""
        return self.data_dir / "BoxPictographDataframe.csv"

    def load_diamond_dataset(self) -> pd.DataFrame | None:
        """Load diamond pictograph dataset."""
        if self.diamond_csv_path.exists():
            return pd.read_csv(self.diamond_csv_path)
        return None

    def load_box_dataset(self) -> pd.DataFrame | None:
        """Load box pictograph dataset."""
        if self.box_csv_path.exists():
            return pd.read_csv(self.box_csv_path)
        return None

    def load_combined_dataset(self) -> pd.DataFrame:
        """Load and combine both diamond and box datasets."""
        diamond_df = self.load_diamond_dataset()
        box_df = self.load_box_dataset()

        datasets = [df for df in [diamond_df, box_df] if df is not None]

        if datasets:
            return pd.concat(datasets, ignore_index=True)
        return pd.DataFrame()

    def validate_data_files(self) -> dict:
        """Check if data files exist and return status."""
        return {
            "diamond_exists": self.diamond_csv_path.exists(),
            "box_exists": self.box_csv_path.exists(),
            "diamond_path": str(self.diamond_csv_path),
            "box_path": str(self.box_csv_path),
            "data_dir": str(self.data_dir),
        }
