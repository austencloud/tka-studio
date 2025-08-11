<!--
SequenceThumbnail Component - Real Data Implementation

Displays individual sequence thumbnails with proper image loading,
metadata, and responsive design following the desktop app's approach.
-->
<script lang="ts">
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		sequence,
		thumbnailService,
		viewMode = 'grid',
		onSelect = () => {},
	} = $props<{
		sequence: BrowseSequenceMetadata;
		thumbnailService: any; // IThumbnailService
		viewMode?: 'grid' | 'list';
		onSelect?: (sequence: BrowseSequenceMetadata) => void;
	}>();

	// ✅ PURE RUNES: State for image loading
	let imageLoaded = $state(false);
	let imageError = $state(false);
	let imageElement = $state<HTMLImageElement | null>(null);

	// ✅ DERIVED RUNES: Computed values
	let thumbnailUrl = $derived.by(() => {
		const firstThumbnail = sequence.thumbnails[0];
		return firstThumbnail
			? thumbnailService.getThumbnailUrl(sequence.id, firstThumbnail)
			: null;
	});

	let difficultyColor = $derived.by(() => {
		switch (sequence.difficultyLevel) {
			case 'beginner':
				return '#10b981'; // green
			case 'intermediate':
				return '#f59e0b'; // amber
			case 'advanced':
				return '#ef4444'; // red
			default:
				return '#6b7280'; // gray
		}
	});

	let sequenceLength = $derived(sequence.sequenceLength || sequence.word.length || 0);

	// Handle thumbnail click
	function handleClick() {
		onSelect(sequence);
	}

	// Handle image load events
	function handleImageLoad() {
		imageLoaded = true;
		imageError = false;
	}

	function handleImageError() {
		imageError = true;
		imageLoaded = false;
	}
</script>

<!-- Thumbnail container with responsive design -->
<div
	class="sequence-thumbnail"
	class:list-view={viewMode === 'list'}
	class:grid-view={viewMode === 'grid'}
	role="button"
	tabindex="0"
	on:click={handleClick}
	on:keydown={(e) => e.key === 'Enter' && handleClick()}
