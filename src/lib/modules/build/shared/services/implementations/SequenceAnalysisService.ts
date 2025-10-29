import { inject, injectable } from "inversify";
import { TYPES } from "$shared/inversify/types";
import type { GridPosition } from "$shared/pictograph/grid/domain/enums/grid-enums";
import type { BeatData } from "../../domain/models/BeatData";
import type { SequenceData } from "$shared/foundation/domain/models/SequenceData";
import type { IBetaDetectionService } from "$shared/pictograph/prop/services/contracts/IBetaDetectionService";
import type {
	ISequenceAnalysisService,
	CircularityAnalysis,
	CircularType,
	StrictCapType,
} from "../contracts/ISequenceAnalysisService";

/**
 * Sequence Analysis Service Implementation
 *
 * Analyzes sequences to detect circular patterns and CAP potential.
 *
 * Key Concepts:
 * - Beta positions form an octagon with 8 positions (beta1-beta8)
 * - Circular sequences must start and end in beta positions
 * - Distance between positions determines the circular type:
 *   - Distance 0: Same position (static)
 *   - Distance 2 or 6: Adjacent 90° (quartered)
 *   - Distance 4: Opposite 180° (halved)
 */
@injectable()
export class SequenceAnalysisService implements ISequenceAnalysisService {
	constructor(
		@inject(TYPES.IBetaDetectionService)
		private readonly betaDetectionService: IBetaDetectionService
	) {}

	/**
	 * Analyze a sequence for circular properties
	 */
	analyzeCircularity(sequence: SequenceData): CircularityAnalysis {
		// Get start and end beats
		const startBeat = this.getStartBeat(sequence);
		const endBeat = this.getEndBeat(sequence);

		// Default non-circular result
		const defaultResult: CircularityAnalysis = {
			isCircular: false,
			circularType: null,
			startPosition: null,
			endPosition: null,
			startIsBeta: false,
			endIsBeta: false,
			possibleCapTypes: [],
			description: "Not circular",
		};

		// Check if we have valid start and end beats
		if (!startBeat || !endBeat) {
			return defaultResult;
		}

		// Get start and end positions
		const startPosition = startBeat.startPosition;
		const endPosition = endBeat.endPosition;

		if (!startPosition || !endPosition) {
			return defaultResult;
		}

		// Check if both positions are beta positions
		const startIsBeta = this.isBetaPosition(startPosition);
		const endIsBeta = this.isBetaPosition(endPosition);

		if (!startIsBeta || !endIsBeta) {
			return {
				...defaultResult,
				startPosition,
				endPosition,
				startIsBeta,
				endIsBeta,
				description: "Positions are not both beta positions",
			};
		}

		// Determine circular type
		const circularType = this.getCircularType(startPosition, endPosition);

		if (!circularType) {
			return {
				...defaultResult,
				startPosition,
				endPosition,
				startIsBeta,
				endIsBeta,
				description: "Invalid circular relationship",
			};
		}

		// Get possible CAP types based on circular type
		const possibleCapTypes = this.getPossibleCapTypesForCircularType(circularType);

		return {
			isCircular: true,
			circularType,
			startPosition,
			endPosition,
			startIsBeta,
			endIsBeta,
			possibleCapTypes,
			description: this.buildCircularDescription(startPosition, endPosition, circularType),
		};
	}

	/**
	 * Check if a sequence is circular-capable (simple boolean check)
	 */
	isCircularCapable(sequence: SequenceData): boolean {
		const analysis = this.analyzeCircularity(sequence);
		return analysis.isCircular;
	}

	/**
	 * Get possible CAP types for a circular sequence
	 */
	getPossibleCapTypes(sequence: SequenceData): readonly StrictCapType[] {
		const analysis = this.analyzeCircularity(sequence);
		return analysis.possibleCapTypes;
	}

