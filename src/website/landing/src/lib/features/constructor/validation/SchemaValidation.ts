/**
 * Runtime Schema Validation for Web App
 *
 * Provides runtime validation against the JSON schemas to ensure
 * data compatibility between Python backend and TypeScript frontend.
 */

// For now, we'll use a lightweight validation approach
// In production, you might want to use a library like Ajv for full JSON Schema validation

import type { MotionData, BeatData, SequenceData } from '../types/GeneratedTypes.js';

// Motion data validation (matches motion-data-v2.json schema)
export function validateMotionData(data: unknown): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (typeof data !== 'object' || data === null) {
    return { valid: false, errors: ['Data must be an object'] };
  }

  const obj = data as Record<string, unknown>;

  // Required fields validation
  const requiredFields = ['motionType', 'propRotDir', 'startLoc', 'endLoc', 'turns', 'startOri', 'endOri'];
  for (const field of requiredFields) {
    if (!(field in obj)) {
      errors.push(`Missing required field: ${field}`);
    }
  }

  // Enum validations
  const validMotionTypes = ['pro', 'anti', 'float', 'dash', 'static'];
  if (obj.motionType && !validMotionTypes.includes(obj.motionType as string)) {
    errors.push(`Invalid motionType: ${obj.motionType}. Must be one of: ${validMotionTypes.join(', ')}`);
  }

  const validPropRotDirs = ['cw', 'ccw', 'no_rot'];
  if (obj.propRotDir && !validPropRotDirs.includes(obj.propRotDir as string)) {
    errors.push(`Invalid propRotDir: ${obj.propRotDir}. Must be one of: ${validPropRotDirs.join(', ')}`);
  }

  const validLocations = ['n', 'e', 's', 'w', 'ne', 'nw', 'se', 'sw'];
  if (obj.startLoc && !validLocations.includes(obj.startLoc as string)) {
    errors.push(`Invalid startLoc: ${obj.startLoc}. Must be one of: ${validLocations.join(', ')}`);
  }
  if (obj.endLoc && !validLocations.includes(obj.endLoc as string)) {
    errors.push(`Invalid endLoc: ${obj.endLoc}. Must be one of: ${validLocations.join(', ')}`);
  }

  const validOrientations = ['in', 'out', 'clock', 'counter'];
  if (obj.startOri && !validOrientations.includes(obj.startOri as string)) {
    errors.push(`Invalid startOri: ${obj.startOri}. Must be one of: ${validOrientations.join(', ')}`);
  }
  if (obj.endOri && !validOrientations.includes(obj.endOri as string)) {
    errors.push(`Invalid endOri: ${obj.endOri}. Must be one of: ${validOrientations.join(', ')}`);
  }

  // Type validations
  if (obj.turns !== undefined && (typeof obj.turns !== 'number' || obj.turns < 0)) {
    errors.push(`Invalid turns: ${obj.turns}. Must be a non-negative number`);
  }

  return { valid: errors.length === 0, errors };
}

// Beat data validation (matches beat-data-v2.json schema)
export function validateBeatData(data: unknown): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (typeof data !== 'object' || data === null) {
    return { valid: false, errors: ['Data must be an object'] };
  }

  const obj = data as Record<string, unknown>;

  // Required fields
  if (typeof obj.beatNumber !== 'number' || obj.beatNumber < 0) {
    errors.push(`Invalid beatNumber: ${obj.beatNumber}. Must be a non-negative number`);
  }

  if (typeof obj.letter !== 'string' || obj.letter.length === 0) {
    errors.push(`Invalid letter: ${obj.letter}. Must be a non-empty string`);
  }

  // Optional but validated fields
  if (obj.duration !== undefined && (typeof obj.duration !== 'number' || obj.duration <= 0)) {
    errors.push(`Invalid duration: ${obj.duration}. Must be a positive number`);
  }

  // Validate nested motion data
  if (obj.blueMotion) {
    const blueMotionResult = validateMotionData(obj.blueMotion);
    if (!blueMotionResult.valid) {
      errors.push(...blueMotionResult.errors.map(e => `blueMotion.${e}`));
    }
  }

  if (obj.redMotion) {
    const redMotionResult = validateMotionData(obj.redMotion);
    if (!redMotionResult.valid) {
      errors.push(...redMotionResult.errors.map(e => `redMotion.${e}`));
    }
  }

  // Boolean fields
  if (obj.blueReversal !== undefined && typeof obj.blueReversal !== 'boolean') {
    errors.push(`Invalid blueReversal: ${obj.blueReversal}. Must be a boolean`);
  }
  if (obj.redReversal !== undefined && typeof obj.redReversal !== 'boolean') {
    errors.push(`Invalid redReversal: ${obj.redReversal}. Must be a boolean`);
  }
  if (obj.filled !== undefined && typeof obj.filled !== 'boolean') {
    errors.push(`Invalid filled: ${obj.filled}. Must be a boolean`);
  }

  // Array fields
  if (obj.tags !== undefined && !Array.isArray(obj.tags)) {
    errors.push(`Invalid tags: ${obj.tags}. Must be an array`);
  }

  return { valid: errors.length === 0, errors };
}

