<!-- src/routes/auth/callback/[platform]/+page.svelte -->
<script lang="ts">
	import { onMount } from 'svelte';
	import { page } from '$app/stores'; // TODO: Update to use the new API
	import { goto } from '$app/navigation';
	import { handleOAuthCallback } from '$lib/services/auth';
	import { logger } from '$lib/core/logging';

	let isProcessing = $state(true);
	let success = $state(false);
	let errorMessage = $state('');

	onMount(async () => {
		try {
			// Get platform from route parameter
			const platform = $page.params.platform?.toUpperCase();
			if (!platform) {
				throw new Error('Platform not specified');
			}

			// Get authorization code from URL
			const code = $page.url.searchParams.get('code');
			if (!code) {
				throw new Error('Authorization code not found');
			}

			// Handle the callback
			success = await handleOAuthCallback(platform, code);

			// Redirect back to the app after a short delay
			setTimeout(() => {
				goto('/');
			}, 2000);
		} catch (error) {
			logger.error('OAuth callback error', {
				error: error instanceof Error ? error : new Error(String(error))
			});
			errorMessage = error instanceof Error ? error.message : 'Authentication failed';
			success = false;
		} finally {
			isProcessing = false;
		}
	});
</script>

<div class="auth-callback-container">
	<div class="auth-callback-card">
		<h1>Authentication {isProcessing ? 'in progress' : success ? 'successful' : 'failed'}</h1>

		{#if isProcessing}
			<div class="loading-spinner">
				<i class="fa-solid fa-spinner fa-spin"></i>
			</div>
			<p>Processing your authentication...</p>
		{:else if success}
			<div class="success-icon">
				<i class="fa-solid fa-check-circle"></i>
			</div>
			<p>Authentication successful! Redirecting you back to the app...</p>
		{:else}
			<div class="error-icon">
				<i class="fa-solid fa-exclamation-circle"></i>
			</div>
			<p>Authentication failed: {errorMessage}</p>
			<button onclick={() => goto('/')}>Return to App</button>
		{/if}
	</div>
</div>

<style>
	.auth-callback-container {
		display: flex;
		justify-content: center;
		align-items: center;
		min-height: 100vh;
		background-color: #f5f5f5;
	}

	.auth-callback-card {
		background-color: white;
		border-radius: 8px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		padding: 2rem;
		text-align: center;
		max-width: 400px;
		width: 90%;
	}

	h1 {
		font-size: 1.5rem;
		margin-bottom: 1.5rem;
		color: #333;
	}

	.loading-spinner,
	.success-icon,
	.error-icon {
		font-size: 3rem;
		margin-bottom: 1rem;
	}

	.loading-spinner {
		color: #3498db;
	}

	.success-icon {
		color: #2ecc71;
	}

	.error-icon {
		color: #e74c3c;
	}

	p {
		margin-bottom: 1.5rem;
		color: #666;
	}

	button {
		background-color: #3498db;
		color: white;
		border: none;
		border-radius: 4px;
		padding: 0.75rem 1.5rem;
		font-size: 1rem;
		cursor: pointer;
		transition: background-color 0.3s;
	}

	button:hover {
		background-color: #2980b9;
	}
</style>
