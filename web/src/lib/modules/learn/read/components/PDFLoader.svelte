<!--
PDF Loader Component

Displays loading progress and status for PDF processing.
-->
<script lang="ts">
  import type { PDFLoadingState } from "../domain";
  import { LoadingSpinner } from "$shared/foundation/ui";

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

<div class="pdf-loader">
  {#if loadingState.isLoading}
    {#if isCacheLoading}
      <!-- Simple spinner for cached content -->
      <div class="cache-loading-container">
        <LoadingSpinner size="medium" message="Loading from cache..." />
      </div>
    {:else}
      <!-- Full progress loading for new content -->
      <div class="loading-container">
        <div class="loading-header">
          <h3>📖 Loading Your Book...</h3>
          <p class="loading-stage">{loadingState.stage}</p>
        </div>
        
        <div class="progress-container">
          <div class="progress-bar">
            <div 
              class="progress-fill" 
              style="width: {loadingState.progress}%"
            ></div>
          </div>
          <span class="progress-text">{Math.round(loadingState.progress)}%</span>
        </div>
        
        <div class="loading-animation">
          <div class="book-icon">📚</div>
          <div class="sparkles">✨</div>
        </div>
      </div>
    {/if}
  {:else if loadingState.error}
    <div class="error-container">
      <div class="error-icon">😞</div>
      <h3>Oops! Something went wrong</h3>
      <p class="error-message">{loadingState.error}</p>
      <button class="retry-button" onclick={() => window.location.reload()}>
        Try Again
      </button>
    </div>
  {:else}
    <div class="ready-container">
      <div class="ready-icon">📖</div>
      <p class="ready-message">{loadingState.stage}</p>
    </div>
  {/if}
</div>

<style>
  .pdf-loader {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    min-height: 300px;
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  }

  .loading-container,
  .cache-loading-container,
  .error-container,
  .ready-container {
    text-align: center;
    max-width: 400px;
  }

  .cache-loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }

  .loading-header h3 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
    font-size: 1.5rem;
  }

  .loading-stage {
    margin: 0 0 1.5rem 0;
    color: #7f8c8d;
    font-size: 1rem;
  }

  .progress-container {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 2rem;
  }

  .progress-bar {
    flex: 1;
    height: 8px;
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    overflow: hidden;
  }

  .progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #3498db, #2ecc71);
    border-radius: 4px;
    transition: width 0.3s ease;
  }

  .progress-text {
    font-weight: 600;
    color: #2c3e50;
    min-width: 40px;
  }

  .loading-animation {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 1rem;
    font-size: 2rem;
  }

  .book-icon {
    animation: bounce 2s infinite;
  }

  .sparkles {
    animation: sparkle 1.5s infinite;
  }

  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-10px);
    }
    60% {
      transform: translateY(-5px);
    }
  }

  @keyframes sparkle {
    0%, 100% {
      opacity: 0.3;
      transform: scale(0.8);
    }
    50% {
      opacity: 1;
      transform: scale(1.2);
    }
  }

  .error-container {
    color: #e74c3c;
  }

  .error-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .error-container h3 {
    margin: 0 0 1rem 0;
    color: #c0392b;
  }

  .error-message {
    margin: 0 0 1.5rem 0;
    color: #7f8c8d;
    font-size: 0.9rem;
  }

  .retry-button {
    background: #e74c3c;
    color: white;
    border: none;
    padding: 0.75rem 1.5rem;
    border-radius: 6px;
    cursor: pointer;
    font-size: 1rem;
    transition: background 0.2s ease;
  }

  .retry-button:hover {
    background: #c0392b;
  }

  .ready-container {
    color: #27ae60;
  }

  .ready-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }

  .ready-message {
    margin: 0;
    color: #2c3e50;
    font-size: 1.1rem;
  }
</style>