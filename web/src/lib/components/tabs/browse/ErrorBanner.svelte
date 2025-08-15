<script lang="ts">
  import { slide } from "svelte/transition";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    show = false,
    message = "",
    onDismiss = () => {},
  } = $props<{
    show?: boolean;
    message?: string;
    onDismiss?: () => void;
  }>();
</script>

<!-- Error banner -->
{#if show}
  <div class="error-banner" transition:slide>
    <div class="error-content">
      <span class="error-message">{message}</span>
      <button class="error-dismiss" onclick={onDismiss}>✕</button>
    </div>
  </div>
{/if}

<style>
  .error-banner {
    flex-shrink: 0;
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 8px;
    margin: var(--spacing-md);
    padding: var(--spacing-md);
    z-index: 100;
  }

  .error-content {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: var(--spacing-md);
  }

  .error-message {
    color: #dc2626;
    font-weight: 500;
    flex: 1;
  }

  .error-dismiss {
    background: none;
    border: none;
    color: #dc2626;
    font-size: 1.2rem;
    cursor: pointer;
    padding: var(--spacing-xs);
    border-radius: 4px;
    transition: background-color 0.2s;
  }

  .error-dismiss:hover {
    background: rgba(239, 68, 68, 0.1);
  }
</style>
