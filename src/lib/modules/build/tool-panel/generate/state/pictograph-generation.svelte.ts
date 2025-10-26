/**
 * Movement Generation State - Svelte 5 runes
 *
 * Reactive state management for movement pattern generation.
 * Wraps movement generation services with runes for UI reactivity.
 * Follows TKA architecture: services handle business logic, runes handle reactivity.
 */

import { Letter, type PictographData, resolveSyncUnsafe } from "$shared";
import { TYPES } from "$shared/inversify/types";
import type { IPictographGenerator } from "../shared/services/contracts";

/**
 * Creates reactive state for pictograph generation
 */
export function createPictographGenerationState() {
  // Get services from DI container
  const pictographGenerator = resolveSyncUnsafe<IPictographGenerator>(
    TYPES.IPictographGenerator
  );

  // Core reactive state
  let isGenerating = $state(false);
  let pictographsByLetter = $state<Record<string, PictographData[]>>({});
  let selectedLetter = $state<string>("");
  let error = $state<string | null>(null);
  let lastGenerated = $state<string | null>(null);

  // Filter state
  let filterText = $state("");
  let showOnlyGenerated = $state(false);

  // Derived computed values
  const filteredLetters = $derived(() => {
    const letters = Object.keys(pictographsByLetter);

    if (showOnlyGenerated) {
      return letters.filter((letter) => pictographsByLetter[letter].length > 0);
    }

    if (filterText.trim()) {
      const filter = filterText.toLowerCase().trim();
      return letters.filter((letter) => letter.toLowerCase().includes(filter));
    }

    return letters;
  });

  const generationStats = $derived(() => ({
    totalLetters: Object.keys(pictographsByLetter).length,
    totalPictographs: Object.values(pictographsByLetter).reduce(
      (sum, pictographs) => sum + pictographs.length,
      0
    ),
    filteredCount: filteredLetters.length,
    isFiltered: filterText.trim() !== "" || showOnlyGenerated,
  }));

  const availableLetters = $derived(() => Object.values(Letter));

  // Actions
  async function generatePictographs(
    letter: string
  ): Promise<PictographData[] | null> {
    if (isGenerating) return null;

    isGenerating = true;
    error = null;

    try {
      const pictographs = pictographGenerator.getPictographsByLetter(letter);

      if (pictographs) {
        // Update the collection
        pictographsByLetter[letter] = pictographs;
        selectedLetter = letter;
        lastGenerated = letter;

        return pictographs;
      } else {
        error = `No generator found for letter: ${letter}`;
        return null;
      }
    } catch (err) {
      error = err instanceof Error ? err.message : "Unknown error occurred";
      return null;
    } finally {
      isGenerating = false;
    }
  }

  async function generateAllPictographs(): Promise<void> {
    if (isGenerating) return;

    isGenerating = true;
    error = null;

    try {
      const allPictographs = pictographGenerator.getAllPictographs();
      // Group pictographs by letter
      const grouped: Record<string, PictographData[]> = {};
      for (const pictograph of allPictographs) {
        const letter = pictograph.letter?.toString() || "unknown";
        if (!grouped[letter]) {
          grouped[letter] = [];
        }
        grouped[letter].push(pictograph);
      }
      pictographsByLetter = grouped;
      lastGenerated = "all";
    } catch (err) {
      error =
        err instanceof Error
          ? err.message
          : "Failed to generate all pictographs";
    } finally {
      isGenerating = false;
    }
  }

  function clearPictographs(): void {
    pictographsByLetter = {};
    selectedLetter = "";
    error = null;
    lastGenerated = null;
  }

  function selectLetter(letter: string): void {
    selectedLetter = letter;
  }

  function setFilter(text: string): void {
    filterText = text;
  }

  function toggleShowOnlyGenerated(): void {
    showOnlyGenerated = !showOnlyGenerated;
  }

  function clearError(): void {
    error = null;
  }

  function getPictographsByLetter(
    letter: string
  ): PictographData[] | undefined {
    return pictographsByLetter[letter];
  }

  function hasPictographs(letter: string): boolean {
    return (
      letter in pictographsByLetter && pictographsByLetter[letter].length > 0
    );
  }

  // Export reactive state and actions
  return {
    // State
    get isGenerating() {
      return isGenerating;
    },
    get pictographsByLetter() {
      return pictographsByLetter;
    },
    get selectedLetter() {
      return selectedLetter;
    },
    get error() {
      return error;
    },
    get lastGenerated() {
      return lastGenerated;
    },
    get filterText() {
      return filterText;
    },
    get showOnlyGenerated() {
      return showOnlyGenerated;
    },

    // Derived state
    get filteredLetters() {
      return filteredLetters;
    },
    get generationStats() {
      return generationStats;
    },
    get availableLetters() {
      return availableLetters;
    },

    // Actions
    generatePictographs,
    generateAllPictographs,
    clearPictographs,
    selectLetter,
    setFilter,
    toggleShowOnlyGenerated,
    clearError,
    getPictographsByLetter,
    hasPictographs,
  };
}

export type PictographGenerationState = ReturnType<
  typeof createPictographGenerationState
>;
