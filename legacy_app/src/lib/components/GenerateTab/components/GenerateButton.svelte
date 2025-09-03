<!-- src/lib/components/GenerateTab/components/GenerateButton.svelte -->
<script lang="ts">
	import { slide } from 'svelte/transition';

	// Use Svelte 5 props rune instead of export let
	const props = $props<{
		isLoading?: boolean;
		hasError?: boolean;
		statusMessage?: string;
		text?: string;
		onClick?: () => void;
	}>();

	// Default values with derived values
	const isLoading = $derived(props.isLoading ?? false);
	const hasError = $derived(props.hasError ?? false);
	const statusMessage = $derived(props.statusMessage ?? '');
	const text = $derived(props.text ?? 'Generate Sequence');

	// Handle click
	function handleClick() {
		if (!isLoading && props.onClick) {
			props.onClick();
		}
	}
</script>

<div class="button-container">
	<button
		class="generate-button"
		class:loading={isLoading}
		class:error={hasError}
		onclick={handleClick}
		disabled={isLoading}
	>
		<div class="button-content">
			{#if isLoading}
				<div class="spinner-container">
					<div class="spinner"></div>
				</div>
				<span class="button-text">{statusMessage || 'Generating...'}</span>
			{:else if hasError}
				<div class="icon-container error-icon">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<path
							d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
						></path>
						<line x1="12" y1="9" x2="12" y2="13"></line>
						<line x1="12" y1="17" x2="12.01" y2="17"></line>
					</svg>
				</div>
				<span class="button-text">Try Again</span>
			{:else}
				<div class="icon-container">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2"
						stroke-linecap="round"
						stroke-linejoin="round"
					>
						<polygon points="5 3 19 12 5 21 5 3"></polygon>
					</svg>
				</div>
				<span class="button-text">{text}</span>
			{/if}
		</div>

		<div class="button-background"></div>
	</button>

	{#if hasError}
		<div class="error-message" transition:slide={{ duration: 300 }}>
			{statusMessage}
		</div>
	{/if}
</div>

<style>
	.button-container {
		display: flex;
		flex-direction: column;
		align-items: center;
		gap: 0.75rem;
		width: 100%;
		max-width: 300px;
	}

	.generate-button {
		position: relative;
		width: 100%;
		padding: 0;
		border: none;
		border-radius: 0.5rem;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		overflow: hidden;
		background: transparent;
		height: 3.5rem;
	}

	.button-content {
		position: relative;
		z-index: 2;
		display: flex;
		align-items: center;
		justify-content: center;
		gap: 0.75rem;
		width: 100%;
		height: 100%;
		padding: 0 1.5rem;
		color: white;
	}

	.button-background {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: linear-gradient(
			135deg,
			var(--color-accent, #3a7bd5),
			var(--color-accent-secondary, #2a5298)
		);
		z-index: 1;
		transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
	}

	.generate-button:hover:not(:disabled) .button-background {
		transform: scale(1.05);
	}

	.generate-button:active:not(:disabled) .button-background {
		transform: scale(0.98);
	}

	.generate-button:disabled {
		cursor: not-allowed;
	}

	.generate-button:disabled .button-background {
		opacity: 0.7;
	}

	.loading .button-background {
		background: linear-gradient(
			135deg,
			var(--color-accent-muted, #5a8bd5),
			var(--color-accent, #3a7bd5)
		);
		animation: pulse 2s infinite;
	}

	.error .button-background {
		background: linear-gradient(
			135deg,
			var(--color-error, #d54a3a),
			var(--color-error-dark, #b83a2e)
		);
	}

	.button-text {
		font-weight: 600;
		letter-spacing: 0.02em;
	}

	.icon-container,
	.spinner-container {
		display: flex;
		align-items: center;
		justify-content: center;
		width: 1.5rem;
		height: 1.5rem;
	}

	.error-icon {
		color: rgba(255, 255, 255, 0.9);
	}

	.error-message {
		color: var(--color-error, #d54a3a);
		font-size: 0.875rem;
		text-align: center;
		max-width: 300px;
		padding: 0.75rem 1rem;
		background: rgba(213, 74, 58, 0.1);
		border-radius: 0.375rem;
		border-left: 3px solid var(--color-error, #d54a3a);
		width: 100%;
	}

	.spinner {
		width: 1.25rem;
		height: 1.25rem;
		border: 2px solid rgba(255, 255, 255, 0.3);
		border-radius: 50%;
		border-top-color: white;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		to {
			transform: rotate(360deg);
		}
	}

	@keyframes pulse {
		0% {
			opacity: 1;
		}
		50% {
			opacity: 0.8;
		}
		100% {
			opacity: 1;
		}
	}

	/* Add a subtle shadow effect */
	.generate-button::after {
		content: '';
		position: absolute;
		bottom: -5px;
		left: 5%;
		width: 90%;
		height: 10px;
		background: rgba(0, 0, 0, 0.2);
		filter: blur(10px);
		border-radius: 50%;
		z-index: 0;
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.generate-button:hover:not(:disabled)::after {
		opacity: 0.5;
	}
</style>
