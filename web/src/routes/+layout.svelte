<script lang="ts">
  import type { Snippet } from "svelte";
  import { onMount, setContext } from "svelte";
  import "../app.css";
  import type { Container } from "inversify";
  import { container as inversifyContainer } from "../lib/services/inversify/container";

  interface Props {
    children: Snippet;
  }

  let { children }: Props = $props();

  // Application bootstrap
  let container: Container | null = $state(null);
  let isInitialized = $state(false);
  let initializationError = $state<string | null>(null);

  // Set context immediately (will be null initially)
  setContext("di-container", () => {
    return container;
  });

  onMount(async () => {
    try {
      // Clean up problematic sessionStorage values first
      const { cleanupSessionStorage } = await import(
        "$lib/utils/session-storage-cleanup"
      );
      cleanupSessionStorage();

      try {
        // Use InversifyJS container directly
        container = inversifyContainer;

        // Mark as initialized
        isInitialized = true;
      } catch (error) {
        console.error("❌ Failed to initialize application:", error);
        initializationError =
          error instanceof Error ? error.message : "Unknown error";
      }
    } catch (outerError) {
      console.error(
        "🚨 CRITICAL: Application initialization failed:",
        outerError
      );
      initializationError = "Critical initialization failure";
    }
  });
</script>

<svelte:head>
  <!-- Default title only if page doesn't set one -->
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
</svelte:head>

{#if initializationError}
  <div class="error-screen">
    <h1>Initialization Failed</h1>
    <p>{initializationError}</p>
    <button onclick={() => window.location.reload()}>Retry</button>
  </div>
{:else if !isInitialized}
  <div class="loading-screen">
    <div class="spinner"></div>
    <p>Initializing TKA...</p>
  </div>
{:else}
  <!-- Container is provided via context, children renders with access -->
  {@render children()}
{/if}

<style>
  .error-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
    text-align: center;
  }

  .loading-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    padding: 2rem;
    text-align: center;
  }

  .spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin-bottom: 1rem;
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
