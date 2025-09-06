import { BetaPropDirectionCalculator } from './BetaPropDirectionCalculator';
import type { PictographData } from '$lib/types/PictographData';
import type { PropData } from '$lib/components/objects/Prop/PropData';
import type { Direction } from '$lib/types/Types';
import type { MotionData } from '$lib/components/objects/Motion/MotionData';
import { PRO, ANTI, FLOAT } from '$lib/types/Constants';

/**
 * Interface for the offset calculator
 */
interface BetaOffsetCalculator {
	calculateNewPositionWithOffset(
		coords: { x: number; y: number },
		direction: Direction
	): { x: number; y: number };
}

/**
 * Class that handles repositioning props based on different letter types
 * TypeScript implementation of the Python RepositionBetaByLetterHandler
 */
export default class RepositionBetaByLetterHandler {
	private pictographData: PictographData;
	private dirCalculator: BetaPropDirectionCalculator;
	private betaOffsetCalculator: BetaOffsetCalculator;

	/**
	 * Constructor for the RepositionBetaByLetterHandler
	 * @param directionCalculator The direction calculator to use
	 * @param pictographData The pictograph data to work with
	 */
	constructor(directionCalculator: BetaPropDirectionCalculator, pictographData: PictographData) {
		this.pictographData = pictographData;
		this.dirCalculator = directionCalculator;

		// Initialize the offset calculator
		this.betaOffsetCalculator = {
			calculateNewPositionWithOffset: (coords: { x: number; y: number }, direction: Direction) => {
				const offset = 25; // Standard offset value
				const movementMap: Record<Direction, { x: number; y: number }> = {
					up: { x: 0, y: -offset },
					down: { x: 0, y: offset },
					left: { x: -offset, y: 0 },
					right: { x: offset, y: 0 },
					upright: { x: offset, y: -offset },
					upleft: { x: -offset, y: -offset },
					downright: { x: offset, y: offset },
					downleft: { x: -offset, y: offset }
				};
				const movement = movementMap[direction] || { x: 0, y: 0 };
				return {
					x: coords.x + movement.x,
					y: coords.y + movement.y
				};
			}
		};
	}

	/**
	 * Repositions props for G and H letters
	 */
	reposition_G_H(): void {
		const redMotion = this.pictographData.redMotionData;
		const redPropData = this.pictographData.redPropData;
		const bluePropData = this.pictographData.bluePropData;

		if (!redMotion || !redPropData || !bluePropData) return;

		// Get the direction from red motion
		const furtherDirection = this.dirCalculator.getDirectionFromMotion(redMotion);
		if (!furtherDirection) return;

		// Get the opposite direction
		const otherDirection = this.dirCalculator.getOppositeDirection(furtherDirection);

		// Move the props in opposite directions
		this.moveProp(redPropData, furtherDirection);
		this.moveProp(bluePropData, otherDirection);
	}

	/**
	 * Repositions props for I letter
	 */
	reposition_I(): void {
		const redMotion = this.pictographData.redMotionData;
		const blueMotion = this.pictographData.blueMotionData;
		const redPropData = this.pictographData.redPropData;
		const bluePropData = this.pictographData.bluePropData;

		if (!redMotion || !blueMotion || !redPropData || !bluePropData) return;

		// Find pro and anti props
		const proProp =
			redMotion.motionType === PRO
				? redPropData
				: blueMotion.motionType === PRO
					? bluePropData
					: null;
		const antiProp =
			redMotion.motionType === ANTI
				? redPropData
				: blueMotion.motionType === ANTI
					? bluePropData
					: null;

		if (!proProp || !antiProp) return;

		// Find pro motion
		const proMotion = proProp === redPropData ? redMotion : blueMotion;

		// Get directions
		const proDirection = this.dirCalculator.getDirectionFromMotion(proMotion);
		if (!proDirection) return;

		const antiDirection = this.dirCalculator.getOppositeDirection(proDirection);

		// Move props
		this.moveProp(proProp, proDirection);
		this.moveProp(antiProp, antiDirection);
	}

	/**
	 * Repositions props for J, K, and L letters
	 */
	reposition_J_K_L(): void {
		const redMotion = this.pictographData.redMotionData;
		const blueMotion = this.pictographData.blueMotionData;
		const redPropData = this.pictographData.redPropData;
		const bluePropData = this.pictographData.bluePropData;

		if (!redMotion || !blueMotion || !redPropData || !bluePropData) return;

		// Get directions from motions
		const redDir = this.dirCalculator.getDirectionFromMotion(redMotion);
		const blueDir = this.dirCalculator.getDirectionFromMotion(blueMotion);

		if (redDir && blueDir) {
			this.moveProp(redPropData, redDir);
			this.moveProp(bluePropData, blueDir);
		}
	}

