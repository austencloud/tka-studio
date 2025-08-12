<script lang="ts">
	import ConstructorApp from '$lib/components/constructor/ConstructorApp.svelte';
	import AppNavigation from '$lib/components/constructor/AppNavigation.svelte';
	import { onMount } from 'svelte';

	let isInitialized = $state(false);
	let currentTab = $state('builder');

	function handleTabChange(event: CustomEvent<string>) {
		currentTab = event.detail;
	}

	onMount(() => {
		// Initialize the constructor app
		setTimeout(() => {
			isInitialized = true;
		}, 500);
	});
</script>

<svelte:head>
	<title>Constructor - The Kinetic Alphabet</title>
	<meta name="description" content="Create and visualize flow arts sequences with The Kinetic Constructor." />
</svelte:head>

<div class="constructor-container">
	{#if isInitialized}
		<AppNavigation {currentTab} on:tabChange={handleTabChange} />
		<ConstructorApp {currentTab} />
	{:else}
		<div class="loading-state">
			<div class="loading-spinner"></div>
			<p>Initializing Constructor...</p>
		</div>
	{/if}
</div>

<style>
	.constructor-container {
		height: 100vh;
		display: flex;
		flex-direction: column;
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
