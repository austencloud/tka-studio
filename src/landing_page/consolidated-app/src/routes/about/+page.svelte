<script lang="ts">
	import AboutContent from '$lib/components/landing/About.svelte';
</script>

<svelte:head>
	<title>About - The Kinetic Alphabet</title>
	<meta name="description" content="Learn about The Kinetic Alphabet system and its revolutionary approach to flow arts choreography." />
</svelte:head>

<div class="about-page">
	<AboutContent />
</div>

<style>
	.about-page {
		min-height: 100vh;
		padding: 2rem;
	}
</style>