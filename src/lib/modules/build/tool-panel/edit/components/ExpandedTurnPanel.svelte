<!-- ExpandedTurnPanel - REFACTORED with Design Tokens -->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from '$shared';
  import { resolve, TYPES } from '$shared';
  import { onMount } from 'svelte';
  import type { ITurnControlService } from '../services/TurnControlService';

  // Props
  const {
    color,
    currentBeatData,
    layoutMode = 'comfortable',
    onTurnAmountChanged,
    onEditTurnsRequested,
    onCollapse
  } = $props<{
    color: 'blue' | 'red';
    currentBeatData: BeatData | null;
    layoutMode?: 'compact' | 'balanced' | 'comfortable';
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
    onEditTurnsRequested: () => void;
    onCollapse: () => void;
  }>();

  // Services
  const turnControlService = resolve(TYPES.ITurnControlService) as ITurnControlService;
  let hapticService: IHapticFeedbackService;

  // Display helpers
  const displayLabel = $derived(() => color === 'blue' ? 'Left' : 'Right');

  function getCurrentTurnValue(): number {
    return turnControlService.getCurrentTurnValue(currentBeatData, color);
  }

  function getTurnValue(): string {
    const turnValue = getCurrentTurnValue();
    return turnControlService.getTurnValue(turnValue);
  }

  function getMotionType(): string {
    if (!currentBeatData) return 'Static';
    const motion = color === 'blue' ? currentBeatData.motions?.blue : currentBeatData.motions?.red;
    if (!motion) return 'Static';
    const type = motion.motionType || 'static';
    return type.charAt(0).toUpperCase() + type.slice(1);
  }

  function getRotationDirection(): string {
    if (!currentBeatData) return 'NO_ROTATION';
    const motion = color === 'blue' ? currentBeatData.motions?.blue : currentBeatData.motions?.red;
    if (!motion) return 'NO_ROTATION';
    return motion.rotationDirection || 'NO_ROTATION';
  }

  function shouldShowRotationButtons(): boolean {
    const rotDir = getRotationDirection();
    return rotDir !== 'NO_ROTATION';
  }

  function canDecrementTurn(): boolean {
    const turnValue = getCurrentTurnValue();
    return turnControlService.canDecrementTurn(turnValue);
  }

  function canIncrementTurn(): boolean {
    const turnValue = getCurrentTurnValue();
    return turnControlService.canIncrementTurn(turnValue);
  }

  // Handlers
  function handleTurnDecrement() {
    const currentValue = getCurrentTurnValue();
    const newValue = turnControlService.decrementTurn(currentValue);
    hapticService?.trigger("selection");
    onTurnAmountChanged(color, newValue);
    console.log(`${color} turn decremented to ${newValue}`);
  }

  function handleTurnIncrement() {
    const currentValue = getCurrentTurnValue();
    const newValue = turnControlService.incrementTurn(currentValue);
    hapticService?.trigger("selection");
    onTurnAmountChanged(color, newValue);
    console.log(`${color} turn incremented to ${newValue}`);
  }

  function handleTurnLabelClick() {
    hapticService?.trigger("selection");
    console.log(`${color} turn label clicked - opening modal`);
    onEditTurnsRequested();
  }

  function handleRotationDirectionToggle(direction: string) {
    hapticService?.trigger("selection");
    console.log(`${color} rotation direction toggled to ${direction}`);
    // TODO: Implement rotation direction change handler
  }

  function handleClose() {
    hapticService?.trigger("selection");
    onCollapse();
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });
</script>

<div
  class="turn-panel"
  class:blue={color === 'blue'}
  class:red={color === 'red'}
  class:compact={layoutMode === 'compact'}
  class:balanced={layoutMode === 'balanced'}
  class:comfortable={layoutMode === 'comfortable'}
  data-testid={`expanded-turn-panel-${color}`}
