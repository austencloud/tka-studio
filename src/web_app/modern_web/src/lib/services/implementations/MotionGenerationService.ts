/**
 * Motion Generation Service - Generate individual motions
 * 
 * This service will eventually port the motion generation algorithms
 * from the desktop application. For now, it provides basic motion generation.
 */

import type { MotionData, BeatData } from '@tka/schemas';
import type { 
	IMotionGenerationService,
	GenerationOptions 
} from '../interfaces';

export class MotionGenerationService implements IMotionGenerationService {

	/**
	 * Generate a motion for a specific color
	 */
	async generateMotion(
		color: 'blue' | 'red',
		options: GenerationOptions,
		previousBeats: BeatData[]
	): Promise<MotionData> {
		try {
			console.log(`Generating ${color} motion`);

			// Basic motion generation (placeholder)
			const motionTypes = ['pro', 'anti', 'float', 'dash', 'static'] as const;
			const locations = ['n', 'e', 's', 'w', 'ne', 'se', 'sw', 'nw'] as const;
			const orientations = ['in', 'out', 'clock', 'counter'] as const;
			const rotationDirections = ['cw', 'ccw', 'no_rot'] as const;

			// Simple random selection (will be replaced with proper algorithms)
			const motionType = this.randomChoice(motionTypes);
			const startLoc = this.randomChoice(locations);
			const endLoc = this.randomChoice(locations);
			const startOri = this.randomChoice(orientations);
			const endOri = this.randomChoice(orientations);
			const propRotDir = this.randomChoice(rotationDirections);

			// Calculate turns based on motion type and locations
			const turns = this.calculateTurns(motionType, startLoc, endLoc);

			const motion: MotionData = {
				motionType,
				propRotDir,
				startLoc,
				endLoc,
				turns,
				startOri,
				endOri
			};

			console.log(`Generated ${color} motion:`, motion);
			return motion;
		} catch (error) {
			console.error(`Failed to generate ${color} motion:`, error);
			throw new Error(`Motion generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	/**
	 * Calculate turns for a motion
	 */
	private calculateTurns(
		motionType: string,
		startLoc: string,
		endLoc: string
	): number {
		// Simple turn calculation (placeholder)
		if (motionType === 'static') return 0;
		if (motionType === 'dash') return 0;
		
		// For pro/anti/float, calculate based on location change
		const locationOrder = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
		const startIndex = locationOrder.indexOf(startLoc);
		const endIndex = locationOrder.indexOf(endLoc);
		
		if (startIndex === -1 || endIndex === -1) return 1;
		
		const distance = Math.abs(endIndex - startIndex);
		return Math.min(distance, 8 - distance);
	}

	/**
	 * Random choice helper
	 */
	private randomChoice<T>(array: readonly T[]): T {
		return array[Math.floor(Math.random() * array.length)];
	}

	/**
	 * Generate motion with constraints
	 */
	async generateConstrainedMotion(
		color: 'blue' | 'red',
		options: GenerationOptions,
		previousBeats: BeatData[],
		constraints: {
			allowedMotionTypes?: string[];
			allowedStartLocations?: string[];
			allowedEndLocations?: string[];
		}
	): Promise<MotionData> {
		// TODO: Implement constrained generation
		// For now, use basic generation
		return this.generateMotion(color, options, previousBeats);
	}

	/**
	 * Validate if a motion is valid given the context
	 */
	validateMotion(
		motion: MotionData,
		color: 'blue' | 'red',
		previousBeats: BeatData[]
	): { isValid: boolean; reasons: string[] } {
		const reasons: string[] = [];

		// Basic validation
		if (!motion.motionType) {
			reasons.push('Motion type is required');
		}

		if (!motion.startLoc) {
			reasons.push('Start location is required');
		}

		if (!motion.endLoc) {
			reasons.push('End location is required');
		}

		// TODO: Add more sophisticated validation rules from desktop app

		return {
			isValid: reasons.length === 0,
			reasons
		};
	}
}
