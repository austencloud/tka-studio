/**
 * Start Position Service - Implementation
 * 
 * Provides start position management functionality for the construct workflow.
 * Based on the desktop StartPositionOrchestrator but simplified for web.
 */

import type { 
	IStartPositionService,
	BeatData,
	PictographData,
	ValidationResult,
	GridMode,
	MotionType
} from '../interfaces';

export class StartPositionService implements IStartPositionService {
	private readonly DEFAULT_START_POSITIONS = {
		diamond: ['alpha1_alpha1', 'beta5_beta5', 'gamma11_gamma11'],
		box: ['alpha2_alpha2', 'beta4_beta4', 'gamma12_gamma12']
	};

	constructor() {
		console.log('🎯 StartPositionService initialized');
	}

	async getAvailableStartPositions(propType: string, gridMode: GridMode): Promise<BeatData[]> {
		console.log(`📍 Getting available start positions for ${propType} in ${gridMode} mode`);
		
		try {
			const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];
			
			const beatData: BeatData[] = startPositionKeys.map((key, index) => {
				const [startPos, endPos] = key.split('_');
				
				return {
					beat: 0,
					pictograph_data: this.createStartPositionPictograph(key, index, gridMode)
				};
			});
			
			console.log(`✅ Generated ${beatData.length} start positions`);
			return beatData;
			
		} catch (error) {
			console.error('❌ Error getting start positions:', error);
			return [];
		}
	}

	async setStartPosition(startPosition: BeatData): Promise<void> {
		console.log('🎯 Setting start position:', startPosition.pictograph_data?.id);
		
		try {
			// Store in localStorage for persistence (similar to legacy implementation)
			if (typeof window !== 'undefined') {
				localStorage.setItem('start_position', JSON.stringify(startPosition));
			}
			
			console.log('✅ Start position set successfully');
			
		} catch (error) {
			console.error('❌ Error setting start position:', error);
			throw new Error(`Failed to set start position: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	validateStartPosition(position: BeatData): ValidationResult {
		const errors: string[] = [];
		
		if (!position.pictograph_data) {
			errors.push('Start position must have pictograph data');
		}
		
		if (!position.pictograph_data?.motions?.blue && !position.pictograph_data?.motions?.red) {
			errors.push('Start position must have at least one motion');
		}
		
		// Validate motion types are static for start positions
		if (position.pictograph_data?.motions?.blue?.motionType !== 'static') {
			errors.push('Blue motion must be static for start positions');
		}
		
		if (position.pictograph_data?.motions?.red?.motionType !== 'static') {
			errors.push('Red motion must be static for start positions');
		}
		
		return {
			isValid: errors.length === 0,
			errors
		};
	}

	async getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]> {
		console.log(`📍 Getting default start positions for ${gridMode} mode`);
		
		try {
			const startPositionKeys = this.DEFAULT_START_POSITIONS[gridMode];
			
			const pictographData: PictographData[] = startPositionKeys.map((key, index) => 
				this.createStartPositionPictograph(key, index, gridMode)
			);
			
			console.log(`✅ Generated ${pictographData.length} default start positions`);
			return pictographData;
			
		} catch (error) {
			console.error('❌ Error getting default start positions:', error);
			return [];
		}
	}

	private createStartPositionPictograph(key: string, index: number, gridMode: GridMode): PictographData {
		const [startPos, endPos] = key.split('_');
		
		// Determine letter based on position key
		let letter: string;
		if (key.includes('alpha')) letter = 'α';
		else if (key.includes('beta')) letter = 'β';
		else if (key.includes('gamma')) letter = 'γ';
		else letter = key;
		
		// Create base locations for the positions
		const locations = ['n', 's', 'e', 'w', 'ne', 'se', 'sw', 'nw'];
		const blueLocation = locations[index % locations.length];
		const redLocation = locations[(index + 4) % locations.length]; // Offset for variety
		
		return {
			id: `start-pos-${key}-${index}`,
			gridData: { mode: gridMode },
			arrows: { blue: {}, red: {} },
			props: { blue: {}, red: {} },
			motions: {
				blue: {
					motionType: 'static',
					propRotDir: 'no_rot',
					startLocation: blueLocation as any,
					endLocation: blueLocation as any,
					turns: 0,
					startOrientation: 'in',
					endOrientation: 'in'
				},
				red: {
					motionType: 'static',
					propRotDir: 'no_rot',
					startLocation: redLocation as any,
					endLocation: redLocation as any,
					turns: 0,
					startOrientation: 'out',
					endOrientation: 'out'
				}
			},
			letter
		};
	}
}
