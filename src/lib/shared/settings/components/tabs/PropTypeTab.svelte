<!-- PropTypeTab.svelte - Prop type selection with actual desktop app files -->
<script lang="ts">
  import type { AppSettings, IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { onMount } from "svelte";

  let { settings, onUpdate } = $props<{
    settings: AppSettings;
    onUpdate?: (event: { key: string; value: unknown }) => void;
  }>();

  // Services
  let hapticService: IHapticFeedbackService;

  // Grid container tracking for responsive sizing
  let gridContainerElement: HTMLDivElement | null = null;
  let containerWidth = $state(0);
  let containerHeight = $state(0);

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(
      TYPES.IHapticFeedbackService
    );

    // Setup ResizeObserver to track container dimensions
    if (!gridContainerElement) return;

    const resizeObserver = new ResizeObserver((entries) => {
      for (const entry of entries) {
        if (entry.borderBoxSize?.[0]) {
          containerWidth = entry.borderBoxSize[0].inlineSize;
          containerHeight = entry.borderBoxSize[0].blockSize;
        } else {
          containerWidth = entry.contentRect.width;
          containerHeight = entry.contentRect.height;
        }
      }
    });

    resizeObserver.observe(gridContainerElement);

    return () => {
      resizeObserver.disconnect();
    };
  });

  // Exact prop types from desktop app prop_type_tab.py
  const propTypes = [
    { id: "Staff", label: "Staff", image: "/images/props/staff.svg" },
    {
      id: "Simplestaff",
      label: "Simple Staff",
      image: "/images/props/simple_staff.svg",
    },
    { id: "Club", label: "Club", image: "/images/props/club.svg" },
    { id: "Fan", label: "Fan", image: "/images/props/fan.svg" },
    { id: "Triad", label: "Triad", image: "/images/props/triad.svg" },
    { id: "Minihoop", label: "Mini Hoop", image: "/images/props/minihoop.svg" },
    { id: "Buugeng", label: "Buugeng", image: "/images/props/buugeng.svg" },
    {
      id: "Triquetra",
      label: "Triquetra",
      image: "/images/props/triquetra.svg",
    },
    { id: "Sword", label: "Sword", image: "/images/props/sword.svg" },
    { id: "Chicken", label: "Chicken", image: "/images/props/chicken.png" },
    { id: "Hand", label: "Hand", image: "/images/props/hand.svg" },
    { id: "Guitar", label: "Guitar", image: "/images/props/guitar.svg" },
  ];

  let selectedPropType = $state(settings.propType || "Staff");

  // Calculate optimal grid layout based on container size
  const gridLayout = $derived(() => {
    const totalItems = propTypes.length; // 12 items

    // Determine columns smoothly based on container width (no breakpoints!)
    let columns = 3; // Default
    if (containerWidth >= 900) columns = 6;
    else if (containerWidth >= 650) columns = 6;
    else if (containerWidth >= 450) columns = 4;
    else if (containerWidth >= 300) columns = 3;

    const rows = Math.ceil(totalItems / columns);

    return { columns, rows };
  });

  function selectPropType(propType: string) {
    // Trigger selection haptic feedback for prop type selection
    hapticService?.trigger("selection");

    selectedPropType = propType;
    onUpdate?.({ key: "propType", value: propType });
  }
</script>

<div class="tab-content">
  <div class="prop-container" bind:this={gridContainerElement}>
    <div
      class="prop-grid"
      style:--grid-columns={`repeat(${gridLayout().columns}, 1fr)`}
      style:--grid-rows={`repeat(${gridLayout().rows}, 1fr)`}
    >
      {#each propTypes as prop}
        <button
          class="prop-button"
          class:selected={selectedPropType === prop.id}
          onclick={() => selectPropType(prop.id)}
          onkeydown={(e) => {
            if (e.key === "Enter" || e.key === " ") {
              e.preventDefault();
              selectPropType(prop.id);
            }
          }}
          aria-label={`Select ${prop.label} prop type`}
          aria-pressed={selectedPropType === prop.id}
          title={`${prop.label} - Click to select this prop type`}
        >
          <div class="prop-image-container">
            <img
              src={prop.image}
              alt={prop.label}
              class="prop-image"
              loading="lazy"
            />
          </div>
          <span class="prop-label">{prop.label}</span>
        </button>
      {/each}
    </div>
  </div>
</div>

<style>
  .tab-content {
    width: 100%;
    height: 100%; /* Fill parent */
    max-width: var(--max-content-width, 100%);
    margin: 0 auto;
    container-type: inline-size;
    display: flex; /* Make it a flex container */
    flex-direction: column;
  }

  .prop-container {
    width: 100%;
    flex: 1; /* Grow to fill available space */
    min-height: 0; /* Critical for flex child */
    display: flex;
    flex-direction: column;
  }

  .prop-grid {
    display: grid;
    width: 100%;
    flex: 1; /* Fill parent flex container */
    min-height: 0; /* Critical: allows grid to shrink in flex container */

    /* Use CSS variables calculated from JavaScript */
    grid-template-columns: var(--grid-columns, repeat(3, 1fr));
    grid-template-rows: var(--grid-rows, repeat(4, 1fr)); /* Equal-height rows */

    /* Fluid gap using container query units - scales smoothly with container size */
    gap: clamp(12px, 3cqi, 24px);

    /* Don't center - let items fill cells */
    align-items: stretch; /* Default, but explicit for clarity */
    justify-items: stretch;
  }

  /* Grid items stretch to fill their cells automatically */
  .prop-grid > .prop-button {
    min-height: 0; /* Allow shrinking below content size */
    min-width: 0;
    /* Don't set explicit width/height - let grid cells define size */
  }

  .prop-button {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    background: rgba(255, 255, 255, 0.06);
    border: 2px solid rgba(255, 255, 255, 0.15);
    cursor: pointer;
    transition: all 0.2s ease-out;
    color: rgba(255, 255, 255, 0.85);
    position: relative;
    padding: 10px;
    gap: 6px;
    border-radius: 10px;
    box-sizing: border-box;
  }

  .prop-button:hover {
    background: rgba(255, 255, 255, 0.1);
    border-color: rgba(255, 255, 255, 0.35);
    color: #ffffff;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .prop-button.selected {
    background: rgba(99, 102, 241, 0.25);
    border-color: #6366f1;
    color: #ffffff;
    box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
  }

  .prop-button:focus-visible {
    outline: 2px solid #6366f1;
    outline-offset: 2px;
    border-color: rgba(99, 102, 241, 0.6);
  }

  .prop-button:active {
    transform: scale(0.98);
  }

  .prop-image-container {
    display: flex;
    align-items: center;
    justify-content: center;
    flex: 1;
    width: 100%;
    min-height: 0;
  }

  .prop-image {
    max-width: 100%;
    max-height: 100%;
    opacity: 0.85;
    transition: opacity 0.2s ease;
  }

  .prop-button:hover .prop-image {
    opacity: 1;
  }

  .prop-button.selected .prop-image {
    opacity: 1;
  }

  .prop-label {
    text-align: center;
    line-height: 1.2;
    word-break: break-word;
    white-space: normal;
    max-width: 100%;
    font-size: 11px;
    font-weight: 500;
    flex-shrink: 0;
  }
</style>
