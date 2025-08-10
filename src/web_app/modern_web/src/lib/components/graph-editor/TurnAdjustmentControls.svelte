<!-- TurnAdjustmentControls.svelte - Blue and red turn amount grid controls -->
<script lang="ts">
	import type { BeatData } from '$services/interfaces';
	import { onMount } from 'svelte';
	// Create dispatcher for events
	import { createEventDispatcher } from 'svelte';
	const dispatch = createEventDispatcher();

	// Props
	let { currentBeatData = null }: { currentBeatData?: BeatData | null } = $props();

	// State variables
	let blueTurnAmount = $state(0);
	let redTurnAmount = $state(0);
	let selectedColor = $state<'blue' | 'red' | null>(null);
	let selectedArrow = $state<string | null>(null);

	// Turn amount options
	const turnAmountOptions = [0, 0.5, 1, 1.5, 2, 2.5, 3];

	// Handle turn amount clicks
	function handleTurnAmountClick(color: 'blue' | 'red', turnAmount: number) {
		if (color === 'blue') {
			blueTurnAmount = turnAmount;
		} else {
			redTurnAmount = turnAmount;
		}

		selectedColor = color;
		selectedArrow = `${color}_turn_${turnAmount}`;

		// Dispatch the change event
		dispatch('turnAmountChanged', {
			color,
			turnAmount,
		});

		console.log(`TurnAdjustmentControls: ${color} turn amount set to ${turnAmount}`);
	}

	// Get currently selected arrow
	export function getSelectedArrow(): string | null {
		return selectedArrow;
	}

	// Update turn amounts from beat data
	function updateFromBeatData(beatData: BeatData | null) {
		if (!beatData?.pictograph_data) return;

		const pictograph = beatData.pictograph_data;

		// Update turn amounts from pictograph data
		if (pictograph.motions?.blue?.turns !== undefined) {
			blueTurnAmount =
				typeof pictograph.motions.blue.turns === 'number'
					? pictograph.motions.blue.turns
					: 0;
		}
		if (pictograph.motions?.red?.turns !== undefined) {
			redTurnAmount =
				typeof pictograph.motions.red.turns === 'number' ? pictograph.motions.red.turns : 0;
		}

		console.log('TurnAdjustmentControls: Updated from beat data', {
			blue: blueTurnAmount,
			red: redTurnAmount,
		});
	}

	// Format turn display
	function formatTurnDisplay(turnAmount: number): string {
		if (turnAmount === 0) return '0';
		return turnAmount > 0 ? `+${turnAmount}` : `${turnAmount}`;
	}

	// Get turn description
	function getTurnDescription(turnAmount: number): string {
		if (turnAmount === 0) return 'No turn';
		if (turnAmount > 0) return `${turnAmount} clockwise`;
		return `${Math.abs(turnAmount)} counter-clockwise`;
	}

	// Reactive updates
	$effect(() => {
		updateFromBeatData(currentBeatData);
	});

	onMount(() => {
		console.log('TurnAdjustmentControls mounted');
	});
</script>

