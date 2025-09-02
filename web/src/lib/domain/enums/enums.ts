/**
 * Core Domain Enums
 *
 * All enumeration types used throughout the TKA domain models.
 * Centralized location for type-safe constants and values.
 * Based on modern desktop app's enums.py
 */

export enum Timing {
  TOG = "tog",
  SPLIT = "split",
  QUARTER = "quarter",
  NONE = "none",
}

export enum Direction {
  SAME = "same",
  OPP = "opp",
  NONE = "none",
}

export enum MotionType {
  PRO = "pro",
  ANTI = "anti",
  FLOAT = "float",
  DASH = "dash",
  STATIC = "static",
}

export enum HandMotionType {
  SHIFT = "shift",
  DASH = "dash",
  STATIC = "static",
}

export enum HandPath {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  DASH = "dash",
  STATIC = "static",
}

export enum MotionColor {
  BLUE = "blue",
  RED = "red",
}

export enum RotationDirection {
  CLOCKWISE = "cw",
  COUNTER_CLOCKWISE = "ccw",
  NO_ROTATION = "noRotation",
}

export enum Orientation {
  IN = "in",
  OUT = "out",
  CLOCK = "clock",
  COUNTER = "counter",
}

export enum Location {
  NORTH = "n",
  EAST = "e",
  SOUTH = "s",
  WEST = "w",
  NORTHEAST = "ne",
  SOUTHEAST = "se",
  SOUTHWEST = "sw",
  NORTHWEST = "nw",
}

export enum GridPositionGroup {
  ALPHA = "alpha",
  BETA = "beta",
  GAMMA = "gamma",
}

export enum GridPosition {
  ALPHA1 = "alpha1",
  ALPHA2 = "alpha2",
  ALPHA3 = "alpha3",
  ALPHA4 = "alpha4",
  ALPHA5 = "alpha5",
  ALPHA6 = "alpha6",
  ALPHA7 = "alpha7",
  ALPHA8 = "alpha8",

  BETA1 = "beta1",
  BETA2 = "beta2",
  BETA3 = "beta3",
  BETA4 = "beta4",
  BETA5 = "beta5",
  BETA6 = "beta6",
  BETA7 = "beta7",
  BETA8 = "beta8",

  GAMMA1 = "gamma1",
  GAMMA2 = "gamma2",
  GAMMA3 = "gamma3",
  GAMMA4 = "gamma4",
  GAMMA5 = "gamma5",
  GAMMA6 = "gamma6",
  GAMMA7 = "gamma7",
  GAMMA8 = "gamma8",
  GAMMA9 = "gamma9",
  GAMMA10 = "gamma10",
  GAMMA11 = "gamma11",
  GAMMA12 = "gamma12",
  GAMMA13 = "gamma13",
  GAMMA14 = "gamma14",
  GAMMA15 = "gamma15",
  GAMMA16 = "gamma16",
}

export enum GridMode {
  DIAMOND = "diamond",
  BOX = "box",
  SKEWED = "skewed",
}

export enum PositionSystem {
  ALPHA_TO_ALPHA = "alpha_to_alpha",
  ALPHA_TO_BETA = "alpha_to_beta",
  ALPHA_TO_GAMMA = "alpha_to_gamma",
  BETA_TO_ALPHA = "beta_to_alpha",
  BETA_TO_BETA = "beta_to_beta",
  BETA_TO_GAMMA = "beta_to_gamma",
  GAMMA_TO_ALPHA = "gamma_to_alpha",
  GAMMA_TO_BETA = "gamma_to_beta",
  GAMMA_TO_GAMMA = "gamma_to_gamma",
}

export enum DifficultyLevel {
  BEGINNER = "beginner",
  INTERMEDIATE = "intermediate",
  ADVANCED = "advanced",
}

export enum PropContinuity {
  CONTINUOUS = "continuous",
  RANDOM = "random",
}

export enum GenerationMode {
  FREEFORM = "freeform",
  CIRCULAR = "circular",
}

export enum PropType {
  STAFF = "staff",
  CLUB = "club",
  HOOP = "hoop",
  BUUGENG = "buugeng",
  FAN = "fan",
  TRIAD = "triad",
  MINIHOOP = "minihoop",
  POI = "poi",
}

