<!--
Letter Type Selector - Svelte Version
Simple horizontal row of numbered buttons for letter types in freeform mode.
-->
<script lang="ts">
  import { LetterType } from "$domain";

  interface Props {
    initialValue?: Set<LetterType>;
  }

  let {
    initialValue = new Set([
      LetterType.TYPE1,
      LetterType.TYPE2,
      LetterType.TYPE3,
      LetterType.TYPE4,
      LetterType.TYPE5,
      LetterType.TYPE6,
    ]),
  }: Props = $props();

  // State
  let currentValue = $state(new Set(initialValue));

  // Letter type data with exact legacy double border colors
  const letterTypes: Array<{
    type: LetterType;
    number: string;
    primaryColor: string;
    secondaryColor: string;
  }> = [
    {
      type: LetterType.TYPE1,
      number: "1",
      primaryColor: "#36c3ff",
      secondaryColor: "#6F2DA8",
    },
    {
      type: LetterType.TYPE2,
      number: "2",
      primaryColor: "#6F2DA8",
      secondaryColor: "#6F2DA8",
    },
    {
      type: LetterType.TYPE3,
      number: "3",
      primaryColor: "#26e600",
      secondaryColor: "#6F2DA8",
    },
    {
      type: LetterType.TYPE4,
      number: "4",
      primaryColor: "#26e600",
      secondaryColor: "#26e600",
    },
    {
      type: LetterType.TYPE5,
      number: "5",
      primaryColor: "#00b3ff",
      secondaryColor: "#26e600",
    },
    {
      type: LetterType.TYPE6,
      number: "6",
      primaryColor: "#eb7d00",
      secondaryColor: "#eb7d00",
    },
  ];

  // Handle button click
  function toggleLetterType(letterType: LetterType) {
    const newValue = new Set(currentValue);

    if (newValue.has(letterType)) {
      newValue.delete(letterType);
      // Ensure at least one type is selected
      if (newValue.size === 0) {
        newValue.add(letterType);
      }
    } else {
      newValue.add(letterType);
    }

    currentValue = newValue;

    // Dispatch value change
    const event = new CustomEvent("valueChanged", {
      detail: { value: newValue },
    });
    document.dispatchEvent(event);
  }

  // Public methods
  export function setValue(value: Set<LetterType>) {
    currentValue = new Set(value);
  }

  export function getValue() {
    return new Set(currentValue);
  }
</script>

<div class="letter-type-selector">
  <div class="header-label">Filter by type:</div>

  <div class="button-layout">
    {#each letterTypes as { type, number, primaryColor, secondaryColor }}
      <button
        class="type-button"
        class:checked={currentValue.has(type)}
        onclick={() => toggleLetterType(type)}
        style="
					{currentValue.has(type)
          ? `border: 3px solid ${secondaryColor}; outline: 2px solid ${primaryColor}; outline-offset: -1px;`
          : ''}
				"
        type="button"
      >
        {number}
      </button>
    {/each}
  </div>
</div>

<style>
  .letter-type-selector {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 8px;
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
    align-items: center;
    gap: 8px;
  }

  .type-button {
    width: 60px;
    height: 45px;
    background: white;
    border: 2px solid rgba(150, 150, 150, 0.4);
    border-radius: 6px;
    color: black;
    font-size: 14px;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .type-button:hover:not(.checked) {
    background: rgba(240, 240, 240, 1);
    border-color: rgba(180, 180, 180, 0.5);
  }

  .type-button.checked {
    background: white;
    font-weight: bold;
  }

  .type-button.checked:hover {
    background: rgba(250, 250, 250, 1);
  }
</style>
