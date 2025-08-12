<!-- SequenceDetails.svelte - Sequence metadata and details display -->
<script lang="ts">
	import type { SequenceData } from '$domain/SequenceData';

	interface Props {
		sequence?: SequenceData & {
			difficulty?: number;
			tags?: readonly string[];
			description?: string;
			author?: string;
			dateCreated?: string;
			isFavorite?: boolean;
			word?: string;
			length?: number;
			startPosition?: string;
			gridMode?: string;
			dateAdded?: Date;
		};
	}

	let { sequence }: Props = $props();

	function getDifficultyColor(difficulty: number) {
		const colors: Record<number, string> = {
			1: '#10b981', // green
			2: '#f59e0b', // yellow
			3: '#ef4444', // red
			4: '#8b5cf6', // purple
		};
		return colors[difficulty] || '#6366f1';
	}

	function getDifficultyLabel(difficulty: number) {
		const labels: Record<number, string> = {
			1: 'Beginner',
			2: 'Intermediate',
			3: 'Advanced',
			4: 'Expert',
		};
		return labels[difficulty] || 'Unknown';
	}

	// Check if sequence has tags
	let hasTags = $derived(sequence?.tags && sequence.tags.length > 0);
</script>

<div class="sequence-details">
	<h3>Details</h3>

	<div class="details-grid">
		<div class="detail-item">
			<span class="detail-label">Length</span>
			<span class="detail-value">{sequence?.length || 0} beats</span>
		</div>

		<div class="detail-item">
			<span class="detail-label">Author</span>
			<span class="detail-value">{sequence?.author || 'Unknown'}</span>
		</div>

		<div class="detail-item">
			<span class="detail-label">Difficulty</span>
			<span
				class="detail-value"
				style="color: {getDifficultyColor(sequence?.difficulty || 1)}"
			>
				{getDifficultyLabel(sequence?.difficulty || 1)}
			</span>
		</div>
	</div>

	{#if hasTags}
		<div class="tags-section">
			<h4>Tags</h4>
			<div class="tags-container">
				{#each sequence?.tags || [] as tag}
					<span class="tag">{tag}</span>
				{/each}
			</div>
		</div>
	{/if}
</div>

<style>
	/* Sequence Details */
	.sequence-details {
		flex: 1;
	}

	.sequence-details h3 {
		font-size: var(--font-size-lg);
		color: var(--foreground);
		margin: 0 0 var(--spacing-md) 0;
		font-weight: 600;
	}

	.details-grid {
		display: grid;
		gap: var(--spacing-sm);
		margin-bottom: var(--spacing-lg);
	}

	.detail-item {
		display: flex;
		justify-content: space-between;
		align-items: center;
		padding: var(--spacing-sm);
		background: rgba(255, 255, 255, 0.05);
		border-radius: 8px;
		border: 1px solid rgba(255, 255, 255, 0.1);
	}

	.detail-label {
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
		font-weight: 500;
	}

	.detail-value {
		font-size: var(--font-size-sm);
		color: var(--foreground);
		font-weight: 600;
		text-align: right;
		text-transform: capitalize;
	}

	.tags-section h4 {
		font-size: var(--font-size-base);
		color: var(--foreground);
		margin: 0 0 var(--spacing-sm) 0;
		font-weight: 600;
	}

	.tags-container {
		display: flex;
		flex-wrap: wrap;
		gap: var(--spacing-xs);
	}

	.tag {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		font-size: var(--font-size-xs);
		color: var(--muted-foreground);
		font-weight: 500;
	}
</style>
