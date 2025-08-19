/**
 * SVG Configuration - Shared Constants
 *
 * Shared configuration values for SVG rendering services.
 * Extracted from PictographRenderingService for reusability.
 */

export interface ISvgConfiguration {
  readonly SVG_SIZE: number;
  readonly CENTER_X: number;
  readonly CENTER_Y: number;
}

export class SvgConfiguration implements ISvgConfiguration {
  readonly SVG_SIZE = 950;
  readonly CENTER_X = 475;
  readonly CENTER_Y = 475;
}