>
	<!-- Image container with aspect ratio -->
	<div class="image-container">
		{#if thumbnailUrl}
			<img
				bind:this={imageElement}
				src={thumbnailUrl}
				alt={`${sequence.word} sequence thumbnail`}
				class="thumbnail-image"
				class:loaded={imageLoaded}
				class:error={imageError}
				on:load={handleImageLoad}
				on:error={handleImageError}
			/>
		{/if}

		<!-- Loading state -->
		{#if !imageLoaded && !imageError && thumbnailUrl}
			<div class="loading-placeholder">
				<div class="loading-spinner"></div>
			</div>
		{/if}

		<!-- Error state or no thumbnail -->
		{#if imageError || !thumbnailUrl}
			<div class="error-placeholder">
				<div class="placeholder-icon">📄</div>
				<div class="placeholder-text">{sequence.word}</div>
			</div>
		{/if}

		<!-- Favorite indicator -->
		{#if sequence.isFavorite}
			<div class="favorite-indicator">⭐</div>
		{/if}

		<!-- Difficulty indicator -->
		<div class="difficulty-indicator" style="background-color: {difficultyColor}">
			{sequence.difficultyLevel?.[0]?.toUpperCase() || '?'}
		</div>
	</div>

	<!-- Metadata section -->
	<div class="metadata-section">
		<h3 class="sequence-title">{sequence.word}</h3>

		{#if viewMode === 'grid'}
			<!-- Grid view: compact metadata -->
			<div class="grid-metadata">
				<div class="beat-count">{sequenceLength} beats</div>
				{#if sequence.author}
					<div class="author">by {sequence.author}</div>
				{/if}
			</div>
		{:else}
			<!-- List view: detailed metadata -->
			<div class="list-metadata">
				<div class="metadata-row">
					<span class="label">Length:</span>
					<span class="value">{sequenceLength} beats</span>
				</div>
				{#if sequence.author}
					<div class="metadata-row">
						<span class="label">Author:</span>
						<span class="value">{sequence.author}</span>
					</div>
				{/if}
				{#if sequence.difficultyLevel}
					<div class="metadata-row">
						<span class="label">Difficulty:</span>
						<span class="value" style="color: {difficultyColor}">
							{sequence.difficultyLevel}
						</span>
					</div>
				{/if}
				{#if sequence.dateAdded}
					<div class="metadata-row">
						<span class="label">Added:</span>
						<span class="value">
							{new Date(sequence.dateAdded).toLocaleDateString()}
						</span>
					</div>
				{/if}
			</div>
		{/if}

		<!-- Tags (if any) -->
		{#if sequence.tags.length > 0}
			<div class="tags">
				{#each sequence.tags.slice(0, 3) as tag}
					<span class="tag">{tag}</span>
				{/each}
			</div>
		{/if}
	</div>
</div>

<style>
	.sequence-thumbnail {
		background: rgba(255, 255, 255, 0.95);
		border: 1px solid rgba(200, 220, 240, 0.8);
		border-radius: 12px;
		overflow: hidden;
		cursor: pointer;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		display: flex;
		flex-direction: column;
		position: relative;
	}

	.sequence-thumbnail:hover {
		background: rgba(240, 248, 255, 0.98);
		border-color: rgba(100, 150, 255, 0.6);
		transform: translateY(-2px);
		box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
	}

	.sequence-thumbnail:focus {
		outline: 2px solid rgba(100, 150, 255, 0.8);
		outline-offset: 2px;
	}

	/* Grid view (default) */
	.grid-view {
		aspect-ratio: 4/5;
		min-height: 200px;
	}

	/* List view */
	.list-view {
		flex-direction: row;
		aspect-ratio: unset;
		height: 120px;
	}

	.list-view .image-container {
		width: 120px;
		flex-shrink: 0;
	}

	.list-view .metadata-section {
		flex: 1;
		padding: 16px;
	}

	/* Image container */
	.image-container {
		position: relative;
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #f8fafc;
		overflow: hidden;
	}

	.thumbnail-image {
		width: 100%;
		height: 100%;
		object-fit: cover;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.thumbnail-image.loaded {
		opacity: 1;
	}

	.thumbnail-image.error {
		display: none;
	}

	/* Loading state */
	.loading-placeholder {
		position: absolute;
		inset: 0;
		display: flex;
		align-items: center;
		justify-content: center;
		background: #f1f5f9;
	}

	.loading-spinner {
		width: 24px;
		height: 24px;
		border: 2px solid #e2e8f0;
		border-top-color: #3b82f6;
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	/* Error/placeholder state */
	.error-placeholder {
		position: absolute;
		inset: 0;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: #f8fafc;
		color: #64748b;
		text-align: center;
		padding: 16px;
	}

	.placeholder-icon {
		font-size: 2rem;
		margin-bottom: 8px;
	}

	.placeholder-text {
		font-size: 0.875rem;
		font-weight: 600;
		word-break: break-all;
	}

	/* Indicators */
	.favorite-indicator {
		position: absolute;
		top: 8px;
		right: 8px;
		font-size: 1rem;
		background: rgba(255, 255, 255, 0.9);
		border-radius: 50%;
		width: 24px;
		height: 24px;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	.difficulty-indicator {
		position: absolute;
		bottom: 8px;
		right: 8px;
		color: white;
		font-size: 0.75rem;
		font-weight: 700;
		border-radius: 50%;
		width: 20px;
		height: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
	}

	/* Metadata section */
	.metadata-section {
		padding: 12px;
		background: white;
	}

	.sequence-title {
		font-size: 1rem;
		font-weight: 700;
		color: #1e293b;
		margin: 0 0 8px 0;
		line-height: 1.2;
		word-break: break-all;
	}

	/* Grid metadata */
	.grid-metadata {
		display: flex;
		flex-direction: column;
		gap: 4px;
	}

	.beat-count {
		font-size: 0.875rem;
		color: #3b82f6;
		font-weight: 600;
	}

	.author {
		font-size: 0.75rem;
		color: #64748b;
	}

	/* List metadata */
	.list-metadata {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.metadata-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.875rem;
	}

	.label {
		color: #64748b;
		font-weight: 500;
	}

	.value {
		color: #1e293b;
		font-weight: 600;
	}

	/* Tags */
	.tags {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		margin-top: 8px;
	}

	.tag {
		background: #e0e7ff;
		color: #3730a3;
		font-size: 0.625rem;
		font-weight: 600;
		padding: 2px 6px;
		border-radius: 4px;
		text-transform: uppercase;
		letter-spacing: 0.025em;
	}

	/* Responsive design */
	@media (max-width: 768px) {
		.grid-view {
			min-height: 180px;
		}

		.list-view {
			height: 100px;
		}

		.list-view .image-container {
			width: 100px;
		}

		.metadata-section {
			padding: 8px;
		}

		.sequence-title {
			font-size: 0.875rem;
		}
	}
</style>
