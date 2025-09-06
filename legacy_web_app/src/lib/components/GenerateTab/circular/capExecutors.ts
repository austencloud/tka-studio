type Sequence = any[];

interface CAPExecutor {
  (sequence: Sequence): Sequence;
}

export const capExecutors: Record<string, CAPExecutor> = {
  mirrored: mirroredExecutor,
  rotated: rotatedExecutor,
  'mirrored_complementary': mirroredComplementaryExecutor,
  'rotated_complementary': rotatedComplementaryExecutor,
  'mirrored_swapped': mirroredSwappedExecutor,
  'rotated_swapped': rotatedSwappedExecutor,
  'strict_mirrored': strictMirroredExecutor,
  'strict_rotated': strictRotatedExecutor,
  'strict_complementary': strictComplementaryExecutor,
  'strict_swapped': strictSwappedExecutor,
  'swapped_complementary': swappedComplementaryExecutor
};

function mirroredExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const mirroredHalf = sequence.slice(0, halfLength).map(mirrorBeat);
  return [...sequence, ...mirroredHalf];
}

function rotatedExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const rotatedHalf = sequence.slice(0, halfLength).map(rotateBeat);
  return [...sequence, ...rotatedHalf];
}

function mirroredComplementaryExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const complementaryHalf = sequence.slice(0, halfLength).map(complementaryBeat);
  return [...sequence, ...complementaryHalf];
}

function rotatedComplementaryExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const rotatedComplementaryHalf = sequence.slice(0, halfLength).map(rotateComplementaryBeat);
  return [...sequence, ...rotatedComplementaryHalf];
}

function mirroredSwappedExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const swappedMirroredHalf = sequence.slice(0, halfLength).map(swapAndMirrorBeat);
  return [...sequence, ...swappedMirroredHalf];
}

function rotatedSwappedExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const swappedRotatedHalf = sequence.slice(0, halfLength).map(swapAndRotateBeat);
  return [...sequence, ...swappedRotatedHalf];
}

function strictMirroredExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const strictMirroredHalf = sequence.slice(0, halfLength).map(strictMirrorBeat);
  return [...sequence, ...strictMirroredHalf];
}

function strictRotatedExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const strictRotatedHalf = sequence.slice(0, halfLength).map(strictRotateBeat);
  return [...sequence, ...strictRotatedHalf];
}

function strictComplementaryExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const strictComplementaryHalf = sequence.slice(0, halfLength).map(strictComplementaryBeat);
  return [...sequence, ...strictComplementaryHalf];
}

function strictSwappedExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const strictSwappedHalf = sequence.slice(0, halfLength).map(strictSwapBeat);
  return [...sequence, ...strictSwappedHalf];
}

function swappedComplementaryExecutor(sequence: Sequence): Sequence {
  const halfLength = Math.floor(sequence.length / 2);
  const swappedComplementaryHalf = sequence.slice(0, halfLength).map(swapComplementaryBeat);
  return [...sequence, ...swappedComplementaryHalf];
}

// Helper transformation functions
function mirrorBeat(beat: any) {
  return {
    ...beat,
    orientation: mirrorOrientation(beat.orientation),
    position: mirrorPosition(beat.position)
  };
}

function rotateBeat(beat: any) {
  return {
    ...beat,
    orientation: rotateOrientation(beat.orientation),
    position: rotatePosition(beat.position)
  };
}

function complementaryBeat(beat: any) {
  return {
    ...beat,
    orientation: complementOrientation(beat.orientation)
  };
}

function rotateComplementaryBeat(beat: any) {
  return {
    ...beat,
    orientation: rotateComplementOrientation(beat.orientation),
    position: rotatePosition(beat.position)
  };
}

function swapAndMirrorBeat(beat: any) {
  return {
    ...beat,
    orientation: swapAndMirrorOrientation(beat.orientation),
    position: mirrorPosition(beat.position)
  };
}

function swapAndRotateBeat(beat: any) {
  return {
    ...beat,
    orientation: swapAndRotateOrientation(beat.orientation),
    position: rotatePosition(beat.position)
  };
}

function strictMirrorBeat(beat: any) {
  return mirrorBeat(beat);
}

function strictRotateBeat(beat: any) {
  return rotateBeat(beat);
}

function strictComplementaryBeat(beat: any) {
  return complementaryBeat(beat);
}

function strictSwapBeat(beat: any) {
  return {
    ...beat,
    orientation: swapOrientation(beat.orientation)
  };
}

function swapComplementaryBeat(beat: any) {
  return {
    ...beat,
    orientation: swapComplementOrientation(beat.orientation)
  };
}

// These would be real implementations in your actual system
function mirrorOrientation(orientation: any) { return orientation; }
function mirrorPosition(position: any) { return position; }
function rotateOrientation(orientation: any) { return orientation; }
function rotatePosition(position: any) { return position; }
function complementOrientation(orientation: any) { return orientation; }
function rotateComplementOrientation(orientation: any) { return orientation; }
function swapAndMirrorOrientation(orientation: any) { return orientation; }
function swapAndRotateOrientation(orientation: any) { return orientation; }
function swapOrientation(orientation: any) { return orientation; }
function swapComplementOrientation(orientation: any) { return orientation; }