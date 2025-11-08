<!--
ModalHeader.svelte - Reusable modal header component
Displays modal title and close button
-->
<script lang="ts">
  let {
    title,
    icon = "",
    onClose,
  } = $props<{
    title: string;
    icon?: string;
    onClose: () => void;
  }>();
</script>

<div class="modal-header">
  <h2 id="modal-title">
    {icon}{#if icon}&nbsp;{/if}{title}
  </h2>
  <button class="close-button" onclick={onClose} aria-label="Close modal">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>
</div>

<style>
  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    flex-shrink: 0;
  }

  h2 {
    margin: 0;
    font-size: 24px;
    font-weight: 700;
    color: white;
  }

  .close-button {
    /* 44px minimum for touch targets on mobile */
    width: 44px;
    height: 44px;
    padding: 0;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
  }

  .close-button svg {
    width: 20px;
    height: 20px;
    color: white;
  }

  .close-button:hover {
    background: rgba(239, 68, 68, 0.3);
    border-color: rgba(239, 68, 68, 0.5);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  /* Mobile responsive - maintain 44px minimum */
  @media (max-width: 640px) {
    .modal-header {
      padding: 16px 20px 12px;
    }

    h2 {
      font-size: 20px;
    }

    .close-button {
      width: 44px; /* Maintain 44px minimum */
      height: 44px;
    }

    .close-button svg {
      width: 18px;
      height: 18px;
    }
  }

  /* Optimize for very narrow devices - still 44px minimum */
  @media (max-width: 380px) {
    .modal-header {
      padding: 14px 16px 10px;
    }

    h2 {
      font-size: 18px;
    }

    .close-button {
      width: 44px; /* NEVER below 44px for accessibility */
      height: 44px;
    }

    .close-button svg {
      width: 16px;
      height: 16px;
    }
  }
</style>
