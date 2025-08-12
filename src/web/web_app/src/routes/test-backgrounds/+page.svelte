<script lang="ts">
	import BackgroundDemo from '$lib/components/backgrounds/BackgroundDemo.svelte';
</script>

<svelte:head>
	<title>Background System Test</title>
</svelte:head>

<main>
	<h1>Background Animation System Test</h1>
	<p>Testing the complete background system with interactive controls</p>

	<div class="demo-container">
		<BackgroundDemo
			backgroundType="snowfall"
			quality="medium"
			showControls={true}
			width={1200}
			height={800}
		/>
	</div>
</main>

<style>
	main {
		padding: 20px;
		font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
	}

	h1 {
		color: #333;
		margin-bottom: 10px;
	}

	p {
		color: #666;
		margin-bottom: 30px;
	}

	.demo-container {
		border: 2px solid #ddd;
		border-radius: 8px;
		overflow: hidden;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
	}
</style>
