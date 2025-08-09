import { g as generatorStore, d as determineRotationDirection } from "./rotationDeterminer.js";
const VALID_LETTER_TYPES = ["type1", "type2", "type3", "type4"];
const VALID_ORIENTATIONS = ["in", "out", "cw", "ccw"];
const VALID_POSITIONS = [
  "alpha1_alpha1",
  "alpha2_alpha2",
  "beta4_beta4",
  "beta5_beta5",
  "gamma11_gamma11",
  "gamma12_gamma12"
];
function validateFreeformSequence(sequence, selectedLetterTypes) {
  const validators = [
    validateSequenceLength,
    validateLetterTypeCompatibility,
    validateOrientations,
    validatePositions,
    validateTurnIntensity
  ];
  const errors = [];
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
function validateSequenceLength(sequence, selectedLetterTypes) {
  const errors = [];
  if (!sequence || sequence.length === 0) {
    errors.push("Sequence cannot be empty");
  }
  if (sequence.length < 4) {
    errors.push("Sequence must have at least 4 beats");
  }
  if (sequence.length > 64) {
    errors.push("Sequence cannot exceed 64 beats");
  }
  return { isValid: errors.length === 0, errors };
}
function validateLetterTypeCompatibility(sequence, selectedLetterTypes) {
  const errors = [];
  const validTypes = selectedLetterTypes.length > 0 ? selectedLetterTypes : VALID_LETTER_TYPES;
  for (const [index, beat] of sequence.entries()) {
    if (!validTypes.includes(beat.letterType)) {
      errors.push(`Beat ${index} has incompatible letter type: ${beat.letterType}`);
    }
  }
  return { isValid: errors.length === 0, errors };
}
function validateOrientations(sequence, selectedLetterTypes) {
  const errors = [];
  for (const [index, beat] of sequence.entries()) {
    if (!VALID_ORIENTATIONS.includes(beat.orientation.blue)) {
      errors.push(`Invalid blue orientation at beat ${index}: ${beat.orientation.blue}`);
    }
    if (!VALID_ORIENTATIONS.includes(beat.orientation.red)) {
      errors.push(`Invalid red orientation at beat ${index}: ${beat.orientation.red}`);
    }
  }
  return { isValid: errors.length === 0, errors };
}
function validatePositions(sequence, selectedLetterTypes) {
  const errors = [];
  const positions = new Set(sequence.map((beat) => beat.position));
  if (positions.size < 2) {
    errors.push("Sequence must have at least 2 unique positions");
  }
  for (const [index, beat] of sequence.entries()) {
    if (!VALID_POSITIONS.includes(beat.position)) {
      errors.push(`Invalid position at beat ${index}: ${beat.position}`);
    }
  }
  return { isValid: errors.length === 0, errors };
}
function validateTurnIntensity(sequence, selectedLetterTypes) {
  const errors = [];
  for (const [index, beat] of sequence.entries()) {
    if (beat.turnIntensity < 0 || beat.turnIntensity > 3) {
      errors.push(`Invalid turn intensity at beat ${index}: ${beat.turnIntensity}`);
    }
  }
  return { isValid: errors.length === 0, errors };
}
function generateOrientations() {
  const orientations = ["north", "east", "south", "west"];
  const blueOrientation = orientations[Math.floor(Math.random() * orientations.length)];
  const redOrientation = orientations[Math.floor(Math.random() * orientations.length)];
  return { blue: blueOrientation, red: redOrientation };
}
function mapPositions(beatIndex) {
  const positions = ["alpha1", "beta3", "gamma5"];
  return positions[beatIndex % positions.length];
}
async function createFreeformSequence(options) {
  try {
    generatorStore.startGeneration();
    generatorStore.updateProgress(10, "Initializing freeform sequence generation");
    const rotationDirection = determineRotationDirection(options.propContinuity);
    generatorStore.updateProgress(30, "Generating base sequence");
    const baseSequence = generateBaseSequence(options);
    generatorStore.updateProgress(70, "Validating sequence");
    const validationResult = validateFreeformSequence(
      baseSequence,
      options.letterTypes || []
      // Pass letterTypes array instead of capType
    );
    if (!validationResult.isValid) {
      throw new Error(validationResult.errors.join("; "));
    }
    generatorStore.updateProgress(90, "Finalizing sequence");
    const finalSequence = postProcessSequence(baseSequence);
    generatorStore.completeGeneration();
    return finalSequence;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "Failed to generate freeform sequence";
    generatorStore.setError(errorMessage);
    throw error;
  }
}
function generateBaseSequence(options) {
  const sequence = [];
  for (let i = 0; i < options.numBeats; i++) {
    const beat = generateSingleBeat(options, i);
    sequence.push(beat);
  }
  return sequence;
}
function generateSingleBeat(options, beatIndex) {
  return {
    beat: beatIndex,
    turnIntensity: calculateTurnIntensity(options.turnIntensity),
    orientation: generateOrientations(),
    position: mapPositions(beatIndex),
    letterType: selectLetterType(options.letterTypes || [])
  };
}
function calculateTurnIntensity(baseTurnIntensity) {
  const variation = Math.random() * 0.5 - 0.25;
  return Math.max(0, baseTurnIntensity + variation);
}
function selectLetterType(letterTypes) {
  if (letterTypes.length === 0) {
    const allTypes = ["type1", "type2", "type3", "type4"];
    return allTypes[Math.floor(Math.random() * allTypes.length)];
  }
  return letterTypes[Math.floor(Math.random() * letterTypes.length)];
}
function postProcessSequence(sequence) {
  return sequence.map((beat) => ({
    ...beat,
    finalOrientation: normalizeOrientation(beat.orientation)
  }));
}
function normalizeOrientation(orientation) {
  return orientation;
}
export {
  createFreeformSequence
};
