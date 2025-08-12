<!-- FullscreenImageViewer.svelte - Image display and navigation for fullscreen viewer -->
<script lang="ts">
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';
	import type { IThumbnailService } from '$services/interfaces';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	let {
		sequence,
		thumbnailService,
		currentVariationIndex = $bindable(0),
	} = $props<{
		sequence?: BrowseSequenceMetadata;
		thumbnailService?: IThumbnailService;
		currentVariationIndex?: number;
	}>();

	// Derived state
	let currentVariation = $derived(
		sequence?.thumbnails && sequence.thumbnails.length > 0
			? sequence.thumbnails[currentVariationIndex] || sequence.thumbnails[0]
			: null
	);

	let currentImageUrl = $derived(currentVariation ? getThumbnailUrl(currentVariation) : '');

	let hasMultipleVariations = $derived(sequence?.thumbnails && sequence.thumbnails.length > 1);

	let canGoPrev = $derived(currentVariationIndex > 0);
	let canGoNext = $derived(
		hasMultipleVariations &&
			sequence &&
			sequence.thumbnails &&
			currentVariationIndex < sequence.thumbnails.length - 1
	);

	// Image loading state
	let isImageLoading = $state(true);
	let imageError = $state(false);

	// Helper function to get thumbnail URL
	function getThumbnailUrl(thumbnailPath: string): string {
		if (!thumbnailService || !sequence) return '';

		try {
			if (thumbnailPath.startsWith('http://') || thumbnailPath.startsWith('https://')) {
				return thumbnailPath;
			}
			return thumbnailService.getThumbnailUrl(sequence.id, thumbnailPath);
		} catch (error) {
			console.error('Error getting thumbnail URL:', error);
			return '';
		}
	}

	// Navigation functions
	function goToPrevVariation() {
		if (canGoPrev) {
			currentVariationIndex--;
			resetImageState();
		}
	}

	function goToNextVariation() {
		if (canGoNext) {
			currentVariationIndex++;
			resetImageState();
		}
	}

	function resetImageState() {
		isImageLoading = true;
		imageError = false;
	}

	function handleImageLoad() {
		isImageLoading = false;
		imageError = false;
	}

	function handleImageError() {
		isImageLoading = false;
		imageError = true;
	}

	// Keyboard navigation
	function handleKeydown(event: KeyboardEvent) {
		if (event.key === 'ArrowLeft') {
			event.preventDefault();
			goToPrevVariation();
		} else if (event.key === 'ArrowRight') {
			event.preventDefault();
			goToNextVariation();
		}
	}

	// Reset state when sequence changes
	$effect(() => {
		if (sequence) {
			currentVariationIndex = 0;
			resetImageState();
		}
	});
</script>

<svelte:window onkeydown={handleKeydown} />

