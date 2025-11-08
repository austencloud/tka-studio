<!--
  ConfirmDialog.svelte - MIGRATED TO BITS UI

  A classy confirmation dialog with glassmorphism styling.
  Now built on Bits UI Dialog for better accessibility and maintainability.

  BENEFITS:
  - WCAG AAA compliant accessibility out of the box
  - Better focus management and keyboard navigation
  - Portal rendering (no z-index issues)
  - Automatic ARIA attributes
  - Better screen reader support
-->
<script lang="ts">
  import { Dialog as DialogPrimitive } from "bits-ui";
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { quintOut } from "svelte/easing";
  import { fade, scale } from "svelte/transition";

  let {
    isOpen = $bindable(false),
    title,
    message,
    confirmText = "Continue",
    cancelText = "Cancel",
    onConfirm,
    onCancel,
    variant = "warning",
  } = $props<{
    isOpen?: boolean;
    title: string;
    message: string;
    confirmText?: string;
    cancelText?: string;
    onConfirm: () => void;
    onCancel: () => void;
    variant?: "warning" | "danger" | "info";
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Handle confirm button
  function handleConfirm() {
    // Trigger appropriate haptic feedback based on variant
    if (variant === "danger") {
      hapticService?.trigger("warning");
    } else {
      hapticService?.trigger("success");
    }

    onConfirm();
    isOpen = false;
  }

  // Handle cancel button
  function handleCancel() {
    // Trigger navigation haptic feedback for cancel
    hapticService?.trigger("selection");

    onCancel();
    isOpen = false;
  }

  // Handle open change from Bits UI
  function handleOpenChange(open: boolean) {
    if (!open && isOpen) {
      // User closed via escape or backdrop
      handleCancel();
    }
    isOpen = open;
  }
</script>

<DialogPrimitive.Root open={isOpen} onOpenChange={handleOpenChange}>
  <DialogPrimitive.Portal>
    <DialogPrimitive.Overlay
      transition={fade}
      transitionConfig={{ duration: 200 }}
      class="dialog-backdrop"
    />
    <DialogPrimitive.Content
      transition={scale}
      transitionConfig={{ duration: 200, easing: quintOut, start: 0.95 }}
      class="dialog-container {variant}"
    >
      <!-- Icon -->
      <div class="dialog-icon">
        {#if variant === "warning"}
          <span class="icon">⚠️</span>
        {:else if variant === "danger"}
          <span class="icon">🗑️</span>
        {:else}
          <span class="icon">ℹ️</span>
        {/if}
      </div>

      <!-- Content -->
      <div class="dialog-content">
        <DialogPrimitive.Title class="dialog-title"
          >{title}</DialogPrimitive.Title
        >
        <DialogPrimitive.Description class="dialog-message">
          {message}
        </DialogPrimitive.Description>
      </div>

      <!-- Actions -->
      <div class="dialog-actions">
        <button class="dialog-button cancel-button" onclick={handleCancel}>
          {cancelText}
        </button>
        <button class="dialog-button confirm-button" onclick={handleConfirm}>
          {confirmText}
        </button>
      </div>
    </DialogPrimitive.Content>
  </DialogPrimitive.Portal>
</DialogPrimitive.Root>

<style>
  :global(.dialog-backdrop) {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 20px;
  }

  :global(.dialog-container) {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(30, 30, 35, 0.95);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 32px;
    max-width: 480px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    z-index: 1001;
  }

  :global(.dialog-container.warning) {
    border-color: rgba(255, 193, 7, 0.3);
  }

  :global(.dialog-container.danger) {
    border-color: rgba(244, 67, 54, 0.3);
  }

  :global(.dialog-container.info) {
    border-color: rgba(33, 150, 243, 0.3);
  }

  .dialog-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 20px;
  }

  .icon {
    font-size: 48px;
    line-height: 1;
  }

  .dialog-content {
    text-align: center;
    margin-bottom: 28px;
  }

  :global(.dialog-title) {
    margin: 0 0 12px 0;
    font-size: 24px;
    font-weight: 600;
    color: var(--text-color, #ffffff);
    font-family: "Monotype Corsiva", cursive, serif;
    font-style: italic;
  }

  :global(.dialog-message) {
    margin: 0;
    font-size: 16px;
    line-height: 1.6;
    color: rgba(255, 255, 255, 0.8);
  }

  .dialog-actions {
    display: flex;
    gap: 12px;
    justify-content: center;
  }

  .dialog-button {
    padding: 12px 32px;
    border-radius: 8px;
    font-size: 16px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: 2px solid transparent;
    min-width: 120px;
  }

  .cancel-button {
    background: rgba(255, 255, 255, 0.1);
    color: rgba(255, 255, 255, 0.9);
    border-color: rgba(255, 255, 255, 0.2);
  }

  .cancel-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
  }

  .confirm-button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-color: rgba(255, 255, 255, 0.2);
  }

  .confirm-button:hover {
    background: linear-gradient(135deg, #7c8ff0 0%, #8a5bb0 100%);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  }

  :global(.dialog-container.warning) .confirm-button {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
  }

  :global(.dialog-container.warning) .confirm-button:hover {
    background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%);
    box-shadow: 0 4px 12px rgba(245, 158, 11, 0.4);
  }

  :global(.dialog-container.danger) .confirm-button {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
  }

  :global(.dialog-container.danger) .confirm-button:hover {
    background: linear-gradient(135deg, #f87171 0%, #ef4444 100%);
    box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
  }

  /* Mobile responsive */
  @media (max-width: 768px) {
    :global(.dialog-container) {
      padding: 24px;
      max-width: 90%;
    }

    :global(.dialog-title) {
      font-size: 20px;
    }

    :global(.dialog-message) {
      font-size: 14px;
    }

    .dialog-button {
      padding: 10px 24px;
      font-size: 14px;
      min-width: 100px;
    }

    .icon {
      font-size: 40px;
    }
  }
</style>
