/**
 * Core sequence interpretation debugging engine
 * Provides comprehensive analysis and validation of sequence interpretation logic
 */

import type {
	SequenceData,
	SequenceStep,
	PropAttributes,
	PropState
	// MotionType, // Not used currently
	// PropRotDir, // Not used currently
	// Orientation // Not used currently
} from '../../types/core.js';

import type {
	BeatDebugInfo,
	PropDebugInfo,
	RotationInterpretation,
	PropValidation,
	OrientationContinuityCheck,
	TurnCountCheck,
	DebugConfiguration,
	DebugOverrides,
	DebugSession,
	ValidationSummary
	// DebugEvent, // Not used currently
	// DebugMetrics // Not used currently
} from '../../types/debug.js';

import { AnimationEngine } from '../engine/animation-engine.js';
import { mapPositionToCoordinates } from '../../utils/math/diamond-grid.js';
import {
	getOrientationAngle,
	getDegreesForTurns,
	getRotationMultiplier,
	degreesToRadians
	// normalizeAngle // Not used currently
} from '../../config/sequence-interpretation.js';

import {
	calculateProIsolationStaffAngle,
	calculateAntispinTargetAngle,
	calculateStaticStaffAngle,
	calculateDashTargetAngle
} from '../../utils/math/prop-calculations.js';

/**
 * Main debugging engine for sequence interpretation
 */
export class SequenceDebugger {
	private animationEngine: AnimationEngine;
	private sequenceData: SequenceData | null = null;
	private debugHistory: BeatDebugInfo[] = [];
	private configuration: DebugConfiguration;
	private overrides: DebugOverrides;
	private currentSession: DebugSession | null = null;
	private eventListeners: Map<string, Function[]> = new Map();

	constructor(config?: Partial<DebugConfiguration>) {
		this.animationEngine = new AnimationEngine();
		this.configuration = this.createDefaultConfiguration(config);
		this.overrides = this.createDefaultOverrides();
	}

	// ============================================================================
	// SESSION MANAGEMENT
	// ============================================================================

	startSession(sequenceData: SequenceData, sessionId?: string): DebugSession {
		this.sequenceData = sequenceData;
		this.animationEngine.initialize(sequenceData);

		const metadata = sequenceData[0] || {};
		this.currentSession = {
			id: sessionId || this.generateSessionId(),
			sequenceId: (metadata as any).id || 'unknown',
			sequenceWord: (metadata as any).word || 'unknown',
			startTime: Date.now(),
			configuration: { ...this.configuration },
			overrides: this.cloneOverrides(this.overrides),
			history: [],
			validationSummary: this.createEmptyValidationSummary(),
			notes: []
		};

		this.debugHistory = [];
		this.emitEvent('session_started', { session: this.currentSession });
		return this.currentSession;
	}

	endSession(): DebugSession | null {
		if (!this.currentSession) {
			return null;
		}

		this.currentSession.endTime = Date.now();
		this.currentSession.history = [...this.debugHistory];
		this.currentSession.validationSummary = this.generateValidationSummary();

		this.emitEvent('session_ended', { session: this.currentSession });

		const session = this.currentSession;
		this.currentSession = null;
		return session;
	}

	// ============================================================================
	// BEAT-BY-BEAT ANALYSIS
	// ============================================================================

	analyzeBeat(beatNumber: number): BeatDebugInfo | null {
		if (!this.sequenceData || !this.animationEngine) {
			return null;
		}

		// const startTime = performance.now(); // Not used currently

		// Calculate animation state
		this.animationEngine.calculateState(beatNumber);
		const blueState = this.animationEngine.getBluePropState();
		const redState = this.animationEngine.getRedPropState();

		// Get sequence step data
		const stepData = this.getStepDataForBeat(beatNumber);
		if (!stepData) {
			return null;
		}

		const { currentStep, nextStep, t } = stepData;

		// Analyze blue prop
		const blueDebugInfo = this.analyzeProp(
			'blue',
			currentStep.blue_attributes,
			nextStep.blue_attributes,
			blueState,
			beatNumber,
			t
		);

		// Analyze red prop
		const redDebugInfo = this.analyzeProp(
			'red',
			currentStep.red_attributes,
			nextStep.red_attributes,
			redState,
			beatNumber,
			t
		);

		const debugInfo: BeatDebugInfo = {
			beatNumber,
			stepIndex: Math.floor(beatNumber - 1),
			t,
			blueProps: blueDebugInfo,
			redProps: redDebugInfo,
			timestamp: Date.now()
		};

		// Store in history if recording is enabled
		if (this.configuration.recordHistory) {
			this.addToHistory(debugInfo);
		}

		// Emit event
		this.emitEvent('beat_calculated', { debugInfo });

		// const calculationTime = performance.now() - startTime; // Not used currently

		// Auto-validate if enabled
		if (this.configuration.autoValidate) {
			this.validateBeat(debugInfo);
		}

		return debugInfo;
	}

