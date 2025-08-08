<script>
  export let size = 'medium'; // 'small', 'medium', 'large'
  export let message = 'Loading...';
  export let showMessage = true;
</script>

<div class="loading-container" class:small={size === 'small'} class:large={size === 'large'}>
  <div class="spinner"></div>
  {#if showMessage}
    <p class="loading-message">{message}</p>
  {/if}
</div>

<style>
  .loading-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  .small .spinner {
    width: 20px;
    height: 20px;
    border-width: 2px;
  }

  .large .spinner {
    width: 60px;
    height: 60px;
    border-width: 4px;
  }

  .loading-message {
    margin-top: 1rem;
    color: #666;
    font-size: 0.9rem;
  }

  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
  }
</style>
