<!-- ErrorState.svelte - Error state component for StartPositionPicker -->
<script lang="ts">
  const {
    hasRefreshButton = true,
    message = "Unable to load start positions. Please try refreshing the page.",
    onRefresh = () => {
      if (typeof window !== "undefined") window.location.reload();
    },
  } = $props<{
    hasRefreshButton?: boolean;
    message?: string;
    onRefresh?: () => void;
  }>();
</script>

<div class="error-container">
  <p>{message}</p>
  {#if hasRefreshButton}
    <button class="refresh-button" onclick={onRefresh}> Refresh </button>
  {/if}
</div>

<style>
  .error-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: var(--spacing-xl);
    color: var(--foreground);
  }

  .error-container p {
    margin-bottom: var(--spacing-md);
    font-size: 1rem;
  }

  .refresh-button {
    margin-top: 15px;
    padding: 10px 20px;
    background: var(--primary);
    color: var(--primary-foreground);
    border: none;
    border-radius: var(--border-radius);
    cursor: pointer;
    font-size: 1rem;
  }

  .refresh-button:hover {
    background: var(--primary-hover, var(--primary));
    opacity: 0.9;
  }
</style>
