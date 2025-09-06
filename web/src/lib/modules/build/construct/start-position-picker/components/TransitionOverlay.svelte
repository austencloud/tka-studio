<!-- TransitionOverlay.svelte - Loading overlay during transitions -->
<div class="loading-overlay">
  <div class="loading-spinner"></div>
  <p>Loading options...</p>
</div>

<style>
  .loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(
      255,
      255,
      255,
      0.8
    ); /* Semi-transparent instead of solid white */
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    opacity: 0;
    animation: fadeIn 0.1s ease-in forwards; /* Quick fade in */
  }

  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--border, #e2e8f0);
    border-top: 3px solid var(--primary, #3b82f6);
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 12px;
  }

  p {
    margin: 0;
    color: var(--foreground, #1f2937);
    font-size: 0.9rem;
    font-weight: 500;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  @keyframes spin {
    0% {
      transform: rotate(0deg);
    }
    100% {
      transform: rotate(360deg);
    }
  }
</style>
