import { onMount, onDestroy } from 'svelte';

/**
 * Interface for the tools panel manager parameters
 */
export interface ToolsPanelManagerParams {
	setToolsPanelOpen: (isOpen: boolean | ((current: boolean) => boolean)) => void;
	parentPanelOpen?: boolean;
}

/**
 * Manages the tools panel state and event handling
 * @param params Tools panel manager parameters
 * @returns Object with tools panel management functions and event handlers
 */
export function useToolsPanelManager(params: ToolsPanelManagerParams) {
	const { setToolsPanelOpen, parentPanelOpen } = params;

	/**
	 * Toggles the tools panel open/closed state
	 */
	function toggleToolsPanel() {
		// Create and dispatch a custom event
		const event = new CustomEvent('toggleToolsPanel', {
			bubbles: true,
			composed: true
		});
		document.dispatchEvent(event);

		// If parent's panel is not open, also toggle our local panel
		if (!parentPanelOpen) {
			// Get the current state and toggle it
			// We need to use a callback to get the current state
			setToolsPanelOpen((current) => !current);
		}
	}

	/**
	 * Sets up event listeners for tools panel actions
	 * @returns Cleanup function to remove event listeners
	 */
	function setupEventListeners() {
		let closeToolsPanelListener: (event: Event) => void;

		// Set up event listeners on mount
		onMount(() => {
			// Listen for close tools panel events
			closeToolsPanelListener = () => {
				setToolsPanelOpen(false);
			};
			document.addEventListener('close-tools-panel', closeToolsPanelListener);
		});

		// Clean up event listeners on destroy
		onDestroy(() => {
			if (closeToolsPanelListener) {
				document.removeEventListener('close-tools-panel', closeToolsPanelListener);
			}
		});
	}

	return {
		toggleToolsPanel,
		setupEventListeners
	};
}
