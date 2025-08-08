/**
 * Data Factories v2
 *
 * Factory functions that match the behavior of Python Pydantic models.
 * These provide immutable data creation and validation.
 */

import type {
  MotionData,
  BeatData,
  SequenceData,
  PictographData,
  MotionType,
  PropRotDir,
  Location,
  Orientation,
  GridMode,
  MotionDataFactory,
  BeatDataFactory,
  SequenceDataFactory,
  MotionDataUpdate,
  BeatDataUpdate,
  SequenceDataUpdate
} from '../types/GeneratedTypes.js';

// Runtime validation helpers
function isValidMotionType(value: unknown): value is MotionType {
  return typeof value === 'string' &&
    ['pro', 'anti', 'float', 'dash', 'static'].includes(value);
}

function isValidPropRotDir(value: unknown): value is PropRotDir {
  return typeof value === 'string' &&
    ['cw', 'ccw', 'no_rot'].includes(value);
}

function isValidLocation(value: unknown): value is Location {
  return typeof value === 'string' &&
    ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'].includes(value);
}

function isValidOrientation(value: unknown): value is Orientation {
  return typeof value === 'string' &&
    ['in', 'out', 'clock', 'counter'].includes(value);
}

// MotionData Factory (matches create_default_motion_data)
export const createMotionDataFactory = (): MotionDataFactory => ({
  createDefault: (overrides: Partial<MotionData> = {}): MotionData => {
    const defaults: MotionData = {
      motionType: 'pro',
      propRotDir: 'cw',
      startLoc: 'n',
      endLoc: 'e',
      turns: 0.0,
      startOri: 'in',
      endOri: 'in'
    };

    return { ...defaults, ...overrides };
  },

  fromJson: (json: Record<string, any>): MotionData => {
    // Validate required fields
    if (!isValidMotionType(json.motionType)) {
      throw new Error(`Invalid motionType: ${json.motionType}`);
    }
    if (!isValidPropRotDir(json.propRotDir)) {
      throw new Error(`Invalid propRotDir: ${json.propRotDir}`);
    }
    if (!isValidLocation(json.startLoc)) {
      throw new Error(`Invalid startLoc: ${json.startLoc}`);
    }
    if (!isValidLocation(json.endLoc)) {
      throw new Error(`Invalid endLoc: ${json.endLoc}`);
    }
    if (!isValidOrientation(json.startOri)) {
      throw new Error(`Invalid startOri: ${json.startOri}`);
    }
    if (!isValidOrientation(json.endOri)) {
      throw new Error(`Invalid endOri: ${json.endOri}`);
    }

    return {
      motionType: json.motionType,
      propRotDir: json.propRotDir,
      startLoc: json.startLoc,
      endLoc: json.endLoc,
      turns: typeof json.turns === 'number' ? json.turns : 0.0,
      startOri: json.startOri,
      endOri: json.endOri
    };
  },

  validate: (data: unknown): data is MotionData => {
    if (typeof data !== 'object' || data === null) return false;

    const obj = data as Record<string, unknown>;

    return isValidMotionType(obj.motionType) &&
           isValidPropRotDir(obj.propRotDir) &&
           isValidLocation(obj.startLoc) &&
           isValidLocation(obj.endLoc) &&
           typeof obj.turns === 'number' &&
           isValidOrientation(obj.startOri) &&
           isValidOrientation(obj.endOri);
  }
});

// BeatData Factory (matches create_default_beat_data)
export const createBeatDataFactory = (): BeatDataFactory => {
  const motionFactory = createMotionDataFactory();

  return {
    createDefault: (beatNumber: number, letter: string, overrides: Partial<BeatData> = {}): BeatData => {
      if (beatNumber < 0) {
        throw new Error('Beat number must be non-negative');
      }
      if (!letter || typeof letter !== 'string') {
        throw new Error('Letter must be a non-empty string');
      }

      const defaults: BeatData = {
        beatNumber,
        letter,
        duration: 1.0,
        blueMotion: motionFactory.createDefault(),
        redMotion: motionFactory.createDefault(),
        pictographData: null,
        blueReversal: false,
        redReversal: false,
        filled: false,
        tags: [],
        glyphData: null
      };

      return { ...defaults, ...overrides };
    },

    fromJson: (json: Record<string, any>): BeatData => {
      if (typeof json.beatNumber !== 'number' || json.beatNumber < 0) {
        throw new Error(`Invalid beatNumber: ${json.beatNumber}`);
      }
      if (typeof json.letter !== 'string' || !json.letter) {
        throw new Error(`Invalid letter: ${json.letter}`);
      }

      return {
        beatNumber: json.beatNumber,
        letter: json.letter,
        duration: typeof json.duration === 'number' && json.duration > 0 ? json.duration : 1.0,
        blueMotion: motionFactory.fromJson(json.blueMotion || {}),
        redMotion: motionFactory.fromJson(json.redMotion || {}),
        pictographData: json.pictographData || null,
        blueReversal: Boolean(json.blueReversal),
        redReversal: Boolean(json.redReversal),
        filled: Boolean(json.filled),
        tags: Array.isArray(json.tags) ? json.tags : [],
        glyphData: json.glyphData || null
      };
    },

    validate: (data: unknown): data is BeatData => {
      if (typeof data !== 'object' || data === null) return false;

      const obj = data as Record<string, unknown>;
      const motionFactory = createMotionDataFactory();

      return typeof obj.beatNumber === 'number' &&
             obj.beatNumber >= 0 &&
             typeof obj.letter === 'string' &&
             obj.letter.length > 0 &&
             typeof obj.duration === 'number' &&
             obj.duration > 0 &&
             motionFactory.validate(obj.blueMotion) &&
             motionFactory.validate(obj.redMotion) &&
             typeof obj.blueReversal === 'boolean' &&
             typeof obj.redReversal === 'boolean' &&
             typeof obj.filled === 'boolean' &&
             Array.isArray(obj.tags);
    }
  };
};

