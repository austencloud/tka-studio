<!--
	Glass Scrollable Container

	A beautiful glassmorphism scrollable container that provides consistent,
	elegant scrollbars across all components. Properly implemented for Svelte 5.
-->
<script lang="ts">
	export type ScrollbarVariant = 
		| 'primary'
		| 'secondary' 
		| 'minimal'
		| 'hover'
		| 'gradient';

	export type ScrollDirection = 'vertical' | 'horizontal' | 'both' | 'auto';

	// Props with proper Svelte 5 syntax
	interface Props {
		variant?: ScrollbarVariant;
		height?: string;
		width?: string;
		maxHeight?: string;
		maxWidth?: string;
		scrollDirection?: ScrollDirection;
		className?: string;
		style?: string;
		onScroll?: (event: Event) => void;
		onScrollEnd?: () => void;
		children?: import('svelte').Snippet;
	}

	let {
		variant = 'primary',
		height,
		width,
		maxHeight,
		maxWidth,
		scrollDirection = 'vertical',
		className = '',
		style = '',
		onScroll,
		onScrollEnd,
		children
	}: Props = $props();

	// Generate CSS classes
	const scrollbarClass = `glass-scrollbar-${variant}`;
	const overflowClass = getOverflowClass(scrollDirection);
	const combinedClasses = `glass-scroll-container ${scrollbarClass} ${overflowClass} ${className}`.trim();

	// Generate inline styles
	const inlineStyles = [
		height && `height: ${height}`,
		width && `width: ${width}`,
		maxHeight && `max-height: ${maxHeight}`,
		maxWidth && `max-width: ${maxWidth}`,
		style
	].filter(Boolean).join('; ');

	// Scroll direction utility
	function getOverflowClass(direction: ScrollDirection): string {
		switch (direction) {
			case 'vertical':
				return 'overflow-y-auto overflow-x-hidden';
			case 'horizontal':
				return 'overflow-x-auto overflow-y-hidden';
			case 'both':
				return 'overflow-auto';
			case 'auto':
				return 'overflow-auto';
			default:
				return 'overflow-y-auto overflow-x-hidden';
		}
	}

	// Handle scroll events
	let scrollTimeout: number;
	function handleScroll(event: Event) {
		onScroll?.(event);
		
		// Handle scroll end detection
		if (onScrollEnd) {
			clearTimeout(scrollTimeout);
			scrollTimeout = setTimeout(() => {
				onScrollEnd();
			}, 150);
		}
	}
</script>

<div 
	class={combinedClasses}
	style={inlineStyles}
	onscroll={handleScroll}
	role="region"
	tabindex="0"
>
	{#if children}
		{@render children()}
	{/if}
</div>

<style>
	.glass-scroll-container {
		/* Base container styling */
		position: relative;
		display: block;
		background: transparent;
		border-radius: var(--desktop-border-radius-sm, 8px);
		
		/* Smooth scrolling behavior */
		scroll-behavior: smooth;
		
		/* Focus styling for accessibility */
		outline: none;
		transition: all var(--desktop-transition-normal, 0.2s ease);
	}

	.glass-scroll-container:focus-visible {
		box-shadow: 
			0 0 0 2px var(--desktop-primary-blue-border, rgba(70, 130, 180, 1.0)),
			0 0 8px rgba(70, 130, 180, 0.3);
	}

	/* Enhanced container with backdrop blur for content */
	.glass-scroll-container::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: rgba(255, 255, 255, 0.02);
		border-radius: inherit;
		pointer-events: none;
		z-index: -1;
		backdrop-filter: blur(5px);
		-webkit-backdrop-filter: blur(5px);
	}

	/* Overflow utility classes */
	.overflow-y-auto {
		overflow-y: auto;
	}

	.overflow-x-auto {
		overflow-x: auto;
	}

	.overflow-auto {
		overflow: auto;
	}

	.overflow-y-hidden {
		overflow-y: hidden;
	}

	.overflow-x-hidden {
		overflow-x: hidden;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.glass-scroll-container {
			/* Disable smooth scrolling on mobile for performance */
			scroll-behavior: auto;
		}
	}

	/* High contrast mode support */
	@media (prefers-contrast: high) {
		.glass-scroll-container::before {
			background: rgba(255, 255, 255, 0.05);
			backdrop-filter: none;
		}
	}

	/* Reduced motion support */
	@media (prefers-reduced-motion: reduce) {
		.glass-scroll-container {
			scroll-behavior: auto;
			transition: none;
		}
	}
</style>
