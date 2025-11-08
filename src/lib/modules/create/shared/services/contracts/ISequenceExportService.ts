/**
 * Service for exporting sequence data in various formats
 */
export interface ISequenceExportService {
  /**
   * Create a condensed, human-readable version of sequence data
   * Removes: IDs, placement data, metadata, redundant fields
   * Keeps: Essential motion data for reconstruction
   *
   * @param sequenceData - The full sequence data to condense
   * @returns Condensed sequence data suitable for sharing and debugging
   */
  createCondensedSequence(sequenceData: any): CondensedSequenceData;
}

/**
 * Condensed sequence data structure
 * Contains only essential information needed to reconstruct the sequence
 */
export interface CondensedSequenceData {
  word: string;
  startPosition?: CondensedStartPosition;
  beats: CondensedBeatData[];
}

/**
 * Condensed start position data
 */
export interface CondensedStartPosition {
  letter: string;
  gridPosition?: string;
  motions: {
    blue: CondensedStartMotion;
    red: CondensedStartMotion;
  };
}

/**
 * Condensed start motion data (location and orientation only)
 */
export interface CondensedStartMotion {
  startLocation: string;
  startOrientation: string;
}

/**
 * Condensed beat data
 */
export interface CondensedBeatData {
  letter: string;
  beatNumber: number;
  gridPosition?: string;
  duration: number;
  blueReversal: boolean;
  redReversal: boolean;
  motions: {
    blue: CondensedMotionData;
    red: CondensedMotionData;
  };
}

/**
 * Condensed motion data (essential fields only)
 */
export interface CondensedMotionData {
  motionType: string;
  rotationDirection: string;
  startLocation: string;
  endLocation: string;
  turns: number;
  startOrientation: string;
  endOrientation: string;
}
