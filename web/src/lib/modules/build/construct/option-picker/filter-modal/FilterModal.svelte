<!--
FilterModal.svelte - Progressive filter modal

Features:
- Step 1: Choose primary sort method (radio buttons)
- Step 2: Choose secondary filters based on primary selection (checkboxes)
- Clear visual hierarchy and mobile-friendly design
- Live option count display
- Glass morphism design matching TKA system
-->
<script lang="ts">
  import { quintOut } from "svelte/easing";
  import { fade, fly } from "svelte/transition";

  // Props
  const {
    isOpen = false,
    currentSortMethod = "type",
    activeFilters = {},
    optionCount = 0,
    onClose = () => {},
    onSortMethodChange = () => {},
    onFilterToggle = () => {},
    onClearFilters = () => {},
  }: {
    isOpen?: boolean;
    currentSortMethod?: string;
    activeFilters?: Record<string, boolean>;
    optionCount?: number;
    onClose?: () => void;
    onSortMethodChange?: (method: string) => void;
    onFilterToggle?: (filterKey: string) => void;
    onClearFilters?: () => void;
  } = $props();

  // Sort method options
  const sortMethods = [
    { value: "type", label: "Filter by Type", description: "Group options by movement type (1-6)" },
    { value: "endPosition", label: "Filter by End Position", description: "Group by final position (Alpha, Beta, Gamma)" },
    { value: "reversals", label: "Filter by Reversals", description: "Group by reversal count (Continuous, 1, 2)" },
  ];

  // Secondary filter options based on sort method
  const secondaryFilters = $derived(() => {
    switch (currentSortMethod) {
      case "type":
        return [
          { key: "type1", label: "Type 1", description: "Dual-Shift (A-V)" },
          { key: "type2", label: "Type 2", description: "Shift (W, X, Y, Z, Σ, Δ, θ, Ω)" },
          { key: "type3", label: "Type 3", description: "Cross-Shift (W-, X-, Y-, Z-, Σ-, Δ-, θ-, Ω-)" },
          { key: "type4", label: "Type 4", description: "Dash (Φ, Ψ, Λ)" },
          { key: "type5", label: "Type 5", description: "Dual-Dash (Φ-, Ψ-, Λ-)" },
          { key: "type6", label: "Type 6", description: "Static (α, β, Γ)" },
        ];
      case "endPosition":
        return [
          { key: "alpha", label: "Alpha", description: "Ends in Alpha position" },
          { key: "beta", label: "Beta", description: "Ends in Beta position" },
          { key: "gamma", label: "Gamma", description: "Ends in Gamma position" },
        ];
      case "reversals":
        return [
          { key: "continuous", label: "Continuous", description: "No reversals in motion" },
          { key: "1-reversal", label: "1 Reversal", description: "One direction change" },
          { key: "2-reversals", label: "2 Reversals", description: "Two direction changes" },
        ];
      default:
        return [];
    }
  });

  // Check if any secondary filters are active
  const hasActiveSecondaryFilters = $derived(() => {
    const filters = secondaryFilters();
    return filters.some((filter: { key: string; label: string; description: string }) => activeFilters[filter.key]);
  });

  // Handle backdrop click
  function handleBackdropClick(event: MouseEvent) {
    if (event.target === event.currentTarget) {
      onClose();
    }
  }

  // Handle escape key
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') {
      onClose();
    }
  }
</script>

