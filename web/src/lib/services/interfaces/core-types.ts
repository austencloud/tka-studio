/**
 * Core Types and Shared Interfaces
 *
 * Fundamental types used across multiple service domains.
 * This file contains shared data structures, coordinates, and utility types.
 */

import type { GridData, PictographData } from "../../domain";
import { GridMode as DomainGridMode } from "../../domain";

// Re-export domain types for service interfaces
export type { GridData, PictographData };
import type {
  DifficultyLevel,
  Location,
  MotionColor,
  MotionType,
  Orientation,
} from "../../domain/enums";

// ============================================================================
// BASIC COORDINATE TYPES
// ============================================================================

export interface Coordinates {
  x: number;
  y: number;
}

export interface GridPoint {
  coordinates: Coordinates;
}

// ============================================================================
// ARROW POSITIONING TYPES
// ============================================================================

// ArrowPosition moved to $lib/services/positioning/types.ts

export interface LegacyArrowData {
  id: string;
  color: MotionColor;
  motionType: MotionType;
  location: Location;
  startOrientation: Orientation;
  endOrientation: Orientation;
  rotationDirection: string;
  turns: number;
  isMirrored: boolean;
  coords?: Coordinates;
  rotAngle?: number;
  svgCenter?: Coordinates;
  svgMirrored?: boolean;
}

export interface ArrowPlacementConfig {
  pictographData: PictographData;
  gridData: GridData;
  checker?: unknown;
}

// ============================================================================
// PROP TYPES
// ============================================================================

export interface PropPlacementData {
  id: string;
  propType: string;
  color: MotionColor;
  location: Location;
  position: Coordinates;
  rotation: number;
}

export interface PropPosition {
  x: number;
  y: number;
  rotation: number;
}

// ============================================================================
// TYPE ALIASES
// ============================================================================

// Use centralized enum types - no duplicates!
export type HandRotDir = "cw_shift" | "ccw_shift";
export type GridMode = DomainGridMode;

// Re-export types from domain
export type {
  DifficultyLevel,
  MotionColor,
  PropContinuity,
} from "../../domain/enums";

// ============================================================================
// OPTION FILTER TYPES
// ============================================================================

export interface OptionFilters {
  difficulty?: DifficultyLevel;
  motionTypes?: MotionType[];
  minTurns?: number;
  maxTurns?: number;
}

// ============================================================================
// SERVICE REGISTRY TYPES
// ============================================================================

export type ServiceInterface<T> = {
  readonly name: string;
  readonly _type?: T;
};

/**
 * Helper function to define service interfaces for the DI container
 */
export function defineService<T>(name: string): ServiceInterface<T> {
  return { name } as ServiceInterface<T>;
}
