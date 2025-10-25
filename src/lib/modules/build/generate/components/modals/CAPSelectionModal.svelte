<!--
CAPSelectionModal.svelte - Modal for selecting CAP components
Refactored for better separation of concerns
Uses portal to render at document.body level for proper z-index stacking
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { CAPComponent, resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import { generateExplanationText } from "./cap-components";
  import CAPComponentGrid from "./CAPComponentGrid.svelte";
  import CAPExplanationPanel from "./CAPExplanationPanel.svelte";
  import CAPModalHeader from "./CAPModalHeader.svelte";
  import { portal } from "./portal";

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

    // Prevent body scroll when modal is open
    if (isOpen) {
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.body.style.overflow = "";
    };
  });

  // Generate explanation text based on selected components
  const explanationText = $derived(generateExplanationText(selectedComponents));

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
    class="cap-modal-backdrop"
    use:portal
    onclick={handleBackdropClick}
    onkeydown={(e) => e.key === 'Escape' && onClose()}
    tabindex="-1"
    role="dialog"
    aria-modal="true"
    aria-labelledby="cap-title"
  >
    <div class="cap-modal-content">
      <CAPModalHeader title="Select CAP Type" onClose={onClose} />
      <CAPComponentGrid
        {selectedComponents}
        onToggleComponent={handleToggle}
      />
      <CAPExplanationPanel {explanationText} />
    </div>
  </div>
{/if}

<style>
  .cap-modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    width: 100vw;
    height: 100dvh; /* Use dynamic viewport height to account for browser UI */
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 999999;
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

  .cap-modal-content {
    position: relative;
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
    width: 90dvw;
    height: 90dvh; /* Use dynamic viewport height to account for browser UI */
    max-height: 90%; /* Fallback for browsers that don't support dvh */
    display: flex;
    flex-direction: column;
    gap: clamp(16px, 3vh, 24px);
    padding: clamp(20px, 4vh, 32px) clamp(16px, 3vw, 24px);
    box-shadow:
      0 0 20px rgba(139, 92, 246, 0.6),
      0 0 40px rgba(139, 92, 246, 0.4),
      0 8px 32px rgba(0, 0, 0, 0.3),
      inset 0 1px 0 rgba(255, 255, 255, 0.2);
    overflow-y: auto;
  }

  .cap-modal-content::before {
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

  /* 🎯 No media query overrides - modal stays at 80% width and 80vh height */
</style>
