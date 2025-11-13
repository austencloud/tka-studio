<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { SequenceState } from "../../../state";
  import BeatGrid from "./BeatGrid.svelte";
  // import WorkspaceHeader from "./WorkspaceHeader.svelte"; // Moved to TopBar

  let {
    sequenceState,
    currentWord = "",
    onBeatSelected,
    onStartPositionSelected,
    onBeatDelete,
    selectedBeatNumber = null,
    practiceBeatNumber = null,
    isSideBySideLayout = false,
    isMultiSelectMode = false,
    selectedBeatNumbers = new Set<number>(),
    onBeatLongPress,
    onStartLongPress,
  } = $props<{
    sequenceState: SequenceState;
    currentWord?: string;
    onBeatSelected?: (beatNumber: number) => void;
    onStartPositionSelected?: () => void;
    onBeatDelete?: (beatNumber: number) => void;
    selectedBeatNumber?: number | null; // 0=start, 1=first beat, 2=second beat, etc.
    practiceBeatNumber?: number | null; // 0=start, 1=first beat, 2=second beat, etc.
    isSideBySideLayout?: boolean;
    isMultiSelectMode?: boolean;
    selectedBeatNumbers?: Set<number>;
    onBeatLongPress?: (beatNumber: number) => void;
    onStartLongPress?: () => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Progressive word building during animation
  let progressiveWord = $state("");
  let isAnimating = $state(false);

  // Use progressive word during animation, otherwise use the full current word
  const displayWord = $derived(isAnimating ? progressiveWord : currentWord);

  // Reference to the beat grid wrapper for event listening
  let beatGridWrapperRef: HTMLDivElement | undefined = $state();

  // Initialize haptic service on mount
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Effect: Reactive custom event handling for beat animations
  // Automatically manages event listeners based on beatGridWrapperRef availability
  $effect(() => {
    if (!beatGridWrapperRef) return;

    // Capture reference for closure (TypeScript flow analysis)
    const wrapper = beatGridWrapperRef;

    const handleBeatLetterAnimated = (event: Event) => {
      const customEvent = event as CustomEvent;
      const { letter } = customEvent.detail;
      progressiveWord += letter;
      isAnimating = true;
    };

    const handleSequentialAnimationComplete = () => {
      isAnimating = false;
      progressiveWord = "";
    };

    wrapper.addEventListener("beat-letter-animated", handleBeatLetterAnimated);
    wrapper.addEventListener(
      "sequential-animation-complete",
      handleSequentialAnimationComplete
    );

    return () => {
      wrapper.removeEventListener(
        "beat-letter-animated",
        handleBeatLetterAnimated
      );
      wrapper.removeEventListener(
        "sequential-animation-complete",
        handleSequentialAnimationComplete
      );
    };
  });

  const currentSequence = $derived(sequenceState.currentSequence);
  const selectedStartPosition = $derived(sequenceState.selectedStartPosition);
  const removingBeatIndex = $derived(sequenceState.getRemovingBeatIndex());
  const removingBeatIndices = $derived(sequenceState.getRemovingBeatIndices());
  const isClearing = $derived(sequenceState.getIsClearing());

  // Convert selectedStartPosition (PictographData) to BeatData format for BeatGrid
  const startPositionBeat = $derived(() => {
    if (!selectedStartPosition) return null;

    // Create BeatData that extends the PictographData
    return {
      ...selectedStartPosition,
      beatNumber: 0,
      duration: 1000,
      blueReversal: false,
      redReversal: false,
      isBlank: false,
    };
  });

  function handleBeatClick(beatNumber: number) {
    hapticService?.trigger("selection");
    onBeatSelected?.(beatNumber);
  }

  function handleStartPositionClick() {
    hapticService?.trigger("selection");
    onStartPositionSelected?.();
  }
</script>

<div class="sequence-container">
  <div class="content-wrapper">
    <div class="label-and-beatframe-unit">
      <!-- Workspace header with word label - MOVED TO TOP BAR -->
      <!-- <WorkspaceHeader
        word={displayWord}
        {isMultiSelectMode}
        sequence={currentSequence}
      /> -->

      <div bind:this={beatGridWrapperRef} class="beat-grid-wrapper">
        <BeatGrid
          beats={currentSequence?.beats ?? []}
          startPosition={startPositionBeat() ?? undefined}
          onBeatClick={handleBeatClick}
          onStartClick={handleStartPositionClick}
          {onBeatDelete}
          {selectedBeatNumber}
          {removingBeatIndex}
          {removingBeatIndices}
          {isClearing}
          {practiceBeatNumber}
          {isSideBySideLayout}
          {isMultiSelectMode}
          {selectedBeatNumbers}
          {onBeatLongPress}
          {onStartLongPress}
        />
      </div>
    </div>
  </div>
</div>

<style>
  .sequence-container {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    min-height: 0;
    overflow: visible;
    padding: 0; /* Removed padding - parent SequenceDisplay handles top spacing for word label */
    box-sizing: border-box;
    transition: all 0.3s ease-out;
  }

  .content-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    flex: 1;
    min-height: 0;
    transition: all 0.3s ease-out;
  }

  .label-and-beatframe-unit {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
    gap: 0;
    flex: 1 1 auto;
    min-height: 0;
    transition: all 0.3s ease-out;
  }

  .beat-grid-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    flex: 1 1 auto;
    min-height: 0;
  }
</style>
