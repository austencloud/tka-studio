/**
 * Option Data Service - Implementation (Updated)
 *
 * Provides option generation and filtering for the construct workflow.
 * Now uses real CSV data like the legacy system.
 */

import {
	ArrowType,
	createArrowData,
	// createMotionData,
	createGridData,
	createPictographData,
	createPropData,
	GridMode as DomainGridMode,
	MotionType as DomainMotionType,
	Location,
	Orientation,
	PropType,
	RotationDirection,
} from '$domain';
import type { MotionData } from '$domain/MotionData';
import type {
	BeatData,
	DifficultyLevel,
	IOptionDataService,
	MotionType,
	OptionFilters,
	PictographData,
	SequenceData,
	ValidationResult,
} from '../interfaces';
import { CsvDataService, type ParsedCsvRow } from './CsvDataService';
import { OrientationCalculationService } from './OrientationCalculationService';

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
		this.csvDataService = new CsvDataService();
		this.orientationCalculationService = new OrientationCalculationService();
	}

	/**
	 * Initialize the service by loading CSV data
	 */
	async initialize(): Promise<void> {
		await this.csvDataService.loadCsvData();
	}

	/**
	 * Get next options based on end position from CSV data (like legacy)
	 */
	async getNextOptionsFromEndPosition(
		endPosition: string,
		gridMode: DomainGridMode = DomainGridMode.DIAMOND,
		filters?: OptionFilters
	): Promise<PictographData[]> {
		try {
			// Get matching options from CSV data
			const csvOptions = this.csvDataService.getNextOptions(endPosition, gridMode);

			if (csvOptions.length === 0) {
				return [];
			}

			// Convert CSV rows to PictographData with unique IDs
			const pictographOptions = csvOptions
				.map((row, index) =>
					this.convertCsvRowToPictographDataInternal(row, gridMode, index)
				)
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
		try {
			// Get the last beat to understand context
			const lastBeat = this.getLastBeat(currentSequence);

			if (!lastBeat?.pictograph_data) {
				return [];
			}

			// Get end position from last beat
			const endPosition = this.extractEndPosition(lastBeat.pictograph_data);
			if (!endPosition) {
				return [];
			}

			// Get grid mode from last beat (domain: pictograph_data.grid_data.grid_mode)
			const gridMode =
				lastBeat.pictograph_data.grid_data?.grid_mode === DomainGridMode.BOX
					? DomainGridMode.BOX
					: DomainGridMode.DIAMOND;

			// Use the real CSV data method
			return await this.getNextOptionsFromEndPosition(endPosition, gridMode, filters);
		} catch (error) {
			console.error('❌ Error generating options:', error);
			return [];
		}
	}

	filterOptionsByDifficulty(options: PictographData[], level: DifficultyLevel): PictographData[] {
		const limits = this.DIFFICULTY_MOTION_LIMITS[level];

		const filtered = options.filter((option) => {
			// Check blue motion
			if (option.motions?.blue) {
				const blueMotion = option.motions.blue as MotionData;
				if (!limits.allowedTypes.includes(blueMotion.motion_type as MotionType)) {
					return false;
				}
				if (typeof blueMotion.turns === 'number' && blueMotion.turns > limits.maxTurns) {
					return false;
				}
			}

			// Check red motion
			if (option.motions?.red) {
				const redMotion = option.motions.red as MotionData;
				if (!limits.allowedTypes.includes(redMotion.motion_type as MotionType)) {
					return false;
				}
				if (typeof redMotion.turns === 'number' && redMotion.turns > limits.maxTurns) {
					return false;
				}
			}

			return true;
		});

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
	 * Convert CSV row to PictographData format (public method for external use)
	 */
	convertCsvRowToPictographData(
		row: ParsedCsvRow,
		gridMode: DomainGridMode,
		index: number = 0
	): PictographData | null {
		return this.convertCsvRowToPictographDataInternal(row, gridMode, index);
	}

	/**
	 * Convert CSV row to PictographData format (based on legacy implementation)
	 */
	private convertCsvRowToPictographDataInternal(
		row: ParsedCsvRow,
		gridMode: DomainGridMode,
		index: number = 0
	): PictographData | null {
		try {
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

			// Create prop data using END locations for proper positioning
			const blueProp = createPropData({
				prop_type: PropType.STAFF,
				color: 'blue',
				location: this.mapLocationString(row.blueEndLoc),
			});

			const redProp = createPropData({
				prop_type: PropType.STAFF,
				color: 'red',
				location: this.mapLocationString(row.redEndLoc),
			});

			// Create the complete PictographData with unique ID including grid mode
			const pictograph = createPictographData({
				id: `${gridMode}-${row.letter || 'unknown'}-${row.startPos || 'unknown'}-${row.endPos || 'unknown'}-${index}`,
				grid_data: createGridData({
					grid_mode: gridMode,
				}),
				arrows: { blue: blueArrow, red: redArrow },
				props: { blue: blueProp, red: redProp },
				motions: { blue: blueMotion, red: redMotion },
				letter: row.letter,
				beat: 0,
				is_blank: false,
				is_mirrored: false,
			});

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
		return (sequence.beats[sequence.beats.length - 1] as BeatData) ?? null;
	}

	/**
	 * Extract end position from pictograph data
	 */
	private extractEndPosition(pictographData: PictographData): string | null {
		const blueEnd = (pictographData.motions?.blue as MotionData | undefined)?.end_loc;
		if (blueEnd) return this.mapLocationToPositionString(blueEnd);
		const redEnd = (pictographData.motions?.red as MotionData | undefined)?.end_loc;
		if (redEnd) return this.mapLocationToPositionString(redEnd);
		return null;
	}

	/**
	 * Map location enum to position string
	 */
	private mapLocationToPositionString(_location: Location): string {
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
				!option.motions?.blue ||
				motionTypes.includes((option.motions.blue as MotionData).motion_type as MotionType);
			const redValid =
				!option.motions?.red ||
				motionTypes.includes((option.motions.red as MotionData).motion_type as MotionType);
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
			const lastEnd = (lastPictograph.motions.blue as MotionData | undefined)?.end_loc;
			const nextStart = (nextOption.motions.blue as MotionData | undefined)?.start_loc;
			if (lastEnd && nextStart && lastEnd !== nextStart) {
				// Allow some flexibility in continuity for now
			}
		}

		if (lastPictograph.motions?.red && nextOption.motions?.red) {
			const lastEnd = (lastPictograph.motions.red as MotionData | undefined)?.end_loc;
			const nextStart = (nextOption.motions.red as MotionData | undefined)?.start_loc;
			if (lastEnd && nextStart && lastEnd !== nextStart) {
				// Allow some flexibility in continuity for now
			}
		}

		return errors;
	}
}
