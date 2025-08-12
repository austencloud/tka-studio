<!--
ThumbnailMetadata Component - Metadata Display

Displays sequence metadata including title, difficulty, length, author, date, and tags.
Extracted from SequenceThumbnail.svelte for better separation of concerns.
-->
<script lang="ts">
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		sequence,
		viewMode = 'grid',
		showExtendedInfo = false,
	} = $props<{
		sequence: BrowseSequenceMetadata;
		viewMode?: 'grid' | 'list';
		showExtendedInfo?: boolean;
	}>();

	// ✅ DERIVED RUNES: Computed values
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

	let difficultyLabel = $derived.by(() => {
		switch (sequence.difficultyLevel) {
			case 'beginner':
				return 'Beginner';
			case 'intermediate':
				return 'Intermediate';
			case 'advanced':
				return 'Advanced';
			default:
				return 'Unknown';
		}
	});

	let formattedLength = $derived.by(() => {
		const beats = sequence.length;
		return beats === 1 ? '1 beat' : `${beats} beats`;
	});
</script>

<div class="metadata-section" class:list-view={viewMode === 'list'}>
	<!-- Title -->
	<h3 class="sequence-title">{sequence.word}</h3>

	<!-- Basic metadata row -->
	<div class="metadata-row">
		<!-- Difficulty badge -->
		<span class="difficulty-badge" style="background-color: {difficultyColor}">
			{difficultyLabel}
		</span>

		<!-- Length -->
		<span class="length-info">{formattedLength}</span>
	</div>

	<!-- Extended info (for list view or when requested) -->
	{#if showExtendedInfo || viewMode === 'list'}
		<div class="extended-info">
			<!-- Author -->
			{#if sequence.author}
				<div class="info-item">
					<span class="info-label">Author:</span>
					<span class="info-value">{sequence.author}</span>
				</div>
			{/if}

			<!-- Date added -->
			{#if sequence.dateAdded}
				<div class="info-item">
					<span class="info-label">Added:</span>
					<span class="info-value">
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

<style>
	.metadata-section {
		padding: 12px;
		flex: 1;
		display: flex;
		flex-direction: column;
		gap: 8px;
	}

	.metadata-section.list-view {
		padding: 8px 12px;
		justify-content: center;
	}

	.sequence-title {
		font-size: 1rem;
		font-weight: 600;
		color: #1f2937;
		margin: 0;
		line-height: 1.2;
		word-break: break-word;
	}

	.metadata-row {
		display: flex;
		align-items: center;
		gap: 8px;
		flex-wrap: wrap;
	}

	.difficulty-badge {
		color: white;
		font-size: 0.625rem;
		font-weight: 700;
		padding: 2px 6px;
		border-radius: 4px;
		text-transform: uppercase;
		letter-spacing: 0.025em;
		white-space: nowrap;
	}

	.length-info {
		font-size: 0.75rem;
		color: #6b7280;
		font-weight: 500;
	}

	.extended-info {
		display: flex;
		flex-direction: column;
		gap: 4px;
		font-size: 0.75rem;
	}

	.info-item {
		display: flex;
		gap: 4px;
	}

	.info-label {
		color: #6b7280;
		font-weight: 500;
		min-width: 50px;
	}

	.info-value {
		color: #374151;
		font-weight: 400;
	}

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
		.metadata-section {
			padding: 8px;
		}

		.sequence-title {
			font-size: 0.875rem;
		}

		.difficulty-badge {
			font-size: 0.5rem;
			padding: 1px 4px;
		}

		.length-info {
			font-size: 0.625rem;
		}

		.extended-info {
			font-size: 0.625rem;
		}
	}
</style>