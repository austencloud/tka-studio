<script lang="ts">
	import { svgStringToImage } from '../../svgStringToImage.js';
	import { SVGGenerator } from '../../utils/canvas/SVGGenerator.js';

	// Props
	let {
		width = 500,
		height = 500,
		onGridImageLoad
	}: {
		width?: number;
		height?: number;
		onGridImageLoad?: (_image: HTMLImageElement) => void;
	} = $props();

	// Layer2 visibility state with localStorage persistence
	let layer2Visible = $state(false);

	// Dark mode detection
	let isDarkMode = $state(false);

	// Initialize from localStorage and detect dark mode
	$effect(() => {
		if (typeof window !== 'undefined') {
			const saved = localStorage.getItem('grid-layer2-visible');
			layer2Visible = saved === 'true';
			isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
		}
	});

	// Save layer2 visibility to localStorage
	$effect(() => {
		if (typeof window !== 'undefined') {
			localStorage.setItem('grid-layer2-visible', layer2Visible.toString());
		}
	});

	// Watch for theme changes
	$effect(() => {
		if (typeof window !== 'undefined') {
			const observer = new MutationObserver(() => {
				isDarkMode = document.documentElement.getAttribute('data-theme') === 'dark';
			});

			observer.observe(document.documentElement, {
				attributes: true,
				attributeFilter: ['data-theme']
			});

			return () => observer.disconnect();
		}
	});

	// Grid regeneration when layer2 or theme changes
	$effect(() => {
		layer2Visible;
		isDarkMode;
		loadGridImage();
	});

	async function loadGridImage() {
		try {
			const currentGridSvg = SVGGenerator.generateGridSvg(layer2Visible, isDarkMode);
			const gridImage = await svgStringToImage(currentGridSvg, width, height);
			onGridImageLoad?.(gridImage);
		} catch (err) {
			console.error('Failed to load grid image:', err);
		}
	}

	// Expose public methods
	export function getLayer2Visible(): boolean {
		return layer2Visible;
	}

	export function setLayer2Visible(visible: boolean): void {
		layer2Visible = visible;
	}

	export function regenerateGrid(): void {
		loadGridImage();
	}
</script>

<div class="grid-controls">
	<label class="layer2-toggle">
		<input type="checkbox" bind:checked={layer2Visible} title="Show/hide layer2 grid points" />
		<span>Show Layer2 Points</span>
	</label>
</div>

<style>
	.grid-controls {
		position: absolute;
		top: 8px;
		right: 8px;
		background: var(--color-surface);
		border: 1px solid var(--color-border);
		border-radius: 6px;
		padding: 0.5rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
		transition: all 0.3s ease;
	}

	.layer2-toggle {
		display: flex;
		align-items: center;
		cursor: pointer;
		font-size: 0.85rem;
		color: var(--color-text-primary);
		margin: 0;
		user-select: none;
	}

	.layer2-toggle input[type='checkbox'] {
		margin-right: 0.5rem;
		cursor: pointer;
		accent-color: var(--color-primary);
	}

	.layer2-toggle span {
		font-weight: 500;
	}

	.layer2-toggle:hover {
		color: var(--color-primary);
	}

	/* Dark mode adjustments */
	:global([data-theme='dark']) .grid-controls {
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
	}
</style>
