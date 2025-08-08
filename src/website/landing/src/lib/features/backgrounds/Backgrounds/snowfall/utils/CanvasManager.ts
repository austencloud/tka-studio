import { dimensions } from '../snowfallState.svelte';

export const createCanvasManager = () => {
	let canvas: HTMLCanvasElement | null = null;
	let resizeTimeout: number | null = null;
	let resizeCallback: (() => void) | null = null;

	const initialize = (canvasElement: HTMLCanvasElement, onResize?: () => void): void => {
		canvas = canvasElement;

		if (onResize) {
			resizeCallback = onResize;
		}

		if (typeof window === 'undefined') return;

		const initialWidth = window.innerWidth;
		const initialHeight = window.innerHeight;

		dimensions.set({
			width: initialWidth,
			height: initialHeight
		});

		canvas.width = initialWidth;
		canvas.height = initialHeight;

		window.addEventListener('resize', handleResize);

		document.addEventListener('visibilitychange', handleVisibilityChange);
	};

	const handleResize = (): void => {
		if (!canvas) return;

		if (typeof window === 'undefined') return;

		if (resizeTimeout) {
			cancelAnimationFrame(resizeTimeout);
		}

		resizeTimeout = requestAnimationFrame(() => {
			const newWidth = window.innerWidth;
			const newHeight = window.innerHeight;

			canvas!.width = newWidth;
			canvas!.height = newHeight;

			dimensions.set({ width: newWidth, height: newHeight });

			if (resizeCallback) {
				resizeCallback();
			}
		});
	};

	const handleVisibilityChange = (): void => {};

	const cleanup = (): void => {
		if (typeof window === 'undefined') return;

		window.removeEventListener('resize', handleResize);
		document.removeEventListener('visibilitychange', handleVisibilityChange);

		if (resizeTimeout) {
			cancelAnimationFrame(resizeTimeout);
		}

		canvas = null;
		resizeCallback = null;
	};

	return {
		initialize,
		handleResize,
		cleanup
	};
};
