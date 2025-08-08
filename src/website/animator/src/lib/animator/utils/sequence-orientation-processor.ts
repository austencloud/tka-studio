/**
 * Sequence orientation processor - applies finalized orientation mappings to sequence data
 * This replaces dynamic orientation calculations with precise, manually-validated rotation angles
 */

import type { SequenceData, SequenceStep, PropAttributes } from '../types/core.js';
import { getOrientationAngleRadians } from './orientation-mapping.js';
import { setManualRotationRadians } from './manual-rotation.js';

/**
 * Process a complete sequence to use orientation-based rotations
 * This is the main function to integrate the finalized orientation mappings
 */
export function processSequenceWithOrientationMappings(sequenceData: SequenceData): SequenceData {
	// Processing sequence with finalized orientation mappings

	const [metadata, ...steps] = sequenceData;

	const processedSteps = steps.map((step, _index) => {
		const sequenceStep = step as SequenceStep;
		const processedStep = { ...sequenceStep };

		// Process blue prop attributes
		if (shouldApplyOrientationMapping(sequenceStep.blue_attributes)) {
			processedStep.blue_attributes = applyOrientationMappingToAttributes(
				sequenceStep.blue_attributes,
				`Beat ${sequenceStep.beat} Blue`
			);
		}

		// Process red prop attributes
		if (shouldApplyOrientationMapping(sequenceStep.red_attributes)) {
			processedStep.red_attributes = applyOrientationMappingToAttributes(
				sequenceStep.red_attributes,
				`Beat ${sequenceStep.beat} Red`
			);
		}

		return processedStep;
	});

	// Processed sequence steps with orientation mappings
	return [metadata, ...processedSteps];
}

/**
 * Check if orientation mapping should be applied to prop attributes
 */
function shouldApplyOrientationMapping(attributes: PropAttributes): boolean {
	// Only apply if we have both start and end orientations
	// and don't already have manual rotation overrides
	return (
		attributes.start_ori !== undefined &&
		attributes.end_ori !== undefined &&
		attributes.manual_start_rotation === undefined &&
		attributes.manual_end_rotation === undefined
	);
}

/**
 * Apply orientation mapping to prop attributes
 */
function applyOrientationMappingToAttributes(
	attributes: PropAttributes,
	_context: string = ''
): PropAttributes {
	if (!attributes.start_ori || !attributes.end_ori) {
		// Missing orientation data, skipping orientation mapping
		return attributes;
	}

	// Get rotation angles from the finalized orientation mappings
	const startAngleRadians = getOrientationAngleRadians(attributes.start_loc, attributes.start_ori);
	const endAngleRadians = getOrientationAngleRadians(attributes.end_loc, attributes.end_ori);

	// Applied orientation mapping with calculated angles

	// Apply manual rotation using the mapped angles
	return setManualRotationRadians(
		attributes,
		startAngleRadians,
		endAngleRadians,
		'shortest' // Use shortest path for smooth transitions
	);
}

/**
 * Validate sequence data integrity for orientation processing
 */
