/**
 * Type definitions for the sequence interpretation debugging system
 */

import type {
	PropAttributes,
	// SequenceStep, // Not used currently
	// PropState, // Not used currently
	MotionType,
	PropRotDir,
	Orientation
} from './core.js';

// ============================================================================
// DEBUGGING STATE TYPES
// ============================================================================

export interface BeatDebugInfo {
	beatNumber: number;
	stepIndex: number;
	t: number; // Interpolation factor (0-1)
	blueProps: PropDebugInfo;
	redProps: PropDebugInfo;
	timestamp: number;
}

export interface PropDebugInfo {
	// Input attributes
	attributes: PropAttributes;

	// Calculated values
	startCoords: { x: number; y: number };
	endCoords: { x: number; y: number };
	currentCoords: { x: number; y: number };
	centerPathAngle: number;
	staffRotationAngle: number;

	// Interpretation details
	interpretation: RotationInterpretation;

	// Validation results
	validation: PropValidation;
}

export interface RotationInterpretation {
	motionType: MotionType;
	startOriAngle: number;
	endOriAngle: number;
	turnsDegrees: number;
	rotationDirection: PropRotDir;
	totalRotation: number;
	isFloat: boolean;
	calculationMethod: string;
	intermediateValues: Record<string, number>;
}

export interface PropValidation {
	isValid: boolean;
	warnings: string[];
	errors: string[];
	orientationContinuity: OrientationContinuityCheck;
	turnCountAccuracy: TurnCountCheck;
}

export interface OrientationContinuityCheck {
	isValid: boolean;
	expectedStartOri: number;
	actualStartOri: number;
	difference: number;
	previousBeatEndOri?: number;
}

export interface TurnCountCheck {
	isValid: boolean;
	expectedTurns: number;
	calculatedTurns: number;
	difference: number;
}

// ============================================================================
// DEBUGGING CONFIGURATION TYPES
// ============================================================================

export interface DebugConfiguration {
	enabled: boolean;
	captureMode: 'realtime' | 'manual' | 'step';
	validationLevel: 'basic' | 'detailed' | 'comprehensive';
	visualizationMode: 'overlay' | 'sidebyside' | 'modal';
	autoValidate: boolean;
	recordHistory: boolean;
	maxHistorySize: number;
}

export interface DebugOverrides {
	beatOverrides: Map<number, BeatOverride>;
	globalOverrides: GlobalOverrides;
}

export interface BeatOverride {
	beatNumber: number;
	blueOverrides?: PropOverride;
	redOverrides?: PropOverride;
	enabled: boolean;
}

export interface PropOverride {
	motionType?: MotionType;
	startOri?: Orientation;
	endOri?: Orientation;
	propRotDir?: PropRotDir;
	turns?: number;
	startLoc?: string;
	endLoc?: string;
}

export interface GlobalOverrides {
	turnToDegreesMapping?: Record<number, number>;
	orientationToAngleMapping?: Record<string, number>;
	motionTypeConfig?: Record<MotionType, any>;
}

// ============================================================================
// DEBUGGING SESSION TYPES
// ============================================================================

export interface DebugSession {
	id: string;
	sequenceId: string;
	sequenceWord: string;
	startTime: number;
	endTime?: number;
	configuration: DebugConfiguration;
	overrides: DebugOverrides;
	history: BeatDebugInfo[];
	validationSummary: ValidationSummary;
	notes: string[];
}

export interface ValidationSummary {
	totalBeats: number;
	validBeats: number;
	warningCount: number;
	errorCount: number;
	orientationIssues: number;
	turnCountIssues: number;
	commonIssues: string[];
}

// ============================================================================
// DEBUGGING INTERFACE TYPES
// ============================================================================

export interface DebugModalState {
	isOpen: boolean;
	activeTab: 'overview' | 'beatEditor' | 'validation' | 'configuration' | 'export';
	selectedBeat: number | null;
	selectedProp: 'blue' | 'red' | null;
	viewMode: 'table' | 'graph' | 'timeline';
}

export interface BeatEditorState {
	editingBeat: number | null;
	originalAttributes: PropAttributes | null;
	modifiedAttributes: PropAttributes | null;
	previewMode: boolean;
	showComparison: boolean;
}

export interface ValidationDisplayState {
	filterLevel: 'all' | 'errors' | 'warnings';
	sortBy: 'beat' | 'severity' | 'type';
	expandedItems: Set<string>;
	showDetails: boolean;
}

// ============================================================================
// UTILITY TYPES
// ============================================================================

export type DebugEventType =
	| 'beat_calculated'
	| 'validation_completed'
	| 'override_applied'
	| 'configuration_changed'
	| 'session_started'
	| 'session_ended';

export interface DebugEvent {
	type: DebugEventType;
	timestamp: number;
	data: any;
	beatNumber?: number;
}

export interface DebugMetrics {
	calculationTime: number;
	validationTime: number;
	renderTime: number;
	memoryUsage: number;
	frameRate: number;
}

// ============================================================================
// EXPORT TYPES
// ============================================================================

export interface DebugExport {
	session: DebugSession;
	rawData: BeatDebugInfo[];
	configuration: DebugConfiguration;
	validationResults: ValidationSummary;
	exportTime: number;
	version: string;
}

export interface DebugImport {
	data: DebugExport;
	isValid: boolean;
	errors: string[];
	warnings: string[];
}
