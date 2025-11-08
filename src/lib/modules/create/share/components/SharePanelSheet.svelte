<!--
  SharePanelSheet.svelte

  Bottom sheet wrapper around SharePanel with matching layout to AnimationPanel.
-->
<script lang="ts">
  import { Drawer, SheetDragHandle } from "$shared";
  import { tryGetCreateModuleContext } from "../../shared/context";
  import type { SequenceData } from "$shared";
  import type { ShareState } from "../state";
  import SharePanel from "./SharePanel.svelte";

  let {
    show = $bindable(false),
    sequence = null,
    shareState = null,
    onClose,
    onSequenceUpdate,
    heading = "Share Sequence",
  }: {
    show?: boolean;
    sequence?: SequenceData | null;
    shareState?: ShareState | null;
    onClose?: () => void;
    onSequenceUpdate?: (sequence: SequenceData) => void;
    heading?: string;
  } = $props();

  function handleClose() {
    show = false;
    onClose?.();
  }

  // Watch for external close (e.g., via vaul-svelte gesture)
  let wasOpen = $state(show);
  $effect(() => {
    if (wasOpen && !show) {
      // Drawer was closed externally (gesture, etc.)
      onClose?.();
    }
    wasOpen = show;
  });

  const createModuleContext = tryGetCreateModuleContext();
  const isSideBySideLayout = $derived(
    createModuleContext
      ? createModuleContext.layout.shouldUseSideBySideLayout
      : false
  );
  const drawerPlacement = $derived(isSideBySideLayout ? "right" : "bottom");
</script>

<Drawer
  bind:isOpen={show}
  labelledBy="share-panel-title"
  onclose={handleClose}
  closeOnBackdrop={true}
  focusTrap={true}
  lockScroll={true}
  showHandle={false}
  respectLayoutMode={true}
  placement={drawerPlacement}
  class="share-sheet"
  backdropClass="share-sheet__backdrop"
>
  <div class="share-sheet__container" class:desktop-layout={isSideBySideLayout}>
    <SheetDragHandle class={isSideBySideLayout ? "side-handle" : ""} />
    <header class="share-sheet__header">
      <h2 id="share-panel-title">{heading}</h2>
      <button
        class="share-sheet__close"
        onclick={handleClose}
        aria-label="Close share panel"
      >
        <i class="fas fa-times"></i>
      </button>
    </header>

    <div class="share-sheet__content">
      <SharePanel
        currentSequence={sequence}
        {shareState}
        onClose={handleClose}
        {...onSequenceUpdate ? { onSequenceUpdate } : {}}
      />
    </div>
  </div>
</Drawer>

<style>
  /* Use unified sheet system variables */
  :global(.drawer-content.share-sheet) {
    --sheet-z-index: var(--sheet-z-modal);
    --sheet-backdrop-bg: var(--backdrop-opaque);
    --sheet-backdrop-filter: var(--backdrop-blur-strong);
    --sheet-bg: var(--sheet-bg-gradient);
    --sheet-max-height: 100vh;
    --sheet-shadow: var(--sheet-shadow-elevated);
  }

  /* Container - full screen modern gradient */
  .share-sheet__container {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    height: 100dvh;
    overflow: hidden;
  }

  .share-sheet__container.desktop-layout {
    height: 100%;
    max-height: none;
  }

  /* Position drag handle on the left for side-by-side layout */
  .share-sheet__container.desktop-layout
    :global(.sheet-drag-handle.side-handle) {
    position: absolute;
    top: 50%;
    left: 18px;
    width: 4px;
    height: 48px;
    margin: 0;
    border-radius: 999px;
    transform: translateY(-50%);
  }

  /* Header - Modern 2026 styling */
  .share-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding: 16px 20px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(12px);
    flex-shrink: 0;
    background: rgba(255, 255, 255, 0.02);
  }

  .share-sheet__header h2 {
    font-size: 20px;
    font-weight: 700;
    background: linear-gradient(
      135deg,
      #ffffff 0%,
      rgba(255, 255, 255, 0.8) 100%
    );
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.02em;
  }

  /* Close button with modern styling */
  .share-sheet__close {
    width: var(--sheet-close-size-default);
    height: var(--sheet-close-size-default);
    border-radius: 50%;
    border: none;
    background: var(--sheet-close-bg);
    color: rgba(255, 255, 255, 0.9);
    font-size: 20px;
    cursor: pointer;
    transition: all var(--sheet-transition-spring);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .share-sheet__close:hover {
    background: var(--sheet-close-bg-hover);
    transform: scale(1.08) rotate(90deg);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
  }

  .share-sheet__close:active {
    transform: scale(0.95) rotate(90deg);
  }

  .share-sheet__close:focus-visible {
    outline: 3px solid rgba(191, 219, 254, 0.7);
    outline-offset: 3px;
  }

  /* Content area - full height */
  .share-sheet__content {
    flex: 1;
    min-height: 0;
    overflow: hidden;
  }

  @media (max-width: 768px) {
    .share-sheet__header {
      padding: 18px 20px 10px;
    }

    .share-sheet__header h2 {
      font-size: 18px;
    }
  }

  @media (max-width: 480px) {
    .share-sheet__header {
      padding: 16px 18px 10px;
    }

    .share-sheet__header h2 {
      font-size: 17px;
    }

    .share-sheet__close {
      width: var(--sheet-close-size-small);
      height: var(--sheet-close-size-small);
      font-size: 18px;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .share-sheet__close {
      transition: none;
    }

    .share-sheet__close:hover,
    .share-sheet__close:active {
      transform: none;
    }
  }
</style>
