/**
 * 🔗 TKA RESOLVER CHAIN
 *
 * Sophisticated service resolution system with multiple resolution strategies,
 * fallback mechanisms, and advanced dependency injection patterns.
 */

import { ServiceInterface, ServiceScope, ResolutionContext } from './types.js';
import { ServiceRegistry } from './ServiceRegistry.js';

/**
 * Base interface for service resolvers
 */
export interface IServiceResolver {
    readonly name: string;
    readonly priority: number;
    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean;
    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null;
}

/**
 * Singleton service resolver
 */
export class SingletonResolver implements IServiceResolver {
    readonly name = 'SingletonResolver';
    readonly priority = 100;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.scope === ServiceScope.Singleton;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        // Check if instance already exists
        let instance = registry.getSingletonInstance(serviceInterface);
        if (instance) {
            return instance;
        }

        // Create new instance
        const descriptor = registry.getDescriptor(serviceInterface);
        if (!descriptor) return null;

        if (descriptor.implementation) {
            instance = this._createInstance(descriptor.implementation, container, context);
        } else if (descriptor.factory) {
            instance = descriptor.factory();
        } else if (descriptor.instance) {
            instance = descriptor.instance;
        }

        if (instance) {
            registry.setSingletonInstance(serviceInterface, instance);
        }

        return instance;
    }

    private _createInstance<T>(
        implementation: new (...args: any[]) => T,
        container: any,
        context: ResolutionContext
    ): T {
        // Advanced constructor injection would go here
        // For now, simple instantiation
        return new implementation();
    }
}

/**
 * Transient service resolver
 */
export class TransientResolver implements IServiceResolver {
    readonly name = 'TransientResolver';
    readonly priority = 90;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.scope === ServiceScope.Transient;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        const descriptor = registry.getDescriptor(serviceInterface);
        if (!descriptor) return null;

        if (descriptor.implementation) {
            return this._createInstance(descriptor.implementation, container, context);
        } else if (descriptor.factory) {
            return descriptor.factory();
        }

        return null;
    }

    private _createInstance<T>(
        implementation: new (...args: any[]) => T,
        container: any,
        context: ResolutionContext
    ): T {
        return new implementation();
    }
}

/**
 * Scoped service resolver
 */
export class ScopedResolver implements IServiceResolver {
    readonly name = 'ScopedResolver';
    readonly priority = 95;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.scope === ServiceScope.Scoped ||
               descriptor?.scope === ServiceScope.Request ||
               descriptor?.scope === ServiceScope.Session ||
               descriptor?.scope === ServiceScope.Component;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        const scopeId = this._determineScopeId(context);
        if (!scopeId) return null;

        // Check if instance already exists in scope
        let instance = registry.getScopedInstance(serviceInterface, scopeId);
        if (instance) {
            return instance;
        }

        // Create new instance for scope
        const descriptor = registry.getDescriptor(serviceInterface);
        if (!descriptor) return null;

        if (descriptor.implementation) {
            instance = this._createInstance(descriptor.implementation, container, context);
        } else if (descriptor.factory) {
            instance = descriptor.factory();
        }

        if (instance) {
            registry.setScopedInstance(serviceInterface, scopeId, instance);
        }

        return instance;
    }

    private _determineScopeId(context: ResolutionContext): string | null {
        // Determine scope ID based on context
        if (context.scopeId) return context.scopeId;
        if (context.requestId) return `request_${context.requestId}`;
        if (context.sessionId) return `session_${context.sessionId}`;
        if (context.componentId) return `component_${context.componentId}`;
        return null;
    }

    private _createInstance<T>(
        implementation: new (...args: any[]) => T,
        container: any,
        context: ResolutionContext
    ): T {
        return new implementation();
    }
}

/**
 * Factory service resolver
 */
export class FactoryResolver implements IServiceResolver {
    readonly name = 'FactoryResolver';
    readonly priority = 85;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.scope === ServiceScope.Factory && !!descriptor.factory;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        const descriptor = registry.getDescriptor(serviceInterface);
        if (!descriptor?.factory) return null;

