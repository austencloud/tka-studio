export type ServiceScope = 'singleton' | 'transient' | 'scoped';

export class ServiceContainer {
	private services: Map<string, any> = new Map();
	private factories: Map<string, () => any> = new Map();
	private scopes: Map<string, ServiceScope> = new Map();
	private scopedInstances: Map<symbol, Map<string, any>> = new Map();
	private currentScope?: symbol;

	register<T>(token: string, instance: T, scope: ServiceScope = 'singleton'): void {
		this.services.set(token, instance);
		this.scopes.set(token, scope);
	}

	registerFactory<T>(token: string, factory: () => T, scope: ServiceScope = 'singleton'): void {
		this.factories.set(token, factory);
		this.scopes.set(token, scope);
	}

	get<T>(token: string): T {
		// Check for scoped instance first
		if (this.currentScope && this.scopes.get(token) === 'scoped') {
			const scopeMap = this.scopedInstances.get(this.currentScope);
			if (scopeMap?.has(token)) {
				return scopeMap.get(token) as T;
			}
		}

		// Check for singleton service
		if (this.services.has(token) && this.scopes.get(token) !== 'transient') {
			return this.services.get(token) as T;
		}

		// Create from factory if available
		if (this.factories.has(token)) {
			const factory = this.factories.get(token);
			if (!factory) {
				throw new Error(`Factory for service '${token}' exists but is undefined`);
			}

			const instance = factory();

			// Store instance according to its scope
			const scope = this.scopes.get(token) || 'singleton';

			if (scope === 'singleton') {
				this.services.set(token, instance);
			} else if (scope === 'scoped' && this.currentScope) {
				let scopeMap = this.scopedInstances.get(this.currentScope);
				if (!scopeMap) {
					scopeMap = new Map();
					this.scopedInstances.set(this.currentScope, scopeMap);
				}
				scopeMap.set(token, instance);
			}

			return instance as T;
		}

		throw new Error(`Service not found: ${token}`);
	}

	has(token: string): boolean {
		return this.services.has(token) || this.factories.has(token);
	}

	beginScope(): symbol {
		const scope = Symbol('service-scope');
		this.scopedInstances.set(scope, new Map());
		this.currentScope = scope;
		return scope;
	}

	endScope(scope: symbol): void {
		this.scopedInstances.delete(scope);
		if (this.currentScope === scope) {
			this.currentScope = undefined;
		}
	}

	setCurrentScope(scope: symbol): void {
		if (!this.scopedInstances.has(scope)) {
			throw new Error('Invalid scope provided');
		}
		this.currentScope = scope;
	}

	clear(): void {
		this.services.clear();
		this.factories.clear();
		this.scopes.clear();
		this.scopedInstances.clear();
		this.currentScope = undefined;
	}
}
