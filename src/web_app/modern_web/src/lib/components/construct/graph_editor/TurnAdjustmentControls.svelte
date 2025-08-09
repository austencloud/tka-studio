<!--
Turn Adjustment Controls - Svelte Version
Modern turn adjustment controls with direct turn value selection.
-->
<script lang="ts">
	import CurrentTurnDisplay from './CurrentTurnDisplay.svelte';
	import TurnValueButtonGrid from './TurnValueButtonGrid.svelte';

	// Types
	interface BeatData {
		beat: number;
		letter?: string;
		pictograph_data?: any;
		metadata?: Record<string, any>;
	}

	// Props
	interface Props {
		onTurnAmountChanged?: (color: string, turnAmount: number) => void;
		onBeatDataUpdated?: (beatData: BeatData) => void;
	}

	let { onTurnAmountChanged, onBeatDataUpdated }: Props = $props();

	// State
	let currentBeatData: BeatData | null = $state(null);
	let blueTurnAmount = $state(0.0);
	let redTurnAmount = $state(0.0);

	// Available turn values (fl = float = 0.25)
	const turnValues = ['fl', '0', '0.5', '1', '1.5', '2', '2.5', '3'];
	const turnValueMap: Record<string, number> = {
		fl: 0.25, // float = quarter turn
		'0': 0.0,
		'0.5': 0.5,
		'1': 1.0,
		'1.5': 1.5,
		'2': 2.0,
		'2.5': 2.5,
		'3': 3.0,
	};

	// Component references
	let blueCurrentDisplayRef: CurrentTurnDisplay;
	let redCurrentDisplayRef: CurrentTurnDisplay;
	let blueGridRef: TurnValueButtonGrid;
	let redGridRef: TurnValueButtonGrid;

	// Handle turn value selection
	function onTurnValueSelected(color: 'blue' | 'red', turnValue: string) {
		const turnAmount = turnValueMap[turnValue];

		// Update internal state
		if (color === 'blue') {
			blueTurnAmount = turnAmount;
			blueCurrentDisplayRef?.setValue(turnValue);
			blueGridRef?.setSelected(turnValue);
		} else {
			redTurnAmount = turnAmount;
			redCurrentDisplayRef?.setValue(turnValue);
			redGridRef?.setSelected(turnValue);
		}

		// Update beat data if available
		if (currentBeatData) {
			updateBeatWithTurnChanges();
		}

		// Emit signal
		onTurnAmountChanged?.(color, turnAmount);
		console.log(
			'🔄 [TURN_CONTROLS]',
			color,
			'turn value selected:',
			turnValue,
			'(' + turnAmount + ')'
		);
	}

	// Update beat data with new turn values
	function updateBeatWithTurnChanges() {
		if (!currentBeatData) return;

		try {
			const updatedBeat = { ...currentBeatData };

			// Update pictograph data motions if they exist
			if (updatedBeat.pictograph_data?.motions) {
				if (updatedBeat.pictograph_data.motions.blue && blueTurnAmount !== 0) {
					updatedBeat.pictograph_data.motions.blue = {
						...updatedBeat.pictograph_data.motions.blue,
						turns: blueTurnAmount,
					};
				}

				if (updatedBeat.pictograph_data.motions.red && redTurnAmount !== 0) {
					updatedBeat.pictograph_data.motions.red = {
						...updatedBeat.pictograph_data.motions.red,
						turns: redTurnAmount,
					};
				}
			}

			currentBeatData = updatedBeat;
			onBeatDataUpdated?.(updatedBeat);
			console.log('📊 [TURN_CONTROLS] Beat data updated with turn changes');
		} catch (error) {
			console.error('❌ [TURN_CONTROLS] Error updating beat with turn changes:', error);
		}
	}

	// Find turn value string from numeric amount
	function findTurnValueString(turnAmount: number): string {
		for (const [valueStr, amount] of Object.entries(turnValueMap)) {
			if (Math.abs(amount - turnAmount) < 0.01) {
				return valueStr;
			}
		}
		return '0'; // Default fallback
	}

	// Update turn displays
	function updateTurnDisplays() {
		const blueValue = findTurnValueString(blueTurnAmount);
		const redValue = findTurnValueString(redTurnAmount);

		blueCurrentDisplayRef?.setValue(blueValue);
		blueGridRef?.setSelected(blueValue);
		redCurrentDisplayRef?.setValue(redValue);
		redGridRef?.setSelected(redValue);
	}

	// Public methods
	export function setBeatData(beatData: BeatData | null) {
		currentBeatData = beatData;

		if (beatData) {
			// Extract current turn amounts from beat data
			if (beatData.pictograph_data?.motions?.blue) {
				blueTurnAmount = beatData.pictograph_data.motions.blue.turns || 0.0;
			} else {
				blueTurnAmount = 0.0;
			}

			if (beatData.pictograph_data?.motions?.red) {
				redTurnAmount = beatData.pictograph_data.motions.red.turns || 0.0;
			} else {
				redTurnAmount = 0.0;
			}
		} else {
			// Reset to defaults
			blueTurnAmount = 0.0;
			redTurnAmount = 0.0;
		}

		// Update UI displays
		updateTurnDisplays();

		console.log('🔄 [TURN_CONTROLS] Beat data set, turn amounts:', {
			blue: blueTurnAmount,
			red: redTurnAmount,
		});
	}
</script>

<div class="turn-adjustment-controls">
	<!-- Blue turn panel (left side) -->
	<div class="turn-panel blue-panel">
		<CurrentTurnDisplay
			bind:this={blueCurrentDisplayRef}
			color="blue"
			initialValue={findTurnValueString(blueTurnAmount)}
		/>

		<TurnValueButtonGrid
			bind:this={blueGridRef}
			color="blue"
			{turnValues}
			{turnValueMap}
			onValueSelected={(value) => onTurnValueSelected('blue', value)}
		/>
	</div>

	<!-- Red turn panel (right side) -->
	<div class="turn-panel red-panel">
		<CurrentTurnDisplay
			bind:this={redCurrentDisplayRef}
			color="red"
			initialValue={findTurnValueString(redTurnAmount)}
		/>

		<TurnValueButtonGrid
			bind:this={redGridRef}
			color="red"
			{turnValues}
			{turnValueMap}
			onValueSelected={(value) => onTurnValueSelected('red', value)}
		/>
	</div>
</div>

<style>
	.turn-adjustment-controls {
		display: flex;
		height: 100%;
		gap: 12px;
		padding: 8px;
		background: transparent;
	}

	.turn-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 10px;
		padding: 12px;
		gap: 10px;
		backdrop-filter: blur(8px);
	}

	.blue-panel {
		border-color: rgba(0, 102, 204, 0.4);
		background: rgba(0, 102, 204, 0.05);
	}

	.red-panel {
		border-color: rgba(204, 0, 0, 0.4);
		background: rgba(204, 0, 0, 0.05);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.turn-adjustment-controls {
			flex-direction: column;
			gap: 8px;
			padding: 6px;
		}

		.turn-panel {
			flex: none;
			min-height: 140px;
			padding: 10px;
			gap: 8px;
		}
	}
</style>
