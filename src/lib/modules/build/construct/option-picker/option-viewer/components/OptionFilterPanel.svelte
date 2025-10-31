<!--
OptionFilterPanel.svelte - Filter options dropdown panel

Provides a dedicated UI for filtering option viewer content:
- All/Continuous toggle
- Future filter options (grid mode, difficulty, etc.)
- Dropdown interaction sliding down from header
- Auto-dismisses on selection
-->

<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { fly, fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

  // Props
  const {
    isOpen = false,
    isContinuousOnly = false,
    onClose = () => {},
    onToggleContinuous = () => {},
  } = $props<{
    isOpen?: boolean;
    isContinuousOnly?: boolean;
    onClose?: () => void;
    onToggleContinuous?: (isContinuousOnly: boolean) => void;
  }>();

  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function handleClose() {
    onClose();
  }

  function handleContinuityToggle(value: boolean) {
    hapticService?.trigger("selection");
    onToggleContinuous(value);
    // Auto-dismiss after selection
    setTimeout(() => {
      onClose();
    }, 150); // Small delay for haptic feedback to register
  }

  // Close on backdrop click
  function handleBackdropClick() {
    handleClose();
  }

  // Close on escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === "Escape" && isOpen) {
      handleClose();
    }
  }
</script>

<svelte:window on:keydown={handleKeydown} />

{#if isOpen}
  <!-- Backdrop -->
  <div
    class="filter-backdrop"
    transition:fade={{ duration: 200, easing: cubicOut }}
    onclick={handleBackdropClick}
    role="presentation"
  ></div>

  <!-- Dropdown Panel -->
  <div
    class="filter-panel"
    transition:fly={{ y: -20, duration: 300, easing: cubicOut }}
    role="dialog"
    aria-labelledby="filter-panel-title"
    aria-modal="true"
  >
    <div class="filter-panel-header">
      <h2 id="filter-panel-title" class="filter-panel-title">
        <i class="fas fa-filter"></i>
        Filter Options
      </h2>
      <button
        class="close-button"
        onclick={handleClose}
        aria-label="Close filter panel"
        type="button"
      >
        <i class="fas fa-times"></i>
      </button>
    </div>

    <div class="filter-panel-content">
      <!-- Continuity Filter Section -->
      <div class="filter-section">
        <h3 class="section-title">Show Options</h3>
        <div class="toggle-group">
          <button
            class="toggle-option"
            class:active={!isContinuousOnly}
            onclick={() => handleContinuityToggle(false)}
            aria-pressed={!isContinuousOnly}
          >
            <div class="toggle-icon">
              <i class="fas fa-th"></i>
            </div>
            <div class="toggle-label">
              <div class="label-text">All Options</div>
              <div class="label-description">Show all available options</div>
            </div>
          </button>

          <button
            class="toggle-option"
            class:active={isContinuousOnly}
            onclick={() => handleContinuityToggle(true)}
            aria-pressed={isContinuousOnly}
          >
            <div class="toggle-icon">
              <i class="fas fa-link"></i>
            </div>
            <div class="toggle-label">
              <div class="label-text">Continuous Only</div>
              <div class="label-description">Show only continuous options</div>
            </div>
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  /* Backdrop overlay */
  .filter-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
    z-index: 999;
  }

  /* Dropdown panel */
  .filter-panel {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    max-height: 70vh;
    background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 0 0 16px 16px;
    box-shadow:
      0 8px 32px rgba(0, 0, 0, 0.4),
      0 4px 16px rgba(0, 0, 0, 0.3);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    z-index: 1000;
  }

  .filter-panel-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px 24px 16px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    background: rgba(255, 255, 255, 0.03);
  }

  .filter-panel-title {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.25rem;
    font-weight: 700;
    color: rgba(255, 255, 255, 0.95);
    margin: 0;
  }

  .filter-panel-title i {
    font-size: 1.1rem;
    color: rgba(147, 197, 253, 0.9);
  }

  .close-button {
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 50%;
    /* 44px minimum for touch targets on mobile */
    width: 44px;
    height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    color: rgba(255, 255, 255, 0.7);
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .close-button:hover {
    background: rgba(255, 255, 255, 0.12);
    color: rgba(255, 255, 255, 0.95);
    transform: scale(1.05);
  }

  .close-button:active {
    transform: scale(0.95);
  }

  .filter-panel-content {
    flex: 1;
    overflow-y: auto;
    padding: 20px 24px 24px;
    display: flex;
    flex-direction: column;
    gap: 20px;
  }

  .filter-section {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .section-title {
    font-size: 0.85rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin: 0;
  }

  .toggle-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .toggle-option {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 16px 20px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    text-align: left;
  }

  .toggle-option:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .toggle-option.active {
    background: rgba(59, 130, 246, 0.15);
    border-color: rgba(59, 130, 246, 0.5);
    box-shadow: 0 4px 16px rgba(59, 130, 246, 0.25);
  }

  .toggle-option.active:hover {
    background: rgba(59, 130, 246, 0.2);
    border-color: rgba(59, 130, 246, 0.6);
  }

  .toggle-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 48px;
    height: 48px;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    font-size: 1.25rem;
    color: rgba(255, 255, 255, 0.7);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .toggle-option.active .toggle-icon {
    background: rgba(59, 130, 246, 0.25);
    color: rgba(147, 197, 253, 1);
  }

  .toggle-label {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }

  .label-text {
    font-size: 1rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
  }

  .label-description {
    font-size: 0.85rem;
    color: rgba(255, 255, 255, 0.6);
  }

  .filter-section.future {
    padding: 20px;
    background: rgba(255, 255, 255, 0.03);
    border: 1px dashed rgba(255, 255, 255, 0.15);
    border-radius: 12px;
  }

  .future-note {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 0.9rem;
    color: rgba(255, 255, 255, 0.5);
    margin: 0;
    font-style: italic;
  }

  .future-note i {
    color: rgba(147, 197, 253, 0.6);
  }
</style>

