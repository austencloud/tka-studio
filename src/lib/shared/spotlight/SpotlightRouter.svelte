<script lang="ts">
  /**
   * SpotlightRouter
   * Domain: Spotlight Viewer Routing
   *
   * Responsibilities:
   * - Listen for URL-based spotlight route changes
   * - Manage spotlight viewer visibility
   * - Sync URL state with legacy spotlight state
   * - Render SpotlightViewer component
   */
  import { onMount } from "svelte";
  import SpotlightViewer from "../../modules/explore/spotlight/components/SpotlightViewer.svelte";
  import {
    closeSpotlightViewer,
    getShowSpotlight,
    getSpotlightSequence,
    getSpotlightThumbnailService,
  } from "../application/state/app-state.svelte";
  import type { RouteState } from "../navigation/utils/sheet-router";
  import {
    closeSpotlight,
    getCurrentSpotlight,
    onRouteChange,
  } from "../navigation/utils/sheet-router";

  // Legacy spotlight state (from global app state)
  let showSpotlight = $derived(getShowSpotlight());
  let spotlightSequence = $derived(getSpotlightSequence());
  let spotlightThumbnailService = $derived(getSpotlightThumbnailService());

  // Route-based spotlight state
  let spotlightSequenceId = $state<string | null>(null);

  onMount(() => {
    if (typeof window === "undefined") {
      return;
    }

    const cleanupFns: Array<() => void> = [];

    // Listen for route changes (spotlight, etc.)
    const cleanupRouteListener = onRouteChange((state: RouteState) => {
      spotlightSequenceId = state.spotlight || null;

      // Sync with legacy spotlight state if needed
      if (state.spotlight && !getShowSpotlight()) {
        // Route opened spotlight - SpotlightViewer will handle fetching
      } else if (!state.spotlight && getShowSpotlight()) {
        // Route closed spotlight
        closeSpotlightViewer();
      }
    });
    cleanupFns.push(cleanupRouteListener);

    // Initialize spotlight from URL on mount
    const initialSpotlight = getCurrentSpotlight();
    if (initialSpotlight) {
      spotlightSequenceId = initialSpotlight;
    }

    return () => {
      cleanupFns.forEach((cleanup) => {
        try {
          cleanup();
        } catch (error) {
          console.warn("Failed to clean up spotlight router:", error);
        }
      });
    };
  });

  function handleClose() {
    closeSpotlightViewer();
    if (spotlightSequenceId) {
      closeSpotlight();
    }
  }
</script>

<!-- Spotlight Viewer - rendered at root level for proper z-index -->
<!-- Route-aware: Opens via ?spotlight={id} or legacy showSpotlight state -->
{#if (showSpotlight && spotlightSequence && spotlightThumbnailService) || spotlightSequenceId}
  <SpotlightViewer
    show={showSpotlight || !!spotlightSequenceId}
    {...(spotlightSequence ? { sequence: spotlightSequence } : {})}
    {...(spotlightThumbnailService ? { thumbnailService: spotlightThumbnailService } : {})}
    onClose={handleClose}
  />
{/if}
