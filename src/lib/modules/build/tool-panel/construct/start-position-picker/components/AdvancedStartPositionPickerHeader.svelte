<!-- AdvancedStartPositionPickerHeader.svelte - Header with grid mode toggle -->
<script lang="ts">
  import type { GridMode, IHapticFeedbackService } from "$shared";
  import { GridMode as GridModeEnum, resolve, TYPES } from "$shared";

  const {
    currentGridMode,
    onGridModeChange,
    onBack,
  }: {
    currentGridMode: GridMode;
    onGridModeChange: (gridMode: GridMode) => void;
    onBack: () => void;
  } = $props();

  const hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);

  function toggleGridMode() {
    hapticService?.trigger("selection");
    const newMode = currentGridMode === GridModeEnum.DIAMOND ? GridModeEnum.BOX : GridModeEnum.DIAMOND;
    onGridModeChange(newMode);
  }
</script>

<div class="advanced-start-pos-picker-header">
  <button class="back-button" onclick={onBack} aria-label="Go back to start position picker">
    <span class="back-icon">←</span>
  </button>
  <h3 class="title">Variations</h3>
  <button
    class="grid-mode-toggle"
    class:box-mode={currentGridMode === GridModeEnum.BOX}
    onclick={toggleGridMode}
    aria-label="Toggle between Diamond and Box modes"
    title={currentGridMode === GridModeEnum.DIAMOND ? 'Diamond mode' : 'Box mode'}
  >
    <span class="mode-emoji">{currentGridMode === GridModeEnum.DIAMOND ? '◇' : '□'}</span>
  </button>
</div>

<style>
  .advanced-start-pos-picker-header {
    position: relative;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 12px;
    min-height: 48px;
    background: linear-gradient(180deg, rgba(255, 255, 255, 0.12) 0%, rgba(255, 255, 255, 0.02) 100%);
    backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255, 255, 255, 0.15);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .back-button {
    position: absolute;
    left: 8px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.8);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 18px;
    border-radius: 6px;
    min-width: 36px;
    min-height: 36px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Desktop hover - only on hover-capable devices */
  @media (hover: hover) {
    .back-button:hover {
      background: rgba(255, 255, 255, 0.15);
      color: rgba(255, 255, 255, 1);
      border-color: rgba(255, 255, 255, 0.4);
      transform: scale(1.05);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
  }

  /* Mobile/universal active state */
  .back-button:active {
    transform: scale(0.95);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .back-icon {
    display: inline-block;
    font-weight: bold;
  }

  .title {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    margin: 0;
    font-size: 18px;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.9);
    white-space: nowrap;
  }

  .grid-mode-toggle {
    position: absolute;
    right: 8px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    cursor: pointer;
    padding: 6px 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: rgba(255, 255, 255, 0.8);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 18px;
    border-radius: 6px;
    min-width: 36px;
    min-height: 36px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  /* Desktop hover - only on hover-capable devices */
  @media (hover: hover) {
    .grid-mode-toggle:hover {
      background: rgba(255, 255, 255, 0.15);
      border-color: rgba(255, 255, 255, 0.4);
      transform: scale(1.05);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
  }

  /* Mobile/universal active state */
  .grid-mode-toggle:active {
    transform: scale(0.95);
    transition: transform 0.1s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .mode-emoji {
    display: inline-block;
    font-size: 20px;
    line-height: 1;
  }
</style>
