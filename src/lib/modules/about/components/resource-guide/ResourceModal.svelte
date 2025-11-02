<script lang="ts">
  import { createFocusTrap } from "$lib/shared/settings/utils/focus-trap.svelte";
  import { useScrollLock } from "$lib/shared/ui/utils/scroll-lock.svelte";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import RelatedResourcesPanel from "./RelatedResourcesPanel.svelte";
  import ResourceModalCloseButton from "./ResourceModalCloseButton.svelte";
  import ResourceModalFooter from "./ResourceModalFooter.svelte";
  import ResourceModalHeader from "./ResourceModalHeader.svelte";
  import ResourceModalNavigation from "./ResourceModalNavigation.svelte";
  import type { ResourceModalData } from "./types";

  let {
    isOpen = false,
    onClose = () => {},
    modalData = null,
    children,
  } = $props<{
    isOpen?: boolean;
    onClose?: () => void;
    modalData?: ResourceModalData | null;
    children?: any;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // DOM element references
  let modalContainer: HTMLElement | undefined = $state();
  let modalContent: HTMLElement | undefined = $state();
  let closeButton: HTMLButtonElement | undefined = $state();

  // State
  let previouslyFocusedElement: HTMLElement | null = null;

  // Derived data from props
  const data = $derived(modalData);
  const loading = $derived(false);

  // Handle close with haptic feedback
  function handleClose() {
    hapticService?.trigger("selection");
    onClose();
  }

  // Handle navigation with haptic feedback
  function handleNavigate() {
    hapticService?.trigger("selection");
  }

  // Handle backdrop click
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === modalContainer) {
      handleClose();
    }
  }

  // Handle modal state changes with $effect
  $effect(() => {
    if (isOpen) {
      // Store previously focused element
      if (typeof document !== "undefined") {
        previouslyFocusedElement = document.activeElement as HTMLElement;

        // Focus the close button after a brief delay
        setTimeout(() => {
          if (closeButton) {
            closeButton.focus();
          }
        }, 100);
      }

      // Set up focus trap
      if (modalContent) {
        const focusTrap = createFocusTrap({
          container: modalContent,
          onEscape: handleClose,
          autoFocus: false, // We handle focus manually above
        });

        return () => {
          focusTrap.cleanup();

          // Restore focus
          if (previouslyFocusedElement) {
            previouslyFocusedElement.focus();
          }
        };
      }
    }
    return undefined;
  });

  // Use scroll lock utility
  $effect(() => {
    return useScrollLock(isOpen);
  });
</script>

{#if isOpen}
  <!-- Modal Overlay -->
  <div
    class="modal-overlay"
    bind:this={modalContainer}
    onclick={handleBackdropClick}
    onkeydown={(e) =>
      e.key === "Enter" && handleBackdropClick(e as unknown as MouseEvent)}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    aria-describedby="modal-description"
    tabindex="-1"
  >
    <!-- Modal Container -->
    <div class="modal-container" bind:this={modalContent}>
      {#if closeButton !== undefined}
        <ResourceModalCloseButton
          onClose={handleClose}
          bind:buttonRef={closeButton}
        />
      {/if}

      {#if loading}
        <!-- Loading State -->
        <div class="modal-loading">
          <div class="loading-spinner"></div>
          <p>Loading resource...</p>
        </div>
      {:else if data}
        <!-- Resource Content -->
        <div class="resource-content">
          <ResourceModalHeader
            title={data.title}
            subtitle={data.subtitle}
            creator={data.creator}
            creatorColor={data.creatorColor}
            category={data.category}
            level={data.level}
            heroGradient={data.heroGradient}
          />

          <ResourceModalNavigation
            sections={data.tableOfContents}
            onNavigate={handleNavigate}
          />

          <!-- Main Content -->
          <main class="resource-main" id="modal-description">
            {@render children?.()}
          </main>

          <RelatedResourcesPanel
            resources={data.relatedResources}
            onNavigate={handleNavigate}
          />

          <ResourceModalFooter url={data.url} onNavigate={handleNavigate} />
        </div>
      {:else}
        <!-- No Data State -->
        <div class="modal-error">
          <h2>Resource Not Found</h2>
          <p>The requested resource could not be loaded.</p>
        </div>
      {/if}
    </div>
  </div>
{/if}

<style>
  /* Modal Overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    z-index: 1000;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: var(--spacing-lg);
    animation: fadeIn 0.3s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  /* Modal Container */
  .modal-container {
    background: var(--surface-color);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: var(--border-radius-lg);
    max-width: 900px;
    max-height: 90vh;
    width: 100%;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    animation: slideIn 0.3s ease-out;
  }

  @keyframes slideIn {
    from {
      opacity: 0;
      transform: translateY(-50px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }

  /* Loading State */
  .modal-loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-3xl);
    gap: var(--spacing-lg);
    color: var(--text-color);
  }

  .loading-spinner {
    width: 40px;
    height: 40px;
    border: 3px solid rgba(255, 255, 255, 0.1);
    border-top: 3px solid var(--primary-color);
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  /* Resource Content */
  .resource-content {
    display: flex;
    flex-direction: column;
    height: 100%;
    max-height: 90vh;
  }

  /* Main Content */
  .resource-main {
    flex: 1;
    overflow-y: auto;
    padding: var(--spacing-xl);
  }

  /* Error State */
  .modal-error {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--spacing-3xl);
    text-align: center;
    color: var(--text-color);
  }

  .modal-error h2 {
    margin-bottom: var(--spacing-md);
    color: var(--text-color);
  }

  /* Mobile Responsive */
  @media (max-width: 768px) {
    .modal-overlay {
      padding: var(--spacing-md);
    }

    .modal-container {
      max-height: 95vh;
    }

    .resource-main {
      padding: var(--spacing-md);
    }
  }

  /* Reduced motion support */
  @media (prefers-reduced-motion: reduce) {
    .modal-overlay,
    .modal-container {
      animation: none;
      transition: none;
    }

    .loading-spinner {
      animation: none;
    }
  }
</style>