// SequenceData Factory (matches create_default_sequence_data)
export const createSequenceDataFactory = (): SequenceDataFactory => {
  const beatFactory = createBeatDataFactory();

  return {
    createDefault: (name: string, length: number = 8): SequenceData => {
      if (!name || typeof name !== 'string') {
        throw new Error('Name must be a non-empty string');
      }
      if (typeof length !== 'number' || length < 1) {
        throw new Error('Length must be a positive number');
      }

      return {
        name,
        beats: [],
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        version: '2.0',
        length,
        difficulty: null,
        tags: []
      };
    },

    fromJson: (json: Record<string, any>): SequenceData => {
      if (typeof json.name !== 'string' || !json.name) {
        throw new Error(`Invalid name: ${json.name}`);
      }

      const beats = Array.isArray(json.beats)
        ? json.beats.map(beatData => beatFactory.fromJson(beatData))
        : [];

      return {
        name: json.name,
        beats,
        createdAt: json.createdAt || null,
        updatedAt: json.updatedAt || null,
        version: json.version || '2.0',
        length: typeof json.length === 'number' && json.length >= 1 ? json.length : 8,
        difficulty: json.difficulty || null,
        tags: Array.isArray(json.tags) ? json.tags : []
      };
    },

    validate: (data: unknown): data is SequenceData => {
      if (typeof data !== 'object' || data === null) return false;

      const obj = data as Record<string, unknown>;

      return typeof obj.name === 'string' &&
             obj.name.length > 0 &&
             Array.isArray(obj.beats) &&
             obj.beats.every(beat => beatFactory.validate(beat)) &&
             typeof obj.version === 'string' &&
             typeof obj.length === 'number' &&
             obj.length >= 1 &&
             Array.isArray(obj.tags);
    },

    // Immutable operations (matching Python behavior)
    addBeat: (sequence: SequenceData, beat: BeatData): SequenceData => {
      return {
        ...sequence,
        beats: [...sequence.beats, beat],
        updatedAt: new Date().toISOString()
      };
    },

    updateBeat: (sequence: SequenceData, index: number, beat: BeatData): SequenceData => {
      if (index < 0 || index >= sequence.beats.length) {
        throw new Error(`Invalid beat index: ${index}`);
      }

      const newBeats = [...sequence.beats];
      newBeats[index] = beat;

      return {
        ...sequence,
        beats: newBeats,
        updatedAt: new Date().toISOString()
      };
    }
  };
};

// Convenience exports (matching Python create_default_* functions)
export const createDefaultMotionData = createMotionDataFactory().createDefault;
export const createDefaultBeatData = createBeatDataFactory().createDefault;
export const createDefaultSequenceData = createSequenceDataFactory().createDefault;

// Factory instances
export const motionDataFactory = createMotionDataFactory();
export const beatDataFactory = createBeatDataFactory();
export const sequenceDataFactory = createSequenceDataFactory();

// Update utilities for immutable operations
export function updateMotionData(motion: MotionData, updates: MotionDataUpdate): MotionData {
  return { ...motion, ...updates };
}

export function updateBeatData(beat: BeatData, updates: BeatDataUpdate): BeatData {
  return { ...beat, ...updates };
}

export function updateSequenceData(sequence: SequenceData, updates: SequenceDataUpdate): SequenceData {
  return {
    ...sequence,
    ...updates,
    updatedAt: new Date().toISOString()
  };
}
