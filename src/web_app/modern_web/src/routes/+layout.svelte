<script lang="ts">
	import '../app.css';
	import { onMount, setContext } from 'svelte';
	import type { ServiceContainer } from '@tka/shared/di/core/ServiceContainer';
	import type { Snippet } from 'svelte';

	console.log('🔥 Layout script is executing!');

	interface Props {
		children: Snippet;
	}

	let { children }: Props = $props();

	// Application bootstrap
	let container: ServiceContainer | null = $state(null);
	let isInitialized = $state(false);
	let initializationError = $state<string | null>(null);

	console.log('🔥 About to set context...');
	// Set context immediately (will be null initially)
	setContext('di-container', () => container);
	console.log('🔥 Context set!');

	console.log('🔥 About to register onMount...');
	onMount(async () => {
		console.log('🔥🔥🔥 ONMOUNT IS RUNNING! 🔥🔥🔥');
		try {
			console.log('🔥 Layout onMount started - WITH VITE-PLUGIN-TERMINAL!');

			console.log('🔄 About to start DI container initialization...');

		try {
			console.log('🚀 Starting DI container initialization...');

			// Import bootstrap function
			console.log('📦 Importing bootstrap module...');
			const { createWebApplication } = await import('$services/bootstrap');
			console.log('✅ Bootstrap module imported successfully');

			// Create DI container
			console.log('🏗️ Creating DI container...');
			container = await createWebApplication();
			console.log('✅ DI container created successfully');

			// Mark as initialized
			isInitialized = true;
			console.log('✅ DI container initialized successfully');
		} catch (error) {
			console.error('❌ Error during initialization:', error);
			console.error('❌ Error type:', typeof error);
			console.error('❌ Error constructor:', error?.constructor?.name);
			console.error('❌ Error message:', error instanceof Error ? error.message : String(error));
			console.error('❌ Error stack:', error instanceof Error ? error.stack : 'No stack trace');

			initializationError = error instanceof Error ? error.message : 'Unknown error';
			console.error('❌ Failed to initialize application:', error);
		}
	} catch (outerError) {
		console.error('🚨 CRITICAL: onMount itself failed:', outerError);
		initializationError = 'Critical initialization failure';
	}
});
console.log('🔥 onMount registered successfully!');
</script>

<svelte:head>
	<title>TKA - The Kinetic Constructor</title>
</svelte:head>

{#if initializationError}
	<div class="error-screen">
		<h1>Initialization Failed</h1>
		<p>{initializationError}</p>
		<button onclick={() => window.location.reload()}>Retry</button>
	</div>
{:else if !isInitialized}
	<div class="loading-screen">
		<div class="spinner"></div>
		<p>Initializing TKA...</p>
	</div>
{:else}
	<!-- Container is provided via context, children renders with access -->
	{@render children()}
{/if}

<style>
	.error-screen {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		padding: 2rem;
		text-align: center;
	}
	
	.loading-screen {
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		padding: 2rem;
		text-align: center;
	}
	
	.spinner {
		width: 40px;
		height: 40px;
		border: 4px solid #f3f3f3;
		border-top: 4px solid #3498db;
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin-bottom: 1rem;
	}
	
	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
