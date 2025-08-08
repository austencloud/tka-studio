<script lang="ts">
	import type { DictionaryItem } from '../../types/core.js';
	import ThumbnailImage from './ThumbnailImage.svelte';
	import ThumbnailOverlay from './ThumbnailOverlay.svelte';
	import ThumbnailMeta from './ThumbnailMeta.svelte';

	// Props
	let {
		item,
		onSelect
	}: {
		item: DictionaryItem;
		onSelect?: () => void;
	} = $props();

	// Computed properties
	const hasMultipleVersions = $derived(item.versions.length > 1);

	function handleCardClick(): void {
		onSelect?.();
	}

	function handleKeyDown(event: KeyboardEvent): void {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			onSelect?.();
		}
	}

	function handlePlay(): void {
		onSelect?.();
	}

	// Format author name for accessibility
	function formatAuthor(author?: string): string {
		if (!author) return 'Unknown Author';
		return author.length > 20 ? `${author.substring(0, 20)}...` : author;
	}
</script>

<div
	class="thumbnail-card"
	role="button"
	tabindex="0"
	onclick={handleCardClick}
	onkeydown={handleKeyDown}
	aria-label={`Select sequence ${item.name} by ${formatAuthor(item.metadata.author)}`}
>
	<ThumbnailImage
		src={item.thumbnailUrl || item.filePath}
		alt={`Thumbnail for ${item.name}`}
		{hasMultipleVersions}
		versionCount={item.versions.length}
	>
		{#snippet overlay()}
			<ThumbnailOverlay onPlay={handlePlay} />
		{/snippet}
	</ThumbnailImage>

	<ThumbnailMeta {item} />
</div>

<style>
	.thumbnail-card {
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 8px;
		overflow: hidden;
		cursor: pointer;
		transition: all 0.2s ease;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		display: flex;
		flex-direction: column;
		height: fit-content;
	}

	.thumbnail-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		border-color: var(--color-primary);
	}

	.thumbnail-card:focus {
		outline: none;
		box-shadow: 0 0 0 3px var(--color-primary-alpha);
	}

	/* Show overlay on hover */
	.thumbnail-card:hover :global(.card-overlay) {
		opacity: 1;
	}
</style>
