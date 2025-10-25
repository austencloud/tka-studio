<!--
CAPSelectionModal.svelte - Modal for selecting CAP components
Extracted from CAPCard for better separation of concerns
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { CAPComponent, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let {
    isOpen,
    selectedComponents,
    onToggleComponent,
    onClose
  } = $props<{
    isOpen: boolean;
    selectedComponents: Set<CAPComponent>;
    onToggleComponent: (component: CAPComponent) => void;
    onClose: () => void;
  }>();

  let hapticService: IHapticFeedbackService;

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });

  // Component data with colors and icons
  const capComponents = [
    {
      component: CAPComponent.ROTATED,
      label: "Rotated",
      icon: "🔄",
      color: "#36c3ff",
    },
    {
      component: CAPComponent.MIRRORED,
      label: "Mirrored",
      icon: "🪞",
      color: "#6F2DA8",
    },
    {
      component: CAPComponent.SWAPPED,
      label: "Swapped",
      icon: "🔀",
      color: "#26e600",
    },
    {
      component: CAPComponent.COMPLEMENTARY,
      label: "Complementary",
      icon: "🎨",
      color: "#eb7d00",
    }
  ];

  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  function handleToggle(component: CAPComponent) {
    hapticService?.trigger("selection");
    onToggleComponent(component);
  }
</script>

