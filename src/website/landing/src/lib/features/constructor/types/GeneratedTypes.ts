/**
 * Generated TypeScript Types v2
 *
 * Based on modern desktop Pydantic models with camelCase JSON serialization.
 * These types ensure compatibility between Python backend and TypeScript frontend.
 *
 * GENERATED FROM: Desktop Pydantic models
 * DO NOT EDIT MANUALLY - Regenerate when Python models change
 */

// Core type aliases matching Pydantic Literal types
export type MotionType = 'pro' | 'anti' | 'float' | 'dash' | 'static';
export type PropRotDir = 'cw' | 'ccw' | 'no_rot';
export type Location = 'n' | 'e' | 's' | 'w' | 'ne' | 'nw' | 'se' | 'sw';
export type Orientation = 'in' | 'out' | 'clock' | 'counter';
export type GridMode = 'diamond' | 'box';
export type StartEndPos =
  | 'alpha1' | 'alpha2' | 'alpha3' | 'alpha4' | 'alpha5' | 'alpha6' | 'alpha7' | 'alpha8'
  | 'beta1' | 'beta2' | 'beta3' | 'beta4' | 'beta5' | 'beta6' | 'beta7' | 'beta8'
  | 'gamma1' | 'gamma2' | 'gamma3' | 'gamma4' | 'gamma5' | 'gamma6' | 'gamma7' | 'gamma8';
export type Timing = 'together' | 'split';
export type Direction = 'same' | 'opp';

// Core interfaces matching Pydantic models exactly

/**
 * Motion data with camelCase JSON serialization
 * Matches: MotionData from pydantic_models.py
 */
export interface MotionData {
  motionType: MotionType;
  propRotDir: PropRotDir;
  startLoc: Location;
  endLoc: Location;
  turns: number;
  startOri: Orientation;
  endOri: Orientation;
}

/**
 * Pictograph data with camelCase JSON serialization
 * Matches: PictographData from pydantic_models.py
 */
export interface PictographData {
  gridMode: GridMode;
  grid: string;
  letter?: string | null;
  startPos?: StartEndPos | null;
  endPos?: StartEndPos | null;
  timing?: Timing | null;
  direction?: Direction | null;
  isStartPosition?: boolean | null;
  gridData?: Record<string, any> | null;
}

/**
 * Beat data with camelCase JSON serialization
 * Matches: BeatData from pydantic_models.py
 */
export interface BeatData {
  beatNumber: number;
  letter: string;
  duration: number;
  blueMotion: MotionData;
  redMotion: MotionData;
  pictographData?: PictographData | null;
  blueReversal: boolean;
  redReversal: boolean;
  filled: boolean;
  tags: string[];
  glyphData?: Record<string, any> | null;
}

/**
 * Sequence data with camelCase JSON serialization
 * Matches: SequenceData from pydantic_models.py
 */
export interface SequenceData {
  name: string;
  beats: BeatData[];
  createdAt?: string | null;
  updatedAt?: string | null;
  version: string;
  length: number;
  difficulty?: string | null;
  tags: string[];
}

// Factory function types (to be implemented)
export interface MotionDataFactory {
  createDefault(overrides?: Partial<MotionData>): MotionData;
  fromJson(json: Record<string, any>): MotionData;
  validate(data: unknown): data is MotionData;
}

export interface BeatDataFactory {
  createDefault(beatNumber: number, letter: string, overrides?: Partial<BeatData>): BeatData;
  fromJson(json: Record<string, any>): BeatData;
  validate(data: unknown): data is BeatData;
}

export interface SequenceDataFactory {
  createDefault(name: string, length?: number): SequenceData;
  fromJson(json: Record<string, any>): SequenceData;
  validate(data: unknown): data is SequenceData;
  addBeat(sequence: SequenceData, beat: BeatData): SequenceData;
  updateBeat(sequence: SequenceData, index: number, beat: BeatData): SequenceData;
}

// Utility types for immutable updates
export type MotionDataUpdate = Partial<MotionData>;
export type BeatDataUpdate = Partial<BeatData>;
export type SequenceDataUpdate = Partial<SequenceData>;

// Legacy compatibility (for gradual migration)
export interface LegacyMotionData {
  // Old snake_case format for backward compatibility
  motion_type: MotionType;
  prop_rot_dir: PropRotDir;
  start_loc: Location;
  end_loc: Location;
  turns: number;
  start_ori: Orientation;
  end_ori: Orientation;
}

// Conversion utilities
export interface DataConverter {
  motionToLegacy(motion: MotionData): LegacyMotionData;
  motionFromLegacy(legacy: LegacyMotionData): MotionData;
  beatToLegacy(beat: BeatData): any; // Legacy beat format
  beatFromLegacy(legacy: any): BeatData;
}
