<script lang="ts">
	import AnimatorApp from '$lib/animator/AnimatorApp.svelte';
	import { onMount } from 'svelte';

	let isLoaded = $state(false);

	onMount(() => {
		// Initialize animator
		setTimeout(() => {
			isLoaded = true;
		}, 300);
	});
</script>

<svelte:head>
	<title>Animator - The Kinetic Alphabet</title>
	<meta name="description" content="Animate and visualize flow arts sequences with the TKA Animator." />
</svelte:head>

<div class="animator-container">
	{#if isLoaded}
		<AnimatorApp />
	{:else}
		<div class="loading-state">
			<div class="loading-spinner"></div>
			<p>Loading Animator...</p>
		</div>
	{/if}
</div>

<style>
	.animator-container {
		height: 100vh;
		background: var(--surface-color);
	}

	.loading-state {
		display: flex;
		flex-direction: column;
		justify-content: center;
		align-items: center;
		height: 100vh;
		gap: 1rem;
		color: var(--text-color);
	}

	.loading-spinner {
		width: 40px;
		height: 40px;
		border: 3px solid var(--surface-color);
		border-top: 3px solid var(--primary-color);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
