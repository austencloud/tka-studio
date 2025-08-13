<!--
Animation States Component

Displays loading, error, and empty states for the animation panel.
-->
<script lang="ts">
	// Props
	const {
		loading = false,
		error = null,
		hasSequence = false,
		onRetry = () => {}
	} = $props<{
		loading?: boolean;
		error?: string | null;
		hasSequence?: boolean;
		onRetry?: () => void;
	}>();
</script>

{#if loading}
	<div class="loading-state">
		<div class="loading-spinner"></div>
		<p>Loading sequence...</p>
	</div>
{:else if error}
	<div class="error-state">
		<p>❌ {error}</p>
		<button onclick={onRetry}>Retry</button>
	</div>
{:else if !hasSequence}
	<div class="empty-state">
		<p>🎬 Select a sequence to animate</p>
		<p class="hint">Click the animate button (🎬) on any sequence card</p>
	</div>
{/if}

<style>
	.loading-state,
	.error-state,
	.empty-state {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		text-align: center;
		padding: 2.5rem 1.5rem;
		color: rgba(255, 255, 255, 0.7);
		background: rgba(255, 255, 255, 0.03);
		border: 1px solid rgba(255, 255, 255, 0.08);
		border-radius: 16px;
		backdrop-filter: blur(10px);
	}

	.loading-spinner {
		width: 36px;
		height: 36px;
		border: 3px solid rgba(255, 255, 255, 0.1);
		border-top: 3px solid #818cf8;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1.25rem;
		box-shadow: 0 0 20px rgba(129, 140, 248, 0.3);
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.error-state button {
		background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
		color: white;
		border: 1px solid rgba(255, 255, 255, 0.2);
		padding: 0.625rem 1.25rem;
		border-radius: 12px;
		cursor: pointer;
		font-size: 0.875rem;
		margin-top: 1rem;
		transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
		backdrop-filter: blur(10px);
		box-shadow: 
			0 2px 8px rgba(99, 102, 241, 0.3),
			inset 0 1px 0 rgba(255, 255, 255, 0.2);
	}

	.error-state button:hover {
		background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);
		transform: translateY(-2px);
		box-shadow: 
			0 6px 20px rgba(99, 102, 241, 0.4),
			inset 0 1px 0 rgba(255, 255, 255, 0.3);
	}

	.hint {
		font-style: italic;
		color: rgba(255, 255, 255, 0.5);
		text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.loading-spinner {
			animation: none;
		}
		
		.error-state button {
			transition: none;
		}
	}
</style>
