<!--
  AnimateTab.svelte - Advanced Animation Visualization Module

  Modes:
  - Single: Animate one sequence (full-screen canvas)
  - Tunnel: Overlay two sequences with different colors
  - Mirror: Side-by-side view with one mirrored
  - Grid: 2×2 grid with rotation offsets

  Navigation via tabs controlled by bottom navigation
-->
<script lang="ts">
  import { navigationState } from "$shared";
  import { onMount } from "svelte";
  import { createAnimateModuleState } from "./shared/state/animate-module-state.svelte";
  import type { AnimateMode } from "./shared/state/animate-module-state.svelte";

  // Import mode panels
  import SingleModePanel from "./modes/SingleModePanel.svelte";
  import TunnelModePanel from "./modes/TunnelModePanel.svelte";
  import MirrorModePanel from "./modes/MirrorModePanel.svelte";
  import GridModePanel from "./modes/GridModePanel.svelte";

  // Create module state
  const animateState = createAnimateModuleState();

  // Sync current mode with navigation state
  $effect(() => {
    const section = navigationState.activeTab;
    if (
      section === "single" ||
      section === "tunnel" ||
      section === "mirror" ||
      section === "grid"
    ) {
      animateState.setCurrentMode(section as AnimateMode);
    }
  });

  // Initialize on mount
  onMount(() => {
    console.log("✅ AnimateTab: Mounted");

    // Set default mode if none persisted
    const section = navigationState.activeTab;
    if (
      !section ||
      (section !== "single" &&
        section !== "tunnel" &&
        section !== "mirror" &&
        section !== "grid")
    ) {
      navigationState.setActiveTab("single");
    }
  });

  // Check if mode is active
  function isModeActive(mode: AnimateMode): boolean {
    return animateState.currentMode === mode;
  }
</script>

<div class="animate-tab">
  <!-- Mode-specific panels -->
  <div class="content-container">
    <!-- Single Mode -->
    <div class="mode-panel" class:active={isModeActive("single")}>
      <SingleModePanel {animateState} />
    </div>

    <!-- Tunnel Mode -->
    <div class="mode-panel" class:active={isModeActive("tunnel")}>
      <TunnelModePanel {animateState} />
    </div>

    <!-- Mirror Mode -->
    <div class="mode-panel" class:active={isModeActive("mirror")}>
      <MirrorModePanel {animateState} />
    </div>

    <!-- Grid Mode -->
    <div class="mode-panel" class:active={isModeActive("grid")}>
      <GridModePanel {animateState} />
    </div>
  </div>

</div>

<style>
  .animate-tab {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    background: linear-gradient(135deg, rgba(20, 25, 35, 1) 0%, rgba(15, 20, 30, 1) 100%);
    color: var(--foreground, #ffffff);
  }

  /* Content container */
  .content-container {
    position: relative;
    flex: 1;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  /* Mode panels */
  .mode-panel {
    position: absolute;
    inset: 0;
    display: none;
    width: 100%;
    height: 100%;
    overflow: hidden;
  }

  .mode-panel.active {
    display: flex;
    flex-direction: column;
  }
</style>
