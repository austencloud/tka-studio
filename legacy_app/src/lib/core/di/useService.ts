import { onMount, getContext } from 'svelte';
import { writable, type Writable } from 'svelte/store';
import { getService } from './serviceContext';
import type { ServiceToken } from './ServiceTokens';

export function useService<T>(token: string | ServiceToken): {
	service: Writable<T | null>;
	isReady: Writable<boolean>;
} {
	const service = writable<T | null>(null);
	const isReady = writable(false);

	onMount(() => {
		try {
			const instance = getService<T>(token);
			service.set(instance);
			isReady.set(true);
		} catch (error) {
			console.error(`Error getting service ${token}:`, error);
			isReady.set(false);
		}

		return () => {
			service.set(null);
			isReady.set(false);
		};
	});

	return {
		service,
		isReady
	};
}
