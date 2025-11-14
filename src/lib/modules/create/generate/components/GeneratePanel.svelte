<!--
GeneratePanel.svelte - Clean, focused generation panel component

Card-based architecture with integrated Generate button:
- Settings: CardBasedSettingsContainer.svelte (card grid with all controls)
- Generate button: GenerateButtonCard.svelte (integrated into card grid)
- Config state: generateConfigState.svelte.ts
- Generation actions: generateActionsState.svelte.ts
- Device state: generateDeviceState.svelte.ts
- Responsive padding: Modern CSS container queries with cqi/cqb units (automatic scaling)
-->
<script lang="ts">
  import type { SequenceState } from "$create/shared/state";
  import { resolve, TYPES } from "$shared";
  import type { IDeviceDetector } from "$shared/device/services/contracts";
  import { onMount } from "svelte";
  import {
    createDeviceState,
    createGenerationActionsState,
    createGenerationConfigState,
  } from "../state";
  import { GeneratorPadder } from "../shared/services/implementations";
  import CardBasedSettingsContainer from "./CardBasedSettingsContainer.svelte";

  // Props
  let {
    sequenceState,
    isDesktop = false,
  }: {
    sequenceState: SequenceState;
    isDesktop?: boolean;
  } = $props();

  // Animation is always sequential with gentle bloom
  const isSequentialAnimation = true;

  // ===== State Management =====
  const configState = createGenerationConfigState();
  const actionsState = createGenerationActionsState(
    sequenceState,
    () => isSequentialAnimation
  );
  const deviceState = createDeviceState();

  // ===== Padding Service =====
  const paddingService = new GeneratorPadder();

  // Aspect-ratio-aware padding based on panel dimensions
  let panelElement = $state<HTMLElement | null>(null);
  let paddingTop = $state(12);
  let paddingRight = $state(12);
  let paddingBottom = $state(12);
  let paddingLeft = $state(12);

  // Debug info
  let debugWidth = $state(0);
  let debugHeight = $state(0);
  let debugAspectRatio = $state(1);
  let debugSizeScale = $state(1);

  // ===== Device Service Integration =====
  onMount(() => {
    try {
      const deviceService = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      deviceState.initializeDevice(deviceService);
    } catch (error) {
      // Fallback handled in deviceState
    }
  });

  // ===== Reactive ResizeObserver Setup =====
  // Use $effect to set up ResizeObserver when panelElement becomes available
  $effect(() => {
    if (!panelElement) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        const { width, height } = entry.contentRect;

        // Update debug values
        debugWidth = width;
        debugHeight = height;
        debugAspectRatio = width / height;

        // Calculate padding using service
        const padding = paddingService.calculatePadding(width, height);

        paddingTop = padding.top;
        paddingRight = padding.right;
        paddingBottom = padding.bottom;
        paddingLeft = padding.left;
        debugSizeScale = padding.scale;
      }
    });

    resizeObserver.observe(panelElement);

    // Cleanup function
    return () => {
      resizeObserver.disconnect();
    };
  });
</script>

<div
  class="generate-panel"
  bind:this={panelElement}
  data-layout={deviceState.layoutMode}
  data-allow-scroll={deviceState.shouldAllowScrolling}
  data-is-desktop={isDesktop}
  style="--min-touch-target: {deviceState.minTouchTarget}px; --element-spacing: {deviceState.elementSpacing}px; --padding-top: {paddingTop}; --padding-right: {paddingRight}; --padding-bottom: {paddingBottom}; --padding-left: {paddingLeft};"
>
  <div class="generate-panel-inner">
    <CardBasedSettingsContainer
      config={configState.config}
      isFreeformMode={configState.isFreeformMode}
      updateConfig={configState.updateConfig}
      isGenerating={actionsState.isGenerating}
      onGenerateClicked={actionsState.onGenerateClicked}
    />
  </div>

  <!-- <div class="debug-overlay">
    <div>Width: {Math.round(debugWidth)}px</div>
    <div>Height: {Math.round(debugHeight)}px</div>
    <div>Aspect: {debugAspectRatio.toFixed(2)}</div>
    <div>Scale: {debugSizeScale.toFixed(2)}x</div>
    <div>T/R/B/L: {Math.round(paddingTop)}/{Math.round(paddingRight)}/{Math.round(paddingBottom)}/{Math.round(paddingLeft)}</div>
  </div> -->
</div>

<style>
  .generate-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: visible; /* Allow card hover effects to be fully visible */
    gap: 0;
  }

  /* Inner wrapper with aspect-ratio-aware padding */
  .generate-panel-inner {
    flex: 1;
    display: flex;
    flex-direction: column;
    min-height: 0;

    /* Aspect-ratio-aware padding: different values for portrait vs landscape */
    /* Portrait: more top/bottom padding, less left/right */
    /* Landscape: more left/right padding, less top/bottom */
    padding-top: calc(var(--padding-top, 12) * 1px);
    padding-right: calc(var(--padding-right, 12) * 1px);
    padding-bottom: calc(var(--padding-bottom, 12) * 1px);
    padding-left: calc(var(--padding-left, 12) * 1px);
  }

  /* Ensure no scrolling is forced when not appropriate */
  .generate-panel[data-allow-scroll="false"] {
    overflow: hidden;
  }

  /* Debug Overlay */
  .debug-overlay {
    position: absolute;
    bottom: 8px;
    right: 8px;
    background: rgba(0, 0, 0, 0.9);
    color: #00ff00;
    font-family: monospace;
    font-size: 12px;
    padding: 8px 12px;
    border-radius: 4px;
    z-index: 10000;
    pointer-events: none;
    line-height: 1.6;
  }
</style>