	private analyzeProp(
		propColor: 'blue' | 'red',
		currentAttrs: PropAttributes,
		nextAttrs: PropAttributes,
		propState: PropState,
		beatNumber: number,
		t: number
	): PropDebugInfo {
		// Apply overrides if they exist
		const effectiveAttrs = this.applyOverrides(currentAttrs, propColor, beatNumber);

		// Calculate coordinates
		const startCoords = mapPositionToCoordinates(effectiveAttrs.start_loc);
		const endCoords = mapPositionToCoordinates(nextAttrs.start_loc);
		const currentCoords = {
			x: startCoords.x + (endCoords.x - startCoords.x) * t,
			y: startCoords.y + (endCoords.y - startCoords.y) * t
		};

		// Calculate center path angle
		const centerPathAngle = Math.atan2(
			currentCoords.y - 475, // Grid center Y
			currentCoords.x - 475 // Grid center X
		);

		// Analyze rotation interpretation
		const interpretation = this.analyzeRotationInterpretation(effectiveAttrs, centerPathAngle, t);

		// Calculate staff rotation using the same logic as animation engine
		const staffRotationAngle = this.calculateStaffRotation(centerPathAngle, effectiveAttrs, t);

		// Validate the prop
		const validation = this.validateProp(effectiveAttrs, interpretation, beatNumber, propColor);

		return {
			attributes: effectiveAttrs,
			startCoords,
			endCoords,
			currentCoords,
			centerPathAngle,
			staffRotationAngle,
			interpretation,
			validation
		};
	}

	private analyzeRotationInterpretation(
		attrs: PropAttributes,
		centerPathAngle: number,
		t: number
	): RotationInterpretation {
		const startOriAngle = getOrientationAngle(attrs.start_ori);
		const endOriAngle = getOrientationAngle(attrs.end_ori);
		const turnsDegrees = getDegreesForTurns(attrs.turns || 0);
		const rotationDirection = attrs.prop_rot_dir;
		const isFloat = (attrs.turns || 0) === 0;

		let totalRotation = 0;
		let calculationMethod = '';
		const intermediateValues: Record<string, number> = {};

		// Calculate total rotation based on motion type
		switch (attrs.motion_type) {
			case 'pro':
				if (isFloat) {
					totalRotation = degreesToRadians(90) * getRotationMultiplier(rotationDirection);
					calculationMethod = 'pro_float';
				} else {
					const orientationChange = endOriAngle - startOriAngle;
					const turnRotation = degreesToRadians(turnsDegrees);
					const directionMultiplier = getRotationMultiplier(rotationDirection);

					totalRotation = orientationChange + turnRotation * directionMultiplier;
					calculationMethod = 'pro_standard';

					intermediateValues.orientationChange = orientationChange;
					intermediateValues.turnRotation = turnRotation;
					intermediateValues.directionMultiplier = directionMultiplier;
				}
				break;

			case 'anti':
				// Anti-spin calculation logic
				totalRotation = endOriAngle - startOriAngle;
				totalRotation += degreesToRadians(turnsDegrees) * getRotationMultiplier(rotationDirection);
				calculationMethod = 'anti_spin';
				break;

			case 'static':
				totalRotation = startOriAngle - centerPathAngle;
				calculationMethod = 'static_orientation';
				break;

			case 'dash': {
				let angleDiff = endOriAngle - startOriAngle;
				if (angleDiff > Math.PI) {
					angleDiff -= 2 * Math.PI;
				}
				if (angleDiff < -Math.PI) {
					angleDiff += 2 * Math.PI;
				}
				totalRotation = angleDiff;
				calculationMethod = 'dash_interpolation';
				intermediateValues.angleDiff = angleDiff;
				break;
			}

			default:
				totalRotation = 0;
				calculationMethod = 'none';
		}

		intermediateValues.startOriAngle = startOriAngle;
		intermediateValues.endOriAngle = endOriAngle;
		intermediateValues.centerPathAngle = centerPathAngle;
		intermediateValues.t = t;

		return {
			motionType: attrs.motion_type,
			startOriAngle,
			endOriAngle,
			turnsDegrees,
			rotationDirection: rotationDirection || 'no_rot',
			totalRotation,
			isFloat,
			calculationMethod,
			intermediateValues
		};
	}

