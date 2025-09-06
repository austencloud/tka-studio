<script lang="ts">
  import type { Container } from "inversify";
  import type { Snippet } from "svelte";
  import { onMount, setContext } from "svelte";
  import "../app.css";

  interface Props {
    children: Snippet;
  }

  let { children }: Props = $props();

  // Application bootstrap - simplified to just DI container setup
  let container: Container | null = $state(null);
  let containerError = $state<string | null>(null);

  // Set context immediately (will be null initially)
  setContext("di-container", () => {
    return container;
  });

  onMount(async () => {
    console.log("🚀 Root layout: Setting up DI container only");
    try {
      // Clean up problematic sessionStorage values first
      const { cleanupSessionStorage } = await import(
        "$lib/shared/utils/session-storage-cleanup"
      );
      cleanupSessionStorage();

      // Dynamically import container only on client-side to avoid SSR issues
      const { container: inversifyContainer } = await import(
        "$lib/shared/inversify/container"
      );

      // Set up DI container - this is all we need at root level
      container = inversifyContainer;
      console.log(
        "✅ Root layout: DI container ready, handing off to MainApplication"
      );
    } catch (error) {
      console.error("❌ Root layout: Failed to set up DI container:", error);
      containerError =
        error instanceof Error ? error.message : "Container setup failed";
    }
  });
</script>

<svelte:head>
  <!-- Default title only if page doesn't set one -->
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width" />
</svelte:head>

{#if containerError}
  <div class="error-screen">
    <h1>Critical Error</h1>
    <p>{containerError}</p>
    <button onclick={() => window.location.reload()}>Retry</button>
  </div>
{:else if container}
  <!-- Only render children when container is ready -->
  {@render children()}
{:else}
  <!-- Brief loading while container sets up -->
  <div class="error-screen">
    <p>Setting up services...</p>
  </div>
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
</style>
