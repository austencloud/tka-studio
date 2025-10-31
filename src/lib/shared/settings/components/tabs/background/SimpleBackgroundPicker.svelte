<!--
  SimpleBackgroundPicker.svelte - UI for selecting/creating simple backgrounds

  Provides:
  - 4 preset gradients
  - Custom gradient builder (2-4 colors)
  - Randomize button
  - Solid color picker
  - Live preview
-->
<script lang="ts">
  import type { IHapticFeedbackService } from "$shared";
  import { resolve, TYPES } from "$shared";
  import { GradientGeneratorService } from "$shared/background/simple/services/GradientGeneratorService";

  const {
    selectedType,
    backgroundColor,
    gradientColors,
    gradientDirection,
    onUpdate,
  } = $props<{
    selectedType: "solid" | "gradient";
    backgroundColor?: string;
    gradientColors?: string[];
    gradientDirection?: number;
    onUpdate: (settings: {
      type: "solid" | "gradient";
      color?: string;
      colors?: string[];
      direction?: number;
    }) => void;
  }>();

  // Services
  const hapticService = resolve<IHapticFeedbackService>(
    TYPES.IHapticFeedbackService
  );

  // Local state
  let currentType = $state<"solid" | "gradient">(selectedType);
  let currentColor = $state(backgroundColor || "#1a1a2e");
  let currentColors = $state(gradientColors || ["#667eea", "#764ba2"]);
  let currentDirection = $state(gradientDirection || 135);

  // Preset gradients
  const presetGradients = GradientGeneratorService.PRESET_GRADIENTS;

  function handleTypeChange(type: "solid" | "gradient") {
    currentType = type;
    hapticService?.trigger("selection");

    if (type === "solid") {
      onUpdate({ type, color: currentColor });
    } else {
      onUpdate({ type, colors: currentColors, direction: currentDirection });
    }
  }

  function handleColorChange(event: Event) {
    const target = event.target as HTMLInputElement;
    currentColor = target.value;
    onUpdate({ type: "solid", color: currentColor });
  }

  function handlePresetSelect(preset: (typeof presetGradients)[0]) {
    currentColors = [...preset.colors];
    currentDirection = preset.direction;
    currentType = "gradient";
    hapticService?.trigger("selection");
    onUpdate({
      type: "gradient",
      colors: currentColors,
      direction: currentDirection,
    });
  }

  function handleRandomize() {
    const numColors = currentColors.length;
    const randomGradient =
      GradientGeneratorService.generateRandomGradient(numColors);
    currentColors = randomGradient.colors;
    currentDirection = randomGradient.direction;
    hapticService?.trigger("selection");
    onUpdate({
      type: "gradient",
      colors: currentColors,
      direction: currentDirection,
    });
  }

  function handleColorUpdate(index: number, event: Event) {
    const target = event.target as HTMLInputElement;
    currentColors[index] = target.value;
    onUpdate({
      type: "gradient",
      colors: [...currentColors],
      direction: currentDirection,
    });
  }

  function handleAddColor() {
    if (currentColors.length < 4) {
      currentColors = [...currentColors, "#ffffff"];
      hapticService?.trigger("selection");
      onUpdate({
        type: "gradient",
        colors: currentColors,
        direction: currentDirection,
      });
    }
  }

  function handleRemoveColor(index: number) {
    if (currentColors.length > 2) {
      currentColors = currentColors.filter(
        (_: string, i: number) => i !== index
      );
      hapticService?.trigger("selection");
      onUpdate({
        type: "gradient",
        colors: currentColors,
        direction: currentDirection,
      });
    }
  }

  function handleDirectionChange(event: Event) {
    const target = event.target as HTMLInputElement;
    currentDirection = parseInt(target.value);
    onUpdate({
      type: "gradient",
      colors: currentColors,
      direction: currentDirection,
    });
  }

  // Generate preview gradient CSS
  const previewGradient = $derived(() => {
    if (currentType === "solid") {
      return currentColor;
    } else {
      const colorStops = currentColors.join(", ");
      return `linear-gradient(${currentDirection}deg, ${colorStops})`;
    }
  });
