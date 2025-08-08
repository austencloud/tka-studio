<script lang="ts">
	import type { Snippet } from 'svelte';

	// Props
	let {
		isSticky = false,
		onToggleSticky,
		onCloseSticky,
		children
	}: {
		isSticky?: boolean;
		onToggleSticky?: () => void;
		onCloseSticky?: () => void;
		children?: Snippet;
	} = $props();
</script>

<!-- Mobile sticky animation toggle -->
<button
	type="button"
	class="sticky-toggle mobile-only"
	onclick={onToggleSticky}
	aria-label="Toggle sticky animation viewer"
>
	{isSticky ? 'Exit Sticky View' : 'Sticky View'}
</button>

<div class="canvas-container" class:sticky={isSticky}>
	{#if isSticky}
		<button
			type="button"
			class="close-sticky"
			onclick={onCloseSticky}
			aria-label="Close sticky view"
		>
			✕
		</button>
	{/if}
	{@render children?.()}
</div>

<style>
	/* Sticky Animation Viewer */
	.sticky-toggle {
		margin-top: 0.5rem;
		padding: 0.5rem 1rem;
		background: var(--color-primary);
		color: white;
		border: none;
		border-radius: 6px;
		cursor: pointer;
		font-size: 0.9rem;
		transition: all 0.2s ease;
	}

	.sticky-toggle:hover {
		background: var(--color-primary-dark, #1976d2);
		transform: translateY(-1px);
	}

	.canvas-container {
		display: flex;
		justify-content: center;
		align-items: center;
		padding: 2rem;
		background: var(--color-surface);
		border-radius: 8px;
		border: 1px solid var(--color-border);
		min-height: 500px;
		flex: 1;
		width: 100%;
		max-width: none;
		transition: all 0.3s ease;
		position: relative;
	}

	.canvas-container.sticky {
		position: sticky;
		top: 16px;
		z-index: 100;
		background: var(--color-surface);
		border: 2px solid var(--color-primary);
		border-radius: 12px;
		box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
		margin-bottom: 1rem;
	}

	.close-sticky {
		position: absolute;
		top: 8px;
		right: 8px;
		width: 32px;
		height: 32px;
		background: rgba(0, 0, 0, 0.7);
		color: white;
		border: none;
		border-radius: 50%;
		cursor: pointer;
		font-size: 1.2rem;
		display: flex;
		align-items: center;
		justify-content: center;
		z-index: 10;
		transition: all 0.2s ease;
	}

	.close-sticky:hover {
		background: rgba(0, 0, 0, 0.9);
		transform: scale(1.1);
	}

	/* Mobile/Desktop Visibility Classes */
	.mobile-only {
		display: none;
	}

	/* Mobile Layout */
	@media (max-width: 768px) {
		.mobile-only {
			display: block;
		}

		.canvas-container {
			padding: 0.75rem;
			min-height: 180px;
			flex: 1;
		}
	}

	/* Responsive Design */
	@media (max-width: 1200px) {
		.canvas-container {
			padding: 1.5rem;
			min-height: 400px;
		}
	}

	/* Tablet Layout */
	@media (max-width: 1024px) {
		.canvas-container {
			min-height: 350px;
		}
	}

	/* Small Mobile Layout */
	@media (max-width: 480px) {
		.canvas-container {
			padding: 0.5rem;
			min-height: 150px;
		}
	}
</style>
