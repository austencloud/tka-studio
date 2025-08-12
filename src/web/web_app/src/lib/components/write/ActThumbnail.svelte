<!-- ActThumbnail.svelte - Individual act thumbnail widget -->
<script lang="ts">
	import type { ActThumbnailInfo } from '$lib/types/write';
	import { generateActThumbnail } from '$lib/types/write';

	// Props
	interface Props {
		actInfo: ActThumbnailInfo;
		onActSelected?: (filePath: string) => void;
	}

	let { actInfo, onActSelected }: Props = $props();

	// Handle thumbnail click
	function handleClick() {
		onActSelected?.(actInfo.filePath);
	}

	// Handle keyboard events
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleClick();
		}
	}

	// Format date for display
	function formatDate(date: Date): string {
		return date.toLocaleDateString();
	}

	// Generate thumbnail image
	const thumbnailSrc = $derived(
		actInfo.thumbnail ||
			generateActThumbnail({
				id: actInfo.id,
				name: actInfo.name,
				description: actInfo.description,
				sequences: Array(actInfo.sequenceCount).fill(null),
				...(actInfo.hasMusic ? { musicFile: { name: 'music.mp3', path: '' } } : {}),
				metadata: { created: new Date(), modified: actInfo.lastModified },
			})
	);
</script>

<div
	class="act-thumbnail"
	onclick={handleClick}
	onkeydown={handleKeyDown}
	role="button"
	tabindex="0"
>
	<!-- Thumbnail Image -->
	<div class="thumbnail-image">
		<img src={thumbnailSrc} alt={actInfo.name} />
	</div>

	<!-- Act Info -->
	<div class="act-info">
		<h4 class="act-name">{actInfo.name}</h4>
		<p class="act-description">{actInfo.description || 'No description'}</p>
		<div class="act-metadata">
			<span class="sequence-count">
				{actInfo.sequenceCount} sequence{actInfo.sequenceCount !== 1 ? 's' : ''}
			</span>
			{#if actInfo.hasMusic}
				<span class="music-indicator">♪</span>
			{/if}
		</div>
		<div class="last-modified">
			Modified: {formatDate(actInfo.lastModified)}
		</div>
	</div>
</div>

<style>
	.act-thumbnail {
		background: rgba(40, 40, 50, 0.8);
		border: 2px solid rgba(80, 80, 100, 0.5);
		border-radius: 8px;
		padding: var(--spacing-sm);
		cursor: pointer;
		transition: all var(--transition-normal);
		width: 160px;
		min-height: 200px;
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		backdrop-filter: var(--glass-backdrop);
	}

	.act-thumbnail:hover {
		background: rgba(60, 60, 70, 0.9);
		border-color: rgba(120, 120, 140, 0.8);
		transform: translateY(-2px);
		box-shadow: var(--shadow-glass-hover);
	}

	.act-thumbnail:active {
		transform: translateY(0);
	}

	.thumbnail-image {
		width: 100%;
		height: 120px;
		border-radius: 4px;
		overflow: hidden;
		background: rgba(20, 20, 30, 0.5);
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.thumbnail-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
		border-radius: 4px;
	}

	.act-info {
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: var(--spacing-xs);
	}

	.act-name {
		color: rgba(255, 255, 255, 0.9);
		font-size: var(--font-size-sm);
		font-weight: bold;
		margin: 0;
		line-height: 1.2;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
	}

	.act-description {
		color: rgba(255, 255, 255, 0.7);
		font-size: var(--font-size-xs);
		margin: 0;
		line-height: 1.3;
		overflow: hidden;
		display: -webkit-box;
		-webkit-line-clamp: 2;
		line-clamp: 2;
		-webkit-box-orient: vertical;
		text-overflow: ellipsis;
	}

	.act-metadata {
		display: flex;
		align-items: center;
		gap: var(--spacing-xs);
		margin-top: auto;
	}

	.sequence-count {
		color: rgba(255, 255, 255, 0.8);
		font-size: var(--font-size-xs);
		font-weight: 500;
	}

	.music-indicator {
		color: rgba(100, 200, 100, 0.9);
		font-size: var(--font-size-sm);
		font-weight: bold;
	}

	.last-modified {
		color: rgba(255, 255, 255, 0.5);
		font-size: var(--font-size-xs);
		margin-top: var(--spacing-xs);
	}

	/* Focus styles for accessibility */
	.act-thumbnail:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.6);
		outline-offset: 2px;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.act-thumbnail {
			width: 140px;
			min-height: 180px;
		}

		.thumbnail-image {
			height: 100px;
		}

		.act-name {
			font-size: var(--font-size-xs);
		}

		.act-description {
			font-size: 10px;
		}
	}

	@media (max-width: 480px) {
		.act-thumbnail {
			width: 120px;
			min-height: 160px;
		}

		.thumbnail-image {
			height: 80px;
		}
	}
</style>
