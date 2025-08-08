/**
 * Start Position Service - Implementation
 *
 * Provides start position management functionality for the construct workflow.
 * Based on the desktop StartPositionOrchestrator but simplified for web.
 */

import type {
	IStartPositionService,
	ValidationResult,
	GridMode,
	MotionType
} from '../interfaces';
import type { BeatData, PictographData } from '../../domain';
import {
	createPictographData,
	createArrowData,
	createPropData,
	createBeatData,
	createMotionData,
	createGridData,
	ArrowType,
	PropType,
	MotionType as DomainMotionType,
	Location,
	Orientation,
	RotationDirection,
	GridMode as DomainGridMode
} from '../../domain'; export class StartPositionService implements IStartPositionService {
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

				return createBeatData({
					beat_number: 0,
					is_blank: false,
					pictograph_data: this.createStartPositionPictograph(key, index, gridMode)
				});
			}); console.log(`✅ Generated ${beatData.length} start positions`);
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
		if (position.pictograph_data?.motions?.blue?.motion_type !== DomainMotionType.STATIC) {
			errors.push('Blue motion must be static for start positions');
		}

		if (position.pictograph_data?.motions?.red?.motion_type !== DomainMotionType.STATIC) {
			errors.push('Red motion must be static for start positions');
		}

		return {
			isValid: errors.length === 0,
			errors
		};
	} async getDefaultStartPositions(gridMode: GridMode): Promise<PictographData[]> {
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
		const locations = [Location.NORTH, Location.SOUTH, Location.EAST, Location.WEST, Location.NORTHEAST, Location.SOUTHEAST, Location.SOUTHWEST, Location.NORTHWEST];
		const blueLocation = locations[index % locations.length];
		const redLocation = locations[(index + 4) % locations.length]; // Offset for variety

		console.log(`🎯 Creating start position ${key} - Blue: ${blueLocation}, Red: ${redLocation}`);

		// Create proper arrow data with location
		const blueArrow = createArrowData({
			arrow_type: ArrowType.BLUE,
			color: 'blue',
			turns: 0,
			location: blueLocation
		});

		const redArrow = createArrowData({
			arrow_type: ArrowType.RED,
			color: 'red',
			turns: 0,
			location: redLocation
		});

		console.log(`🏹 Created arrows - Blue: ${JSON.stringify({id: blueArrow.id, location: blueArrow.location})}, Red: ${JSON.stringify({id: redArrow.id, location: redArrow.location})}`);

		// Create proper prop data with location
		const blueProp = createPropData({
			prop_type: PropType.STAFF,
			color: 'blue',
			location: blueLocation
		});

		const redProp = createPropData({
			prop_type: PropType.STAFF,
			color: 'red',
			location: redLocation
		});

		// Create proper motion data
		const blueMotion = createMotionData({
			motion_type: DomainMotionType.STATIC,
			prop_rot_dir: RotationDirection.NO_ROTATION,
			start_loc: blueLocation,
			end_loc: blueLocation,
			turns: 0,
			start_ori: Orientation.IN,
			end_ori: Orientation.IN
		});

		const redMotion = createMotionData({
			motion_type: DomainMotionType.STATIC,
			prop_rot_dir: RotationDirection.NO_ROTATION,
			start_loc: redLocation,
			end_loc: redLocation,
			turns: 0,
			start_ori: Orientation.OUT,
			end_ori: Orientation.OUT
		});

		const pictograph = createPictographData({
			id: `start-pos-${key}-${index}`,
			grid_data: createGridData({ grid_mode: gridMode === 'diamond' ? DomainGridMode.DIAMOND : DomainGridMode.BOX }),
			arrows: { blue: blueArrow, red: redArrow },
			props: { blue: blueProp, red: redProp },
			motions: { blue: blueMotion, red: redMotion },
			letter,
			beat: index,
			is_blank: false,
			is_mirrored: false
		});

		console.log(`🎨 Final pictograph arrows - Blue: ${JSON.stringify({id: pictograph.arrows?.blue?.id, location: pictograph.arrows?.blue?.location})}, Red: ${JSON.stringify({id: pictograph.arrows?.red?.id, location: pictograph.arrows?.red?.location})}`);

		return pictograph;
	}
}
