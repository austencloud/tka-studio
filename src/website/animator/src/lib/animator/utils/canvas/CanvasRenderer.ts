import type { PropState } from '../../types/core.js';
import { ANIMATION_CONSTANTS } from '../../constants/animation.js';

/**
 * Utility class for canvas rendering operations
 */
export class CanvasRenderer {
	/**
	 * Clear the entire canvas
	 */
	static clearCanvas(ctx: CanvasRenderingContext2D, width: number, height: number): void {
		ctx.clearRect(0, 0, width, height);
	}

	/**
	 * Draw the grid image on the canvas
	 */
	static drawGrid(
		ctx: CanvasRenderingContext2D,
		gridImage: HTMLImageElement,
		width: number,
		height: number
	): void {
		ctx.drawImage(gridImage, 0, 0, width, height);
	}

	/**
	 * Draw a prop (staff) on the canvas
	 */
	static drawProp(
		ctx: CanvasRenderingContext2D,
		image: HTMLImageElement,
		prop: PropState,
		canvasWidth: number
	): void {
		ctx.save();

		const gridScaleFactor = canvasWidth / ANIMATION_CONSTANTS.GRID_VIEWBOX_SIZE;

		// Use coordinates directly from the simplified engine
		const canvasX = prop.x * gridScaleFactor;
		const canvasY = prop.y * gridScaleFactor;

		ctx.translate(canvasX, canvasY);
		ctx.rotate(prop.staffRotationAngle);

		const staffWidth = ANIMATION_CONSTANTS.STAFF_VIEWBOX_WIDTH * gridScaleFactor;
		const staffHeight = ANIMATION_CONSTANTS.STAFF_VIEWBOX_HEIGHT * gridScaleFactor;
		const centerOffsetX = ANIMATION_CONSTANTS.STAFF_CENTER_X * gridScaleFactor;
		const centerOffsetY = ANIMATION_CONSTANTS.STAFF_CENTER_Y * gridScaleFactor;

		ctx.drawImage(image, -centerOffsetX, -centerOffsetY, staffWidth, staffHeight);
		ctx.restore();
	}

	/**
	 * Render the complete canvas scene
	 */
	static renderScene(
		ctx: CanvasRenderingContext2D,
		width: number,
		height: number,
		gridVisible: boolean,
		gridImage: HTMLImageElement | null,
		blueStaffImage: HTMLImageElement | null,
		redStaffImage: HTMLImageElement | null,
		blueProp: PropState,
		redProp: PropState
	): void {
		// Clear canvas
		this.clearCanvas(ctx, width, height);

		// Draw grid if visible and available
		if (gridVisible && gridImage) {
			this.drawGrid(ctx, gridImage, width, height);
		}

		// Draw blue staff if available
		if (blueStaffImage) {
			this.drawProp(ctx, blueStaffImage, blueProp, width);
		}

		// Draw red staff if available
		if (redStaffImage) {
			this.drawProp(ctx, redStaffImage, redProp, width);
		}
	}
}
