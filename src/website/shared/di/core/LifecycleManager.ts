/**
 * 🔄 TKA LIFECYCLE MANAGER
 *
 * Advanced service lifecycle management with sophisticated scoping,
 * disposal patterns, and resource cleanup.
 */

import { ServiceScope, ResolutionContext, IDisposable, IInitializable } from './types.js';

export class LifecycleManager {
    private readonly _scopes = new Map<string, ScopeManager>();
    private readonly _disposables = new Set<IDisposable>();
    private readonly _initializables = new Set<IInitializable>();
    private _currentScope?: string;

    /**
     * Create a new scope for scoped services
     */
    createScope(scopeId: string): void {
        if (this._scopes.has(scopeId)) {
            throw new Error(`Scope '${scopeId}' already exists`);
        }

        const scopeManager = new ScopeManager(scopeId);
        this._scopes.set(scopeId, scopeManager);
    }

    /**
     * Dispose a scope and cleanup its instances
     */
    disposeScope(scopeId: string): void {
        const scopeManager = this._scopes.get(scopeId);
        if (scopeManager) {
            scopeManager.dispose();
            this._scopes.delete(scopeId);
        }

        if (this._currentScope === scopeId) {
            this._currentScope = undefined;
        }
    }

    /**
     * Set the current scope for scoped service resolution
     */
    setCurrentScope(scopeId: string): void {
        if (!this._scopes.has(scopeId)) {
            throw new Error(`Scope '${scopeId}' does not exist`);
        }
        this._currentScope = scopeId;
    }

    /**
     * Get the current scope ID
     */
    getCurrentScope(): string | undefined {
        return this._currentScope;
    }

    /**
     * Apply lifecycle management to a service instance
     */
    createWithLifecycle<T>(instance: T, context: ResolutionContext): T {
        // Initialize if needed
        if (this._isInitializable(instance)) {
            this._initializables.add(instance);
            this._initializeInstance(instance);
        }

        // Track disposables
        if (this._isDisposable(instance)) {
            this._disposables.add(instance);
        }

        // Apply scope-specific lifecycle
        this._applyScopeLifecycle(instance, context);

        return instance;
    }

    /**
     * Get lifecycle information for debugging
     */
    getLifecycleInfo() {
        return {
            scopes: Array.from(this._scopes.keys()),
            currentScope: this._currentScope,
            disposables: this._disposables.size,
            initializables: this._initializables.size,
            scopeDetails: Object.fromEntries(
                Array.from(this._scopes.entries()).map(([id, manager]) => [
                    id,
                    manager.getInfo()
                ])
            )
        };
    }

    /**
     * Dispose all managed resources
     */
    dispose(): void {
        // Dispose all scopes
        for (const scopeManager of this._scopes.values()) {
            scopeManager.dispose();
        }
        this._scopes.clear();

        // Dispose all tracked disposables
        for (const disposable of this._disposables) {
            try {
                disposable.dispose();
            } catch (error) {
                console.error('Error disposing service:', error);
            }
        }
        this._disposables.clear();
        this._initializables.clear();
        this._currentScope = undefined;
    }

    private _isDisposable(instance: any): instance is IDisposable {
        return instance && typeof instance.dispose === 'function';
    }

    private _isInitializable(instance: any): instance is IInitializable {
        return instance && typeof instance.initialize === 'function';
    }

    private async _initializeInstance(instance: IInitializable): Promise<void> {
        try {
            const result = instance.initialize();
            if (result instanceof Promise) {
                await result;
            }
        } catch (error) {
            console.error('Error initializing service:', error);
        }
    }

    private _applyScopeLifecycle<T>(instance: T, context: ResolutionContext): void {
        const scopeId = this._determineScopeId(context);
        if (scopeId) {
            const scopeManager = this._scopes.get(scopeId);
            if (scopeManager) {
                scopeManager.addInstance(instance);
            }
        }
    }

    private _determineScopeId(context: ResolutionContext): string | undefined {
        if (context.scopeId) return context.scopeId;
        if (context.requestId) return `request_${context.requestId}`;
        if (context.sessionId) return `session_${context.sessionId}`;
        if (context.componentId) return `component_${context.componentId}`;
        return this._currentScope;
    }
}

/**
 * Manages instances within a specific scope
 */
class ScopeManager {
    private readonly _scopeId: string;
    private readonly _instances = new Set<any>();
    private readonly _createdAt = new Date();
    private _disposed = false;

    constructor(scopeId: string) {
        this._scopeId = scopeId;
    }

    addInstance(instance: any): void {
        if (this._disposed) {
            throw new Error(`Scope '${this._scopeId}' has been disposed`);
        }
        this._instances.add(instance);
    }

    removeInstance(instance: any): void {
        this._instances.delete(instance);
    }

    getInfo() {
        return {
            scopeId: this._scopeId,
            instanceCount: this._instances.size,
            createdAt: this._createdAt,
            disposed: this._disposed
        };
    }

    dispose(): void {
        if (this._disposed) return;

        // Dispose all instances that are disposable
        for (const instance of this._instances) {
            if (instance && typeof instance.dispose === 'function') {
                try {
                    instance.dispose();
                } catch (error) {
                    console.error(`Error disposing instance in scope '${this._scopeId}':`, error);
                }
            }
        }

        this._instances.clear();
        this._disposed = true;
    }
}