        return descriptor.factory();
    }
}

/**
 * Lazy service resolver
 */
export class LazyResolver implements IServiceResolver {
    readonly name = 'LazyResolver';
    readonly priority = 80;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.scope === ServiceScope.Lazy;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        // Lazy resolution is handled by LazyProxy
        // This resolver shouldn't be called directly for lazy services
        return null;
    }
}

/**
 * Instance service resolver
 */
export class InstanceResolver implements IServiceResolver {
    readonly name = 'InstanceResolver';
    readonly priority = 110;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.scope === ServiceScope.Instance && !!descriptor.instance;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        const descriptor = registry.getDescriptor(serviceInterface);
        return descriptor?.instance || null;
    }
}

/**
 * Fallback resolver for unregistered services
 */
export class FallbackResolver implements IServiceResolver {
    readonly name = 'FallbackResolver';
    readonly priority = 0;

    canResolve<T>(serviceInterface: ServiceInterface<T>, registry: ServiceRegistry): boolean {
        // Can always attempt to resolve, but will likely fail
        return true;
    }

    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        // Attempt to create instance directly from interface type
        try {
            if (serviceInterface.type) {
                return new serviceInterface.type();
            }
        } catch {
            // Fallback failed
        }

        return null;
    }
}

/**
 * Main resolver chain that orchestrates service resolution
 */
export class ResolverChain {
    private readonly _resolvers: IServiceResolver[] = [];

    constructor() {
        // Register resolvers in priority order (highest first)
        this._resolvers.push(
            new InstanceResolver(),
            new SingletonResolver(),
            new ScopedResolver(),
            new TransientResolver(),
            new FactoryResolver(),
            new LazyResolver(),
            new FallbackResolver()
        );

        // Sort by priority (highest first)
        this._resolvers.sort((a, b) => b.priority - a.priority);
    }

    /**
     * Resolve a service using the resolver chain
     */
    resolve<T>(
        serviceInterface: ServiceInterface<T>,
        registry: ServiceRegistry,
        container: any,
        context: ResolutionContext
    ): T | null {
        for (const resolver of this._resolvers) {
            if (resolver.canResolve(serviceInterface, registry)) {
                try {
                    const instance = resolver.resolve(serviceInterface, registry, container, context);
                    if (instance !== null && instance !== undefined) {
                        // Log successful resolution
                        this._logResolution(serviceInterface.name, resolver.name, true);
                        return instance;
                    }
                } catch (error) {
                    // Log failed resolution attempt
                    this._logResolution(serviceInterface.name, resolver.name, false, error);
                    // Continue to next resolver
                }
            }
        }

        // No resolver could handle this service
        this._logResolution(serviceInterface.name, 'None', false, new Error('No suitable resolver found'));
        return null;
    }

    /**
     * Add a custom resolver to the chain
     */
    addResolver(resolver: IServiceResolver): void {
        this._resolvers.push(resolver);
        this._resolvers.sort((a, b) => b.priority - a.priority);
    }

    /**
     * Remove a resolver from the chain
     */
    removeResolver(resolverName: string): boolean {
        const index = this._resolvers.findIndex(r => r.name === resolverName);
        if (index >= 0) {
            this._resolvers.splice(index, 1);
            return true;
        }
        return false;
    }

    /**
     * Get all registered resolvers
     */
    getResolvers(): IServiceResolver[] {
        return [...this._resolvers];
    }

    /**
     * Get resolver by name
     */
    getResolver(name: string): IServiceResolver | null {
        return this._resolvers.find(r => r.name === name) || null;
    }

    private _logResolution(serviceName: string, resolverName: string, success: boolean, error?: any): void {
        // In a real implementation, this would use a proper logging system
        if (typeof console !== 'undefined') {
            const message = `[ResolverChain] ${serviceName} -> ${resolverName}: ${success ? 'SUCCESS' : 'FAILED'}`;
            if (success) {
                console.debug(message);
            } else {
                console.warn(message, error);
            }
        }
    }
}
