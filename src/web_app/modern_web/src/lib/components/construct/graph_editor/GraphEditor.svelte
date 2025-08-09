<!--
Graph Editor - Svelte Version
Professional Graph Editor for TKA - Clean Component Architecture

A visually rich, pictograph-centered graph editor component designed for embedded use
in stack widgets. Features a modern UI with pictograph display and dual adjustment panels.
-->
<script lang="ts">
	import PictographDisplaySection from './PictographDisplaySection.svelte';
	import MainAdjustmentPanel from './MainAdjustmentPanel.svelte';

	// Types
	interface BeatData {
		beat: number;
		letter?: string;
		pictograph_data?: any;
		metadata?: Record<string, any>;
	}

	interface SequenceData {
		name: string;
		beats: BeatData[];
		metadata?: Record<string, any>;
	}

	// Props
	interface Props {
		workbenchWidth?: number;
		workbenchHeight?: number;
	}

	let { workbenchWidth = 800, workbenchHeight = 600 }: Props = $props();

	// State
	let currentSequence: SequenceData | null = $state(null);
	let selectedBeatIndex: number | null = $state(null);
	let selectedBeatData: BeatData | null = $state(null);

	// Component references
	let pictographDisplayRef: PictographDisplaySection;
	let adjustmentPanelRef: MainAdjustmentPanel;

	// Event handlers
	function onPictographUpdated(beatIndex: number, beatData: BeatData) {
		console.log('📸 [GRAPH_EDITOR] Pictograph updated for beat:', beatIndex);

		// Emit custom event for parent to handle
		const event = new CustomEvent('beatModified', {
			detail: { beatIndex, beatData },
		});
		document.dispatchEvent(event);
	}

	function onOrientationChanged(color: string, orientation: any) {
		console.log('🧭 [GRAPH_EDITOR] Orientation changed:', color, orientation);

		// Create orientation data for compatibility
		const orientationData = {
			color,
			orientation: orientation,
			type: 'orientation_change',
		};

		// Emit custom event
		const event = new CustomEvent('arrowSelected', {
			detail: orientationData,
		});
		document.dispatchEvent(event);

		// Trigger pictograph update immediately
		if (selectedBeatData && pictographDisplayRef) {
			pictographDisplayRef.updatePictographOnly(selectedBeatIndex || 0, selectedBeatData);
		}
	}

	function onTurnAmountChanged(color: string, turnAmount: number) {
		console.log('🔄 [GRAPH_EDITOR] Turn amount changed:', color, turnAmount);

		const turnData = {
			color,
			turn_amount: turnAmount,
			type: 'turn_change',
		};

		// Emit custom event
		const event = new CustomEvent('arrowSelected', {
			detail: turnData,
		});
		document.dispatchEvent(event);
	}

	function onBeatDataUpdated(beatData: BeatData) {
		console.log('📊 [GRAPH_EDITOR] Beat data updated:', beatData);

		selectedBeatData = beatData;

		// Emit custom event
		const event = new CustomEvent('beatModified', {
			detail: {
				beatIndex: selectedBeatIndex || 0,
				beatData,
			},
		});
		document.dispatchEvent(event);
	}

	// Public API methods
	export function setSequence(sequence: SequenceData | null): boolean {
		try {
			currentSequence = sequence;
			console.log('📂 [GRAPH_EDITOR] Sequence set:', sequence?.name || 'None');
			return true;
		} catch (error) {
			console.error('❌ [GRAPH_EDITOR] Error setting sequence:', error);
			return false;
		}
	}

	export function updateCurrentSequence(sequence: SequenceData | null): boolean {
		return setSequence(sequence);
	}

	export function setSelectedBeatData(beatIndex: number, beatData: BeatData | null): boolean {
		try {
			selectedBeatIndex = beatIndex;
			selectedBeatData = beatData;

			// Update components
			if (pictographDisplayRef) {
				pictographDisplayRef.updateDisplay(beatIndex, beatData);
			}
			if (adjustmentPanelRef) {
				adjustmentPanelRef.setBeatData(beatIndex, beatData);
			}

			console.log('✅ [GRAPH_EDITOR] Beat data set successfully:', beatIndex);
			return true;
		} catch (error) {
			console.error('❌ [GRAPH_EDITOR] Error setting beat data:', error);
			return false;
		}
	}

	export function getCurrentSequence(): SequenceData | null {
		return currentSequence;
	}

	export function getSelectedBeatIndex(): number | null {
		return selectedBeatIndex;
	}
</script>

<div class="graph-editor" style="width: {workbenchWidth}px; height: 300px;">
	<!-- Pictograph Display Section (top 65%) -->
	<div class="pictograph-section">
		<PictographDisplaySection bind:this={pictographDisplayRef} {onPictographUpdated} />
	</div>

	<!-- Main Adjustment Panel (bottom 35%) -->
	<div class="adjustment-section">
		<MainAdjustmentPanel
			bind:this={adjustmentPanelRef}
			{onOrientationChanged}
			{onTurnAmountChanged}
			{onBeatDataUpdated}
		/>
	</div>
</div>

<style>
	.graph-editor {
		display: flex;
		flex-direction: column;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		backdrop-filter: blur(10px);
		padding: 10px;
		gap: 10px;
		overflow: hidden;
	}

	.pictograph-section {
		flex: 65; /* 65% of available space */
		min-height: 150px;
		overflow: hidden;
	}

	.adjustment-section {
		flex: 35; /* 35% of available space */
		min-height: 100px;
		overflow: hidden;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.graph-editor {
			height: auto;
			min-height: 400px;
		}

		.pictograph-section {
			flex: 60;
		}

		.adjustment-section {
			flex: 40;
		}
	}
</style>
