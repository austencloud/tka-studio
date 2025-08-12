<script lang="ts">
  export let size: 'small' | 'medium' | 'large' = 'medium';
  export let text: string = 'Loading...';
  export let fullscreen: boolean = false;
</script>

<div class="loading-container" class:fullscreen>
  <div class="loading-content">
    <div class="spinner" class:small={size === 'small'} class:large={size === 'large'}>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
      <div class="spinner-ring"></div>
    </div>
    {#if text}
      <p class="loading-text">{text}</p>
    {/if}
  </div>
</div>

<style>
  .loading-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
  }
  
  .loading-container.fullscreen {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(255, 255, 255, 0.9);
    z-index: 9999;
    backdrop-filter: blur(2px);
  }
  
  .loading-content {
    text-align: center;
  }
  
  .spinner {
    position: relative;
    width: 60px;
    height: 60px;
    margin: 0 auto var(--spacing-md) auto;
  }
  
  .spinner.small {
    width: 30px;
    height: 30px;
  }
  
  .spinner.large {
    width: 80px;
    height: 80px;
  }
  
  .spinner-ring {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: 3px solid transparent;
    border-top-color: var(--primary-color);
    border-radius: 50%;
    animation: spin 1.2s linear infinite;
  }
  
  .spinner-ring:nth-child(2) {
    border-top-color: var(--secondary-color);
    animation-duration: 1.8s;
    animation-direction: reverse;
    width: 80%;
    height: 80%;
    top: 10%;
    left: 10%;
  }
  
  .spinner-ring:nth-child(3) {
    border-top-color: var(--accent-color);
    animation-duration: 2.4s;
    width: 60%;
    height: 60%;
    top: 20%;
    left: 20%;
  }
  
  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }
  
  .loading-text {
    color: var(--text-secondary);
    font-size: var(--font-size-base);
    margin: 0;
    animation: pulse 1.5s ease-in-out infinite;
  }
  
  @keyframes pulse {
    0%, 100% {
      opacity: 0.7;
    }
    50% {
      opacity: 1;
    }
  }
  
  /* Dark mode support */
  @media (prefers-color-scheme: dark) {
    .loading-container.fullscreen {
      background: rgba(0, 0, 0, 0.8);
    }
  }
</style>
