<script lang="ts">
	// ✅ PURE RUNES: Type definitions
	export interface SequenceData {
		id: string;
		name: string;
		difficulty: number;
		createdDate: Date;
		thumbnail?: string;
		description?: string;
		tags?: string[];
		author?: string;
		duration?: number;
		beatCount?: number;
	}

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		sequence,
		viewMode = 'grid',
		onSelect = () => {},
	} = $props<{
		sequence: SequenceData;
		viewMode?: 'grid' | 'list';
		onSelect?: (sequence: SequenceData) => void;
	}>();

	function handleSelect() {
		onSelect(sequence);
	}

	function getDifficultyColor(difficulty: number): string {
		const colors: Record<number, string> = {
			1: '#10b981', // green
			2: '#f59e0b', // yellow
			3: '#ef4444', // red
			4: '#8b5cf6', // purple
		};
		return colors[difficulty] || '#6366f1';
	}

	function getDifficultyLabel(difficulty: number): string {
		const labels: Record<number, string> = {
			1: 'Beginner',
			2: 'Intermediate',
			3: 'Advanced',
			4: 'Expert',
		};
		return labels[difficulty] || 'Unknown';
	}

	function formatDate(date: Date) {
		return date.toLocaleDateString('en-US', {
			month: 'short',
			day: 'numeric',
		});
	}
</script>

<div
	class="sequence-thumbnail"
	class:list-view={viewMode === 'list'}
	onclick={handleSelect}
	onkeydown={(e) => e.key === 'Enter' && handleSelect()}
	role="button"
	tabindex="0"
