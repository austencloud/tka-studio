import type { BeatData } from "$domain";
import type { PropState } from "../types/PropState";

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

export interface PropStates {
  blue: PropState;
  red: PropState;
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
}
