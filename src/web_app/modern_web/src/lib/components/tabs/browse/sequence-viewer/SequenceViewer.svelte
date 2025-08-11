<!-- SequenceViewer.svelte - Main coordinator component using pure Svelte 5 runes -->
<script lang="ts">
	import type { SequenceData } from '$domain/SequenceData';
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';
	import { ThumbnailService } from '$lib/services/implementations/ThumbnailService';
	import { slide } from 'svelte/transition';
	import SequenceActions from './SequenceActions.svelte';
	import SequenceDetails from './SequenceDetails.svelte';
	import SequenceEmptyState from './SequenceEmptyState.svelte';
	import SequenceImageViewer from './SequenceImageViewer.svelte';
	import SequenceViewerHeader from './SequenceViewerHeader.svelte';

	interface Props {
		sequence?: (SequenceData & BrowseSequenceMetadata & { variations?: unknown[] }) | null;
		onBackToBrowser?: () => void;
		onSequenceAction?: (action: string, sequence: SequenceData) => void;
	}

	let { sequence = null, onBackToBrowser, onSequenceAction }: Props = $props();

	// Thumbnail service for generating image URLs
	const thumbnailService = new ThumbnailService();

	// Variation state management with runes
	let currentVariationIndex = $state(0);

	// Reset variation index when sequence changes
	$effect(() => {
		if (sequence) {
			currentVariationIndex = 0;
		}
	});

	// Derived current variation with proper image URL from thumbnails
	let currentVariation = $derived.by(() => {
		if (!sequence) return undefined;

		// Check if sequence has variations with imageUrl (legacy format)
		const legacyVariation = sequence?.variations?.[currentVariationIndex] as
			| { imageUrl?: string }
			| undefined;
		if (legacyVariation?.imageUrl) {
			return legacyVariation;
		}

		// Check if sequence has direct imageUrl (legacy format)
		const legacySequence = sequence as { imageUrl?: string };
		if (legacySequence.imageUrl) {
			return { imageUrl: legacySequence.imageUrl };
		}

		// Use thumbnails array from BrowseSequenceMetadata (new format)
		if (sequence.thumbnails && sequence.thumbnails.length > 0) {
			const thumbnailPath =
				sequence.thumbnails[currentVariationIndex] || sequence.thumbnails[0];
			if (thumbnailPath) {
				const imageUrl = thumbnailService.getThumbnailUrl(sequence.id, thumbnailPath);
				return { imageUrl };
			}
		}

		return undefined;
	});

	// Variation navigation handlers
	function nextVariation() {
		if (!sequence) return;

		// Handle legacy variations
		if (sequence.variations && currentVariationIndex < sequence.variations.length - 1) {
			currentVariationIndex++;
			return;
		}

		// Handle thumbnails array
		if (sequence.thumbnails && currentVariationIndex < sequence.thumbnails.length - 1) {
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
		if (sequence) {
			onSequenceAction?.(action, sequence);
		}
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
