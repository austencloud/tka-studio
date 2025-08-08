<script lang="ts">
	// Props
	let {
		sidebarWidth = $bindable(),
		isResizing = $bindable(),
		onResizeStart
	}: {
		sidebarWidth: number;
		isResizing: boolean;
		onResizeStart?: (_e: MouseEvent) => void;
	} = $props();

	// Resize state
	let resizeStartX = $state(0);
	let resizeStartWidth = $state(0);

	// Direct resize function for immediate response - no processing during drag
	function updateSidebarWidth(newWidth: number): void {
		sidebarWidth = newWidth;
	}

	// Resizable sidebar functions
	function handleResizeStart(e: MouseEvent): void {
		isResizing = true;
		resizeStartX = e.clientX;
		resizeStartWidth = sidebarWidth;

		// Add global event listeners FIRST for immediate response
		document.addEventListener('mousemove', handleResizeMove);
		document.addEventListener('mouseup', handleResizeEnd);
		document.body.style.cursor = 'col-resize';
		document.body.style.userSelect = 'none';

		// Call parent handler if provided
		onResizeStart?.(e);
	}

	function handleResizeMove(e: MouseEvent): void {
		if (!isResizing) return;

		const deltaX = e.clientX - resizeStartX;
		const newWidth = resizeStartWidth + deltaX;

		// Constrain width between 300px and 80% of viewport width
		const maxWidth = typeof window !== 'undefined' ? window.innerWidth * 0.8 : 800;
		const constrainedWidth = Math.max(300, Math.min(maxWidth, newWidth));

		// Update immediately for responsive feel
		updateSidebarWidth(constrainedWidth);
	}

	function handleResizeEnd(): void {
		isResizing = false;

		// Remove global event listeners
		document.removeEventListener('mousemove', handleResizeMove);
		document.removeEventListener('mouseup', handleResizeEnd);
		document.body.style.cursor = '';
		document.body.style.userSelect = '';

		// Trigger a single layout update after resize is complete
		// Use setTimeout to ensure it happens after the current event loop
		setTimeout(() => {
			// Force a single reflow to update any layout-dependent elements
			if (typeof window !== 'undefined') {
				window.dispatchEvent(new Event('resize'));
			}
		}, 0);
	}

	// Preset sizing functions
	function setSidebarToPercentage(percentage: number): void {
		if (typeof window !== 'undefined') {
			const newWidth = window.innerWidth * (percentage / 100);
			const maxWidth = window.innerWidth * 0.8;
			sidebarWidth = Math.max(300, Math.min(maxWidth, newWidth));
		}
	}

	// Expose public methods
	export function startResize(e: MouseEvent): void {
		handleResizeStart(e);
	}

	export function getResizeState() {
		return {
			sidebarWidth,
			isResizing
		};
	}

	export function setSidebar50(): void {
		setSidebarToPercentage(50);
	}

	export function setSidebar75(): void {
		setSidebarToPercentage(75);
	}

	export function setSidebar25(): void {
		setSidebarToPercentage(25);
	}
</script>

<!-- This component manages sidebar resize state but doesn't render anything -->
