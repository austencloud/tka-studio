<!--
  ExportToast.svelte

  Toast notification for export completion (success or error).
  Auto-dismisses after 5 seconds.
-->
<script lang="ts">
  import { onMount } from "svelte";

  let {
    show = false,
    type = "success",
    message = "",
    onDismiss = () => {},
  }: {
    show?: boolean;
    type?: "success" | "error";
    message?: string;
    onDismiss?: () => void;
  } = $props();

  let timeout: ReturnType<typeof setTimeout> | null = null;

  // Auto-dismiss after 5 seconds
  $effect(() => {
    if (show) {
      if (timeout) clearTimeout(timeout);
      timeout = setTimeout(() => {
        onDismiss();
      }, 5000);
    }
    return () => {
      if (timeout) clearTimeout(timeout);
    };
  });
</script>

{#if show}
  <div class="toast-container">
    <div class="toast toast--{type}" role="alert" aria-live="polite">
      <div class="toast-icon">
        {#if type === "success"}
          <i class="fas fa-check-circle"></i>
        {:else}
          <i class="fas fa-exclamation-circle"></i>
        {/if}
      </div>
      <div class="toast-content">
        <div class="toast-title">
          {#if type === "success"}
            Export Complete
          {:else}
            Export Failed
          {/if}
        </div>
        <div class="toast-message">{message}</div>
      </div>
      <button
        class="toast-close"
        onclick={onDismiss}
        aria-label="Dismiss notification"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>
  </div>
{/if}

<style>
  .toast-container {
    position: fixed;
    bottom: 24px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 2000;
    pointer-events: none;
  }

  .toast {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 16px 20px;
    background: linear-gradient(
      135deg,
      rgba(30, 30, 40, 0.98),
      rgba(20, 20, 30, 0.98)
    );
    backdrop-filter: blur(20px);
    border-radius: 12px;
    min-width: 320px;
    max-width: 480px;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.5),
      0 0 0 1px rgba(255, 255, 255, 0.1);
    pointer-events: auto;
    animation: toast-slide-up 0.4s cubic-bezier(0.32, 0.72, 0, 1);
  }

  @keyframes toast-slide-up {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  .toast--success {
    border-left: 4px solid #10b981;
  }

  .toast--error {
    border-left: 4px solid #ef4444;
  }

  .toast-icon {
    font-size: 24px;
    flex-shrink: 0;
  }

  .toast--success .toast-icon {
    color: #10b981;
  }

  .toast--error .toast-icon {
    color: #ef4444;
  }

  .toast-content {
    flex: 1;
    min-width: 0;
  }

  .toast-title {
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    margin-bottom: 4px;
  }

  .toast-message {
    font-size: 13px;
    color: rgba(255, 255, 255, 0.7);
    line-height: 1.4;
  }

  .toast-close {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: none;
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.7);
    font-size: 14px;
    cursor: pointer;
    flex-shrink: 0;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .toast-close:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: scale(1.1);
  }

  .toast-close:active {
    transform: scale(0.95);
  }

  /* Mobile */
  @media (max-width: 768px) {
    .toast-container {
      bottom: 80px;
      left: 16px;
      right: 16px;
      transform: none;
    }

    .toast {
      min-width: auto;
      width: 100%;
    }
  }

  /* Reduced Motion */
  @media (prefers-reduced-motion: reduce) {
    .toast {
      animation: none;
    }

    .toast-close {
      transition: none;
    }

    .toast-close:hover {
      transform: none;
    }
  }
</style>
