/**
 * SVG Configuration - Shared Constants
 *
 * Shared configuration values for SVG rendering services.
 * Extracted from PictographRenderingService for reusability.
 */

import type { ISvgConfiguration } from "$contracts";
import { injectable } from "inversify";

@injectable()
export class SvgConfiguration implements ISvgConfiguration {
  readonly SVG_SIZE = 950;
  readonly CENTER_X = 475;
  readonly CENTER_Y = 475;
}
