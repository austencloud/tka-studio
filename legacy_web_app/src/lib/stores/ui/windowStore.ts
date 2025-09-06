import { writable, readable } from 'svelte/store';

function createWindowHeight() {
	if (typeof window === 'undefined') {
		// SSR-safe fallback
		return readable('100vh');
	}

	const { subscribe, set } = writable(`${window.innerHeight}px`);

	function update() {
		set(`${window.innerHeight}px`);
	}

	window.addEventListener('resize', update);
	update();

	return {
		subscribe,
		// Optional: call this in onDestroy if you want to clean up
		_destroy: () => window.removeEventListener('resize', update)
	};
}

export const windowHeight = createWindowHeight();
