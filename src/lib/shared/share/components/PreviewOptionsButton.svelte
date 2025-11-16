<!-- PreviewOptionsButton.svelte - Button to open preview and options drawer -->
<script lang="ts">
  let {
    canShare = false,
    onClick,
  }: {
    canShare?: boolean;
    onClick?: () => void;
  } = $props();
</script>

<button class="preview-options-button" onclick={onClick} disabled={!canShare}>
  <i class="fas fa-eye"></i>
  <span>Preview & Options</span>
  <i class="fas fa-chevron-right"></i>
</button>

<style>
  .preview-options-button {
    width: 100%;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 16px 20px;
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.12),
      rgba(37, 99, 235, 0.08)
    );
    border: 1.5px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    color: rgba(255, 255, 255, 0.95);
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
  }

  .preview-options-button:hover:not(:disabled) {
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.18),
      rgba(37, 99, 235, 0.12)
    );
    border-color: rgba(59, 130, 246, 0.4);
    transform: translateY(-1px);
  }

  .preview-options-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
    transform: none !important;
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .preview-options-button {
      transition-duration: 0.01ms !important;
    }

    .preview-options-button:hover {
      transform: none !important;
    }
  }
</style>
