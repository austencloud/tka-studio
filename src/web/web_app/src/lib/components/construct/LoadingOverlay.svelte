<!--
	LoadingOverlay.svelte
	
	A reusable loading overlay component extracted from ConstructTab.
	Shows a spinner and message while operations are in progress.
-->
<script lang="ts">
	// Props
	const { message = 'Processing...' } = $props<{ message?: string }>();
</script>

<div class="loading-overlay" data-testid="loading-overlay">
	<div class="loading-spinner"></div>
	<p>{message}</p>
</div>

<style>
	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		backdrop-filter: blur(4px);
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 4px solid var(--muted);
		border-top: 4px solid var(--primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: var(--spacing-md);
	}

	.loading-overlay p {
		color: var(--foreground);
		font-size: var(--font-size-lg);
		margin: 0;
		font-weight: 500;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}
</style>
