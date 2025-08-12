<!-- SequenceCard.svelte - Individual sequence card component -->
<script lang="ts">
	import type { SequenceData } from '$services/interfaces';
	import { onMount } from 'svelte';

	interface Props {
		sequence: SequenceData;
	}

	let { sequence }: Props = $props();

	// Card element used in bind:this
	// @ts-expect-error: Used in bind:this but not referenced in code
	let cardElement: HTMLElement;
	let imageLoaded = $state(false);
	let imageError = $state(false);

	// Derived properties
	let sequenceName = $derived(sequence.name || 'Untitled Sequence');
	let beatCount = $derived(sequence.beats?.length || sequence.sequence_length || 0);
	let difficulty = $derived(sequence.difficulty_level || 'Intermediate');
	let gridMode = $derived(sequence.grid_mode || 'diamond');
	let author = $derived(sequence.author || 'Unknown');

	// Generate a placeholder color based on sequence name
	let placeholderColor = $derived(() => {
		const colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#06b6d4'];
		const hash = sequenceName.split('').reduce((a, b) => {
			a = (a << 5) - a + b.charCodeAt(0);
			return a & a;
		}, 0);
		return colors[Math.abs(hash) % colors.length];
	});

	// Simulate image loading (since we don't have actual sequence images)
	onMount(() => {
		// Simulate image loading delay
		const loadTimeout = setTimeout(
			() => {
				imageLoaded = true;
			},
			Math.random() * 1000 + 500
		);

		return () => clearTimeout(loadTimeout);
	});

	function handleCardClick() {
		console.log('Sequence card clicked:', sequenceName);
		// TODO: Implement card click behavior (show details, edit, etc.)
	}

	// Handle keyboard events
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleCardClick();
		}
	}

	function handleExportCard() {
		console.log('Export card:', sequenceName);
		// TODO: Implement individual card export
	}

	function handleViewDetails() {
		console.log('View details:', sequenceName);
		// TODO: Implement details view
	}
</script>

<div
	class="sequence-card"
	bind:this={cardElement}
	onclick={handleCardClick}
	onkeydown={handleKeyDown}
	title="Click to view sequence details"
	role="button"
	tabindex="0"
