// TypeScript types for the pictograph animator

export interface PropState {
  centerPathAngle: number;
  staffRotationAngle: number;
  x: number;
  y: number;
}

export interface PropAttributes {
  start_loc: string;
  end_loc: string;
  start_ori: string;
  end_ori: string;
  prop_rot_dir: string;
  turns: number;
  motion_type: string;
}

export interface StepDefinition {
  beat?: number;
  letter?: string;
  letter_type?: string;
  duration?: number;
  start_pos?: string;
  end_pos?: string;
  timing?: string;
  direction?: string;
  blue_attributes: PropAttributes;
  red_attributes: PropAttributes;
  sequence_start_position?: string;
  arrayIndex?: number;
}

export interface SequenceMetadata {
  word: string;
  author: string;
  level: number;
  prop_type: string;
  grid_mode: string;
  is_circular: boolean;
  can_be_CAP: boolean;
  is_strict_rotated_CAP: boolean;
  is_strict_mirrored_CAP: boolean;
  is_strict_swapped_CAP: boolean;
  is_mirrored_swapped_CAP: boolean;
  is_rotated_swapped_CAP: boolean;
}

export interface StepEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

export interface AnimationState {
  isPlaying: boolean;
  currentBeat: number;
  speed: number;
  continuousLoop: boolean;
  totalBeats: number;
  lastTimestamp: number | null;
  animationFrameId: number | null;
}

export interface CanvasState {
  ctx: CanvasRenderingContext2D | null;
  imagesLoaded: boolean;
  canvasReady: boolean;
  gridImage: HTMLImageElement | null;
  blueStaffImage: HTMLImageElement | null;
  redStaffImage: HTMLImageElement | null;
}

export type MessageType = "error" | "success";
