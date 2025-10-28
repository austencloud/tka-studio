/**
 * Build Tab Responsive Layout Service Contract
 *
 * Manages responsive layout decisions specifically for BuildTab's two-panel interface:
 * - Workspace Panel + Tool Panel arrangement (side-by-side vs stacked)
 * - Viewport tracking and dimensions for BuildTab context
 * - Device type detection for construction interface optimization
 * - Navigation bar positioning relative to BuildTab panels
 *
 * Domain: Build Module - Sequence Construction Interface
 * Extracted from BuildTab.svelte monolith to follow DI architecture.
 */

export interface IBuildTabResponsiveLayoutService {
  /**
   * Initialize the service and start tracking viewport changes
   */
  initialize(): void;

  /**
   * Clean up subscriptions and observers
   */
  dispose(): void;

  /**
   * Get current viewport width
   */
  getViewportWidth(): number;

  /**
   * Get current viewport height
   */
  getViewportHeight(): number;

  /**
   * Get current navigation layout (top or left)
   */
  getNavigationLayout(): 'top' | 'left';

  /**
   * Determine if BuildTab panels should use side-by-side layout
   * (Workspace left, Tool Panel right) vs stacked layout (Workspace top, Tool Panel bottom)
   * Based on device type, orientation, and viewport size
   */
  shouldUseSideBySideLayout(): boolean;

  /**
   * Check if device is desktop
   */
  isDesktop(): boolean;

  /**
   * Check if device is landscape mobile
   */
  isLandscapeMobile(): boolean;

  /**
   * Check if viewport is wide enough for side-by-side layout
   */
  hasWideViewport(): boolean;

  /**
   * Subscribe to layout changes
   * @param callback Called when layout configuration changes
   * @returns Unsubscribe function
   */
  onLayoutChange(callback: () => void): () => void;

  /**
   * Get aspect ratio of current viewport
   */
  getAspectRatio(): number;

  /**
   * Detect if device is likely a Z Fold in unfolded state
   */
  isLikelyZFoldUnfolded(): boolean;
}
