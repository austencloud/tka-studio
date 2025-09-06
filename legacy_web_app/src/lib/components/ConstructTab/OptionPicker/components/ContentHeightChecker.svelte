<script lang="ts">
	import { debounce } from '$lib/utils/debounce';

	// Props using Svelte 5 runes
	const { panelElement = null, contentElement = null } = $props<{
		panelElement?: HTMLElement | null;
		contentElement?: HTMLElement | null;
	}>();

	// State using Svelte 5 runes
	let contentIsShort = $state(false);

	// Function to check if content is short enough to be centered
	export function checkContentHeight() {
		if (!panelElement || !contentElement) return;

		// Get the panel height and content height
		const panelHeight = panelElement.clientHeight;
		const contentHeight = contentElement.scrollHeight;

		// Content is short if it's less than the panel height
		const isShort = contentHeight < panelHeight;

		// Update the state
		contentIsShort = isShort;

		// Log for debugging
		if (import.meta.env.DEV) {
			console.debug('Content height check:', {
				panelHeight,
				contentHeight,
				isShort
			});
		}
	}

	// Create a debounced version of the check function
	const debouncedCheckContentHeight = debounce(checkContentHeight, 100);

	// Create a resize observer to detect when the container height changes
	let resizeObserver: ResizeObserver;

	// Set up the resize observer when the component mounts
	$effect(() => {
		if (!panelElement || !contentElement) return;

		// Create a new ResizeObserver
		resizeObserver = new ResizeObserver(() => {
			debouncedCheckContentHeight();
		});

		// Start observing both elements
		resizeObserver.observe(panelElement);
		resizeObserver.observe(contentElement);

		// Initial check
		setTimeout(checkContentHeight, 0);

		// Clean up when the component is destroyed or dependencies change
		return () => {
			if (resizeObserver) {
				resizeObserver.disconnect();
			}
		};
	});

	// Handle window resize events
	function handleWindowResize() {
		debouncedCheckContentHeight();
	}

	// Add window resize listener when the component mounts
	$effect(() => {
		window.addEventListener('resize', handleWindowResize);

		// Clean up when the component is destroyed
		return () => {
			window.removeEventListener('resize', handleWindowResize);
		};
	});

	// Export the contentIsShort state
	export { contentIsShort };
</script>