	private calculateStaffRotation(
		centerPathAngle: number,
		attrs: PropAttributes,
		t: number
	): number {
		switch (attrs.motion_type) {
			case 'pro':
				return calculateProIsolationStaffAngle(
					attrs.start_ori,
					attrs.end_ori,
					attrs.prop_rot_dir,
					attrs.turns,
					t
				);

			case 'anti':
				return calculateAntispinTargetAngle(
					centerPathAngle,
					attrs.start_ori,
					attrs.end_ori,
					attrs.prop_rot_dir,
					attrs.turns,
					t
				);

			case 'static':
				return calculateStaticStaffAngle(centerPathAngle, attrs.start_ori);

			case 'dash':
				return calculateDashTargetAngle(centerPathAngle, attrs.start_ori, attrs.end_ori, t);

			default:
				return 0;
		}
	}

	// ============================================================================
	// VALIDATION LOGIC
	// ============================================================================

	private validateProp(
		attrs: PropAttributes,
		interpretation: RotationInterpretation,
		beatNumber: number,
		propColor: 'blue' | 'red'
	): PropValidation {
		const warnings: string[] = [];
		const errors: string[] = [];

		// Validate orientation continuity
		const orientationContinuity = this.checkOrientationContinuity(attrs, beatNumber, propColor);

		if (!orientationContinuity.isValid) {
			warnings.push(
				`Orientation discontinuity detected: expected ${orientationContinuity.expectedStartOri.toFixed(2)}, got ${orientationContinuity.actualStartOri.toFixed(2)}`
			);
		}

		// Validate turn count accuracy
		const turnCountCheck = this.checkTurnCountAccuracy(attrs, interpretation);
		if (!turnCountCheck.isValid) {
			warnings.push(
				`Turn count mismatch: expected ${turnCountCheck.expectedTurns}, calculated ${turnCountCheck.calculatedTurns.toFixed(2)}`
			);
		}

		// Check for common issues
		if (attrs.turns === undefined) {
			warnings.push('Turns value is undefined');
		}

		if (attrs.prop_rot_dir === undefined) {
			warnings.push('Rotation direction is undefined');
		}

		if (!attrs.start_ori || !attrs.end_ori) {
			warnings.push('Start or end orientation is missing');
		}

		return {
			isValid: errors.length === 0,
			warnings,
			errors,
			orientationContinuity,
			turnCountAccuracy: turnCountCheck
		};
	}

	private checkOrientationContinuity(
		attrs: PropAttributes,
		beatNumber: number,
		propColor: 'blue' | 'red'
	): OrientationContinuityCheck {
		// Get previous beat's end orientation
		const previousBeat = this.debugHistory.find((h) => h.beatNumber === beatNumber - 1);
		const previousEndOri = previousBeat
			? propColor === 'blue'
				? previousBeat.blueProps.interpretation.endOriAngle
				: previousBeat.redProps.interpretation.endOriAngle
			: undefined;

		const currentStartOri = getOrientationAngle(attrs.start_ori);

		const isValid =
			previousEndOri === undefined || Math.abs(previousEndOri - currentStartOri) < 0.01;

		return {
			isValid,
			expectedStartOri: previousEndOri || currentStartOri,
			actualStartOri: currentStartOri,
			difference: previousEndOri ? Math.abs(previousEndOri - currentStartOri) : 0,
			previousBeatEndOri: previousEndOri
		};
	}

	private checkTurnCountAccuracy(
		attrs: PropAttributes,
		interpretation: RotationInterpretation
	): TurnCountCheck {
		const expectedTurns = attrs.turns || 0;
		const calculatedTurns = Math.abs(interpretation.totalRotation) / (2 * Math.PI);
		const difference = Math.abs(expectedTurns - calculatedTurns);

		return {
			isValid: difference < 0.1, // Allow small tolerance
			expectedTurns,
			calculatedTurns,
			difference
		};
	}

	// ============================================================================
	// UTILITY METHODS
	// ============================================================================

	private createDefaultConfiguration(config?: Partial<DebugConfiguration>): DebugConfiguration {
		return {
			enabled: true,
			captureMode: 'realtime',
			validationLevel: 'detailed',
			visualizationMode: 'modal',
			autoValidate: true,
			recordHistory: true,
			maxHistorySize: 1000,
			...config
		};
	}

	private createDefaultOverrides(): DebugOverrides {
		return {
			beatOverrides: new Map(),
			globalOverrides: {}
		};
	}

