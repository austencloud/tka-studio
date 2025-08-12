from dataclasses import dataclass


@dataclass
class Position2D:
    x: float
    y: float


@dataclass
class Velocity2D:
    dx: float
    dy: float


@dataclass
class AnimationBounds:
    width: float
    height: float


# Aurora-specific types
@dataclass
class BlobState:
    position: Position2D
    velocity: Velocity2D
    size: float
    opacity: float
    size_delta: float
    opacity_delta: float


@dataclass
class SparkleState:
    position: Position2D
    size: float
    opacity: float
    pulse_speed: float


# Snowfall-specific types
@dataclass
class SnowflakeState:
    x: float
    y: float
    size: int
    speed: float
    image_index: int


@dataclass
class SantaState:
    x: float
    y: float
    speed: float
    direction: int
    active: bool
    opacity: float


@dataclass
class ShootingStarState:
    position: Position2D
    velocity: Velocity2D
    size: float
    speed: float
    tail: list[tuple[float, float, float]]  # (x, y, size) tuples
    tail_length: int
    tail_opacity: float
    off_screen: bool


# Starfield-specific types
@dataclass
class StarState:
    position: Position2D
    size: float
    color: tuple[int, int, int, int]  # RGBA
    spikiness: int
    twinkle_speed: float
    twinkle_phase: float


@dataclass
class CometState:
    position: Position2D
    prev_position: Position2D
    velocity: Velocity2D
    size: float
    speed: float
    tail: list[tuple[float, float, float]]
    color: tuple[int, int, int]
    active: bool
    fading: bool
    off_screen: bool


@dataclass
class UFOState:
    position: Position2D
    velocity: Velocity2D
    size: float
    speed: float
    active: bool
    paused: bool
    pause_duration: int
    glow_phase: float


# Bubbles-specific types
@dataclass
class BubbleState:
    position: Position2D
    size: float
    speed: float
    opacity: float
    highlight_factor: float


@dataclass
class FishState:
    position: Position2D
    velocity: Velocity2D
    size: float
    speed: float
    image_index: int
