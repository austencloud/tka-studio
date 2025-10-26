<!--
SavePresetModal.svelte - Premium modal for saving current settings as a preset
Provides a beautiful, unified experience for creating new presets
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import IconGrid from "./IconGrid.svelte";
  import ModalActions from "./ModalActions.svelte";
  import ModalHeader from "./ModalHeader.svelte";
  import { portal } from "./portal";

  let {
    onSave,
    onClose
  } = $props<{
    onSave: (icon?: string) => void;
    onClose: () => void;
  }>();

  let hapticService: IHapticFeedbackService;
  let modalElement: HTMLElement;

  let selectedIcon = $state("⚙️");

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

    // Focus the modal for accessibility
    modalElement?.focus();

    // Prevent body scroll
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = "";
    };
  });

  function handleSave() {
    hapticService?.trigger("selection");
    onSave(selectedIcon);
  }

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      hapticService?.trigger("navigation");
      onClose();
    }
  }

  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      hapticService?.trigger("navigation");
      onClose();
    } else if (event.key === "Enter") {
      handleSave();
    }
  }

  function handleClose() {
    hapticService?.trigger("navigation");
    onClose();
  }
</script>

<div
  class="modal-backdrop"
  use:portal
  onclick={handleBackdropClick}
  onkeydown={handleKeydown}
  bind:this={modalElement}
  tabindex="-1"
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
>
  <div class="modal-content">
    <ModalHeader title="Save Preset" icon="💾" onClose={handleClose} />

    <div class="modal-body">
      <div class="info-banner">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="16" x2="12" y2="12"></line>
          <line x1="12" y1="8" x2="12.01" y2="8"></line>
        </svg>
        <span>Preset name will be auto-generated from your settings</span>
      </div>

      <IconGrid bind:selectedIcon />
    </div>

    <ModalActions
      onCancel={handleClose}
      onConfirm={handleSave}
      cancelLabel="Cancel"
      confirmLabel="Save Preset"
      confirmVariant="success"
    />
  </div>
</div>

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100vh;
    height: 100dvh;
    height: var(--actual-vh, 100vh);
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
    padding: max(16px, env(safe-area-inset-top, 16px))
      max(16px, env(safe-area-inset-right, 16px))
      max(16px, env(safe-area-inset-bottom, 16px))
      max(16px, env(safe-area-inset-left, 16px));
    animation: backdrop-appear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  @keyframes backdrop-appear {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .modal-content {
    background: linear-gradient(
      135deg,
      rgba(255, 255, 255, 0.1) 0%,
      rgba(255, 255, 255, 0.05) 100%
    );
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 16px;
    max-width: min(460px, 90vw);
    width: 100%;
    max-height: var(--modal-max-height, min(85dvh, calc(100dvh - 60px)));
    max-height: var(--modal-max-height, min(85vh, calc(100vh - 60px)));
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: modal-appear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    margin: auto;
    flex-shrink: 0;
    box-sizing: border-box;
    box-shadow:
      0 20px 60px rgba(0, 0, 0, 0.3),
      0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  }

  @keyframes modal-appear {
    from {
      opacity: 0;
      transform: scale(0.95) translateY(20px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }

  .modal-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    gap: 24px;
    overflow-y: auto;
    flex: 1;
    min-height: 0;
  }

  .modal-body::-webkit-scrollbar {
    width: 8px;
  }

  .modal-body::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 4px;
  }

  .modal-body::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
  }

  .modal-body::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.5);
  }

  .info-banner {
    display: flex;
    align-items: center;
    gap: 14px;
    padding: 14px 16px;
    background: linear-gradient(
      135deg,
      rgba(59, 130, 246, 0.15),
      rgba(37, 99, 235, 0.1)
    );
    border: 1px solid rgba(59, 130, 246, 0.3);
    border-radius: 12px;
    color: rgba(147, 197, 253, 1);
    font-size: 14px;
    line-height: 1.5;
    box-shadow: 0 0 0 1px rgba(59, 130, 246, 0.1) inset;
  }

  .info-banner svg {
    width: 22px;
    height: 22px;
    flex-shrink: 0;
    filter: drop-shadow(0 2px 4px rgba(59, 130, 246, 0.3));
  }

  @media (max-width: 640px) {
    .modal-content {
      max-width: 95vw;
      border-radius: 14px;
    }

    .modal-body {
      padding: 20px;
      gap: 20px;
    }

    .info-banner {
      padding: 12px 14px;
      font-size: 13px;
    }

    .info-banner svg {
      width: 20px;
      height: 20px;
    }
  }
</style>
