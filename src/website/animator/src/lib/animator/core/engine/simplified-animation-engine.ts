/**
 * Simplified Animation Engine based on working standalone logic
 * This maintains your modern architecture while using the proven math from standalone
 */

import type { SequenceData, SequenceStep, PropState, PropAttributes } from '../../types/core.js';

interface StepEndpoints {
  startCenterAngle: number;
  startStaffAngle: number;
  targetCenterAngle: number;
  targetStaffAngle: number;
}

export class SimplifiedAnimationEngine {
  private sequenceData: SequenceData | null = null;
  private steps: SequenceStep[] = [];
  private totalBeats = 0;

  // Math constants from working standalone
  private readonly PI = Math.PI;
  private readonly TWO_PI = 2 * Math.PI;
  private readonly HALF_PI = Math.PI / 2;

  // Grid constants from working standalone
  private readonly GRID_VIEWBOX_SIZE = 950;
  private readonly GRID_CENTER = this.GRID_VIEWBOX_SIZE / 2;
  private readonly GRID_HALFWAY_POINT_OFFSET = 151.5;

  private bluePropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
    x: 0,
    y: 0
  };

  private redPropState: PropState = {
    centerPathAngle: 0,
    staffRotationAngle: 0,
    x: 0,
    y: 0
  };

  /**
  * Initialize with sequence data
  */
  initialize(data: SequenceData): boolean {
  try {
  console.log('SimplifiedAnimationEngine: Initializing with data:', data);
  this.sequenceData = data;
  this.steps = data.slice(2) as SequenceStep[]; // Skip metadata and start position
  this.totalBeats = this.steps.length;
  console.log('SimplifiedAnimationEngine: Total beats:', this.totalBeats);
   this.initializePropStates();
  console.log('SimplifiedAnimationEngine: Initialized successfully');
   return true;
   } catch (error) {
			console.error('SimplifiedAnimationEngine: Failed to initialize:', error);
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
  * Calculate state for given beat (using standalone logic)
  */
  calculateState(beat: number): void {
  if (!this.sequenceData || this.steps.length === 0) {
  console.warn('SimplifiedAnimationEngine: No sequence data or steps available');
   return;
		}

    // Constrain beat to valid range
    const constrainedBeat = Math.max(0, Math.min(beat, this.totalBeats));

    // Get start position (index 1 in sequence data)
    const startPosition = this.sequenceData[1] as SequenceStep;

    if (constrainedBeat === 0) {
      // At beat 0, show start position
      this.calculatePropFromStep(this.bluePropState, startPosition.blue_attributes, startPosition.blue_attributes, 0);
      this.calculatePropFromStep(this.redPropState, startPosition.red_attributes, startPosition.red_attributes, 0);
      return;
    }

    if (constrainedBeat >= this.totalBeats) {
      // Show final step
      const finalStep = this.steps[this.steps.length - 1];
      this.calculatePropFromStep(this.bluePropState, finalStep.blue_attributes, finalStep.blue_attributes, 1);
      this.calculatePropFromStep(this.redPropState, finalStep.red_attributes, finalStep.red_attributes, 1);
      return;
    }

    // Find current step and interpolation factor
    const stepIndex = Math.floor(constrainedBeat - 1);
    const t = constrainedBeat - 1 - stepIndex;

    const currentStep = this.steps[stepIndex];
    const nextStep = this.steps[stepIndex + 1] || currentStep;

    // Calculate prop states using standalone logic
    this.calculatePropFromStep(this.bluePropState, currentStep.blue_attributes, nextStep.blue_attributes, t);
    this.calculatePropFromStep(this.redPropState, currentStep.red_attributes, nextStep.red_attributes, t);
  }

  /**
   * Calculate prop state from step data (using standalone approach)
   */
  private calculatePropFromStep(propState: PropState, currentAttrs: PropAttributes, nextAttrs: PropAttributes, t: number): void {
    // Calculate endpoints using standalone logic
    const endpoints = this.calculateStepEndpoints(currentAttrs, nextAttrs);

    // Interpolate angles
    propState.centerPathAngle = this.lerpAngle(endpoints.startCenterAngle, endpoints.targetCenterAngle, t);
    propState.staffRotationAngle = this.lerpAngle(endpoints.startStaffAngle, endpoints.targetStaffAngle, t);

    // Handle pro motion special case (dynamic staff rotation)
    if (currentAttrs.motion_type === 'pro') {
      propState.staffRotationAngle = this.calculateProIsolationStaffAngle(
        propState.centerPathAngle,
        currentAttrs.prop_rot_dir
      );
    }

    // Convert to coordinates for rendering
    this.updateCoordinatesFromAngle(propState);
  }

  /**
   * Calculate step endpoints using standalone logic
   */
  private calculateStepEndpoints(currentAttrs: PropAttributes, nextAttrs: PropAttributes): StepEndpoints {
    const startCenterAngle = this.mapPositionToAngle(currentAttrs.start_loc);
    const startStaffAngle = this.mapOrientationToAngle(currentAttrs.start_ori || 'in', startCenterAngle);
    const targetCenterAngle = this.mapPositionToAngle(nextAttrs.start_loc || currentAttrs.end_loc);

    let targetStaffAngle: number;

    switch (currentAttrs.motion_type) {
      case 'pro':
        targetStaffAngle = this.calculateProIsolationStaffAngle(targetCenterAngle, currentAttrs.prop_rot_dir);
        break;

      case 'anti':
        targetStaffAngle = this.calculateAntispinTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          currentAttrs.turns || 0,
          currentAttrs.prop_rot_dir
        );
        break;

      case 'static':
        targetStaffAngle = this.calculateStaticStaffAngle(targetCenterAngle, currentAttrs.end_ori || currentAttrs.start_ori);
        break;

      case 'dash':
        targetStaffAngle = this.calculateDashTargetAngle(
          startCenterAngle,
          targetCenterAngle,
          startStaffAngle,
          currentAttrs.prop_rot_dir
        );
        break;

      default:
        targetStaffAngle = startStaffAngle;
        break;
    }

    // Handle explicit end orientation override
    if (currentAttrs.motion_type !== 'pro') {
      const endOriAngle = this.mapOrientationToAngle(currentAttrs.end_ori || 'in', targetCenterAngle);
      const explicitEndOri = ['n', 'e', 's', 'w', 'in', 'out'].includes((currentAttrs.end_ori || '').toLowerCase());
      if (explicitEndOri) {
        targetStaffAngle = endOriAngle;
      }
    }

    return {
      startCenterAngle,
      startStaffAngle,
      targetCenterAngle,
      targetStaffAngle
    };
  }

  /**
   * Position mapping from standalone (simple and working)
   */
  private mapPositionToAngle(position: string | undefined): number {
    if (!position) return 0;

    const locationAngles: Record<string, number> = {
      e: 0,
      s: this.HALF_PI,
      w: this.PI,
      n: -this.HALF_PI
    };

    return locationAngles[position.toLowerCase()] || 0;
  }

  /**
   * Orientation mapping from standalone
   */
  private mapOrientationToAngle(orientation: string | undefined, centerPathAngle: number): number {
    if (!orientation) return this.normalizeAnglePositive(centerPathAngle + this.PI);

    const ori = orientation.toLowerCase();

    // Direct angle mappings
    const locationAngles: Record<string, number> = {
      e: 0,
      s: this.HALF_PI,
      w: this.PI,
      n: -this.HALF_PI
    };

    if (locationAngles.hasOwnProperty(ori)) {
      return locationAngles[ori];
    }

    // Relative orientations
    if (ori === 'in') return this.normalizeAnglePositive(centerPathAngle + this.PI);
    if (ori === 'out') return this.normalizeAnglePositive(centerPathAngle);

    return this.normalizeAnglePositive(centerPathAngle + this.PI);
  }

  /**
   * Pro isolation calculation from standalone
   */
  private calculateProIsolationStaffAngle(centerPathAngle: number, propRotDir?: string): number {
    return this.normalizeAnglePositive(centerPathAngle + this.PI);
  }

  /**
   * Antispin calculation from standalone
   */
  private calculateAntispinTargetAngle(
    startCenterAngle: number,
    endCenterAngle: number,
    startStaffAngle: number,
    turns: number,
    propRotDir?: string
  ): number {
    const delta = this.normalizeAngleSigned(endCenterAngle - startCenterAngle);
    const base = -delta;
    const turn = this.PI * turns;
    const dir = propRotDir?.toLowerCase() === 'ccw' ? -1 : 1;

    return this.normalizeAnglePositive(startStaffAngle + base + turn * dir);
  }

  /**
   * Static staff angle calculation
   */
  private calculateStaticStaffAngle(centerPathAngle: number, orientation?: string): number {
    return this.mapOrientationToAngle(orientation, centerPathAngle);
  }

  /**
   * Dash target angle calculation
   */
  private calculateDashTargetAngle(
    startCenterAngle: number,
    endCenterAngle: number,
    startStaffAngle: number,
    propRotDir?: string
  ): number {
    return startStaffAngle; // Dash keeps same staff angle
  }

  /**
   * Update coordinates from center path angle
   */
  private updateCoordinatesFromAngle(propState: PropState): void {
    const centerX = this.GRID_CENTER;
    const centerY = this.GRID_CENTER;
    const inwardFactor = 0.95;

    propState.x = centerX + Math.cos(propState.centerPathAngle) * this.GRID_HALFWAY_POINT_OFFSET * inwardFactor;
    propState.y = centerY + Math.sin(propState.centerPathAngle) * this.GRID_HALFWAY_POINT_OFFSET * inwardFactor;
  }

  /**
   * Angle utilities from standalone
   */
  private normalizeAnglePositive(angle: number): number {
    return ((angle % this.TWO_PI) + this.TWO_PI) % this.TWO_PI;
  }

  private normalizeAngleSigned(angle: number): number {
    const norm = this.normalizeAnglePositive(angle);
    return norm > this.PI ? norm - this.TWO_PI : norm;
  }

  private lerpAngle(a: number, b: number, t: number): number {
    const d = this.normalizeAngleSigned(b - a);
    return this.normalizeAnglePositive(a + d * t);
  }

  private initializePropStates(): void {
  if (!this.sequenceData || this.sequenceData.length < 2) {
  console.log('SimplifiedAnimationEngine: Using default positions');
  // Default positions
  this.bluePropState = {
  centerPathAngle: this.mapPositionToAngle('s'),
  staffRotationAngle: this.mapPositionToAngle('s') + this.PI,
  x: this.GRID_CENTER,
   y: this.GRID_CENTER + this.GRID_HALFWAY_POINT_OFFSET * 0.95
  };
  this.redPropState = {
  centerPathAngle: this.mapPositionToAngle('n'),
  staffRotationAngle: this.mapPositionToAngle('n') + this.PI,
  x: this.GRID_CENTER,
   y: this.GRID_CENTER - this.GRID_HALFWAY_POINT_OFFSET * 0.95
  };
   console.log('SimplifiedAnimationEngine: Default blue prop:', this.bluePropState);
			console.log('SimplifiedAnimationEngine: Default red prop:', this.redPropState);
			return;
		}

    const startState = this.sequenceData[1] as SequenceStep;

    // Initialize blue prop
    const blueStartAngle = this.mapPositionToAngle(startState.blue_attributes.start_loc);
    this.bluePropState.centerPathAngle = blueStartAngle;
    this.bluePropState.staffRotationAngle = this.mapOrientationToAngle(
      startState.blue_attributes.start_ori || 'in',
      blueStartAngle
    );
    this.updateCoordinatesFromAngle(this.bluePropState);

    // Initialize red prop
    const redStartAngle = this.mapPositionToAngle(startState.red_attributes.start_loc);
    this.redPropState.centerPathAngle = redStartAngle;
    this.redPropState.staffRotationAngle = this.mapOrientationToAngle(
      startState.red_attributes.start_ori || 'in',
      redStartAngle
    );
    this.updateCoordinatesFromAngle(this.redPropState);
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

  getMetadata() {
    const meta = this.sequenceData?.[0] || {};
    return {
      totalBeats: this.totalBeats,
      word: meta.word || '',
      author: meta.author || ''
    };
  }
}
