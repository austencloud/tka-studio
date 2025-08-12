<!--
Pictograph Demo Test Route

Test route for E2E pictograph testing. Provides a controlled environment
with data-testid attributes for reliable test automation.
-->
<script lang="ts">
	import PictographDemo from '$lib/components/demo/PictographDemo.svelte';
</script>

<svelte:head>
	<title>Pictograph Demo Test</title>
</svelte:head>

<main class="test-page">
	<div class="test-wrapper" data-testid="pictograph-demo-test">
		<PictographDemo />
	</div>
</main>

<style>
	.test-page {
		padding: 1rem;
		min-height: 100vh;
		background: #f8fafc;
	}

	.test-wrapper {
		max-width: 1400px;
		margin: 0 auto;
		background: white;
		border-radius: 8px;
		padding: 2rem;
		box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
	}
</style>
