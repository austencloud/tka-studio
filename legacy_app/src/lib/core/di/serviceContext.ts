import { getContext, setContext } from 'svelte';
import type { ServiceContainer } from './ServiceContainer';
import type { ServiceToken } from './ServiceTokens';

const CONTAINER_KEY = Symbol('SERVICE_CONTAINER');

export function setServiceContainer(container: ServiceContainer): void {
	setContext(CONTAINER_KEY, container);
}

export function getServiceContainer(): ServiceContainer {
	return getContext(CONTAINER_KEY);
}

export function getService<T>(token: string): T {
	const container = getServiceContainer();
	return container.get<T>(token);
}
