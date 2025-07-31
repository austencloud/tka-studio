# Modern backgrounds package
from .aurora_background import AuroraBackground
from .aurora_borealis_background import AuroraBorealisBackground
from .background_factory import BackgroundFactory
from .background_widget import MainBackgroundWidget
from .bubbles_background import BubblesBackground
from .snowfall_background import SnowfallBackground
from .starfield_background import StarfieldBackground

__all__ = [
    "MainBackgroundWidget",
    "BackgroundFactory",
    "AuroraBackground",
    "AuroraBorealisBackground",
    "BubblesBackground",
    "SnowfallBackground",
    "StarfieldBackground",
]
