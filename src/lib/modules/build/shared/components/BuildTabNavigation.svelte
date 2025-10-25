<!--
	BuildTabNavigation.svelte

	Tab navigation component extracted from BuildTab.
	Handles the 4-tab navigation (Build/Generate/Edit/Export) with active state management.
-->
<script lang="ts">
  import type { ActiveBuildTab } from "$shared";
  import { resolve, TYPES, type IHapticFeedbackService } from "$shared";
  import { onMount } from "svelte";
  import { constructTabTransitionService } from "../services/implementations/BuildTabTransitionService";

  // Service resolution
  let hapticService: IHapticFeedbackService | null = $state(null);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Props from parent
  const {
    activeBuildSubTab: activeBuildsubTab,
    setActiveBuildSubTab: setActiveBuildSubTab,
  }: {
    activeBuildSubTab: ActiveBuildTab;
    setActiveBuildSubTab: (tab: ActiveBuildTab) => void;
  } = $props();

  async function handleTabClick(targetTab: ActiveBuildTab) {
    hapticService?.trigger('navigation');
    await constructTabTransitionService.handleMainTabTransition(
      targetTab,
      activeBuildsubTab,
      setActiveBuildSubTab
    );
  }

  function handleKeyDown(event: KeyboardEvent, targetTab: ActiveBuildTab) {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      hapticService?.trigger('navigation');
      handleTabClick(targetTab);
    }
  }
</script>

<div class="build-tab-navigation" data-testid="tab-navigation">
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "construct"}
    onclick={() => handleTabClick("construct")}
    onkeydown={(e) => handleKeyDown(e, "construct")}
  >
    🔨 Construct
  </button>
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "generate"}
    onclick={() => handleTabClick("generate")}
    onkeydown={(e) => handleKeyDown(e, "generate")}
  >
    ⚡ Generate
  </button>
  <!-- Edit tab removed - now using slide-out panel instead! -->
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "animate"}
    onclick={() => handleTabClick("animate")}
    onkeydown={(e) => handleKeyDown(e, "animate")}
  >
    🎬 Animate
  </button>
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "share"}
    onclick={() => handleTabClick("share")}
    onkeydown={(e) => handleKeyDown(e, "share")}
  >
    <i class="fas fa-share"></i> Share
  </button>
  <button
    type="button"
    class="main-tab-btn"
    class:active={activeBuildsubTab === "record"}
    onclick={() => handleTabClick("record")}
    onkeydown={(e) => handleKeyDown(e, "record")}
  >
    🎥 Record
  </button>
</div>

<style>
  .build-tab-navigation {
    flex-shrink: 0;
    display: flex;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border);
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 12px 12px 0 0;
    padding: 4px;
    gap: 2px;
    position: relative;
    overflow: hidden;
  }

  .build-tab-navigation::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(
      90deg,
      transparent,
      rgba(255, 255, 255, 0.3),
      transparent
    );
  }

  .main-tab-btn {
    flex: 1;
    padding: var(--spacing-md);
    border: none;
    background: transparent;
    color: var(--muted-foreground);
    cursor: pointer;
    transition: all var(--transition-normal);
    font-size: var(--font-size-sm);
    font-weight: 600;
    border: 1px solid transparent;
    border-radius: 8px 8px 0 0;
    position: relative;
    overflow: hidden;
  }

  .main-tab-btn::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: var(--gradient-primary);
    opacity: 0;
    transition: opacity var(--transition-normal);
    z-index: -1;
  }

  .main-tab-btn:hover {
    background: var(--surface-hover);
    color: var(--foreground);
    border-color: rgba(255, 255, 255, 0.15);
    backdrop-filter: var(--glass-backdrop);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  }

  .main-tab-btn.active {
    background: var(--surface-active);
    backdrop-filter: var(--glass-backdrop);
    border: var(--glass-border-hover);
    color: var(--primary-light);
    box-shadow: var(--shadow-glass);
    transform: translateY(-2px);
  }

  .main-tab-btn.active::before {
    opacity: 0.1;
  }

  .main-tab-btn.active::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 3px;
    background: var(--gradient-primary);
    border-radius: 2px 2px 0 0;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .build-tab-navigation {
      flex-wrap: wrap;
    }

    .main-tab-btn {
      flex: 1 1 50%;
      padding: var(--spacing-sm);
      font-size: var(--font-size-xs);
    }
  }
</style>
