/**
 * Option Data Service - Implementation (Updated)
 *
 * Provides option generation and filtering for the construct workflow.
 * Now uses real CSV data like the legacy system.
 */

import type {
	IOptionDataService,
	SequenceData,
	BeatData,
	PictographData,
	ValidationResult,
	OptionFilters,
	DifficultyLevel,
	MotionType,
} from '../interfaces';
import { CsvDataService, type ParsedCsvRow } from './CsvDataService';
import { OrientationCalculationService } from './OrientationCalculationService';
import type { MotionData } from '$domain/MotionData';
import {
	createPictographData,
	createArrowData,
	createPropData,
	createMotionData,
	createGridData,
	ArrowType,
	PropType,
	MotionType as DomainMotionType,
	Location,
	Orientation,
	RotationDirection,
	GridMode as DomainGridMode,
} from '$domain';

export class OptionDataService implements IOptionDataService {
	private readonly MOTION_TYPES: MotionType[] = ['pro', 'anti', 'float', 'dash', 'static'];

	private readonly DIFFICULTY_MOTION_LIMITS = {
		beginner: { maxTurns: 1, allowedTypes: ['pro', 'anti', 'static'] },
		intermediate: { maxTurns: 2, allowedTypes: ['pro', 'anti', 'float', 'static'] },
		advanced: { maxTurns: 3, allowedTypes: ['pro', 'anti', 'float', 'dash', 'static'] },
	};

	private csvDataService: CsvDataService;
	private orientationCalculationService: OrientationCalculationService;

	constructor() {
		console.log('🎲 OptionDataService initialized');
		this.csvDataService = new CsvDataService();
		this.orientationCalculationService = new OrientationCalculationService();
	}

	/**
	 * Initialize the service by loading CSV data
	 */
	async initialize(): Promise<void> {
		await this.csvDataService.loadCsvData();
		console.log('✅ OptionDataService CSV data loaded');
	}

	/**
	 * Get next options based on end position from CSV data (like legacy)
	 */
	async getNextOptionsFromEndPosition(
		endPosition: string,
		gridMode: 'diamond' | 'box' = 'diamond',
		filters?: OptionFilters
	): Promise<PictographData[]> {
		console.log(`🎲 Getting real options for end position: ${endPosition} in ${gridMode} mode`);

		try {
			// Get matching options from CSV data
			const csvOptions = this.csvDataService.getNextOptions(endPosition, gridMode);

			if (csvOptions.length === 0) {
				console.warn(`⚠️ No options found for end position: ${endPosition}`);
				return [];
			}

			// Convert CSV rows to PictographData
			const pictographOptions = csvOptions
				.map((row) => this.convertCsvRowToPictographData(row, gridMode))
				.filter((option): option is PictographData => option !== null);

			// Apply filters
			let filteredOptions = pictographOptions;

			if (filters?.difficulty) {
				filteredOptions = this.filterOptionsByDifficulty(
					filteredOptions,
					filters.difficulty
				);
			}

			if (filters?.motionTypes) {
				filteredOptions = this.filterByMotionTypes(filteredOptions, filters.motionTypes);
			}

			if (filters?.minTurns !== undefined || filters?.maxTurns !== undefined) {
				filteredOptions = this.filterByTurns(
					filteredOptions,
					filters.minTurns,
					filters.maxTurns
				);
			}

			console.log(`✅ Generated ${filteredOptions.length} real options from CSV data`);
			return filteredOptions;
		} catch (error) {
			console.error('❌ Error getting options from CSV:', error);
			return [];
		}
	}

	async getNextOptions(
		currentSequence: SequenceData,
		filters?: OptionFilters
	): Promise<PictographData[]> {
		console.log('🎲 Getting next options for sequence:', currentSequence.id);

		try {
			// Get the last beat to understand context
			const lastBeat = this.getLastBeat(currentSequence);

			if (!lastBeat?.pictograph_data) {
				console.warn('⚠️ No last beat found in sequence');
				return [];
			}

			// Get end position from last beat
			const endPosition = this.extractEndPosition(lastBeat.pictograph_data);
			if (!endPosition) {
				console.warn('⚠️ Could not extract end position from last beat');
				return [];
			}

			// Get grid mode from last beat
			const gridMode = lastBeat.pictograph_data.gridData?.mode === 'box' ? 'box' : 'diamond';

			// Use the real CSV data method
			return await this.getNextOptionsFromEndPosition(endPosition, gridMode, filters);
		} catch (error) {
			console.error('❌ Error generating options:', error);
			return [];
		}
	}

