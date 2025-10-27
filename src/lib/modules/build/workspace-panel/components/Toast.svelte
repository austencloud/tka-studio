<!--
Toast.svelte - Simple toast notification for validation messages

Shows at the bottom center of screen, auto-dismisses after 3 seconds
-->
<script lang="ts">
  // Props
  const {
    message = "",
    onDismiss
  } = $props<{
    message: string;
    onDismiss?: () => void;
  }>();
</script>

{#if message}
  <div class="toast-container">
    <div class="toast" role="alert">
      <i class="fas fa-exclamation-circle"></i>
      <span class="toast-message">{message}</span>
      {#if onDismiss}
        <button
          class="toast-close"
          onclick={onDismiss}
          type="button"
          aria-label="Dismiss"
        >
          <i class="fas fa-times"></i>
        </button>
      {/if}
    </div>
  </div>
{/if}

<style>
  .toast-container {
    position: fixed;
    bottom: 80px; /* Above the button panel */
    left: 50%;
    transform: translateX(-50%);
    z-index: 1000;
    pointer-events: none;
  }

  .toast {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    padding: var(--spacing-md) var(--spacing-lg);
    background: hsl(var(--destructive));
    color: hsl(var(--destructive-foreground));
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
    pointer-events: auto;
    animation: slide-up 0.3s ease-out;
    min-width: 280px;
    max-width: 90vw;
  }

  @keyframes slide-up {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .toast-message {
    flex: 1;
    font-size: var(--font-size-sm);
    font-weight: 500;
  }

  .toast-close {
    background: none;
    border: none;
    color: inherit;
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: 4px;
    transition: background 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 24px;
    min-height: 24px;
  }

  .toast-close:hover {
    background: rgba(255, 255, 255, 0.2);
  }

  .toast-close:active {
    background: rgba(255, 255, 255, 0.3);
  }

  /* Mobile adjustments */
  @media (max-width: 768px) {
    .toast-container {
      bottom: 70px;
      left: var(--spacing-md);
      right: var(--spacing-md);
      transform: none;
    }

    .toast {
      min-width: auto;
      max-width: none;
    }

    .toast-message {
      font-size: var(--font-size-xs);
    }
  }
</style>
