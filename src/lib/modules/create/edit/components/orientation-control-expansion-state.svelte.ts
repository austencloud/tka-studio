/**
 * orientation-control-expansion-state.svelte.ts
 * State management for orientation control expansion/collapse behavior
 *
 * Manages:
 * - Which side (left/right) is currently expanded
 * - Persistence of last expanded side across beat changes
 * - Expansion state transitions
 */

export type ExpandedSide = "blue" | "red" | null;

export function createOrientationControlExpansionState() {
  // Current expanded side
  let expandedSide = $state<ExpandedSide>(null);

  // Last expanded side for persistence across beat changes
  let lastExpandedSide = $state<ExpandedSide>(null);

  return {
    // Getters
    get expandedSide() {
      return expandedSide;
    },
    get lastExpandedSide() {
      return lastExpandedSide;
    },
    get isExpanded() {
      return expandedSide !== null;
    },

    // Actions
    expand: (side: "blue" | "red") => {
      expandedSide = side;
      lastExpandedSide = side;
    },

    collapse: () => {
      expandedSide = null;
      // Note: lastExpandedSide is preserved for persistence
    },

    toggle: (side: "blue" | "red") => {
      if (expandedSide === side) {
        expandedSide = null;
      } else {
        expandedSide = side;
        lastExpandedSide = side;
      }
    },

    // When switching beats, restore the last expanded side if it exists
    restoreLastExpanded: () => {
      if (lastExpandedSide) {
        expandedSide = lastExpandedSide;
      }
    },

    // Check if a specific side is expanded
    isBlueExpanded: () => expandedSide === "blue",
    isRedExpanded: () => expandedSide === "red",
  };
}

export type OrientationControlExpansionState = ReturnType<
  typeof createOrientationControlExpansionState
>;
