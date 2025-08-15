/**
 * EXAMPLE: Proper Sequence State Factory (Svelte 5 + Clean Architecture)
 *
 * This demonstrates the CORRECT way to implement reactive state management
 * that follows the established architectural principles:
 *
 * ✅ Component-scoped state (not global singletons)
 * ✅ Pure reactive wrappers around service calls
 * ✅ Services injected via DI container
 * ✅ No business logic in state layer
 * ✅ Testable and maintainable
 *
 * REPLACE PATTERN: Global singleton state files
 * MIGRATION TARGET: src/lib/state/sequenceState.svelte.ts
 */

import type { BeatData, SequenceData } from "$lib/domain";
import type { ISequenceService } from "$services/interfaces";

/**
 * Creates component-scoped sequence state
 *
 * @param sequenceService - Injected via DI container
 * @returns Reactive state object with getters and actions
 */
export function createSequenceState(sequenceService: ISequenceService) {
  // ============================================================================
  // REACTIVE STATE (Component-scoped)
  // ============================================================================

  let sequences = $state<SequenceData[]>([]);
  let currentSequence = $state<SequenceData | null>(null);
  let selectedBeatIndex = $state<number | null>(null);
  let isLoading = $state(false);
  let error = $state<string | null>(null);

  // ============================================================================
  // DERIVED STATE (Pure reactive calculations)
  // ============================================================================

  let selectedBeat = $derived(() => {
    if (!currentSequence || selectedBeatIndex === null) return null;
    return currentSequence.beats[selectedBeatIndex] ?? null;
  });

  let hasSequence = $derived(() => currentSequence !== null);
  let beatCount = $derived(() => currentSequence?.beats.length ?? 0);
  let hasError = $derived(() => error !== null);

  // ============================================================================
  // ACTIONS (Pure reactive wrappers around service calls)
  // ============================================================================

  async function loadSequences() {
    isLoading = true;
    error = null;

    try {
      // Service call - business logic stays in service layer
      sequences = await sequenceService.getAllSequences();
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load sequences";
      console.error("Failed to load sequences:", err);
    } finally {
      isLoading = false;
    }
  }

  async function selectSequence(id: string) {
    isLoading = true;
    error = null;
    selectedBeatIndex = null; // Reset selection

    try {
      // Service call - no business logic here
      currentSequence = await sequenceService.getSequence(id);
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to load sequence";
      console.error("Failed to select sequence:", err);
    } finally {
      isLoading = false;
    }
  }

  async function updateBeat(beatIndex: number, beatData: BeatData) {
    if (!currentSequence) return;

    isLoading = true;
    error = null;

    try {
      // Service call handles all business logic
      await sequenceService.updateBeat(currentSequence.id, beatIndex, beatData);

      // Update local state after successful service call
      const newBeats = [...currentSequence.beats];
      newBeats[beatIndex] = beatData;
      currentSequence = { ...currentSequence, beats: newBeats };
    } catch (err) {
      error = err instanceof Error ? err.message : "Failed to update beat";
      console.error("Failed to update beat:", err);
    } finally {
      isLoading = false;
    }
  }

  function selectBeat(index: number | null) {
    selectedBeatIndex = index;
  }

  function clearError() {
    error = null;
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  return {
    // Readonly state access
    get sequences() {
      return sequences;
    },
    get currentSequence() {
      return currentSequence;
    },
    get selectedBeat() {
      return selectedBeat;
    },
    get selectedBeatIndex() {
      return selectedBeatIndex;
    },
    get isLoading() {
      return isLoading;
    },
    get error() {
      return error;
    },
    get hasSequence() {
      return hasSequence;
    },
    get beatCount() {
      return beatCount;
    },
    get hasError() {
      return hasError;
    },

    // Actions
    loadSequences,
    selectSequence,
    updateBeat,
    selectBeat,
    clearError,
  };
}

/**
 * USAGE EXAMPLE in component:
 *
 * ```svelte
 * <script lang="ts">
 *   import { resolve } from '$services/bootstrap';
 *   import { createSequenceState } from '$lib/examples/state/sequence-state-factory.svelte';
 *
 *   // Get service from DI container
 *   const sequenceService = resolve('ISequenceService');
 *
 *   // Create component-scoped state
 *   const sequenceState = createSequenceState(sequenceService);
 *
 *   // Use reactive state
 *   $effect(() => {
 *     sequenceState.loadSequences();
 *   });
 * </script>
 *
 * <div>
 *   {#if sequenceState.isLoading}
 *     Loading...
 *   {:else if sequenceState.hasError}
 *     Error: {sequenceState.error}
 *   {:else}
 *     Found {sequenceState.beatCount} beats
 *   {/if}
 * </div>
 * ```
 */

export type SequenceState = ReturnType<typeof createSequenceState>;
