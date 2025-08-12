/**
 * Standalone Ported Engine
 * 
 * This engine ports the exact working logic from the standalone HTML animator.
 * DO NOT MODIFY the core animation logic - it's proven to work.
 */

import type { PropState } from '../../types/core.js';
import {
  lerpAngle,
  calculateStepEndpoints,
  calculateProIsolationStaffAngle,
  type StepDefinition,
  type StepEndpoints
} from '../../utils/standalone-math.js';

// Grid constants from standalone
const GRID_VIEWBOX_SIZE = 950;
const GRID_CENTER = GRID_VIEWBOX_SIZE / 2;
const GRID_HALFWAY_POINT_OFFSET = 151.5;

export interface SequenceMetadata {
  word: string;
  author: string;
  totalBeats: number;
}

/**
 * Standalone Ported Animation Engine
 * Uses exact logic from working standalone HTML animator
 */
export class StandalonePortedEngine {
  private parsedSteps: StepDefinition[] = [];
  private totalBeats = 0;
  private metadata: SequenceMetadata = { word: '', author: '', totalBeats: 0 };

  // Prop states
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
   * Initialize with sequence data in standalone format
   */
  initialize(sequenceData: any[]): boolean {
    try {
      console.log('StandalonePortedEngine: Initializing with data:', sequenceData);

      if (!Array.isArray(sequenceData) || sequenceData.length < 3) {
        throw new Error('Invalid sequence data format');
      }

      // Extract metadata (index 0)
      const meta = sequenceData[0] || {};
      this.metadata = {
        word: meta.word || '',
        author: meta.author || '',
        totalBeats: sequenceData.length - 2 // Subtract metadata and start position
      };

      // Extract steps (index 2 onwards)
      this.parsedSteps = sequenceData;
      this.totalBeats = this.metadata.totalBeats;

      console.log('StandalonePortedEngine: Parsed steps:', this.parsedSteps.length);
      console.log('StandalonePortedEngine: Total beats:', this.totalBeats);

      this.initializePropStates();
      return true;
    } catch (error) {
      console.error('StandalonePortedEngine: Failed to initialize:', error);
      return false;
    }
  }

  /**
   * Reset to initial state
   */
  reset(): void {
    this.initializePropStates();
  }

  /**
   * Calculate state for given beat using exact standalone logic
   */
  calculateState(currentBeat: number): void {
    if (this.parsedSteps.length === 0 || this.totalBeats === 0) {
      console.warn('StandalonePortedEngine: No sequence data available');
      return;
    }

    // EXACT LOGIC FROM STANDALONE HTML - DO NOT MODIFY
    const clampedBeat = Math.max(0, Math.min(currentBeat, this.totalBeats));
    const currentAnimationStepIndex = Math.floor(
      clampedBeat === this.totalBeats ? this.totalBeats - 1 : clampedBeat
    );
    const currentStepArrayIndex = currentAnimationStepIndex + 2; // Map beat 0..N-1 to array index 2..N+1
    const t = clampedBeat === this.totalBeats ? 1.0 : clampedBeat - currentAnimationStepIndex;

    const stepDefinition = this.parsedSteps[currentStepArrayIndex];

    if (!stepDefinition) {
      console.error(
        `StandalonePortedEngine: No step definition for array index ${currentStepArrayIndex} (beat: ${clampedBeat})`
      );
      return;
    }

    const blueEndpoints = calculateStepEndpoints(stepDefinition, 'blue');
    const redEndpoints = calculateStepEndpoints(stepDefinition, 'red');

    if (blueEndpoints && redEndpoints) {
      // EXACT INTERPOLATION LOGIC FROM STANDALONE
      this.bluePropState.centerPathAngle = lerpAngle(
        blueEndpoints.startCenterAngle,
        blueEndpoints.targetCenterAngle,
        t
      );
      this.bluePropState.staffRotationAngle = lerpAngle(
        blueEndpoints.startStaffAngle,
        blueEndpoints.targetStaffAngle,
        t
      );
      this.redPropState.centerPathAngle = lerpAngle(
        redEndpoints.startCenterAngle,
        redEndpoints.targetCenterAngle,
        t
      );
      this.redPropState.staffRotationAngle = lerpAngle(
        redEndpoints.startStaffAngle,
        redEndpoints.targetStaffAngle,
        t
      );

      // Handle pro motion special case
      if (stepDefinition.blue_attributes?.motion_type === 'pro') {
        this.bluePropState.staffRotationAngle = calculateProIsolationStaffAngle(
          this.bluePropState.centerPathAngle,
          stepDefinition.blue_attributes.prop_rot_dir || 'cw'
        );
      }
      if (stepDefinition.red_attributes?.motion_type === 'pro') {
        this.redPropState.staffRotationAngle = calculateProIsolationStaffAngle(
          this.redPropState.centerPathAngle,
          stepDefinition.red_attributes.prop_rot_dir || 'cw'
        );
      }

      // Update coordinates from angles
      this.updateCoordinatesFromAngle(this.bluePropState);
      this.updateCoordinatesFromAngle(this.redPropState);
    } else {
      console.error('StandalonePortedEngine: Could not calculate endpoints for step');
    }
  }

  /**
   * Initialize prop states to start position
   */
  private initializePropStates(): void {
    // Set to center position initially
    this.bluePropState = {
      centerPathAngle: 0,
      staffRotationAngle: Math.PI, // 'in' orientation
      x: 0,
      y: 0,
    };
    this.redPropState = {
      centerPathAngle: Math.PI, // Opposite side
      staffRotationAngle: 0, // 'in' orientation
      x: 0,
      y: 0,
    };

    this.updateCoordinatesFromAngle(this.bluePropState);
    this.updateCoordinatesFromAngle(this.redPropState);
  }

  /**
   * Update x,y coordinates from center path angle
   */
  private updateCoordinatesFromAngle(propState: PropState): void {
    const radius = GRID_HALFWAY_POINT_OFFSET;
    propState.x = Math.cos(propState.centerPathAngle) * radius;
    propState.y = Math.sin(propState.centerPathAngle) * radius;
  }

  // Public getters
  getBluePropState(): PropState {
    return { ...this.bluePropState };
  }

  getRedPropState(): PropState {
    return { ...this.redPropState };
  }

  getTotalBeats(): number {
    return this.totalBeats;
  }

  getMetadata(): SequenceMetadata {
    return { ...this.metadata };
  }
}
