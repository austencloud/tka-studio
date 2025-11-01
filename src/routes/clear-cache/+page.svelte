<script lang="ts">
  import { onMount } from 'svelte';
  import { clearAllFirebaseCache } from '$shared/auth';

  let status = $state('Ready to clear cache...');
  let cleared = $state(false);

  async function clearCache() {
    try {
      status = '🧹 Clearing all Firebase cache...';
      await clearAllFirebaseCache();
      status = '✅ Cache cleared successfully!';
      cleared = true;

      // Auto-redirect to home after 2 seconds
      setTimeout(() => {
        status = '🔄 Redirecting to home...';
        window.location.href = '/';
      }, 2000);
    } catch (error) {
      console.error('Cache clear error:', error);
      status = `❌ Error: ${error}`;
    }
  }

  onMount(() => {
    // Auto-clear on page load
    clearCache();
  });
</script>

<div class="clear-cache-page">
  <div class="container">
    <h1>🧹 Clearing Firebase Cache</h1>
    <p class="status">{status}</p>

    {#if cleared}
      <div class="success">
        <p>✅ All Firebase-related storage has been cleared:</p>
        <ul>
          <li>IndexedDB databases</li>
          <li>localStorage keys</li>
          <li>sessionStorage keys</li>
        </ul>
        <p>You will be redirected to the home page...</p>
      </div>
    {:else}
      <button onclick={clearCache} class="clear-button">
        Clear Cache Manually
      </button>
    {/if}
  </div>
</div>

<style>
  .clear-cache-page {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
  }

  .container {
    background: white;
    padding: 40px;
    border-radius: 12px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    max-width: 500px;
    width: 100%;
    text-align: center;
  }

  h1 {
    margin: 0 0 20px 0;
    color: #333;
    font-size: 28px;
  }

  .status {
    font-size: 18px;
    color: #666;
    margin: 20px 0;
    min-height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .success {
    background: #f0fdf4;
    border: 2px solid #86efac;
    border-radius: 8px;
    padding: 20px;
    margin: 20px 0;
  }

  .success ul {
    text-align: left;
    margin: 10px 0;
    padding-left: 20px;
  }

  .success li {
    margin: 5px 0;
    color: #166534;
  }

  .clear-button {
    background: #667eea;
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
  }

  .clear-button:hover {
    background: #5568d3;
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  .clear-button:active {
    transform: translateY(0);
  }
</style>
