<!--
Main Adjustment Panel - Svelte Version
Orchestrates the stacked widget switching between orientation and turn controls.
-->
<script lang="ts">
	import DualOrientationPicker from './DualOrientationPicker.svelte';
	import TurnAdjustmentControls from './TurnAdjustmentControls.svelte';

	// Types
	interface BeatData {
		beat: number;
		letter?: string;
		pictograph_data?: any;
		metadata?: Record<string, any>;
	}

	// Props
	interface Props {
		onOrientationChanged?: (color: string, orientation: any) => void;
		onTurnAmountChanged?: (color: string, turnAmount: number) => void;
		onBeatDataUpdated?: (beatData: BeatData) => void;
	}

	let { onOrientationChanged, onTurnAmountChanged, onBeatDataUpdated }: Props = $props();

	// State
	let currentBeatData: BeatData | null = $state(null);
	let currentBeatIndex: number | null = $state(null);
	let currentPanelMode: 'orientation' | 'turns' = $state('orientation');

	// Component references
	let orientationPickerRef: DualOrientationPicker;
	let turnControlsRef: TurnAdjustmentControls;

	// Determine panel mode based on beat type
	function determinePanelMode(
		beatIndex: number,
		beatData: BeatData | null
	): 'orientation' | 'turns' {
		if (!beatData) {
			return 'orientation';
		}

		// Check for start position indicators
		const isStartPosition =
			// Explicit start position index
			beatIndex === -1 ||
			// Check metadata for start position marker
			beatData.metadata?.is_start_position ||
			// Check beat number (0 = start position, 1+ = regular beats)
			beatData.beat === 0 ||
			// Check for start position letter
			beatData.letter === 'α' ||
			beatData.letter === 'alpha' ||
			beatData.letter === 'start' ||
			// Check for sequence start position in metadata
			beatData.metadata?.sequence_start_position;

		return isStartPosition ? 'orientation' : 'turns';
	}

	// Show orientation picker panel
	function showOrientationPicker(beatData: BeatData | null) {
		currentPanelMode = 'orientation';
		if (orientationPickerRef) {
			orientationPickerRef.setBeatData(beatData);
		}
	}

	// Show turn controls panel
	function showTurnControls(beatData: BeatData | null) {
		currentPanelMode = 'turns';
		if (turnControlsRef) {
			turnControlsRef.setBeatData(beatData);
		}
	}

	// Handle orientation change from child component
	function handleOrientationChanged(color: string, orientation: any) {
		onOrientationChanged?.(color, orientation);
	}

	// Handle turn amount change from child component
	function handleTurnAmountChanged(color: string, turnAmount: number) {
		onTurnAmountChanged?.(color, turnAmount);
	}

	// Handle beat data update from child components
	function handleBeatDataUpdated(beatData: BeatData) {
		currentBeatData = beatData;
		onBeatDataUpdated?.(beatData);
	}

	// Public methods
	export function setBeatData(beatIndex: number, beatData: BeatData | null) {
		currentBeatIndex = beatIndex;
		currentBeatData = beatData;

		// Determine which panel to show
		const panelMode = determinePanelMode(beatIndex, beatData);

		if (panelMode === 'orientation') {
			showOrientationPicker(beatData);
		} else {
			showTurnControls(beatData);
		}

		console.log(
			'🎛️ [ADJUSTMENT_PANEL] Panel switched to',
			panelMode,
			'mode for beat',
			beatIndex
		);
	}

	export function getCurrentPanelMode(): 'orientation' | 'turns' {
		return currentPanelMode;
	}

	export function forceOrientationMode() {
		showOrientationPicker(currentBeatData);
	}

	export function forceTurnsMode() {
		showTurnControls(currentBeatData);
	}

	export function clearPanels() {
		if (orientationPickerRef) {
			orientationPickerRef.setBeatData(null);
		}
		if (turnControlsRef) {
			turnControlsRef.setBeatData(null);
		}

		currentPanelMode = 'orientation';
		currentBeatData = null;
		currentBeatIndex = null;
	}

	export function getCurrentBeatData(): BeatData | null {
		return currentBeatData;
	}

	export function getCurrentBeatIndex(): number | null {
		return currentBeatIndex;
	}
</script>

<div class="main-adjustment-panel">
	<!-- Context-sensitive panel switching -->
	{#if currentPanelMode === 'orientation'}
		<div class="panel-container" data-panel="orientation">
			<DualOrientationPicker
				bind:this={orientationPickerRef}
				onOrientationChanged={handleOrientationChanged}
				onBeatDataUpdated={handleBeatDataUpdated}
			/>
		</div>
	{:else}
		<div class="panel-container" data-panel="turns">
			<TurnAdjustmentControls
				bind:this={turnControlsRef}
				onTurnAmountChanged={handleTurnAmountChanged}
				onBeatDataUpdated={handleBeatDataUpdated}
			/>
		</div>
	{/if}
</div>

<style>
	.main-adjustment-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow: hidden;
	}

	.panel-container {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-height: 0; /* Allow flexbox to shrink */
	}

	.panel-container[data-panel='orientation'] {
		/* Specific styling for orientation panel if needed */
	}

	.panel-container[data-panel='turns'] {
		/* Specific styling for turn controls panel if needed */
	}

	/* Smooth transitions between panels */
	.panel-container {
		animation: fadeIn 0.3s ease-in-out;
	}

	@keyframes fadeIn {
		from {
			opacity: 0;
			transform: translateY(10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.main-adjustment-panel {
			height: auto;
			min-height: 150px;
		}
	}
</style>
