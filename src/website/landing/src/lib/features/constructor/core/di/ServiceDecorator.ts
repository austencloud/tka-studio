import { getContainer } from './ContainerProvider.js';
import type { ServiceScope } from './ServiceContainer.js';

export interface InjectableOptions {
	scope?: ServiceScope;
}

export function Injectable(token: string, options: InjectableOptions = {}) {
	return function <T extends new (...args: any[]) => any>(constructor: T) {
		const container = getContainer();
		container.registerFactory(token, () => new constructor(), options.scope);
		return constructor;
	};
}
