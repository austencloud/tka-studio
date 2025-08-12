/**
 * 🚀 TKA ENTERPRISE-GRADE SERVICE CONTAINER
 *
 * Next-generation dependency injection container that matches and exceeds
 * the sophistication of the desktop Python DI system.
 *
 * Features:
 * - Advanced lifecycle management (Singleton, Transient, Scoped, Lazy, Factory)
 * - Circular dependency detection and resolution
 * - Performance monitoring and debugging tools
 * - Type-safe interface-based registration
 * - Validation engine with comprehensive error reporting
 * - Resolution chain with fallback strategies
 * - Enterprise-grade debugging and telemetry
 */

import { ServiceRegistry } from './ServiceRegistry.js';
import { ResolverChain } from './ResolverChain.js';
import { LifecycleManager } from './LifecycleManager.js';
import { ValidationEngine } from './ValidationEngine.js';
import { DebuggingTools } from './DebuggingTools.js';
import { ServiceInterface, ServiceScope, ServiceDescriptor, ResolutionContext } from './types.js';
import { LazyProxy } from './LazyProxy.js';
import { ServiceMetrics } from './ServiceMetrics.js';

export class ServiceContainer {
    private readonly _registry: ServiceRegistry;
    private readonly _resolverChain: ResolverChain;
    private readonly _lifecycleManager: LifecycleManager;
    private readonly _validationEngine: ValidationEngine;
    private readonly _debuggingTools: DebuggingTools;
    private readonly _metrics: ServiceMetrics;

    // Resolution state tracking
    private readonly _resolutionStack: Set<string> = new Set();
    private readonly _resolutionDepth: number = 0;
    private readonly _maxResolutionDepth: number = 50;

    // Container metadata
    private readonly _containerId: string;
    private readonly _createdAt: Date;
    private _isDisposed: boolean = false;

