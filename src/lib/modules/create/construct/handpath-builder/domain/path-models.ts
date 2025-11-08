/**
 * Gestural Path Builder Domain Models
 *
 * Pure TypeScript interfaces and types for hand path construction via touch gestures.
 * Represents the domain of drawing hand paths on a grid to create sequences.
 */

import type {
  GridLocation,
  GridMode,
  HandMotionType,
  MotionColor,
  RotationDirection,
} from "$shared";

/**
 * Builder mode - how the user draws paths
 */
export enum PathBuilderMode {
  /** Draw one swipe per beat (discrete) */
  DISCRETE = "discrete",
  /** Continuous drag across multiple beats */
  CONTINUOUS = "continuous",
}

/**
 * A single segment of a hand path from one grid position to another
 */
export interface HandPathSegment {
  readonly beatNumber: number; // 1-indexed beat number in sequence
  readonly startLocation: GridLocation;
  readonly endLocation: GridLocation;
  readonly handMotionType: HandMotionType; // SHIFT, DASH, or STATIC
  readonly timestamp: number; // When this segment was created
}

/**
 * Complete hand path for one hand (blue or red)
 */
export interface HandPath {
  readonly handColor: MotionColor; // BLUE or RED
  readonly segments: readonly HandPathSegment[];
  readonly gridMode: GridMode;
  readonly startingLocation: GridLocation; // First position where hand starts
}

/**
 * Configuration for the gestural path builder session
 */
export interface PathBuilderConfig {
  readonly sequenceLength: number; // Total beats in sequence
  readonly gridMode: GridMode; // DIAMOND or BOX
  readonly startingLocation: GridLocation; // Where the hand starts
  readonly allowedHandMotionTypes: readonly HandMotionType[]; // Which motion types are allowed
}

/**
 * Current state of path building for one hand
 */
export interface PathBuildingState {
  readonly currentBeatNumber: number; // Which beat we're currently drawing (1-indexed)
  readonly currentLocation: GridLocation; // Where the hand currently is
  readonly completedSegments: readonly HandPathSegment[];
  readonly isComplete: boolean; // Has the user finished all beats?
}

/**
 * Result of detecting a swipe gesture
 */
export interface SwipeGesture {
  readonly startLocation: GridLocation;
  readonly endLocation: GridLocation;
  readonly handMotionType: HandMotionType;
  readonly velocity: number; // Pixels per millisecond
  readonly duration: number; // Milliseconds
}

/**
 * Touch/pointer tracking data during gesture
 */
export interface TouchTrackingData {
  readonly startX: number;
  readonly startY: number;
  readonly currentX: number;
  readonly currentY: number;
  readonly startTime: number;
  readonly startLocation: GridLocation;
}

/**
 * Grid position with screen coordinates
 */
export interface GridPositionPoint {
  readonly location: GridLocation;
  readonly x: number; // Screen X coordinate
  readonly y: number; // Screen Y coordinate
  readonly radius: number; // Hit detection radius
}

/**
 * Overall session state for complete sequence construction
 */
export interface GesturalSessionState {
  readonly config: PathBuilderConfig;
  readonly blueHandPath: HandPath | null;
  readonly redHandPath: HandPath | null;
  readonly currentHand: MotionColor; // Which hand is being drawn
  readonly selectedRotationDirection: RotationDirection | null; // User's rotation choice
  readonly isSessionComplete: boolean; // Both hands drawn
}

/**
 * Validation result for a hand path segment
 */
export interface PathSegmentValidation {
  readonly isValid: boolean;
  readonly errorMessage?: string;
  readonly suggestedCorrection?: HandPathSegment;
}

/**
 * State of the advance button for discrete mode
 */
export interface AdvanceButtonState {
  readonly isPressed: boolean;
  readonly pressStartTime: number | null;
  readonly hasMovedSincePress: boolean;
}
