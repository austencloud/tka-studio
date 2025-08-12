<!-- SequenceThumbnail.svelte - Individual sequence thumbnail widget -->
<script lang="ts">
	import type { SequenceData } from '$lib/types/write';
	import { generateSequenceThumbnail } from '$lib/types/write';

	// Props
	interface Props {
		sequence: SequenceData;
		position: number;
		onSequenceClicked?: (position: number) => void;
		onRemoveRequested?: (position: number) => void;
	}

	let { sequence, position, onSequenceClicked, onRemoveRequested }: Props = $props();

	// Handle sequence click
	function handleSequenceClick() {
		onSequenceClicked?.(position);
	}

	// Handle keyboard events
	function handleKeyDown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			handleSequenceClick();
		}
	}

	// Handle remove button click
	function handleRemoveClick(event: Event) {
		event.stopPropagation(); // Prevent sequence click
		onRemoveRequested?.(position);
	}

	// Generate thumbnail
	const thumbnailSrc = $derived(sequence.thumbnail || generateSequenceThumbnail(sequence));
	const beatsCount = $derived(sequence.beats.length);
</script>

<div
	class="sequence-thumbnail"
	onclick={handleSequenceClick}
	onkeydown={handleKeyDown}
	role="button"
	tabindex="0"
>
	<!-- Header with position and remove button -->
	<div class="thumbnail-header">
		<span class="position-number">{position + 1}</span>
		<button
			class="remove-button"
			onclick={handleRemoveClick}
			title="Remove sequence"
			aria-label="Remove sequence"
		>
			×
		</button>
	</div>

	<!-- Sequence preview -->
	<div class="sequence-preview">
		<img src={thumbnailSrc} alt={sequence.name} />
	</div>

	<!-- Sequence info -->
	<div class="sequence-info">
		<div class="sequence-name">{sequence.name}</div>
		<div class="beats-count">{beatsCount} beat{beatsCount !== 1 ? 's' : ''}</div>
	</div>
</div>

<style>
	.sequence-thumbnail {
		background: rgba(40, 40, 50, 0.8);
		border: 2px solid rgba(80, 80, 100, 0.5);
		border-radius: 8px;
		width: 120px;
		height: 110px;
		cursor: pointer;
		transition: all var(--transition-normal);
		display: flex;
		flex-direction: column;
		overflow: hidden;
		backdrop-filter: var(--glass-backdrop);
		position: relative;
	}

	.sequence-thumbnail:hover {
		background: rgba(60, 60, 70, 0.9);
		border-color: rgba(120, 120, 140, 0.8);
		transform: translateY(-2px);
		box-shadow: var(--shadow-glass-hover);
	}

	.sequence-thumbnail:active {
		transform: translateY(0);
	}

	.thumbnail-header {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: var(--spacing-xs);
		background: rgba(20, 20, 30, 0.6);
		border-bottom: 1px solid rgba(80, 80, 100, 0.3);
	}

	.position-number {
		color: rgba(255, 255, 255, 0.8);
		font-size: var(--font-size-xs);
		font-weight: bold;
		background: rgba(100, 150, 200, 0.7);
		padding: 2px 6px;
		border-radius: 4px;
		min-width: 20px;
		text-align: center;
	}

	.remove-button {
		background: rgba(200, 100, 100, 0.7);
		border: none;
		border-radius: 50%;
		width: 18px;
		height: 18px;
		color: white;
		font-size: 12px;
		font-weight: bold;
		cursor: pointer;
		display: flex;
		align-items: center;
		justify-content: center;
		transition: all var(--transition-fast);
		line-height: 1;
	}

	.remove-button:hover {
		background: rgba(220, 120, 120, 0.9);
		transform: scale(1.1);
	}

	.remove-button:active {
		transform: scale(0.95);
	}

	.sequence-preview {
		flex: 1;
		display: flex;
		align-items: center;
		justify-content: center;
		padding: var(--spacing-xs);
		background: rgba(20, 20, 30, 0.3);
	}

	.sequence-preview img {
		width: 100%;
		height: 100%;
		object-fit: contain;
		border-radius: 4px;
	}

	.sequence-info {
		padding: var(--spacing-xs);
		background: rgba(30, 30, 40, 0.8);
		border-top: 1px solid rgba(80, 80, 100, 0.3);
	}

	.sequence-name {
		color: rgba(255, 255, 255, 0.9);
		font-size: var(--font-size-xs);
		font-weight: 500;
		overflow: hidden;
		text-overflow: ellipsis;
		white-space: nowrap;
		margin-bottom: 2px;
	}

	.beats-count {
		color: rgba(255, 255, 255, 0.7);
		font-size: 10px;
		text-align: center;
	}

	/* Focus styles for accessibility */
	.sequence-thumbnail:focus-visible {
		outline: 2px solid rgba(255, 255, 255, 0.6);
		outline-offset: 2px;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.sequence-thumbnail {
			width: 100px;
			height: 90px;
		}

		.position-number {
			font-size: 10px;
			padding: 1px 4px;
			min-width: 16px;
		}

		.remove-button {
			width: 16px;
			height: 16px;
			font-size: 10px;
		}

		.sequence-name {
			font-size: 10px;
		}

		.beats-count {
			font-size: 9px;
		}
	}

	@media (max-width: 480px) {
		.sequence-thumbnail {
			width: 80px;
			height: 70px;
		}

		.thumbnail-header {
			padding: 2px;
		}

		.sequence-info {
			padding: 2px;
		}

		.position-number {
			font-size: 9px;
			padding: 1px 3px;
			min-width: 14px;
		}

		.remove-button {
			width: 14px;
			height: 14px;
			font-size: 9px;
		}

		.sequence-name {
			font-size: 9px;
			margin-bottom: 1px;
		}

		.beats-count {
			font-size: 8px;
		}
	}
</style>
