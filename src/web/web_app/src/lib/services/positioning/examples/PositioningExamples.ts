/**
 * Enhanced Arrow Positioning Usage Examples
 *
 * This file demonstrates how to use the comprehensive arrow positioning services
 * to achieve functional parity with the reference implementation.
 */

import type { ArrowData, MotionData, PictographData } from '$lib/domain';
import type { IArrowPositioningOrchestrator } from '$lib/services/positioning';
import {
	createPositioningOrchestrator,
	getPositioningServiceFactory,
} from '$lib/services/positioning/PositioningServiceFactory';

/**
 * Example 1: Using the Enhanced Positioning Orchestrator
 *
 * The orchestrator coordinates all positioning services for complete arrow positioning.
 */
export async function exampleEnhancedPositioning() {
	// Get the orchestrator from the factory instead of DI container
	const orchestrator = createPositioningOrchestrator();

	// Example pictograph data
	const pictographData = {
		id: 'example',
		letter: 'A',
		grid_mode: 'diamond',
		grid_data: { mode: 'diamond' } as any,
		arrows: {
			blue: {
				color: 'blue',
				is_visible: true,
				position_x: 0,
				position_y: 0,
				rotation_angle: 0,
			} as ArrowData,
			red: {
				color: 'red',
				is_visible: true,
				position_x: 0,
				position_y: 0,
				rotation_angle: 0,
			} as ArrowData,
		},
		motions: {
			blue: {
				motion_type: 'pro' as any,
				start_loc: 'north' as any,
				end_loc: 'east' as any,
				start_ori: 'in' as any,
				end_ori: 'out' as any,
				prop_rot_dir: 'clockwise' as any,
				turns: 1,
				is_visible: true,
			},
			red: {
				motion_type: 'anti' as any,
				start_loc: 'south' as any,
				end_loc: 'west' as any,
				start_ori: 'in' as any,
				end_ori: 'out' as any,
				prop_rot_dir: 'counter_clockwise' as any,
				turns: 0.5,
				is_visible: true,
			},
		},
		props: {},
		beat: 1,
		is_new: false,
		is_current: false,
		is_blank: false,
		is_mirrored: false,
		metadata: {},
	} as PictographData;

	// Calculate all arrow positions
	const updatedPictograph = await orchestrator.calculateAllArrowPositions(pictographData);

	console.log('Enhanced positioning results:');
	console.log('Blue arrow:', updatedPictograph.arrows?.blue);
	console.log('Red arrow:', updatedPictograph.arrows?.red);

	return updatedPictograph;
}

/**
 * Example 2: Using Individual Positioning Services
 *
 * For more granular control, you can use individual services directly.
 */
export async function exampleGranularPositioning() {
	// Get individual services from the factory instead of DI container
	const factory = getPositioningServiceFactory();
	const locationCalculator = factory.createLocationCalculator();
	const rotationCalculator = factory.createRotationCalculator();
	const adjustmentCalculator = factory.createAdjustmentCalculator();
	const coordinateSystem = factory.createCoordinateSystemService();

	// Example motion data
	const motion = {
		motion_type: 'dash' as any,
		start_loc: 'north' as any,
		end_loc: 'south' as any,
		start_ori: 'in' as any,
		end_ori: 'out' as any,
		prop_rot_dir: 'no_rotation' as any,
		turns: 0,
		is_visible: true,
	} as MotionData;

	const pictographData = {
		id: 'dash_example',
		letter: 'DASH_EXAMPLE',
		grid_mode: 'diamond',
		grid_data: { mode: 'diamond' } as any,
		motions: { blue: motion },
		arrows: {},
		props: {},
		beat: 1,
		is_new: false,
		is_current: false,
		is_blank: false,
		is_mirrored: false,
		metadata: {},
	} as PictographData;

	// Step 1: Calculate location using sophisticated location calculator
	const location = locationCalculator.calculateLocation(motion, pictographData);
	console.log('Calculated location:', location);

	// Step 2: Get initial position from precise coordinate system
	const initialPosition = coordinateSystem.getInitialPosition(motion, location);
	console.log('Initial position:', initialPosition);

	// Step 3: Calculate rotation using comprehensive rotation calculator
	const rotation = rotationCalculator.calculateRotation(motion, location);
	console.log('Calculated rotation:', rotation);

	// Step 4: Calculate adjustment using sophisticated adjustment calculator
	const adjustment = await adjustmentCalculator.calculateAdjustment(
		pictographData,
		motion,
		pictographData.letter || '',
		location,
		'blue'
	);
	console.log('Calculated adjustment:', adjustment);

	// Step 5: Combine all calculations
	const finalX = initialPosition.x + adjustment.x;
	const finalY = initialPosition.y + adjustment.y;

	console.log(`Final position: (${finalX}, ${finalY}, ${rotation}°)`);

	return { x: finalX, y: finalY, rotation };
}

