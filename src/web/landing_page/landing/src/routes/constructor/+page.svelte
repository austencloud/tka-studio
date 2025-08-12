<script lang="ts">
  import { onMount } from 'svelte';
  import ConstructTab from '$lib/features/constructor/ConstructTab.svelte';

  let mounted = false;
  let constructorHeight = 'calc(100vh - 80px)'; // Default fallback

  onMount(() => {
    // Calculate the actual header height dynamically
    const header = document.querySelector('header') || document.querySelector('nav');
    if (header) {
      const headerHeight = header.offsetHeight;
      const padding = 20; // Small padding to ensure no overflow
      constructorHeight = `calc(100vh - ${headerHeight + padding}px)`;
      console.log('🎯 Constructor: Dynamic height calculated', {
        headerHeight,
        padding,
        constructorHeight,
        viewportHeight: window.innerHeight
      });
    } else {
      console.log('⚠️ Constructor: No header found, using default height', {
        constructorHeight,
        viewportHeight: window.innerHeight
      });
    }

    mounted = true;
  });
</script>

<svelte:head>
  <title>Kinetic Constructor - The Kinetic Alphabet</title>
  <meta name="description" content="The revolutionary Kinetic Constructor tool for creating, visualizing, and sharing flow arts sequences. Coming soon with advanced features for flow artists." />
</svelte:head>

<main class="constructor-page" style="--constructor-height: {constructorHeight}">
  {#if mounted}
    <div class="constructor-container">
      <ConstructTab />
    </div>
  {:else}
    <div class="loading">
      <p>Loading constructor...</p>
    </div>
  {/if}


</main>

<style>
  /* Override main layout padding for constructor page */
  :global(main) {
    padding: 0 !important;
  }

  .constructor-page {
    /* Full width section that respects navigation and footer */
    width: 100%;
    height: var(--constructor-height);
    background: transparent; /* Let the animated background show through */
    display: flex;
    flex-direction: column;
    margin: 0; /* Remove any default margins */
    padding: 0 2rem; /* Add horizontal padding for breathing room */
    box-sizing: border-box;
  }

  .constructor-container {
    flex: 1;
    width: 100%;
    height: 100%; /* Take full height of parent */
    overflow: hidden;
    background: transparent; /* Transparent to show beautiful starry background */
    border-radius: 1.5rem; /* Rounded edges for seamless integration */
    /* Removed backdrop-filter to let the starry night background show through */
    border: 1px solid rgba(255, 255, 255, 0.05); /* Very subtle border */
    /* Removed heavy box-shadow to avoid obscuring background */
  }

  .loading {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 400px;
    color: white;
    font-size: 1.2rem;
  }
</style>


