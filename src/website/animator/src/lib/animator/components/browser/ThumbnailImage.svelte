<script lang="ts">
	import type { Snippet } from 'svelte';
	import { thumbnailViewportManager } from '../../utils/performance/viewport.js';

	// Props
	let {
		src,
		alt,
		hasMultipleVersions = false,
		versionCount = 0,
		overlay
	}: {
		src: string;
		alt: string;
		hasMultipleVersions?: boolean;
		versionCount?: number;
		overlay?: Snippet;
	} = $props();

	// State
	let isImageLoaded = $state(false);
	let imageError = $state(false);
	let imageElement: HTMLImageElement | null = $state(null);
	let containerElement: HTMLDivElement | null = $state(null);
	let isVisible = $state(false);
	let shouldProcessResize = $state(true);

	// Cleanup functions
	let viewportCleanup: (() => void) | null = null;

	function handleImageLoad(event: Event): void {
		const img = event.target as HTMLImageElement;
		imageElement = img;
		isImageLoaded = true;
		imageError = false;

		// Dynamically adjust container height based on image aspect ratio
		adjustContainerHeight();
	}

	function adjustContainerHeight(): void {
		if (!imageElement || !containerElement || !shouldProcessResize) return;

		// Skip ALL resize processing during sidebar drag for maximum performance
		if (typeof window !== 'undefined' && document.body.style.cursor === 'col-resize') {
			return;
		}

		// Skip resize if not visible
		if (!isVisible) {
			return;
		}

		// Get responsive padding values
		const computedStyle = window.getComputedStyle(containerElement);
		const paddingLeft = parseFloat(computedStyle.paddingLeft);
		const paddingRight = parseFloat(computedStyle.paddingRight);
		const paddingTop = parseFloat(computedStyle.paddingTop);
		const paddingBottom = parseFloat(computedStyle.paddingBottom);

		// Get the container width (accounting for horizontal padding)
		const containerWidth = containerElement.clientWidth - paddingLeft - paddingRight;

		// Calculate the scaled height based on image aspect ratio
		const imageAspectRatio = imageElement.naturalHeight / imageElement.naturalWidth;
		const scaledHeight = containerWidth * imageAspectRatio;

		// Add vertical padding to the scaled height
		const totalHeight = scaledHeight + paddingTop + paddingBottom;

		// Set responsive minimum height
		const minHeight = window.innerWidth <= 480 ? 100 : window.innerWidth <= 768 ? 120 : 150;
		const finalHeight = Math.max(totalHeight, minHeight);

		// Apply the calculated height
		containerElement.style.height = `${finalHeight}px`;
	}

	function handleImageError(): void {
		isImageLoaded = false;
		imageError = true;
	}

	// Simplified viewport and resize handling - no complex resize manager
	$effect(() => {
		if (!containerElement) return;

		// Register with viewport manager for visibility tracking
		viewportCleanup = thumbnailViewportManager.registerThumbnail(
			containerElement,
			() => {
				isVisible = true;
				shouldProcessResize = true;
				// Process resize immediately when becoming visible
				if (isImageLoaded && imageElement) {
					adjustContainerHeight();
				}
			},
			() => {
				isVisible = false;
				shouldProcessResize = false;
			}
		);

		// Simple resize observer that respects sidebar resize state
		const resizeObserver = new ResizeObserver(() => {
			if (isImageLoaded && imageElement) {
				adjustContainerHeight();
			}
		});

		resizeObserver.observe(containerElement);

		return () => {
			viewportCleanup?.();
			resizeObserver.disconnect();
			viewportCleanup = null;
		};
	});
</script>

<div class="card-image-container" bind:this={containerElement}>
	{#if !imageError}
		<img
			{src}
			{alt}
			class="card-image"
			class:loaded={isImageLoaded}
			onload={handleImageLoad}
			onerror={handleImageError}
		/>
	{/if}

	{#if !isImageLoaded && !imageError}
		<div class="image-placeholder">
			<div class="placeholder-spinner"></div>
		</div>
	{/if}

	{#if imageError}
		<div class="image-error">
			<div class="error-icon">🖼️</div>
			<span>Image not available</span>
		</div>
	{/if}

	{#if hasMultipleVersions}
		<div class="version-badge" title={`${versionCount} versions available`}>
			{versionCount}
		</div>
	{/if}

	{#if overlay}
		{@render overlay()}
	{/if}
</div>

<style>
	.card-image-container {
		position: relative;
		width: 100%;
		background: var(--color-surface);
		overflow: hidden;
		display: flex;
		align-items: center;
		justify-content: center;
		border-radius: 8px 8px 0 0;
		padding: 12px;
		box-sizing: border-box;
		min-height: 150px; /* Minimum height for loading states */
		transition:
			height 0.3s ease,
			background-color 0.3s ease; /* Smooth height transitions */
	}

	.card-image {
		width: calc(100% - 24px); /* Account for container padding */
		height: auto;
		object-fit: contain;
		object-position: center;
		opacity: 0;
		transition: opacity 0.3s ease;
		border-radius: 6px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
		display: block;
	}

	.card-image.loaded {
		opacity: 1;
	}

	.image-placeholder,
	.image-error {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		display: flex;
		flex-direction: column;
		align-items: center;
		justify-content: center;
		background: var(--color-surface);
		color: var(--color-text-secondary);
	}

	.image-placeholder {
		background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
		background-size: 200% 100%;
		animation: shimmer 1.5s infinite;
		color: transparent;
	}

	@keyframes shimmer {
		0% {
			background-position: -200% 0;
		}
		100% {
			background-position: 200% 0;
		}
	}

	.placeholder-spinner {
		width: 24px;
		height: 24px;
		border: 2px solid var(--color-border);
		border-top: 2px solid var(--color-primary);
		border-radius: 50%;
		animation: spin 1s linear infinite;
	}

	@keyframes spin {
		0% {
			transform: rotate(0deg);
		}
		100% {
			transform: rotate(360deg);
		}
	}

	.error-icon {
		font-size: 2rem;
		margin-bottom: 0.5rem;
	}

	.image-error span {
		font-size: 0.9rem;
	}

	.version-badge {
		position: absolute;
		top: 8px;
		right: 8px;
		background: var(--color-primary);
		color: white;
		padding: 4px 8px;
		border-radius: 12px;
		font-size: 0.75rem;
		font-weight: 600;
		min-width: 20px;
		text-align: center;
	}

	/* Responsive adjustments */
	@media (max-width: 768px) {
		.card-image-container {
			padding: 16px;
			min-height: 120px;
		}

		.card-image {
			width: calc(100% - 32px); /* Account for larger padding */
		}
	}

	@media (max-width: 480px) {
		.card-image-container {
			padding: 12px;
			min-height: 100px;
		}

		.card-image {
			width: calc(100% - 24px);
		}
	}
</style>
