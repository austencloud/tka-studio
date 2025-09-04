/**
 * Codex State Management with Svelte 5 Runes
 *
 * Handles reactive state for the codex component including
 * search, pictograph data, operations, and orientation using the CodexService.
 * Matches desktop functionality with row organization and control operations.
 */

import type { PictographData } from "$shared/domain";
import { TYPES } from "$shared/inversify/types";

// CRITICAL: Import container to ensure it loads
import type { ICodexService } from "$services";
import { container } from "$shared/inversify/container";

// Container is now loaded successfully - debug messages removed

// TEMPORARY: Import minimal container for testing - REMOVED TO TEST MODULE EXECUTION
// import { resolve } from "$lib/services/inversify/container";

export function createCodexState() {
  console.log("🔧 createCodexState() called - creating new state instance");

  // Using direct container import instead of context

  function getCodexService(): ICodexService {
    console.log("🔧 getCodexService() called - using direct container import");

    // Use the directly imported container instead of context
    return container.get<ICodexService>(TYPES.ICodexService);
  }

  // Core reactive state using Svelte 5 runes
  let searchTerm = $state<string>("");
  let isLoading = $state<boolean>(false);
  let pictographs = $state<PictographData[]>([]);
  let pictographsByLetter = $state<Record<string, PictographData | null>>({});
  let currentOrientation = $state<string>("Diamond");
  let error = $state<string | null>(null);
  let isProcessingOperation = $state<boolean>(false);

  // Get letter rows from service - initialized as empty and loaded when needed
  let letterRows = $state<string[][]>([]);
  let isInitialized = $state<boolean>(false);

  // Derived reactive values
  const filteredPictographs = $derived(
    !searchTerm
      ? pictographs
      : pictographs.filter((pictograph) => {
          const term = searchTerm.toLowerCase();
          const letter = pictograph.letter?.toLowerCase() || "";
          const id = pictograph.id?.toLowerCase() || "";

          return (
            letter.includes(term) ||
            id.includes(term) ||
            letter.startsWith(term)
          );
        })
  );

  // Filtered pictographs by letter for row display
  const filteredPictographsByLetter = $derived(() => {
    if (!searchTerm) return pictographsByLetter;

    const result: Record<string, PictographData | null> = {};
    const term = searchTerm.toLowerCase();

    Object.entries(pictographsByLetter).forEach(([letter, pictograph]) => {
      if (pictograph && letter.toLowerCase().includes(term)) {
        result[letter] = pictograph;
      }
    });

    return result;
  });

  // Load all pictographs and organize by letter
  async function loadAllPictographs() {
    console.log(
      "🔄 loadAllPictographs() called, isLoading:",
      isLoading,
      "isInitialized:",
      isInitialized
    );

    if (isLoading) {
      console.log("⚠️ loadAllPictographs: Already loading, skipping");
      return; // Prevent multiple simultaneous loads
    }

    isLoading = true;
    error = null;

    try {
      const codexService = getCodexService();
      console.log("🔍 Loading all codex pictographs...");

      // Load pictographs from service
      const allPictographs = await codexService.loadAllPictographs();
      pictographs = allPictographs;

      // Also load organized by letter
      pictographsByLetter = await codexService.getAllPictographData();

      // Load letter rows if not already loaded
      if (letterRows.length === 0) {
        letterRows = await codexService.getLettersByRow();
      }

      isInitialized = true;
      console.log("✅ Codex data loaded successfully");
    } catch (err) {
      console.error("Failed to load pictographs:", err);
      error = "Failed to load pictographs. Please try again.";
      pictographs = [];
      pictographsByLetter = {};
    } finally {
      isLoading = false;
    }
  }

  // Operation methods
  async function performRotateOperation() {
    if (isProcessingOperation) return;

    isProcessingOperation = true;
    try {
      const codexService = getCodexService();
      console.log("🔄 Performing rotate operation...");
      const rotatedPictographs =
        await codexService.rotateAllPictographs(pictographs);
      pictographs = rotatedPictographs;

      // Refresh the organized data
      pictographsByLetter = await codexService.getAllPictographData();
    } catch (err) {
      console.error("Failed to rotate pictographs:", err);
      error = "Failed to rotate pictographs. Please try again.";
    } finally {
      isProcessingOperation = false;
    }
  }

  async function performMirrorOperation() {
    if (isProcessingOperation) return;

    isProcessingOperation = true;
    try {
      const codexService = getCodexService();
      console.log("🪞 Performing mirror operation...");
      const mirroredPictographs =
        await codexService.mirrorAllPictographs(pictographs);
      pictographs = mirroredPictographs;

      // Refresh the organized data
      pictographsByLetter = await codexService.getAllPictographData();
    } catch (err) {
      console.error("Failed to mirror pictographs:", err);
      error = "Failed to mirror pictographs. Please try again.";
    } finally {
      isProcessingOperation = false;
    }
  }

  async function performColorSwapOperation() {
    if (isProcessingOperation) return;

    isProcessingOperation = true;
    try {
      const codexService = getCodexService();
      console.log("⚫⚪ Performing color swap operation...");
      const swappedPictographs =
        await codexService.colorSwapAllPictographs(pictographs);
      pictographs = swappedPictographs;

      // Refresh the organized data
      pictographsByLetter = await codexService.getAllPictographData();
    } catch (err) {
      console.error("Failed to swap colors:", err);
      error = "Failed to swap colors. Please try again.";
    } finally {
      isProcessingOperation = false;
    }
  }

  // Public interface
  return {
    // Reactive getters
    get searchTerm() {
      return searchTerm;
    },
    get isLoading() {
      return isLoading;
    },
    get isInitialized() {
      return isInitialized;
    },
    get pictographs() {
      return pictographs;
    },
    get filteredPictographs() {
      return filteredPictographs;
    },
    get pictographsByLetter() {
      return pictographsByLetter;
    },
    get filteredPictographsByLetter() {
      return filteredPictographsByLetter;
    },
    get letterRows() {
      return letterRows;
    },
    get currentOrientation() {
      return currentOrientation;
    },
    get error() {
      return error;
    },
    get isProcessingOperation() {
      return isProcessingOperation;
    },

    // Methods
    setSearchTerm(term: string) {
      searchTerm = term;
    },

    setOrientation(orientation: string) {
      currentOrientation = orientation;
      console.log("🔄 Orientation changed to:", orientation);
    },

    async refreshPictographs() {
      await loadAllPictographs();
    },

    async searchPictographs(term: string) {
      searchTerm = term;
      // The derived value will automatically update the filtered list
    },

    async getPictographByLetter(letter: string) {
      const codexService = getCodexService();
      return await codexService.getPictographByLetter(letter);
    },

    // Operation methods
    async rotatePictographs() {
      await performRotateOperation();
    },

    async mirrorPictographs() {
      await performMirrorOperation();
    },

    async colorSwapPictographs() {
      await performColorSwapOperation();
    },
  };
}
