"""
DEPRECATED: Backward compatibility import
Use option_picker.services.data.beat_loader instead
"""
import warnings
warnings.warn(
    "Importing from option_picker.beat_data_loader is deprecated. "
    "Use option_picker.services.data.beat_loader instead.",
    DeprecationWarning, stacklevel=2
)
from .services.data.beat_loader import BeatDataLoader
__all__ = ['BeatDataLoader']
