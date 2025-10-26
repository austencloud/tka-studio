<!-- OrientationControlPanel.svelte - New expandable orientation controls with button/panel pattern -->
<script lang="ts">
  import type { BeatData, IDeviceDetector } from '$shared';
  import { resolve, TYPES } from '$shared';
  import { onMount } from 'svelte';
  import { slide } from 'svelte/transition';
  import ExpandedOrientationPanel from './ExpandedOrientationPanel.svelte';
  import InlineOrientationControl from './InlineOrientationControl.svelte';
  import { createOrientationControlExpansionState } from './orientation-control-expansion-state.svelte';
  import OrientationControlButton from './OrientationControlButton.svelte';

  // Props
  const {
    currentBeatData,
    onOrientationChanged
  } = $props<{
    currentBeatData: BeatData | null;
    onOrientationChanged: (color: string, orientation: string) => void;
  }>();

  // Services
  const deviceDetector = resolve<IDeviceDetector>(TYPES.IDeviceDetector);

  // State management for expansion
  const expansionState = createOrientationControlExpansionState();

  // Computed device characteristics
  const isDesktop = $derived(deviceDetector.isDesktop());
  const isTablet = $derived(deviceDetector.isTablet());

  // Responsive sizing strategy based on device type
  const layoutMode = $derived(() => {
    // Desktop: Minimize vertical space usage
    if (isDesktop) return 'compact';

    // Tablet: Balanced layout
    if (isTablet) return 'balanced';

    // Mobile: Full touch-friendly sizing
    return 'comfortable';
  });

  // Determine if we should show inline controls or use expandable pattern
  const shouldShowInlineControls = $derived(() => {
    // Desktop has plenty of vertical space in the adjustment section
    // Show inline controls to avoid unnecessary clicks
    if (isDesktop) return true;

    // Tablet and mobile have constrained space
    // Use expandable controls to maximize available space
    return false;
  });

  // Track previous beat index
  let previousBeatIndex = $state<number | null>(null);

  // When beat data changes, collapse any expanded controls
  $effect(() => {
    if (currentBeatData) {
      const currentBeatIndex = currentBeatData.beatNumber;

      // If beat changed, collapse (don't auto-expand)
      if (previousBeatIndex !== null && previousBeatIndex !== currentBeatIndex) {
        expansionState.collapse();
      }

      previousBeatIndex = currentBeatIndex;
    }
  });

  // Handlers
  function handleBlueExpand() {
    expansionState.expand('blue');
  }

  function handleRedExpand() {
    expansionState.expand('red');
  }

  function handleCollapse() {
    expansionState.collapse();
  }

  onMount(() => {
    console.log('OrientationControlPanel mounted - using device-based layout detection');
  });
</script>

<div
  class="orientation-control-panel"
  class:compact={layoutMode() === 'compact'}
  class:balanced={layoutMode() === 'balanced'}
  class:comfortable={layoutMode() === 'comfortable'}
  data-testid="orientation-control-panel"
>
  <div class="controls-container">
    {#if shouldShowInlineControls()}
      <!-- Inline controls when enough space is available -->
      <InlineOrientationControl
        color="blue"
        {currentBeatData}
        {onOrientationChanged}
        layoutMode={layoutMode()}
      />
      <InlineOrientationControl
        color="red"
        {currentBeatData}
        {onOrientationChanged}
        layoutMode={layoutMode()}
      />
    {:else}
      <!-- Expandable button/panel pattern for constrained spaces -->
      <!-- Blue/Left Control -->
      {#if expansionState.isBlueExpanded()}
        <div transition:slide={{ duration: 300, axis: 'y' }}>
          <ExpandedOrientationPanel
            color="blue"
            {currentBeatData}
            {onOrientationChanged}
            onCollapse={handleCollapse}
            layoutMode={layoutMode()}
          />
        </div>
      {:else}
        <OrientationControlButton
          color="blue"
          {currentBeatData}
          isExpanded={expansionState.isRedExpanded()}
          onExpand={handleBlueExpand}
          {onOrientationChanged}
          layoutMode={layoutMode()}
        />
      {/if}

      <!-- Red/Right Control -->
      {#if expansionState.isRedExpanded()}
        <div transition:slide={{ duration: 300, axis: 'y' }}>
          <ExpandedOrientationPanel
            color="red"
            {currentBeatData}
            {onOrientationChanged}
            onCollapse={handleCollapse}
            layoutMode={layoutMode()}
          />
        </div>
      {:else}
        <OrientationControlButton
          color="red"
          {currentBeatData}
          isExpanded={expansionState.isBlueExpanded()}
          onExpand={handleRedExpand}
          {onOrientationChanged}
          layoutMode={layoutMode()}
        />
      {/if}
    {/if}
  </div>
</div>

<style>
  .orientation-control-panel {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
  }

  .controls-container {
    display: flex;
    width: 100%;
    height: 100%;
    align-items: stretch;
  }

  /* Comfortable mode - Mobile, full touch-friendly sizing (default) */
  .orientation-control-panel.comfortable {
    padding: 0px;
  }

  /* Balanced mode - Tablet landscape, moderate sizing */
  .orientation-control-panel.balanced {
    padding: 0px;
  }

  /* Compact mode - Desktop, minimal vertical space */
  .orientation-control-panel.compact {
    padding: 8px;
  }

  /* Responsive adjustments for very small screens */
  @media (max-width: 400px) {
    .orientation-control-panel {
      padding: 12px;
    }
  }
</style>