	private generateSessionId(): string {
		return `debug_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
	}

	private createEmptyValidationSummary(): ValidationSummary {
		return {
			totalBeats: 0,
			validBeats: 0,
			warningCount: 0,
			errorCount: 0,
			orientationIssues: 0,
			turnCountIssues: 0,
			commonIssues: []
		};
	}

	private cloneOverrides(overrides: DebugOverrides): DebugOverrides {
		return {
			beatOverrides: new Map(overrides.beatOverrides),
			globalOverrides: { ...overrides.globalOverrides }
		};
	}

	private addToHistory(debugInfo: BeatDebugInfo): void {
		this.debugHistory.push(debugInfo);

		// Limit history size
		if (this.debugHistory.length > this.configuration.maxHistorySize) {
			this.debugHistory.shift();
		}
	}

	private emitEvent(type: string, data: any): void {
		const listeners = this.eventListeners.get(type) || [];
		listeners.forEach((listener) => listener(data));
	}

	private getStepDataForBeat(beatNumber: number) {
		if (!this.sequenceData) {
			return null;
		}

		const steps = this.sequenceData.slice(2) as SequenceStep[];
		const stepIndex = Math.floor(beatNumber - 1);
		const nextStepIndex = stepIndex + 1;
		const t = beatNumber - 1 - stepIndex;

		const currentStep = steps[stepIndex];
		const nextStep = steps[nextStepIndex] || steps[stepIndex];

		if (!currentStep) {
			return null;
		}

		return { currentStep, nextStep, t };
	}

	private applyOverrides(
		attrs: PropAttributes,
		propColor: 'blue' | 'red',
		beatNumber: number
	): PropAttributes {
		const beatOverride = this.overrides.beatOverrides.get(beatNumber);
		if (!beatOverride || !beatOverride.enabled) {
			return attrs;
		}

		const propOverride =
			propColor === 'blue' ? beatOverride.blueOverrides : beatOverride.redOverrides;
		if (!propOverride) {
			return attrs;
		}

		return {
			...attrs,
			...propOverride
		};
	}

	private validateBeat(debugInfo: BeatDebugInfo): void {
		// Validation logic is already included in analyzeProp
		this.emitEvent('validation_completed', { debugInfo });
	}

	private generateValidationSummary(): ValidationSummary {
		const summary = this.createEmptyValidationSummary();
		summary.totalBeats = this.debugHistory.length;

		this.debugHistory.forEach((beat) => {
			if (beat.blueProps.validation.isValid && beat.redProps.validation.isValid) {
				summary.validBeats++;
			}

			summary.warningCount +=
				beat.blueProps.validation.warnings.length + beat.redProps.validation.warnings.length;
			summary.errorCount +=
				beat.blueProps.validation.errors.length + beat.redProps.validation.errors.length;

			if (
				!beat.blueProps.validation.orientationContinuity.isValid ||
				!beat.redProps.validation.orientationContinuity.isValid
			) {
				summary.orientationIssues++;
			}

			if (
				!beat.blueProps.validation.turnCountAccuracy.isValid ||
				!beat.redProps.validation.turnCountAccuracy.isValid
			) {
				summary.turnCountIssues++;
			}
		});

		return summary;
	}

	// ============================================================================
	// PUBLIC API
	// ============================================================================

	getConfiguration(): DebugConfiguration {
		return { ...this.configuration };
	}

	updateConfiguration(config: Partial<DebugConfiguration>): void {
		this.configuration = { ...this.configuration, ...config };
		this.emitEvent('configuration_changed', { configuration: this.configuration });
	}

	getOverrides(): DebugOverrides {
		return this.cloneOverrides(this.overrides);
	}

	setOverrides(overrides: Partial<DebugOverrides>): void {
		if (overrides.beatOverrides) {
			this.overrides.beatOverrides = overrides.beatOverrides;
		}
		if (overrides.globalOverrides) {
			this.overrides.globalOverrides = {
				...this.overrides.globalOverrides,
				...overrides.globalOverrides
			};
		}
		this.emitEvent('override_applied', { overrides: this.overrides });
	}

	getHistory(): BeatDebugInfo[] {
		return [...this.debugHistory];
	}

	getCurrentSession(): DebugSession | null {
		return this.currentSession;
	}

	addEventListener(type: string, listener: Function): void {
		if (!this.eventListeners.has(type)) {
			this.eventListeners.set(type, []);
		}
		this.eventListeners.get(type)!.push(listener);
	}

	removeEventListener(type: string, listener: Function): void {
		const listeners = this.eventListeners.get(type);
		if (listeners) {
			const index = listeners.indexOf(listener);
			if (index > -1) {
				listeners.splice(index, 1);
			}
		}
	}
}
