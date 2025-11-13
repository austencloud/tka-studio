<!-- OptionsModal.svelte - Unified modal for share options and export actions -->
<script lang="ts">
  import type { IHapticFeedbackService, SequenceData } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ShareOptions } from "../domain";
  import type { ShareState } from "../state";
  import ShareOptionsForm from "./ShareOptionsForm.svelte";

  let {
    show = false,
    currentSequence,
    shareState,
    isMobile = false,
    onClose,
    onDownload,
  }: {
    show?: boolean;
    currentSequence?: SequenceData | null;
    shareState?: ShareState | null;
    isMobile?: boolean;
    onClose?: () => void;
    onDownload?: () => void;
  } = $props();

  // Services
  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Handle modal close
  function handleClose() {
    hapticService?.trigger("selection");
    onClose?.();
  }

  // Handle download action
  function handleDownload() {
    hapticService?.trigger("success");
    onDownload?.();
    onClose?.(); // Close modal after download
  }

  // Handle input changes for user info
  function handleInputChange(key: keyof ShareOptions) {
    return (event: Event) => {
      const target = event.target as HTMLInputElement;
      shareState?.updateOptions({ [key]: target.value });
    };
  }

  // Handle backdrop click
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      handleClose();
    }
  }

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape") {
      handleClose();
    }
  }
</script>

<!-- Modal overlay -->
{#if show}
  <!-- svelte-ignore a11y_no_static_element_interactions -->
  <div
    class="modal-overlay"
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    tabindex="-1"
  >
    <div class="modal-content">
      <!-- Modal Header -->
      <div class="modal-header">
        <h3 id="modal-title" class="modal-title">Customize Share Options</h3>
        <button
          class="modal-close-btn"
          onclick={handleClose}
          aria-label="Close modal"
        >
          ✕
        </button>
      </div>

      <!-- Modal Body -->
      <div class="modal-body">
        <!-- Customization Options -->
        {#if shareState?.options}
          <ShareOptionsForm
            options={shareState.options}
            onOptionsChange={(newOptions) =>
              shareState?.updateOptions(newOptions)}
          />
        {/if}

        <!-- User Info Fields (if enabled) -->
        {#if shareState?.options.addUserInfo}
          <div class="user-info-section">
            <h4 class="group-title">User Information</h4>

            <label class="input-label">
              Name
              <input
                type="text"
                class="text-input"
                value={shareState.options.userName}
                oninput={handleInputChange("userName")}
                placeholder="Your name"
              />
            </label>

            <label class="input-label">
              Notes
              <input
                type="text"
                class="text-input"
                value={shareState.options.notes}
                oninput={handleInputChange("notes")}
                placeholder="Optional notes"
              />
            </label>
          </div>
        {/if}
      </div>

      <!-- Modal Footer -->
      <div class="modal-footer">
        <button class="modal-cancel-btn" onclick={handleClose}> Done </button>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Modal overlay */
  .modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    padding: 1rem;
  }

  .modal-content {
    background: var(--bg-primary);
    border-radius: 12px;
    width: 100%;
    max-width: 500px;
    max-height: 90vh;
    overflow: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
  }

  /* Modal header */
  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1rem;
    border-bottom: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }

  .modal-title {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
  }

  .modal-close-btn {
    background: none;
    border: none;
    font-size: 1.2rem;
    color: var(--text-secondary);
    cursor: pointer;
    padding: 0.25rem;
    border-radius: 4px;
    transition: all 0.2s ease;
  }

  .modal-close-btn:hover {
    background: var(--bg-tertiary);
    color: var(--text-primary);
  }

  /* Modal body */
  .modal-body {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    min-height: 0;
  }

  /* User info section */
  .user-info-section {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid var(--border-color);
  }

  .group-title {
    margin: 0 0 0.75rem 0;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .input-label {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
    font-weight: 500;
    color: var(--text-primary);
  }

  .text-input {
    padding: 0.75rem;
    border: 1px solid var(--border-color);
    border-radius: 8px;
    background: var(--bg-secondary);
    color: var(--text-primary);
    font-size: 1rem;
  }

  .text-input:focus {
    outline: none;
    border-color: var(--accent-color);
  }

  /* Modal footer */
  .modal-footer {
    padding: 1rem;
    border-top: 1px solid var(--border-color);
    background: var(--bg-secondary);
  }

  .modal-cancel-btn {
    width: 100%;
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: none;
    border-radius: 8px;
    padding: 0.75rem;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
  }

  .modal-cancel-btn:hover {
    background: var(--bg-quaternary);
  }

  /* Responsive design */
  @media (max-width: 767px) {
    .modal-overlay {
      padding: 0.5rem;
    }

    .modal-content {
      max-height: 95vh;
    }

    .modal-header,
    .modal-body,
    .modal-footer {
      padding: 0.75rem;
    }
  }
</style>
