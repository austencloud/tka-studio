/**
 * turn-control-expansion-state.svelte.ts
 * State management for turn control expansion/collapse behavior
 *
 * Manages:
 * - Which side (left/right) is currently expanded
 * - Persistence of last expanded side across beat changes
 * - Expansion state transitions
 */

export type ExpandedSide = 'blue' | 'red' | null;

export function createTurnControlExpansionState() {
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
    expand: (side: 'blue' | 'red') => {
      expandedSide = side;
      lastExpandedSide = side;
      console.log(`Turn control expanded: ${side}`);
    },

    collapse: () => {
      console.log(`Turn control collapsed from: ${expandedSide}`);
      expandedSide = null;
      // Note: lastExpandedSide is preserved for persistence
    },

    toggle: (side: 'blue' | 'red') => {
      if (expandedSide === side) {
        expandedSide = null;
        console.log(`Turn control toggled off: ${side}`);
      } else {
        expandedSide = side;
        lastExpandedSide = side;
        console.log(`Turn control toggled on: ${side}`);
      }
    },

    // When switching beats, restore the last expanded side if it exists
    restoreLastExpanded: () => {
      if (lastExpandedSide) {
        expandedSide = lastExpandedSide;
        console.log(`Turn control restored last expanded: ${lastExpandedSide}`);
      }
    },

    // Check if a specific side is expanded
    isBlueExpanded: () => expandedSide === 'blue',
    isRedExpanded: () => expandedSide === 'red',
  };
}

export type TurnControlExpansionState = ReturnType<typeof createTurnControlExpansionState>;
