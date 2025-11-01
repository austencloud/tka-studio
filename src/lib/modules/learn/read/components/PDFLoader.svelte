<!--
PDF Loader Component

Displays loading progress and status for PDF processing.
-->
<script lang="ts">
  import type { PDFLoadingState } from "../domain";
  import type { IHapticFeedbackService } from "$shared";
  import { SkeletonLoader } from "$shared/foundation/ui";
  import { resolve, TYPES } from "$shared";

  // Services
  let hapticService: IHapticFeedbackService;

  // Initialize haptic service
  $effect(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  const { loadingState } = $props<{
    loadingState: PDFLoadingState;
  }>();

  // Check if this is a simple cache loading (no progress tracking needed)
  const isCacheLoading = $derived(
    loadingState.isLoading &&
      loadingState.stage === "Loading from cache..." &&
      loadingState.progress === 0
  );
</script>

{#if loadingState.isLoading}
  <!-- Modern skeleton loading - shows the structure while content loads -->
  <div class="pdf-skeleton">
    <div class="skeleton-header">
      <SkeletonLoader variant="text" width="60%" height="1.5rem" />
      <SkeletonLoader variant="text" width="40%" height="1rem" />
    </div>
    <div class="skeleton-content">
      <SkeletonLoader variant="card" height="600px" />
    </div>
    {#if !isCacheLoading}
      <div class="loading-hint">
        <span class="stage-text">{loadingState.stage}</span>
      </div>
    {/if}
  </div>
{:else if loadingState.error}
  <div class="error-container">
    <h3>Unable to load PDF</h3>
    <p class="error-message">{loadingState.error}</p>
    <button
      class="retry-button"
      onclick={() => {
        // Trigger selection haptic for retry action
        hapticService?.trigger("selection");
        window.location.reload();
      }}
    >
      Try Again
    </button>
  </div>
{/if}

<style>
  .pdf-skeleton {
    padding: var(--spacing-lg);
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .skeleton-header {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-md);
  }

  .skeleton-content {
    width: 100%;
  }

  .loading-hint {
    text-align: center;
    margin-top: var(--spacing-md);
  }

  .stage-text {
    font-size: var(--font-size-sm);
    color: var(--muted-foreground);
    opacity: 0.7;
  }

  .error-container {
    padding: var(--spacing-xl);
    text-align: center;
    max-width: 400px;
    margin: 0 auto;
  }

  .error-container h3 {
    margin: 0 0 var(--spacing-md) 0;
    color: var(--destructive);
    font-size: var(--font-size-xl);
  }

  .error-message {
    margin: 0 0 var(--spacing-lg) 0;
    color: var(--muted-foreground);
    font-size: var(--font-size-sm);
  }

  .retry-button {
    background: var(--destructive);
    color: white;
    border: none;
    padding: var(--spacing-md) var(--spacing-xl);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: var(--font-size-base);
    transition: opacity 0.2s ease;
  }

  .retry-button:hover {
    opacity: 0.9;
  }

  .retry-button:active {
    transform: scale(0.98);
  }
</style>
