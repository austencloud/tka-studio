<!--
FilterModal.svelte

Filter modal component for the Explore module.
Provides filtering options in a modal dialog, triggered by filter button.

Follows Svelte 5 runes + microservices architecture.
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";
  import type { ExploreFilterValue } from "../../shared/domain";

  // ✅ PURE RUNES: Props using modern Svelte 5 runes
  const {
    isOpen = false,
    currentFilter = { type: "all", value: null },
    availableSequenceLengths = [],
    onFilterChange = () => {},
    onClose = () => {},
  } = $props<{
    isOpen?: boolean;
    currentFilter?: { type: string; value: ExploreFilterValue };
    availableSequenceLengths?: number[];
    onFilterChange?: (type: string, value?: ExploreFilterValue) => void;
    onClose?: () => void;
  }>();

  let hapticService: IHapticFeedbackService;
  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );
  });

  // Filter sections matching actual data
  const filterSections = [
    { id: "all", label: "All Sequences" },
    { id: "favorites", label: "Favorites" },
    { id: "difficulty", label: "Difficulty Level" },
    { id: "startingPosition", label: "Starting Position" },
    { id: "startingLetter", label: "Starting Letter" },
    { id: "containsLetters", label: "Contains Letters" },
    { id: "length", label: "Sequence Length" },
    { id: "gridMode", label: "Grid Mode" },
    // Removed tag section - no tags exist yet
  ];

  // Difficulty levels (1-3 based on actual data)
  const difficultyLevels = [1, 2, 3];

  // Starting positions (actual grid positions)
  const startingPositions = ["alpha", "beta", "gamma"];

  // Grid modes (actual modes)
  const gridModes = ["diamond", "box"];

  // Use dynamic sequence lengths from props
  const sequenceLengths = $derived(() =>
    availableSequenceLengths.sort((a: number, b: number) => a - b)
  );

  // Letters for filtering
  const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");

  // State for multi-select filters
  let selectedLetters = $state<string[]>([]);

  // Apply a filter
  function applyFilter(type: string, value?: ExploreFilterValue) {
    hapticService?.trigger("selection");
    onFilterChange(type, value);
  }

  // Toggle letter selection for "Contains Letters" filter
  function toggleLetter(letter: string) {
    if (selectedLetters.includes(letter)) {
      selectedLetters = selectedLetters.filter((l) => l !== letter);
    } else {
      selectedLetters = [...selectedLetters, letter];
    }

    if (selectedLetters.length > 0) {
      applyFilter("containsLetters", selectedLetters);
    } else {
      applyFilter("all");
    }
  }

  // Handle modal close
  function handleClose() {
    hapticService?.trigger("selection");
    onClose();
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
  >
    <div class="modal-content">
      <!-- Modal header -->
      <div class="modal-header">
        <h2 id="filter-modal-title">Filter Sequences</h2>
        <button
          class="close-button"
          onclick={handleClose}
          aria-label="Close filter modal"
        >
          ×
        </button>
      </div>

      <!-- Filter sections -->
      <div class="filter-sections">
        {#each filterSections as section}
          <div class="filter-section">
            <h3>{section.label}</h3>

            {#if section.id === "all"}
              <button
                class="filter-button {currentFilter.type === 'all'
                  ? 'active'
                  : ''}"
                onclick={() => applyFilter("all")}
              >
                Show All Sequences
              </button>
            {:else if section.id === "favorites"}
              <button
                class="filter-button {currentFilter.type === 'favorites'
                  ? 'active'
                  : ''}"
                onclick={() => applyFilter("favorites")}
              >
                Show Favorites Only
              </button>
            {:else if section.id === "difficulty"}
              <div class="difficulty-buttons">
                {#each difficultyLevels as level}
                  <button
                    class="filter-button {currentFilter.type === 'difficulty' &&
                    currentFilter.value === level
                      ? 'active'
                      : ''}"
                    onclick={() => applyFilter("difficulty", level)}
                  >
                    Level {level}
                  </button>
                {/each}
              </div>
            {:else if section.id === "startingPosition"}
              <div class="position-buttons">
                {#each startingPositions as position}
                  <button
                    class="filter-button {currentFilter.type ===
                      'startingPosition' && currentFilter.value === position
                      ? 'active'
                      : ''}"
                    onclick={() => applyFilter("startingPosition", position)}
                  >
                    {position}
                  </button>
                {/each}
              </div>
            {:else if section.id === "startingLetter"}
              <div class="letter-grid">
                {#each letters as letter}
                  <button
                    class="letter-button {currentFilter.type ===
                      'startingLetter' && currentFilter.value === letter
                      ? 'active'
                      : ''}"
                    onclick={() => applyFilter("startingLetter", letter)}
                  >
                    {letter}
                  </button>
                {/each}
              </div>
            {:else if section.id === "containsLetters"}
              <div class="letter-grid">
                {#each letters as letter}
                  <button
                    class="letter-button {selectedLetters.includes(letter)
                      ? 'active'
                      : ''}"
                    onclick={() => toggleLetter(letter)}
                  >
                    {letter}
                  </button>
                {/each}
              </div>
            {:else if section.id === "length"}
              <div class="length-buttons">
                {#each sequenceLengths() as length}
                  <button
                    class="filter-button {currentFilter.type === 'length' &&
                    currentFilter.value === length
                      ? 'active'
                      : ''}"
                    onclick={() => applyFilter("length", length)}
                  >
                    {length} beats
                  </button>
                {/each}
              </div>
            {:else if section.id === "gridMode"}
              <div class="grid-mode-buttons">
                {#each gridModes as mode}
                  <button
                    class="filter-button {currentFilter.type === 'gridMode' &&
                    currentFilter.value === mode
                      ? 'active'
                      : ''}"
                    onclick={() => applyFilter("gridMode", mode)}
                  >
                    {mode}
                  </button>
                {/each}
              </div>
            {/if}
          </div>
        {/each}
      </div>

      <!-- Modal footer -->
      <div class="modal-footer">
        <button class="clear-button" onclick={() => applyFilter("all")}>
          Clear All Filters
        </button>
        <button class="apply-button" onclick={handleClose}>
          Apply Filters
        </button>
      </div>
    </div>
  </div>
{/if}

<style>
  .modal-backdrop {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
  }

  .modal-content {
    background: rgba(255, 255, 255, 0.95);
    backdrop-filter: blur(10px);
    border-radius: 12px;
    padding: 24px;
    max-width: 800px;
    max-height: 80vh;
    overflow-y: auto;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }

  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    padding-bottom: 16px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  }

  .modal-header h2 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 600;
    color: #333;
  }

  .close-button {
    background: none;
    border: none;
    font-size: 2rem;
    cursor: pointer;
    color: #666;
    padding: 0;
    width: 32px;
    height: 32px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    transition: all 0.2s ease;
  }

  .close-button:hover {
    background: rgba(0, 0, 0, 0.1);
    color: #333;
  }

  .filter-sections {
    display: grid;
    gap: 24px;
  }

  .filter-section {
    display: grid;
    gap: 12px;
  }

  .filter-section h3 {
    margin: 0;
    font-size: 1.1rem;
    font-weight: 600;
    color: #444;
  }

  .filter-button {
    padding: 8px 16px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
  }

  .filter-button:hover {
    background: #f5f5f5;
    border-color: #bbb;
  }

  .filter-button.active {
    background: #007bff;
    color: white;
    border-color: #007bff;
  }

  .difficulty-buttons,
  .position-buttons,
  .length-buttons,
  .grid-mode-buttons {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }

  .letter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(40px, 1fr));
    gap: 4px;
  }

  .letter-button {
    padding: 8px;
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.2s ease;
    font-size: 0.9rem;
    text-align: center;
  }

  .letter-button:hover {
    background: #f5f5f5;
    border-color: #bbb;
  }

  .letter-button.active {
    background: #007bff;
    color: white;
    border-color: #007bff;
  }

  .modal-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 24px;
    padding-top: 16px;
    border-top: 1px solid rgba(0, 0, 0, 0.1);
  }

  .clear-button,
  .apply-button {
    padding: 10px 20px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease;
  }

  .clear-button {
    background: #6c757d;
    color: white;
  }

  .clear-button:hover {
    background: #5a6268;
  }

  .apply-button {
    background: #007bff;
    color: white;
  }

  .apply-button:hover {
    background: #0056b3;
  }
</style>
