<script lang="ts">
  import { Beat } from "$lib/components/pictograph";
  import type { BeatData } from "$lib/domain";
  import { resolve } from "$lib/services/bootstrap";
  import { createBeatFrameState } from "$lib/state/beat-frame/beat-frame-state.svelte";

  interface Props {
    beat: BeatData;
    index: number;
    isSelected?: boolean;
    isHovered?: boolean;
    onClick?: (index: number) => void;
    onDoubleClick?: (index: number) => void;
    onHover?: (index: number) => void;
    onLeave?: () => void;
  }

  let {
    beat,
    index,
    isSelected = false,
    isHovered = false,
    onClick,
    onDoubleClick,
    onHover,
    onLeave,
  }: Props = $props();

  // Get service from DI container and create component-scoped state
  const beatFrameService = resolve(
    "IBeatFrameService"
  ) as import("$lib/services/interfaces/beat-frame-interfaces").IBeatFrameService;
  const beatFrameState = createBeatFrameState(beatFrameService);

  const config = $derived(beatFrameState.config);

  function handleClick() {
    onClick?.(index);
  }

  function handleDoubleClick() {
    onDoubleClick?.(index);
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
  ondblclick={handleDoubleClick}
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
