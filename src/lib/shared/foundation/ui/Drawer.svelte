<!--
  Drawer.svelte - Wrapper around vaul-svelte with backward-compatible API

  Provides the same API as the old BottomSheet component for easy migration.
  Built on vaul-svelte for improved gesture handling and accessibility.
-->
<script lang="ts">
  import { Drawer as VaulDrawer } from "vaul-svelte";
  import { createEventDispatcher } from "svelte";

  type CloseReason = "backdrop" | "escape" | "programmatic";

  let {
    isOpen = $bindable(false),
    closeOnBackdrop = true,
    closeOnEscape = true,
    focusTrap = true,
    lockScroll = true,
    labelledBy,
    ariaLabel,
    role = "dialog",
    showHandle = true,
    class: drawerClass = "",
    backdropClass = "",
    placement = "bottom",
    children,
  } = $props<{
    isOpen?: boolean;
    closeOnBackdrop?: boolean;
    closeOnEscape?: boolean;
    focusTrap?: boolean;
    lockScroll?: boolean;
    labelledBy?: string;
    ariaLabel?: string;
    role?: "dialog" | "menu" | "listbox" | "alertdialog";
    showHandle?: boolean;
    class?: string;
    backdropClass?: string;
    placement?: "bottom" | "top" | "right" | "left";
    children?: () => unknown;
  }>();

  const dispatch = createEventDispatcher<{
    close: { reason: CloseReason };
  }>();

  let lastOpenState = false;

  function handleOpenChange(open: boolean) {
    isOpen = open;

    // Emit close event when drawer closes
    if (lastOpenState && !open) {
      dispatch("close", { reason: "programmatic" });
    }

    lastOpenState = open;
  }

  function handleBackdropClick() {
    if (closeOnBackdrop) {
      dispatch("close", { reason: "backdrop" });
      isOpen = false;
    }
  }

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape" && closeOnEscape && isOpen) {
      event.preventDefault();
      dispatch("close", { reason: "escape" });
      isOpen = false;
    }
  }
</script>

<svelte:window onkeydown={handleKeydown} />

<VaulDrawer.Root
  open={isOpen}
  onOpenChange={handleOpenChange}
  dismissible={closeOnBackdrop}
  direction={placement}
  shouldScaleBackground={false}
  noBodyStyles={true}
  scrollLockTimeout={0}
