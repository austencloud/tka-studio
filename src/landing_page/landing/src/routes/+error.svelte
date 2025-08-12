<script lang="ts">
  import { page } from '$app/stores';
  import { onMount } from 'svelte';

  let mounted = false;

  onMount(() => {
    mounted = true;
  });

  $: status = ($page.error as any)?.status || 500;
  $: message = $page.error?.message || 'Something went wrong';
</script>

<svelte:head>
  <title>Error {status} - The Kinetic Alphabet</title>
  <meta name="description" content="An error occurred while loading the page." />
</svelte:head>

<div class="error-container" class:mounted>
  <div class="error-content">
    <div class="error-icon">
      {#if status === 404}
        🔍
      {:else if status >= 500}
        ⚠️
      {:else}
        ❌
      {/if}
    </div>

    <h1 class="error-title">
      {#if status === 404}
        Page Not Found
      {:else if status >= 500}
        Server Error
      {:else}
        Error {status}
      {/if}
    </h1>

    <p class="error-message">
      {#if status === 404}
        The page you're looking for doesn't exist or has been moved.
      {:else if status >= 500}
        We're experiencing technical difficulties. Please try again later.
      {:else}
        {message}
      {/if}
    </p>

    <div class="error-actions">
      <a href="/" class="btn btn-primary">Go Home</a>
      <button
        class="btn btn-secondary"
        on:click={() => window.history.back()}
      >
        Go Back
      </button>
    </div>

    {#if status === 404}
      <div class="suggestions">
        <h3>You might be looking for:</h3>
        <ul>
          <li><a href="/">Home</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact</a></li>
        </ul>
      </div>
    {/if}
  </div>
</div>

<style>
  .error-container {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-lg);
    background: var(--background-color); /* Transparent to show dynamic backgrounds */
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.6s ease;
  }

  .error-container.mounted {
    opacity: 1;
    transform: translateY(0);
  }

  .error-content {
    text-align: center;
    max-width: 500px;

    /* Advanced glassmorphism styling */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop-strong);
    -webkit-backdrop-filter: var(--glass-backdrop-strong);
    border: var(--glass-border);
    padding: var(--spacing-3xl);
    border-radius: var(--border-radius-lg);
    box-shadow: var(--shadow-glass-hover);

  }

  .error-icon {
    font-size: 4rem;
    margin-bottom: var(--spacing-lg);
  }

  .error-title {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-3xl);
  }

  .error-message {
    color: var(--text-secondary);
    margin-bottom: var(--spacing-2xl);
    font-size: var(--font-size-lg);
    line-height: 1.6;
  }

  .error-actions {
    display: flex;
    gap: var(--spacing-md);
    justify-content: center;
    margin-bottom: var(--spacing-xl);
  }

  .btn {
    /* Use global glassmorphism button styling */
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-sm) var(--spacing-lg);
    border: var(--glass-border);
    border-radius: var(--border-radius-lg);
    font-family: inherit;
    font-size: var(--font-size-base);
    font-weight: 600;
    text-decoration: none;
    cursor: pointer;
    position: relative;
    overflow: hidden;

    /* Glassmorphism styling */
    background: var(--surface-color);
    backdrop-filter: var(--glass-backdrop);
    -webkit-backdrop-filter: var(--glass-backdrop);
    color: var(--text-color);
    box-shadow: var(--shadow-glass);

    /* Enhanced transitions */
    transition: all var(--transition-normal);
    will-change: transform, box-shadow, background;
  }

  .btn-primary {
    /* Clean primary button glassmorphism styling */
    background: var(--primary-color);
    color: var(--text-inverse);
    box-shadow: var(--shadow-glass);
  }

  .btn-primary:hover {
    background: var(--primary-light);
    transform: translateY(-2px);
    box-shadow: var(--shadow-glass-hover);
  }

  .btn-secondary {
    background: var(--surface-glass);
    color: var(--text-color);
    border: var(--glass-border-hover);
  }

  .btn-secondary:hover {
    background: var(--surface-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-glass-hover);
  }

  .suggestions {
    margin-top: var(--spacing-xl);
    padding-top: var(--spacing-xl);
    border-top: 1px solid var(--border-color);
  }

  .suggestions h3 {
    color: var(--text-color);
    margin-bottom: var(--spacing-md);
    font-size: var(--font-size-lg);
  }

  .suggestions ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  .suggestions li {
    margin: var(--spacing-sm) 0;
  }

  .suggestions a {
    color: var(--primary-color);
    text-decoration: none;
    font-weight: 500;
  }

  .suggestions a:hover {
    text-decoration: underline;
  }

  @media (max-width: 768px) {
    .error-content {
      padding: var(--spacing-2xl);
      margin: var(--spacing-md);
    }

    .error-actions {
      flex-direction: column;
    }

    .btn {
      width: 100%;
    }
  }
</style>
