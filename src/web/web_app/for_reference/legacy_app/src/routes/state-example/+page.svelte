<script lang="ts">
	import StateExample from '$lib/components/examples/ModernStateExample.svelte';
	import ModernStateExample from '$lib/components/examples/ModernStateExample.svelte';

	// Toggle between old and new state management examples
	let showModernExample = false;
</script>

<div class="container">
	<h1>State Management Examples</h1>

	<div class="tabs">
		<button class:active={!showModernExample} on:click={() => (showModernExample = false)}>
			Current Approach
		</button>
		<button class:active={showModernExample} on:click={() => (showModernExample = true)}>
			Modern Approach
		</button>
	</div>

	{#if showModernExample}
		<div class="example-container">
			<p class="description">
				This example demonstrates the new state management approach using containers and XState v5.
				It shows how to use both UI state and sequence state in a Svelte component.
			</p>

			<ModernStateExample />

			<div class="info">
				<h2>Modern State Management</h2>
				<p>The modern state management system uses:</p>
				<ul>
					<li><strong>State Containers</strong> for simple, direct state access</li>
					<li><strong>XState v5</strong> for improved state machines</li>
					<li><strong>Svelte Runes</strong> for universal reactivity (coming with Svelte 5)</li>
				</ul>
				<p>Benefits of the new approach:</p>
				<ul>
					<li>Less boilerplate compared to traditional Svelte stores</li>
					<li>More direct access to state without subscription management</li>
					<li>Better type safety and IDE support</li>
					<li>Unified API for both simple state and complex state machines</li>
				</ul>
			</div>
		</div>
	{:else}
		<div class="example-container">
			<p class="description">
				This example demonstrates the current state management system using XState and Svelte
				stores. Open your browser's developer console to see state changes.
			</p>

			<StateExample />

			<div class="info">
				<h2>Current State Management</h2>
				<p>The current state management system uses:</p>
				<ul>
					<li><strong>XState</strong> for complex state machines</li>
					<li><strong>Svelte stores</strong> for reactive state</li>
					<li><strong>State registry</strong> for centralized state management</li>
				</ul>
				<p>Try interacting with the example above to see how state changes are handled.</p>
			</div>
		</div>
	{/if}
</div>

<style>
	.container {
		max-width: 1000px;
		margin: 0 auto;
		padding: 20px;
		font-family:
			system-ui,
			-apple-system,
			BlinkMacSystemFont,
			'Segoe UI',
			Roboto,
			sans-serif;
	}

	h1 {
		color: #333;
		margin-bottom: 20px;
	}

	.tabs {
		display: flex;
		margin-bottom: 20px;
		border-bottom: 1px solid #ddd;
	}

	.tabs button {
		padding: 10px 20px;
		background: none;
		border: none;
		border-bottom: 3px solid transparent;
		cursor: pointer;
		font-size: 16px;
		color: #666;
	}

	.tabs button.active {
		border-bottom-color: #007bff;
		color: #007bff;
		font-weight: 500;
	}

	.example-container {
		margin-top: 20px;
	}

	.description {
		margin-bottom: 20px;
		color: #555;
		line-height: 1.5;
	}

	.info {
		margin-top: 40px;
		padding: 20px;
		background: #f9f9f9;
		border-left: 4px solid #007bff;
	}

	h2 {
		margin-top: 0;
		color: #333;
	}

	ul {
		margin-left: 20px;
	}

	li {
		margin-bottom: 10px;
		line-height: 1.5;
	}
</style>
