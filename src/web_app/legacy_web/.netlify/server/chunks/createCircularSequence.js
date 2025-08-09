import { g as generatorStore, d as determineRotationDirection } from "./rotationDeterminer.js";
const capExecutors = {
  mirrored: mirroredExecutor,
  rotated: rotatedExecutor,
  "mirrored_complementary": mirroredComplementaryExecutor,
  "rotated_complementary": rotatedComplementaryExecutor,
  "mirrored_swapped": mirroredSwappedExecutor,
  "rotated_swapped": rotatedSwappedExecutor,
  "strict_mirrored": strictMirroredExecutor,
  "strict_rotated": strictRotatedExecutor,
  "strict_complementary": strictComplementaryExecutor,
  "strict_swapped": strictSwappedExecutor,
  "swapped_complementary": swappedComplementaryExecutor
};
function mirroredExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const mirroredHalf = sequence.slice(0, halfLength).map(mirrorBeat);
  return [...sequence, ...mirroredHalf];
}
function rotatedExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const rotatedHalf = sequence.slice(0, halfLength).map(rotateBeat);
  return [...sequence, ...rotatedHalf];
}
function mirroredComplementaryExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const complementaryHalf = sequence.slice(0, halfLength).map(complementaryBeat);
  return [...sequence, ...complementaryHalf];
}
function rotatedComplementaryExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const rotatedComplementaryHalf = sequence.slice(0, halfLength).map(rotateComplementaryBeat);
  return [...sequence, ...rotatedComplementaryHalf];
}
function mirroredSwappedExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const swappedMirroredHalf = sequence.slice(0, halfLength).map(swapAndMirrorBeat);
  return [...sequence, ...swappedMirroredHalf];
}
function rotatedSwappedExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const swappedRotatedHalf = sequence.slice(0, halfLength).map(swapAndRotateBeat);
  return [...sequence, ...swappedRotatedHalf];
}
function strictMirroredExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const strictMirroredHalf = sequence.slice(0, halfLength).map(strictMirrorBeat);
  return [...sequence, ...strictMirroredHalf];
}
function strictRotatedExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const strictRotatedHalf = sequence.slice(0, halfLength).map(strictRotateBeat);
  return [...sequence, ...strictRotatedHalf];
}
function strictComplementaryExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const strictComplementaryHalf = sequence.slice(0, halfLength).map(strictComplementaryBeat);
  return [...sequence, ...strictComplementaryHalf];
}
function strictSwappedExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const strictSwappedHalf = sequence.slice(0, halfLength).map(strictSwapBeat);
  return [...sequence, ...strictSwappedHalf];
}
function swappedComplementaryExecutor(sequence) {
  const halfLength = Math.floor(sequence.length / 2);
  const swappedComplementaryHalf = sequence.slice(0, halfLength).map(swapComplementaryBeat);
  return [...sequence, ...swappedComplementaryHalf];
}
function mirrorBeat(beat) {
  return {
    ...beat,
    orientation: mirrorOrientation(beat.orientation),
    position: mirrorPosition(beat.position)
  };
}
function rotateBeat(beat) {
  return {
    ...beat,
    orientation: rotateOrientation(beat.orientation),
    position: rotatePosition(beat.position)
  };
}
function complementaryBeat(beat) {
  return {
    ...beat,
    orientation: complementOrientation(beat.orientation)
  };
}
function rotateComplementaryBeat(beat) {
  return {
    ...beat,
    orientation: rotateComplementOrientation(beat.orientation),
    position: rotatePosition(beat.position)
  };
}
function swapAndMirrorBeat(beat) {
  return {
    ...beat,
    orientation: swapAndMirrorOrientation(beat.orientation),
    position: mirrorPosition(beat.position)
  };
}
function swapAndRotateBeat(beat) {
  return {
    ...beat,
    orientation: swapAndRotateOrientation(beat.orientation),
    position: rotatePosition(beat.position)
  };
}
function strictMirrorBeat(beat) {
  return mirrorBeat(beat);
}
function strictRotateBeat(beat) {
  return rotateBeat(beat);
}
function strictComplementaryBeat(beat) {
  return complementaryBeat(beat);
}
function strictSwapBeat(beat) {
  return {
    ...beat,
    orientation: swapOrientation(beat.orientation)
  };
}
function swapComplementaryBeat(beat) {
  return {
    ...beat,
    orientation: swapComplementOrientation(beat.orientation)
  };
}
function mirrorOrientation(orientation) {
  return orientation;
}
function mirrorPosition(position) {
  return position;
}
function rotateOrientation(orientation) {
  return orientation;
}
function rotatePosition(position) {
  return position;
}
function complementOrientation(orientation) {
  return orientation;
}
function rotateComplementOrientation(orientation) {
  return orientation;
}
function swapAndMirrorOrientation(orientation) {
  return orientation;
}
function swapAndRotateOrientation(orientation) {
  return orientation;
}
function swapOrientation(orientation) {
  return orientation;
}
function swapComplementOrientation(orientation) {
  return orientation;
}
function validateCircularSequence(sequence, capType) {
  const validators = [
    validateSequenceLength,
    validateCAPCompatibility,
    validateOrientations,
    validatePositions
  ];
  const errors = [];
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
function validateSequenceLength(sequence, capType) {
  const errors = [];
  if (!sequence || sequence.length === 0) {
    errors.push("Sequence cannot be empty");
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
function validateCAPCompatibility(sequence, capType) {
  const errors = [];
  return {
    isValid: errors.length === 0,
    errors
  };
}
function validateOrientations(sequence, capType) {
  const errors = [];
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
function validatePositions(sequence, capType) {
  const errors = [];
  const positions = new Set(sequence.map((beat) => beat.position));
  if (positions.size < 2) {
    errors.push("Sequence must have varied positions");
  }
  return {
    isValid: errors.length === 0,
    errors
  };
}
function getExpectedLengthMultiple(capType) {
  const multiplierMap = {
    "mirrored": 2,
    "rotated": 2,
    "mirrored_complementary": 2,
    "rotated_complementary": 2,
    "mirrored_swapped": 2,
    "rotated_swapped": 2,
    "strict_mirrored": 2,
    "strict_rotated": 2,
    "strict_complementary": 2,
    "strict_swapped": 2,
    "swapped_complementary": 2
  };
  return multiplierMap[capType] || 2;
}
function isValidOrientation(orientation) {
  return orientation && typeof orientation === "object" && "blue" in orientation && "red" in orientation;
}
function generateOrientations() {
  const orientations = ["north", "east", "south", "west"];
  return orientations[Math.floor(Math.random() * orientations.length)];
}
function mapPositions(beatIndex) {
  const positions = ["alpha1", "beta3", "gamma5", "delta7"];
  return positions[beatIndex % positions.length];
}
async function createCircularSequence(options) {
  try {
    generatorStore.startGeneration();
    generatorStore.updateProgress(10, "Initializing sequence generation");
    const rotationDirection = determineRotationDirection(options.propContinuity);
    generatorStore.updateProgress(30, "Generating base sequence");
    const baseSequence = generateBaseSequence(options);
    generatorStore.updateProgress(50, "Applying CAP transformation");
    const transformedSequence = applyCAP(baseSequence, options.capType);
    generatorStore.updateProgress(70, "Validating sequence");
    const validationResult = validateCircularSequence(transformedSequence, options.capType);
    if (!validationResult.isValid) {
      throw new Error(validationResult.errors.join("; "));
    }
    generatorStore.updateProgress(90, "Finalizing sequence");
    const finalSequence = postProcessSequence(transformedSequence);
    generatorStore.completeGeneration();
    return finalSequence;
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "Failed to generate circular sequence";
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
    position: mapPositions(beatIndex)
  };
}
function calculateTurnIntensity(baseTurnIntensity) {
  const variation = Math.random() * 0.5 - 0.25;
  return Math.max(0, baseTurnIntensity + variation);
}
function applyCAP(sequence, capType) {
  const executor = capExecutors[capType];
  if (!executor) {
    throw new Error(`Unknown CAP type: ${capType}`);
  }
  return executor(sequence);
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
  createCircularSequence
};
