/**
 * Integration utilities for connecting orientation test data with the animation system
 */

import type { PropAttributes, SequenceStep, SequenceData } from '../types/core.js';
import { setManualRotationRadians } from './manual-rotation.js';
import {
	getOrientationAngleRadians,
	loadOrientationMappingsFromJSON
} from './orientation-mapping.js';

/**
 * Apply orientation-based manual rotations to a sequence step
 */
export function applyOrientationBasedRotations(step: SequenceStep): SequenceStep {
	const updatedStep = { ...step };

	// Apply to blue attributes
	if (step.blue_attributes.start_ori && step.blue_attributes.end_ori) {
		const startAngle = getOrientationAngleRadians(
			step.blue_attributes.start_loc,
			step.blue_attributes.start_ori
		);
		const endAngle = getOrientationAngleRadians(
			step.blue_attributes.end_loc,
			step.blue_attributes.end_ori
		);

		updatedStep.blue_attributes = setManualRotationRadians(
			step.blue_attributes,
			startAngle,
			endAngle,
			'shortest'
		);
	}

	// Apply to red attributes
	if (step.red_attributes.start_ori && step.red_attributes.end_ori) {
		const startAngle = getOrientationAngleRadians(
			step.red_attributes.start_loc,
			step.red_attributes.start_ori
		);
		const endAngle = getOrientationAngleRadians(
			step.red_attributes.end_loc,
			step.red_attributes.end_ori
		);

		updatedStep.red_attributes = setManualRotationRadians(
			step.red_attributes,
			startAngle,
			endAngle,
			'shortest'
		);
	}

	return updatedStep;
}

/**
 * Apply orientation-based manual rotations to an entire sequence
 */
export function applyOrientationBasedRotationsToSequence(sequenceData: SequenceData): SequenceData {
	const [metadata, startPosition, ...steps] = sequenceData;

	// Apply to start position
	const updatedStartPosition = applyOrientationBasedRotations(startPosition as SequenceStep);

	// Apply to all steps
	const updatedSteps = steps.map((step) => applyOrientationBasedRotations(step as SequenceStep));

	return [metadata, updatedStartPosition, ...updatedSteps];
}

/**
 * Create a prop attributes object with orientation-based manual rotation
 */
export function createPropAttributesWithOrientation(
	startLoc: string,
	endLoc: string,
	startOri: string,
	endOri: string,
	motionType: string = 'static',
	propRotDir: string = 'no_rot',
	turns: number = 0
): PropAttributes {
	const baseAttributes: PropAttributes = {
		start_loc: startLoc,
		end_loc: endLoc,
		start_ori: startOri as any,
		end_ori: endOri as any,
		motion_type: motionType as any,
		prop_rot_dir: propRotDir as any,
		turns
	};

	// Apply orientation-based rotation
	if (startOri && endOri) {
		const startAngle = getOrientationAngleRadians(startLoc, startOri as any);
		const endAngle = getOrientationAngleRadians(endLoc, endOri as any);

		return setManualRotationRadians(baseAttributes, startAngle, endAngle, 'shortest');
	}

	return baseAttributes;
}

/**
 * Batch convert sequence data to use orientation-based rotations
 */
export function convertSequenceToOrientationBased(
	sequenceData: SequenceData,
	options: {
		preserveExistingManualRotations?: boolean;
		overrideMotionTypes?: boolean;
		defaultDirection?: 'cw' | 'ccw' | 'shortest';
	} = {}
): SequenceData {
	const {
		preserveExistingManualRotations = false,
		overrideMotionTypes = false,
		defaultDirection = 'shortest'
	} = options;

	return sequenceData.map((item, index) => {
		// Skip metadata
		if (index === 0) {
			return item;
		}

		const step = item as SequenceStep;
		const updatedStep = { ...step };

		// Process blue attributes
		if (shouldApplyOrientationRotation(step.blue_attributes, preserveExistingManualRotations)) {
			updatedStep.blue_attributes = applyOrientationToAttributes(
				step.blue_attributes,
				overrideMotionTypes,
				defaultDirection
			);
		}

		// Process red attributes
		if (shouldApplyOrientationRotation(step.red_attributes, preserveExistingManualRotations)) {
			updatedStep.red_attributes = applyOrientationToAttributes(
				step.red_attributes,
				overrideMotionTypes,
				defaultDirection
			);
		}

		return updatedStep;
	}) as SequenceData;
}

/**
 * Check if orientation rotation should be applied to attributes
 */
function shouldApplyOrientationRotation(
	attributes: PropAttributes,
	preserveExisting: boolean
): boolean {
	// Don't apply if preserving existing manual rotations and they exist
	if (preserveExisting && attributes.manual_start_rotation !== undefined) {
		return false;
	}

	// Only apply if both start and end orientations are defined
	return attributes.start_ori !== undefined && attributes.end_ori !== undefined;
}

/**
 * Apply orientation-based rotation to prop attributes
 */
