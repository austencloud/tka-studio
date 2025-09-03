<!-- src/lib/components/SequenceWorkbench/BeatFrame/managers/BeatFrameElementManager.svelte -->
<script lang="ts" module>
	// Export the interface for the component
	export interface BeatFrameElementManager {
		getElement: () => HTMLElement | null;
	}
</script>

<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';
	import { setContext } from 'svelte';
	import { BEAT_FRAME_CONTEXT_KEY } from '../../context/ElementContext';

	// Props
	const {
		containerRef,
		elementReceiver = $bindable<(element: HTMLElement | null) => void>(() => {})
	} = $props<{
		containerRef: HTMLElement | null;
		elementReceiver?: (element: HTMLElement | null) => void;
	}>();

	// Create a reactive state for the element reference
	let beatFrameElementState = $state<HTMLElement | null>(null);

	// This effect ensures the element reference is passed to the parent component
	// whenever the container element or the elementReceiver function changes
	$effect(() => {
		if (containerRef) {
			// Update our reactive state
			beatFrameElementState = containerRef;

			// Set the context for other components to access
			setContext(BEAT_FRAME_CONTEXT_KEY, {
				getElement: () => beatFrameElementState
			});

			// Store the element in global variables for fallback mechanisms
			if (browser) {
				// Store in both variables for maximum compatibility
				(window as any).__beatFrameElementRef = containerRef;
				(window as any).__pendingBeatFrameElement = containerRef;
			}

			// Make sure elementReceiver is a function before calling it
			if (typeof elementReceiver === 'function') {
				try {
					// Call the receiver function
					elementReceiver(containerRef);
				} catch (error) {
					console.error('BeatFrame: Error calling elementReceiver:', error);
				}
			} else {
				console.error('BeatFrame: elementReceiver is not a function:', elementReceiver);
			}

			// Dispatch a custom event as a reliable fallback mechanism
			if (browser) {
				const event = new CustomEvent('beatframe-element-available', {
					bubbles: true,
					detail: { element: containerRef }
				});
				document.dispatchEvent(event);
			}
		} else {
			beatFrameElementState = null;
		}
	});

	// Add a MutationObserver to ensure the element is passed even after DOM changes
	onMount(() => {
		if (browser) {
			// Set up a MutationObserver to detect when the element is added to the DOM
			const observer = new MutationObserver((_mutations) => {
				if (containerRef) {
					// Update our reactive state
					beatFrameElementState = containerRef;

					// Store in global variables for maximum compatibility
					(window as any).__beatFrameElementRef = containerRef;
					(window as any).__pendingBeatFrameElement = containerRef;

					// Make sure elementReceiver is a function before calling it
					if (typeof elementReceiver === 'function') {
						try {
							// Call the receiver function
							elementReceiver(containerRef);
						} catch (error) {
							console.error('BeatFrame: Error calling elementReceiver after DOM mutation:', error);
						}
					}

					// Dispatch a custom event as a reliable fallback mechanism
					const event = new CustomEvent('beatframe-element-available', {
						bubbles: true,
						detail: { element: containerRef }
					});
					document.dispatchEvent(event);
				}
			});

			// Start observing the document body for DOM changes
			observer.observe(document.body, {
				childList: true,
				subtree: true
			});

			return () => {
				// Clean up the observer when the component is destroyed
				observer.disconnect();
			};
		}
	});

	// Export methods for parent components
	export function getElement() {
		return beatFrameElementState;
	}
</script>

<!-- This is an invisible component that just manages element references -->
<div style="display: none;" aria-hidden="true">
	<!-- Status for debugging -->
	{#if beatFrameElementState}
		<!-- Element manager initialized -->
	{/if}
</div>
