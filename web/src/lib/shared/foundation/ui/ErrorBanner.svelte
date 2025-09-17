<script lang="ts">
  import { slide } from "svelte/transition";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    show = false,
    message = "",
    type = "error",
    dismissible = true,
    onDismiss = () => {},
    onRetry = null,
  } = $props<{
    show?: boolean;
    message?: string;
    type?: "error" | "warning" | "info";
    dismissible?: boolean;
    onDismiss?: () => void;
    onRetry?: (() => void) | null;
  }>();

  // ✅ PURE RUNES: Derived state for icon selection
  const icon = $derived(() => {
    switch (type) {
      case "error":
        return "❌";
      case "warning":
        return "⚠️";
      case "info":
        return "ℹ️";
      default:
        return "❌";
    }
  });

  // ✅ PURE RUNES: Derived state for styling
  const bannerClass = $derived(() => {
    const baseClass = "error-banner";
    return `${baseClass} ${baseClass}--${type}`;
  });
</script>

{#if show}
  <div class={bannerClass} transition:slide={{ duration: 300 }}>
    <div class="error-banner__content">
      <span class="error-banner__icon">{icon()}</span>
      <span class="error-banner__message">{message}</span>
    </div>

    <div class="error-banner__actions">
      {#if onRetry}
        <button class="error-banner__button error-banner__button--retry" onclick={onRetry}>
          🔄 Retry
        </button>
      {/if}

      {#if dismissible}
        <button class="error-banner__button error-banner__button--dismiss" onclick={onDismiss}>
          ✕
        </button>
      {/if}
    </div>
  </div>
{/if}

<style>
  .error-banner {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--spacing-md);
    margin-bottom: var(--spacing-md);
    border-radius: 8px;
    border: 1px solid;
    background: var(--surface-glass);
    backdrop-filter: var(--glass-backdrop);
    box-shadow: var(--shadow-sm);
    font-size: var(--font-size-sm);
    line-height: 1.4;
  }

  .error-banner--error {
    border-color: rgba(239, 68, 68, 0.5);
    background: rgba(239, 68, 68, 0.1);
    color: #fca5a5;
  }

  .error-banner--warning {
    border-color: rgba(245, 158, 11, 0.5);
    background: rgba(245, 158, 11, 0.1);
    color: #fbbf24;
  }

  .error-banner--info {
    border-color: rgba(59, 130, 246, 0.5);
    background: rgba(59, 130, 246, 0.1);
    color: #93c5fd;
  }

  .error-banner__content {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    flex: 1;
  }

  .error-banner__icon {
    flex-shrink: 0;
    font-size: 1.1em;
  }

  .error-banner__message {
    flex: 1;
    word-break: break-word;
  }

  .error-banner__actions {
    display: flex;
    align-items: center;
    gap: var(--spacing-sm);
    flex-shrink: 0;
  }

  .error-banner__button {
    padding: var(--spacing-xs) var(--spacing-sm);
    border: none;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.1);
    color: inherit;
    cursor: pointer;
    transition: all var(--transition-fast);
    font-size: var(--font-size-xs);
    line-height: 1;
  }

  .error-banner__button:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-1px);
  }

  .error-banner__button--retry {
    background: rgba(34, 197, 94, 0.2);
    border: 1px solid rgba(34, 197, 94, 0.3);
  }

  .error-banner__button--retry:hover {
    background: rgba(34, 197, 94, 0.3);
  }

  .error-banner__button--dismiss {
    background: rgba(239, 68, 68, 0.2);
    border: 1px solid rgba(239, 68, 68, 0.3);
    min-width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .error-banner__button--dismiss:hover {
    background: rgba(239, 68, 68, 0.3);
  }
</style>
