import type { CAPType } from '../store/settings';

export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export function validateCircularSequence(
  sequence: any[],
  capType: CAPType
): ValidationResult {
  const validators = [
    validateSequenceLength,
    validateCAPCompatibility,
    validateOrientations,
    validatePositions
  ];

  const errors: string[] = [];

  for (const validator of validators) {
    const result = validator(sequence, capType);
    if (!result.isValid) {
      errors.push(...result.errors);
    }
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function validateSequenceLength(
  sequence: any[],
  capType: CAPType
): ValidationResult {
  const errors: string[] = [];

  if (!sequence || sequence.length === 0) {
    errors.push('Sequence cannot be empty');
  }

  const expectedLengthMultiple = getExpectedLengthMultiple(capType);
  if (sequence.length % expectedLengthMultiple !== 0) {
    errors.push(`Sequence length must be divisible by ${expectedLengthMultiple} for ${capType}`);
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function validateCAPCompatibility(
  sequence: any[],
  capType: CAPType
): ValidationResult {
  const errors: string[] = [];

  // Add specific CAP type validation logic
  switch (capType) {
    case 'mirrored':
      if (!isSymmetric(sequence)) {
        errors.push('Mirrored sequence must have symmetric characteristics');
      }
      break;
    case 'rotated':
      if (!isRotationCompatible(sequence)) {
        errors.push('Rotated sequence must have rotational symmetry');
      }
      break;
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function validateOrientations(
  sequence: any[],
  capType: CAPType
): ValidationResult {
  const errors: string[] = [];

  for (const beat of sequence) {
    if (!isValidOrientation(beat.orientation)) {
      errors.push(`Invalid orientation: ${JSON.stringify(beat.orientation)}`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function validatePositions(
  sequence: any[],
  capType: CAPType
): ValidationResult {
  const errors: string[] = [];
  const positions = new Set(sequence.map(beat => beat.position));

  if (positions.size < 2) {
    errors.push('Sequence must have varied positions');
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

function getExpectedLengthMultiple(capType: CAPType): number {
  const multiplierMap: Record<CAPType, number> = {
    'mirrored': 2,
    'rotated': 2,
    'mirrored_complementary': 2,
    'rotated_complementary': 2,
    'mirrored_swapped': 2,
    'rotated_swapped': 2,
    'strict_mirrored': 2,
    'strict_rotated': 2,
    'strict_complementary': 2,
    'strict_swapped': 2,
    'swapped_complementary': 2
  };
  return multiplierMap[capType] || 2;
}

function isSymmetric(sequence: any[]): boolean {
  // Implement symmetric check logic
  return true; // Placeholder
}

function isRotationCompatible(sequence: any[]): boolean {
  // Implement rotation compatibility check logic
  return true; // Placeholder
}

function isValidOrientation(orientation: any): boolean {
  return orientation &&
         typeof orientation === 'object' &&
         'blue' in orientation &&
         'red' in orientation;
}

export const circularValidators = {
  validateCircularSequence,
  validateCAPCompatibility,
  validateOrientations,
  validatePositions
};
