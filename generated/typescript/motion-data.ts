/**
 * Generated from schemas/motion-data.json
 *
 * This file is auto-generated. Do not edit manually.
 * To make changes, update the JSON schema and regenerate.
 */

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
