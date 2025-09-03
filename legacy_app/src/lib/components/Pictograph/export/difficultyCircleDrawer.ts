/**
 * Difficulty Circle Drawer
 *
 * This module provides functionality to draw a circular difficulty indicator
 * similar to the Python implementation.
 */

/**
 * Gradient stop definition
 */
interface GradientStop {
	position: number;
	color: string;
}

/**
 * Gradient definitions for different difficulty levels
 */
const DIFFICULTY_GRADIENTS: Record<number, GradientStop[]> = {
	1: [
		{ position: 0, color: '#F5F5F5' } // Light gray/white
	],
	2: [
		{ position: 0, color: '#AAAAAA' },
		{ position: 0.15, color: '#D2D2D2' },
		{ position: 0.3, color: '#787878' },
		{ position: 0.4, color: '#B4B4B4' },
		{ position: 0.55, color: '#BEBEBE' },
		{ position: 0.75, color: '#828282' },
		{ position: 1, color: '#6E6E6E' }
	],
	3: [
		{ position: 0, color: '#FFD700' }, // Gold
		{ position: 0.2, color: '#EEC900' }, // Goldenrod
		{ position: 0.4, color: '#DAA520' }, // Goldenrod darker
		{ position: 0.6, color: '#B8860B' }, // Dark goldenrod
		{ position: 0.8, color: '#8B4513' }, // Saddle brown
		{ position: 1, color: '#556B2F' } // Dark olive green
	],
	4: [
		{ position: 0, color: '#C8A2C8' },
		{ position: 0.3, color: '#AA84AA' },
		{ position: 0.6, color: '#9400D3' },
		{ position: 1, color: '#640096' }
	],
	5: [
		{ position: 0, color: '#FF4500' },
		{ position: 0.4, color: '#FF0000' },
		{ position: 0.8, color: '#8B0000' },
		{ position: 1, color: '#640000' }
	]
};

/**
 * Creates a gradient for the specified difficulty level
 *
 * @param ctx The canvas rendering context
 * @param x The x position of the circle center
 * @param y The y position of the circle center
 * @param radius The radius of the circle
 * @param difficultyLevel The difficulty level (1-5)
 * @returns The gradient object
 */
function createDifficultyGradient(
	ctx: CanvasRenderingContext2D,
	x: number,
	y: number,
	radius: number,
	difficultyLevel: number
): CanvasGradient {
	// Validate difficulty level
	const level = Math.max(1, Math.min(5, Math.round(difficultyLevel || 1)));

	// Create a linear gradient from top-left to bottom-right
	const gradient = ctx.createLinearGradient(x - radius, y - radius, x + radius, y + radius);

	// Get gradient stops for this difficulty level
	const stops = DIFFICULTY_GRADIENTS[level] || DIFFICULTY_GRADIENTS[1];

	// Add color stops to the gradient
	for (const stop of stops) {
		gradient.addColorStop(stop.position, stop.color);
	}

	return gradient;
}

/**
 * Draws a circular difficulty indicator
 *
 * @param ctx The canvas rendering context
 * @param difficultyLevel The difficulty level (1-5)
 * @param x The x position for the circle center
 * @param y The y position for the circle center
 * @param radius The radius of the circle
 */
export function drawDifficultyCircle(
	ctx: CanvasRenderingContext2D,
	difficultyLevel: number,
	x: number = 60,
	y: number = 60,
	radius: number = 40
): void {
	const level = Math.max(1, Math.min(5, Math.round(difficultyLevel || 1)));

	// Save context for restoration
	ctx.save();

	// Draw the circle
	ctx.beginPath();
	ctx.arc(x, y, radius, 0, Math.PI * 2);

	// Apply gradient fill
	const gradient = createDifficultyGradient(ctx, x, y, radius, level);
	ctx.fillStyle = gradient;
	ctx.fill();

	// Draw border with proportional line width
	ctx.strokeStyle = 'black';
	ctx.lineWidth = Math.max(1, Math.round(radius * 0.05)); // Scale line width with radius
	ctx.stroke();

	// Calculate font size proportional to the circle size
	// Use 60% of the radius for the font size to ensure it fits well
	const fontSize = Math.round(radius * 1.2); // Reduced from 1.5 to fit better
	ctx.font = `bold ${fontSize}px Georgia`;

	// Set text color based on difficulty level
	ctx.fillStyle = level >= 4 ? 'white' : 'black';
	ctx.textAlign = 'center';
	ctx.textBaseline = 'middle';

	// Add shadow for better contrast on darker backgrounds
	if (level >= 4) {
		ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
		ctx.shadowBlur = 2;
		ctx.shadowOffsetX = 1;
		ctx.shadowOffsetY = 1;
	}

	// Apply vertical offset for specific difficulty levels
	const textY = level === 3 ? y - radius * 0.1 : y; // Reduced offset from 0.15 to 0.1

	// Draw the text
	ctx.fillText(level.toString(), x, textY);

	// Log circle details for debugging
	console.log('DifficultyCircleDrawer: Circle rendered', {
		level,
		x,
		y,
		radius,
		fontSize,
		lineWidth: ctx.lineWidth
	});
	ctx.restore();
}
