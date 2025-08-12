/**
 * 📋 TKA SERVICE REGISTRY
 *
 * Advanced service registration and metadata management system
 * that maintains comprehensive information about all registered services.
 */

import {
    ServiceInterface,
    ServiceDescriptor,
    ServiceScope,
    ServiceMetadata,
    Constructor,
    ServiceFactory
} from './types.js';

export class ServiceRegistry {
    private readonly _descriptors = new Map<string, ServiceDescriptor>();
    private readonly _singletonInstances = new Map<string, any>();
    private readonly _scopedInstances = new Map<string, Map<string, any>>();
    private readonly _registrationOrder: string[] = [];

    // Advanced indexing for fast lookups
    private readonly _servicesByScope = new Map<ServiceScope, Set<string>>();
    private readonly _servicesByTag = new Map<string, Set<string>>();
    private readonly _dependencyGraph = new Map<string, Set<string>>();

    // ============================================================================
    // CORE REGISTRATION METHODS
    // ============================================================================

    /**
     * Register a singleton service
     */
    registerSingleton<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: Constructor<T>
    ): void {
        this._registerService(serviceInterface, implementation, ServiceScope.Singleton);
    }

    /**
     * Register a transient service
     */
    registerTransient<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: Constructor<T>
    ): void {
        this._registerService(serviceInterface, implementation, ServiceScope.Transient);
    }

    /**
     * Register a scoped service
     */
    registerScoped<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: Constructor<T>,
        scope: ServiceScope
    ): void {
        this._registerService(serviceInterface, implementation, scope);
    }

    /**
     * Register a factory function
     */
    registerFactory<T>(
        serviceInterface: ServiceInterface<T>,
        factory: ServiceFactory<T>,
        scope: ServiceScope = ServiceScope.Singleton
    ): void {
        const descriptor: ServiceDescriptor<T> = {
            serviceInterface,
            factory,
            scope,
            registeredAt: new Date(),
            metadata: serviceInterface.metadata
        };

        this._storeDescriptor(serviceInterface.name, descriptor);
        this._updateIndexes(serviceInterface.name, scope, serviceInterface.metadata);
    }

    /**
     * Register a specific instance
     */
    registerInstance<T>(
        serviceInterface: ServiceInterface<T>,
        instance: T
    ): void {
        const descriptor: ServiceDescriptor<T> = {
            serviceInterface,
            instance,
            scope: ServiceScope.Instance,
            registeredAt: new Date(),
            metadata: serviceInterface.metadata
        };

        this._storeDescriptor(serviceInterface.name, descriptor);
        this._singletonInstances.set(serviceInterface.name, instance);
        this._updateIndexes(serviceInterface.name, ServiceScope.Instance, serviceInterface.metadata);
    }

    /**
     * Register a lazy service
     */
    registerLazy<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: Constructor<T>
    ): void {
        this._registerService(serviceInterface, implementation, ServiceScope.Lazy);
    }

    // ============================================================================
    // INSTANCE MANAGEMENT
    // ============================================================================

    /**
     * Get singleton instance if exists
     */
    getSingletonInstance<T>(serviceInterface: ServiceInterface<T>): T | null {
        return this._singletonInstances.get(serviceInterface.name) || null;
    }

    /**
     * Store singleton instance
     */
    setSingletonInstance<T>(serviceInterface: ServiceInterface<T>, instance: T): void {
        this._singletonInstances.set(serviceInterface.name, instance);
    }

    /**
     * Get scoped instance if exists
     */
    getScopedInstance<T>(serviceInterface: ServiceInterface<T>, scopeId: string): T | null {
        const scopeMap = this._scopedInstances.get(scopeId);
        return scopeMap?.get(serviceInterface.name) || null;
    }

    /**
     * Store scoped instance
     */
    setScopedInstance<T>(serviceInterface: ServiceInterface<T>, scopeId: string, instance: T): void {
        let scopeMap = this._scopedInstances.get(scopeId);
        if (!scopeMap) {
            scopeMap = new Map();
            this._scopedInstances.set(scopeId, scopeMap);
        }
        scopeMap.set(serviceInterface.name, instance);
    }

    /**
     * Clear scoped instances for a specific scope
     */
    clearScopedInstances(scopeId: string): void {
        this._scopedInstances.delete(scopeId);
    }

    // ============================================================================
    // QUERY AND LOOKUP METHODS
    // ============================================================================

    /**
     * Check if a service is registered
     */
    isRegistered<T>(serviceInterface: ServiceInterface<T>): boolean {
        return this._descriptors.has(serviceInterface.name);
    }

    /**
     * Get service descriptor
     */
    getDescriptor<T>(serviceInterface: ServiceInterface<T>): ServiceDescriptor<T> | null {
        return this._descriptors.get(serviceInterface.name) || null;
    }

    /**
     * Get all registered services
     */
    getRegisteredServices(): string[] {
        return Array.from(this._descriptors.keys());
    }

    /**
     * Get services by scope
     */
    getServicesByScope(scope: ServiceScope): string[] {
        return Array.from(this._servicesByScope.get(scope) || []);
    }

    /**
     * Get services by tag
     */
    getServicesByTag(tag: string): string[] {
        return Array.from(this._servicesByTag.get(tag) || []);
    }

    /**
     * Get service dependencies
     */
    getServiceDependencies(serviceName: string): string[] {
        return Array.from(this._dependencyGraph.get(serviceName) || []);
    }

    /**
     * Get registration order
     */
    getRegistrationOrder(): string[] {
        return [...this._registrationOrder];
    }

    // ============================================================================
    // ADVANCED QUERIES
    // ============================================================================

    /**
     * Find services matching criteria
     */
    findServices(criteria: {
        scope?: ServiceScope;
        tag?: string;
        deprecated?: boolean;
        registeredAfter?: Date;
        registeredBefore?: Date;
    }): ServiceDescriptor[] {
        const results: ServiceDescriptor[] = [];

        for (const descriptor of this._descriptors.values()) {
            let matches = true;

            if (criteria.scope && descriptor.scope !== criteria.scope) {
                matches = false;
            }

            if (criteria.tag && !descriptor.metadata?.tags?.includes(criteria.tag)) {
                matches = false;
            }

            if (criteria.deprecated !== undefined && descriptor.metadata?.deprecated !== criteria.deprecated) {
                matches = false;
            }

            if (criteria.registeredAfter && descriptor.registeredAt < criteria.registeredAfter) {
                matches = false;
            }

            if (criteria.registeredBefore && descriptor.registeredAt > criteria.registeredBefore) {
                matches = false;
            }

            if (matches) {
                results.push(descriptor);
            }
        }

        return results;
    }

    /**
     * Get dependency tree for a service
     */
    getDependencyTree(serviceName: string, visited = new Set<string>()): string[] {
        if (visited.has(serviceName)) {
            return []; // Circular dependency detected
        }

        visited.add(serviceName);
        const dependencies = this._dependencyGraph.get(serviceName) || new Set();
        const tree: string[] = [];

        for (const dependency of dependencies) {
            tree.push(dependency);
            tree.push(...this.getDependencyTree(dependency, new Set(visited)));
        }

        return tree;
    }

    /**
     * Detect circular dependencies
     */
    detectCircularDependencies(): string[][] {
        const cycles: string[][] = [];
        const visited = new Set<string>();
        const recursionStack = new Set<string>();

        const detectCycle = (serviceName: string, path: string[]): void => {
            if (recursionStack.has(serviceName)) {
                const cycleStart = path.indexOf(serviceName);
                cycles.push(path.slice(cycleStart).concat(serviceName));
                return;
            }

            if (visited.has(serviceName)) {
                return;
            }

            visited.add(serviceName);
            recursionStack.add(serviceName);

            const dependencies = this._dependencyGraph.get(serviceName) || new Set();
            for (const dependency of dependencies) {
                detectCycle(dependency, [...path, serviceName]);
            }

            recursionStack.delete(serviceName);
        };

        for (const serviceName of this._descriptors.keys()) {
            if (!visited.has(serviceName)) {
                detectCycle(serviceName, []);
            }
        }

        return cycles;
    }

    // ============================================================================
    // MAINTENANCE AND UTILITIES
    // ============================================================================

    /**
     * Clear all registrations
     */
    clear(): void {
        this._descriptors.clear();
        this._singletonInstances.clear();
        this._scopedInstances.clear();
        this._registrationOrder.length = 0;
        this._servicesByScope.clear();
        this._servicesByTag.clear();
        this._dependencyGraph.clear();
    }

    /**
     * Copy all registrations to another registry
     */
    copyTo(targetRegistry: ServiceRegistry): void {
        for (const [name, descriptor] of this._descriptors) {
            targetRegistry._descriptors.set(name, { ...descriptor });
        }

        for (const [name, instance] of this._singletonInstances) {
            targetRegistry._singletonInstances.set(name, instance);
        }

        targetRegistry._registrationOrder.push(...this._registrationOrder);

        // Copy indexes
        for (const [scope, services] of this._servicesByScope) {
            targetRegistry._servicesByScope.set(scope, new Set(services));
        }

        for (const [tag, services] of this._servicesByTag) {
            targetRegistry._servicesByTag.set(tag, new Set(services));
        }

        for (const [service, deps] of this._dependencyGraph) {
            targetRegistry._dependencyGraph.set(service, new Set(deps));
        }
    }

    /**
     * Get registry statistics
     */
    getStatistics() {
        const scopeCounts = new Map<ServiceScope, number>();
        for (const [scope, services] of this._servicesByScope) {
            scopeCounts.set(scope, services.size);
        }

        return {
            totalServices: this._descriptors.size,
            singletonInstances: this._singletonInstances.size,
            scopedInstances: this._scopedInstances.size,
            scopeCounts: Object.fromEntries(scopeCounts),
            registrationOrder: this._registrationOrder.length,
            circularDependencies: this.detectCircularDependencies().length
        };
    }

    // ============================================================================
    // PRIVATE UTILITIES
    // ============================================================================

    private _registerService<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: Constructor<T>,
        scope: ServiceScope
    ): void {
        const descriptor: ServiceDescriptor<T> = {
            serviceInterface,
            implementation,
            scope,
            registeredAt: new Date(),
            metadata: serviceInterface.metadata
        };

        this._storeDescriptor(serviceInterface.name, descriptor);
        this._updateIndexes(serviceInterface.name, scope, serviceInterface.metadata);
        this._analyzeDependencies(serviceInterface.name, implementation);
    }

    private _storeDescriptor(serviceName: string, descriptor: ServiceDescriptor): void {
        this._descriptors.set(serviceName, descriptor);
        this._registrationOrder.push(serviceName);
    }

    private _updateIndexes(serviceName: string, scope: ServiceScope, metadata?: ServiceMetadata): void {
        // Update scope index
        let scopeSet = this._servicesByScope.get(scope);
        if (!scopeSet) {
            scopeSet = new Set();
            this._servicesByScope.set(scope, scopeSet);
        }
        scopeSet.add(serviceName);

        // Update tag indexes
        if (metadata?.tags) {
            for (const tag of metadata.tags) {
                let tagSet = this._servicesByTag.get(tag);
                if (!tagSet) {
                    tagSet = new Set();
                    this._servicesByTag.set(tag, tagSet);
                }
                tagSet.add(serviceName);
            }
        }
    }

    private _analyzeDependencies(serviceName: string, implementation: Constructor<any>): void {
        // Basic dependency analysis - in a real implementation, this would use
        // reflection or metadata to determine constructor dependencies
        const dependencies = new Set<string>();

        // For now, we'll extract dependencies from metadata if available
        const descriptor = this._descriptors.get(serviceName);
        if (descriptor?.metadata?.dependencies) {
            for (const dep of descriptor.metadata.dependencies) {
                dependencies.add(dep);
            }
        }

        this._dependencyGraph.set(serviceName, dependencies);
    }
}
