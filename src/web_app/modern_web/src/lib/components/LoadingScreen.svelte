/**
 * Loading Screen - Pure Svelte 5 implementation
 * 
 * Shows loading progress during application initialization.
 */

<script lang="ts">
	interface Props {
		progress?: number;
		message?: string;
	}

	let { progress = 0, message = 'Loading...' }: Props = $props();

	// Ensure progress is within bounds
	const clampedProgress = $derived(Math.max(0, Math.min(100, progress)));
</script>

<div class="loading-screen">
	<div class="loading-content">
		<div class="spinner"></div>
		<h2>TKA - The Kinetic Constructor</h2>
		<p class="message">{message}</p>
		
		<div class="progress-container">
			<div class="progress-bar">
				<div 
					class="progress-fill" 
					style="width: {clampedProgress}%"
				></div>
			</div>
			<span class="progress-text">{Math.round(clampedProgress)}%</span>
		</div>
	</div>
</div>

<style>
	.loading-screen {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		background: var(--gradient-cosmic);
		color: var(--foreground);
	}

	.loading-content {
		text-align: center;
		max-width: 400px;
		padding: var(--spacing-2xl);
	}

	.spinner {
		width: 60px;
		height: 60px;
		border: 4px solid rgba(255, 255, 255, 0.1);
		border-top: 4px solid var(--primary-color);
		border-radius: 50%;
		animation: spin 1s linear infinite;
		margin: 0 auto var(--spacing-lg);
	}

	h2 {
		font-size: var(--font-size-2xl);
		font-weight: 600;
		margin-bottom: var(--spacing-md);
		background: var(--gradient-primary);
		background-clip: text;
		-webkit-background-clip: text;
		color: transparent;
	}

	.message {
		font-size: var(--font-size-lg);
		color: var(--muted-foreground);
		margin-bottom: var(--spacing-xl);
	}

	.progress-container {
		display: flex;
		align-items: center;
		gap: var(--spacing-md);
	}

	.progress-bar {
		flex: 1;
		height: 8px;
		background: rgba(255, 255, 255, 0.1);
		border-radius: 4px;
		overflow: hidden;
		backdrop-filter: blur(10px);
	}

	.progress-fill {
		height: 100%;
		background: var(--gradient-primary);
		transition: width var(--transition-normal);
		border-radius: 4px;
	}

	.progress-text {
		font-size: var(--font-size-sm);
		font-weight: 500;
		color: var(--foreground);
		min-width: 40px;
	}

	@keyframes spin {
		0% { transform: rotate(0deg); }
		100% { transform: rotate(360deg); }
	}
</style>
