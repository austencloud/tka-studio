<!-- FullscreenSequenceInfo.svelte - Sequence metadata display for fullscreen viewer -->
<script lang="ts">
	import type { BrowseSequenceMetadata } from '$lib/domain/browse';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const { sequence } = $props<{
		sequence?: BrowseSequenceMetadata;
	}>();
</script>

{#if sequence}
	<div class="sequence-info">
		<!-- Ultra-condensed essential info only -->
		<div class="info-compact">
			<h3 class="sequence-title">{sequence.word}</h3>
			<div class="info-row">
				<span class="info-badge {sequence.difficulty?.toLowerCase() || 'unknown'}">
					{sequence.difficulty || 'Unknown'}
				</span>
				<span class="info-badge {sequence.isFavorite ? 'favorite' : 'not-favorite'}">
					{sequence.isFavorite ? '❤️' : '🤍'}
				</span>
				<span class="info-badge {sequence.isCircular ? 'circular' : 'linear'}">
					{sequence.isCircular ? '🔄' : '➡️'}
				</span>
				{#if sequence.thumbnails && sequence.thumbnails.length > 0}
					<span class="info-badge variations">
						{sequence.thumbnails.length} var{sequence.thumbnails.length !== 1
							? 's'
							: ''}
					</span>
				{/if}
			</div>
		</div>
	</div>
{/if}

<style>
	.sequence-info {
		width: 100%;
		background: rgba(0, 0, 0, 0.8);
		backdrop-filter: blur(10px);
		border: 1px solid rgba(255, 255, 255, 0.1);
		border-radius: 12px;
		padding: 1rem;
		color: white;
		box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
		text-align: center;
	}

	.info-compact {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
	}

	.sequence-title {
		margin: 0;
		font-size: 1.375rem;
		font-weight: 600;
		color: white;
	}

	.info-row {
		display: flex;
		gap: 0.5rem;
		flex-wrap: wrap;
		justify-content: center;
	}

	.info-badge {
		display: inline-flex;
		align-items: center;
		padding: 0.375rem 0.75rem;
		border-radius: 6px;
		font-size: 0.8125rem;
		font-weight: 500;
		background: rgba(255, 255, 255, 0.1);
		border: 1px solid rgba(255, 255, 255, 0.2);
	}

	/* Difficulty badges */
	.info-badge.beginner {
		background: rgba(34, 197, 94, 0.2);
		border-color: rgba(34, 197, 94, 0.4);
		color: #86efac;
	}

	.info-badge.intermediate {
		background: rgba(251, 191, 36, 0.2);
		border-color: rgba(251, 191, 36, 0.4);
		color: #fde047;
	}

	.info-badge.advanced {
		background: rgba(239, 68, 68, 0.2);
		border-color: rgba(239, 68, 68, 0.4);
		color: #fca5a5;
	}

	/* Status badges */
	.info-badge.favorite {
		background: rgba(236, 72, 153, 0.2);
		border-color: rgba(236, 72, 153, 0.4);
	}

	.info-badge.circular {
		background: rgba(59, 130, 246, 0.2);
		border-color: rgba(59, 130, 246, 0.4);
	}

	.info-badge.variations {
		background: rgba(168, 85, 247, 0.2);
		border-color: rgba(168, 85, 247, 0.4);
	}

	/* Mobile adjustments */
	@media (max-width: 768px) {
		.sequence-info {
			padding: 0.75rem;
		}

		.info-row {
			gap: 0.375rem;
		}

		.info-badge {
			font-size: 0.75rem;
			padding: 0.25rem 0.5rem;
		}

		.sequence-title {
			font-size: 1.25rem;
		}
	}
</style>