/**
 * Example 3: Using the Factory Pattern
 *
 * Create positioning services using the factory for consistent configuration.
 */
export function exampleFactoryPattern() {
	// Create orchestrator using factory
	const orchestrator = createPositioningOrchestrator();

	// Factory ensures all services are properly wired together
	console.log('Orchestrator created via factory:', orchestrator);

	return orchestrator;
}

/**
 * Integration Helper: Update Existing Arrow Positioning Service
 *
 * Shows how to integrate the enhanced positioning into existing components.
 */
export class EnhancedArrowPositioningIntegration {
	private orchestrator: IArrowPositioningOrchestrator;

	constructor() {
		// Use the enhanced orchestrator instead of the basic one
		this.orchestrator = createPositioningOrchestrator();
	}

	/**
	 * Enhanced version of the basic calculatePosition method.
	 * Drop-in replacement for existing arrow positioning logic.
	 */
	async calculatePosition(input: {
		arrow_type: 'blue' | 'red';
		motion_type: string;
		location: string;
		grid_mode: string;
		turns: number;
		letter?: string;
		start_orientation?: string;
		end_orientation?: string;
	}): Promise<{ x: number; y: number; rotation: number }> {
		// Convert input to PictographData format
		const motionData: MotionData = {
			motion_type: input.motion_type as any,
			start_loc: input.location as any,
			end_loc: input.location as any, // Simplified
			start_ori: (input.start_orientation || 'in') as any,
			end_ori: (input.end_orientation || 'in') as any,
			prop_rot_dir: 'clockwise' as any, // Default
			turns: input.turns,
			is_visible: true,
		};

		const arrowData: ArrowData = {
			color: input.arrow_type,
			is_visible: true,
			position_x: 0,
			position_y: 0,
			rotation_angle: 0,
		} as ArrowData;

		const pictographData: PictographData = {
			id: 'example',
			letter: input.letter || 'A',
			grid_mode: input.grid_mode,
			grid_data: {
				grid_mode: input.grid_mode as any,
				center_x: 0,
				center_y: 0,
				radius: 100,
				grid_points: {},
			},
			arrows: { [input.arrow_type]: arrowData },
			motions: { [input.arrow_type]: motionData },
			props: {},
			beat: 1,
			is_new: false,
			is_current: false,
			is_blank: false,
			is_mirrored: false,
			metadata: {},
		} as PictographData;

		// Use enhanced positioning (synchronous version for compatibility)
		const [x, y, rotation] = this.orchestrator.calculateArrowPosition(
			arrowData,
			pictographData,
			motionData
		);

		return { x, y, rotation };
	}
}

/**
 * Export all examples for easy testing
 */
export const positioningExamples = {
	enhancedPositioning: exampleEnhancedPositioning,
	granularPositioning: exampleGranularPositioning,
	factoryPattern: exampleFactoryPattern,
	integration: EnhancedArrowPositioningIntegration,
};
