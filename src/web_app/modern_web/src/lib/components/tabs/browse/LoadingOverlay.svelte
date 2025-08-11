<script lang="ts">
	import { fade } from 'svelte/transition';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		show = false,
		message = 'Loading...',
		detail = '',
	} = $props<{
		show?: boolean;
		message?: string;
		detail?: string;
	}>();
</script>

<!-- Loading overlay -->
{#if show}
	<div class="loading-overlay" transition:fade>
		<div class="loading-content">
			<div class="loading-spinner"></div>
			<p>{message}</p>
			{#if detail}
				<p class="loading-detail">{detail}</p>
			{/if}
		</div>
	</div>
{/if}

<style>
	.loading-overlay {
		position: absolute;
		inset: 0;
		background: rgba(0, 0, 0, 0.5);
		backdrop-filter: blur(4px);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
	}

	.loading-content {
		background: white;
		border-radius: 12px;
		padding: var(--spacing-xl);
		text-align: center;
		box-shadow: 0 20px 50px rgba(0, 0, 0, 0.3);
		max-width: 300px;
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 3px solid #e2e8f0;
		border-top-color: var(--primary-color);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto var(--spacing-md);
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	.loading-content p {
		margin: 0;
		color: #374151;
		font-weight: 600;
	}

	.loading-detail {
		font-size: var(--font-size-sm);
		color: #6b7280;
		font-weight: 400;
		margin-top: var(--spacing-xs);
	}
</style>