	filterOptionsByDifficulty(options: PictographData[], level: DifficultyLevel): PictographData[] {
		console.log(`🎯 Filtering ${options.length} options by ${level} difficulty`);

		const limits = this.DIFFICULTY_MOTION_LIMITS[level];

		const filtered = options.filter((option) => {
			// Check blue motion
			if (option.motions?.blue) {
				if (!limits.allowedTypes.includes(option.motions.blue.motionType)) {
					return false;
				}
				if (
					typeof option.motions.blue.turns === 'number' &&
					option.motions.blue.turns > limits.maxTurns
				) {
					return false;
				}
			}

			// Check red motion
			if (option.motions?.red) {
				if (!limits.allowedTypes.includes(option.motions.red.motionType)) {
					return false;
				}
				if (
					typeof option.motions.red.turns === 'number' &&
					option.motions.red.turns > limits.maxTurns
				) {
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
			const continuityErrors = this.validateMotionContinuity(
				lastBeat.pictograph_data,
				option
			);
			errors.push(...continuityErrors);
		}

		return {
			isValid: errors.length === 0,
			errors,
		};
	}

	getAvailableMotionTypes(): MotionType[] {
		return [...this.MOTION_TYPES];
	}

	/**
	 * Convert CSV row to PictographData format (based on legacy implementation)
	 */
	private convertCsvRowToPictographData(
		row: ParsedCsvRow,
		gridMode: 'diamond' | 'box'
	): PictographData | null {
		try {
			console.log(`🔄 Converting CSV row: ${row.letter} ${row.startPos}->${row.endPos}`);

			// Create motion data for blue and red
			const blueMotion = this.createMotionDataFromCsv(row, 'blue');
			const redMotion = this.createMotionDataFromCsv(row, 'red');

			// Create arrow data
			const blueArrow = createArrowData({
				arrow_type: ArrowType.BLUE,
				color: 'blue',
				turns: 0, // Will be set from motion data
				location: this.mapLocationString(row.blueStartLoc),
			});

			const redArrow = createArrowData({
				arrow_type: ArrowType.RED,
				color: 'red',
				turns: 0, // Will be set from motion data
				location: this.mapLocationString(row.redStartLoc),
			});

			// Create prop data
			const blueProp = createPropData({
				prop_type: PropType.STAFF,
				color: 'blue',
				location: this.mapLocationString(row.blueStartLoc),
			});

			const redProp = createPropData({
				prop_type: PropType.STAFF,
				color: 'red',
				location: this.mapLocationString(row.redStartLoc),
			});

			// Create the complete PictographData
			const pictograph = createPictographData({
				id: `option-${row.letter}-${row.startPos}-${row.endPos}`,
				grid_data: createGridData({
					grid_mode: gridMode === 'diamond' ? DomainGridMode.DIAMOND : DomainGridMode.BOX,
				}),
				arrows: { blue: blueArrow, red: redArrow },
				props: { blue: blueProp, red: redProp },
				motions: { blue: blueMotion, red: redMotion },
				letter: row.letter,
				beat: 0,
				is_blank: false,
				is_mirrored: false,
			});

			console.log(`✅ Converted CSV row to pictograph: ${pictograph.id}`);
			return pictograph;
		} catch (error) {
			console.error('❌ Error converting CSV row to PictographData:', error, row);
			return null;
		}
	}

	/**
	 * Create motion data from CSV row with proper orientation calculation
	 */
	private createMotionDataFromCsv(row: ParsedCsvRow, color: 'blue' | 'red'): MotionData {
		const motionType = row[`${color}MotionType`] as string;
		const propRotDir = row[`${color}PropRotDir`] as string;
		const startLoc = row[`${color}StartLoc`] as string;
		const endLoc = row[`${color}EndLoc`] as string;

		// Use orientation calculation service to create motion with proper end orientation
		const motion = this.orientationCalculationService.createMotionWithCalculatedOrientation(
			this.mapMotionType(motionType),
			this.mapRotationDirection(propRotDir),
			this.mapLocationString(startLoc),
			this.mapLocationString(endLoc),
			0, // Basic turns for now - could be enhanced to read from CSV
			Orientation.IN // Standard start orientation
		);

		console.log(
			`🧭 Motion created: ${color} ${motionType} - start: ${motion.start_ori}, end: ${motion.end_ori}`
		);
		return motion;
	}

	/**
	 * Map string motion type to domain enum
	 */
	private mapMotionType(motionType: string): DomainMotionType {
		switch (motionType.toLowerCase()) {
			case 'pro':
				return DomainMotionType.PRO;
			case 'anti':
				return DomainMotionType.ANTI;
			case 'float':
				return DomainMotionType.FLOAT;
			case 'dash':
				return DomainMotionType.DASH;
			case 'static':
				return DomainMotionType.STATIC;
			default:
				return DomainMotionType.PRO;
		}
	}

	/**
	 * Map string rotation direction to domain enum
	 */
	private mapRotationDirection(rotDir: string): RotationDirection {
		switch (rotDir.toLowerCase()) {
			case 'cw':
				return RotationDirection.CLOCKWISE;
			case 'ccw':
				return RotationDirection.COUNTER_CLOCKWISE;
			case 'no_rot':
				return RotationDirection.NO_ROTATION;
			default:
				return RotationDirection.NO_ROTATION;
		}
	}

	/**
	 * Map string location to domain enum
	 */
	private mapLocationString(loc: string): Location {
		switch (loc.toLowerCase()) {
			case 'n':
				return Location.NORTH;
			case 's':
				return Location.SOUTH;
			case 'e':
				return Location.EAST;
			case 'w':
				return Location.WEST;
			case 'ne':
				return Location.NORTHEAST;
			case 'se':
				return Location.SOUTHEAST;
			case 'sw':
				return Location.SOUTHWEST;
			case 'nw':
				return Location.NORTHWEST;
			default:
				return Location.SOUTH;
		}
	}

	private getLastBeat(sequence: SequenceData): BeatData | null {
		if (!sequence.beats || sequence.beats.length === 0) {
			return null;
		}
		return sequence.beats[sequence.beats.length - 1];
	}

	/**
	 * Extract end position from pictograph data
	 */
	private extractEndPosition(pictographData: PictographData): string | null {
		// Try to get from motion data
		if (pictographData.motions?.blue?.endLocation) {
			return this.mapLocationToPositionString(pictographData.motions.blue.endLocation);
		}
		if (pictographData.motions?.red?.endLocation) {
			return this.mapLocationToPositionString(pictographData.motions.red.endLocation);
		}
		return null;
	}

	/**
	 * Map location enum to position string
	 */
	private mapLocationToPositionString(location: Location): string {
		// This would need proper mapping logic based on your position system
		// For now, returning a default
		return 'alpha1'; // Placeholder - needs proper mapping
	}

	private filterByMotionTypes(
		options: PictographData[],
		motionTypes: MotionType[]
	): PictographData[] {
		return options.filter((option) => {
			const blueValid =
				!option.motions?.blue || motionTypes.includes(option.motions.blue.motionType);
			const redValid =
				!option.motions?.red || motionTypes.includes(option.motions.red.motionType);
			return blueValid && redValid;
		});
	}

	private filterByTurns(
		options: PictographData[],
		minTurns?: number,
		maxTurns?: number
	): PictographData[] {
		return options.filter((option) => {
			// Check blue motion turns
			if (option.motions?.blue) {
				const blueTurns =
					typeof option.motions.blue.turns === 'number' ? option.motions.blue.turns : 0;
				if (minTurns !== undefined && blueTurns < minTurns) return false;
				if (maxTurns !== undefined && blueTurns > maxTurns) return false;
			}

			// Check red motion turns
			if (option.motions?.red) {
				const redTurns =
					typeof option.motions.red.turns === 'number' ? option.motions.red.turns : 0;
				if (minTurns !== undefined && redTurns < minTurns) return false;
				if (maxTurns !== undefined && redTurns > maxTurns) return false;
			}

			return true;
		});
	}

	private validateMotionContinuity(
		lastPictograph: PictographData,
		nextOption: PictographData
	): string[] {
		const errors: string[] = [];

		// Basic continuity validation - end positions should connect to start positions
		if (lastPictograph.motions?.blue && nextOption.motions?.blue) {
			if (lastPictograph.motions.blue.endLocation !== nextOption.motions.blue.startLocation) {
				// Allow some flexibility in continuity for now
				console.warn(
					'Blue motion continuity warning:',
					lastPictograph.motions.blue.endLocation,
					'→',
					nextOption.motions.blue.startLocation
				);
			}
		}

		if (lastPictograph.motions?.red && nextOption.motions?.red) {
			if (lastPictograph.motions.red.endLocation !== nextOption.motions.red.startLocation) {
				// Allow some flexibility in continuity for now
				console.warn(
					'Red motion continuity warning:',
					lastPictograph.motions.red.endLocation,
					'→',
					nextOption.motions.red.startLocation
				);
			}
		}

		return errors;
	}
}
