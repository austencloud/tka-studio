<!--
EditPresetModal.svelte - Premium modal for editing preset name and icon
Provides a beautiful, unified experience for customizing presets
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { GenerationPreset } from "../../state/preset.svelte";
  import IconGrid from "./IconGrid.svelte";
  import ModalActions from "./ModalActions.svelte";
  import ModalHeader from "./ModalHeader.svelte";
  import { portal } from "./portal";

  let {
    preset,
    onSave,
    onClose
  } = $props<{
    preset: GenerationPreset;
    onSave: (name: string, icon?: string) => void;
    onClose: () => void;
  }>();

  let hapticService: IHapticFeedbackService;
  let modalElement: HTMLElement;
  let nameInput: HTMLInputElement;

  let presetName = $state(preset.name);
  let selectedIcon = $state(preset.icon || "⚙️");

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

    // Focus the name input
    nameInput?.focus();
    nameInput?.select(); // Select all text for easy editing

    // Prevent body scroll
    document.body.style.overflow = "hidden";

    return () => {
      document.body.style.overflow = "";
    };
  });

  function handleSave() {
    const trimmedName = presetName.trim();
    if (!trimmedName) {
      return;
    }

    hapticService?.trigger("selection");
    onSave(trimmedName, selectedIcon);
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
    } else if (event.key === "Enter" && presetName.trim()) {
      handleSave();
    }
  }

  function handleClose() {
    hapticService?.trigger("navigation");
    onClose();
  }

  const canSave = $derived(presetName.trim().length > 0 && (presetName !== preset.name || selectedIcon !== preset.icon));
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
    <ModalHeader title="Edit Preset" icon="✏️" onClose={handleClose} />

    <div class="modal-body">
      <div class="form-section">
        <label for="preset-name" class="form-label">Preset Name</label>
        <input
          id="preset-name"
          type="text"
          class="name-input"
          bind:value={presetName}
          bind:this={nameInput}
          placeholder="e.g., Diamond 16, My Practice Flow"
          maxlength="50"
        />
      </div>

      <IconGrid bind:selectedIcon label="Icon" />
    </div>

    <ModalActions
      onCancel={handleClose}
      onConfirm={handleSave}
      cancelLabel="Cancel"
      confirmLabel="Save Changes"
      confirmDisabled={!canSave}
      confirmVariant="primary"
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
    gap: 20px;
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

  .form-section {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .form-label {
    color: rgba(255, 255, 255, 0.95);
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.01em;
  }

  .name-input {
    width: 100%;
    padding: 12px 16px;
    background: linear-gradient(
      135deg,
      rgba(0, 0, 0, 0.4),
      rgba(0, 0, 0, 0.3)
    );
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 10px;
    color: white;
    font-size: 15px;
    font-family: inherit;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) inset;
  }

  .name-input:focus {
    outline: none;
    border-color: rgba(59, 130, 246, 0.6);
    background: linear-gradient(
      135deg,
      rgba(0, 0, 0, 0.5),
      rgba(0, 0, 0, 0.4)
    );
    box-shadow:
      0 0 0 3px rgba(59, 130, 246, 0.2),
      0 2px 8px rgba(0, 0, 0, 0.2) inset;
  }

  .name-input::placeholder {
    color: rgba(255, 255, 255, 0.4);
  }

  @media (max-width: 640px) {
    .modal-content {
      max-width: 95vw;
      border-radius: 14px;
    }

    .modal-body {
      padding: 20px;
      gap: 16px;
    }

    .name-input {
      padding: 11px 14px;
      font-size: 14px;
    }
  }
</style>