	/**
	 * Repositions props for Y and Z letters
	 */
	reposition_Y_Z(): void {
		const redMotion = this.pictographData.redMotionData;
		const blueMotion = this.pictographData.blueMotionData;
		const redPropData = this.pictographData.redPropData;
		const bluePropData = this.pictographData.bluePropData;

		if (!redMotion || !blueMotion || !redPropData || !bluePropData) return;

		// Find shift and static motions
		const shiftMotion = this.isShiftMotion(redMotion)
			? redMotion
			: this.isShiftMotion(blueMotion)
				? blueMotion
				: null;
		const staticMotion =
			redMotion.motionType === 'static'
				? redMotion
				: blueMotion.motionType === 'static'
					? blueMotion
					: null;

		if (!shiftMotion || !staticMotion) return;

		// Get direction from shift motion
		const direction = this.dirCalculator.getDirectionFromMotion(shiftMotion);
		if (!direction) return;

		// Find associated props
		const shiftProp = shiftMotion.color === 'red' ? redPropData : bluePropData;
		const staticProp = staticMotion.color === 'red' ? redPropData : bluePropData;

		// Move props
		this.moveProp(shiftProp, direction);
		this.moveProp(staticProp, this.dirCalculator.getOppositeDirection(direction));
	}

	/**
	 * Repositions props for Y' and Z' letters (dash variants)
	 */
	reposition_Y_dash_Z_dash(): void {
		const redMotion = this.pictographData.redMotionData;
		const blueMotion = this.pictographData.blueMotionData;
		const redPropData = this.pictographData.redPropData;
		const bluePropData = this.pictographData.bluePropData;

		if (!redMotion || !blueMotion || !redPropData || !bluePropData) return;

		// Find shift and dash motions
		const shiftMotion = this.isShiftMotion(redMotion)
			? redMotion
			: this.isShiftMotion(blueMotion)
				? blueMotion
				: null;
		const dashMotion =
			redMotion.motionType === 'dash'
				? redMotion
				: blueMotion.motionType === 'dash'
					? blueMotion
					: null;

		if (!shiftMotion || !dashMotion) return;

		// Get direction from shift motion
		const direction = this.dirCalculator.getDirectionFromMotion(shiftMotion);
		if (!direction) return;

		// Find associated props
		const shiftProp = shiftMotion.color === 'red' ? redPropData : bluePropData;
		const dashProp = dashMotion.color === 'red' ? redPropData : bluePropData;

		// Move props
		this.moveProp(shiftProp, direction);
		this.moveProp(dashProp, this.dirCalculator.getOppositeDirection(direction));
	}

	/**
	 * Repositions props for psi letter
	 */
	reposition_psi(): void {
		this.repositionNonShift();
	}

	/**
	 * Repositions props for psi' letter (dash variant)
	 */
	reposition_psi_dash(): void {
		this.repositionNonShift();
	}

	/**
	 * Repositions props for beta letter
	 */
	reposition_beta(): void {
		this.repositionNonShift();
	}

	/**
	 * Common repositioning logic for non-shift letters (psi, psi', beta)
	 */
	private repositionNonShift(): void {
		const redPropData = this.pictographData.redPropData;
		const bluePropData = this.pictographData.bluePropData;

		if (!redPropData || !bluePropData) return;

		// Get direction for non-shift
		const direction = this.dirCalculator.getDirection(redPropData);
		if (!direction) return;

		// Move props in opposite directions
		this.moveProp(redPropData, direction);
		this.moveProp(bluePropData, this.dirCalculator.getOppositeDirection(direction));
	}

	/**
	 * Moves a prop in the specified direction
	 * @param prop The prop to move
	 * @param direction The direction to move in
	 */
	private moveProp(prop: PropData, direction: Direction): void {
		// Use offset calculator to determine new position
		const newPosition = this.betaOffsetCalculator.calculateNewPositionWithOffset(
			prop.coords,
			direction
		);
		prop.coords = newPosition;
	}

	/**
	 * Checks if a motion is a shift motion (pro, anti, float)
	 * @param motion The motion to check
	 * @returns True if the motion is a shift motion
	 */
	private isShiftMotion(motion: MotionData): boolean {
		return [PRO, ANTI, FLOAT].includes(motion.motionType);
	}
}
