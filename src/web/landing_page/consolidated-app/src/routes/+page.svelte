<script lang="ts">
	import Hero from '$lib/components/landing/Hero.svelte';

	let isVisible = $state(false);

	// Use $effect to handle mounting behavior with runes
	$effect(() => {
		isVisible = true;
	});
</script>

<svelte:head>
	<title>The Kinetic Alphabet - Flow Arts Choreography Toolbox</title>
	<meta name="description" content="The Kinetic Alphabet is a revolutionary flow arts choreography toolbox for poi, staff, fans, and other flow arts. Learn, create, and share movement sequences." />
</svelte:head>

<div class="landing-page" class:visible={isVisible}>
	<Hero />
</div>

<style>
	.landing-page {
		opacity: 0;
		transform: translateY(20px);
		transition: all 0.8s ease;
	}

	.landing-page.visible {
		opacity: 1;
		transform: translateY(0);
	}

	@media (prefers-reduced-motion: reduce) {
		.landing-page {
			opacity: 1;
			transform: none;
			transition: none;
		}
	}
</style>
