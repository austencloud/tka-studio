<script lang="ts">
	import { fade } from 'svelte/transition';
	import LoadingSpinner from '$lib/components/MainWidget/loading/LoadingSpinner.svelte';

	// Props
	export let visible: boolean = false;
	export let message: string = 'Loading options...';
	export let transitionDuration: number = 200;
</script>

{#if visible}
	<div
		class="loading-overlay"
		in:fade={{ duration: transitionDuration }}
		out:fade={{ duration: transitionDuration }}
	>
		<div class="loading-content">
			<LoadingSpinner size="medium" />
			<p class="loading-message">{message}</p>
		</div>
	</div>
{/if}

<style>
	.loading-overlay {
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background-color: rgba(0, 0, 0, 0.7);
		display: flex;
		justify-content: center;
		align-items: center;
		z-index: 100;
		backdrop-filter: blur(3px);
		-webkit-backdrop-filter: blur(3px);
	}

	.loading-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 1rem;
		padding: 2rem;
		border-radius: 0.5rem;
		background-color: rgba(30, 40, 60, 0.8);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
	}

	.loading-message {
		color: white;
		font-size: 1rem;
		margin: 0;
		text-align: center;
	}

	/* Make the spinner white */
	:global(.loading-overlay .lds-ring div) {
		border-color: white transparent transparent transparent;
	}
</style>
