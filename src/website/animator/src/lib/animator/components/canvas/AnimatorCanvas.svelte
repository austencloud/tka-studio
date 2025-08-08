<script lang="ts">
	import type { PropState } from '../../types/core.js';
	import { svgStringToImage } from '../../svgStringToImage.js';
	import { ANIMATION_CONSTANTS } from '../../constants/animation.js';
	import { SVGGenerator } from '../../utils/canvas/SVGGenerator.js';
	import { CanvasRenderer } from '../../utils/canvas/CanvasRenderer.js';
	import GridManager from './GridManager.svelte';

	// Modern Svelte 5 props
	let {
		blueProp,
		redProp,
		width = 500,
		height = 500,
		gridVisible = true
	}: {
		blueProp: PropState;
		redProp: PropState;
		width?: number;
		height?: number;
		gridVisible?: boolean;
	} = $props();

	let canvasElement: HTMLCanvasElement;
	let ctx: CanvasRenderingContext2D | null = null;
	let gridImage: HTMLImageElement | null = null;
	let blueStaffImage: HTMLImageElement | null = null;
	let redStaffImage: HTMLImageElement | null = null;
	let imagesLoaded = $state(false);
	let rafId: number | null = null;
	let needsRender = $state(true);
	let gridManager: GridManager;

	// Handle grid image load from GridManager
	function handleGridImageLoad(image: HTMLImageElement): void {
		gridImage = image;
		needsRender = true;
		startRenderLoop();
	}

	// Track prop changes to trigger re-renders
	$effect(() => {
		blueProp;
		redProp;
		gridVisible;
		needsRender = true;
		startRenderLoop();
	});

	// Initial load of staff images and canvas setup
	$effect(() => {
		const loadStaffImages = async () => {
			try {
				[blueStaffImage, redStaffImage] = await Promise.all([
					svgStringToImage(
						SVGGenerator.generateBlueStaffSvg(),
						ANIMATION_CONSTANTS.STAFF_VIEWBOX_WIDTH,
						ANIMATION_CONSTANTS.STAFF_VIEWBOX_HEIGHT
					),
					svgStringToImage(
						SVGGenerator.generateRedStaffSvg(),
						ANIMATION_CONSTANTS.STAFF_VIEWBOX_WIDTH,
						ANIMATION_CONSTANTS.STAFF_VIEWBOX_HEIGHT
					)
				]);

				ctx = canvasElement.getContext('2d');
				imagesLoaded = true;
				needsRender = true;
				startRenderLoop();
			} catch (err) {
				console.error('Failed to load SVG images:', err);
			}
		};

		if (canvasElement) {
			loadStaffImages();
		}

		return () => {
			if (rafId !== null) {
				cancelAnimationFrame(rafId);
			}
		};
	});

	function renderLoop(): void {
		if (!ctx || !imagesLoaded) return;

		if (needsRender) {
			render();
			needsRender = false;
			rafId = requestAnimationFrame(renderLoop);
		} else {
			rafId = null;
		}
	}

	function startRenderLoop(): void {
		if (rafId === null && ctx && imagesLoaded) {
			rafId = requestAnimationFrame(renderLoop);
		}
	}

	function render(): void {
		if (!ctx || !imagesLoaded) return;

		CanvasRenderer.renderScene(
			ctx,
			width,
			height,
			gridVisible,
			gridImage,
			blueStaffImage,
			redStaffImage,
			blueProp,
			redProp
		);
	}
</script>

<div class="canvas-wrapper">
	<canvas bind:this={canvasElement} {width} {height} style:width="{width}px" style:height="{height}px"
	></canvas>

	<GridManager bind:this={gridManager} {width} {height} onGridImageLoad={handleGridImageLoad} />
</div>

<style>
	.canvas-wrapper {
		position: relative;
		display: inline-block;
	}

	canvas {
		border: 1px solid var(--color-border);
		border-radius: 4px;
		background: var(--color-surface);
		transition: all 0.3s ease;
		display: block;
	}
</style>
