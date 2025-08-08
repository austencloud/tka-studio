// types.ts - Complete TypeScript type definitions for the animator
export interface PropAttributes {
  start_loc: string;
  end_loc: string;
  start_ori: string;
  end_ori: string;
  motion_type: "pro" | "anti" | "static" | "dash";
  prop_rot_dir?: "cw" | "ccw";
  turns?: number;
}

export interface SequenceStep {
  beat: number;
  letter: string;
  letter_type?: string;
  duration?: number;
  start_pos?: string;
  end_pos?: string;
  timing?: string;
  direction?: string;
  blue_attributes: PropAttributes;
  red_attributes: PropAttributes;
}

export interface SequenceMetadata {
  word: string;
  author: string;
  level?: number;
  prop_type: string;
  grid_mode: string;
  is_circular?: boolean;
}

export type SequenceData = SequenceMetadata | SequenceStep;

export interface PropState {
  centerPathAngle: number;
  staffRotationAngle: number;
  x: number;
  y: number;
}

export interface AnimationState {
  isPlaying: boolean;
  currentBeat: number;
  totalBeats: number;
  speed: number;
  loop: boolean;
  blueProp: PropState;
  redProp: PropState;
}

export interface RenderingState {
  canvasReady: boolean;
  imagesLoaded: boolean;
  gridImage: HTMLImageElement | null;
  blueStaffImage: HTMLImageElement | null;
  redStaffImage: HTMLImageElement | null;
}

export interface ValidationIssue {
  beat: number;
  prop: "blue" | "red";
  issue: "orientation_discontinuity" | "invalid_motion" | "missing_attribute";
  expected?: string;
  actual?: string;
  message: string;
}
