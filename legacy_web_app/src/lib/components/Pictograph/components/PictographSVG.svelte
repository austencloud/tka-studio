<!--
  PictographSVG Component

  This component provides the SVG element for the pictograph.
-->
<script lang="ts">
  import { get } from 'svelte/store';
  import type { PictographData } from '$lib/types/PictographData';
  import type { Writable } from 'svelte/store';
  import { getPictographAriaLabel } from '../utils/componentPositioning';

  // Props
  export let pictographDataStore: Writable<PictographData>;
  export let state: string;
  export let errorMessage: string | null;
</script>

<svg
  class="pictograph"
  viewBox="0 0 950 950"
  xmlns="http://www.w3.org/2000/svg"
  role="img"
  aria-label={getPictographAriaLabel(state, errorMessage, get(pictographDataStore))}
>
  <slot />
</svg>

<style>
  .pictograph {
    width: 100%;
    height: 100%;
    max-width: 100%;
    max-height: 100%;
    display: block;
    background-color: white;
    transition: transform 0.1s ease-in-out;
    transform: scale(1);
    z-index: 1;
    position: relative;
    border: 1px solid #ccc;
    aspect-ratio: 1;
    margin: auto;
    overflow: visible;
    transform-origin: center center;
    box-sizing: border-box;
    display: flex;
    align-items: center;
    justify-content: center;
  }
</style>