	/**
	 * Determine the circular relationship between two beta positions
	 *
	 * Beta positions form an octagon with 8 positions (1-8).
	 * We calculate the shortest distance around the octagon:
	 * - Distance 0: Same position
	 * - Distance 2 or 6: Adjacent 90° (quartered)
	 * - Distance 4: Opposite 180° (halved)
	 */
	getCircularType(startPosition: GridPosition, endPosition: GridPosition): CircularType | null {
		// Extract beta numbers (e.g., "beta1" → 1)
		const startNum = this.extractBetaNumber(startPosition);
		const endNum = this.extractBetaNumber(endPosition);

		if (startNum === null || endNum === null) {
			return null;
		}

		// Calculate distance around the octagon (shortest path)
		const rawDistance = Math.abs(endNum - startNum);
		const distance = Math.min(rawDistance, 8 - rawDistance);

		// Determine circular type based on distance
		switch (distance) {
			case 0:
				return 'same';
			case 2:
				return 'quartered';
			case 4:
				return 'halved';
			default:
				return null; // Invalid distance for circular patterns
		}
	}

	/**
	 * Check if a position is a beta position
	 */
	isBetaPosition(position: GridPosition): boolean {
		return this.betaDetectionService.isBetaPosition(position);
	}

	/**
	 * Get the first beat with valid pictograph data (start beat)
	 */
	getStartBeat(sequence: SequenceData): BeatData | null {
		if (!sequence.beats || sequence.beats.length === 0) {
			return null;
		}

		// Find first beat with a start position
		for (const beat of sequence.beats) {
			if (beat.startPosition && !beat.isBlank) {
				return beat;
			}
		}

		return null;
	}

	/**
	 * Get the last beat with valid pictograph data (end beat)
	 */
	getEndBeat(sequence: SequenceData): BeatData | null {
		if (!sequence.beats || sequence.beats.length === 0) {
			return null;
		}

		// Find last beat with an end position (iterate backwards)
		for (let i = sequence.beats.length - 1; i >= 0; i--) {
			const beat = sequence.beats[i];
			if (beat.endPosition && !beat.isBlank) {
				return beat;
			}
		}

		return null;
	}

	/**
	 * Get a human-readable description of the circular relationship
	 */
	getCircularDescription(analysis: CircularityAnalysis): string {
		return analysis.description;
	}

	/**
	 * Get possible CAP types based on circular type
	 *
	 * Mapping:
	 * - 'same' → ['static']
	 * - 'halved' → ['mirrored']
	 * - 'quartered' → ['rotated']
	 */
	private getPossibleCapTypesForCircularType(circularType: CircularType): readonly StrictCapType[] {
		switch (circularType) {
			case 'same':
				return ['static'] as const;
			case 'halved':
				return ['mirrored'] as const;
			case 'quartered':
				return ['rotated'] as const;
		}
	}

	/**
	 * Build a human-readable description
	 */
	private buildCircularDescription(
		startPosition: GridPosition,
		endPosition: GridPosition,
		circularType: CircularType
	): string {
		const typeDescriptions: Record<CircularType, string> = {
			same: 'Same position',
			halved: 'Opposite/halved position (180°)',
			quartered: 'Adjacent/quartered position (90°)',
		};

		const typeDesc = typeDescriptions[circularType];
		return `${typeDesc}: ${startPosition} → ${endPosition}`;
	}

	/**
	 * Extract beta number from a GridPosition
	 *
	 * @param position - Grid position like GridPosition.BETA1
	 * @returns The beta number (1-8) or null if not a beta position
	 *
	 * @example
	 * extractBetaNumber(GridPosition.BETA1) → 1
	 * extractBetaNumber(GridPosition.BETA5) → 5
	 * extractBetaNumber(GridPosition.ALPHA1) → null
	 */
	private extractBetaNumber(position: GridPosition): number | null {
		const positionStr = position.toString().toLowerCase();

		// Check if it's a beta position and extract the number
		const match = positionStr.match(/^beta(\d+)$/);
		if (!match) {
			return null;
		}

		const num = parseInt(match[1], 10);

		// Validate it's in range 1-8
		if (num < 1 || num > 8) {
			return null;
		}

		return num;
	}
}
