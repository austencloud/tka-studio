<script>
	import DragTestSvelte from '$lib/components/test/DragTestSvelte.svelte';
</script>

<svelte:head>
	<title>Svelte Drag Performance Test</title>
</svelte:head>

<DragTestSvelte />

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
	}
</style>