function applyOrientationToAttributes(
	attributes: PropAttributes,
	overrideMotionType: boolean,
	defaultDirection: 'cw' | 'ccw' | 'shortest'
): PropAttributes {
	if (!attributes.start_ori || !attributes.end_ori) {
		return attributes;
	}

	const startAngle = getOrientationAngleRadians(attributes.start_loc, attributes.start_ori);
	const endAngle = getOrientationAngleRadians(attributes.end_loc, attributes.end_ori);

	let updatedAttributes = setManualRotationRadians(
		attributes,
		startAngle,
		endAngle,
		defaultDirection
	);

	// Optionally override motion type to indicate this is orientation-based
	if (overrideMotionType) {
		updatedAttributes = {
			...updatedAttributes,
			motion_type: 'static' // or create a new motion type like 'orientation'
		};
	}

	return updatedAttributes;
}

/**
 * Load test interface data and apply it to a sequence
 */
export async function loadTestDataAndApplyToSequence(
	testDataFile: File,
	sequenceData: SequenceData
): Promise<SequenceData> {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.onload = (e) => {
			try {
				const jsonData = e.target?.result as string;
				const success = loadOrientationMappingsFromJSON(jsonData);

				if (success) {
					const updatedSequence = applyOrientationBasedRotationsToSequence(sequenceData);
					resolve(updatedSequence);
				} else {
					reject(new Error('Failed to load orientation mappings from file'));
				}
			} catch (error) {
				reject(error);
			}
		};
		reader.onerror = () => reject(new Error('Failed to read file'));
		reader.readAsText(testDataFile);
	});
}

/**
 * Create a validation report for orientation-based sequence conversion
 */
export function validateOrientationBasedSequence(sequenceData: SequenceData): {
	isValid: boolean;
	errors: string[];
	warnings: string[];
	stats: {
		totalSteps: number;
		stepsWithOrientations: number;
		stepsWithManualRotations: number;
		missingOrientations: Array<{
			beat: number;
			prop: 'blue' | 'red';
			missing: 'start_ori' | 'end_ori' | 'both';
		}>;
	};
} {
	const errors: string[] = [];
	const warnings: string[] = [];
	const missingOrientations: Array<{
		beat: number;
		prop: 'blue' | 'red';
		missing: 'start_ori' | 'end_ori' | 'both';
	}> = [];

	let totalSteps = 0;
	let stepsWithOrientations = 0;
	let stepsWithManualRotations = 0;

	sequenceData.slice(1).forEach((item, _index) => {
		const step = item as SequenceStep;
		totalSteps++;

		// Check blue attributes
		const blueHasStartOri = step.blue_attributes.start_ori !== undefined;
		const blueHasEndOri = step.blue_attributes.end_ori !== undefined;
		const blueHasManualRotation = step.blue_attributes.manual_start_rotation !== undefined;

		if (blueHasStartOri && blueHasEndOri) {
			stepsWithOrientations++;
		} else if (blueHasStartOri || blueHasEndOri) {
			const missing = !blueHasStartOri ? 'start_ori' : 'end_ori';
			missingOrientations.push({ beat: step.beat, prop: 'blue', missing });
			warnings.push(`Step ${step.beat}: Blue prop missing ${missing}`);
		}

		if (blueHasManualRotation) {
			stepsWithManualRotations++;
		}

		// Check red attributes
		const redHasStartOri = step.red_attributes.start_ori !== undefined;
		const redHasEndOri = step.red_attributes.end_ori !== undefined;
		const redHasManualRotation = step.red_attributes.manual_start_rotation !== undefined;

		if (redHasStartOri && redHasEndOri) {
			stepsWithOrientations++;
		} else if (redHasStartOri || redHasEndOri) {
			const missing = !redHasStartOri ? 'start_ori' : 'end_ori';
			missingOrientations.push({ beat: step.beat, prop: 'red', missing });
			warnings.push(`Step ${step.beat}: Red prop missing ${missing}`);
		}

		if (redHasManualRotation) {
			stepsWithManualRotations++;
		}
	});

	return {
		isValid: errors.length === 0,
		errors,
		warnings,
		stats: {
			totalSteps,
			stepsWithOrientations,
			stepsWithManualRotations,
			missingOrientations
		}
	};
}

/**
 * Generate a report comparing dynamic vs orientation-based rotations
 */
export function generateRotationComparisonReport(
	originalSequence: SequenceData,
	orientationBasedSequence: SequenceData
): string {
	const report = ['# Rotation Comparison Report\n'];

	report.push('## Summary');
	report.push(`- Original sequence steps: ${originalSequence.length - 1}`);
	report.push(`- Orientation-based sequence steps: ${orientationBasedSequence.length - 1}\n`);

	report.push('## Step-by-Step Comparison\n');

	for (let i = 1; i < Math.min(originalSequence.length, orientationBasedSequence.length); i++) {
		const originalStep = originalSequence[i] as SequenceStep;
		const orientationStep = orientationBasedSequence[i] as SequenceStep;

		report.push(`### Beat ${originalStep.beat}`);

		// Blue prop comparison
		report.push('**Blue Prop:**');
		report.push(`- Original: ${originalStep.blue_attributes.motion_type} motion`);
		report.push(
			`- Orientation-based: Manual rotation ${orientationStep.blue_attributes.manual_start_rotation !== undefined ? 'applied' : 'not applied'}`
		);

		// Red prop comparison
		report.push('**Red Prop:**');
		report.push(`- Original: ${originalStep.red_attributes.motion_type} motion`);
		report.push(
			`- Orientation-based: Manual rotation ${orientationStep.red_attributes.manual_start_rotation !== undefined ? 'applied' : 'not applied'}`
		);
		report.push('');
	}

	return report.join('\n');
}
