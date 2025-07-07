<!--
  LoadingOverlay Component
  
  Shows a loading overlay during transitions.
-->
<script lang="ts">
  import LoadingSpinner from '$lib/features/constructor/components/shared/LoadingSpinner.svelte';
	import { fade } from 'svelte/transition';

	export let visible = false;
	export let message = 'Loading...';
	export let transitionDuration = 300;
</script>

{#if visible}
	<div 
		class="loading-overlay" 
		transition:fade={{ duration: transitionDuration }}
	>
		<div class="loading-content">
			<LoadingSpinner size="large" />
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
		background: rgba(255, 255, 255, 0.9);
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 1000;
		border-radius: inherit;
	}

	.loading-content {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 16px;
	}

	.loading-message {
		margin: 0;
		font-size: 16px;
		color: #4a5568;
		font-weight: 500;
	}
</style>
