<!--
GeneratePanel.svelte - Clean, focused generation panel component

Refactored into smaller section components for better maintainability:
- Header: GeneratePanelHeader.svelte
- Settings: SettingsContainer.svelte (which includes individual sections)
- Actions: ActionSection.svelte
- Config state moved to generateConfigState.svelte.ts
- Generation actions moved to generateActionsState.svelte.ts
- Device state moved to generateDeviceState.svelte.ts
- Maintains all original functionality with cleaner separation
-->
<script lang="ts">
  import type { SequenceState } from "$build/shared/state";
  import { resolve, TYPES } from "$shared";
  import type { IDeviceDetector } from "$shared/device/services/contracts";
  import { onMount } from "svelte";
  import { createDeviceState, createGenerationActionsState, createGenerationConfigState } from "../state";
  import CardBasedSettingsContainer from "./CardBasedSettingsContainer.svelte";

  // Props
  let {
    sequenceState,
  }: {
    sequenceState: SequenceState;
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


  // ===== Device Service Integration =====
  onMount(() => {
    try {
      const deviceService = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      return deviceState.initializeDevice(deviceService);
    } catch (error) {
      // Fallback handled in deviceState
      return undefined;
    }
  });
</script>

<div
  class="generate-panel"
  data-layout={deviceState.layoutMode}
  data-allow-scroll={deviceState.shouldAllowScrolling}
  style="--min-touch-target: {deviceState.minTouchTarget}px; --element-spacing: {deviceState.elementSpacing}px;"
>
  <CardBasedSettingsContainer
    config={configState.config}
    isFreeformMode={configState.isFreeformMode}
    updateConfig={configState.updateConfig}
    isGenerating={actionsState.isGenerating}
    onGenerateClicked={actionsState.onGenerateClicked}
  />
</div>

<style>
  .generate-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    width: 100%;
    overflow: hidden;
    gap: 0;
  }

  /* Settings container takes up all available space */
  .generate-panel > :global(div:nth-child(1)) {
    flex: 1;
    height: 100%;
    padding: var(--element-spacing);
    border-radius: 8px;
    font-family: "Segoe UI", sans-serif;
    overflow: auto;
    gap: calc(var(--element-spacing) );
  }

  /* Ensure no scrolling is forced when not appropriate */
  .generate-panel[data-allow-scroll="false"] {
    overflow: hidden;
  }
</style>
