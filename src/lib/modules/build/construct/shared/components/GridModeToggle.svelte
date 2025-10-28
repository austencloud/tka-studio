<!--
GridModeToggle.svelte - Single-button toggle showing opposite grid mode
Action-oriented pattern: Shows the mode you can switch TO (not current mode)
-->
<script lang="ts">
  import { GridMode, resolve, TYPES, type IHapticFeedbackService } from "$shared";

  const {
    currentGridMode = GridMode.DIAMOND,
    onGridModeChange,
  } = $props<{
    currentGridMode?: GridMode;
    onGridModeChange?: (gridMode: GridMode) => void;
  }>();

  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  // Action-oriented: Show the mode you can switch TO
  const oppositeMode = $derived(
    currentGridMode === GridMode.DIAMOND ? GridMode.BOX : GridMode.DIAMOND
  );
  
  const oppositeLabel = $derived(
    oppositeMode === GridMode.DIAMOND ? "Diamond" : "Box"
  );
  
  const oppositeIcon = $derived(
    oppositeMode === GridMode.DIAMOND ? "◇" : "▢"
  );

  function handleToggle() {
    hapticService?.trigger("selection");
    onGridModeChange?.(oppositeMode);
  }

  function handleKeyDown(e: KeyboardEvent) {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      handleToggle();
    }
  }
</script>

<button
  class="grid-mode-toggle"
  onclick={handleToggle}
  onkeydown={handleKeyDown}
  role="switch"
  aria-checked={currentGridMode === GridMode.BOX}
  aria-label={`Switch to ${oppositeLabel} mode`}
  title={`Switch to ${oppositeLabel} mode`}
>
  <span class="mode-icon">{oppositeIcon}</span>
  <span class="mode-label">{oppositeLabel}</span>
</button>

<style>
  .grid-mode-toggle {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    
    /* Bigger touch target */
    min-height: 44px;
    min-width: 120px;
    padding: 10px 20px;
    
    /* Glass morphism styling */
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 24px;
    
    /* Typography */
    font-size: 15px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    letter-spacing: 0.3px;
    
    /* Interaction */
    cursor: pointer;
    user-select: none;
    -webkit-tap-highlight-color: transparent;
    
    /* Smooth transitions */
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    
    /* Shadow */
    box-shadow: 
      0 2px 8px rgba(0, 0, 0, 0.1),
      inset 0 1px 0 rgba(255, 255, 255, 0.1);
  }

  .mode-icon {
    font-size: 20px;
    line-height: 1;
  }

  .mode-label {
    font-size: 15px;
    font-weight: 600;
    white-space: nowrap;
  }

  /* Hover state */
  @media (hover: hover) {
    .grid-mode-toggle:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
      box-shadow: 
        0 4px 12px rgba(0, 0, 0, 0.15),
        inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
  }

  /* Active/pressed state */
  .grid-mode-toggle:active {
    transform: translateY(0) scale(0.98);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Focus state */
  .grid-mode-toggle:focus-visible {
    outline: 2px solid #818cf8;
    outline-offset: 2px;
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .grid-mode-toggle {
      transition: none;
    }
    
    .grid-mode-toggle:hover {
      transform: none;
    }
    
    .grid-mode-toggle:active {
      transform: scale(0.98);
    }
  }

  /* Mobile responsive */
  @media (max-width: 600px) {
    .grid-mode-toggle {
      min-height: 40px;
      min-width: 100px;
      padding: 8px 16px;
      gap: 6px;
    }
    
    .mode-icon {
      font-size: 18px;
    }
    
    .mode-label {
      font-size: 14px;
    }
  }
</style>

