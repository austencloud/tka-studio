<!--
	BuildTabContent.svelte

	Build tab content component extracted from ConstructTab.
	Handles the conditional logic for showing either StartPositionPicker or OptionPicker
	based on the current sequence state.
-->
<script lang="ts">
	import { constructTabEventService } from '$services/implementations/ConstructTabEventService';
	import type { BeatData, PictographData } from '$services/interfaces';
	import { constructTabState } from '$stores/constructTabState.svelte';
	import OptionPickerContainer from './OptionPickerContainer.svelte';
	import StartPositionPicker from './StartPositionPicker.svelte';

	console.log('🎯 BuildTabContent script is being processed');

	// Simple debugging
	console.log('🎯 constructTabState available:', !!constructTabState);

	// Reactive state from store
	let shouldShowStartPositionPicker = $derived(constructTabState.shouldShowStartPositionPicker);
	let currentSequence = $derived(constructTabState.currentSequence);
	let gridMode = $derived(constructTabState.gridMode);

	// Add debugging for the reactive values
	$effect(() => {
		console.log(
			'🔍 BuildTabContent shouldShowStartPositionPicker:',
			shouldShowStartPositionPicker
		);
		console.log('🔍 BuildTabContent currentSequence exists:', !!currentSequence);
	});

	// Event handlers
	async function handleStartPositionSelected(startPosition: BeatData) {
		await constructTabEventService.handleStartPositionSelected(startPosition);
	}

	async function handleOptionSelected(option: PictographData) {
		await constructTabEventService.handleOptionSelected(option);
	}
</script>

<div class="build-tab-content" data-testid="build-tab-content">
	{#if shouldShowStartPositionPicker}
		<div class="panel-header">
			<h3>Choose Start Position</h3>
			<p>Select a starting position for your sequence</p>
		</div>
		<div class="panel-content">
			<StartPositionPicker {gridMode} onStartPositionSelected={handleStartPositionSelected} />
		</div>
	{:else}
		<div class="panel-content">
			<OptionPickerContainer onOptionSelected={handleOptionSelected} />
		</div>
	{/if}
</div>

<style>
	.build-tab-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		height: 100%;
		width: 100%;
	}

	.panel-header {
		flex-shrink: 0;
		padding: var(--spacing-lg);
		background: var(--muted) / 30;
		border-bottom: 1px solid var(--border);
		text-align: center;
	}

	.panel-header h3 {
		margin: 0 0 var(--spacing-sm) 0;
		color: var(--foreground);
		font-size: var(--font-size-lg);
		font-weight: 500;
	}

	.panel-header p {
		margin: 0;
		color: var(--muted-foreground);
		font-size: var(--font-size-sm);
	}

	.panel-content {
		flex: 1;
		overflow: auto;
		padding: var(--spacing-lg);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.panel-header {
			padding: var(--spacing-md);
		}
	}
</style>
