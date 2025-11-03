/**
 * Landing Page State Management
 *
 * Manages the full-screen landing modal overlay state.
 */

// ============================================================================
// CONSTANTS
// ============================================================================

const FIRST_VISIT_KEY = "tka-has-visited-studio";

// ============================================================================
// UI STATE
// ============================================================================

export const landingUIState = $state({
  isOpen: false,
  isAnimating: false,
  isAutoOpened: false, // Whether it was auto-opened on first visit
  isEnteringStudio: false, // Whether the entry animation is playing
});

// ============================================================================
// VISIT DETECTION
// ============================================================================

/**
 * Check if this is the user's first visit
 */
export function isFirstVisit(): boolean {
  if (typeof localStorage === "undefined") return false;
  return localStorage.getItem(FIRST_VISIT_KEY) !== "true";
}

/**
 * Mark the studio as visited (called when user enters for the first time)
 */
export function markStudioVisited() {
  if (typeof localStorage === "undefined") return;
  localStorage.setItem(FIRST_VISIT_KEY, "true");
}

/**
 * Reset visit status (for testing/debugging)
 */
export function resetVisitStatus() {
  if (typeof localStorage === "undefined") return;
  localStorage.removeItem(FIRST_VISIT_KEY);
}

// ============================================================================
// ACTIONS
// ============================================================================

/**
 * Open the landing modal with animation
 * @param autoOpened - Whether this was automatically opened (first visit)
 */
export function openLanding(autoOpened: boolean = false) {
  if (landingUIState.isOpen) return;

  landingUIState.isAnimating = true;
  landingUIState.isOpen = true;
  landingUIState.isAutoOpened = autoOpened;

  // Reset animation flag after transition
  setTimeout(() => {
    landingUIState.isAnimating = false;
  }, 400);
}

/**
 * Close the landing modal with animation
 * @param withStudioEntry - Whether to play the studio entry animation
 */
export function closeLanding(withStudioEntry: boolean = false) {
  if (!landingUIState.isOpen) return;

  landingUIState.isAnimating = true;

  // If this is a first-time studio entry, play the special animation
  if (withStudioEntry && landingUIState.isAutoOpened) {
    landingUIState.isEnteringStudio = true;
    markStudioVisited();

    // Extended timing for the entry animation
    setTimeout(() => {
      landingUIState.isOpen = false;
      landingUIState.isAnimating = false;
      landingUIState.isAutoOpened = false;

      // Keep entry animation visible a bit longer
      setTimeout(() => {
        landingUIState.isEnteringStudio = false;
      }, 1200);
    }, 800);
  } else {
    // Standard close animation
    setTimeout(() => {
      landingUIState.isOpen = false;
      landingUIState.isAnimating = false;
      landingUIState.isAutoOpened = false;
    }, 350);
  }
}

/**
 * Toggle landing modal (always manual toggle, never auto-opened)
 */
export function toggleLanding() {
  if (landingUIState.isOpen) {
    closeLanding(false);
  } else {
    openLanding(false);
  }
}
