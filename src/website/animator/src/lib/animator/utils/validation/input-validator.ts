/**
 * Input validation utilities for the animator
 */

import type { /* SequenceData, */ SequenceStep, PropAttributes } from '../../types/core.js';
import { validateManualRotation } from '../manual-rotation.js';

export interface ValidationResult {
	isValid: boolean;
	errors: string[];
	warnings: string[];
}

export class InputValidator {
	/**
	 * Validate speed input
	 */
	static validateSpeed(speed: number): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (isNaN(speed)) {
			errors.push('Speed must be a valid number');
		} else if (speed < 0.1) {
			errors.push('Speed must be at least 0.1x');
		} else if (speed > 3.0) {
			errors.push('Speed must not exceed 3.0x');
		} else if (speed > 2.0) {
			warnings.push('High speeds may cause visual artifacts');
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}

	/**
	 * Validate beat input
	 */
	static validateBeat(beat: number, maxBeat: number): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (isNaN(beat)) {
			errors.push('Beat must be a valid number');
		} else if (beat < 0) {
			errors.push('Beat cannot be negative');
		} else if (beat > maxBeat) {
			errors.push(`Beat cannot exceed ${maxBeat}`);
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}

	/**
	 * Validate canvas dimensions
	 */
	static validateCanvasDimensions(width: number, height: number): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (isNaN(width) || isNaN(height)) {
			errors.push('Canvas dimensions must be valid numbers');
		} else {
			if (width < 100 || height < 100) {
				errors.push('Canvas dimensions must be at least 100x100 pixels');
			} else if (width > 2000 || height > 2000) {
				warnings.push('Large canvas dimensions may impact performance');
			}

			if (width !== height) {
				warnings.push('Non-square canvas may cause visual distortion');
			}
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}

	/**
	 * Validate sequence data structure
	 */
	static validateSequenceData(data: unknown): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (!Array.isArray(data)) {
			errors.push('Sequence data must be an array');
			return { isValid: false, errors, warnings };
		}

		if (data.length < 2) {
			errors.push('Sequence must contain at least metadata and one step');
			return { isValid: false, errors, warnings };
		}

		// Validate metadata (first element)
		const metadata = data[0];
		if (typeof metadata !== 'object' || metadata === null) {
			errors.push('First element must be metadata object');
		} else {
			if (!metadata.word || typeof metadata.word !== 'string') {
				warnings.push('Metadata should include a word property');
			}
			if (!metadata.author || typeof metadata.author !== 'string') {
				warnings.push('Metadata should include an author property');
			}
		}

		// Validate steps
		const steps = data.slice(1) as SequenceStep[];
		for (let i = 0; i < steps.length; i++) {
			const stepValidation = this.validateSequenceStep(steps[i], i + 1);
			errors.push(...stepValidation.errors);
			warnings.push(...stepValidation.warnings);
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}

	/**
	 * Validate a single sequence step
	 */
	static validateSequenceStep(step: SequenceStep, stepNumber: number): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (typeof step !== 'object' || step === null) {
			errors.push(`Step ${stepNumber}: Must be an object`);
			return { isValid: false, errors, warnings };
		}

		// Validate beat number
		if (typeof step.beat !== 'number' || isNaN(step.beat)) {
			errors.push(`Step ${stepNumber}: Beat must be a valid number`);
		} else if (step.beat < 0) {
			errors.push(`Step ${stepNumber}: Beat cannot be negative`);
		}

		// Validate prop attributes
		const blueValidation = this.validatePropAttributes(
			step.blue_attributes,
			`Step ${stepNumber} Blue`
		);
		const redValidation = this.validatePropAttributes(
			step.red_attributes,
			`Step ${stepNumber} Red`
		);

		errors.push(...blueValidation.errors, ...redValidation.errors);
		warnings.push(...blueValidation.warnings, ...redValidation.warnings);

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}

	/**
	 * Validate prop attributes
	 */
	static validatePropAttributes(attrs: PropAttributes, context: string): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (typeof attrs !== 'object' || attrs === null) {
			errors.push(`${context}: Attributes must be an object`);
			return { isValid: false, errors, warnings };
		}

		// Validate required fields
		const requiredFields = ['start_loc', 'end_loc', 'motion_type'];
		for (const field of requiredFields) {
			if (!(field in attrs) || attrs[field as keyof PropAttributes] === undefined) {
				errors.push(`${context}: Missing required field '${field}'`);
			}
		}

		// Validate motion type
		const validMotionTypes = ['static', 'pro', 'anti', 'dash', 'fl'];
		if (attrs.motion_type && !validMotionTypes.includes(attrs.motion_type)) {
			errors.push(`${context}: Invalid motion_type '${attrs.motion_type}'`);
		}

		// Validate locations - include all diamond grid positions
		const validLocations = [
			// Cardinal directions (outer diamond points)
			'n',
			'e',
			's',
			'w',
			// Diagonal directions (layer2 points)
			'ne',
			'se',
			'sw',
			'nw',
			// Hand points
			'n_hand',
			'e_hand',
			's_hand',
			'w_hand',
			// Strict variants
			'ne_strict',
			'se_strict',
			'sw_strict',
			'nw_strict',
			'n_hand_strict',
			'e_hand_strict',
			's_hand_strict',
			'w_hand_strict',
			// Center
			'center'
		];
		if (attrs.start_loc && !validLocations.includes(attrs.start_loc)) {
			errors.push(`${context}: Invalid start_loc '${attrs.start_loc}'`);
		}
		if (attrs.end_loc && !validLocations.includes(attrs.end_loc)) {
			errors.push(`${context}: Invalid end_loc '${attrs.end_loc}'`);
		}

		// Validate orientations
		const validOrientations = ['in', 'out', 'n', 'e', 's', 'w'];
		if (attrs.start_ori && !validOrientations.includes(attrs.start_ori)) {
			warnings.push(`${context}: Unusual start_ori '${attrs.start_ori}'`);
		}
		if (attrs.end_ori && !validOrientations.includes(attrs.end_ori)) {
			warnings.push(`${context}: Unusual end_ori '${attrs.end_ori}'`);
		}

		// Validate rotation direction
		if (attrs.prop_rot_dir && !['cw', 'ccw', 'no_rot'].includes(attrs.prop_rot_dir)) {
			errors.push(`${context}: Invalid prop_rot_dir '${attrs.prop_rot_dir}'`);
		}

		// Validate turns
		if (attrs.turns !== undefined) {
			if (typeof attrs.turns !== 'number' || isNaN(attrs.turns)) {
				errors.push(`${context}: Turns must be a valid number`);
			} else if (attrs.turns < 0) {
				errors.push(`${context}: Turns cannot be negative`);
			} else if (attrs.turns > 10) {
				warnings.push(
					`${context}: High number of turns (${attrs.turns}) may be difficult to visualize`
				);
			}
		}

		// Validate manual rotation fields
		const manualRotationValidation = validateManualRotation(attrs);
		if (!manualRotationValidation.isValid) {
			errors.push(...manualRotationValidation.errors.map((error) => `${context}: ${error}`));
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}

	/**
	 * Validate file type for import
	 */
	static validateFileType(file: File): ValidationResult {
		const errors: string[] = [];
		const warnings: string[] = [];

		if (!file.type.startsWith('image/')) {
			errors.push('File must be an image');
		} else if (file.type !== 'image/png') {
			errors.push('Only PNG files are supported for sequence import');
		}

		if (file.size > 10 * 1024 * 1024) {
			// 10MB
			warnings.push('Large file size may take longer to process');
		}

		return {
			isValid: errors.length === 0,
			errors,
			warnings
		};
	}
}
