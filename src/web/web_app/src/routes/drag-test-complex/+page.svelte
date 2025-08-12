<script>
	import DragTestComplex from '$lib/components/test/DragTestComplex.svelte';
</script>

<svelte:head>
	<title>Complex Drag Performance Test</title>
</svelte:head>

<DragTestComplex />

<style>
	:global(body) {
		margin: 0;
		padding: 0;
		overflow: hidden;
	}
</style>