</script>

<div class="simple-background-picker">
  <!-- Type selector -->
  <div class="type-selector">
    <button
      class="type-button"
      class:selected={currentType === "solid"}
      onclick={() => handleTypeChange("solid")}
    >
      Solid Color
    </button>
    <button
      class="type-button"
      class:selected={currentType === "gradient"}
      onclick={() => handleTypeChange("gradient")}
    >
      Gradient
    </button>
  </div>

  <!-- Preview -->
  <div class="preview-container">
    <div class="preview" style="background: {previewGradient()}"></div>
  </div>

  {#if currentType === "solid"}
    <!-- Solid color picker -->
    <div class="color-picker-container">
      <label for="solid-color">Choose Color:</label>
      <input
        id="solid-color"
        type="color"
        value={currentColor}
        oninput={handleColorChange}
        class="color-input"
      />
      <span class="color-value">{currentColor}</span>
    </div>
  {:else}
    <!-- Gradient controls -->
    <div class="gradient-controls">
      <!-- Preset gradients -->
      <div class="preset-section">
        <h4>Preset Gradients</h4>
        <div class="preset-grid">
          {#each presetGradients as preset, index}
            <button
              class="preset-card"
              style="background: linear-gradient({preset.direction}deg, {preset.colors.join(
                ', '
              )})"
              onclick={() => handlePresetSelect(preset)}
              aria-label="Preset gradient {index + 1}"
            >
              <span class="preset-checkmark">✓</span>
            </button>
          {/each}
        </div>
      </div>

      <!-- Custom gradient builder -->
      <div class="custom-section">
        <div class="section-header">
          <h4>Custom Gradient</h4>
          <button class="randomize-button" onclick={handleRandomize}>
            🎲 Randomize
          </button>
        </div>

        <!-- Color stops -->
        <div class="color-stops">
          {#each currentColors as color, index}
            <div class="color-stop">
              <input
                type="color"
                value={color}
                oninput={(e) => handleColorUpdate(index, e)}
                class="color-input"
              />
              <span class="color-value">{color}</span>
              {#if currentColors.length > 2}
                <button
                  class="remove-color"
                  onclick={() => handleRemoveColor(index)}
                  aria-label="Remove color {index + 1}"
                >
                  ×
                </button>
              {/if}
            </div>
          {/each}
        </div>

        {#if currentColors.length < 4}
          <button class="add-color-button" onclick={handleAddColor}>
            + Add Color
          </button>
        {/if}

        <!-- Direction slider -->
        <div class="direction-control">
          <label for="gradient-direction">Direction: {currentDirection}°</label>
          <input
            id="gradient-direction"
            type="range"
            min="0"
            max="360"
            step="45"
            value={currentDirection}
            oninput={handleDirectionChange}
            class="direction-slider"
          />
        </div>
      </div>
    </div>
  {/if}
</div>

<style>
  .simple-background-picker {
    width: 100%;
    max-height: 100%; /* Constrain height */
    padding: clamp(12px, 2.5cqh, 20px); /* Reduced padding */
    display: flex;
    flex-direction: column;
    gap: clamp(12px, 1.5cqh, 18px); /* Reduced gap */
    container-type: inline-size;
    container-name: simple-picker;
    overflow-y: auto; /* Enable scrolling */
    overflow-x: hidden;
  }

  .type-selector {
    display: flex;
    gap: 8px;
    justify-content: center;
  }

  .type-button {
    padding: 12px 24px;
    border-radius: 10px;
    border: 1.5px solid rgba(255, 255, 255, 0.25);
    background: rgba(255, 255, 255, 0.06);
    color: #ffffff;
    font-size: clamp(14px, 1.5cqw, 16px);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    min-height: 44px;
  }

  .type-button:hover {
    background: rgba(255, 255, 255, 0.12);
    border-color: rgba(99, 102, 241, 0.5);
    transform: scale(1.02);
  }

  .type-button:active {
    transform: scale(0.98);
  }

  .type-button.selected {
    background: rgba(99, 102, 241, 0.25);
    border-color: #6366f1;
    font-weight: 600;
    box-shadow: 0 0 12px rgba(99, 102, 241, 0.3);
  }

  .preview-container {
    width: 100%;
    display: flex;
    justify-content: center;
  }

  .preview {
    width: 100%;
    max-width: 400px;
    height: clamp(120px, 20cqh, 200px);
    border-radius: 12px;
    border: 2px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  }

  .color-picker-container {
    display: flex;
    align-items: center;
    gap: 12px;
    justify-content: center;
  }

  .color-picker-container label {
    color: #ffffff;
    font-size: clamp(14px, 1.4cqw, 16px);
    font-weight: 500;
  }

  .color-input {
    width: 60px;
    height: 44px;
    border-radius: 8px;
    border: 2px solid rgba(255, 255, 255, 0.25);
    cursor: pointer;
  }

  .color-value {
    font-family: monospace;
    font-size: clamp(12px, 1.2cqw, 14px);
    color: rgba(255, 255, 255, 0.9);
  }

  .gradient-controls {
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .preset-section h4,
  .custom-section h4 {
    font-size: clamp(16px, 1.6cqw, 18px);
    font-weight: 600;
    color: #ffffff;
    margin: 0 0 12px 0;
  }

  .preset-grid {
    display: grid;
    grid-template-columns: repeat(
      2,
      1fr
    ); /* Fixed 2 columns for balanced layout */
    gap: 12px;
  }

  /* Responsive: 4 columns on wider screens */
  @media (min-width: 600px) {
    .preset-grid {
      grid-template-columns: repeat(4, 1fr);
    }
  }

  .preset-card {
    aspect-ratio: 1;
    border-radius: 12px;
    border: 2px solid rgba(255, 255, 255, 0.25);
    cursor: pointer;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
    min-height: 80px; /* Ensure reasonable touch target */
  }

  .preset-card:hover {
    transform: scale(1.05);
    border-color: #6366f1;
    box-shadow: 0 0 16px rgba(99, 102, 241, 0.4); /* Indigo glow */
  }

  .preset-card:active {
    transform: scale(1); /* Press feedback */
  }

  .preset-checkmark {
    position: absolute;
    top: 4px;
    right: 4px;
    background: white;
    border-radius: 50%;
    width: 24px;
    height: 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.2s;
  }

  .preset-card:hover .preset-checkmark {
    opacity: 1;
  }

  .section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .randomize-button {
    padding: 8px 16px;
    border-radius: 8px;
    border: 1.5px solid #6366f1;
    background: rgba(99, 102, 241, 0.2);
    color: #ffffff;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .randomize-button:hover {
    background: rgba(99, 102, 241, 0.3);
    border-color: #818cf8;
  }

  .color-stops {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .color-stop {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .remove-color {
    width: 32px;
    height: 32px;
    border-radius: 50%;
    border: 1.5px solid #ef4444;
    background: transparent;
    color: #ef4444;
    font-size: 24px;
    line-height: 1;
    cursor: pointer;
    transition: all 0.2s;
  }

  .remove-color:hover {
    background: rgba(239, 68, 68, 0.2);
  }

  .add-color-button {
    padding: 10px 20px;
    border-radius: 8px;
    border: 1.5px dashed #6366f1;
    background: transparent;
    color: #6366f1;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
  }

  .add-color-button:hover {
    background: rgba(99, 102, 241, 0.1);
  }

  .direction-control {
    display: flex;
    flex-direction: column;
    gap: 8px;
  }

  .direction-control label {
    color: #ffffff;
    font-size: clamp(14px, 1.4cqw, 16px);
    font-weight: 500;
  }

  .direction-slider {
    width: 100%;
    height: 8px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.15);
    outline: none;
    cursor: pointer;
  }

  .direction-slider::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #6366f1;
    cursor: pointer;
  }

  .direction-slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #6366f1;
    cursor: pointer;
    border: none;
  }
</style>
