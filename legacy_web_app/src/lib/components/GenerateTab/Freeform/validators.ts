export interface ValidationResult {
    isValid: boolean;
    errors: string[];
  }

  export interface BeatData {
    beat: number;
    turnIntensity: number;
    orientation: {
      blue: string;
      red: string;
    };
    position: string;
    letterType: string;
  }

  const VALID_LETTER_TYPES = ['type1', 'type2', 'type3', 'type4'];
  const VALID_ORIENTATIONS = ['in', 'out', 'cw', 'ccw'];
  const VALID_POSITIONS = [
    'alpha1_alpha1', 'alpha2_alpha2',
    'beta4_beta4', 'beta5_beta5',
    'gamma11_gamma11', 'gamma12_gamma12'
  ];

  export function validateFreeformSequence(
    sequence: BeatData[],
    selectedLetterTypes: string[]
  ): ValidationResult {
    const validators: Array<(seq: BeatData[], types: string[]) => ValidationResult> = [
      validateSequenceLength,
      validateLetterTypeCompatibility,
      validateOrientations,
      validatePositions,
      validateTurnIntensity
    ];

    const errors: string[] = [];

    for (const validator of validators) {
      const result = validator(sequence, selectedLetterTypes);
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
    sequence: BeatData[],
    selectedLetterTypes: string[]
  ): ValidationResult {
    const errors: string[] = [];

    if (!sequence || sequence.length === 0) {
      errors.push('Sequence cannot be empty');
    }

    if (sequence.length < 4) {
      errors.push('Sequence must have at least 4 beats');
    }

    if (sequence.length > 64) {
      errors.push('Sequence cannot exceed 64 beats');
    }

    return { isValid: errors.length === 0, errors };
  }

  function validateLetterTypeCompatibility(
    sequence: BeatData[],
    selectedLetterTypes: string[]
  ): ValidationResult {
    const errors: string[] = [];

    // If no specific types selected, consider all types valid
    const validTypes = selectedLetterTypes.length > 0
      ? selectedLetterTypes
      : VALID_LETTER_TYPES;

    // Validate letter types
    for (const [index, beat] of sequence.entries()) {
      if (!validTypes.includes(beat.letterType)) {
        errors.push(`Beat ${index} has incompatible letter type: ${beat.letterType}`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }

  function validateOrientations(
    sequence: BeatData[],
    selectedLetterTypes: string[]
  ): ValidationResult {
    const errors: string[] = [];

    for (const [index, beat] of sequence.entries()) {
      // Validate blue orientation
      if (!VALID_ORIENTATIONS.includes(beat.orientation.blue)) {
        errors.push(`Invalid blue orientation at beat ${index}: ${beat.orientation.blue}`);
      }

      // Validate red orientation
      if (!VALID_ORIENTATIONS.includes(beat.orientation.red)) {
        errors.push(`Invalid red orientation at beat ${index}: ${beat.orientation.red}`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }

  function validatePositions(
    sequence: BeatData[],
    selectedLetterTypes: string[]
  ): ValidationResult {
    const errors: string[] = [];
    const positions = new Set(sequence.map(beat => beat.position));

    if (positions.size < 2) {
      errors.push('Sequence must have at least 2 unique positions');
    }

    // Validate each position is valid
    for (const [index, beat] of sequence.entries()) {
      if (!VALID_POSITIONS.includes(beat.position)) {
        errors.push(`Invalid position at beat ${index}: ${beat.position}`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }

  function validateTurnIntensity(
    sequence: BeatData[],
    selectedLetterTypes: string[]
  ): ValidationResult {
    const errors: string[] = [];

    for (const [index, beat] of sequence.entries()) {
      if (beat.turnIntensity < 0 || beat.turnIntensity > 3) {
        errors.push(`Invalid turn intensity at beat ${index}: ${beat.turnIntensity}`);
      }
    }

    return { isValid: errors.length === 0, errors };
  }

  export const freeformValidators = {
    validateFreeformSequence,
    validateLetterTypeCompatibility,
    validateOrientations,
    validatePositions,
    validateTurnIntensity
  };
