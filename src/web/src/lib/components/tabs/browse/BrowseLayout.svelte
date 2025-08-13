<!--
Enhanced Browse Layout with Unified Panel Management

Provides three-section layout with:
- Unified collapse/expand logic for both side panels
- Splitter components for resizing panels by dragging
- Reactive panel state management using runes + services
-->
<script lang="ts">
	import type { Snippet } from 'svelte';
	import Splitter from '$lib/components/ui/Splitter.svelte';
	import type { PanelStateManager } from '$lib/state/panel-state.svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		panelState,
		navigationSidebar,
		centerPanel,
		rightPanel,
		onNavigationResize = () => {},
		onAnimationResize = () => {},
	} = $props<{
		panelState: PanelStateManager;
		navigationSidebar: Snippet;
		centerPanel: Snippet;
		rightPanel?: Snippet;
		onNavigationResize?: (width: number) => void;
		onAnimationResize?: (width: number) => void;
	}>();

	// ✅ DERIVED RUNES: Computed layout values
	let showRightPanel = $derived(rightPanel && panelState.isAnimationVisible);
	let navigationFlexBasis = $derived(`${panelState.navigationWidth}px`);
	let animationFlexBasis = $derived(`${panelState.animationWidth}px`);
	
	// ✅ RESIZE HANDLERS: Connect splitters to panel state
	function handleNavigationResizeStart(startX: number) {
		panelState.startNavigationResize(startX);
	}

	function handleNavigationResizeMove(deltaX: number) {
		if (!panelState.currentResize) return;
		
		const newX = panelState.currentResize.startX + deltaX;
		panelState.updateCurrentResize(newX);
		
		// Notify parent component of resize
		onNavigationResize(panelState.navigationPanel.width);
	}

	function handleNavigationResizeEnd() {
		panelState.endCurrentResize();
	}

	function handleAnimationResizeStart(startX: number) {
		panelState.startAnimationResize(startX);
	}

	function handleAnimationResizeMove(deltaX: number) {
		if (!panelState.currentResize) return;
		
		const newX = panelState.currentResize.startX - deltaX; // Reversed for right panel
		panelState.updateCurrentResize(newX);
		
		// Notify parent component of resize
		onAnimationResize(panelState.animationPanel.width);
	}

	function handleAnimationResizeEnd() {
		panelState.endCurrentResize();
	}
</script>

