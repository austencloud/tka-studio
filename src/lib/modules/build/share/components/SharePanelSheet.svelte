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
    heading = "Share Sequence",
  }: {
    show?: boolean;
    sequence?: SequenceData | null;
    onClose?: () => void;
    heading?: string;
  } = $props();

  function handleClose() {
    onClose?.();
  }
</script>

<BottomSheet
  isOpen={show}
  labelledBy="share-panel-title"
  on:close={handleClose}
  closeOnBackdrop={true}
  focusTrap={true}
  lockScroll={true}
  showHandle={false}
  class="share-sheet"
  backdropClass="share-sheet__backdrop"
>
  <div class="share-sheet__container">
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
      <SharePanel currentSequence={sequence} onClose={handleClose} />
    </div>
  </div>
</BottomSheet>

<style>
  /* Backdrop - opaque to cover workspace */
  :global(.share-sheet__backdrop) {
    z-index: 1200;
    background: rgba(0, 0, 0, 0.85) !important;
    backdrop-filter: blur(8px);
  }

  /* Container - full screen modern gradient */
  .share-sheet__container {
    position: relative;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100vh;
    height: 100dvh;
    background: linear-gradient(
      135deg,
      rgba(20, 25, 35, 0.98) 0%,
      rgba(15, 20, 30, 0.95) 100%
    );
    box-shadow: 0 -20px 60px rgba(0, 0, 0, 0.5);
    overflow: hidden;
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
    background: linear-gradient(135deg, #ffffff 0%, rgba(255, 255, 255, 0.8) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0;
    letter-spacing: -0.02em;
  }

  /* Close button with modern styling */
  .share-sheet__close {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.9);
    font-size: 20px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .share-sheet__close:hover {
    background: rgba(255, 255, 255, 0.16);
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
