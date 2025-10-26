/**
 * Record Tab State
 *
 * Manages state for the Record tab including playback, beat progression, and metronome.
 * Follows TKA patterns: factory function returning state with getters/setters.
 */

import type { SequenceData } from "$shared";

/**
 * Creates record tab state for practice and recording functionality
 */
export function createRecordTabState(sequenceData: SequenceData | null = null) {
  // ============================================================================
  // REACTIVE STATE
  // ============================================================================

  let isPlaying = $state(false);
  let currentBeatIndex = $state(0);
  let bpm = $state(60);
  let isMetronomeEnabled = $state(true);
  let sequence = $state<SequenceData | null>(sequenceData);
  let totalBeats = $derived(sequence?.beats?.length || 0);
  let hasSequence = $derived(sequence !== null && totalBeats > 0);
  let isAtEnd = $derived(currentBeatIndex >= totalBeats - 1);

  // ============================================================================
  // STATE MUTATIONS
  // ============================================================================

  function play() {
    if (!hasSequence) {
      console.warn("Cannot play: no sequence loaded");
      return;
    }
    isPlaying = true;
  }

  function pause() {
    isPlaying = false;
  }

  function togglePlayPause() {
    if (isPlaying) {
      pause();
    } else {
      play();
    }
  }

  function reset() {
    currentBeatIndex = 0;
    isPlaying = false;
  }

  function nextBeat() {
    if (currentBeatIndex < totalBeats - 1) {
      currentBeatIndex++;
    } else {
      // Loop back to start or stop
      currentBeatIndex = 0;
      isPlaying = false; // Stop at end for now
    }
  }

  function setBpm(newBpm: number) {
    bpm = Math.max(30, Math.min(180, newBpm));
  }

  function setMetronomeEnabled(enabled: boolean) {
    isMetronomeEnabled = enabled;
  }

  function setSequence(newSequence: SequenceData | null) {
    sequence = newSequence;
    reset(); // Reset playback when sequence changes
  }

  function setCurrentBeatIndex(index: number) {
    if (index >= 0 && index < totalBeats) {
      currentBeatIndex = index;
    }
  }

  // ============================================================================
  // PUBLIC API
  // ============================================================================

  return {
    // Readonly state
    get isPlaying() {
      return isPlaying;
    },
    get currentBeatIndex() {
      return currentBeatIndex;
    },
    get bpm() {
      return bpm;
    },
    get isMetronomeEnabled() {
      return isMetronomeEnabled;
    },
    get sequence() {
      return sequence;
    },
    get totalBeats() {
      return totalBeats;
    },
    get hasSequence() {
      return hasSequence;
    },
    get isAtEnd() {
      return isAtEnd;
    },

    // Actions
    play,
    pause,
    togglePlayPause,
    reset,
    nextBeat,
    setBpm,
    setMetronomeEnabled,
    setSequence,
    setCurrentBeatIndex,
  };
}
