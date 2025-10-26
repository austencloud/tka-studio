/**
 * Animation Panel State
 *
 * Manages animation panel visibility and collapse state.
 * Extracted from RightPanel.svelte for better separation of concerns.
 *
 * ✅ Pure Svelte 5 state management
 * ✅ No business logic, just UI state
 * ✅ Haptic feedback integration
 */

import type { IHapticFeedbackService } from "$shared";

/**
 * Creates animation panel state for managing panel visibility and collapse
 *
 * @param hapticService - Optional haptic feedback service for tactile responses
 * @returns Reactive state object for animation panel
 */
export function createAnimationPanelState(hapticService?: IHapticFeedbackService) {
  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  let isAnimationVisible = $state(true);
  let isAnimationCollapsed = $state(false);

  // ============================================================================
  // STATE MUTATIONS
  // ============================================================================

  function toggleAnimationCollapse() {
    // Trigger haptic feedback for user interaction
    hapticService?.trigger("navigation");

    isAnimationCollapsed = !isAnimationCollapsed;
  }

  function setAnimationVisible(visible: boolean) {
    isAnimationVisible = visible;
  }

  function setAnimationCollapsed(collapsed: boolean) {
    isAnimationCollapsed = collapsed;
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  return {
    // Readonly state access
    get isAnimationVisible() {
      return isAnimationVisible;
    },
    get isAnimationCollapsed() {
      return isAnimationCollapsed;
    },

    // State mutations
    toggleAnimationCollapse,
    setAnimationVisible,
    setAnimationCollapsed,
  };
}
