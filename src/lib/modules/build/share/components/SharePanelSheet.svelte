<!--
  SharePanelSheet.svelte

  Bottom sheet wrapper around SharePanel with matching layout to AnimationPanel.
-->
<script lang="ts">
  import { BottomSheet } from "$shared";
  import type { SequenceData } from "$shared";
  import SharePanel from "./SharePanel.svelte";

  const {
    show = false,
    sequence = null,
    onClose,
    toolPanelHeight = 0,
    heading = "Share Sequence",
  }: {
    show?: boolean;
    sequence?: SequenceData | null;
    onClose?: () => void;
    toolPanelHeight?: number;
    heading?: string;
  } = $props();

  const panelHeightStyle = $derived(() => {
    if (toolPanelHeight > 0) {
      return `height: ${toolPanelHeight}px;`;
    }
    return "height: 70vh;";
  });

  function handleClose() {
    onClose?.();
  }
</script>

<BottomSheet
  isOpen={show}
  labelledBy="share-panel-title"
  on:close={handleClose}
  class="share-sheet"
  backdropClass="share-sheet__backdrop"
>
  <div class="share-sheet__container" style={panelHeightStyle()}>
    <header class="share-sheet__header">
      <h2 id="share-panel-title">{heading}</h2>
      <button
        class="share-sheet__close"
        onclick={handleClose}
        aria-label="Close share panel"
      >
        <span aria-hidden="true">&times;</span>
      </button>
    </header>

    <div class="share-sheet__content">
      <SharePanel currentSequence={sequence} />
    </div>
  </div>
</BottomSheet>

<style>
  :global(.share-sheet__backdrop) {
    z-index: 1200;
  }

  :global(.share-sheet.share-sheet__backdrop) {
    background: rgba(17, 24, 39, 0.75);
  }

  .share-sheet__container {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    border-radius: 32px 32px 0 0;
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.96), rgba(30, 64, 175, 0.88));
    padding: 24px;
    box-shadow:
      0 -18px 45px rgba(8, 14, 35, 0.45),
      inset 0 1px 0 rgba(255, 255, 255, 0.05);
    overflow: hidden;
  }

  .share-sheet__header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    margin-bottom: 16px;
  }

  .share-sheet__header h2 {
    font-size: 20px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.92);
    margin: 0;
  }

  .share-sheet__close {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    font-size: 20px;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .share-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
    transform: scale(1.05);
  }

  .share-sheet__close:active {
    transform: scale(0.95);
  }

  .share-sheet__close:focus-visible {
    outline: 2px solid rgba(191, 219, 254, 0.7);
    outline-offset: 2px;
  }

  .share-sheet__content {
    flex: 1;
    min-height: 0;
  }

  @media (max-width: 768px) {
    .share-sheet__container {
      border-radius: 28px 28px 0 0;
      padding: 20px 18px;
    }

    .share-sheet__header h2 {
      font-size: 18px;
    }
  }

  @media (max-width: 480px) {
    .share-sheet__container {
      border-radius: 24px 24px 0 0;
      padding: 18px 16px;
    }

    .share-sheet__header h2 {
      font-size: 17px;
    }

    .share-sheet__close {
      width: 40px;
      height: 40px;
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
