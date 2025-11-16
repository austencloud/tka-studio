<!-- Toast.svelte - Temporary notification for save status -->
<script lang="ts">
  let { message = "", show = false, duration = 3000 } = $props<{
    message?: string;
    show?: boolean;
    duration?: number;
  }>();

  let timeoutId: ReturnType<typeof setTimeout> | null = null;
  let isVisible = $state(false);

  $effect(() => {
    if (show) {
      isVisible = true;
      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(() => {
        isVisible = false;
      }, duration);
    }

    return () => {
      if (timeoutId) clearTimeout(timeoutId);
    };
  });
</script>

{#if isVisible}
  <div class="toast" role="status" aria-live="polite">
    <i class="fas fa-check-circle"></i>
    <span>{message}</span>
  </div>
{/if}

<style>
  .toast {
    position: fixed;
    bottom: calc(env(safe-area-inset-bottom, 0px) + 80px);
    left: 50%;
    transform: translateX(-50%);
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 12px 20px;
    background: rgba(34, 197, 94, 0.95); /* Green success */
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 24px;
    color: white;
    font-size: 14px;
    font-weight: 500;
    box-shadow:
      0 4px 12px rgba(0, 0, 0, 0.3),
      0 2px 4px rgba(0, 0, 0, 0.2);
    z-index: 10000;
    pointer-events: none;
    animation: slideUp 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .toast i {
    font-size: 16px;
  }

  @keyframes slideUp {
    from {
      opacity: 0;
      transform: translateX(-50%) translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateX(-50%) translateY(0);
    }
  }

  /* Desktop positioning */
  @media (min-width: 769px) {
    .toast {
      bottom: 24px;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .toast {
      animation: none;
    }
  }
</style>
