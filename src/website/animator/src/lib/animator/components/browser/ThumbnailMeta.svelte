<script lang="ts">
	import type { DictionaryItem } from '../../types/core.js';

	// Props
	let {
		item
	}: {
		item: DictionaryItem;
	} = $props();

	// Computed properties
	const stepCount = $derived(item.sequenceData.length - 2); // Subtract metadata and start position

	// Format author name
	function formatAuthor(author?: string): string {
		if (!author) return 'Unknown Author';
		return author.length > 20 ? `${author.substring(0, 20)}...` : author;
	}

	// Get difficulty indicator
	function getDifficultyLevel(level?: number): string {
		if (!level) return 'Unknown';
		if (level <= 1) return 'Beginner';
		if (level <= 3) return 'Intermediate';
		return 'Advanced';
	}

	// Get step count description
	function getStepDescription(count: number): string {
		if (count <= 5) return 'Short';
		if (count <= 10) return 'Medium';
		return 'Long';
	}
</script>

<div class="card-content">
	<div class="card-header">
		<h3 class="card-title">{item.name}</h3>
		{#if item.metadata.level}
			<span class="difficulty-badge" title={`Level ${item.metadata.level}`}>
				{getDifficultyLevel(item.metadata.level)}
			</span>
		{/if}
	</div>

	<div class="card-meta">
		<div class="meta-item">
			<span class="meta-label">Author:</span>
			<span class="meta-value">{formatAuthor(item.metadata.author)}</span>
		</div>

		<div class="meta-item">
			<span class="meta-label">Steps:</span>
			<span class="meta-value">
				{stepCount} ({getStepDescription(stepCount)})
			</span>
		</div>

		{#if item.metadata.grid_mode}
			<div class="meta-item">
				<span class="meta-label">Grid:</span>
				<span class="meta-value">{item.metadata.grid_mode}</span>
			</div>
		{/if}
	</div>

	{#if item.metadata.word && item.metadata.word !== item.name}
		<div class="card-description">
			<span class="description-label">Word:</span>
			<span class="description-text">{item.metadata.word}</span>
		</div>
	{/if}
</div>

<style>
	.card-content {
		padding: 0.75rem;
		flex: 1;
		display: flex;
		flex-direction: column;
		min-height: 0;
	}

	.card-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		margin-bottom: 0.5rem;
		gap: 0.5rem;
	}

	.card-title {
		margin: 0;
		font-size: 1.1rem;
		font-weight: 600;
		color: var(--color-text-primary);
		line-height: 1.2;
		flex: 1;
	}

	.difficulty-badge {
		background: var(--color-surface);
		color: var(--color-text-secondary);
		padding: 2px 8px;
		border-radius: 12px;
		font-size: 0.75rem;
		font-weight: 500;
		white-space: nowrap;
		border: 1px solid var(--color-border);
		transition: all 0.3s ease;
	}

	.card-meta {
		display: flex;
		flex-direction: column;
		gap: 0.2rem;
		margin-bottom: 0.5rem;
	}

	.meta-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 0.8rem;
	}

	.meta-label {
		color: var(--color-text-secondary);
		font-weight: 500;
	}

	.meta-value {
		color: var(--color-text-primary);
		text-align: right;
	}

	.card-description {
		padding-top: 0.5rem;
		border-top: 1px solid var(--color-border);
		font-size: 0.8rem;
		transition: border-color 0.3s ease;
	}

	.description-label {
		color: var(--color-text-secondary);
		font-weight: 500;
		margin-right: 0.5rem;
	}

	.description-text {
		color: var(--color-text-primary);
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.card-content {
			padding: 1rem;
		}

		.card-title {
			font-size: 1.2rem;
		}

		.meta-item {
			font-size: 0.9rem;
		}

		.card-description {
			font-size: 0.9rem;
		}
	}
</style>
