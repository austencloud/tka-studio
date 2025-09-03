type RotationDirection = 'clockwise' | 'counterclockwise';
type PropContinuity = 'continuous' | 'random';

export function determineRotationDirection(
  propContinuity: PropContinuity
): { blue: RotationDirection; red: RotationDirection } {
  if (propContinuity === 'continuous') {
    // Ensure consistent rotation between both props
    const baseDirection = Math.random() < 0.5 ? 'clockwise' : 'counterclockwise';
    return {
      blue: baseDirection,
      red: baseDirection
    };
  }

  // Random rotation for each prop
  return {
    blue: Math.random() < 0.5 ? 'clockwise' : 'counterclockwise',
    red: Math.random() < 0.5 ? 'clockwise' : 'counterclockwise'
  };
}

export function invertRotationDirection(direction: RotationDirection): RotationDirection {
  return direction === 'clockwise' ? 'counterclockwise' : 'clockwise';
}

export const rotationUtils = {
  determineRotationDirection,
  invertRotationDirection
};