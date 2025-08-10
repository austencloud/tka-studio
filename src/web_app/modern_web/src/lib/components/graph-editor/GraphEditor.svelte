<!-- GraphEditor.svelte - Professional Graph Editor ported from desktop -->
<script lang="ts">
	import ModernPictograph from '$lib/components/pictograph/Pictograph.svelte';
	import {
		getCurrentSequence,
		getSelectedBeatData,
		getSelectedBeatIndex,
	} from '$lib/state/sequenceState.svelte';
	import type { BeatData } from '$services/interfaces';
	import { onMount } from 'svelte';
	import MainAdjustmentPanel from './MainAdjustmentPanel.svelte';

	// Props - optional external data
	const { onArrowSelected: _onArrowSelected, onVisibilityChanged: _onVisibilityChanged } =
		$props<{
			onBeatModified?: (beatIndex: number, beatData: BeatData) => void;
			onArrowSelected?: (arrowData: {
				color: string;
				orientation?: string;
				turn_amount?: number;
				type: string;
			}) => void;
			onVisibilityChanged?: (isVisible: boolean) => void;
		}>();

	// Reactive state from stores
	let currentSequence = $derived(getCurrentSequence());
	let selectedBeatIndex = $derived(getSelectedBeatIndex());
	let selectedBeatData = $derived(getSelectedBeatData());

	// Component references
	let modernPictograph = $state<ModernPictograph>();
	let adjustmentPanel = $state<MainAdjustmentPanel>();

	// Internal state
	let errorMessage = $state<string | null>(null);

	// Handle orientation changes
	function handleOrientationChanged(color: string, orientation: string) {
		try {
			const orientationData = {
				color,
				orientation,
				type: 'orientation_change',
			};
			_onArrowSelected?.(orientationData);
			console.log(`Graph Editor: ${color} orientation changed to ${orientation}`);

			// Trigger pictograph update immediately
			if (selectedBeatData && modernPictograph) {
				// ModernPictograph is reactive - no manual update needed
				console.log('Pictograph will update reactively');
			}
		} catch (error) {
			console.error('Error handling orientation change:', error);
			errorMessage = 'Failed to update orientation';
		}
	}

	// Handle turn amount changes
	function handleTurnAmountChanged(color: string, turnAmount: number) {
		try {
			const turnData = {
				color,
				turn_amount: turnAmount,
				type: 'turn_change',
			};
			_onArrowSelected?.(turnData);
			console.log(`Graph Editor: ${color} turn amount changed to ${turnAmount}`);
		} catch (error) {
			console.error('Error handling turn amount change:', error);
			errorMessage = 'Failed to update turn amount';
		}
	}

	// Update components when beat data changes
	$effect(() => {
		if (selectedBeatIndex !== null && selectedBeatData) {
			// ModernPictograph updates reactively via props
			// No manual update needed

			// Update adjustment panel
			if (adjustmentPanel) {
				adjustmentPanel.setBeatData(selectedBeatIndex, selectedBeatData);
			}
		}
	});

	// Clear error message after 5 seconds
	$effect(() => {
		if (errorMessage) {
			const timeout = setTimeout(() => {
				errorMessage = null;
			}, 5000);

			return () => clearTimeout(timeout);
		}
		return undefined;
	});

	onMount(() => {
		console.log('Graph Editor mounted');
		_onVisibilityChanged?.(true);

		return () => {
			_onVisibilityChanged?.(false);
		};
	});
</script>