export enum VTGMode {
  SPLIT_SAME = "SS",
  SPLIT_OPP = "SO",
  TOG_SAME = "TS",
  TOG_OPP = "TO",
  QUARTER_SAME = "QS",
  QUARTER_OPP = "QO",
}

export enum ElementalType {
  WATER = "water",
  FIRE = "fire",
  EARTH = "earth",
}

export enum LetterType {
  TYPE1 = "Type1",
  TYPE2 = "Type2",
  TYPE3 = "Type3",
  TYPE4 = "Type4",
  TYPE5 = "Type5",
  TYPE6 = "Type6",
}

export enum GlyphType {
  TKA = "tka",
  REVERSALS = "reversals",
  VTG = "vtg",
  ELEMENTAL = "elemental",
  POSITIONS = "positions",
}

export enum SliceSize {
  HALVED = "halved",
  QUARTERED = "quartered",
}

// Fundamental CAP components that can be combined
export enum CAPComponent {
  ROTATED = "rotated",
  MIRRORED = "mirrored",
  SWAPPED = "swapped",
  COMPLEMENTARY = "complementary",
}

// Legacy CAP types for backward compatibility
export enum CAPType {
  STRICT_ROTATED = "strictRotated",
  STRICT_MIRRORED = "strictMirrored",
  STRICT_SWAPPED = "strictSwapped",
  STRICT_COMPLEMENTARY = "strictComplementary",
  SWAPPED_COMPLEMENTARY = "swappedComplementary",
  ROTATED_COMPLEMENTARY = "rotatedComplementary",
  MIRRORED_SWAPPED = "mirroredSwapped",
  MIRRORED_COMPLEMENTARY = "mirroredComplementary",
  ROTATED_SWAPPED = "rotatedSwapped",
  MIRRORED_ROTATED = "mirroredRotated",
  MIRRORED_COMPLEMENTARY_ROTATED = "mirroredComplementaryRotated",
}

// OptionPickerReversalFilter removed - use ReversalFilter instead

export enum OptionPickerSortMethod {
  LETTER_TYPE = "letterType",
  END_POSITION = "endPosition",
  REVERSALS = "reversals",
}

export enum DeviceType {
  SMALL_MOBILE = "smallMobile",
  MOBILE = "mobile",
  TABLET = "tablet",
  DESKTOP = "desktop",
  LARGE_DESKTOP = "largeDesktop",
}

export enum ContainerAspect {
  TALL = "tall",
  SQUARE = "square",
  WIDE = "wide",
  WIDISH = "widish",
}

export enum ReversalFilter {
  ALL = "all",
  CONTINUOUS = "continuous",
  ONE_REVERSAL = "oneReversal",
  TWO_REVERSALS = "twoReversals",
}

export enum LayoutCategory {
  SINGLE_ITEM = "singleItem",
  TWO_ITEMS = "twoItems",
  FEW_ITEMS = "fewItems",
  MEDIUM_ITEMS = "mediumItems",
  MANY_ITEMS = "manyItems",
}

// ============================================================================
// BROWSE ENUMS
// ============================================================================

export enum FilterType {
  STARTING_LETTER = "starting_letter",
  CONTAINS_LETTERS = "contains_letters",
  LENGTH = "length",
  DIFFICULTY = "difficulty",
  startPosition = "startPosition",
  AUTHOR = "author",
  GRID_MODE = "gridMode",
  ALL_SEQUENCES = "all_sequences",
  FAVORITES = "favorites",
  RECENT = "recent",
}

export enum SortMethod {
  ALPHABETICAL = "alphabetical",
  dateAdded = "dateAdded",
  difficultyLevel = "difficultyLevel",
  sequenceLength = "sequenceLength",
  AUTHOR = "author",
  POPULARITY = "popularity",
}

// ============================================================================
// LAYOUT ENUMS
// ============================================================================

export enum ResizeDirection {
  HORIZONTAL = "horizontal",
  VERTICAL = "vertical",
  BOTH = "both",
  RIGHT = "right",
}

export enum ResizeOperation {
  START = "start",
  RESIZE = "resize",
  END = "end",
}
