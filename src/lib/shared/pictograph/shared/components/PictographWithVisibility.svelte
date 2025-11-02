<!--
PictographWithVisibility.svelte - Enhanced Pictograph with Visibility Controls

Extends the basic Pictograph component with sophisticated visibility controls
matching the legacy desktop app's behavior.
-->
<script lang="ts">
  import type { BeatData, PictographData } from "$shared";
  import { onMount } from "svelte";
  import { getVisibilityStateManager } from "../state/visibility-state.svelte";
  import Pictograph from "./Pictograph.svelte";

  let {
    pictographData = null,
    beatData = null,
    onClick,
    enableVisibility = true,
    forceShowAll = false,
  } = $props<{
    /** Pictograph data to render */
    pictographData?: PictographData | null;
    /** Beat data (alternative to pictographData) */
    beatData?: BeatData | null;
    /** Click handler */
    onClick?: () => void;
    /** Animation duration for transitions */
    animationDuration?: number;
    /** Show loading indicator */
    showLoadingIndicator?: boolean;
    /** Beat number for display */
    beatNumber?: number | null;
    /** Is this a start position? */
    isStartPosition?: boolean;
    /** Enable visibility controls (default: true) */
    enableVisibility?: boolean;
    /** Force show all elements (for visibility preview) */
    forceShowAll?: boolean;
  }>();

  // Visibility state manager
  let visibilityManager = getVisibilityStateManager();
  let visibilityUpdateCount = $state(0);

  // Force re-render when visibility changes
  function handleVisibilityChange() {
    visibilityUpdateCount++;
  }

  onMount(() => {
    if (enableVisibility) {
      visibilityManager.registerObserver(handleVisibilityChange);

      return () => {
        visibilityManager.unregisterObserver(handleVisibilityChange);
      };
    }

    return undefined;
  });

  // Derived state - get effective pictograph data with visibility applied
  const effectivePictographData = $derived(() => {
    // Force reactivity by accessing visibilityUpdateCount
    visibilityUpdateCount;

    const originalData = pictographData || beatData?.pictographData;
    if (!originalData || !enableVisibility || forceShowAll) {
      return originalData;
    }

    // Apply visibility filters
    const filteredData = { ...originalData };

    // Filter letter based on TKA visibility
    if (!visibilityManager.getGlyphVisibility("TKA")) {
      filteredData.letter = null;
    }

    return filteredData;
  });
</script>

<!-- Enhanced Pictograph with Visibility Controls -->
<div
  class="pictograph-with-visibility"
  class:visibility-enabled={enableVisibility}
  class:force-show-all={forceShowAll}
>
  <!-- Base Pictograph Component -->
  <Pictograph pictographData={effectivePictographData()} />
</div>

<style>
  .pictograph-with-visibility {
    position: relative;
    width: 100%;
    height: 100%;
  }
</style>
