import { ServiceContainer } from './ServiceContainer';
import { browser } from '$app/environment';

let container: ServiceContainer;

export function getContainer(): ServiceContainer {
	if (!container) {
		container = new ServiceContainer();
	}
	return container;
}

export function createContainer(): ServiceContainer {
	return new ServiceContainer();
}
