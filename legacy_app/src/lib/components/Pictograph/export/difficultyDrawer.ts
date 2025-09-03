/**
 * Difficulty Drawer
 *
 * This module provides functionality to draw a difficulty label on the exported image.
 */

/**
 * Draws a difficulty label in the top-left corner of the canvas
 *
 * @param ctx The canvas rendering context
 * @param difficultyLevel The difficulty level (1-5)
 * @param x The x position for the label
 * @param y The y position for the label
 */
export function drawDifficultyLabel(
  ctx: CanvasRenderingContext2D,
  difficultyLevel: number,
  x: number = 20,
  y: number = 20
): void {
  // Validate difficulty level
  const level = Math.max(1, Math.min(5, Math.round(difficultyLevel || 1)));

  // Save context for restoration
  ctx.save();

  // Draw background
  const width = 100;
  const height = 30;
  const radius = 5;

  // Draw rounded rectangle
  ctx.beginPath();
  ctx.moveTo(x + radius, y);
  ctx.lineTo(x + width - radius, y);
  ctx.quadraticCurveTo(x + width, y, x + width, y + radius);
  ctx.lineTo(x + width, y + height - radius);
  ctx.quadraticCurveTo(x + width, y + height, x + width - radius, y + height);
  ctx.lineTo(x + radius, y + height);
  ctx.quadraticCurveTo(x, y + height, x, y + height - radius);
  ctx.lineTo(x, y + radius);
  ctx.quadraticCurveTo(x, y, x + radius, y);
  ctx.closePath();

  // Fill with gradient based on difficulty
  const gradient = ctx.createLinearGradient(x, y, x + width, y + height);

  // Set gradient colors based on difficulty
  switch (level) {
    case 1:
      gradient.addColorStop(0, 'rgba(0, 150, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(0, 200, 0, 0.8)');
      break;
    case 2:
      gradient.addColorStop(0, 'rgba(100, 150, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(150, 200, 0, 0.8)');
      break;
    case 3:
      gradient.addColorStop(0, 'rgba(200, 150, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(250, 200, 0, 0.8)');
      break;
    case 4:
      gradient.addColorStop(0, 'rgba(200, 100, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(250, 150, 0, 0.8)');
      break;
    case 5:
      gradient.addColorStop(0, 'rgba(200, 0, 0, 0.8)');
      gradient.addColorStop(1, 'rgba(250, 50, 0, 0.8)');
      break;
    default:
      gradient.addColorStop(0, 'rgba(100, 100, 100, 0.8)');
      gradient.addColorStop(1, 'rgba(150, 150, 150, 0.8)');
  }

  ctx.fillStyle = gradient;
  ctx.fill();

  // Add subtle border
  ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
  ctx.lineWidth = 1;
  ctx.stroke();

  // Draw text
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 14px Arial';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(`Level ${level}`, x + width / 2, y + height / 2);

  // Add shadow for better readability
  ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
  ctx.shadowBlur = 2;
  ctx.shadowOffsetX = 1;
  ctx.shadowOffsetY = 1;

  // Restore context
  ctx.restore();
}
