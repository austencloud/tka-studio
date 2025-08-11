<script lang="ts">
	import type { Snippet } from 'svelte';

	// ✅ PURE RUNES: Props using modern Svelte 5 runes
	const {
		isNavigationCollapsed = false,
		navigationSidebar,
		centerPanel,
		rightPanel,
	} = $props<{
		isNavigationCollapsed?: boolean;
		navigationSidebar: Snippet;
		centerPanel: Snippet;
		rightPanel: Snippet;
	}>();
</script>

<!-- Main three-column layout: Navigation | Panels | Viewer -->
<div class="main-layout">
	<!-- Navigation Sidebar (left) -->
	<div class="navigation-sidebar-container" class:collapsed={isNavigationCollapsed}>
		{@render navigationSidebar()}
	</div>

	<!-- Center - Stacked panels (Filter/Browser) -->
	<div class="center-panel-stack">
		{@render centerPanel()}
	</div>

	<!-- Right side - Sequence Viewer Panel -->
	<div class="right-panel">
		{@render rightPanel()}
	</div>
</div>

<style>
	.main-layout {
		display: flex;
		flex: 1;
		gap: 0;
		overflow: hidden;
	}

	/* Three-column layout */
	.navigation-sidebar-container {
		flex: 0 0 250px; /* Fixed width for navigation */
		display: flex;
		flex-direction: column;
		overflow: hidden;
		border-right: var(--glass-border);
		background: rgba(255, 255, 255, 0.05);
		transition: flex-basis var(--transition-normal);
	}

	.navigation-sidebar-container.collapsed {
		flex: 0 0 60px; /* Collapsed width */
	}

	.center-panel-stack {
		flex: 1; /* Flexible width for main content */
		display: flex;
		flex-direction: column;
		overflow: hidden;
		min-width: 0;
	}

	.right-panel {
		flex: 0 0 350px; /* Fixed width for viewer */
		display: flex;
		flex-direction: column;
		overflow: hidden;
		min-width: 0;
		border-left: var(--glass-border);
	}

	/* Responsive design */
	@media (max-width: 1200px) {
		.navigation-sidebar-container {
			flex: 0 0 200px; /* Smaller navigation on tablets */
		}

		.right-panel {
			flex: 0 0 300px; /* Smaller viewer on tablets */
		}
	}

	@media (max-width: 1024px) {
		.main-layout {
			flex-direction: column;
		}

		.navigation-sidebar-container {
			flex: 0 0 auto;
			max-height: 200px;
			border-right: none;
			border-bottom: var(--glass-border);
		}

		.center-panel-stack {
			flex: 1;
		}

		.right-panel {
			flex: 0 0 auto;
			max-height: 400px;
			border-left: none;
			border-top: var(--glass-border);
		}
	}

	@media (max-width: 768px) {
		.main-layout {
			gap: 0;
		}
	}
</style>
