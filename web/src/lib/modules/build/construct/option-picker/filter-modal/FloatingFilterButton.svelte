<!--
FloatingFilterButton.svelte - Floating filter button that replaces the header

Features:
- Floats above the option grid in the Z-axis
- Shows current filter status as subtitle
- Opens filter modal on click
- Mobile-friendly design with proper touch targets
- Beautiful glassmorphism styling to match TKA design system
-->
<script lang="ts">
  // Props
  const {
    currentSortMethod = "type",
    activeFilters = [],
    optionCount = 0,
    onOpenModal = () => {},
  }: {
    currentSortMethod?: string;
    activeFilters?: string[];
    optionCount?: number;
    onOpenModal?: () => void;
  } = $props();

  // Computed status text
  function getStatusText(): string {
    if (activeFilters.length === 0) {
      return `Filter by ${capitalize(currentSortMethod)} • ${optionCount} options`;
    }
    
    const filterText = activeFilters.join(", ");
    return `${filterText} • ${optionCount} options`;
  }

  function capitalize(str: string): string {
    return str.charAt(0).toUpperCase() + str.slice(1);
  }
</script>

<div class="floating-filter-container">
  <button
    class="floating-filter-button"
    onclick={onOpenModal}
    aria-label="Open filter options"
    title="Click to change filters and sorting"
  >
    <div class="button-content">
      <span class="filter-icon" aria-hidden="true">⚙️</span>
      <span class="button-text">Filter</span>
    </div>
  </button>
</div>

<style>
  .floating-filter-container {
    position: absolute;
    top: 16px;
    right: 16px;
    z-index: 100;
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 8px;
    pointer-events: none; /* Allow clicks to pass through the container */
  }

  .floating-filter-button {
    /* Restore pointer events for the button itself */
    pointer-events: auto;
    
    /* Glass morphism styling using TKA design system */
    background: var(--surface-color, linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05)));
    backdrop-filter: blur(var(--glass-blur, 20px));
    -webkit-backdrop-filter: blur(var(--glass-blur, 20px));
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.2));
    border-radius: var(--radius-lg, 16px);
    box-shadow: var(--shadow-glass, 0 8px 32px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2));

    /* Size and spacing */
    padding: var(--spacing-3, 12px) var(--spacing-4, 16px);
    min-width: 80px;
    min-height: 48px; /* Touch-friendly minimum */

    /* Typography */
    color: var(--text-primary, #ffffff);
    font-weight: var(--font-weight-semibold, 600);
    font-size: var(--text-sm, 14px);

    /* Interactions */
    cursor: pointer;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    user-select: none;
    touch-action: manipulation;

    /* Layout */
    display: flex;
    align-items: center;
    justify-content: center;

    /* Remove default button styles */
    border: none;
    outline: none;
  }

  .button-content {
    display: flex;
    align-items: center;
    gap: 8px;
  }

  .filter-icon {
    font-size: 16px;
    line-height: 1;
  }

  .button-text {
    font-weight: 600;
    line-height: 1;
  }

  .floating-filter-button:hover {
    background: var(--surface-color-hover, linear-gradient(135deg, rgba(255, 255, 255, 0.25), rgba(255, 255, 255, 0.1)));
    border: 1px solid var(--glass-border-hover, rgba(255, 255, 255, 0.3));
    box-shadow: var(--shadow-glass-hover, 0 12px 40px rgba(0, 0, 0, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.3));
    transform: translateY(-2px);
  }

  .floating-filter-button:active {
    transform: translateY(0);
    box-shadow: var(--shadow-glass-active, 0 4px 16px rgba(0, 0, 0, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.2));
  }

  .status-text {
    line-height: 1.2;
  }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .floating-filter-container {
      top: 12px;
      right: 12px;
    }

    .floating-filter-button {
      min-width: 70px;
      min-height: 44px;
      padding: 10px 14px;
      font-size: 13px;
    }

    .filter-icon {
      font-size: 14px;
    }

    .filter-status {
      font-size: 11px;
      padding: 4px 8px;
    }
  }

  @media (max-width: 480px) {
    .floating-filter-container {
      top: 8px;
      right: 8px;
    }

    .floating-filter-button {
      min-width: 60px;
      min-height: 40px;
      padding: 8px 12px;
      font-size: 12px;
    }

    .filter-status {
      font-size: 10px;
    }

    /* On very small screens, consider hiding the text and just showing icon */
    .button-text {
      display: none;
    }

    .floating-filter-button {
      min-width: 40px;
      padding: 8px;
    }
  }
</style>
