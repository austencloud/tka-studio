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

  /* Placeholder styling */
  .placeholder-panel {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
    padding: var(--spacing-xl);
  }

  .placeholder-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--spacing-lg);
    text-align: center;
    max-width: 500px;
  }

  .placeholder-content h2 {
    font-size: 2rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(135deg, #ec4899, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .placeholder-content p {
    font-size: 1.125rem;
    opacity: 0.7;
    margin: 0;
  }

  .placeholder-button {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) var(--spacing-xl);
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.2), rgba(139, 92, 246, 0.2));
    border: 1px solid rgba(236, 72, 153, 0.3);
    border-radius: var(--border-radius-lg);
    color: white;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .placeholder-button:hover {
    background: linear-gradient(135deg, rgba(236, 72, 153, 0.3), rgba(139, 92, 246, 0.3));
    border-color: rgba(236, 72, 153, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(236, 72, 153, 0.3);
  }

  .placeholder-button:active {
    transform: translateY(0);
  }

  /* Color preview for tunnel mode */
  .color-preview {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius-md);
  }

  .color-box {
    width: 60px;
    height: 40px;
    border-radius: var(--border-radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 600;
    color: white;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  /* Mirror preview */
  .mirror-preview {
    display: flex;
    align-items: center;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius-md);
  }

  .mirror-box {
    width: 100px;
    height: 60px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: var(--border-radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    font-weight: 600;
    color: white;
  }

  .mirror-preview i {
    font-size: 1.5rem;
    opacity: 0.5;
  }

  /* Grid preview */
  .grid-preview {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-sm);
    padding: var(--spacing-md);
    background: rgba(255, 255, 255, 0.05);
    border-radius: var(--border-radius-md);
  }

  .grid-box {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, #3b82f6, #8b5cf6);
    border-radius: var(--border-radius-sm);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    font-weight: 600;
    color: white;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .placeholder-content h2 {
      font-size: 1.5rem;
    }

    .placeholder-content p {
      font-size: 1rem;
    }

    .color-box {
      width: 50px;
      height: 35px;
      font-size: 0.625rem;
    }

    .mirror-box {
      width: 80px;
      height: 50px;
    }

    .grid-box {
      width: 60px;
      height: 60px;
    }
  }
</style>
