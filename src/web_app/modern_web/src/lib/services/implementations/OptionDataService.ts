/**
 * Option Data Service - Implementation
 * 
 * Provides option generation and filtering for the construct workflow.
 * Based on desktop option picker services but simplified for web.
 */

import type { 
	IOptionDataService,
	SequenceData,
	BeatData,
	PictographData,
	ValidationResult,
	OptionFilters,
	DifficultyLevel,
	MotionType
} from '../interfaces';

export class OptionDataService implements IOptionDataService {
	private readonly MOTION_TYPES: MotionType[] = ['pro', 'anti', 'float', 'dash', 'static'];
	
	private readonly DIFFICULTY_MOTION_LIMITS = {
		beginner: { maxTurns: 1, allowedTypes: ['pro', 'anti', 'static'] },
		intermediate: { maxTurns: 2, allowedTypes: ['pro', 'anti', 'float', 'static'] },
		advanced: { maxTurns: 3, allowedTypes: ['pro', 'anti', 'float', 'dash', 'static'] }
	};

	constructor() {
		console.log('🎲 OptionDataService initialized');
	}

	async getNextOptions(currentSequence: SequenceData, filters?: OptionFilters): Promise<PictographData[]> {
		console.log('🎲 Generating next options for sequence:', currentSequence.id);
		
		try {
			// Get the last beat to understand context
			const lastBeat = this.getLastBeat(currentSequence);
			const contextualOptions = await this.generateContextualOptions(lastBeat, filters);
			
			// Apply filters
			let filteredOptions = contextualOptions;
			
			if (filters?.difficulty) {
				filteredOptions = this.filterOptionsByDifficulty(filteredOptions, filters.difficulty);
			}
			
			if (filters?.motionTypes) {
				filteredOptions = this.filterByMotionTypes(filteredOptions, filters.motionTypes);
			}
			
			if (filters?.minTurns !== undefined || filters?.maxTurns !== undefined) {
				filteredOptions = this.filterByTurns(filteredOptions, filters.minTurns, filters.maxTurns);
			}
			
			console.log(`✅ Generated ${filteredOptions.length} options`);
			return filteredOptions;
			
		} catch (error) {
			console.error('❌ Error generating options:', error);
			return [];
		}
	}

	filterOptionsByDifficulty(options: PictographData[], level: DifficultyLevel): PictographData[] {
		console.log(`🎯 Filtering ${options.length} options by ${level} difficulty`);
		
		const limits = this.DIFFICULTY_MOTION_LIMITS[level];
		
		const filtered = options.filter(option => {
			// Check blue motion
			if (option.motions?.blue) {
				if (!limits.allowedTypes.includes(option.motions.blue.motionType)) {
					return false;
				}
				if (typeof option.motions.blue.turns === 'number' && option.motions.blue.turns > limits.maxTurns) {
					return false;
				}
			}
			
			// Check red motion
			if (option.motions?.red) {
				if (!limits.allowedTypes.includes(option.motions.red.motionType)) {
					return false;
				}
				if (typeof option.motions.red.turns === 'number' && option.motions.red.turns > limits.maxTurns) {
					return false;
				}
			}
			
			return true;
		});
		
		console.log(`🎯 Filtered to ${filtered.length} options for ${level} level`);
		return filtered;
	}

	validateOptionCompatibility(option: PictographData, sequence: SequenceData): ValidationResult {
		const errors: string[] = [];
		
		// Check if option has required motion data
		if (!option.motions?.blue && !option.motions?.red) {
			errors.push('Option must have at least one motion');
		}
		
		// Check for sequence compatibility
		const lastBeat = this.getLastBeat(sequence);
		if (lastBeat?.pictograph_data) {
			// Validate motion continuity
			const continuityErrors = this.validateMotionContinuity(lastBeat.pictograph_data, option);
			errors.push(...continuityErrors);
		}
		
		return {
			isValid: errors.length === 0,
			errors
		};
	}

	getAvailableMotionTypes(): MotionType[] {
		return [...this.MOTION_TYPES];
	}

	private getLastBeat(sequence: SequenceData): BeatData | null {
		if (!sequence.beats || sequence.beats.length === 0) {
			return null;
		}
		return sequence.beats[sequence.beats.length - 1];
	}

	private async generateContextualOptions(lastBeat: BeatData | null, filters?: OptionFilters): Promise<PictographData[]> {
		// Generate a variety of options based on context
		const options: PictographData[] = [];
		const gridMode = lastBeat?.pictograph_data?.gridData?.mode || 'diamond';
		
		// Generate different motion combinations
		const motionCombinations = this.getMotionCombinations(filters?.motionTypes);
		
		motionCombinations.forEach((combo, index) => {
			const option = this.createOptionPictograph(combo, index, gridMode, lastBeat);
			options.push(option);
		});
		
		return options;
	}