<!-- Modal backdrop -->
{#if isOpen}
  <div 
    class="modal-backdrop"
    onclick={handleBackdropClick}
    onkeydown={handleKeydown}
    role="dialog"
    aria-modal="true"
    aria-labelledby="filter-modal-title"
    tabindex="-1"
    transition:fade={{ duration: 300, easing: quintOut }}
  >
    <!-- Modal content -->
    <div 
      class="modal-content"
      transition:fly={{ x: 300, duration: 400, easing: quintOut }}
    >
      <!-- Header -->
      <div class="modal-header">
        <h2 id="filter-modal-title" class="modal-title">Filter Options</h2>
        <button 
          class="close-button"
          onclick={onClose}
          aria-label="Close filter modal"
        >
          ✕
        </button>
      </div>

      <!-- Primary Sort Selection -->
      <div class="scrollable-content">
        <div class="filter-section">
          <h3 class="section-title">Sort & Display</h3>
          <div class="radio-group">
            {#each sortMethods as method}
              <label class="radio-option">
                <input
                  type="radio"
                  name="sortMethod"
                  value={method.value}
                  checked={currentSortMethod === method.value}
                  onchange={() => onSortMethodChange(method.value)}
                />
                <div class="radio-content">
                  <span class="radio-label">{method.label}</span>
                  <span class="radio-description">{method.description}</span>
                </div>
              </label>
            {/each}
          </div>
        </div>

        <!-- Secondary Filters -->
        {#if secondaryFilters().length > 0}
          <div class="filter-section">
            <h3 class="section-title">
              {#if currentSortMethod === "type"}
                Type Filters
              {:else if currentSortMethod === "endPosition"}
                Position Filters  
              {:else if currentSortMethod === "reversals"}
                Reversal Filters
              {/if}
            </h3>
            <div class="checkbox-group">
              {#each secondaryFilters() as filter}
                <label class="checkbox-option">
                  <input
                    type="checkbox"
                    checked={activeFilters[filter.key] || false}
                    onchange={() => onFilterToggle(filter.key)}
                  />
                  <div class="checkbox-content">
                    <span class="checkbox-label">{filter.label}</span>
                    <span class="checkbox-description">{filter.description}</span>
                  </div>
                </label>
              {/each}
            </div>
          </div>
        {/if}
      </div>

      <!-- Footer -->
      <div class="modal-footer">
        <div class="option-count">
          <span class="count-text">{optionCount} options match</span>
        </div>
        
        <div class="footer-actions">
          {#if hasActiveSecondaryFilters()}
            <button 
              class="clear-button"
              onclick={onClearFilters}
            >
              Clear Filters
            </button>
          {/if}
          <button 
            class="apply-button"
            onclick={onClose}
          >
            Apply & Close
          </button>
        </div>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(var(--glass-blur, 8px));
    -webkit-backdrop-filter: blur(var(--glass-blur, 8px));
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: flex-end;
    padding: 20px;
  }

  .modal-content {
    background: var(--surface-color, linear-gradient(135deg, rgba(255, 255, 255, 0.95), rgba(255, 255, 255, 0.9)));
    backdrop-filter: blur(var(--glass-blur, 20px));
    -webkit-backdrop-filter: blur(var(--glass-blur, 20px));
    border: 1px solid var(--glass-border, rgba(255, 255, 255, 0.3));
    border-radius: var(--radius-xl, 24px);
    box-shadow: var(--shadow-modal, 0 20px 60px rgba(0, 0, 0, 0.2), inset 0 1px 0 rgba(255, 255, 255, 0.3));
    
    width: 400px;
    max-width: 100vw;
    max-height: 90vh;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  .modal-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 24px 16px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }

  .modal-title {
    margin: 0;
    font-size: 20px;
    font-weight: 700;
    color: var(--foreground, #1f2937);
  }

  .close-button {
    background: none;
    border: none;
    font-size: 20px;
    cursor: pointer;
    padding: 8px;
    border-radius: 8px;
    color: var(--foreground, #6b7280);
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(0, 0, 0, 0.1);
    color: var(--foreground, #1f2937);
  }

  .scrollable-content {
    flex: 1;
    overflow-y: auto;
    min-height: 0; /* Important for flexbox scrolling */
  }

  .filter-section {
    padding: 20px 24px;
  }

  .filter-section:not(:last-child) {
    border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  }

  .section-title {
    margin: 0 0 16px 0;
    font-size: 16px;
    font-weight: 600;
    color: var(--foreground, #1f2937);
  }

  .radio-group, .checkbox-group {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .radio-option, .checkbox-option {
    display: flex;
    align-items: flex-start;
    gap: 12px;
    cursor: pointer;
    padding: 12px;
    border-radius: 12px;
    transition: all 0.2s ease;
  }

  .radio-option:hover, .checkbox-option:hover {
    background: rgba(0, 0, 0, 0.05);
  }

  .radio-content, .checkbox-content {
    display: flex;
    flex-direction: column;
    gap: 4px;
    flex: 1;
  }

  .radio-label, .checkbox-label {
    font-size: 14px;
    font-weight: 500;
    color: var(--foreground, #1f2937);
    line-height: 1.4;
  }

  .radio-description, .checkbox-description {
    font-size: 12px;
    color: var(--foreground, #6b7280);
    line-height: 1.3;
  }

  input[type="radio"], input[type="checkbox"] {
    margin: 2px 0 0 0;
    cursor: pointer;
  }

  .modal-footer {
    padding: 16px 24px 24px;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }

  .option-count {
    flex: 1;
  }

  .count-text {
    font-size: 14px;
    font-weight: 600;
    color: var(--foreground, #059669);
  }

  .footer-actions {
    display: flex;
    gap: 12px;
  }

  .clear-button, .apply-button {
    padding: 8px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s ease;
    border: none;
  }

  .clear-button {
    background: rgba(239, 68, 68, 0.1);
    color: #dc2626;
  }

  .clear-button:hover {
    background: rgba(239, 68, 68, 0.2);
  }

  .apply-button {
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    color: white;
  }

  .apply-button:hover {
    background: linear-gradient(135deg, #2563eb, #1e40af);
    transform: translateY(-1px);
  }

  /* Mobile responsiveness */
  @media (max-width: 768px) {
    .modal-backdrop {
      padding: 0;
      align-items: stretch;
      justify-content: stretch;
    }

    .modal-content {
      width: 100%;
      max-width: none;
      border-radius: 0;
      height: 100vh;
      max-height: none;
    }

    .modal-header {
      padding: 20px 20px 16px;
    }

    .filter-section {
      padding: 16px 20px;
    }

    .modal-footer {
      padding: 16px 20px 20px;
    }
  }

  @media (max-width: 480px) {
    .modal-header {
      padding: 16px 16px 12px;
    }

    .modal-title {
      font-size: 18px;
    }

    .filter-section {
      padding: 12px 16px;
    }

    .modal-footer {
      padding: 12px 16px 16px;
      flex-direction: column;
      gap: 12px;
      align-items: stretch;
    }

    .footer-actions {
      justify-content: stretch;
    }

    .clear-button, .apply-button {
      flex: 1;
    }
  }
</style>