<div class="image-viewer">
	<div class="image-container">
		{#if isImageLoading}
			<div class="loading-spinner">
				<div class="spinner"></div>
				<p>Loading image...</p>
			</div>
		{/if}

		{#if imageError}
			<div class="error-state">
				<div class="error-icon">⚠️</div>
				<p>Failed to load image</p>
				<button class="retry-button" onclick={resetImageState}> Retry </button>
			</div>
		{:else if currentImageUrl}
			<img
				src={currentImageUrl}
				alt={sequence?.word || 'Sequence'}
				class="sequence-image"
				class:loading={isImageLoading}
				onload={handleImageLoad}
				onerror={handleImageError}
			/>
		{/if}

		<!-- Navigation arrows -->
		{#if hasMultipleVariations}
			<button
				class="nav-arrow prev"
				class:disabled={!canGoPrev}
				onclick={goToPrevVariation}
				disabled={!canGoPrev}
				aria-label="Previous variation"
			>
				<span class="arrow-icon">‹</span>
			</button>

			<button
				class="nav-arrow next"
				class:disabled={!canGoNext}
				onclick={goToNextVariation}
				disabled={!canGoNext}
				aria-label="Next variation"
			>
				<span class="arrow-icon">›</span>
			</button>
		{/if}
	</div>

	<!-- Variation indicator -->
	{#if hasMultipleVariations && sequence?.thumbnails}
		<div class="variation-indicator">
			<span class="variation-text">
				Variation {currentVariationIndex + 1} of {sequence.thumbnails.length}
			</span>
			<div class="variation-dots">
				{#each sequence.thumbnails as _, index}
					<button
						class="variation-dot"
						class:active={index === currentVariationIndex}
						onclick={() => {
							currentVariationIndex = index;
							resetImageState();
						}}
						aria-label={`Go to variation ${index + 1}`}
					></button>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	.image-viewer {
		flex: 1;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		padding: 1rem;
		min-height: 0;
		width: 100%;
	}

	.image-container {
		position: relative;
		width: 100%;
		height: 100%;
		max-width: 100%;
		max-height: 80vh;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.sequence-image {
		width: 100%;
		height: 100%;
		max-width: 100%;
		max-height: 100%;
		object-fit: contain;
		border-radius: 8px;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
		transition: opacity 0.3s ease;
	}

	.sequence-image.loading {
		opacity: 0.5;
	}

	.loading-spinner {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		color: white;
	}

	.spinner {
		width: 3rem;
		height: 3rem;
		border: 3px solid rgba(255, 255, 255, 0.3);
		border-top: 3px solid white;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.error-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		color: white;
		text-align: center;
	}

	.error-icon {
		font-size: 3rem;
	}

	.retry-button {
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: white;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.retry-button:hover {
		background: rgba(255, 255, 255, 0.2);
	}

	.nav-arrow {
		position: absolute;
		top: 50%;
		transform: translateY(-50%);
		background: rgba(0, 0, 0, 0.7);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: white;
		width: 3rem;
		height: 3rem;
		border-radius: 50%;
		display: flex;
		align-items: center;
		justify-content: center;
		cursor: pointer;
		transition: all 0.2s ease;
		z-index: 10;
	}

	.nav-arrow:hover:not(.disabled) {
		background: rgba(0, 0, 0, 0.9);
		border-color: rgba(255, 255, 255, 0.4);
		transform: translateY(-50%) scale(1.1);
	}

	.nav-arrow.disabled {
		opacity: 0.3;
		cursor: not-allowed;
	}

	.nav-arrow.prev {
		left: -4rem;
	}

	.nav-arrow.next {
		right: -4rem;
	}

	.arrow-icon {
		font-size: 1.5rem;
		font-weight: bold;
	}

	.variation-indicator {
		margin-top: 2rem;
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		color: white;
	}

	.variation-text {
		font-size: 0.875rem;
		opacity: 0.8;
	}

	.variation-dots {
		display: flex;
		gap: 0.5rem;
	}

	.variation-dot {
		width: 0.75rem;
		height: 0.75rem;
		border-radius: 50%;
		border: 1px solid rgba(255, 255, 255, 0.3);
		background: rgba(255, 255, 255, 0.1);
		cursor: pointer;
		transition: all 0.2s ease;
	}

	.variation-dot:hover {
		background: rgba(255, 255, 255, 0.3);
		border-color: rgba(255, 255, 255, 0.5);
	}

	.variation-dot.active {
		background: white;
		border-color: white;
	}

	/* Mobile adjustments */
	@media (max-width: 768px) {
		.image-viewer {
			padding: 1rem;
			max-width: none;
		}

		.image-container {
			max-height: 60vh;
		}

		.nav-arrow {
			width: 2.5rem;
			height: 2.5rem;
		}

		.nav-arrow.prev {
			left: -3rem;
		}

		.nav-arrow.next {
			right: -3rem;
		}

		.arrow-icon {
			font-size: 1.25rem;
		}
	}
</style>
