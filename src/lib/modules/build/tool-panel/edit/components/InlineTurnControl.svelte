<!-- InlineTurnControl.svelte - Full turn controls shown inline when space permits -->
<script lang="ts">
  import type { BeatData, IHapticFeedbackService } from '$shared';
  import { resolve, TYPES } from '$shared';
  import { onMount } from 'svelte';
  import type { ITurnControlService } from '../services/TurnControlService';

  // Props
  const {
    color,
    currentBeatData,
    layoutMode = 'compact',
    onTurnAmountChanged,
    onEditTurnsRequested
  } = $props<{
    color: 'blue' | 'red';
    currentBeatData: BeatData | null;
    layoutMode?: 'compact' | 'balanced' | 'comfortable';
    onTurnAmountChanged: (color: string, turnAmount: number) => void;
    onEditTurnsRequested: () => void;
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
  }

  function handleTurnIncrement() {
    const currentValue = getCurrentTurnValue();
    const newValue = turnControlService.incrementTurn(currentValue);
    hapticService?.trigger("selection");
    onTurnAmountChanged(color, newValue);
  }

  function handleTurnLabelClick() {
    hapticService?.trigger("selection");
    onEditTurnsRequested();
  }

  onMount(() => {
    hapticService = resolve<IHapticFeedbackService>(TYPES.IHapticFeedbackService);
  });
</script>

<div
  class="inline-turn-control"
  class:blue={color === 'blue'}
  class:red={color === 'red'}
  class:compact={layoutMode === 'compact'}
  class:balanced={layoutMode === 'balanced'}
  class:comfortable={layoutMode === 'comfortable'}
  data-testid={`inline-turn-control-${color}`}
>
  <!-- Header with side label and motion badge -->
  <div class="control-header">
    <span class="side-label">{displayLabel()}</span>
    <span class="motion-badge">{getMotionType()}</span>
  </div>

  <!-- Turn controls - horizontal on desktop, vertical on mobile -->
  <div class="turn-controls">
    <button
      class="turn-btn decrement-btn"
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
      class="turn-btn increment-btn"
      onclick={handleTurnIncrement}
      disabled={!canIncrementTurn()}
      aria-label="Increase turn amount"
    >
      <i class="fas fa-plus"></i>
    </button>
  </div>
</div>

<style>
  .inline-turn-control {
    flex: 1;
    display: flex;
    flex-direction: column;
    border: 4px solid;
    border-radius: 12px;
    background: white;
    container-type: inline-size; /* Enable container queries for intelligent text sizing */
  }

  /* Layout mode sizing */
  .inline-turn-control.comfortable {
    gap: 12px;
    padding: 16px;
  }

  .inline-turn-control.balanced {
    gap: 10px;
    padding: 12px;
    border-width: 3px;
  }

  .inline-turn-control.compact {
    gap: 8px;
    padding: 10px;
    border-width: 2px;
    border-radius: 8px;
  }

  .inline-turn-control.blue {
    border-color: #3b82f6;
    background: linear-gradient(135deg, rgba(59, 130, 246, 0.05) 0%, white 100%);
  }

  .inline-turn-control.red {
    border-color: #ef4444;
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, white 100%);
  }

  /* Header */
  .control-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-bottom: 8px;
    border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    /* Fixed height prevents layout shifts from text wrapping */
    min-height: 28px;
    gap: 8px; /* Ensure spacing between label and badge */
  }

  .side-label {
    font-weight: 600;
    white-space: nowrap; /* Prevent wrapping */
    /* Fluid typography using container queries - scales down if needed */
    font-size: clamp(10px, 3.5cqw, 16px);
  }

  .inline-turn-control.blue .side-label {
    color: #3b82f6;
  }

  .inline-turn-control.red .side-label {
    color: #ef4444;
  }

  .motion-badge {
    padding: clamp(2px, 0.5cqw, 3px) clamp(4px, 2cqw, 8px);
    background: rgba(0, 0, 0, 0.08);
    border-radius: 4px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    color: #333;
    white-space: nowrap; /* Prevent wrapping */
    /* Fluid typography - scales to fit container, prevents overflow */
    font-size: clamp(7px, 2.2cqw, 11px);
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 50%; /* Don't dominate header */
  }

  /* Turn controls - responsive layout */
  .turn-controls {
    display: flex;
    align-items: center;
    gap: 8px;
    flex: 1;
    justify-content: center;
  }

  /* Desktop: Horizontal layout (minus - display - plus) */
  .inline-turn-control.compact .turn-controls {
    flex-direction: row;
    gap: 10px;
  }

  /* Tablet/Mobile: Vertical layout (plus - display - minus) */
  .inline-turn-control.balanced .turn-controls,
  .inline-turn-control.comfortable .turn-controls {
    flex-direction: column;
    gap: 8px;
  }

  .turn-btn {
    border: 2px solid;
    border-radius: 8px;
    background: white;
    color: black;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
    flex-shrink: 0;
  }

  /* Compact (desktop) - square buttons for horizontal layout */
  .inline-turn-control.compact .turn-btn {
    width: 48px;
    height: 48px;
    font-size: 18px;
    border-width: 2px;
  }

  /* Balanced/Comfortable - full-width buttons for vertical layout */
  .inline-turn-control.balanced .turn-btn {
    width: 100%;
    height: 40px;
    font-size: 18px;
  }

  .inline-turn-control.comfortable .turn-btn {
    width: 100%;
    height: 48px;
    font-size: 20px;
  }

  .inline-turn-control.blue .turn-btn {
    border-color: #3b82f6;
  }

  .inline-turn-control.red .turn-btn {
    border-color: #ef4444;
  }

  .turn-btn:hover:not(:disabled) {
    transform: translateY(-1px);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  }

  .turn-btn:active:not(:disabled) {
    transform: translateY(0);
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  }

  .turn-btn:disabled {
    opacity: 0.3;
    cursor: not-allowed;
  }

  .turn-display {
    border: 3px solid;
    border-radius: 8px;
    background: white;
    color: black;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .turn-display {
    /* Intelligent fluid sizing based on container width */
    font-size: clamp(18px, 6cqw, 32px);
    white-space: nowrap; /* Never wrap turn value */
    overflow: hidden;
    text-overflow: ellipsis;
  }

  /* Compact (desktop) - grows to fill horizontal space */
  .inline-turn-control.compact .turn-display {
    flex: 1;
    min-width: 60px; /* Reduced to allow more flexibility */
    height: 48px;
    border-width: 2px;
  }

  /* Balanced/Comfortable - full width for vertical layout */
  .inline-turn-control.balanced .turn-display {
    width: 100%;
    height: 56px;
  }

  .inline-turn-control.comfortable .turn-display {
    width: 100%;
    height: 64px;
  }

  .inline-turn-control.blue .turn-display {
    border-color: #3b82f6;
  }

  .inline-turn-control.red .turn-display {
    border-color: #ef4444;
  }

  .turn-display:hover {
    transform: scale(1.02);
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
  }

  .turn-display:active {
    transform: scale(0.98);
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  }
</style>
