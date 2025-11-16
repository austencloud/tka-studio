<!--
Gallery Top Bar Controls
Renders the Gallery controls in the TopBar when desktop sidebar is visible
Uses shared gallery controls state from ExploreModule (Svelte 5 runes pattern)
-->
<script lang="ts">
  import { ViewPresetsDropdown } from "../../filtering/components";
  import { NavigationDropdown } from "../../navigation/components";
  import { galleryControlsManager } from "../state/gallery-controls-state.svelte";

  // Get gallery controls from global reactive state (provided by ExploreModule)
  const galleryControls = $derived(galleryControlsManager.current);
</script>

{#if galleryControls}
  <div class="gallery-topbar-controls">
    <div class="controls-group">
      <!-- 1. View Presets Dropdown -->
      <div class="control-item">
        <ViewPresetsDropdown
          currentFilter={galleryControls.currentFilter}
          onFilterChange={galleryControls.onFilterChange}
        />
      </div>

      <!-- 2. Sort & Jump Dropdown -->
      <div class="control-item">
        <NavigationDropdown
          currentSortMethod={galleryControls.currentSortMethod}
          availableSections={galleryControls.availableNavigationSections}
          onSectionClick={galleryControls.scrollToSection}
          onSortMethodChange={galleryControls.onSortMethodChange}
        />
      </div>

      <!-- 3. Advanced Filter Button -->
      <div class="control-item">
        <button
          class="advanced-filter-button"
          onclick={() => galleryControls.openFilterModal()}
          type="button"
          aria-label="Advanced filters"
        >
          <i class="fas fa-sliders-h"></i>
          <span>Filters</span>
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .gallery-topbar-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    max-width: 100%;
    padding: 0 8px;
  }

  .controls-group {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: nowrap;
  }

  .control-item {
    flex-shrink: 0;
  }

  /* Advanced Filter Button - matching the style from ExploreModule */
  .advanced-filter-button {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 10px 16px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.9);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    white-space: nowrap;
  }

  .advanced-filter-button:hover {
    background: rgba(255, 255, 255, 0.15);
    border-color: rgba(255, 255, 255, 0.4);
  }

  .advanced-filter-button:active {
    transform: scale(0.98);
  }

  /* Compact styling for TopBar */
  @media (max-width: 1200px) {
    .controls-group {
      gap: 8px;
    }

    .advanced-filter-button {
      padding: 8px 12px;
      font-size: 0.875rem;
    }
  }

  /* Reduced motion */
  @media (prefers-reduced-motion: reduce) {
    .advanced-filter-button {
      transition: none;
    }
  }
</style>
