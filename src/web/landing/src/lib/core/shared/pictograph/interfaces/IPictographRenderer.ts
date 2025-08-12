/**
 * 🎨 SIMPLIFIED PICTOGRAPH RENDERING INTERFACES
 *
 * Simplified interfaces for pictograph rendering in the landing project.
 */

// ============================================================================
// CORE RENDERING INTERFACES
// ============================================================================

/**
 * Main pictograph renderer interface
 */
export interface IPictographRenderer {
  /**
   * Render a complete pictograph from data
   */
  renderPictograph(data: any): Promise<SVGElement>;

  /**
   * Set renderer visibility options
   */
  setVisibility(options: RendererVisibilityOptions): void;
}

/**
 * Pictograph orchestrator interface
 */
export interface IPictographOrchestrator {
  /**
   * Create a pictograph with default data
   */
  createPictograph(): any;
}

// ============================================================================
// DATA TYPES
// ============================================================================

export interface RendererVisibilityOptions {
  grid?: boolean;
  props?: boolean;
  arrows?: boolean;
  blueMotion?: boolean;
  redMotion?: boolean;
  elemental?: boolean;
  vtg?: boolean;
  tka?: boolean;
  positions?: boolean;
}