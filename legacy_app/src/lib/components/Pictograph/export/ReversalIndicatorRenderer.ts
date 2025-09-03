/**
 * Reversal Indicator Renderer
 *
 * This module provides functionality to render reversal indicators on the canvas.
 */

import type { Beat } from '$lib/types/Beat';

/**
 * Draws reversal indicators for a beat
 *
 * @param ctx The canvas rendering context
 * @param beat The beat to draw reversal indicators for
 * @param x The x position of the beat
 * @param y The y position of the beat
 * @param beatSize The size of the beat
 */
export function drawReversalIndicators(
  ctx: CanvasRenderingContext2D,
  beat: Beat,
  x: number,
  y: number,
  beatSize: number
): void {
  // Check if the beat has reversal indicators
  if (beat && (beat.metadata?.blueReversal || beat.metadata?.redReversal)) {
    console.log(`EnhancedExporter: Beat has reversal indicators`, {
      blueReversal: beat.metadata?.blueReversal,
      redReversal: beat.metadata?.redReversal
    });

    // Draw reversal indicators
    const indicatorSize = beatSize * 0.1; // 10% of beat size
    const indicatorY = y + beatSize - indicatorSize * 1.5; // Position at bottom of beat
    const indicatorSpacing = indicatorSize * 0.5;

    // Calculate center position for the indicators
    const centerX = x + beatSize / 2;
    let currentX = centerX;

    // If both indicators are present, adjust starting position
    if (beat.metadata?.blueReversal && beat.metadata?.redReversal) {
      currentX = centerX - indicatorSize / 2 - indicatorSpacing / 2;
    }

    // Draw blue reversal indicator
    if (beat.metadata?.blueReversal) {
      ctx.fillStyle = 'blue';
      ctx.beginPath();
      ctx.arc(currentX, indicatorY, indicatorSize / 2, 0, Math.PI * 2);
      ctx.fill();

      // Move to next position if needed
      if (beat.metadata?.redReversal) {
        currentX += indicatorSize + indicatorSpacing;
      }
    }

    // Draw red reversal indicator
    if (beat.metadata?.redReversal) {
      ctx.fillStyle = 'red';
      ctx.beginPath();
      ctx.arc(currentX, indicatorY, indicatorSize / 2, 0, Math.PI * 2);
      ctx.fill();
    }
  }
}
