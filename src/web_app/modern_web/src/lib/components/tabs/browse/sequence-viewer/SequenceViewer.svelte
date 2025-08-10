<!-- SequenceViewer.svelte - Main coordinator component using pure Svelte 5 runes -->
<script lang="ts">
	import { slide } from 'svelte/transition';
	import SequenceActions from './SequenceActions.svelte';
	import SequenceDetails from './SequenceDetails.svelte';
	import SequenceEmptyState from './SequenceEmptyState.svelte';
	import SequenceImageViewer from './SequenceImageViewer.svelte';
	import SequenceViewerHeader from './SequenceViewerHeader.svelte';

	interface Props {
		sequence?: any;
		onBackToBrowser?: () => void;
		onSequenceAction?: (action: string, sequence: any) => void;
	}

	let { sequence = null, onBackToBrowser, onSequenceAction }: Props = $props();

	// Variation state management with runes
	let currentVariationIndex = $state(0);

	// Reset variation index when sequence changes
	$effect(() => {
		if (sequence) {
			currentVariationIndex = 0;
		}
	});

	// Derived current variation
	let currentVariation = $derived(sequence?.variations?.[currentVariationIndex] || sequence);

	// Variation navigation handlers
	function nextVariation() {
		if (
			sequence &&
			sequence.variations &&
			currentVariationIndex < sequence.variations.length - 1
		) {
			currentVariationIndex++;
		}
	}

	function prevVariation() {
		if (currentVariationIndex > 0) {
			currentVariationIndex--;
		}
	}

	// Event handlers
	function handleBackToBrowser() {
		onBackToBrowser?.();
	}

	function handleSequenceAction(action: string) {
		onSequenceAction?.(action, sequence);
	}
</script>

<div class="sequence-viewer-panel">
	{#if sequence}
		<div class="viewer-content" transition:slide={{ duration: 300 }}>
			<SequenceViewerHeader {sequence} onBackToBrowser={handleBackToBrowser} />

			<SequenceImageViewer
				{sequence}
				{currentVariation}
				{currentVariationIndex}
				onNextVariation={nextVariation}
				onPrevVariation={prevVariation}
			/>

			<SequenceDetails {sequence} />

			<SequenceActions onAction={handleSequenceAction} />
		</div>
	{:else}
		<SequenceEmptyState />
	{/if}
</div>

<style>
	.sequence-viewer-panel {
		display: flex;
		flex-direction: column;
		height: 100%;
		background: rgba(255, 255, 255, 0.02);
		overflow: hidden;
	}

	.viewer-content {
		display: flex;
		flex-direction: column;
		height: 100%;
		overflow-y: auto;
		padding: var(--spacing-lg);
		gap: var(--spacing-lg);
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.viewer-content {
			padding: var(--spacing-md);
			gap: var(--spacing-md);
		}
	}
</style>
