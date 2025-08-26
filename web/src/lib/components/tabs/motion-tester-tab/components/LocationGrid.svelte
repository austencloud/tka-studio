<!--
LocationGrid.svelte - Visual 3x3 grid for location selection

Replaces dropdown with intuitive visual grid showing N/E/S/W positions.
Much more intuitive than dropdown for spatial location selection.
-->
<script lang="ts">
  import { GridMode, type Location } from "$lib/domain/enums";

  interface Props {
    selectedLocation: string;
    onLocationChange: (location: Location) => void;
    label: string;
    color: string;
    gridMode?: GridMode;
  }

  let {
    selectedLocation,
    onLocationChange,
    label,
    color,
    gridMode = GridMode.DIAMOND,
  }: Props = $props();

  // Enable beta positions (NW, NE, SW, SE) in box mode
  const locations = $derived([
    {
      id: "nw",
      label: gridMode === GridMode.BOX ? "NW" : "",
      disabled: gridMode !== GridMode.BOX,
    },
    { id: "n", label: "N", disabled: false },
    {
      id: "ne",
      label: gridMode === GridMode.BOX ? "NE" : "",
      disabled: gridMode !== GridMode.BOX,
    },
    { id: "w", label: "W", disabled: false },
    { id: "center", label: "●", disabled: true },
    { id: "e", label: "E", disabled: false },
    {
      id: "sw",
      label: gridMode === GridMode.BOX ? "SW" : "",
      disabled: gridMode !== GridMode.BOX,
    },
    { id: "s", label: "S", disabled: false },
    {
      id: "se",
      label: gridMode === GridMode.BOX ? "SE" : "",
      disabled: gridMode !== GridMode.BOX,
    },
  ]);

  function handleLocationClick(locationId: string) {
    if (locationId !== "center") {
      // Handle both single character (N, E, S, W) and beta positions (NW, NE, SW, SE)
      onLocationChange(locationId.toUpperCase() as Location);
    }
  }

  function isSelected(locationId: string): boolean {
    return locationId.toLowerCase() === selectedLocation.toLowerCase();
  }
</script>

<div class="location-grid-container">
  <div class="grid-label">{label}</div>
  <div class="location-grid" style="--accent-color: {color}">
    {#each locations as location}
      <button
        class="grid-cell"
        class:selected={isSelected(location.id)}
        class:disabled={location.disabled}
        class:available={!location.disabled}
        disabled={location.disabled}
        onclick={() => handleLocationClick(location.id)}
        aria-label={location.disabled
          ? ""
          : `Select ${location.label} position`}
        title={location.disabled ? "" : `${location.label} position`}
      >
        <span class="cell-content">{location.label}</span>
      </button>
    {/each}
  </div>
</div>

<style>
  .location-grid-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
  }

  .grid-label {
    font-size: 11px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }

  .location-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    grid-template-rows: repeat(3, 1fr);
    gap: 3px;
    padding: 6px;
    background: rgba(0, 0, 0, 0.3);
    border-radius: 10px;
    border: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.2);
  }

  .grid-cell {
    width: 32px;
    height: 32px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-radius: 6px;
    background: rgba(255, 255, 255, 0.08);
    color: rgba(255, 255, 255, 0.7);
    font-size: 13px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }

  .grid-cell.disabled {
    background: rgba(0, 0, 0, 0.1);
    border-color: rgba(255, 255, 255, 0.05);
    cursor: default;
    color: rgba(255, 255, 255, 0.15);
    box-shadow: none;
  }

  .grid-cell.available:hover {
    background: rgba(var(--accent-color), 0.2);
    border-color: rgba(var(--accent-color), 0.4);
    color: white;
    transform: scale(1.05);
  }

  .grid-cell.selected {
    background: linear-gradient(
      135deg,
      rgba(var(--accent-color), 0.3),
      rgba(var(--accent-color), 0.2)
    );
    border-color: rgba(var(--accent-color), 0.6);
    color: white;
    box-shadow:
      0 0 8px rgba(var(--accent-color), 0.3),
      inset 0 1px 2px rgba(255, 255, 255, 0.1);
  }

  .grid-cell.selected::before {
    content: "";
    position: absolute;
    inset: 2px;
    border-radius: 2px;
    background: linear-gradient(
      135deg,
      rgba(var(--accent-color), 0.1),
      transparent
    );
    pointer-events: none;
  }

  .cell-content {
    position: relative;
    z-index: 1;
  }

  /* Focus styles for accessibility */
  .grid-cell:focus {
    outline: none;
    box-shadow: 0 0 0 2px rgba(var(--accent-color), 0.5);
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .grid-cell {
      width: 28px;
      height: 28px;
      font-size: 12px;
    }

    .location-grid {
      gap: 2px;
      padding: 4px;
    }
  }
</style>
