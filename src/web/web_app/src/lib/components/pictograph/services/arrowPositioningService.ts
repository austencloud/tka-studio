/**
 * Arrow Positioning Service for Svelte Components
 *
 * Provides a simple interface for arrow positioning that uses the sophisticated
 * positioning pipeline we've built and tested.
 */

import type { ArrowData, MotionData, PictographData } from '$lib/domain';
import { ArrowType } from '$lib/domain';
import type { IArrowPositioningOrchestrator } from '$lib/services/positioning';
import { getPositioningServiceFactory } from '$lib/services/positioning/PositioningServiceFactory';

export interface ArrowPositionResult {
	x: number;
	y: number;
	rotation: number;
}

export interface ArrowPositioningInput {
	arrow_type: 'blue' | 'red';
	motion_type: string;
	location: string;
	grid_mode: string;
	turns: number;
	letter?: string;
	start_orientation?: string;
	end_orientation?: string;
}

export interface Position {
	x: number;
	y: number;
}

export class ArrowPositioningService {
	private orchestrator: IArrowPositioningOrchestrator;

	constructor() {
		// Use the singleton factory to get a properly configured orchestrator
		// This prevents recreating placement services and reloading data on hot reload
		const factory = getPositioningServiceFactory();
		this.orchestrator = factory.createPositioningOrchestrator();
	}

	/**
	 * Calculate arrow position using the sophisticated positioning pipeline
	 */
	async calculatePosition(
		arrowData: ArrowData,
		motionData: MotionData,
		pictographData: PictographData
	): Promise<ArrowPositionResult> {
		console.log(
			`🎯 ArrowPositioningService.calculatePosition called for ${arrowData.color} arrow`
		);
		console.log(`Arrow data:`, {
			motion_type: arrowData.motion_type,
			start_orientation: arrowData.start_orientation,
			end_orientation: arrowData.end_orientation,
			turns: arrowData.turns,
			position_x: arrowData.position_x,
			position_y: arrowData.position_y,
		});
		console.log(`Motion data:`, {
			motion_type: motionData.motion_type,
			start_loc: motionData.start_loc,
			end_loc: motionData.end_loc,
			turns: motionData.turns,
		});

		try {
			// Use the sophisticated positioning pipeline
			console.log(`🔧 Calling orchestrator.calculateArrowPosition...`);
			const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
				arrowData,
				pictographData,
				motionData
			);

			console.log(`✅ Orchestrator returned: (${x}, ${y}) rotation: ${rotation}°`);
			return { x, y, rotation };
		} catch (error) {
			console.error('Sophisticated positioning failed, using fallback:', error);
			return this.getFallbackPosition(motionData);
		}
	}

	/**
	 * Synchronous position calculation (may not include full adjustments)
	 */
	calculatePositionSync(
		arrowData: ArrowData,
		motionData: MotionData,
		pictographData: PictographData
	): ArrowPositionResult {
		try {
			console.log(`🎯 Calculating sync position for ${arrowData.color} arrow`);
			console.log(
				`Motion: ${motionData.motion_type}, Start: ${motionData.start_loc}, End: ${motionData.end_loc}`
			);

			// Use the synchronous positioning method
			const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
				arrowData,
				pictographData,
				motionData
			);

			console.log(`✅ Calculated sync position: (${x}, ${y}) rotation: ${rotation}°`);

			return { x, y, rotation };
		} catch (error) {
			console.error('Synchronous positioning failed, using fallback:', error);
			return this.getFallbackPosition(motionData);
		}
	}

	/**
	 * Determine if arrow should be mirrored based on motion data
	 */
	shouldMirror(
		arrowData: ArrowData,
		_motionData: MotionData,
		pictographData: PictographData
	): boolean {
		try {
			return this.orchestrator.shouldMirrorArrow(arrowData, pictographData);
		} catch (error) {
			console.warn('Failed to determine mirror state, using default:', error);
			return false;
		}
	}

	/**
	 * Legacy interface for backward compatibility
	 */
	async calculatePosition_legacy(input: ArrowPositioningInput): Promise<Position> {
		const arrowData: ArrowData = {
			color: input.arrow_type,
			arrow_type: input.arrow_type === 'blue' ? ArrowType.BLUE : ArrowType.RED,
			location: input.location,
			motion_type: input.motion_type,
		} as ArrowData;

		const motionData: MotionData = {
			motion_type: input.motion_type,
			start_loc: input.location,
			start_ori: input.start_orientation || 'in',
			end_ori: input.end_orientation || 'in',
			prop_rot_dir: 'cw',
			turns: input.turns,
		} as MotionData;

		const pictographData: PictographData = {
			letter: input.letter || 'A',
			grid_mode: input.grid_mode,
			motions: {
				[input.arrow_type]: motionData,
			},
		} as PictographData;

		const result = await this.calculatePosition(arrowData, motionData, pictographData);
		return { x: result.x, y: result.y };
	}

	/**
	 * Fallback position calculation using basic coordinates
	 */
	private getFallbackPosition(motionData: MotionData): ArrowPositionResult {
		const coordinates = this.calculateLocationCoordinates(motionData.start_loc || 'center');
		console.log(`🔄 Using fallback position: (${coordinates.x}, ${coordinates.y})`);

		return {
			x: coordinates.x,
			y: coordinates.y,
			rotation: 0,
		};
	}

	/**
	 * Basic coordinate calculation as fallback
	 */
	private calculateLocationCoordinates(location: string): { x: number; y: number } {
		// Diamond grid coordinates from legacy desktop circle_coords.json
		const diamondCoordinates: Record<string, { x: number; y: number }> = {
			// Cardinal directions (hand_points)
			n: { x: 475.0, y: 331.9 },
			e: { x: 618.1, y: 475.0 },
			s: { x: 475.0, y: 618.1 },
			w: { x: 331.9, y: 475.0 },

			// Diagonal directions (layer2_points) - used for arrows
			ne: { x: 618.1, y: 331.9 },
			se: { x: 618.1, y: 618.1 },
			sw: { x: 331.9, y: 618.1 },
			nw: { x: 331.9, y: 331.9 },

			// Center point
			center: { x: 475.0, y: 475.0 },
		};

		const coords = diamondCoordinates[location.toLowerCase()];
		return coords || { x: 475.0, y: 475.0 };
	}
}

// Create singleton instance
export const arrowPositioningService = new ArrowPositioningService();
