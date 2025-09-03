<!-- src/lib/components/SequenceWorkbench/RightPanel/RightPanel.svelte -->
<script lang="ts">
  import { workbenchStore } from "$lib/state/stores/workbenchStore";
  import ModernGenerationControls from "./ModernGenerationControls.svelte";
  import OptionPickerWithDebug from "$lib/components/ConstructTab/OptionPicker/OptionPickerWithDebug.svelte";
  import StartPosPicker from "$lib/components/ConstructTab/StartPosPicker/StartPosPicker.svelte";
  import TransitionWrapper from "./TransitionWrapper.svelte";
  import { isSequenceEmpty } from "$lib/state/machines/sequenceMachine/persistence";
  import { fade, fly } from "svelte/transition";
  import { cubicInOut } from "svelte/easing";

  // Transition parameters
  const transitionDuration = 400;
  const fadeParams = { duration: transitionDuration, easing: cubicInOut };
  const flyParams = {
    duration: transitionDuration,
    easing: cubicInOut,
    y: 20,
  };
</script>

<div class="right-panel">
  {#if $workbenchStore.activeTab === "generate"}
    <div in:fly={flyParams} out:fade={fadeParams}>
      <ModernGenerationControls />
    </div>
  {:else}
    <TransitionWrapper isSequenceEmpty={$isSequenceEmpty} {transitionDuration}>
      <div slot="startPosPicker" class="full-height-wrapper">
        <StartPosPicker />
      </div>
      <div slot="optionPicker" class="full-height-wrapper">
        <OptionPickerWithDebug />
      </div>
    </TransitionWrapper>
  {/if}
</div>

<style>
  .right-panel {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    flex-direction: column;
    border-radius: 0.75rem;
    border: 1px solid rgba(255, 255, 255, 0.1);
    overflow: hidden;
  }

  /* Button panel container removed - now handled by SharedWorkbench */

  .full-height-wrapper {
    height: 100%;
    display: flex;
    flex-direction: column;
  }
</style>
