/**
 * SVG Config - Shared Constants
 *
 * Shared configuration values for SVG rendering services.
 * Extracted from PictographRenderingService for reusability.
 */

import type { ISvgConfig } from "$shared";
import { injectable } from "inversify";

@injectable()
export class SvgConfig implements ISvgConfig {
  readonly SVG_SIZE = 950;
  readonly CENTER_X = 475;
  readonly CENTER_Y = 475;
}
