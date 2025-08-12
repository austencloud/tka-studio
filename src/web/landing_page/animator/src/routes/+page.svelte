<script lang="ts">
	import AnimatorApp from '$lib/animator/AnimatorApp.svelte';
	import { browser } from '$app/environment';

	// State using Svelte 5 runes
	let isClient = $state(false);

	// Metadata for SEO and accessibility
	const title = 'Pictograph Animator - Interactive Prop Visualization';
	const description =
		'Visualize and animate flow art patterns with this interactive tool for props like poi, staff, and hoops.';

	// Handle client-side hydration properly to avoid SSR issues with canvas
	$effect(() => {
		if (browser) {
			isClient = true;
		}
	});
</script>

<svelte:head>
	<title>{title}</title>
	<meta name="description" content={description} />
	<meta name="viewport" content="width=device-width, initial-scale=1" />
</svelte:head>

<main>
	{#if isClient}
		<AnimatorApp />
	{:else}
		<div class="loading">
			<p>Loading animator...</p>
		</div>
	{/if}
</main>

<style>
	/* Page layout */
	main {
		width: 100%;
		height: 100vh;
		height: 100dvh;
		display: flex;
		flex-direction: column;
	}

	.loading {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 400px;
		background-color: var(--color-background, #f9f9f9);
		border-radius: 6px;
		color: var(--color-text-primary, #333);
	}
</style>
