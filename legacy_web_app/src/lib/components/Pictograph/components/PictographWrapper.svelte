<!--
  PictographWrapper Component

  This component provides the wrapper element for the pictograph.
-->
<script lang="ts">
  import { get } from 'svelte/store';
  import type { PictographData } from '$lib/types/PictographData';
  import type { Writable } from 'svelte/store';
  import { getPictographElement, getPictographRole } from '../utils/PictographRenderUtils';
  import { handleClick } from '../handlers/PictographEventHandler';

  // Props
  export let pictographDataStore: Writable<PictographData>;
  export let onClick: (() => void) | undefined = undefined;
  export let state: string;
</script>

<!-- Use a button if onClick is provided, otherwise use a div -->
<svelte:element
  this={getPictographElement(onClick)}
  class="pictograph-wrapper"
  on:click={() => handleClick(onClick)}
  aria-label={onClick
    ? `Pictograph for letter ${get(pictographDataStore)?.letter || 'unknown'}`
    : undefined}
  role={getPictographRole(onClick)}
  data-state={state}
  data-letter={get(pictographDataStore)?.letter || 'none'}
  {...onClick ? { type: 'button' } : {}}
>
  <slot />
</svelte:element>

<style>
  .pictograph-wrapper {
    width: 100%;
    height: 100%;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    box-sizing: border-box;
    aspect-ratio: 1;
  }

  .pictograph-wrapper:hover {
    cursor: pointer;
  }

  .pictograph-wrapper:hover :global(.pictograph) {
    transform: scale(1.05);
    z-index: 4;
    border: 4px solid #48bb78;
    box-shadow:
      0 0 0 2px rgba(72, 187, 120, 0.4),
      0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .pictograph-wrapper:active :global(.pictograph) {
    transform: scale(1);
    transition-duration: 0.05s;
  }

  .pictograph-wrapper:focus-visible {
    outline: none;
  }

  .pictograph-wrapper:focus-visible :global(.pictograph) {
    outline: 3px solid #4299e1;
    outline-offset: 2px;
  }

  .pictograph-wrapper[data-state='error'] :global(.pictograph) {
    border-color: #fc8181;
    box-shadow: 0 0 0 1px #fc8181;
  }
</style>