// Sequence data validation (matches sequence-data-v2.json schema)
export function validateSequenceData(data: unknown): { valid: boolean; errors: string[] } {
  const errors: string[] = [];

  if (typeof data !== 'object' || data === null) {
    return { valid: false, errors: ['Data must be an object'] };
  }

  const obj = data as Record<string, unknown>;

  // Required fields
  if (typeof obj.name !== 'string' || obj.name.length === 0) {
    errors.push(`Invalid name: ${obj.name}. Must be a non-empty string`);
  }

  if (!Array.isArray(obj.beats)) {
    errors.push(`Invalid beats: ${obj.beats}. Must be an array`);
  } else {
    // Validate each beat
    obj.beats.forEach((beat, index) => {
      const beatResult = validateBeatData(beat);
      if (!beatResult.valid) {
        errors.push(...beatResult.errors.map(e => `beats[${index}].${e}`));
      }
    });
  }

  // Optional but validated fields
  if (obj.length !== undefined && (typeof obj.length !== 'number' || obj.length < 1)) {
    errors.push(`Invalid length: ${obj.length}. Must be a positive number`);
  }

  if (obj.version !== undefined && typeof obj.version !== 'string') {
    errors.push(`Invalid version: ${obj.version}. Must be a string`);
  }

  if (obj.tags !== undefined && !Array.isArray(obj.tags)) {
    errors.push(`Invalid tags: ${obj.tags}. Must be an array`);
  }

  return { valid: errors.length === 0, errors };
}

// Validation utilities
export function assertValidMotionData(data: unknown): asserts data is MotionData {
  const result = validateMotionData(data);
  if (!result.valid) {
    throw new Error(`Invalid MotionData: ${result.errors.join(', ')}`);
  }
}

export function assertValidBeatData(data: unknown): asserts data is BeatData {
  const result = validateBeatData(data);
  if (!result.valid) {
    throw new Error(`Invalid BeatData: ${result.errors.join(', ')}`);
  }
}

export function assertValidSequenceData(data: unknown): asserts data is SequenceData {
  const result = validateSequenceData(data);
  if (!result.valid) {
    throw new Error(`Invalid SequenceData: ${result.errors.join(', ')}`);
  }
}

// Type guards
export function isValidMotionData(data: unknown): data is MotionData {
  return validateMotionData(data).valid;
}

export function isValidBeatData(data: unknown): data is BeatData {
  return validateBeatData(data).valid;
}

export function isValidSequenceData(data: unknown): data is SequenceData {
  return validateSequenceData(data).valid;
}

// Cross-platform compatibility helpers
export function validateDataFromPython(data: unknown, expectedType: 'motion' | 'beat' | 'sequence'): { valid: boolean; errors: string[] } {
  switch (expectedType) {
    case 'motion':
      return validateMotionData(data);
    case 'beat':
      return validateBeatData(data);
    case 'sequence':
      return validateSequenceData(data);
    default:
      return { valid: false, errors: [`Unknown data type: ${expectedType}`] };
  }
}