<div class="turn-adjustment-controls" data-testid="turn-adjustment-controls">
	<!-- Blue turn controls -->
	<div class="turn-section blue-section">
		<div class="section-header">
			<h4>Blue Prop Turns</h4>
			<div class="current-value">
				<span class="turn-amount">{formatTurnDisplay(blueTurnAmount)}</span>
				<span class="turn-desc">{getTurnDescription(blueTurnAmount)}</span>
			</div>
		</div>
		<div class="turn-grid">
			{#each turnAmountOptions as turnValue}
				<button
					class="turn-btn blue-btn"
					class:active={blueTurnAmount === turnValue && selectedColor === 'blue'}
					class:selected={blueTurnAmount === turnValue}
					onclick={() => handleTurnAmountClick('blue', turnValue)}
				>
					{formatTurnDisplay(turnValue)}
				</button>
			{/each}
		</div>
	</div>

	<!-- Turn direction legend -->
	<div class="turn-legend">
		<div class="legend-item">
			<span class="legend-symbol">+</span>
			<span class="legend-text">Clockwise</span>
		</div>
		<div class="legend-item">
			<span class="legend-symbol">-</span>
			<span class="legend-text">Counter-clockwise</span>
		</div>
		<div class="legend-item">
			<span class="legend-symbol">0</span>
			<span class="legend-text">No turn</span>
		</div>
	</div>

	<!-- Red turn controls -->
	<div class="turn-section red-section">
		<div class="section-header">
			<h4>Red Prop Turns</h4>
			<div class="current-value">
				<span class="turn-amount">{formatTurnDisplay(redTurnAmount)}</span>
				<span class="turn-desc">{getTurnDescription(redTurnAmount)}</span>
			</div>
		</div>
		<div class="turn-grid">
			{#each turnAmountOptions as turnValue}
				<button
					class="turn-btn red-btn"
					class:active={redTurnAmount === turnValue && selectedColor === 'red'}
					class:selected={redTurnAmount === turnValue}
					onclick={() => handleTurnAmountClick('red', turnValue)}
				>
					{formatTurnDisplay(turnValue)}
				</button>
			{/each}
		</div>
	</div>
</div>

<style>
	.turn-adjustment-controls {
		display: flex;
		flex-direction: row;
		gap: var(--spacing-md);
		height: 100%;
	}

	.turn-section {
		flex: 1;
		background: rgba(255, 255, 255, 0.05);
		border-radius: var(--border-radius);
		padding: var(--spacing-md);
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.blue-section {
		border-color: rgba(59, 130, 246, 0.3);
		background: rgba(59, 130, 246, 0.05);
	}

	.red-section {
		border-color: rgba(239, 68, 68, 0.3);
		background: rgba(239, 68, 68, 0.05);
	}

	.section-header {
		margin-bottom: var(--spacing-md);
		padding-bottom: var(--spacing-sm);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	}

	.section-header h4 {
		margin: 0 0 var(--spacing-xs) 0;
		font-size: var(--font-size-md);
		font-weight: 600;
		color: var(--foreground);
	}

	.current-value {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-xs);
	}

	.turn-amount {
		font-size: var(--font-size-lg);
		font-weight: 700;
		color: var(--foreground);
	}

	.turn-desc {
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
		font-style: italic;
	}

	.turn-grid {
		display: grid;
		grid-template-columns: repeat(7, 1fr);
		gap: var(--spacing-xs);
	}

	.turn-btn {
		aspect-ratio: 1;
		padding: var(--spacing-sm);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: var(--border-radius);
		background: rgba(255, 255, 255, 0.05);
		color: var(--foreground);
		font-size: var(--font-size-sm);
		font-weight: 600;
		cursor: pointer;
		transition: all 0.2s ease;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.turn-btn:hover {
		background: rgba(255, 255, 255, 0.1);
		transform: translateY(-1px);
	}

	.blue-btn.selected {
		background: rgba(59, 130, 246, 0.2);
		border-color: rgba(59, 130, 246, 0.5);
		color: rgb(59, 130, 246);
	}

	.red-btn.selected {
		background: rgba(239, 68, 68, 0.2);
		border-color: rgba(239, 68, 68, 0.5);
		color: rgb(239, 68, 68);
	}

	.blue-btn.active {
		background: rgba(59, 130, 246, 0.3);
		border-color: rgb(59, 130, 246);
		box-shadow: 0 0 10px rgba(59, 130, 246, 0.3);
	}

	.red-btn.active {
		background: rgba(239, 68, 68, 0.3);
		border-color: rgb(239, 68, 68);
		box-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
	}

	.turn-legend {
		display: flex;
		flex-direction: column;
		gap: var(--spacing-xs);
		justify-content: center;
		padding: var(--spacing-md);
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: var(--border-radius);
		min-width: 140px;
		flex-shrink: 0;
		align-self: center;
		text-align: center;
	}

	.legend-item {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		font-size: var(--font-size-sm);
	}

	.legend-symbol {
		font-weight: 700;
		color: var(--primary);
		min-width: 16px;
		text-align: center;
	}

	.legend-text {
		color: var(--muted-foreground);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.turn-adjustment-controls {
			flex-direction: column;
			gap: var(--spacing-sm);
		}

		.turn-section {
			padding: var(--spacing-sm);
		}

		.turn-grid {
			grid-template-columns: repeat(4, 1fr);
			gap: var(--spacing-xs);
		}

		.turn-btn {
			padding: var(--spacing-xs);
			font-size: var(--font-size-xs);
		}

		.turn-legend {
			flex-direction: row;
			gap: var(--spacing-xs);
			min-width: unset;
			align-self: stretch;
		}
	}

	@media (max-width: 480px) {
		.section-header {
			flex-direction: column;
			align-items: flex-start;
			gap: var(--spacing-xs);
		}

		.current-value {
			align-self: flex-end;
		}

		.turn-legend {
			flex-direction: column;
			gap: var(--spacing-xs);
		}
	}
</style>
