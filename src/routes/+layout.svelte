<script lang="ts">
  import FullscreenPrompt from "$lib/shared/components/FullscreenPrompt.svelte";
  import type { Container } from "inversify";
  import type { Snippet } from "svelte";
  import { onMount, setContext } from "svelte";
  import { authStore } from "$shared/auth";
  import { registerCacheClearShortcut } from "$lib/shared/utils/cache-buster";
  import { setupHMRHelpers } from "$lib/shared/dev/hmr-helper";
  import "../app.css";

  let { children } = $props<{
    children: Snippet;
  }>();

  // Application bootstrap - simplified to just DI container setup
  let container: Container | null = $state(null);
  let containerError = $state<string | null>(null);

  // Set context immediately (will be null initially)
  setContext("di-container", () => {
    return container;
  });

  // HMR support - re-initialize container when modules are hot-reloaded
  if (import.meta.hot) {
    import.meta.hot.accept(async () => {
      try {
        // CRITICAL: Wait for next frame before resetting container
        // This ensures Chrome DevTools mobile emulation dimensions are stable
        await new Promise(resolve => requestAnimationFrame(() => resolve(undefined)));

        const { getContainer, resetContainer } = await import("$shared");
        resetContainer();
        container = await getContainer();
      } catch (error) {
        console.error("❌ HMR: Failed to re-initialize container:", error);
        containerError = "HMR container re-initialization failed";
      }
    });
  }

  // Reactive viewport height tracking using Svelte 5 runes
  let viewportHeight = $state(0);

  // Update viewport height on window resize and visualViewport changes
  function updateViewportHeight() {
    if (typeof window !== "undefined") {
      // Use visualViewport for accurate height that accounts for browser chrome
      const height = window.visualViewport?.height ?? window.innerHeight;
      viewportHeight = height;
      // Update CSS custom property for use throughout the app
      document.documentElement.style.setProperty(
        "--viewport-height",
        `${height}px`
      );
    }
  }

  onMount(() => {
    // Register cache clear shortcut (Ctrl+Shift+Delete)
    registerCacheClearShortcut();

    // Setup HMR development helpers (Ctrl+Shift+R for hard reload)
    setupHMRHelpers();

    // REMOVED: checkAndClearIfBroken() - it was causing infinite reload loops in mobile emulation
    // Use ?clear-cache URL parameter or Ctrl+Shift+Delete instead

    // Async initialization
    (async () => {
      // Initialize Firebase Auth listener (handles redirect result)
      await authStore.initialize();

      try {
        // Dynamically import container only on client-side to avoid SSR issues
        const { getContainer, resetContainer } = await import("$shared");

        // HMR support - reset container if it's stale
        if (import.meta.hot) {
          resetContainer();
        }

        // Set up DI container - this automatically caches it
        container = await getContainer();

        // Initialize glyph cache for faster preview rendering
        const { TYPES } = await import("$shared/inversify/types");
        type IGlyphCacheService = { initialize: () => Promise<void> };
        const glyphCache = container.get<IGlyphCacheService>(
          TYPES.IGlyphCacheService
        );
        glyphCache.initialize().catch((error: unknown) => {
          console.warn("⚠️ Glyph cache initialization failed:", error);
        });

        // Set up viewport height tracking
        updateViewportHeight(); // Initial calculation

        // Listen to visualViewport resize (more reliable than window resize for mobile)
        if (window.visualViewport) {
          window.visualViewport.addEventListener(
            "resize",
            updateViewportHeight
          );
          window.visualViewport.addEventListener(
            "scroll",
            updateViewportHeight
          );
        }

        // Fallback to window resize for browsers that don't support visualViewport
        window.addEventListener("resize", updateViewportHeight);
      } catch (error) {
        console.error("❌ Root layout: Failed to set up DI container:", error);
        containerError =
          error instanceof Error ? error.message : "Container setup failed";
      }
    })();

    // Return synchronous cleanup function
    return () => {
      // Clean up auth listener
      authStore.cleanup();

      if (window.visualViewport) {
        window.visualViewport.removeEventListener(
          "resize",
          updateViewportHeight
        );
        window.visualViewport.removeEventListener(
          "scroll",
          updateViewportHeight
        );
      }
      window.removeEventListener("resize", updateViewportHeight);
    };
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

  <!-- Fullscreen prompt for extreme constraints -->
  <FullscreenPrompt />
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
