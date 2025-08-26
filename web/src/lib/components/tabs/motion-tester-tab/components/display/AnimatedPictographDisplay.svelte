<!--
AnimatedPictographDisplay.svelte - Displays animated pictograph with error handling

Single responsibility: Render the animated pictograph or show error state.
No animation controls, no data creation - just pure display logic.
-->
<script lang="ts">
  import Pictograph from "$lib/components/core/pictograph/Pictograph.svelte";
  import type { PictographData } from "$lib/domain";

  interface Props {
    pictographData: PictographData | null;
    size?: number;
    debug?: boolean;
  }

  let { pictographData }: Props = $props();
</script>

<div class="pictograph-display">
  {#if pictographData}
    <Pictograph {pictographData} />
  {:else}
    <div class="error-state">
      <span class="error-icon" aria-hidden="true">⚠️</span>
      <p>Unable to display pictograph</p>
    </div>
  {/if}
</div>

<style>
  .pictograph-display {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
  }

  .error-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #f87171;
    text-align: center;
    padding: 40px;
  }

  .error-icon {
    font-size: 32px;
    margin-bottom: 12px;
  }

  .error-state p {
    margin: 0;
    font-size: 16px;
    color: #fca5a5;
  }
</style>
