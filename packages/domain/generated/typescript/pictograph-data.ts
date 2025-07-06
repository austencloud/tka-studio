/**
 * Generated from schemas/pictograph-data.json
 *
 * This file is auto-generated. Do not edit manually.
 * To make changes, update the JSON schema and regenerate.
 */

/**
 * Complete pictograph data structure containing all visual and motion information for TKA pictographs
 */
export interface PictographData {
  /**
   * TKA letter designation for this pictograph
   */
  letter?:
    | null
    | 'A'
    | 'B'
    | 'C'
    | 'D'
    | 'E'
    | 'F'
    | 'G'
    | 'H'
    | 'I'
    | 'J'
    | 'K'
    | 'L'
    | 'M'
    | 'N'
    | 'O'
    | 'P'
    | 'Q'
    | 'R'
    | 'S'
    | 'T'
    | 'U'
    | 'V'
    | 'W'
    | 'X'
    | 'Y'
    | 'Z'
    | 'Σ'
    | 'Δ'
    | 'θ'
    | 'Ω'
    | 'W-'
    | 'X-'
    | 'Y-'
    | 'Z-'
    | 'Σ-'
    | 'Δ-'
    | 'θ-'
    | 'Ω-'
    | 'Φ'
    | 'Ψ'
    | 'Λ'
    | 'Φ-'
    | 'Ψ-'
    | 'Λ-'
    | 'α'
    | 'β'
    | 'Γ';
  /**
   * Starting position on the TKA grid
   */
  start_pos?:
    | null
    | 'alpha1'
    | 'alpha2'
    | 'alpha3'
    | 'alpha4'
    | 'alpha5'
    | 'alpha6'
    | 'alpha7'
    | 'alpha8'
    | 'beta1'
    | 'beta2'
    | 'beta3'
    | 'beta4'
    | 'beta5'
    | 'beta6'
    | 'beta7'
    | 'beta8'
    | 'gamma1'
    | 'gamma2'
    | 'gamma3'
    | 'gamma4'
    | 'gamma5'
    | 'gamma6'
    | 'gamma7'
    | 'gamma8'
    | 'gamma9'
    | 'gamma10'
    | 'gamma11'
    | 'gamma12'
    | 'gamma13'
    | 'gamma14'
    | 'gamma15'
    | 'gamma16';
  /**
   * Ending position on the TKA grid
   */
  end_pos?:
    | null
    | 'alpha1'
    | 'alpha2'
    | 'alpha3'
    | 'alpha4'
    | 'alpha5'
    | 'alpha6'
    | 'alpha7'
    | 'alpha8'
    | 'beta1'
    | 'beta2'
    | 'beta3'
    | 'beta4'
    | 'beta5'
    | 'beta6'
    | 'beta7'
    | 'beta8'
    | 'gamma1'
    | 'gamma2'
    | 'gamma3'
    | 'gamma4'
    | 'gamma5'
    | 'gamma6'
    | 'gamma7'
    | 'gamma8'
    | 'gamma9'
    | 'gamma10'
    | 'gamma11'
    | 'gamma12'
    | 'gamma13'
    | 'gamma14'
    | 'gamma15'
    | 'gamma16';
  /**
   * VTG timing - split or together
   */
  timing?: null | 'split' | 'tog';
  /**
   * VTG direction - same or opposite
   */
  direction?: null | 'same' | 'opp';
  /**
   * Grid display mode
   */
  grid_mode: 'diamond' | 'box';
  /**
   * Grid positioning and configuration data
   */
  grid_data?: {
    center_x?: number;
    center_y?: number;
    radius?: number;
    [k: string]: unknown;
  } | null;
  /**
   * Motion data for blue prop/arrow
   */
  blue_motion_data?: MotionData | null;
  /**
   * Motion data for red prop/arrow
   */
  red_motion_data?: MotionData | null;
  /**
   * Red prop visual data
   */
  red_prop_data?: {
    prop_type?: string;
    color?: string;
    position_x?: number;
    position_y?: number;
    [k: string]: unknown;
  } | null;
  /**
   * Blue prop visual data
   */
  blue_prop_data?: {
    prop_type?: string;
    color?: string;
    position_x?: number;
    position_y?: number;
    [k: string]: unknown;
  } | null;
  /**
   * Red arrow visual data
   */
  red_arrow_data?: {
    arrow_type?: string;
    color?: string;
    position_x?: number;
    position_y?: number;
    rotation_angle?: number;
    [k: string]: unknown;
  } | null;
  /**
   * Blue arrow visual data
   */
  blue_arrow_data?: {
    arrow_type?: string;
    color?: string;
    position_x?: number;
    position_y?: number;
    rotation_angle?: number;
    [k: string]: unknown;
  } | null;
  /**
   * Grid identifier string
   */
  grid: string;
  /**
   * Flag indicating if this is a start position pictograph
   */
  is_start_position?: boolean;
}
/**
 * Immutable motion data for props and arrows. Replaces complex motion attribute dictionaries.
 */
export interface MotionData {
  /**
   * Type of motion being performed
   */
  motion_type: 'pro' | 'anti' | 'float' | 'dash' | 'static';
  /**
   * Direction of prop rotation
   */
  prop_rot_dir: 'cw' | 'ccw' | 'no_rot';
  /**
   * Starting location on the grid
   */
  start_loc: 'n' | 'e' | 's' | 'w' | 'ne' | 'nw' | 'se' | 'sw';
  /**
   * Ending location on the grid
   */
  end_loc: 'n' | 'e' | 's' | 'w' | 'ne' | 'nw' | 'se' | 'sw';
  /**
   * Number of turns in the motion
   */
  turns: number;
  /**
   * Starting orientation
   */
  start_ori: 'in' | 'out' | 'clock' | 'counter';
  /**
   * Ending orientation
   */
  end_ori: 'in' | 'out' | 'clock' | 'counter';
}
