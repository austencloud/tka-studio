<!--
  AnimationPanel.svelte

  Pure presentation component for animation display.
  All business logic lives in AnimationCoordinator.

  This component:
  - Receives all state as props
  - Displays UI based on props
  - Emits events when user interacts
  - Has ZERO business logic
  - ONLY shows animation and allows exiting (export moved to Share panel)
-->
<script lang="ts">
  import AnimatorCanvas from "$create/animate/components/AnimatorCanvas.svelte";
  import AnimationControls from "$create/animate/components/AnimationControls.svelte";
  import { CreatePanelDrawer } from "$create/shared/components";
  import PanelHeader from "$create/shared/components/PanelHeader.svelte";
  import { GridMode, type Letter, type BeatData } from "$shared";
  import type { PropState } from "$create/animate/domain/types/PropState";

  // Props - ALL state comes from parent
  let {
    show = false,
    combinedPanelHeight = 0,
    isSideBySideLayout = false,
    loading = false,
    error = null,
    speed = 1,
    blueProp = null,
    redProp = null,
    gridVisible = true,
    gridMode = null,
    letter = null,
    beatData = null,
    onClose = () => {},
    onSpeedChange = () => {},
    onCanvasReady = () => {},
  }: {
    show?: boolean;
    combinedPanelHeight?: number;
    isSideBySideLayout?: boolean;
    loading?: boolean;
    error?: string | null;
    speed?: number;
    blueProp?: PropState | null;
    redProp?: PropState | null;
    gridVisible?: boolean;
    gridMode?: GridMode | null | undefined;
    letter?: Letter | null;
    beatData?: BeatData | null;
    onClose?: () => void;
    onSpeedChange?: (newSpeed: number) => void;
    onCanvasReady?: (canvas: HTMLCanvasElement | null) => void;
  } = $props();
</script>

<CreatePanelDrawer
  isOpen={show}
  panelName="animation"
  {combinedPanelHeight}
  showHandle={true}
  closeOnBackdrop={false}
  focusTrap={false}
  lockScroll={false}
  labelledBy="animation-panel-title"
  {onClose}
>
  <div
    class="animation-panel"
    role="dialog"
    aria-labelledby="animation-panel-title"
  >
    <PanelHeader
      title="Animation Viewer"
      isMobile={!isSideBySideLayout}
      {onClose}
    />

    <h2 id="animation-panel-title" class="sr-only">Animation Viewer</h2>

    {#if loading}
      <div class="loading-message">Loading animation...</div>
    {:else if error}
      <div class="error-message">{error}</div>
    {:else}
      <!-- Animation Viewer -->
      <div class="canvas-container">
        <AnimatorCanvas
          {blueProp}
          {redProp}
          {gridVisible}
          {gridMode}
          {letter}
          {beatData}
          {onCanvasReady}
        />
      </div>

      <AnimationControls {speed} {onSpeedChange} />
    {/if}
  </div>
</CreatePanelDrawer>

<style>
  .animation-panel {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align to top for header */
    gap: 16px;
    padding: 0; /* No padding - PanelHeader handles its own spacing */
    padding-bottom: calc(24px + env(safe-area-inset-bottom));
    width: 100%;
    height: 100%;
    /* Background is on CreatePanelDrawer */
    background: transparent;
  }

  .sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border: 0;
  }

  .canvas-container {
    container-type: size;
    container-name: animator-canvas;
    flex: 1;
    width: 100%;
    max-width: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 0;
    padding: 0 24px; /* Horizontal padding for canvas */
  }

  .loading-message,
  .error-message {
    padding: 2rem;
    text-align: center;
    color: rgba(255, 255, 255, 0.7);
    font-size: 0.9rem;
  }

  .error-message {
    color: rgba(255, 100, 100, 0.9);
  }

  /* Mobile responsive adjustments */
  @media (max-width: 768px) {
    .animation-panel {
      padding: 0 16px 16px 16px;
      padding-bottom: calc(16px + env(safe-area-inset-bottom));
      gap: 12px;
    }
  }

  @media (max-width: 480px) {
    .animation-panel {
      padding: 0 12px 12px 12px;
      padding-bottom: calc(12px + env(safe-area-inset-bottom));
      gap: 8px;
    }
  }

  /* Landscape mobile: Adjust spacing */
  @media (min-aspect-ratio: 17/10) and (max-height: 500px) {
    .animation-panel {
      padding: 0 12px 12px 12px;
      gap: 8px;
    }

    .canvas-container {
      max-width: 500px;
    }
  }
</style>
