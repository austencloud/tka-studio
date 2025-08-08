<script lang="ts">
	import { ANIMATION_CONSTANTS } from '../../constants/animation.js';

	// Modern Svelte 5 props
	let { errorMsg = '', successMsg = '' }: { errorMsg?: string; successMsg?: string } = $props();

	// Auto-hide success message after 5 seconds
	let successTimeout: ReturnType<typeof setTimeout> | null = null;

	// Use $effect instead of reactive statement
	$effect(() => {
		if (successMsg) {
			if (successTimeout) {
				clearTimeout(successTimeout);
			}

			successTimeout = setTimeout(() => {
				successMsg = '';
			}, ANIMATION_CONSTANTS.SUCCESS_MESSAGE_TIMEOUT);
		}

		// Cleanup function
		return () => {
			if (successTimeout) {
				clearTimeout(successTimeout);
			}
		};
	});
</script>

{#if errorMsg}
	<div class="message error" role="alert">
		<div class="message-icon">❌</div>
		<div class="message-content">
			<strong>Error:</strong>
			{errorMsg}
		</div>
	</div>
{/if}

{#if successMsg}
	<div class="message success" role="status">
		<div class="message-icon">✅</div>
		<div class="message-content">
			<strong>Success:</strong>
			{successMsg}
		</div>
	</div>
{/if}

<style>
	.message {
		display: flex;
		align-items: flex-start;
		gap: 0.75rem;
		padding: 1rem;
		border-radius: 8px;
		margin: 0.5rem 0;
		border-left: 4px solid;
		animation: slideIn 0.3s ease-out;
		transition: all 0.3s ease;
	}

	.error {
		background: var(--color-surface);
		border-left-color: var(--color-error);
		color: var(--color-error);
	}

	.success {
		background: var(--color-surface);
		border-left-color: var(--color-success);
		color: var(--color-success);
	}

	.message-icon {
		font-size: 1.2rem;
		flex-shrink: 0;
		margin-top: 0.1rem;
	}

	.message-content {
		flex: 1;
		line-height: 1.5;
	}

	.message-content strong {
		display: block;
		margin-bottom: 0.25rem;
		font-weight: 600;
	}

	@keyframes slideIn {
		from {
			opacity: 0;
			transform: translateY(-10px);
		}
		to {
			opacity: 1;
			transform: translateY(0);
		}
	}

	@media (max-width: 768px) {
		.message {
			padding: 0.75rem;
			gap: 0.5rem;
		}

		.message-icon {
			font-size: 1rem;
		}
	}
</style>
