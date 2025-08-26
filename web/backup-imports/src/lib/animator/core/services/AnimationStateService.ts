/**
 * Animation State Service
 *
 * Focused service for managing prop states and coordinate calculations.
 * Single responsibility: Prop state management and coordinate transformations.
 */

import type { PropState } from "../../../components/animator/types/PropState.js";
import { calculateCoordinatesFromAngle } from "../../utils/math/index.js";
import type {
  IAnimationStateService,
  PropStates,
  InterpolationResult,
} from "$lib/services/di/interfaces/animator-interfaces";

export class AnimationStateService implements IAnimationStateService {
  private bluePropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
    x: 0,
    y: 0,
  };

  private redPropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
    x: 0,
    y: 0,
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
    // Update blue prop state
    this.updateBluePropState({
      centerPathAngle: interpolationResult.blueAngles.centerPathAngle,
      staffRotationAngle: interpolationResult.blueAngles.staffRotationAngle,
    });

    // Update red prop state
    this.updateRedPropState({
      centerPathAngle: interpolationResult.redAngles.centerPathAngle,
      staffRotationAngle: interpolationResult.redAngles.staffRotationAngle,
    });

    return this.getPropStates();
  }

  /**
   * Update blue prop state
   */
  updateBluePropState(updates: Partial<PropState>): void {
    this.bluePropState = { ...this.bluePropState, ...updates };
    this.updateCoordinatesFromAngle(this.bluePropState);
  }

  /**
   * Update red prop state
   */
  updateRedPropState(updates: Partial<PropState>): void {
    this.redPropState = { ...this.redPropState, ...updates };
    this.updateCoordinatesFromAngle(this.redPropState);
  }

  /**
   * Set prop states directly (for initialization)
   */
  setPropStates(blue: PropState, red: PropState): void {
    this.bluePropState = { ...blue };
    this.redPropState = { ...red };
    this.updateCoordinatesFromAngle(this.bluePropState);
    this.updateCoordinatesFromAngle(this.redPropState);
  }

  /**
   * Reset prop states to default
   */
  resetPropStates(): void {
    this.bluePropState = {
      centerPathAngle: 0,
      staffRotationAngle: Math.PI,
      x: 0,
      y: 0,
    };
    this.redPropState = {
      centerPathAngle: Math.PI,
      staffRotationAngle: 0,
      x: 0,
      y: 0,
    };
    this.updateCoordinatesFromAngle(this.bluePropState);
    this.updateCoordinatesFromAngle(this.redPropState);
  }

  /**
   * Update x,y coordinates from center path angle
   * EXACT LOGIC FROM STANDALONE ANIMATOR
   */
  private updateCoordinatesFromAngle(propState: PropState): void {
    const coordinates = calculateCoordinatesFromAngle(
      propState.centerPathAngle
    );
    propState.x = coordinates.x;
    propState.y = coordinates.y;
  }
}