<div class="browse-layout" class:resizing={panelState.isAnyPanelResizing}>
	<!-- Navigation Sidebar (left) -->
	<div 
		class="navigation-panel"
		class:collapsed={panelState.isNavigationCollapsed}
		style="flex-basis: {navigationFlexBasis};"
	>
		{@render navigationSidebar()}
	</div>

	<!-- Splitter between navigation and center -->
	<Splitter
		direction="right"
		disabled={panelState.isNavigationCollapsed}
		onResizeStart={handleNavigationResizeStart}
		onResizeMove={handleNavigationResizeMove}
		onResizeEnd={handleNavigationResizeEnd}
	/>

	<!-- Center Panel (flexible) -->
	<div class="center-panel">
		{@render centerPanel()}
	</div>

	<!-- Splitter between center and animation (only when animation panel is visible) -->
	{#if showRightPanel}
		<Splitter
			direction="left"
			disabled={panelState.isAnimationCollapsed}
			onResizeStart={handleAnimationResizeStart}
			onResizeMove={handleAnimationResizeMove}
			onResizeEnd={handleAnimationResizeEnd}
		/>

		<!-- Animation Panel (right) -->
		<div 
			class="animation-panel"
			class:collapsed={panelState.isAnimationCollapsed}
			style="flex-basis: {animationFlexBasis};"
		>
			{@render rightPanel()}
		</div>
	{/if}
</div>

<style>
	.browse-layout {
		display: flex;
		flex: 1;
		height: 100%;
		overflow: hidden;
		background: transparent;
		position: relative;
		color: white;
	}

	.browse-layout.resizing {
		user-select: none;
		cursor: col-resize;
	}

	/* Navigation Panel */
	.navigation-panel {
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		border-right: var(--glass-border);
		background: rgba(255, 255, 255, 0.02);
		backdrop-filter: blur(10px);
		transition: flex-basis var(--transition-normal);
		min-width: 60px; /* Ensure collapsed state is visible */
	}

	/* Disable transitions during resize for immediate feedback */
	.browse-layout.resizing .navigation-panel {
		transition: none;
	}

	.navigation-panel.collapsed {
		flex-basis: 60px !important; /* Override inline style when collapsed */
	}

	/* Center Panel */
	.center-panel {
		flex: 1;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		min-width: 0; /* Allow flex shrinking */
		background: rgba(255, 255, 255, 0.01);
	}

	/* Animation Panel */
	.animation-panel {
		flex-shrink: 0;
		display: flex;
		flex-direction: column;
		overflow: hidden;
		border-left: var(--glass-border);
		background: rgba(255, 255, 255, 0.02);
		backdrop-filter: blur(10px);
		transition: flex-basis var(--transition-normal);
		min-width: 60px; /* Ensure collapsed state is visible */
	}

	/* Disable transitions during resize for immediate feedback */
	.browse-layout.resizing .animation-panel {
		transition: none;
	}

	.animation-panel.collapsed {
		flex-basis: 60px !important; /* Override inline style when collapsed */
	}

	/* Panel borders and glass effect */
	.navigation-panel,
	.animation-panel {
		border-color: rgba(255, 255, 255, 0.1);
	}

	.navigation-panel::before,
	.animation-panel::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(
			135deg,
			rgba(255, 255, 255, 0.05) 0%,
			rgba(255, 255, 255, 0.02) 50%,
			rgba(255, 255, 255, 0.05) 100%
		);
		pointer-events: none;
		opacity: 0;
		transition: opacity var(--transition-normal);
	}

	.navigation-panel:hover::before,
	.animation-panel:hover::before {
		opacity: 1;
	}

	/* Responsive design */
	@media (max-width: 1024px) {
		.browse-layout {
			flex-direction: column;
		}

		.navigation-panel {
			flex-basis: auto !important;
			max-height: 200px;
			border-right: none;
			border-bottom: var(--glass-border);
		}

		.center-panel {
			flex: 1;
		}

		.animation-panel {
			flex-basis: auto !important;
			max-height: 400px;
			border-left: none;
			border-top: var(--glass-border);
		}

		/* Hide splitters on tablet/mobile - panels stack vertically */
		.browse-layout :global(.splitter) {
			display: none;
		}
	}

	@media (max-width: 768px) {
		.navigation-panel,
		.animation-panel {
			/* On mobile, panels could slide in/out or be managed by drawer system */
			position: absolute;
			top: 0;
			bottom: 0;
			z-index: 100;
			transform: translateX(-100%);
			transition: transform var(--transition-normal);
		}

		.animation-panel {
			right: 0;
			left: auto;
			transform: translateX(100%);
		}
	}

	/* High contrast mode support */
	@media (prefers-contrast: high) {
		.navigation-panel,
		.animation-panel {
			border-color: currentColor;
			background: rgba(0, 0, 0, 0.8);
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.navigation-panel,
		.animation-panel,
		.browse-layout {
			transition: none;
		}
	}

	/* Focus management for accessibility */
	.navigation-panel:focus-within,
	.animation-panel:focus-within {
		outline: 2px solid var(--color-primary);
		outline-offset: -2px;
	}

	/* Ensure proper layering during resize */
	.browse-layout.resizing .navigation-panel,
	.browse-layout.resizing .animation-panel {
		z-index: 1;
	}

	.browse-layout.resizing .center-panel {
		z-index: 0;
	}
</style>
