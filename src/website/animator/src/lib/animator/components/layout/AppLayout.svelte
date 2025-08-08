<script lang="ts">
	import type { Snippet } from 'svelte';

	// Props
	let {
		sidebarWidth = typeof window !== 'undefined' ? window.innerWidth * 0.5 : 600, // Default to 50% of viewport width
		isResizing = false,
		onResizeStart,
		sidebar,
		children
	}: {
		sidebarWidth?: number;
		isResizing?: boolean;
		onResizeStart?: (_e: MouseEvent) => void;
		sidebar?: Snippet;
		children?: Snippet;
	} = $props();
</script>

<div class="app-layout">
	<!-- Left Sidebar: Sequence Browser -->
	<aside class="sidebar" style:width="{sidebarWidth}px">
		{@render sidebar?.()}
	</aside>

	<!-- Resizable Splitter -->
	<button
		type="button"
		class="resize-handle"
		class:resizing={isResizing}
		onmousedown={onResizeStart}
		title="Drag to resize sidebar"
		aria-label="Resize sidebar"
	></button>

	<!-- Right Main Area: Animator -->
	<main class="main-content">
		{@render children?.()}
	</main>
</div>

<style>
	.app-layout {
		display: flex;
		flex: 1;
		min-height: 0; /* Important for flex children to shrink */
	}

	/* Left Sidebar */
	.sidebar {
		background: var(--color-surface);
		border-right: 1px solid var(--color-border);
		display: flex;
		flex-direction: column;
		flex-shrink: 0;
		min-width: 300px;
		max-width: 80vw;
		transition: all 0.3s ease;
	}

	/* Resize Handle */
	.resize-handle {
		width: 4px;
		background: var(--color-border);
		cursor: col-resize;
		flex-shrink: 0;
		transition: background-color 0.2s ease;
		position: relative;
		border: none;
	}

	.resize-handle:hover {
		background: var(--color-primary);
	}

	.resize-handle.resizing {
		background: var(--color-primary);
	}

	.resize-handle::before {
		content: '';
		position: absolute;
		top: 0;
		left: -2px;
		right: -2px;
		bottom: 0;
		cursor: col-resize;
	}

	/* Right Main Content */
	.main-content {
		flex: 1;
		display: flex;
		flex-direction: column;
		min-width: 0; /* Important for flex children to shrink */
		background: var(--color-background);
		transition: background-color 0.3s ease;
		overflow-y: auto;
		min-height: 0;
	}

	/* Responsive Design */
	@media (max-width: 1200px) {
		.resize-handle {
			width: 6px;
		}
	}

	/* Tablet Layout */
	@media (max-width: 1024px) {
		.app-layout {
			flex-direction: column;
		}

		.sidebar {
			width: 100% !important;
			height: 45vh;
			max-height: 500px;
			border-right: none;
			border-bottom: 1px solid var(--color-border, #e0e0e0);
			min-width: unset;
			max-width: unset;
		}

		.resize-handle {
			display: none;
		}

		.main-content {
			height: 55vh;
			min-height: 400px;
		}
	}

	/* Mobile Layout */
	@media (max-width: 768px) {
		.app-layout {
			flex-direction: column;
			height: calc(100vh - 60px); /* Account for header */
			height: calc(100dvh - 60px);
		}

		.sidebar {
			width: 100% !important;
			height: 60vh; /* Increased from 50vh for better browsing */
			max-height: none;
			border-right: none;
			border-bottom: 1px solid var(--color-border);
			min-width: unset;
			max-width: unset;
			overflow: hidden;
		}

		.main-content {
			height: 40vh; /* Reduced to give more space to sidebar */
			min-height: 200px;
			overflow: hidden;
		}
	}

	/* Small Mobile Layout */
	@media (max-width: 480px) {
		.sidebar {
			height: 65vh; /* Even more space for browsing on small screens */
		}

		.main-content {
			height: 35vh;
			min-height: 180px;
		}
	}
</style>
