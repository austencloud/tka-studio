<!--
GeneratePanel.svelte - Clean, focused generation panel component

Refactored into smaller section components for better maintainability:
- Header: GeneratePanelHeader.svelte
- Settings: SettingsContainer.svelte (which includes individual sections)
- Actions: ActionSection.svelte
- Configuration state moved to generateConfigState.svelte.ts
- Generation actions moved to generateActionsState.svelte.ts
- Device state moved to generateDeviceState.svelte.ts
- Maintains all original functionality with cleaner separation
-->
<script lang="ts">
  import type { IDeviceDetector } from "$contracts";
  import { resolve, TYPES } from "$lib/services/inversify/container";
  import { onMount } from "svelte";
  // Import section components
  import ActionSection from "./components/ActionSection.svelte";
  import GeneratePanelHeader from "./components/GeneratePanelHeader.svelte";
  import SettingsContainer from "./components/SettingsContainer.svelte";
  // Import simple state managers
  import { createGenerationActionsState } from "$state";
  import { createGenerationConfigState } from "$state";
  import { createDeviceState } from "$state";

  // ===== State Management =====
  const configState = createGenerationConfigState();
  const actionsState = createGenerationActionsState();
  const deviceState = createDeviceState();

  // ===== Device Service Integration =====
  onMount(() => {
    try {
      const deviceService = resolve<IDeviceDetector>(TYPES.IDeviceDetector);
      return deviceState.initializeDevice(deviceService);
    } catch (error) {
      console.log("GeneratePanel: Device service not ready yet:", error);
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
  <GeneratePanelHeader />

  <SettingsContainer
    config={configState.config}
    isFreeformMode={configState.isFreeformMode}
  />

  <ActionSection
    onAutoCompleteClicked={actionsState.onAutoCompleteClicked}
    onGenerateClicked={actionsState.onGenerateClicked}
    config={configState.config}
    isGenerating={actionsState.isGenerating}
  />
</div>

<!-- Main panel styling only - child components handle their own styles -->
<style>
  .generate-panel {
    display: flex;
    flex-direction: column;
    height: 100%;
    padding: 16px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.9);
    font-family: "Segoe UI", sans-serif;
    gap: var(--element-spacing);
    overflow: hidden;
  }

  /* Responsive layouts based on device capabilities */
  .generate-panel[data-layout="spacious"] {
    padding: calc(var(--element-spacing) * 1.5);
    gap: calc(var(--element-spacing) * 1.5);
  }

  .generate-panel[data-layout="compact"] {
    padding: 12px;
    gap: calc(var(--element-spacing) * 0.75);
  }

  /* Ensure no scrolling is forced when not appropriate */
  .generate-panel[data-allow-scroll="false"] {
    overflow: hidden;
  }

  /* Mobile-specific adjustments */
  @media (max-width: 768px) {
    .generate-panel {
      padding: var(--element-spacing);
    }
  }
</style>
