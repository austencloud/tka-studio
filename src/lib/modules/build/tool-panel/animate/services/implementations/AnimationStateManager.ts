/**
 * Animation State Service
 *
 * Focused service for managing prop states and coordinate calculations.
 * Single responsibility: Prop state management and coordinate transformations.
 */

import type { PropState, PropStates } from "$shared";
import { injectable } from "inversify";
import type { IAnimationStateManager, InterpolationResult } from "../contracts";

@injectable()
export class AnimationStateManager implements IAnimationStateManager {
  constructor() {}

  private bluePropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
  };

  private redPropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
  };

  /**
   * Get current blue prop state
   */
  getBluePropState(): PropState {
    return { ...this.bluePropState };
  }

  /**
   * Get current red prop state
   */
  getRedPropState(): PropState {
    return { ...this.redPropState };
  }

  /**
   * Get both prop states
   */
  getPropStates(): PropStates {
    return {
      blue: this.getBluePropState(),
      red: this.getRedPropState(),
    };
  }

  /**
   * Update prop states from interpolation result
   */
  updatePropStates(interpolationResult: InterpolationResult): PropStates {
    // Update blue prop state - include x,y if provided (dash motions)
    const blueUpdate: Partial<PropState> = {
      centerPathAngle: interpolationResult.blueAngles.centerPathAngle,
      staffRotationAngle: interpolationResult.blueAngles.staffRotationAngle,
    };
    if ('x' in interpolationResult.blueAngles && 'y' in interpolationResult.blueAngles) {
      blueUpdate.x = interpolationResult.blueAngles.x;
      blueUpdate.y = interpolationResult.blueAngles.y;
    }
    this.updateBluePropState(blueUpdate);

    // Update red prop state - include x,y if provided (dash motions)
    const redUpdate: Partial<PropState> = {
      centerPathAngle: interpolationResult.redAngles.centerPathAngle,
      staffRotationAngle: interpolationResult.redAngles.staffRotationAngle,
    };
    if ('x' in interpolationResult.redAngles && 'y' in interpolationResult.redAngles) {
      redUpdate.x = interpolationResult.redAngles.x;
      redUpdate.y = interpolationResult.redAngles.y;
    }
    this.updateRedPropState(redUpdate);

    return this.getPropStates();
  }

  /**
   * Update blue prop state
   * Dash motions provide their own x,y coordinates, other motions only provide angles
   */
  updateBluePropState(updates: Partial<PropState>): void {
    this.bluePropState = { ...this.bluePropState, ...updates };
  }

  /**
   * Update red prop state
   * Dash motions provide their own x,y coordinates, other motions only provide angles
   */
  updateRedPropState(updates: Partial<PropState>): void {
    this.redPropState = { ...this.redPropState, ...updates };
  }

  /**
   * Set prop states directly (for initialization)
   */
  setPropStates(blue: PropState, red: PropState): void {
    this.bluePropState = { ...blue };
    this.redPropState = { ...red };
  }

  /**
   * Reset prop states to default
   */
  resetPropStates(): void {
    this.bluePropState = {
      centerPathAngle: 0,
      staffRotationAngle: Math.PI,
    };
    this.redPropState = {
      centerPathAngle: Math.PI,
      staffRotationAngle: 0,
    };
  }
}