>
	<!-- Card Header -->
	<div class="card-header">
		<h3 class="sequence-name" title={sequenceName}>
			{sequenceName}
		</h3>
		<div class="card-actions">
			<button
				class="action-btn"
				onclick={(e) => {
					e.stopPropagation();
					handleExportCard();
				}}
				title="Export this card"
			>
				📤
			</button>
			<button
				class="action-btn"
				onclick={(e) => {
					e.stopPropagation();
					handleViewDetails();
				}}
				title="View details"
			>
				🔍
			</button>
		</div>
	</div>

	<!-- Card Image/Preview -->
	<div class="card-preview">
		{#if imageLoaded && !imageError}
			<!-- Placeholder for actual sequence image -->
			<div class="sequence-preview" style:background-color={placeholderColor()}>
				<div class="preview-content">
					<div class="sequence-visualization">
						<!-- Simple visualization placeholder -->
						<div class="grid-indicator {gridMode}">
							{#each Array(Math.min(beatCount, 8)) as _, i}
								<div class="beat-dot" style:animation-delay="{i * 0.1}s"></div>
							{/each}
						</div>
					</div>
					<div class="preview-overlay">
						<span class="beat-count-large">{beatCount}</span>
						<span class="beat-label">beats</span>
					</div>
				</div>
			</div>
		{:else if imageError}
			<!-- Error State -->
			<div class="image-error">
				<div class="error-icon">❌</div>
				<span class="error-text">Failed to load</span>
			</div>
		{:else}
			<!-- Loading State -->
			<div class="image-loading">
				<div class="loading-spinner"></div>
				<span class="loading-text">Loading...</span>
			</div>
		{/if}
	</div>

	<!-- Card Footer -->
	<div class="card-footer">
		<div class="card-metadata">
			<div class="metadata-row">
				<span class="metadata-label">Beats:</span>
				<span class="metadata-value">{beatCount}</span>
			</div>
			<div class="metadata-row">
				<span class="metadata-label">Difficulty:</span>
				<span class="metadata-value difficulty-{difficulty.toLowerCase()}"
					>{difficulty}</span
				>
			</div>
			<div class="metadata-row">
				<span class="metadata-label">Grid:</span>
				<span class="metadata-value">{gridMode}</span>
			</div>
			{#if author !== 'Unknown'}
				<div class="metadata-row">
					<span class="metadata-label">Author:</span>
					<span class="metadata-value" title={author}>{author}</span>
				</div>
			{/if}
		</div>
	</div>
</div>

<style>
	.sequence-card {
	background: var(--surface-glass);
	backdrop-filter: var(--glass-backdrop);
	border: var(--glass-border);
	border-radius: 12px;
	overflow: hidden;
	cursor: pointer;
	transition: all var(--transition-normal);
	box-shadow: var(--shadow-glass);
	display: flex;
	flex-direction: column;
	min-height: 320px;
}

	.sequence-card:hover {
	background: var(--surface-hover);
	border: var(--glass-border-hover);
	transform: translateY(-2px);
	box-shadow: var(--shadow-glass-hover);
}

	/* Card Header */
	.card-header {
	padding: 12px 16px;
	background: rgba(255, 255, 255, 0.03);
	backdrop-filter: blur(10px);
	border-bottom: 1px solid rgba(255, 255, 255, 0.08);
	display: flex;
	justify-content: space-between;
	align-items: center;
	gap: 8px;
}

	.sequence-name {
	margin: 0;
	font-size: 16px;
	font-weight: 600;
	color: rgba(255, 255, 255, 0.95);
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.5);
	flex: 1;
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
}

	.card-actions {
		display: flex;
		gap: 4px;
		flex-shrink: 0;
	}

	.action-btn {
	width: 28px;
	height: 28px;
	border: 1px solid rgba(255, 255, 255, 0.2);
	border-radius: 6px;
	background: rgba(255, 255, 255, 0.05);
	backdrop-filter: blur(8px);
	cursor: pointer;
	display: flex;
	align-items: center;
	justify-content: center;
	font-size: 12px;
	transition: all var(--transition-fast);
	opacity: 0.8;
}

	.action-btn:hover {
	opacity: 1;
	background: rgba(255, 255, 255, 0.1);
	border-color: rgba(255, 255, 255, 0.4);
	transform: scale(1.1);
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

	/* Card Preview */
	.card-preview {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: center;
	min-height: 180px;
	background: rgba(255, 255, 255, 0.02);
	position: relative;
	overflow: hidden;
}

	.sequence-preview {
		width: 100%;
		height: 100%;
		position: relative;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.preview-content {
		position: relative;
		width: 100%;
		height: 100%;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.sequence-visualization {
		position: absolute;
		inset: 20px;
		display: flex;
		align-items: center;
		justify-content: center;
	}

	.grid-indicator {
		display: grid;
		gap: 8px;
		align-items: center;
		justify-items: center;
	}

	.grid-indicator.diamond {
		grid-template-columns: repeat(2, 1fr);
		transform: rotate(45deg);
	}

	.grid-indicator.box {
		grid-template-columns: repeat(3, 1fr);
	}

	.beat-dot {
		width: 12px;
		height: 12px;
		background: rgba(255, 255, 255, 0.8);
		border-radius: 50%;
		animation: pulse 2s infinite;
	}

	.preview-overlay {
		position: absolute;
		bottom: 16px;
		right: 16px;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		padding: 8px 12px;
		border-radius: 8px;
		text-align: center;
		backdrop-filter: blur(4px);
	}

	.beat-count-large {
		display: block;
		font-size: 24px;
		font-weight: bold;
		line-height: 1;
	}

	.beat-label {
		font-size: 10px;
		text-transform: uppercase;
		letter-spacing: 0.5px;
		opacity: 0.8;
	}

	/* Loading and Error States */
	.image-loading,
	.image-error {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 12px;
		color: var(--muted-foreground);
	}

	.loading-spinner {
		width: 32px;
		height: 32px;
		border: 3px solid var(--muted);
		border-top: 3px solid var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	.loading-text,
	.error-text {
		font-size: 14px;
		font-weight: 500;
	}

	.error-icon {
		font-size: 32px;
	}

	/* Card Footer */
	.card-footer {
	padding: 12px 16px;
	background: rgba(255, 255, 255, 0.03);
	backdrop-filter: blur(10px);
	border-top: 1px solid rgba(255, 255, 255, 0.08);
}

	.card-metadata {
		display: flex;
		flex-direction: column;
		gap: 6px;
	}

	.metadata-row {
		display: flex;
		justify-content: space-between;
		align-items: center;
		font-size: 12px;
	}

	.metadata-label {
	color: rgba(255, 255, 255, 0.6);
	font-weight: 500;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.3);
}

	.metadata-value {
	color: rgba(255, 255, 255, 0.9);
	font-weight: 600;
	text-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
	overflow: hidden;
	text-overflow: ellipsis;
	white-space: nowrap;
	max-width: 120px;
	text-align: right;
}

	/* Difficulty Colors */
	.difficulty-beginner {
		color: #10b981;
	}

	.difficulty-intermediate {
		color: #f59e0b;
	}

	.difficulty-advanced {
		color: #ef4444;
	}

	.difficulty-expert {
		color: #8b5cf6;
	}

	/* Animations */
	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	@keyframes pulse {
		0%,
		100% {
			opacity: 0.6;
			transform: scale(0.8);
		}
		50% {
			opacity: 1;
			transform: scale(1);
		}
	}

	/* Responsive Design */
	@media (max-width: 768px) {
		.sequence-card {
			min-height: 280px;
		}

		.card-preview {
			min-height: 150px;
		}

		.sequence-name {
			font-size: 14px;
		}

		.metadata-row {
			font-size: 11px;
		}

		.beat-count-large {
			font-size: 20px;
		}
	}
</style>