	private getMotionCombinations(allowedTypes?: MotionType[]) {
		const types = allowedTypes || this.MOTION_TYPES;
		const combinations = [];
		
		// Generate various combinations
		for (let i = 0; i < Math.min(types.length, 12); i++) {
			const blueType = types[i % types.length];
			const redType = types[(i + 2) % types.length];
			
			combinations.push({
				blue: { type: blueType, turns: this.getRandomTurns(blueType) },
				red: { type: redType, turns: this.getRandomTurns(redType) }
			});
		}
		
		return combinations;
	}

	private getRandomTurns(motionType: MotionType): number | 'fl' {
		if (motionType === 'float') return 'fl';
		if (motionType === 'static') return 0;
		
		const possibleTurns = [0.5, 1, 1.5, 2, 2.5, 3];
		return possibleTurns[Math.floor(Math.random() * possibleTurns.length)];
	}

	private createOptionPictograph(combo: any, index: number, gridMode: string, lastBeat?: BeatData | null): PictographData {
		// Create locations that make sense contextually
		const locations = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'];
		const blueStart = locations[index % locations.length];
		const blueEnd = locations[(index + 2) % locations.length];
		const redStart = locations[(index + 4) % locations.length];
		const redEnd = locations[(index + 6) % locations.length];
		
		return {
			id: `option-${index}-${combo.blue.type}-${combo.red.type}`,
			gridData: { mode: gridMode as any },
			arrows: { blue: {}, red: {} },
			props: { blue: {}, red: {} },
			motions: {
				blue: {
					motionType: combo.blue.type,
					propRotDir: combo.blue.type === 'pro' ? 'cw' : combo.blue.type === 'anti' ? 'ccw' : 'no_rot',
					startLocation: blueStart as any,
					endLocation: blueEnd as any,
					turns: combo.blue.turns,
					startOrientation: 'in',
					endOrientation: 'out'
				},
				red: {
					motionType: combo.red.type,
					propRotDir: combo.red.type === 'pro' ? 'cw' : combo.red.type === 'anti' ? 'ccw' : 'no_rot',
					startLocation: redStart as any,
					endLocation: redEnd as any,
					turns: combo.red.turns,
					startOrientation: 'out',
					endOrientation: 'in'
				}
			},
			letter: this.generateRandomLetter()
		};
	}

	private generateRandomLetter(): string {
		const letters = ['α', 'β', 'γ', 'δ', 'ε', 'ζ', 'η', 'θ'];
		return letters[Math.floor(Math.random() * letters.length)];
	}

	private filterByMotionTypes(options: PictographData[], motionTypes: MotionType[]): PictographData[] {
		return options.filter(option => {
			const blueValid = !option.motions?.blue || motionTypes.includes(option.motions.blue.motionType);
			const redValid = !option.motions?.red || motionTypes.includes(option.motions.red.motionType);
			return blueValid && redValid;
		});
	}

	private filterByTurns(options: PictographData[], minTurns?: number, maxTurns?: number): PictographData[] {
		return options.filter(option => {
			// Check blue motion turns
			if (option.motions?.blue) {
				const blueTurns = typeof option.motions.blue.turns === 'number' ? option.motions.blue.turns : 0;
				if (minTurns !== undefined && blueTurns < minTurns) return false;
				if (maxTurns !== undefined && blueTurns > maxTurns) return false;
			}
			
			// Check red motion turns
			if (option.motions?.red) {
				const redTurns = typeof option.motions.red.turns === 'number' ? option.motions.red.turns : 0;
				if (minTurns !== undefined && redTurns < minTurns) return false;
				if (maxTurns !== undefined && redTurns > maxTurns) return false;
			}
			
			return true;
		});
	}

	private validateMotionContinuity(lastPictograph: PictographData, nextOption: PictographData): string[] {
		const errors: string[] = [];
		
		// Basic continuity validation - end positions should connect to start positions
		if (lastPictograph.motions?.blue && nextOption.motions?.blue) {
			if (lastPictograph.motions.blue.endLocation !== nextOption.motions.blue.startLocation) {
				// Allow some flexibility in continuity for now
				console.warn('Blue motion continuity warning:', 
					lastPictograph.motions.blue.endLocation, '→', nextOption.motions.blue.startLocation);
			}
		}
		
		if (lastPictograph.motions?.red && nextOption.motions?.red) {
			if (lastPictograph.motions.red.endLocation !== nextOption.motions.red.startLocation) {
				// Allow some flexibility in continuity for now
				console.warn('Red motion continuity warning:', 
					lastPictograph.motions.red.endLocation, '→', nextOption.motions.red.startLocation);
			}
		}
		
		return errors;
	}
}
