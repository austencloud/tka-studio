<!-- FullscreenActionButtons.svelte - Action buttons for fullscreen viewer -->
<script lang="ts">
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const { sequence, onAction = () => {} } = $props<{
		sequence?: BrowseSequenceMetadata;
		onAction?: (action: string, sequence: BrowseSequenceMetadata) => void;
	}>();

	function handleAction(action: string) {
		if (sequence) {
			console.log(`🎬 Fullscreen action: ${action} on sequence:`, sequence.id);
			onAction(action, sequence);
		}
	}
</script>

<div class="action-buttons">
	<div class="button-group">
		<button
			class="action-button edit"
			onclick={() => handleAction('edit')}
			aria-label="Edit sequence"
		>
			<span class="button-icon">✏️</span>
			<span class="button-text">Edit</span>
		</button>

		<button
			class="action-button favorite"
			class:favorited={sequence?.isFavorite}
			onclick={() => handleAction('save')}
			aria-label={sequence?.isFavorite ? 'Remove from favorites' : 'Add to favorites'}
		>
			<span class="button-icon">{sequence?.isFavorite ? '❤️' : '🤍'}</span>
			<span class="button-text">{sequence?.isFavorite ? 'Favorited' : 'Favorite'}</span>
		</button>

		<button
			class="action-button delete"
			onclick={() => handleAction('delete')}
			aria-label="Delete sequence"
		>
			<span class="button-icon">🗑️</span>
			<span class="button-text">Delete</span>
		</button>
	</div>
</div>

<style>
	.action-buttons {
		width: 100%;
	}

	.button-group {
		display: flex;
		flex-direction: row;
		gap: 1rem;
		justify-content: center;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 1.5rem;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
	}

	.action-button {
		display: flex;
		align-items: center;
		gap: 0.5rem;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
		color: white;
		padding: 0.75rem 1.5rem;
		border-radius: 1.5rem;
		cursor: pointer;
		transition: all 0.2s ease;
		font-size: 0.875rem;
		font-weight: 500;
		min-width: 6rem;
		justify-content: center;
	}

	.action-button:hover {
		background: rgba(255, 255, 255, 0.2);
		border-color: rgba(255, 255, 255, 0.3);
		transform: translateY(-2px);
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
	}

	.action-button:active {
		transform: translateY(0);
	}

	.action-button.edit:hover {
		background: rgba(59, 130, 246, 0.3);
		border-color: rgba(59, 130, 246, 0.5);
		color: #60a5fa;
	}

	.action-button.favorite:hover {
		background: rgba(239, 68, 68, 0.3);
		border-color: rgba(239, 68, 68, 0.5);
		color: #f87171;
	}

	.action-button.favorite.favorited {
		background: rgba(239, 68, 68, 0.2);
		border-color: rgba(239, 68, 68, 0.4);
		color: #f87171;
	}

	.action-button.delete:hover {
		background: rgba(220, 38, 38, 0.3);
		border-color: rgba(220, 38, 38, 0.5);
		color: #fca5a5;
	}

	.button-icon {
		font-size: 1rem;
		line-height: 1;
	}

	.button-text {
		font-size: 0.875rem;
		font-weight: 500;
	}

	/* Mobile adjustments */
	@media (max-width: 768px) {
		.action-buttons {
			bottom: 1rem;
			left: 1rem;
			right: 1rem;
			transform: none;
		}

		.button-group {
			justify-content: center;
			padding: 0.75rem;
			gap: 0.75rem;
		}

		.action-button {
			padding: 0.5rem 1rem;
			min-width: auto;
			flex: 1;
		}

		.button-text {
			display: none;
		}

		.button-icon {
			font-size: 1.25rem;
		}
	}

	@media (max-width: 480px) {
		.button-group {
			gap: 0.5rem;
			padding: 0.5rem;
		}

		.action-button {
			padding: 0.5rem;
			border-radius: 50%;
			width: 3rem;
			height: 3rem;
			min-width: auto;
		}
	}
</style>
