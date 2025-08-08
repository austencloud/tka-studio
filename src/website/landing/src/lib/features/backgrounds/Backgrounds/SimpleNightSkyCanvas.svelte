<script lang="ts">
	import { onMount, onDestroy } from 'svelte';
	import { NightSkyBackgroundSystem } from './nightSky/NightSkyBackgroundSystem.js';
	import type { Dimensions } from './types/types.js';

	let canvas: HTMLCanvasElement;
	let nightSkySystem: NightSkyBackgroundSystem;
	let animationFrame: number;
	let isInitialized = false;
	let resizeTimeout: ReturnType<typeof setTimeout>;

	onMount(() => {
		if (!canvas) return;

		const init = async () => {
			const ctx = canvas.getContext('2d');
			if (!ctx) return;

			// Set up canvas dimensions with proper viewport handling
			const updateCanvasSize = () => {
				const rect = canvas.getBoundingClientRect();
				const dpr = window.devicePixelRatio || 1;

				// Use viewport dimensions for full coverage
				const width = window.innerWidth;
				const height = window.innerHeight;

				canvas.width = width * dpr;
				canvas.height = height * dpr;
				ctx.scale(dpr, dpr);
				canvas.style.width = `${width}px`;
				canvas.style.height = `${height}px`;

				return { width, height };
			};

			let dimensions = updateCanvasSize();

			// Create and initialize the night sky system
			nightSkySystem = new NightSkyBackgroundSystem();
			await nightSkySystem.initialize(dimensions, 'medium');
			isInitialized = true;

			// Animation loop
			const animate = () => {
				if (!isInitialized || !nightSkySystem || !ctx) return;

				// Clear canvas with proper dimensions
				ctx.clearRect(0, 0, dimensions.width, dimensions.height);

				// Update and draw the night sky
				nightSkySystem.update(dimensions);
				nightSkySystem.draw(ctx, dimensions);

				animationFrame = requestAnimationFrame(animate);
			};

			// Start animation
			animate();

			// Debounced resize handler for better performance
			const handleResize = () => {
				// Clear any existing timeout
				if (resizeTimeout) {
					clearTimeout(resizeTimeout);
				}

				// Debounce resize events to avoid excessive updates
				resizeTimeout = setTimeout(async () => {
					const newDimensions = updateCanvasSize();

					// Check if dimensions actually changed significantly
					const widthChange = Math.abs(newDimensions.width - dimensions.width);
					const heightChange = Math.abs(newDimensions.height - dimensions.height);

					if (widthChange > 10 || heightChange > 10) {
						dimensions = newDimensions;

						// Re-initialize the night sky system with new dimensions
						if (nightSkySystem && isInitialized) {
							nightSkySystem.cleanup();
							await nightSkySystem.initialize(dimensions, 'medium');
						}
					}
				}, 100); // 100ms debounce for faster response
			};

			window.addEventListener('resize', handleResize);

			// Return cleanup function
			return () => {
				window.removeEventListener('resize', handleResize);
				if (resizeTimeout) {
					clearTimeout(resizeTimeout);
				}
			};
		};

		init();
	});

	onDestroy(() => {
		if (animationFrame) {
			cancelAnimationFrame(animationFrame);
		}
		if (resizeTimeout) {
			clearTimeout(resizeTimeout);
		}
		if (nightSkySystem) {
			nightSkySystem.cleanup();
		}
	});
</script>

<canvas
	bind:this={canvas}
	class="night-sky-canvas"
	aria-label="Animated night sky background with stars, constellations, and moon"
></canvas>

<style>
	.night-sky-canvas {
		position: fixed; /* Use fixed positioning for better viewport coverage */
		top: 0;
		left: 0;
		width: 100vw; /* Full viewport width */
		height: 100vh; /* Full viewport height */
		z-index: -1;
		pointer-events: none;
		display: block;
		/* Ensure smooth transitions during resize */
		transition: none; /* Disable transitions to avoid flickering */
	}

	/* Ensure canvas fills viewport on all screen sizes */
	@media (orientation: landscape) {
		.night-sky-canvas {
			width: 100vw;
			height: 100vh;
		}
	}

	@media (orientation: portrait) {
		.night-sky-canvas {
			width: 100vw;
			height: 100vh;
		}
	}
</style>
