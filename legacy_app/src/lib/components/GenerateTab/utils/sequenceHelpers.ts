export interface Beat {
    index: number;
    orientation: {
      blue: string;
      red: string;
    };
    position: string;
    turnIntensity: number;
  }

  export function generateBaseSequence(
    length: number,
    options: {
      turnIntensity: number,
      propContinuity: 'continuous' | 'random'
    }
  ): Beat[] {
    return Array.from({ length }, (_, index) => ({
      index,
      orientation: generateOrientation(options),
      position: determinePosition(index),
      turnIntensity: calculateTurnIntensity(options.turnIntensity)
    }));
  }

  function generateOrientation(options: { propContinuity: 'continuous' | 'random' }) {
    const generateSingleOrientation = () =>
      ['in', 'out', 'cw', 'ccw'][Math.floor(Math.random() * 4)];

    if (options.propContinuity === 'continuous') {
      const baseOrientation = generateSingleOrientation();
      return { blue: baseOrientation, red: baseOrientation };
    }

    return {
      blue: generateSingleOrientation(),
      red: generateSingleOrientation()
    };
  }

  function determinePosition(index: number): string {
    const positions = [
      'alpha1_alpha1',
      'beta5_beta5',
      'gamma11_gamma11'
    ];
    return positions[index % positions.length];
  }

  function calculateTurnIntensity(baseTurnIntensity: number): number {
    // Add some randomness to turn intensity
    const variation = Math.random() * 0.5 - 0.25;
    return Math.max(0, baseTurnIntensity + variation);
  }

  export function transformSequence(
    sequence: Beat[],
    transformationType: string
  ): Beat[] {
    switch (transformationType) {
      case 'mirrored':
        return mirrorSequence(sequence);
      case 'rotated':
        return rotateSequence(sequence);
      default:
        return sequence;
    }
  }

  function mirrorSequence(sequence: Beat[]): Beat[] {
    return sequence.map(beat => ({
      ...beat,
      orientation: {
        blue: invertOrientation(beat.orientation.blue),
        red: invertOrientation(beat.orientation.red)
      }
    }));
  }

  function rotateSequence(sequence: Beat[]): Beat[] {
    return sequence.map(beat => ({
      ...beat,
      position: rotatePosition(beat.position)
    }));
  }

  function invertOrientation(orientation: string): string {
    const invertMap: Record<string, string> = {
      'in': 'out',
      'out': 'in',
      'cw': 'ccw',
      'ccw': 'cw'
    };
    return invertMap[orientation] || orientation;
  }

  function rotatePosition(position: string): string {
    const rotationMap: Record<string, string> = {
      'alpha1_alpha1': 'beta5_beta5',
      'beta5_beta5': 'gamma11_gamma11',
      'gamma11_gamma11': 'alpha1_alpha1'
    };
    return rotationMap[position] || position;
  }

  export const sequenceUtils = {
    generateBaseSequence,
    transformSequence
  };