>
  <!-- Header -->
  <div class="turn-header">
    <div class="turn-title">
      <span class="turn-label">{displayLabel()}</span>
      <span class="motion-badge">{getMotionType()}</span>
    </div>
    <button
      class="close-btn"
      onclick={handleClose}
      aria-label="Close panel"
    >
      <i class="fas fa-times"></i>
    </button>
  </div>

  <!-- Main controls -->
  <div class="turn-controls">
    <button
      class="turn-btn decrement"
      onclick={handleTurnDecrement}
      disabled={!canDecrementTurn()}
      aria-label="Decrease turn amount"
    >
      <i class="fas fa-minus"></i>
    </button>

    <button
      class="turn-display"
      onclick={handleTurnLabelClick}
      aria-label="Select specific turn amount"
    >
      {getTurnValue()}
    </button>

    <button
      class="turn-btn increment"
      onclick={handleTurnIncrement}
      disabled={!canIncrementTurn()}
      aria-label="Increase turn amount"
    >
      <i class="fas fa-plus"></i>
    </button>
  </div>

  <!-- Rotation controls (conditional) -->
  {#if shouldShowRotationButtons()}
    <div class="rotation-section">
      <span class="rotation-label">Rotation:</span>
      <div class="rotation-btns">
        <button
          class="rotation-btn"
          class:active={getRotationDirection() === 'COUNTER_CLOCKWISE'}
          onclick={() => handleRotationDirectionToggle('COUNTER_CLOCKWISE')}
          aria-label="Counter-clockwise rotation"
        >
          <i class="fas fa-undo"></i>
        </button>
        <button
          class="rotation-btn"
          class:active={getRotationDirection() === 'CLOCKWISE'}
          onclick={() => handleRotationDirectionToggle('CLOCKWISE')}
          aria-label="Clockwise rotation"
        >
          <i class="fas fa-redo"></i>
        </button>
      </div>
    </div>
  {/if}
</div>

<style>
  /* Base panel */
  .turn-panel {
    flex: 1;
    display: flex;
    flex-direction: column;
    border-radius: 12px;

    /* Smooth height transition for expansion/collapse */
    max-height: 500px; /* Large enough to accommodate all content */
    overflow: hidden;
    transition: max-height var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1)),
                opacity var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1)),
                transform var(--transition-normal, 0.3s cubic-bezier(0.4, 0, 0.2, 1));

    /* Initial animation when first rendered */
    animation: expandIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  }

  /* Compact mode (Desktop) */
  .turn-panel.compact {
    gap: 8px;
    padding: 8px;
    border-width: 2px;
    border-radius: 8px;
  }

  /* Balanced mode (Tablet) */
  .turn-panel.balanced {
    gap: 10px;
    padding: 12px;
    border-width: 3px;
    border-radius: 10px;
  }

  /* Comfortable mode (Mobile) */
  .turn-panel.comfortable {
    gap: 12px;
    padding: 16px;
    border-width: 4px;
    border-radius: 12px;
  }

  /* Color variants */
  .turn-panel.blue {
    border-color: #3b82f6;
    border-style: solid;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, white 100%);
  }

  .turn-panel.red {
    border-color: #ef4444;
    border-style: solid;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, white 100%);
  }

  @keyframes expandIn {
    from {
      opacity: 0;
      transform: scale(0.95);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }

  /* Header */
  .turn-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 2px solid rgba(0, 0, 0, 0.1);
  }

  .turn-panel.compact .turn-header {
    padding-bottom: 6px;
  }

  .turn-panel.balanced .turn-header {
    padding-bottom: 8px;
  }

  .turn-panel.comfortable .turn-header {
    padding-bottom: 10px;
  }

  .turn-title {
    display: flex;
    align-items: center;
    gap: 12px;
  }

  .turn-label {
    font-weight: 700;
  }

  .turn-panel.compact .turn-label {
    font-size: 14px;
  }

  .turn-panel.balanced .turn-label {
    font-size: 15px;
  }

  .turn-panel.comfortable .turn-label {
    font-size: 16px;
  }

  .turn-panel.blue .turn-label {
    color: #3b82f6;
  }

  .turn-panel.red .turn-label {
    color: #ef4444;
  }

  .motion-badge {
    background: rgba(0, 0, 0, 0.08);
    border-radius: 6px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: #333;
  }

  .turn-panel.compact .motion-badge {
    padding: 2px 6px;
    font-size: 9px;
  }

  .turn-panel.balanced .motion-badge {
    padding: 2px 6px;
    font-size: 10px;
  }

  .turn-panel.comfortable .motion-badge {
    padding: 3px 8px;
    font-size: 11px;
  }

  .close-btn {
    border: none;
    border-radius: 50%;
    background: rgba(0, 0, 0, 0.08);
    color: #666;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .turn-panel.compact .close-btn {
    width: 28px;
    height: 28px;
    font-size: 14px;
  }

  .turn-panel.balanced .close-btn {
    width: 32px;
    height: 32px;
    font-size: 16px;
  }

  .turn-panel.comfortable .close-btn {
    width: 36px;
    height: 36px;
    font-size: 18px;
  }

  .close-btn:hover {
    background: rgba(0, 0, 0, 0.12);
    transform: scale(1.1);
  }

  .close-btn:active {
    transform: scale(0.95);
  }

  /* Main controls */
  .turn-controls {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
  }

  .turn-btn {
    border-radius: 50%;
    background: white;
    color: black;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .turn-panel.compact .turn-btn {
    width: 36px;
    height: 36px;
    font-size: 16px;
    border-width: 2px;
  }

  .turn-panel.balanced .turn-btn {
    width: 40px;
    height: 40px;
    font-size: 18px;
    border-width: 3px;
  }

  .turn-panel.comfortable .turn-btn {
    width: 48px;
    height: 48px;
    font-size: 20px;
    border-width: 4px;
  }

  .turn-panel.blue .turn-btn {
    border-color: #3b82f6;
    border-style: solid;
  }

  .turn-panel.red .turn-btn {
    border-color: #ef4444;
    border-style: solid;
  }

  .turn-btn:hover:not(:disabled) {
    transform: scale(1.1);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .turn-btn:active:not(:disabled) {
    transform: scale(0.95);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  }

  .turn-btn:disabled {
    opacity: 0.4;
    cursor: not-allowed;
  }

  .turn-display {
    flex: 1;
    background: white;
    color: black;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .turn-panel.compact .turn-display {
    min-width: 48px;
    height: 48px;
    font-size: 24px;
    border-width: 2px;
    border-radius: 8px;
  }

  .turn-panel.balanced .turn-display {
    min-width: 56px;
    height: 56px;
    font-size: 28px;
    border-width: 3px;
    border-radius: 10px;
  }

  .turn-panel.comfortable .turn-display {
    min-width: 64px;
    height: 64px;
    font-size: 32px;
    border-width: 4px;
    border-radius: 12px;
  }

  .turn-panel.blue .turn-display {
    border-color: #3b82f6;
    border-style: solid;
  }

  .turn-panel.red .turn-display {
    border-color: #ef4444;
    border-style: solid;
  }

  .turn-display:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  }

  .turn-display:active {
    transform: scale(0.98);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  }

  /* Rotation controls */
  .rotation-section {
    display: flex;
    align-items: center;
    justify-content: center;
    background: rgba(0, 0, 0, 0.08);
    border-radius: 8px;
  }

  .turn-panel.compact .rotation-section {
    gap: 6px;
    padding: 6px;
  }

  .turn-panel.balanced .rotation-section {
    gap: 8px;
    padding: 8px;
  }

  .turn-panel.comfortable .rotation-section {
    gap: 10px;
    padding: 10px;
  }

  .rotation-label {
    font-weight: 600;
    color: #666;
  }

  .turn-panel.compact .rotation-label {
    font-size: 12px;
  }

  .turn-panel.balanced .rotation-label {
    font-size: 13px;
  }

  .turn-panel.comfortable .rotation-label {
    font-size: 14px;
  }

  .rotation-btns {
    display: flex;
  }

  .turn-panel.compact .rotation-btns {
    gap: 6px;
  }

  .turn-panel.balanced .rotation-btns {
    gap: 8px;
  }

  .turn-panel.comfortable .rotation-btns {
    gap: 10px;
  }

  .rotation-btn {
    border: 3px solid;
    border-radius: 50%;
    background: white;
    color: #666;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .turn-panel.compact .rotation-btn {
    width: 32px;
    height: 32px;
    font-size: 14px;
  }

  .turn-panel.balanced .rotation-btn {
    width: 36px;
    height: 36px;
    font-size: 16px;
  }

  .turn-panel.comfortable .rotation-btn {
    width: 44px;
    height: 44px;
    font-size: 18px;
  }

  .turn-panel.blue .rotation-btn {
    border-color: #3b82f6;
  }

  .turn-panel.red .rotation-btn {
    border-color: #ef4444;
  }

  .rotation-btn:hover {
    transform: scale(1.1);
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.15);
  }

  .turn-panel.blue .rotation-btn.active {
    background: #3b82f6;
    color: white;
  }

  .turn-panel.red .rotation-btn.active {
    background: #ef4444;
    color: white;
  }
</style>
