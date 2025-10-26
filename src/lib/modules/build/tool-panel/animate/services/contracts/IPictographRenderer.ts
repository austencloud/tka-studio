/**
 * Pictograph and Rendering Service Interfaces
 *
 * Interfaces for pictograph rendering, SVG generation, and visual representation
 * of sequences and beats.
 */
// ============================================================================
// SHARED TYPES (imported from core-types to avoid duplication)
// ============================================================================

import type { PictographData } from "../../../../../shared";


// ============================================================================
// SERVICE CONTRACTS (Behavioral Interfaces)
// ============================================================================

export interface IPictographRenderer {
  renderPictograph(data: PictographData): Promise<SVGElement>;
}
