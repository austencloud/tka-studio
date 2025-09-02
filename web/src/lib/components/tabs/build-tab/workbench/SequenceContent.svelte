<script lang="ts">
  import type { SequenceState } from "$state";
  import BeatFrame from "./BeatFrame.svelte";

  interface Props {
    sequenceState: SequenceState;
    onBeatSelected?: (index: number) => void;
  }

  let { sequenceState, onBeatSelected }: Props = $props();

  const currentSequence = $derived(sequenceState.currentSequence);
  const selectedBeatIndex = $derived(sequenceState.selectedBeatIndex);

  // TODO: Add scroll functionality back later
  let beatFrameShouldScroll = $state(false);

  function handleBeatClick(index: number) {
    onBeatSelected?.(index);
  }
</script>

<div
  class="sequence-container"
  style:justify-content={beatFrameShouldScroll ? "flex-start" : "center"}
  style:align-items={beatFrameShouldScroll ? "stretch" : "center"}
>
  <div class="content-wrapper" class:scroll-mode-active={beatFrameShouldScroll}>
    <div
      class="label-and-beatframe-unit"
      class:scroll-mode-active={beatFrameShouldScroll}
    >
      <!-- Removed sequence name label as requested -->

      <div
        class="beat-frame-wrapper"
        class:scroll-mode-active={beatFrameShouldScroll}
      >
        <BeatFrame
          beats={currentSequence?.beats ?? []}
          startPosition={currentSequence?.startPosition ?? null}
          {selectedBeatIndex}
          onBeatClick={handleBeatClick}
          isScrollable={beatFrameShouldScroll}
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
    padding: 10px 0 10px 0;
    box-sizing: border-box;
    transition: all 0.3s ease-out;
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
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

  .content-wrapper.scroll-mode-active {
    justify-content: flex-start;
  }

  .label-and-beatframe-unit {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    height: 100%;
    gap: 0;
    flex: 1 1 auto; /* Changed from 0 0 auto to allow growth */
    min-height: 0; /* Allow shrinking */
    transition: all 0.3s ease-out;
  }

  .label-and-beatframe-unit.scroll-mode-active {
    width: 100%;
    flex: 1 1 auto;
    min-height: 0;
  }

  .beat-frame-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    flex: 1 1 auto;
    min-height: 0;
  }

  .beat-frame-wrapper.scroll-mode-active {
    justify-content: flex-start;
    align-items: stretch;
  }
</style>
