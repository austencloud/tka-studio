<script lang="ts">
	interface Props {
		error: string;
		onRetry: () => void;
	}

	let { error, onRetry }: Props = $props();

	// Extract error details if possible
	const errorDetails = $derived(() => {
		try {
			// Try to parse if it's a JSON error
			const parsed = JSON.parse(error);
			return parsed;
		} catch {
			// Return as plain string
			return { message: error };
		}
	});

	const displayMessage = $derived(() => {
		if (typeof errorDetails === 'object' && errorDetails && 'message' in errorDetails) {
			return (errorDetails as { message: string }).message;
		}
		return error;
	});
</script>

/** * Error Screen - Pure Svelte 5 implementation * * Shows error state with retry functionality
during application initialization. */

<div class="error-screen">
	<div class="error-content glass-surface">
		<div class="error-icon">
			<svg
				width="64"
				height="64"
				viewBox="0 0 24 24"
				fill="none"
				xmlns="http://www.w3.org/2000/svg"
			>
				<circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2" />
				<path d="m15 9-6 6" stroke="currentColor" stroke-width="2" />
				<path d="m9 9 6 6" stroke="currentColor" stroke-width="2" />
			</svg>
		</div>

		<h1>Initialization Failed</h1>
		<p class="error-message">{displayMessage}</p>

		<div class="error-actions">
			<button class="btn btn-primary" onclick={onRetry}>
				<svg
					width="16"
					height="16"
					viewBox="0 0 24 24"
					fill="none"
					xmlns="http://www.w3.org/2000/svg"
				>
					<path
						d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"
						stroke="currentColor"
						stroke-width="2"
					/>
					<path d="M21 3v5h-5" stroke="currentColor" stroke-width="2" />
					<path
						d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"
						stroke="currentColor"
						stroke-width="2"
					/>
					<path d="M8 16H3v5" stroke="currentColor" stroke-width="2" />
				</svg>
				Retry
			</button>

			<button class="btn btn-glass" onclick={() => (window.location.href = '/')}>
				Go Home
			</button>
		</div>

		<details class="error-details">
			<summary>Technical Details</summary>
			<pre class="error-stack">{error}</pre>
		</details>
	</div>
</div>

<style>
	.error-screen {
		display: flex;
		align-items: center;
		justify-content: center;
		min-height: 100vh;
		padding: var(--spacing-lg);
		background: var(--gradient-cosmic);
	}

	.error-content {
		max-width: 500px;
		padding: var(--spacing-2xl);
		text-align: center;
		color: var(--foreground);
	}

	.error-icon {
		color: #ef4444;
		margin-bottom: var(--spacing-lg);
	}

	h1 {
		font-size: var(--font-size-2xl);
		font-weight: 600;
		margin-bottom: var(--spacing-md);
		color: var(--foreground);
	}

	.error-message {
		font-size: var(--font-size-base);
		color: var(--muted-foreground);
		margin-bottom: var(--spacing-xl);
		line-height: 1.6;
	}

	.error-actions {
		display: flex;
		gap: var(--spacing-md);
		justify-content: center;
		margin-bottom: var(--spacing-xl);
	}

	.error-details {
		margin-top: var(--spacing-lg);
		text-align: left;
	}

	.error-details summary {
		cursor: pointer;
		padding: var(--spacing-sm);
		font-size: var(--font-size-sm);
		color: var(--muted-foreground);
		user-select: none;
	}

	.error-details summary:hover {
		color: var(--foreground);
	}

	.error-stack {
		background: rgba(0, 0, 0, 0.2);
		padding: var(--spacing-md);
		border-radius: 8px;
		font-size: var(--font-size-xs);
		color: var(--muted-foreground);
		white-space: pre-wrap;
		word-break: break-word;
		max-height: 200px;
		overflow-y: auto;
		margin-top: var(--spacing-sm);
	}

	/* Button overrides for error screen */
	.btn {
		display: inline-flex;
		align-items: center;
		gap: var(--spacing-xs);
		min-width: 120px;
	}

	.btn svg {
		width: 16px;
		height: 16px;
	}
</style>
