/**
 * Test for the new ArrowPositioningOrchestrator
 *
 * Verifies that it properly uses the ArrowAdjustmentCalculator instead of hardcoded (0,0).
 */

import type { ArrowData, MotionData, PictographData } from '$lib/domain';
import { ArrowType, GridMode, Location, MotionType } from '$lib/domain';
import { describe, expect, it } from 'vitest';
import { ArrowAdjustmentCalculator } from '../../calculation/ArrowAdjustmentCalculator';
import { ArrowLocationCalculator } from '../../calculation/ArrowLocationCalculator';
import { ArrowRotationCalculator } from '../../calculation/ArrowRotationCalculator';
import { ArrowCoordinateSystemService } from '../../coordinate_system/ArrowCoordinateSystemService';
import { ArrowPositioningOrchestrator } from '../ArrowPositioningOrchestrator';

describe('ArrowPositioningOrchestrator Integration', () => {
	it('should use ArrowAdjustmentCalculator for sophisticated positioning', async () => {
		// Create real services
		const locationCalculator = new ArrowLocationCalculator();
		const rotationCalculator = new ArrowRotationCalculator();
		const adjustmentCalculator = new ArrowAdjustmentCalculator();
		const coordinateSystem = new ArrowCoordinateSystemService();

		// Create the orchestrator with our sophisticated pipeline
		const orchestrator = new ArrowPositioningOrchestrator(
			locationCalculator,
			rotationCalculator,
			adjustmentCalculator,
			coordinateSystem
		);

		const arrowData: ArrowData = {
			color: 'blue',
			arrow_type: ArrowType.MOTION,
			is_visible: true,
		};

		const motionData: MotionData = {
			motion_type: MotionType.PRO,
			prop_rot_dir: 'cw',
			start_location: Location.NORTH,
			end_location: Location.SOUTH,
		};

		const pictographData: PictographData = {
			letter: 'A',
			grid_mode: GridMode.DIAMOND,
			arrows: { blue: arrowData },
			motions: { blue: motionData },
		};

		// Test the async method (which should use full adjustment pipeline)
		const [x, y, rotation] = await orchestrator.calculateArrowPositionAsync(
			arrowData,
			pictographData,
			motionData
		);

		// The position should not be just the initial position (should include adjustments)
		expect(x).toBeTypeOf('number');
		expect(y).toBeTypeOf('number');
		expect(rotation).toBeTypeOf('number');

		// Log for manual verification that it's using adjustments
		console.log(`Final position: (${x}, ${y}) with rotation ${rotation}°`);

		// The key test: position should be different from just the initial coordinate system position
		const initialPosition = coordinateSystem.getInitialPosition(motionData, Location.SOUTH);
		console.log(`Initial position: (${initialPosition.x}, ${initialPosition.y})`);

		// If adjustments are working, the final position should be different
		// (unless the adjustment happens to be exactly (0,0) which is unlikely for pro motion)
		const hasAdjustment = x !== initialPosition.x || y !== initialPosition.y;
		console.log(`Has adjustment applied: ${hasAdjustment}`);

		// This should be true now that we're using the real ArrowAdjustmentCalculator
		expect(hasAdjustment).toBe(true);
	});

	it('should handle all arrows in a pictograph with sophisticated positioning', () => {
		// Create real services
		const locationCalculator = new ArrowLocationCalculator();
		const rotationCalculator = new ArrowRotationCalculator();
		const adjustmentCalculator = new ArrowAdjustmentCalculator();
		const coordinateSystem = new ArrowCoordinateSystemService();

		const orchestrator = new ArrowPositioningOrchestrator(
			locationCalculator,
			rotationCalculator,
			adjustmentCalculator,
			coordinateSystem
		);

		const pictographData: PictographData = {
			letter: 'B',
			grid_mode: GridMode.DIAMOND,
			arrows: {
				blue: {
					color: 'blue',
					arrow_type: ArrowType.MOTION,
					is_visible: true,
				},
				red: {
					color: 'red',
					arrow_type: ArrowType.MOTION,
					is_visible: true,
				},
			},
			motions: {
				blue: {
					motion_type: MotionType.PRO,
					prop_rot_dir: 'cw',
					start_location: Location.NORTH,
					end_location: Location.SOUTH,
				},
				red: {
					motion_type: MotionType.ANTI,
					prop_rot_dir: 'ccw',
					start_location: Location.EAST,
					end_location: Location.WEST,
				},
			},
		};

		// Process all arrows
		const result = orchestrator.calculateAllArrowPositions(pictographData);

		// Verify that positions were calculated for all arrows
		expect(result.arrows?.blue?.position_x).toBeTypeOf('number');
		expect(result.arrows?.blue?.position_y).toBeTypeOf('number');
		expect(result.arrows?.blue?.rotation_angle).toBeTypeOf('number');

		expect(result.arrows?.red?.position_x).toBeTypeOf('number');
		expect(result.arrows?.red?.position_y).toBeTypeOf('number');
		expect(result.arrows?.red?.rotation_angle).toBeTypeOf('number');

		console.log('Blue arrow final position:', {
			x: result.arrows?.blue?.position_x,
			y: result.arrows?.blue?.position_y,
			rotation: result.arrows?.blue?.rotation_angle,
		});

		console.log('Red arrow final position:', {
			x: result.arrows?.red?.position_x,
			y: result.arrows?.red?.position_y,
			rotation: result.arrows?.red?.rotation_angle,
		});
	});
});
