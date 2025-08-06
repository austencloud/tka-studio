"""
Core Domain Enums

All enumeration types used throughout the TKA domain models.
Centralized location for type-safe constants and values.
"""

from __future__ import annotations

from enum import Enum


class Timing(Enum):
    TOG = "tog"
    SPLIT = "split"


class Direction(Enum):
    SAME = "same"
    OPP = "opp"


class MotionType(Enum):
    """Types of motion for props and arrows."""

    PRO = "pro"
    ANTI = "anti"
    FLOAT = "float"
    DASH = "dash"
    STATIC = "static"


class HandMotionType(Enum):
    """Types of motion for props and arrows."""

    SHIFT = "shift"
    DASH = "dash"
    STATIC = "static"


class HandPath(Enum):
    """Hand rotation directions."""

    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    DASH = "dash"
    STATIC = "static"


class RotationDirection(Enum):
    """Rotation directions."""

    CLOCKWISE = "cw"
    COUNTER_CLOCKWISE = "ccw"
    NO_ROTATION = "no_rot"


class PropRotationDirection(Enum):
    """Prop rotation directions matching legacy constants."""

    CLOCKWISE = "clockwise"
    COUNTER_CLOCKWISE = "counter_clockwise"
    NO_ROT = "no_rot"


class Orientation(Enum):
    """Prop orientations."""

    IN = "in"
    OUT = "out"
    CLOCK = "clock"
    COUNTER = "counter"


class Location(Enum):
    """Location constants matching legacy exactly."""

    NORTH = "n"
    EAST = "e"
    SOUTH = "s"
    WEST = "w"
    NORTHEAST = "ne"
    SOUTHEAST = "se"
    SOUTHWEST = "sw"
    NORTHWEST = "nw"


"""Remove redundant Position enum - use existing GridPosition"""
# Position enum removed - using existing GridPosition


class GridPosition(Enum):
    """Grid positions matching legacy constants exactly."""

    # Alpha positions (radial)
    ALPHA1 = "alpha1"
    ALPHA2 = "alpha2"
    ALPHA3 = "alpha3"
    ALPHA4 = "alpha4"
    ALPHA5 = "alpha5"
    ALPHA6 = "alpha6"
    ALPHA7 = "alpha7"
    ALPHA8 = "alpha8"

    # Beta positions (box)
    BETA1 = "beta1"
    BETA2 = "beta2"
    BETA3 = "beta3"
    BETA4 = "beta4"
    BETA5 = "beta5"
    BETA6 = "beta6"
    BETA7 = "beta7"
    BETA8 = "beta8"

    # Gamma positions (diamond)
    GAMMA1 = "gamma1"
    GAMMA2 = "gamma2"
    GAMMA3 = "gamma3"
    GAMMA4 = "gamma4"
    GAMMA5 = "gamma5"
    GAMMA6 = "gamma6"
    GAMMA7 = "gamma7"
    GAMMA8 = "gamma8"
    GAMMA9 = "gamma9"
    GAMMA10 = "gamma10"
    GAMMA11 = "gamma11"
    GAMMA12 = "gamma12"
    GAMMA13 = "gamma13"
    GAMMA14 = "gamma14"
    GAMMA15 = "gamma15"
    GAMMA16 = "gamma16"


class VTGMode(Enum):
    """VTG (Vertical/Timing/Grid) modes for pictograph classification."""

    SPLIT_SAME = "SS"
    SPLIT_OPP = "SO"
    TOG_SAME = "TS"
    TOG_OPP = "TO"
    QUARTER_SAME = "QS"
    QUARTER_OPP = "QO"


class ElementalType(Enum):
    """Elemental types for pictograph classification."""

    WATER = "water"
    FIRE = "fire"
    EARTH = "earth"
    AIR = "air"
    SUN = "sun"
    MOON = "moon"


class LetterType(Enum):
    """Letter types for TKA glyph classification."""

    TYPE1 = "Type1"
    TYPE2 = "Type2"
    TYPE3 = "Type3"
    TYPE4 = "Type4"
    TYPE5 = "Type5"
    TYPE6 = "Type6"
    TYPE7 = "Type7"
    TYPE8 = "Type8"
    TYPE9 = "Type9"


class ArrowColor(Enum):
    """Arrow colors matching legacy constants."""

    RED = "red"
    BLUE = "blue"


class GridMode(Enum):
    """Grid modes for pictograph rendering."""

    DIAMOND = "diamond"
    BOX = "box"


class ArrowType(Enum):
    """Types of arrows in pictographs."""

    BLUE = "blue"
    RED = "red"


class PropType(Enum):
    """Types of props in pictographs."""

    # Hand props
    HAND = "hand"

    # Staff variants
    STAFF = "staff"
    SIMPLESTAFF = "simplestaff"
    BIGSTAFF = "bigstaff"

    # Club variants
    CLUB = "club"

    # Buugeng variants
    BUUGENG = "buugeng"
    BIGBUUGENG = "bigbuugeng"
    FRACTALGENG = "fractalgeng"

    # Ring variants
    EIGHTRINGS = "eightrings"
    BIG_EIGHT_RINGS = "bigeightrings"

    # Hoop variants
    MINIHOOP = "minihoop"
    BIGHOOP = "bighoop"

    # Star variants
    DOUBLESTAR = "doublestar"
    BIGDOUBLESTAR = "bigdoublestar"

    # Other props
    FAN = "fan"
    TRIAD = "triad"
    QUIAD = "quiad"
    SWORD = "sword"
    GUITAR = "guitar"
    UKULELE = "ukulele"
    CHICKEN = "chicken"
    TRIQUETRA = "triquetra"
    TRIQUETRA2 = "triquetra2"


class Letter(Enum):
    """Letter constants for TKA glyphs."""

    # Type 1 - Dual Shift
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"
    J = "J"
    K = "K"
    L = "L"
    M = "M"
    N = "N"
    O = "O"
    P = "P"
    Q = "Q"
    R = "R"
    S = "S"
    T = "T"
    U = "U"
    V = "V"

    # Type 2 - Shift
    W = "W"
    X = "X"
    Y = "Y"
    Z = "Z"
    SIGMA = "Σ"
    DELTA = "Δ"
    THETA = "θ"
    OMEGA = "Ω"

    # Type 3 - Cross Shift
    W_CROSS = "W-"
    X_CROSS = "X-"
    Y_CROSS = "Y-"
    Z_CROSS = "Z-"
    SIGMA_CROSS = "Σ-"
    DELTA_CROSS = "Δ-"
    THETA_CROSS = "θ-"
    OMEGA_CROSS = "Ω-"

    # Type 4 - Dash
    PHI = "Φ"
    PSI = "Ψ"
    LAMBDA = "Λ"

    # Type 5 - Dual Dash
    PHI_DUAL = "Φ-"
    PSI_DUAL = "Ψ-"
    LAMBDA_DUAL = "Λ-"

    # Type 6 - Static
    ALPHA = "α"
    BETA = "β"
    GAMMA = "Γ"


class BackgroundType(Enum):
    """Available background types."""

    AURORA = "Aurora"
    AURORA_BOREALIS = "AuroraBorealis"
    BUBBLES = "Bubbles"
    SNOWFALL = "Snowfall"
    STARFIELD = "Starfield"


class PickerMode(Enum):
    """Picker display modes."""

    BASIC = "basic"
    ADVANCED = "advanced"
    AUTO = "auto"