>
  <VaulDrawer.Portal>
    <VaulDrawer.Overlay
      class={`drawer-overlay ${backdropClass}`.trim()}
      onclick={handleBackdropClick}
    />
    <VaulDrawer.Content
      class={`drawer-content ${drawerClass}`.trim()}
      data-placement={placement}
      {role}
      aria-modal="true"
      aria-labelledby={labelledBy}
      aria-label={ariaLabel}
    >
      {#if showHandle}
        <div class="drawer-handle" aria-hidden="true"></div>
      {/if}
      <div class="drawer-inner">
        {@render children?.()}
      </div>
    </VaulDrawer.Content>
  </VaulDrawer.Portal>
</VaulDrawer.Root>

<style>
  /* Overlay (backdrop) - MUST be lower z-index than content */
  :global(.drawer-overlay) {
    position: fixed;
    inset: 0;
    z-index: calc(var(--sheet-z-index, var(--sheet-z-base, 50)) - 1) !important;
    background: var(--sheet-backdrop-bg, var(--backdrop-medium, rgba(0, 0, 0, 0.5)));
    backdrop-filter: var(--sheet-backdrop-filter, var(--backdrop-blur-medium, blur(8px)));
  }

  /* Edit panel backdrop - completely transparent */
  :global(.drawer-overlay.edit-panel-backdrop) {
    background: transparent !important;
    backdrop-filter: none !important;
    pointer-events: none !important;
  }

  /* Drawer content container */
  :global(.drawer-content) {
    position: fixed;
    z-index: var(--sheet-z-index, var(--sheet-z-base, 50)) !important;
    display: flex;
    flex-direction: column;
    outline: none;

    /* Default styling for bottom placement */
    background: var(--sheet-bg, var(--sheet-bg-glass, rgba(20, 25, 35, 0.95)));
    backdrop-filter: var(--sheet-filter, var(--glass-backdrop-strong, blur(24px)));
    border: var(--sheet-border, var(--sheet-border-subtle, 1px solid rgba(255, 255, 255, 0.1)));
    box-shadow: var(--sheet-shadow, var(--sheet-shadow-bottom, 0 -4px 24px rgba(0, 0, 0, 0.3)));
  }

  /* Bottom placement */
  :global(.drawer-content[data-placement="bottom"]) {
    bottom: 0;
    left: 0;
    right: 0;
    width: var(--sheet-width, min(720px, 100%));
    max-height: var(--sheet-max-height, min(95vh, var(--modal-max-height, 95vh)));
    margin: 0 auto;
    border-top-left-radius: var(--sheet-border-radius-top-left, var(--sheet-radius-large, 20px));
    border-top-right-radius: var(--sheet-border-radius-top-right, var(--sheet-radius-large, 20px));
    border-bottom: none;
  }

  /* Top placement */
  :global(.drawer-content[data-placement="top"]) {
    top: 0;
    left: 0;
    right: 0;
    width: var(--sheet-width, min(720px, 100%));
    max-height: var(--sheet-max-height, min(95vh, var(--modal-max-height, 95vh)));
    margin: 0 auto;
    border-bottom-left-radius: var(--sheet-radius-large, 20px);
    border-bottom-right-radius: var(--sheet-radius-large, 20px);
    border-top: none;
  }

  /* Right placement */
  :global(.drawer-content[data-placement="right"]) {
    top: 0;
    right: 0;
    bottom: 0;
    height: 100vh;
    width: var(--sheet-width, min(600px, 90vw));
    border-left: var(--sheet-border-strong, 2px solid rgba(255, 255, 255, 0.15));
    border-right: none;
    border-top-left-radius: var(--sheet-radius-large, 20px);
    border-bottom-left-radius: var(--sheet-radius-large, 20px);
  }

  /* Left placement */
  :global(.drawer-content[data-placement="left"]) {
    top: 0;
    left: 0;
    bottom: 0;
    height: 100vh;
    width: var(--sheet-width, min(600px, 90vw));
    border-right: var(--sheet-border-strong, 2px solid rgba(255, 255, 255, 0.15));
    border-left: none;
    border-top-right-radius: var(--sheet-radius-large, 20px);
    border-bottom-right-radius: var(--sheet-radius-large, 20px);
  }

  /* Handle */
  .drawer-handle {
    position: relative;
    width: 40px;
    height: 4px;
    margin: 10px auto 8px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.3);
    flex-shrink: 0;
  }

  /* Inner content container - NO OVERFLOW */
  .drawer-inner {
    flex: 1;
    /* CRITICAL: No overflow here! Child components should handle their own scrolling.
       This allows vaul-svelte's gesture detection to work correctly. */
    min-height: 0;
    display: flex;
    flex-direction: column;
  }

  /* Scrollbar styling */
  .drawer-inner::-webkit-scrollbar {
    width: 8px;
  }

  .drawer-inner::-webkit-scrollbar-track {
    background: transparent;
  }

  .drawer-inner::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .drawer-inner::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  /* Mobile adjustments */
  @media (max-width: 480px) {
    :global(.drawer-content[data-placement="bottom"]) {
      border-top-left-radius: var(--sheet-radius-medium, 16px);
      border-top-right-radius: var(--sheet-radius-medium, 16px);
    }
  }

  /* High contrast mode */
  @media (prefers-contrast: high) {
    :global(.drawer-content) {
      background: rgba(0, 0, 0, 0.98);
      border: 2px solid white;
    }

    .drawer-handle {
      background: rgba(255, 255, 255, 0.8);
    }
  }
</style>
