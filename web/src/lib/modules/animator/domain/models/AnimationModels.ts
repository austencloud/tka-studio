import type {
  BeatData,
  Location,
  MotionType,
  Orientation,
  RotationDirection,
} from "$shared/domain";

export interface InterpolationResult {
  blueAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  redAngles: {
    centerPathAngle: number;
    staffRotationAngle: number;
  };
  isValid: boolean;
}

export interface BeatCalculationResult {
  currentBeatIndex: number;
  beatProgress: number;
  currentBeatData: BeatData;
  isValid: boolean;
}

export interface AnimationConfig {
  duration: number;
  easing: string;
  autoPlay: boolean;
  loop: boolean;
}

export interface AnimationState {
  isPlaying: boolean;
  currentFrame: number;
  totalFrames: number;
  progress: number;
  currentBeat: number;
}

export interface PropVisibility {
  blue: boolean;
  red: boolean;
}
export interface MotionEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

/**
 * Motion Test Parameters
 * Domain model for motion testing and configuration
 */
export interface AnimatedMotionParams {
  startLocation: Location;
  endLocation: Location;
  motionType: MotionType;
  turns: number | "fl"; // Support both numeric turns and float
  rotationDirection: RotationDirection;
  startOrientation: Orientation;
  endOrientation: Orientation;
}

// Legacy alias for backward compatibility
export type MotionTestParams = AnimatedMotionParams;

// Motion calculation utilities
export function calculateMotionEndpoints(
  _params: AnimatedMotionParams
): MotionEndpoints {
  return {
    startCenterAngle: 0,
    startStaffAngle: 0,
    targetCenterAngle: 90,
    targetStaffAngle: 90,
  };
}

export function lerpAngle(start: number, end: number, t: number): number {
  return start + (end - start) * t;
}

export interface LetterIdentificationResult {
  letter: string;
  confidence: number;
  isValid: boolean;
}

export interface LetterMapping {
  startPosition: Location;
  endPosition: Location;
  blueMotionType: MotionType;
  redMotionType: MotionType;
  // Add other motion properties as needed
  turns?: number | "fl";
  rotationDirection?: RotationDirection;
  startOrientation?: Orientation;
  endOrientation?: Orientation;
}
