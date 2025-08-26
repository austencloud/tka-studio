<!--
CAP Type Selector - Svelte Version
Simple row of 4 toggleable buttons for selecting circular arrangement pattern types.
-->
<script lang="ts">
  import { CAPType, CAPComponent } from "$lib/domain";

  interface Props {
    initialValue?: CAPType;
    onvalueChanged?: (value: CAPType) => void;
  }

  let { initialValue = CAPType.STRICT_ROTATED, onvalueChanged }: Props =
    $props();

  // State - track which components are selected
  let selectedComponents = $state(new Set<CAPComponent>());

  // Component data with colors and icons
  const capComponents: Array<{
    component: CAPComponent;
    label: string;
    icon: string;
    color: string;
  }> = [
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
    },
  ];

  // Generate CAP type from selected components
  function generateCAPType(components: Set<CAPComponent>): CAPType {
    if (components.size === 0) return CAPType.STRICT_ROTATED;

    const sorted = Array.from(components).sort();

    // Single components (strict)
    if (sorted.length === 1) {
      switch (sorted[0]) {
        case CAPComponent.ROTATED:
          return CAPType.STRICT_ROTATED;
        case CAPComponent.MIRRORED:
          return CAPType.STRICT_MIRRORED;
        case CAPComponent.SWAPPED:
          return CAPType.STRICT_SWAPPED;
        case CAPComponent.COMPLEMENTARY:
          return CAPType.STRICT_COMPLEMENTARY;
      }
    }

    // Two components - use alphabetical order for consistency
    if (sorted.length === 2) {
      const [first, second] = sorted;
      if (
        first === CAPComponent.COMPLEMENTARY &&
        second === CAPComponent.MIRRORED
      )
        return CAPType.MIRRORED_COMPLEMENTARY;
      if (
        first === CAPComponent.COMPLEMENTARY &&
        second === CAPComponent.ROTATED
      )
        return CAPType.ROTATED_COMPLEMENTARY;
      if (
        first === CAPComponent.COMPLEMENTARY &&
        second === CAPComponent.SWAPPED
      )
        return CAPType.SWAPPED_COMPLEMENTARY;
      if (first === CAPComponent.MIRRORED && second === CAPComponent.ROTATED)
        return CAPType.MIRRORED_ROTATED;
      if (first === CAPComponent.MIRRORED && second === CAPComponent.SWAPPED)
        return CAPType.MIRRORED_SWAPPED;
      if (first === CAPComponent.ROTATED && second === CAPComponent.SWAPPED)
        return CAPType.ROTATED_SWAPPED;
    }

    // Three components
    if (
      sorted.length === 3 &&
      sorted.includes(CAPComponent.MIRRORED) &&
      sorted.includes(CAPComponent.COMPLEMENTARY) &&
      sorted.includes(CAPComponent.ROTATED)
    ) {
      return CAPType.MIRRORED_COMPLEMENTARY_ROTATED;
    }

    // Default fallback
    return CAPType.STRICT_ROTATED;
  }

  // Parse CAP type to extract components (for initialization)
  function parseComponents(capType: CAPType): Set<CAPComponent> {
    const components = new Set<CAPComponent>();

    if (capType.includes("rotated")) components.add(CAPComponent.ROTATED);
    if (capType.includes("mirrored")) components.add(CAPComponent.MIRRORED);
    if (capType.includes("swapped")) components.add(CAPComponent.SWAPPED);
    if (capType.includes("complementary"))
      components.add(CAPComponent.COMPLEMENTARY);

    return components;
  }

  // Initialize from legacy CAP type
  $effect(() => {
    selectedComponents = parseComponents(initialValue);
  });

  // Handle component toggle
  function toggleComponent(component: CAPComponent) {
    const newComponents = new Set(selectedComponents);

    if (newComponents.has(component)) {
      newComponents.delete(component);
      // Ensure at least one component is selected
      if (newComponents.size === 0) {
        newComponents.add(component);
      }
    } else {
      newComponents.add(component);
    }

    selectedComponents = newComponents;
    const capType = generateCAPType(newComponents);
    onvalueChanged?.(capType);
  }

  // Public methods
  export function setValue(value: CAPType) {
    selectedComponents = parseComponents(value);
  }

  export function getValue(): CAPType {
    return generateCAPType(selectedComponents);
  }
</script>

<div class="cap-type-selector">
  <div class="header-label">CAP Components:</div>

  <div class="button-layout">
    {#each capComponents as { component, label, icon, color }}
      <button
        class="cap-button"
        class:checked={selectedComponents.has(component)}
        onclick={() => toggleComponent(component)}
        style="
					{selectedComponents.has(component)
          ? `background: ${color}; border-color: ${color}; color: white;`
          : `border-color: ${color}; color: ${color};`}
				"
        type="button"
      >
        <span class="button-icon">{icon}</span>
        <span class="button-label">{label}</span>
      </button>
    {/each}
  </div>
</div>

<style>
  .cap-type-selector {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    padding: 8px 0;
  }

  .header-label {
    color: rgba(255, 255, 255, 0.9);
    font-size: 14px;
    font-weight: 500;
    text-align: center;
  }

  .button-layout {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    justify-content: center;
    max-width: 100%;
  }

  .cap-button {
    flex: 1;
    min-width: 0;
    max-width: 120px;
    height: 44px;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.2);
    border-radius: 8px;
    color: rgba(255, 255, 255, 0.7);
    font-size: 12px;
    font-weight: 500;
    padding: 6px 8px;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2px;
    text-align: center;
    white-space: nowrap;
    overflow: hidden;
  }

  .cap-button:hover:not(.checked) {
    background: rgba(255, 255, 255, 0.1);
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  }

  .cap-button.checked {
    font-weight: 600;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .button-icon {
    font-size: 16px;
    line-height: 1;
  }

  .button-label {
    font-size: 10px;
    line-height: 1.2;
    font-weight: inherit;
  }

  /* Responsive adjustments */
  @media (max-width: 768px) {
    .button-layout {
      gap: 6px;
    }

    .cap-button {
      min-width: 70px;
      max-width: 90px;
      height: 40px;
      padding: 4px 6px;
    }

    .button-icon {
      font-size: 14px;
    }

    .button-label {
      font-size: 9px;
    }
  }
</style>