    constructor(containerId?: string) {
        this._containerId = containerId || `container_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        this._createdAt = new Date();

        // Initialize sophisticated modules
        this._registry = new ServiceRegistry();
        this._resolverChain = new ResolverChain();
        this._lifecycleManager = new LifecycleManager();
        this._validationEngine = new ValidationEngine();
        this._debuggingTools = new DebuggingTools(this._containerId);
        this._metrics = new ServiceMetrics();

        this._debuggingTools.logContainerCreation(this._containerId, this._createdAt);
    }

    // ============================================================================
    // CORE REGISTRATION API - Type-Safe Interface-Based
    // ============================================================================

    /**
     * Register a service as singleton (one instance per container)
     */
    registerSingleton<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: new (...args: any[]) => T
    ): void {
        this._ensureNotDisposed();
        this._validationEngine.validateRegistration(serviceInterface, implementation);
        this._registry.registerSingleton(serviceInterface, implementation);
        this._debuggingTools.logRegistration(serviceInterface.name, 'singleton', implementation.name);
    }

    /**
     * Register a service as transient (new instance per resolution)
     */
    registerTransient<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: new (...args: any[]) => T
    ): void {
        this._ensureNotDisposed();
        this._validationEngine.validateRegistration(serviceInterface, implementation);
        this._registry.registerTransient(serviceInterface, implementation);
        this._debuggingTools.logRegistration(serviceInterface.name, 'transient', implementation.name);
    }

    /**
     * Register a service with specific scope
     */
    registerScoped<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: new (...args: any[]) => T,
        scope: ServiceScope
    ): void {
        this._ensureNotDisposed();
        this._validationEngine.validateRegistration(serviceInterface, implementation);
        this._registry.registerScoped(serviceInterface, implementation, scope);
        this._debuggingTools.logRegistration(serviceInterface.name, scope, implementation.name);
    }

    /**
     * Register a factory function for custom instantiation
     */
    registerFactory<T>(
        serviceInterface: ServiceInterface<T>,
        factory: () => T,
        scope: ServiceScope = ServiceScope.Singleton
    ): void {
        this._ensureNotDisposed();
        this._validationEngine.validateFactoryRegistration(serviceInterface, factory);
        this._registry.registerFactory(serviceInterface, factory, scope);
        this._debuggingTools.logFactoryRegistration(serviceInterface.name, scope);
    }

    /**
     * Register a specific instance
     */
    registerInstance<T>(
        serviceInterface: ServiceInterface<T>,
        instance: T
    ): void {
        this._ensureNotDisposed();
        this._validationEngine.validateInstanceRegistration(serviceInterface, instance);
        this._registry.registerInstance(serviceInterface, instance);
        this._debuggingTools.logInstanceRegistration(serviceInterface.name, instance);
    }

    /**
     * Register a lazy service that will be instantiated on first access
     */
    registerLazy<T>(
        serviceInterface: ServiceInterface<T>,
        implementation: new (...args: any[]) => T
    ): void {
        this._ensureNotDisposed();
        this._validationEngine.validateRegistration(serviceInterface, implementation);
        this._registry.registerLazy(serviceInterface, implementation);
        this._debuggingTools.logRegistration(serviceInterface.name, 'lazy', implementation.name);
    }

    // ============================================================================
    // ADVANCED RESOLUTION API - Enterprise-Grade Features
    // ============================================================================

    /**
     * Resolve a service instance with full validation and debugging
     */
    resolve<T>(serviceInterface: ServiceInterface<T>): T {
        this._ensureNotDisposed();

        const startTime = performance.now();
        const context = this._createResolutionContext(serviceInterface);

        try {
            // Check for circular dependencies
            if (this._resolutionStack.has(serviceInterface.name)) {
                throw new Error(
                    `Circular dependency detected: ${Array.from(this._resolutionStack).join(' -> ')} -> ${serviceInterface.name}`
                );
            }

            // Check resolution depth
            if (this._resolutionDepth >= this._maxResolutionDepth) {
                throw new Error(`Maximum resolution depth (${this._maxResolutionDepth}) exceeded`);
            }

            this._resolutionStack.add(serviceInterface.name);

            // Use resolver chain for sophisticated resolution
            const instance = this._resolverChain.resolve<T>(
                serviceInterface,
                this._registry,
                this,
                context
            );

            if (instance === null || instance === undefined) {
                throw new Error(`Service not found: ${serviceInterface.name}`);
            }

            // Apply lifecycle management
            const managedInstance = this._lifecycleManager.createWithLifecycle(instance, context);

            // Record successful resolution
            const resolutionTime = performance.now() - startTime;
            this._metrics.recordResolution(serviceInterface.name, resolutionTime, true);
            this._debuggingTools.recordResolution(serviceInterface.name, resolutionTime, true);

            return managedInstance;

        } catch (error) {
            const resolutionTime = performance.now() - startTime;
            this._metrics.recordResolution(serviceInterface.name, resolutionTime, false);
            this._debuggingTools.recordResolution(serviceInterface.name, resolutionTime, false, error);
            throw error;
        } finally {
            this._resolutionStack.delete(serviceInterface.name);
        }
    }

    /**
     * Resolve a service as a lazy proxy
     */
    resolveLazy<T>(serviceInterface: ServiceInterface<T>): LazyProxy<T> {
        this._ensureNotDisposed();
        return new LazyProxy<T>(serviceInterface, this);
    }

    /**
     * Try to resolve a service, returning null if not found
     */
    tryResolve<T>(serviceInterface: ServiceInterface<T>): T | null {
        try {
            return this.resolve(serviceInterface);
        } catch {
            return null;
        }
    }

    /**
     * Check if a service is registered
     */
    isRegistered<T>(serviceInterface: ServiceInterface<T>): boolean {
        return this._registry.isRegistered(serviceInterface);
    }

    // ============================================================================
    // SCOPE MANAGEMENT - Advanced Lifecycle Control
    // ============================================================================

    /**
     * Create a new scope for scoped services
     */
    createScope(scopeId: string): void {
        this._lifecycleManager.createScope(scopeId);
        this._debuggingTools.logScopeCreation(scopeId);
    }

    /**
     * Dispose a scope and cleanup its instances
     */
    disposeScope(scopeId: string): void {
        this._lifecycleManager.disposeScope(scopeId);
        this._debuggingTools.logScopeDisposal(scopeId);
    }

    /**
     * Set the current scope for scoped service resolution
     */
    setCurrentScope(scopeId: string): void {
        this._lifecycleManager.setCurrentScope(scopeId);
    }

    // ============================================================================
    // DEBUGGING AND MONITORING - Enterprise Observability
    // ============================================================================

    /**
     * Get comprehensive container diagnostics
     */
    getDiagnostics() {
        return {
            containerId: this._containerId,
            createdAt: this._createdAt,
            isDisposed: this._isDisposed,
            registeredServices: this._registry.getRegisteredServices(),
            metrics: this._metrics.getMetrics(),
            debugInfo: this._debuggingTools.getDebugInfo(),
            lifecycleInfo: this._lifecycleManager.getLifecycleInfo()
        };
    }

    /**
     * Get performance metrics
     */
    getMetrics() {
        return this._metrics.getMetrics();
    }

    /**
     * Clear all performance metrics
     */
    clearMetrics(): void {
        this._metrics.clear();
    }

    /**
     * Enable or disable debug mode
     */
    setDebugMode(enabled: boolean): void {
        this._debuggingTools.setDebugMode(enabled);
    }

    // ============================================================================
    // CONTAINER LIFECYCLE - Proper Resource Management
    // ============================================================================

    /**
     * Dispose the container and cleanup all resources
     */
    dispose(): void {
        if (this._isDisposed) return;

        this._lifecycleManager.dispose();
        this._registry.clear();
        this._metrics.clear();
        this._debuggingTools.dispose();

        this._isDisposed = true;
        this._debuggingTools.logContainerDisposal(this._containerId);
    }

    /**
     * Clone the container with all registrations
     */
    clone(newContainerId?: string): ServiceContainer {
        const cloned = new ServiceContainer(newContainerId);
        this._registry.copyTo(cloned._registry);
        return cloned;
    }

    // ============================================================================
    // PRIVATE UTILITIES
    // ============================================================================

    private _createResolutionContext<T>(serviceInterface: ServiceInterface<T>): ResolutionContext {
        return {
            serviceInterface,
            containerId: this._containerId,
            resolutionStack: Array.from(this._resolutionStack),
            resolutionDepth: this._resolutionDepth,
            timestamp: new Date()
        };
    }

    private _ensureNotDisposed(): void {
        if (this._isDisposed) {
            throw new Error(`Container ${this._containerId} has been disposed`);
        }
    }
}
