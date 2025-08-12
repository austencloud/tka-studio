<script>
	import ReactivityTest from '$lib/test/ReactivityTest.svelte';
</script>

<svelte:head>
	<title>Reactivity Test</title>
</svelte:head>

<main>
	<h1>Svelte 5 Runes Reactivity Test</h1>
	<ReactivityTest />
</main>

<style>
	main {
		padding: 20px;
		background: #0a0a0a;
		color: white;
		min-height: 100vh;
	}

	h1 {
		color: #fff;
		margin-bottom: 20px;
	}
</style>
