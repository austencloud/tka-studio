<!--
  PictographError Component

  Shows error state for pictograph components.
-->
<script lang="ts">
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	export let error: any = null;
	export let debug = false;
	export let animationDuration = 200;

	const dispatch = createEventDispatcher();

	$: errorMessage = getErrorMessage(error);

	function getErrorMessage(error: any): string {
		if (!error) return 'Unknown error';
		if (typeof error === 'string') return error;
		if (error.message) return error.message;
		return 'An error occurred';
	}

	function handleRetry() {
		dispatch('retry');
	}
</script>

<div class="pictograph-error" class:debug transition:fade={{ duration: animationDuration }}>
	<div class="error-icon">
		<svg viewBox="0 0 950 950" xmlns="http://www.w3.org/2000/svg">
			<circle cx="475" cy="450" r="40" fill="#fed7d7" />
			<text
				x="475"
				y="450"
				dominant-baseline="middle"
				text-anchor="middle"
				font-size="40"
				fill="#e53e3e"
			>
				!
			</text>
		</svg>
	</div>

	<div class="error-content">
		<div class="error-title">Error</div>
		<div class="error-message">{errorMessage}</div>

		{#if debug && error}
			<details class="error-details">
				<summary>Debug Info</summary>
				<pre>{JSON.stringify(error, null, 2)}</pre>
			</details>
		{/if}

		<button class="retry-button" on:click={handleRetry}>
			Retry
		</button>
	</div>
</div>

<style>
	.pictograph-error {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		width: 100%;
		height: 100%;
		background: rgba(254, 215, 215, 0.1);
		border-radius: 8px;
		padding: 16px;
		text-align: center;
	}

	.error-icon {
		width: 60px;
		height: 60px;
		margin-bottom: 12px;
	}

	.error-icon svg {
		width: 100%;
		height: 100%;
	}

	.error-content {
		max-width: 200px;
	}

	.error-title {
		font-size: 16px;
		font-weight: 600;
		color: #e53e3e;
		margin-bottom: 4px;
	}

	.error-message {
		font-size: 12px;
		color: #718096;
		margin-bottom: 12px;
		line-height: 1.4;
	}

	.error-details {
		margin-bottom: 12px;
		text-align: left;
	}

	.error-details summary {
		font-size: 11px;
		color: #a0aec0;
		cursor: pointer;
		margin-bottom: 4px;
	}

	.error-details pre {
		font-size: 10px;
		color: #4a5568;
		background: rgba(0, 0, 0, 0.05);
		padding: 8px;
		border-radius: 4px;
		overflow: auto;
		max-height: 100px;
	}

	.retry-button {
		background: #4299e1;
		color: white;
		border: none;
		padding: 6px 12px;
		border-radius: 4px;
		font-size: 12px;
		cursor: pointer;
		transition: background-color 0.2s;
	}

	.retry-button:hover {
		background: #3182ce;
	}

	.pictograph-error.debug {
		border: 2px dashed #f56565;
		background: rgba(254, 215, 215, 0.2);
	}
</style>
