/**
 * Legacy Arrow Positioning Orchestrator
 *
 * DEPRECATED: This is the old basic orchestrator that hardcodes adjustments to (0,0).
 * It was ignoring the sophisticated ArrowAdjustmentCalculator pipeline.
 *
 * Kept for reference only. The new ArrowPositioningOrchestrator uses the full pipeline.
 */

import type { ArrowData, MotionData, PictographData } from '$lib/domain';
import type {
	IArrowAdjustmentCalculator,
	IArrowCoordinateSystemService,
	IArrowLocationCalculator,
	IArrowPositioningOrchestrator,
	IArrowRotationCalculator,
} from '../../core-services';
import type { Point } from '../../types';

export class LegacyArrowPositioningOrchestrator implements IArrowPositioningOrchestrator {
	private locationCalculator: IArrowLocationCalculator;
	private rotationCalculator: IArrowRotationCalculator;
	private coordinateSystem: IArrowCoordinateSystemService;

	private mirrorConditions = {
		anti: { cw: true, ccw: false },
		other: { cw: false, ccw: true },
	};

	constructor(
		locationCalculator: IArrowLocationCalculator,
		rotationCalculator: IArrowRotationCalculator,
		_adjustmentCalculator: IArrowAdjustmentCalculator,
		coordinateSystem: IArrowCoordinateSystemService
	) {
		this.locationCalculator = locationCalculator;
		this.rotationCalculator = rotationCalculator;
		this.coordinateSystem = coordinateSystem;
	}

	calculateArrowPosition(
		arrowData: ArrowData,
		pictographData: PictographData,
		motionData?: MotionData
	): [number, number, number] {
		/**Calculate arrow position using streamlined microservices pipeline.*/
		const motion = motionData || this.getMotionFromPictograph(arrowData, pictographData);

		if (!motion) {
			console.warn(`No motion data for ${arrowData.color}, returning center position`);
			const center = this.coordinateSystem.getSceneCenter();
			return [center.x, center.y, 0.0];
		}

		const location = this.locationCalculator.calculateLocation(motion, pictographData);
		let initialPosition = this.coordinateSystem.getInitialPosition(motion, location);
		initialPosition = this.ensureValidPosition(initialPosition);

		const rotation = this.rotationCalculator.calculateRotation(motion, location);

		// PROBLEM: This is hardcoded to (0,0) - ignores the ArrowAdjustmentCalculator!
		const adjustmentX = 0;
		const adjustmentY = 0;
		console.log(`🔧 Extracted adjustment values: [${adjustmentX}, ${adjustmentY}]`);

		const finalX = initialPosition.x + adjustmentX;
		const finalY = initialPosition.y + adjustmentY;

		return [finalX, finalY, rotation];
	}

	calculateAllArrowPositions(pictographData: PictographData): PictographData {
		/**Calculate positions and mirror states for all arrows in the pictograph.*/
		let updatedPictograph = pictographData;

		for (const [color, arrowData] of Object.entries(pictographData.arrows || {})) {
			const motionData = pictographData.motions?.[color];

			if (arrowData.is_visible && motionData) {
				// Calculate position and rotation
				const [x, y, rotation] = this.calculateArrowPosition(
					arrowData,
					pictographData,
					motionData
				);

				// Calculate mirror state
				const shouldMirror = this.shouldMirrorArrow(arrowData, pictographData);

				// Update arrow with all calculated values
				updatedPictograph = this.updateArrowInPictograph(updatedPictograph, color, {
					position_x: x,
					position_y: y,
					rotation_angle: rotation,
					is_mirrored: shouldMirror,
				});
			}
		}

		return updatedPictograph;
	}

	shouldMirrorArrow(arrowData: ArrowData, pictographData?: PictographData): boolean {
		/**Determine if arrow should be mirrored.*/
		let motion: MotionData | undefined;
		if (pictographData?.motions) {
			motion = pictographData.motions[arrowData.color];
		}

		if (!motion) {
			return false;
		}

		const motionType = (motion.motion_type || '').toLowerCase();
		const propRotDir = (motion.prop_rot_dir || '').toLowerCase();

		if (motionType === 'anti') {
			const antiConditions = this.mirrorConditions.anti;
			return antiConditions[propRotDir as keyof typeof antiConditions] || false;
		}
		const otherConditions = this.mirrorConditions.other;
		return otherConditions[propRotDir as keyof typeof otherConditions] || false;
	}

	applyMirrorTransform(arrowItem: HTMLElement | SVGElement, shouldMirror: boolean): void {
		/**Apply mirror transformation.*/
		try {
			const rect = arrowItem.getBoundingClientRect();
			const centerX = rect.left + rect.width / 2;
			const centerY = rect.top + rect.height / 2;

			const scaleX = shouldMirror ? -1 : 1;
			const transform = `translate(${centerX}px, ${centerY}px) scale(${scaleX}, 1) translate(${-centerX}px, ${-centerY}px)`;

			arrowItem.style.transform = transform;
		} catch (error) {
			console.warn('Failed to apply mirror transform:', error);
		}
	}

	private getMotionFromPictograph(
		arrowData: ArrowData,
		pictographData: PictographData
	): MotionData | undefined {
		/**Extract motion data from pictograph data.*/
		if (!pictographData?.motions) {
			return undefined;
		}
		return pictographData.motions[arrowData.color];
	}

	private ensureValidPosition(initialPosition: Point): Point {
		/**Ensure position object has valid x and y attributes.*/
		if (
			initialPosition &&
			typeof initialPosition.x === 'number' &&
			typeof initialPosition.y === 'number'
		) {
			return initialPosition;
		}

		return { x: 475.0, y: 475.0 };
	}

	private updateArrowInPictograph(
		pictographData: PictographData,
		color: string,
		updates: Partial<ArrowData>
	): PictographData {
		/**Update arrow properties in pictograph data.*/
		// Create a deep copy and update the specific arrow
		const updatedPictograph = { ...pictographData };

		if (updatedPictograph.arrows && updatedPictograph.arrows[color]) {
			updatedPictograph.arrows = {
				...updatedPictograph.arrows,
				[color]: {
					...updatedPictograph.arrows[color],
					...updates,
				},
			};
			console.log(`✅ Updated ${color} arrow with:`, updates);
		} else {
			console.warn(`❌ Could not update ${color} arrow: not found in pictograph data`);
		}

		return updatedPictograph;
	}
}
