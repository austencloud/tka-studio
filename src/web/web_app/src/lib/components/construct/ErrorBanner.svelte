<!--
	ErrorBanner.svelte

	A reusable error banner component extracted from ConstructTab.
	Displays error messages with a dismiss button.
-->
<script lang="ts">
	import { clearError } from '$stores/constructTabState.svelte';

	// Props
	const { message } = $props<{ message: string }>();

	function handleDismiss() {
		clearError();
	}
</script>

<div class="error-banner" data-testid="error-banner">
	<p>❌ {message}</p>
	<button type="button" onclick={handleDismiss}>Dismiss</button>
</div>

<style>
	.error-banner {
		flex-shrink: 0;
		background: var(--destructive) / 10;
		color: var(--destructive);
		padding: var(--spacing-md) var(--spacing-lg);
		display: flex;
		justify-content: space-between;
		align-items: center;
		border-bottom: 1px solid var(--destructive) / 20;
	}

	.error-banner p {
		margin: 0;
		font-size: var(--font-size-sm);
	}

	.error-banner button {
		padding: var(--spacing-xs) var(--spacing-sm);
		background: var(--destructive);
		color: var(--destructive-foreground);
		border: none;
		border-radius: var(--border-radius-sm);
		cursor: pointer;
		font-size: var(--font-size-xs);
	}

	.error-banner button:hover {
		opacity: 0.9;
	}
</style>