{#if isOpen}
  <div
    class="modal-backdrop"
    onclick={handleBackdropClick}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    role="dialog"
    aria-modal="true"
    aria-labelledby="cap-title"
    tabindex="-1"
  >
    <div class="modal-content">
      <!-- Scrollable content area -->
      <div class="modal-scroll-content">
        <!-- Header with close button -->
        <div class="modal-header">
          <div class="header-spacer"></div>
          <h2 id="cap-title">CAP Type</h2>
          <button
            class="close-button"
            onclick={onClose}
            aria-label="Close CAP selection"
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>

        <!-- Component Selection Grid -->
        <div class="component-grid">
          {#each capComponents as { component, label, icon, color: componentColor }}
            <button
              class="component-button"
              class:selected={selectedComponents.has(component)}
              onclick={() => handleToggle(component)}
              style="--component-color: {componentColor};"
              aria-label="{label} - {selectedComponents.has(component) ? 'selected' : 'not selected'}"
            >
              <div class="component-icon">{icon}</div>
              <div class="component-label">{label}</div>

              {#if selectedComponents.has(component)}
                <div class="selected-indicator">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                    <polyline points="20,6 9,17 4,12"></polyline>
                  </svg>
                </div>
              {/if}
            </button>
          {/each}
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    backdrop-filter: blur(4px);
    display: flex;
    align-items: center; /* Center modal vertically */
    justify-content: center; /* Center modal horizontally */
    z-index: 9999;
    padding: 0;
    animation: fadeIn 0.25s ease-out;
  }

  @keyframes fadeIn {
    from {
      opacity: 0;
    }
    to {
      opacity: 1;
    }
  }

  .modal-content {
    position: relative;
    /* Animated mesh gradient matching the card */
    background: linear-gradient(135deg,
      #4338ca 0%,
      #6b21a8 12.5%,
      #db2777 25%,
      #f97316 37.5%,
      #eab308 50%,
      #22c55e 62.5%,
      #0891b2 75%,
      #3b82f6 87.5%,
      #6366f1 100%
    );
    background-size: 300% 300%;
    animation: meshGradientFlow 15s ease infinite, modalSlideIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);

    border-radius: 20px;
    margin: 16px;
    width: calc(100% - 32px);
    /* Let height be determined by content on shorter screens */
    height: auto;
    max-height: calc(100vh - 32px);
    display: flex;
    flex-direction: column;
    box-shadow:
      0 0 20px rgba(139, 92, 246, 0.6),
      0 0 40px rgba(139, 92, 246, 0.4),
      0 8px 32px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    overflow: hidden;
  }

  /* Add dark overlay to ensure text contrast */
  .modal-content::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.15);
    pointer-events: none;
    z-index: 0;
  }

  @keyframes modalSlideIn {
    from {
      transform: scale(0.9) translateY(20px);
      opacity: 0;
    }
    to {
      transform: scale(1) translateY(0);
      opacity: 1;
    }
  }

  @keyframes meshGradientFlow {
    0%, 100% {
      background-position: 0% 50%;
    }
    25% {
      background-position: 50% 100%;
    }
    50% {
      background-position: 100% 50%;
    }
    75% {
      background-position: 50% 0%;
    }
  }

  .close-button {
    background: rgba(0, 0, 0, 0.3);
    border: none;
    border-radius: 8px;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    padding: 8px;
    width: 36px;
    height: 36px;
    flex-shrink: 0;
  }

  .close-button:hover {
    background: rgba(0, 0, 0, 0.5);
    transform: scale(1.05);
  }

  .close-button svg {
    width: 20px;
    height: 20px;
  }

  .modal-scroll-content {
    flex: 1;
    overflow: hidden;
    padding: clamp(16px, 3vw, 24px);
    display: flex;
    flex-direction: column;
    gap: clamp(12px, 2vw, 16px);
    position: relative;
    z-index: 1;
    min-height: 0;
    /* Center content vertically on tall screens only */
    justify-content: center;
  }

  /* Don't center on shorter screens - start from top for better space usage */
  @media (max-height: 900px) {
    .modal-scroll-content {
      justify-content: flex-start;
      flex: 0 1 auto; /* Don't force expansion */
    }
  }

  .modal-header {
    display: grid;
    grid-template-columns: 36px 1fr 36px;
    align-items: center;
    gap: clamp(8px, 2vw, 12px);
    flex-shrink: 0;
    margin-bottom: clamp(12px, 2.5vh, 20px);
    position: relative;
  }

  .header-spacer {
    width: 36px;
  }

  .modal-header h2 {
    color: white;
    font-size: clamp(18px, 3vw, 24px);
    font-weight: 700;
    margin: 0;
    text-shadow: 0 2px 6px rgba(0, 0, 0, 0.4);
    text-align: center;
  }

  .component-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(2, 1fr); /* Equal row heights */
    gap: clamp(10px, 2vw, 14px);
    /* Center the grid instead of stretching to fill */
    align-self: center;
    justify-self: center;
    width: 100%;
    /* Ensure grid fits in available space - critical for seeing all 4 buttons */
    max-height: 100%;
    /* Ensure buttons shrink to fit if needed */
    overflow: hidden;
    /* Center each item inside its grid cell */
    place-items: center;
  }

  .component-button {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: clamp(4px, 1vh, 8px); /* Space between icon and label */
    padding: clamp(12px, 2.5vw, 16px);
    background: rgba(0, 0, 0, 0.2);
    border: 2px solid rgba(255, 255, 255, 0.3);
    border-radius: 12px;
    cursor: pointer;
    text-align: center;
    color: white;
    transition: all 0.2s ease;
    /* Keep buttons nicely proportioned - slightly taller than wide */
    aspect-ratio: 4 / 5;
    /* CRITICAL: Prevent buttons from exceeding available height */
    min-height: 0;
    max-height: 100%;
  }

  .component-button:hover {
    background: rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.5);
    transform: translateY(-2px);
  }

  .component-button.selected {
    background: color-mix(in srgb, var(--component-color) 25%, rgba(0, 0, 0, 0.3));
    border-color: var(--component-color);
    border-width: 2px;
  }

  .component-button.selected:hover {
    background: color-mix(in srgb, var(--component-color) 35%, rgba(0, 0, 0, 0.3));
  }

  .component-icon {
    font-size: clamp(24px, 4.5vw, 32px);
    line-height: 1;
    flex-shrink: 0; /* Prevent icon from shrinking */
  }

  .component-label {
    font-size: clamp(13px, 2.2vw, 16px);
    font-weight: 600;
    color: white;
    line-height: 1.2;
    word-break: keep-all; /* Prevent word breaking */
  }

  .selected-indicator {
    position: absolute;
    top: 8px;
    right: 8px;
    width: 24px;
    height: 24px;
    color: white;
    background: rgba(0, 0, 0, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .selected-indicator svg {
    width: 14px;
    height: 14px;
  }

  /* 📱 TABLET & LARGE PHONES: Optimized for bigger screens */
  @media (min-width: 500px) and (max-width: 1024px) and (orientation: portrait) {
    .modal-content {
      margin: clamp(20px, 3vw, 32px);
      width: calc(100% - clamp(40px, 6vw, 64px));
      height: calc(100% - clamp(40px, 6vw, 64px));
      max-width: 600px;
      max-height: 800px;
      /* Center the modal itself */
      margin-left: auto;
      margin-right: auto;
    }

    .component-grid {
      gap: clamp(12px, 2.5vw, 18px);
      max-height: min(500px, 60vh);
    }

    .component-button {
      padding: clamp(16px, 3vw, 24px);
      aspect-ratio: 4 / 5;
    }

    .component-icon {
      font-size: clamp(28px, 5vw, 40px);
    }

    .component-label {
      font-size: clamp(14px, 2.5vw, 18px);
    }

    .selected-indicator {
      width: 28px;
      height: 28px;
      top: 10px;
      right: 10px;
    }

    .selected-indicator svg {
      width: 16px;
      height: 16px;
    }
  }

  /* Mobile responsive - smaller phones */
  @media (max-width: 499px) {
    .component-grid {
      grid-template-columns: repeat(2, 1fr);
      gap: clamp(8px, 2vw, 12px);
      /* Use grid auto-rows to fit 2 rows in available space */
      grid-auto-rows: minmax(0, 1fr);
    }

    .component-button {
      padding: clamp(12px, 3vw, 16px);
      /* Removed min-height - aspect-ratio handles proportions */
    }

    .component-icon {
      font-size: clamp(20px, 5vw, 28px);
    }

    .component-label {
      font-size: clamp(12px, 3vw, 14px);
    }
  }

  /* 🚨 SHORT SCREENS: Ensure all 4 buttons visible on compact devices */
  @media (max-height: 850px) and (orientation: portrait) {
    .modal-scroll-content {
      /* Less vertical centering on short screens */
      justify-content: flex-start;
      padding-top: clamp(14px, 2.5vh, 20px);
    }

    .component-grid {
      /* Let content determine size naturally */
      max-height: none;
      grid-auto-rows: minmax(0, 1fr);
    }

    .component-button {
      /* Slightly wider than tall for compact space usage */
      aspect-ratio: 5 / 4;
      padding: clamp(10px, 2vw, 14px);
      gap: clamp(4px, 0.8vh, 6px);
    }

    .component-icon {
      font-size: clamp(20px, 4vw, 26px);
    }

    .component-label {
      font-size: clamp(11px, 2.5vw, 13px);
    }
  }

  /* 🚨 VERY SHORT SCREENS: Even more compact (Galaxy Fold, small phones) */
  @media (max-height: 700px) and (orientation: portrait) {
    .modal-content {
      margin: 12px 16px;
      width: calc(100% - 32px);
      height: auto; /* Don't force height, let content determine it */
      max-height: calc(100vh - 24px);
    }

    .modal-scroll-content {
      padding: 14px 16px;
      gap: 10px;
    }

    .modal-header {
      margin-bottom: 10px;
    }

    .modal-header h2 {
      font-size: 16px;
    }

    .component-grid {
      gap: 8px;
      /* Don't constrain height - let aspect ratio and available width determine size */
      max-height: none;
    }

    .component-button {
      /* Slightly wider than tall for better space usage */
      aspect-ratio: 5 / 4;
      padding: 10px 8px;
      gap: 4px;
    }

    .component-icon {
      font-size: 22px;
    }

    .component-label {
      font-size: 11px;
      line-height: 1.1;
    }

    .close-button {
      width: 30px;
      height: 30px;
      padding: 6px;
    }

    .close-button svg {
      width: 16px;
      height: 16px;
    }

    .selected-indicator {
      width: 18px;
      height: 18px;
      top: 6px;
      right: 6px;
    }

    .selected-indicator svg {
      width: 10px;
      height: 10px;
    }
  }

  /* Very small screens */
  @media (max-width: 400px) {
    .modal-content {
      margin: 12px;
      width: calc(100% - 24px);
      height: calc(100% - 24px);
    }

    .component-grid {
      gap: clamp(6px, 2vw, 8px);
    }

    .component-button {
      padding: clamp(8px, 2.5vw, 12px);
      /* Removed min-height - aspect-ratio handles proportions */
    }

    .component-icon {
      font-size: clamp(18px, 5vw, 22px);
    }

    .component-label {
      font-size: clamp(10px, 2.8vw, 12px);
    }
  }

  /* 🌅 LANDSCAPE MODE: Horizontal row layout for better space usage */
  @media (orientation: landscape) and (max-height: 600px) {
    .modal-content {
      margin: 12px 16px;
      width: calc(100% - 32px);
      height: calc(100% - 24px);
    }

    .modal-scroll-content {
      padding: clamp(12px, 2vh, 16px) clamp(16px, 3vw, 24px);
    }

    .modal-header {
      margin-bottom: clamp(8px, 1.5vh, 12px);
    }

    .modal-header h2 {
      font-size: clamp(16px, 2.5vh, 20px);
    }

    .component-grid {
      /* Switch to horizontal row layout */
      grid-template-columns: repeat(4, 1fr);
      gap: clamp(8px, 1.5vw, 12px);
      max-height: none; /* Allow natural sizing in landscape */
    }

    .component-button {
      /* Adjust aspect ratio for landscape - wider buttons work better */
      aspect-ratio: 1 / 1;
      padding: clamp(8px, 1.5vh, 12px) clamp(6px, 1vw, 10px);
    }

    .component-icon {
      font-size: clamp(20px, 4vh, 28px);
    }

    .component-label {
      font-size: clamp(10px, 1.8vh, 13px);
    }

    .selected-indicator {
      width: 20px;
      height: 20px;
      top: 6px;
      right: 6px;
    }

    .selected-indicator svg {
      width: 12px;
      height: 12px;
    }

    .close-button {
      width: 32px;
      height: 32px;
      padding: 6px;
    }

    .close-button svg {
      width: 18px;
      height: 18px;
    }
  }

  /* 📱 LANDSCAPE + VERY NARROW: Even more compact (e.g., iPhone SE landscape) */
  @media (orientation: landscape) and (max-height: 400px) {
    .modal-content {
      margin: 8px 12px;
      width: calc(100% - 24px);
      height: calc(100% - 16px);
    }

    .modal-scroll-content {
      padding: 8px 12px;
      gap: 8px;
    }

    .modal-header {
      margin-bottom: 6px;
    }

    .modal-header h2 {
      font-size: 14px;
    }

    .component-grid {
      gap: 6px;
    }

    .component-button {
      aspect-ratio: 1 / 1;
      padding: 6px 4px;
    }

    .component-icon {
      font-size: 18px;
    }

    .component-label {
      font-size: 9px;
    }

    .close-button {
      width: 28px;
      height: 28px;
    }
  }
</style>