>
	<!-- Thumbnail Image/Placeholder -->
	<div class="thumbnail-image">
		{#if sequence.thumbnailUrl}
			<img src={sequence.thumbnailUrl} alt={sequence.word} />
		{:else}
			<!-- Placeholder with sequence info -->
			<div class="placeholder-content">
				<div class="sequence-word">{sequence.word}</div>
				<div class="sequence-meta">
					<span class="grid-mode">{sequence.gridMode}</span>
					<span class="start-pos">{sequence.startPosition}</span>
				</div>
			</div>
		{/if}

		<!-- Overlay with favorite star -->
		{#if sequence.isFavorite}
			<div class="favorite-overlay">
				<span class="favorite-star">⭐</span>
			</div>
		{/if}
	</div>

	<!-- Sequence Info -->
	<div class="sequence-info">
		<div class="info-header">
			<h3 class="sequence-title">{sequence.word}</h3>
			<div
				class="difficulty-badge"
				style="--difficulty-color: {getDifficultyColor(sequence.difficulty)}"
			>
				{sequence.difficulty}
			</div>
		</div>

		<div class="sequence-details">
			<div class="detail-row">
				<span class="detail-label">Length:</span>
				<span class="detail-value">{sequence.length} beats</span>
			</div>
			<div class="detail-row">
				<span class="detail-label">Start:</span>
				<span class="detail-value">{sequence.startPosition}</span>
			</div>
			<div class="detail-row">
				<span class="detail-label">Grid:</span>
				<span class="detail-value">{sequence.gridMode}</span>
			</div>
		</div>

		{#if viewMode === 'list'}
			<div class="extended-info">
				<div class="detail-row">
					<span class="detail-label">Author:</span>
					<span class="detail-value">{sequence.author}</span>
				</div>
				<div class="detail-row">
					<span class="detail-label">Added:</span>
					<span class="detail-value">{formatDate(sequence.dateAdded)}</span>
				</div>
				<div class="detail-row">
					<span class="detail-label">Difficulty:</span>
					<span
						class="detail-value"
						style="color: {getDifficultyColor(sequence.difficulty)}"
					>
						{getDifficultyLabel(sequence.difficulty)}
					</span>
				</div>
			</div>
		{/if}

		{#if sequence.tags && sequence.tags.length > 0}
			<div class="tags-container">
				{#each sequence.tags as tag}
					<span class="tag">{tag}</span>
				{/each}
			</div>
		{/if}
	</div>
</div>

<style>
	.sequence-thumbnail {
		background: var(--surface-glass);
		border: var(--glass-border);
		border-radius: 12px;
		backdrop-filter: var(--glass-backdrop);
		box-shadow: var(--shadow-glass);
		overflow: hidden;
		cursor: pointer;
		transition: all var(--transition-normal);
		position: relative;
		min-height: 280px;
	}

	.sequence-thumbnail:hover {
		border-color: var(--primary-color);
		box-shadow: var(--shadow-glass-hover);
		transform: translateY(-4px);
	}

	.sequence-thumbnail:active {
		transform: translateY(-2px);
	}

	/* List view layout */
	.sequence-thumbnail.list-view {
		display: flex;
		flex-direction: row;
		min-height: 120px;
		max-height: 120px;
	}

	.sequence-thumbnail.list-view .thumbnail-image {
		width: 160px;
		flex-shrink: 0;
	}

	.sequence-thumbnail.list-view .sequence-info {
		flex: 1;
		padding: var(--spacing-md);
		display: flex;
		flex-direction: column;
		justify-content: space-between;
	}

	/* Thumbnail Image */
	.thumbnail-image {
		position: relative;
		width: 100%;
		height: 160px;
		background: linear-gradient(
			135deg,
			rgba(99, 102, 241, 0.2),
			rgba(168, 85, 247, 0.2),
			rgba(6, 182, 212, 0.2)
		);
		display: flex;
		align-items: center;
		justify-content: center;
		overflow: hidden;
	}

	.thumbnail-image img {
		width: 100%;
		height: 100%;
		object-fit: cover;
	}

	.placeholder-content {
		text-align: center;
		color: white;
		padding: var(--spacing-md);
	}

	.sequence-word {
		font-size: var(--font-size-xl);
		font-weight: 600;
		margin-bottom: var(--spacing-xs);
		text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}

	.sequence-meta {
		display: flex;
		gap: var(--spacing-xs);
		font-size: var(--font-size-sm);
		opacity: 0.9;
	}

	.grid-mode,
	.start-pos {
		padding: 2px 6px;
		background: rgba(255, 255, 255, 0.2);
		border-radius: 4px;
		text-transform: capitalize;
	}

	.favorite-overlay {
		position: absolute;
		top: var(--spacing-sm);
		right: var(--spacing-sm);
		background: rgba(0, 0, 0, 0.5);
		border-radius: 50%;
		width: 32px;
		height: 32px;
		display: flex;
		align-items: center;
		justify-content: center;
		backdrop-filter: blur(10px);
	}

	.favorite-star {
		font-size: var(--font-size-base);
	}

	/* Sequence Info */
	.sequence-info {
		padding: var(--spacing-md);
		display: flex;
		flex-direction: column;
		gap: var(--spacing-sm);
		flex: 1;
	}

	.info-header {
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: var(--spacing-sm);
	}

	.sequence-title {
		font-size: var(--font-size-lg);
		font-weight: 600;
		color: var(--foreground);
		margin: 0;
		flex: 1;
		line-height: 1.3;
	}

	.difficulty-badge {
		--difficulty-color: var(--primary-color);

		display: flex;
		align-items: center;
		justify-content: center;
		width: 24px;
		height: 24px;
		background: var(--difficulty-color);
		color: white;
		border-radius: 50%;
		font-size: var(--font-size-sm);
		font-weight: 600;
		flex-shrink: 0;
	}

	.sequence-details {
		display: flex;
		flex-direction: column;
		gap: 2px;
	}

	.detail-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: var(--font-size-sm);
	}

	.detail-label {
		color: var(--muted-foreground);
		font-weight: 500;
	}

	.detail-value {
		color: var(--foreground);
		font-weight: 600;
		text-transform: capitalize;
	}

	.extended-info {
		display: flex;
		flex-direction: column;
		gap: 2px;
		margin-top: var(--spacing-xs);
		padding-top: var(--spacing-xs);
		border-top: 1px solid rgba(255, 255, 255, 0.1);
	}

	.tags-container {
		display: flex;
		flex-wrap: wrap;
		gap: 4px;
		margin-top: var(--spacing-xs);
	}

	.tag {
		padding: 2px 6px;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		border-radius: 12px;
		font-size: var(--font-size-xs);
		color: var(--muted-foreground);
		font-weight: 500;
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.sequence-thumbnail {
			min-height: 240px;
		}

		.thumbnail-image {
			height: 120px;
		}

		.sequence-word {
			font-size: var(--font-size-lg);
		}

		.sequence-title {
			font-size: var(--font-size-base);
		}

		.sequence-thumbnail.list-view {
			flex-direction: column;
			min-height: 200px;
			max-height: none;
		}

		.sequence-thumbnail.list-view .thumbnail-image {
			width: 100%;
			height: 100px;
		}
	}

	@media (max-width: 480px) {
		.sequence-info {
			padding: var(--spacing-sm);
		}

		.thumbnail-image {
			height: 100px;
		}
	}
</style>
