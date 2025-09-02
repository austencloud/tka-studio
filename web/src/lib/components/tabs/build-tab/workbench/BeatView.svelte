<script lang="ts">
  import type { BeatData } from "$domain";
  import { resolve, TYPES } from "$lib/services/inversify/container";
  import { createBeatFrameState } from "$state";
  import Beat from "./Beat.svelte";

  interface Props {
    beat: BeatData;
    index: number;
    isSelected?: boolean;
    isHovered?: boolean;
    onClick?: (index: number) => void;
    onHover?: (index: number) => void;
    onLeave?: () => void;
  }

  let {
    beat,
    index,
    isSelected = false,
    isHovered = false,
    onClick,
    onHover,
    onLeave,
  }: Props = $props();

  const beatFrameService = resolve<import("$contracts").IBeatFrameService>(
    TYPES.IBeatFrameService
  );
  const beatFrameState = createBeatFrameState(beatFrameService);

  const config = $derived(beatFrameState.config);

  function handleClick() {
    onClick?.(index);
  }

  function handleMouseEnter() {
    onHover?.(index);
  }

  function handleMouseLeave() {
    onLeave?.();
  }

  function handleKeyPress(event: KeyboardEvent) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      onClick?.(index);
    }
  }
</script>

<div
  class="beat-view"
  class:selected={isSelected}
  class:hovered={isHovered}
  class:blank={beat.isBlank}
  class:has-pictograph={beat.pictographData != null}
  style:width="{config.beatSize}px"
  style:height="{config.beatSize}px"
  style="position: relative; display: flex; align-items: center; justify-content: center;"
  onclick={handleClick}
  onkeypress={handleKeyPress}
  onmouseenter={handleMouseEnter}
  onmouseleave={handleMouseLeave}
  role="button"
  tabindex="0"
  aria-label="Beat {beat.beatNumber ?? index + 1}"
>
  <div class="beat-content">
    <!-- Use Beat component which handles all beat-specific logic -->
    <Beat
      {beat}
      {index}
      {isSelected}
      {isHovered}
      onClick={handleClick}
      width={config.beatSize - 2}
      height={config.beatSize - 2}
    />
  </div>
</div>

<style>
  .beat-view {
    position: relative;
    border: 1px solid #d0d7de;
    border-radius: 6px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: border-color 0.15s ease;
    background: transparent;
    user-select: none;
  }

  .beat-view:hover,
  .beat-view.hovered {
    border-color: #6ea8fe;
  }

  .beat-view.selected {
    border-color: #28a745;
    box-shadow: 0 0 0 2px rgba(40, 167, 69, 0.2);
  }

  .beat-view.blank {
    background: #f8f9fa;
    border-style: dashed;
  }

  .beat-view.has-pictograph {
    background: transparent;
  }

  .beat-content {
    text-align: center;
    font-weight: 600;
  }

  /* Focus styles for accessibility */
  .beat-view:focus {
    outline: none;
    border-color: #007bff;
    box-shadow: 0 0 0 2px rgba(0, 123, 255, 0.25);
  }
</style>
