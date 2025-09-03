<script lang="ts">
	import { onMount } from 'svelte';
	import { fade } from 'svelte/transition';
	import BrowserPanel from './browser/BrowserPanel.svelte';
	import SheetPanel from './sheet/SheetPanel.svelte';
	import MusicPlayer from './player/MusicPlayer.svelte';
	import ResizeHandle from './browser/ResizeHandle.svelte';
	import * as ToastManager from '../shared/ToastManager.svelte';
	import { actStore } from './stores/actStore';
	import { uiStore } from './stores/uiStore';

	// Handle resize
	function handleResize(width: number) {
		uiStore.updateBrowserPanelWidth(width);
	}

	// Handle keyboard shortcuts
	function handleKeyDown(event: KeyboardEvent) {
		// Check if Ctrl/Cmd key is pressed
		const isCtrlOrCmd = event.ctrlKey || event.metaKey;

		// Undo: Ctrl/Cmd + Z
		if (isCtrlOrCmd && event.key === 'z' && !event.shiftKey) {
			event.preventDefault();
			const actionDescription = actStore.undo();
			if (actionDescription) {
				ToastManager.showInfo(`Undid: ${actionDescription}`, {
					action: {
						label: 'Redo',
						onClick: () => actStore.redo()
					}
				});
			}
		}

		// Redo: Ctrl/Cmd + Shift + Z or Ctrl/Cmd + Y
		if (
			(isCtrlOrCmd && event.key === 'z' && event.shiftKey) ||
			(isCtrlOrCmd && event.key === 'y')
		) {
			event.preventDefault();
			const actionDescription = actStore.redo();
			if (actionDescription) {
				ToastManager.showInfo(`Redid: ${actionDescription}`, {
					action: {
						label: 'Undo',
						onClick: () => actStore.undo()
					}
				});
			}
		}
	}

	// Initialize the act store on mount
	onMount(() => {
		actStore.initialize();

		// Add global keyboard event listener
		window.addEventListener('keydown', handleKeyDown);

		// Clean up on unmount
		return () => {
			window.removeEventListener('keydown', handleKeyDown);
		};
	});
</script>

<div class="write-tab">
	<div class="write-tab-content">
		<div class="sheet-panel-container">
			<SheetPanel />
		</div>

		{#if $uiStore.isBrowserPanelOpen}
			<div class="browser-panel-container" transition:fade={{ duration: 200 }}>
				<div class="resize-handle-wrapper">
					<ResizeHandle onResize={handleResize} />
				</div>
				<BrowserPanel />
			</div>
		{:else}
			<button
				class="open-browser-button"
				on:click={() => uiStore.setBrowserPanelOpen(true)}
				aria-label="Open browser panel"
			>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					width="24"
					height="24"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
				>
					<line x1="3" y1="12" x2="21" y2="12"></line>
					<line x1="3" y1="6" x2="21" y2="6"></line>
					<line x1="3" y1="18" x2="21" y2="18"></line>
				</svg>
			</button>
		{/if}
	</div>

	<MusicPlayer />

	<!-- Toast notifications -->
	<ToastManager.default />
</div>

<style>
	.write-tab {
		display: flex;
		flex-direction: column;
		height: 100%;
		width: 100%;
		background-color: #1a1a1a;
		color: #e0e0e0;
	}

	.write-tab-content {
		display: flex;
		flex: 1;
		width: 100%; /* Ensure it takes full width */
		overflow: hidden;
	}

	.sheet-panel-container {
		flex: 1; /* Take up all available space */
		width: 100%; /* Ensure it takes full width */
		overflow: hidden;
	}

	.browser-panel-container {
		overflow: hidden;
		flex-shrink: 0; /* Prevent browser panel from shrinking */
		position: relative; /* For positioning the resize handle */
	}

	.resize-handle-wrapper {
		position: absolute;
		top: 0;
		left: 0;
		height: 100%;
		z-index: 20;
	}

	.open-browser-button {
		position: absolute;
		top: 1rem;
		right: 1rem;
		background-color: #2a2a2a;
		border: none;
		color: #e0e0e0;
		cursor: pointer;
		padding: 0.5rem;
		border-radius: 4px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
		z-index: 10;
		transition: background-color 0.2s;
	}

	.open-browser-button:hover {
		background-color: #3a3a3a;
	}

	/* Responsive adjustments */
	@media (max-width: 640px) {
		.browser-panel-container {
			position: absolute;
			top: 0;
			right: 0;
			bottom: 0;
			width: 80%;
			max-width: 300px;
			z-index: 100;
			box-shadow: -2px 0 10px rgba(0, 0, 0, 0.5);
		}
	}
</style>