export function validateSequenceOrientationIntegrity(sequenceData: SequenceData): {
	isValid: boolean;
	errors: string[];
	warnings: string[];
} {
	const errors: string[] = [];
	const warnings: string[] = [];

	const [_metadata, ...steps] = sequenceData;
	const sequenceSteps = steps as SequenceStep[];

	// Check for orientation continuity between beats
	for (let i = 0; i < sequenceSteps.length - 1; i++) {
		const currentStep = sequenceSteps[i];
		const nextStep = sequenceSteps[i + 1];

		// Check blue prop continuity
		if (currentStep.blue_attributes.end_ori !== nextStep.blue_attributes.start_ori) {
			errors.push(
				`Beat ${currentStep.beat} → ${nextStep.beat}: Blue prop orientation mismatch. ` +
					`End orientation '${currentStep.blue_attributes.end_ori}' does not match ` +
					`next start orientation '${nextStep.blue_attributes.start_ori}'`
			);
		}

		// Check red prop continuity
		if (currentStep.red_attributes.end_ori !== nextStep.red_attributes.start_ori) {
			errors.push(
				`Beat ${currentStep.beat} → ${nextStep.beat}: Red prop orientation mismatch. ` +
					`End orientation '${currentStep.red_attributes.end_ori}' does not match ` +
					`next start orientation '${nextStep.red_attributes.start_ori}'`
			);
		}
	}

	// Check for missing orientations
	sequenceSteps.forEach((step) => {
		if (!step.blue_attributes.start_ori || !step.blue_attributes.end_ori) {
			warnings.push(`Beat ${step.beat}: Blue prop missing orientation data`);
		}
		if (!step.red_attributes.start_ori || !step.red_attributes.end_ori) {
			warnings.push(`Beat ${step.beat}: Red prop missing orientation data`);
		}
	});

	return {
		isValid: errors.length === 0,
		errors,
		warnings
	};
}

/**
 * Generate a report comparing original vs orientation-processed sequence
 */
export function generateOrientationProcessingReport(
	originalSequence: SequenceData,
	processedSequence: SequenceData
): string {
	const report = ['# Orientation Processing Report\n'];

	const [, ...originalSteps] = originalSequence;
	const [, ...processedSteps] = processedSequence;

	report.push(`## Summary`);
	report.push(`- Original steps: ${originalSteps.length}`);
	report.push(`- Processed steps: ${processedSteps.length}`);
	report.push(`- Processing date: ${new Date().toISOString()}\n`);

	report.push(`## Step-by-Step Changes\n`);

	for (let i = 0; i < Math.min(originalSteps.length, processedSteps.length); i++) {
		const originalStep = originalSteps[i] as SequenceStep;
		const processedStep = processedSteps[i] as SequenceStep;

		report.push(`### Beat ${originalStep.beat}`);

		// Blue prop changes
		const blueHasManualRotation = processedStep.blue_attributes.manual_start_rotation !== undefined;
		report.push(`**Blue Prop:**`);
		report.push(
			`- Position: ${originalStep.blue_attributes.start_loc} → ${originalStep.blue_attributes.end_loc}`
		);
		report.push(
			`- Orientation: ${originalStep.blue_attributes.start_ori} → ${originalStep.blue_attributes.end_ori}`
		);
		report.push(`- Manual rotation applied: ${blueHasManualRotation ? 'Yes' : 'No'}`);

		// Red prop changes
		const redHasManualRotation = processedStep.red_attributes.manual_start_rotation !== undefined;
		report.push(`**Red Prop:**`);
		report.push(
			`- Position: ${originalStep.red_attributes.start_loc} → ${originalStep.red_attributes.end_loc}`
		);
		report.push(
			`- Orientation: ${originalStep.red_attributes.start_ori} → ${originalStep.red_attributes.end_ori}`
		);
		report.push(`- Manual rotation applied: ${redHasManualRotation ? 'Yes' : 'No'}`);
		report.push('');
	}

	return report.join('\n');
}

/**
 * Export the finalized orientation mappings for external use
 */
export function exportFinalizedOrientationMappings(): string {
	return JSON.stringify(
		{
			n_hand: { in: 90, out: 270, clockwise: 90, counter: 180 },
			e_hand: { in: 180, out: 0, clockwise: 90, counter: 270 },
			s_hand: { in: 270, out: 90, clockwise: 180, counter: 270 },
			w_hand: { in: 0, out: 180, clockwise: 270, counter: 90 },
			ne: { in: 135, out: 315, clockwise: 45, counter: 225 },
			se: { in: 225, out: 45, clockwise: 135, counter: 315 },
			sw: { in: 315, out: 135, clockwise: 225, counter: 45 },
			nw: { in: 45, out: 225, clockwise: 315, counter: 135 }
		},
		null,
		2
	);
}
