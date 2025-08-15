<!--
	Codex Control Panel Component

	Provides control buttons and orientation selector for codex operations.
	Matches desktop CodexControlPanel functionality with rotate, mirror, 
	color swap buttons and orientation selector.
-->
<script lang="ts">
  // Props
  interface Props {
    onRotate?: () => void;
    onMirror?: () => void;
    onColorSwap?: () => void;
    onOrientationChange?: (orientation: string) => void;
    currentOrientation?: string;
  }

  let {
    onRotate,
    onMirror,
    onColorSwap,
    onOrientationChange,
    currentOrientation = "Diamond",
  }: Props = $props();

  // Available orientations (matches desktop options)
  const orientations = ["Diamond", "Box", "Skewed"];

  // Handle orientation change
  function handleOrientationChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    onOrientationChange?.(target.value);
  }

  // Button click handlers
  function handleRotateClick() {
    console.log("🔄 Rotate button clicked");
    onRotate?.();
  }

  function handleMirrorClick() {
    console.log("🪞 Mirror button clicked");
    onMirror?.();
  }

  function handleColorSwapClick() {
    console.log("⚫⚪ Color swap button clicked");
    onColorSwap?.();
  }
</script>

<div class="codex-control-panel">
  <!-- Orientation Selector Section -->
  <div class="orientation-section">
    <label for="orientation-selector" class="orientation-label"
      >Orientation:</label
    >
    <select
      id="orientation-selector"
      class="orientation-selector"
      value={currentOrientation}
      onchange={handleOrientationChange}
    >
      {#each orientations as orientation}
        <option value={orientation}>{orientation}</option>
      {/each}
    </select>
  </div>

  <!-- Control Buttons Section -->
  <div class="control-buttons">
    <button
      class="control-button rotate-button"
      onclick={handleRotateClick}
      title="Rotate all pictographs 90° clockwise"
    >
      <span class="button-icon">↻</span>
    </button>

    <button
      class="control-button mirror-button"
      onclick={handleMirrorClick}
      title="Mirror all pictographs vertically"
    >
      <span class="button-icon">⟷</span>
    </button>

    <button
      class="control-button color-swap-button"
      onclick={handleColorSwapClick}
      title="Swap red and blue colors"
    >
      <span class="button-icon">⚊⚋</span>
    </button>
  </div>
</div>

<style>
  .codex-control-panel {
    display: flex;
    flex-direction: column;
    gap: var(--desktop-spacing-lg);
    padding: var(--desktop-spacing-lg);
    background: var(--desktop-bg-secondary);
    border: 1px solid var(--desktop-border-secondary);
    border-radius: var(--desktop-border-radius);
    margin-bottom: var(--desktop-spacing-md);
  }

  .orientation-section {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: var(--desktop-spacing-md);
  }

  .orientation-label {
    color: var(--desktop-text-primary);
    font-family: var(--desktop-font-family);
    font-size: var(--desktop-font-size-sm);
    font-weight: bold;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  .orientation-selector {
    padding: var(--desktop-spacing-sm) var(--desktop-spacing-md);
    background: var(--desktop-bg-tertiary);
    border: 2px solid var(--desktop-border-secondary);
    border-radius: var(--desktop-border-radius-xs);
    color: var(--desktop-text-primary);
    font-family: var(--desktop-font-family);
    font-size: var(--desktop-font-size-sm);
    min-width: 80px;
    cursor: pointer;
    outline: none;
    transition: all var(--desktop-transition-normal);
  }

  .orientation-selector:hover {
    border-color: var(--desktop-border-primary);
    background: var(--desktop-bg-secondary);
  }

  .orientation-selector:focus {
    border-color: var(--desktop-primary-blue-border);
  }

  .control-buttons {
    display: flex;
    justify-content: center;
    gap: var(--desktop-spacing-md);
  }

  .control-button {
    width: 40px;
    height: 40px;
    background: var(--desktop-bg-tertiary);
    border: 2px solid var(--desktop-border-secondary);
    border-radius: var(--desktop-border-radius-xs);
    color: var(--desktop-text-primary);
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: var(--desktop-font-size-lg);
    transition: all var(--desktop-transition-normal);
    position: relative;
    overflow: hidden;
  }

  .control-button:hover {
    background: var(--desktop-bg-secondary);
    border-color: var(--desktop-border-primary);
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }

  .control-button:active {
    background: var(--desktop-bg-primary);
    border-color: var(--desktop-border-primary);
    transform: translateY(0);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  }

  .button-icon {
    display: block;
    line-height: 1;
    text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
  }

  /* Specific button styling */
  .rotate-button:hover {
    border-color: var(--desktop-primary-blue-border);
  }

  .mirror-button:hover {
    border-color: var(--desktop-primary-green-border);
  }

  .color-swap-button:hover {
    border-color: var(--desktop-primary-purple-border);
  }

  /* Ripple effect for button clicks */
  .control-button::after {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 0;
    height: 0;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.3);
    transform: translate(-50%, -50%);
    transition:
      width 0.3s,
      height 0.3s;
  }

  .control-button:active::after {
    width: 60px;
    height: 60px;
  }

  /* Responsive design */
  @media (max-width: 768px) {
    .codex-control-panel {
      padding: var(--desktop-spacing-md);
      gap: var(--desktop-spacing-md);
    }

    .control-button {
      width: 36px;
      height: 36px;
      font-size: var(--desktop-font-size-base);
    }

    .orientation-selector {
      padding: var(--desktop-spacing-xs) var(--desktop-spacing-sm);
      font-size: var(--desktop-font-size-xs);
      min-width: 70px;
    }
  }
</style>