<div class="graph-editor" data-testid="graph-editor">
	<!-- Error display -->
	{#if errorMessage}
		<div class="error-banner">
			<span>⚠️ {errorMessage}</span>
			<button onclick={() => (errorMessage = null)}>×</button>
		</div>
	{/if}

	<!-- Main content area -->
	<div class="graph-content">
		<!-- Top section: Pictograph Display (65% height) -->
		<div class="pictograph-section">
			<div class="pictograph-header">
				<h3>Pictograph</h3>
				{#if selectedBeatIndex !== null}
					<div class="beat-info">
						<span class="beat-number">Beat {selectedBeatIndex + 1}</span>
						{#if currentSequence}
							<span class="sequence-name">{currentSequence.name}</span>
						{/if}
					</div>
				{/if}
			</div>
			<div class="pictograph-display">
				{#if selectedBeatData?.pictograph_data}
					<ModernPictograph
						bind:this={modernPictograph}
						pictographData={selectedBeatData.pictograph_data}
						beatNumber={selectedBeatIndex || 0}
						onClick={() => console.log('Pictograph clicked')}
					/>
				{:else}
					<div class="no-pictograph">
						<div class="placeholder-icon">🎭</div>
						<p>Select a beat to view its pictograph</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- Bottom section: Adjustment Panel (35% height) -->
		<div class="adjustment-section">
			<MainAdjustmentPanel
				bind:this={adjustmentPanel}
				{selectedBeatIndex}
				{selectedBeatData}
				onOrientationChanged={handleOrientationChanged}
				onTurnAmountChanged={handleTurnAmountChanged}
			/>
		</div>
	</div>
</div>

<style>
	.graph-editor {
		display: flex;
		flex-direction: column;
		width: 100%;
		height: 100%;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 16px;
		overflow: hidden;
		backdrop-filter: blur(10px);
		min-height: 400px;
	}

	.error-banner {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--spacing-sm) var(--spacing-md);
		background: rgba(255, 0, 0, 0.1);
		border-bottom: 1px solid rgba(255, 0, 0, 0.3);
		color: var(--destructive);
		font-size: var(--font-size-sm);
	}

	.error-banner button {
		background: none;
		border: none;
		color: var(--destructive);
		cursor: pointer;
		font-size: var(--font-size-lg);
		padding: 0;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.graph-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		padding: var(--spacing-md);
		gap: var(--spacing-md);
		min-height: 0;
	}

	.pictograph-section {
		flex: 65;
		min-height: 0;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: var(--border-radius);
		overflow: hidden;
		display: flex;
		flex-direction: column;
	}

	.pictograph-header {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--spacing-md);
		background: rgba(255, 255, 255, 0.1);
		border-bottom: 1px solid rgba(255, 255, 255, 0.1);
		flex-shrink: 0;
	}

	.pictograph-header h3 {
		margin: 0;
		color: var(--foreground);
		font-size: var(--font-size-lg);
		font-weight: 600;
	}

	.beat-info {
		display: flex;
		gap: var(--spacing-sm);
		align-items: center;
	}

	.beat-number {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--primary);
		color: var(--primary-foreground);
		border-radius: var(--border-radius-sm);
		font-size: var(--font-size-sm);
		font-weight: 500;
	}

	.sequence-name {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--muted);
		color: var(--muted-foreground);
		border-radius: var(--border-radius-sm);
		font-size: var(--font-size-sm);
		font-weight: 500;
	}

	.pictograph-display {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--spacing-lg);
		min-height: 0;
		max-height: 100%;
		width: 100%;
	}

	.no-pictograph {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		color: var(--muted-foreground);
		gap: var(--spacing-md);
	}

	.placeholder-icon {
		font-size: 3rem;
		opacity: 0.5;
	}

	.no-pictograph p {
		margin: 0;
		font-size: var(--font-size-md);
	}

	.adjustment-section {
		flex: 35;
		min-height: 0;
		background: rgba(255, 255, 255, 0.05);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: var(--border-radius);
		overflow: hidden;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.graph-content {
			padding: var(--spacing-sm);
			gap: var(--spacing-sm);
		}

		.pictograph-section {
			flex: 55;
		}

		.adjustment-section {
			flex: 45;
		}

		.pictograph-header {
			padding: var(--spacing-sm);
			flex-direction: column;
			gap: var(--spacing-xs);
		}

		.beat-info {
			flex-direction: column;
			gap: var(--spacing-xs);
		}

		.pictograph-display {
			padding: var(--spacing-md);
		}
	}

	@media (max-width: 480px) {
		.graph-content {
			flex-direction: column;
		}

		.pictograph-section,
		.adjustment-section {
			flex: none;
			height: 50%;
		}
	}
</style>
