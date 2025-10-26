<!--
PresetSelectionModal.svelte - Modal for selecting saved generation presets
Displays user-saved presets with delete option and allows loading preset configuration
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { GenerationPreset } from "../../state/preset.svelte";
  import ModalHeader from "./ModalHeader.svelte";
  import { portal } from "./portal";
  import PresetGrid from "./PresetGrid.svelte";

  let {
    presets,
    onPresetSelect,
    onPresetDelete,
    onPresetEdit,
    onClose
  } = $props<{
    presets: GenerationPreset[];
    onPresetSelect: (preset: GenerationPreset) => void;
    onPresetDelete: (presetId: string) => void;
    onPresetEdit: (preset: GenerationPreset) => void;
    onClose: () => void;
  }>();

  let hapticService: IHapticFeedbackService;
  let modalElement: HTMLElement;

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
    <ModalHeader title="Load Preset" icon="⚙️" onClose={handleClose} />
    <PresetGrid
      {presets}
      {onPresetSelect}
      {onPresetEdit}
      {onPresetDelete}
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
    animation: backdrop-appear 0.3s ease-out;
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
    max-width: min(900px, 92vw);
    width: 100%;
    max-height: var(--modal-max-height, min(90dvh, calc(100dvh - 30px)));
    max-height: var(--modal-max-height, min(90vh, calc(100vh - 30px)));
    display: flex;
    flex-direction: column;
    overflow: hidden;
    animation: modal-appear 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    margin: auto;
    flex-shrink: 0;
    box-sizing: border-box;
    padding-top: env(safe-area-inset-top, 0);
    padding-bottom: env(safe-area-inset-bottom, 0);
    padding-left: env(safe-area-inset-left, 0);
    padding-right: env(safe-area-inset-right, 0);
    box-shadow:
      0 20px 60px rgba(0, 0, 0, 0.3),
      0 0 0 1px rgba(255, 255, 255, 0.1) inset;
  }

  /* Optimize for narrow devices (foldable phones, etc.) */
  @media (max-width: 380px) {
    .modal-backdrop {
      padding: 12px;
    }

    .modal-content {
      max-width: 96vw;
      border-radius: 12px;
    }
  }

  @keyframes modal-appear {
    from {
      opacity: 0;
      transform: scale(0.9) translateY(20px);
    }
    to {
      opacity: 1;
      transform: scale(1) translateY(0);
    }
  }
</style>
