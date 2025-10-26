<!--
CAPModalHeader.svelte - Modal header with centered title for CAP Selection Modal
Uses grid layout for perfect centering
-->
<script lang="ts">
  let {
    title,
    onClose
  } = $props<{
    title: string;
    onClose: () => void;
  }>();
</script>

<div class="cap-modal-header">
  <div class="header-spacer"></div>
  <h2 id="cap-title">{title}</h2>
  <button
    class="cap-modal-close-button"
    onclick={onClose}
    aria-label="Close CAP selection"
  >
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <line x1="18" y1="6" x2="6" y2="18"></line>
      <line x1="6" y1="6" x2="18" y2="18"></line>
    </svg>
  </button>
</div>

<style>
  .cap-modal-header {
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    gap: clamp(8px, 2cqw, 14px);
    flex-shrink: 0;
    min-height: 0;
  }

  .header-spacer {
    width: clamp(24px, 5cqw, 36px);
  }

  .cap-modal-header h2 {
    color: white;
    font-size: clamp(14px, 3.5cqi, 22px);
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    text-align: center;
    white-space: nowrap;
  }

  .cap-modal-close-button {
    background: rgba(0, 0, 0, 0.3);
    border: none;
    border-radius: clamp(10px, 2.5cqi, 14px);
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    padding: clamp(8px, 2cqi, 12px);
    width: clamp(40px, 7cqw, 52px);
    height: clamp(40px, 7cqw, 52px);
    flex-shrink: 0;
  }


  .cap-modal-close-button:hover {
    background: rgba(0, 0, 0, 0.5);
    transform: scale(1.05);
  }

  .cap-modal-close-button svg {
    width: 60%;
    height: 60%;
  }
</style>
