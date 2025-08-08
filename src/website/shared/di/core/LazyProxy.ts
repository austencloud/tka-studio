/**
 * 🔄 TKA LAZY PROXY
 *
 * Sophisticated lazy loading proxy that defers service instantiation
 * until first access, with transparent method forwarding.
 */

import { ServiceInterface } from './types.js';

export class LazyProxy<T> {
    private _instance: T | null = null;
    private _isInitialized = false;
    private readonly _serviceInterface: ServiceInterface<T>;
    private readonly _container: any;
    private readonly _proxy: T;

    constructor(serviceInterface: ServiceInterface<T>, container: any) {
        this._serviceInterface = serviceInterface;
        this._container = container;

        // Create a proxy that intercepts all property access
        this._proxy = new Proxy(this as any, {
            get: (target, prop, receiver) => {
                // Handle special proxy properties
                if (prop === '_getInstance') {
                    return () => this._getInstance();
                }
                if (prop === '_isInitialized') {
                    return this._isInitialized;
                }
                if (prop === 'toString') {
                    return () => `[LazyProxy for ${this._serviceInterface.name}]`;
                }
                if (prop === Symbol.toStringTag) {
                    return `LazyProxy<${this._serviceInterface.name}>`;
                }

                // Get the actual instance and forward the property access
                const instance = this._getInstance();
                const value = (instance as any)[prop];

                // If it's a function, bind it to the instance
                if (typeof value === 'function') {
                    return value.bind(instance);
                }

                return value;
            },

            set: (target, prop, value, receiver) => {
                // Forward property setting to the actual instance
                const instance = this._getInstance();
                (instance as any)[prop] = value;
                return true;
            },

            has: (target, prop) => {
                // Check if property exists on the actual instance
                const instance = this._getInstance();
                return prop in instance;
            },

            ownKeys: (target) => {
                // Return keys from the actual instance
                const instance = this._getInstance();
                return Reflect.ownKeys(instance);
            },

            getOwnPropertyDescriptor: (target, prop) => {
                // Get property descriptor from the actual instance
                const instance = this._getInstance();
                return Reflect.getOwnPropertyDescriptor(instance, prop);
            },

            defineProperty: (target, prop, descriptor) => {
                // Define property on the actual instance
                const instance = this._getInstance();
                return Reflect.defineProperty(instance, prop, descriptor);
            },

            deleteProperty: (target, prop) => {
                // Delete property from the actual instance
                const instance = this._getInstance();
                return Reflect.deleteProperty(instance, prop);
            }
        });

        return this._proxy;
    }

    /**
     * Get the actual instance, creating it if necessary
     */
    private _getInstance(): T {
        if (!this._isInitialized) {
            try {
                this._instance = this._container.resolve(this._serviceInterface);
                this._isInitialized = true;
            } catch (error) {
                throw new Error(
                    `Failed to lazily resolve service '${this._serviceInterface.name}': ${error}`
                );
            }
        }

        if (this._instance === null || this._instance === undefined) {
            throw new Error(
                `Lazy resolution of service '${this._serviceInterface.name}' returned null or undefined`
            );
        }

        return this._instance;
    }

    /**
     * Check if the proxy has been initialized
     */
    get isInitialized(): boolean {
        return this._isInitialized;
    }

    /**
     * Get the service interface
     */
    get serviceInterface(): ServiceInterface<T> {
        return this._serviceInterface;
    }

    /**
     * Force initialization of the lazy service
     */
    initialize(): T {
        return this._getInstance();
    }

    /**
     * Reset the lazy proxy (for testing purposes)
     */
    reset(): void {
        this._instance = null;
        this._isInitialized = false;
    }
}

/**
 * Create a lazy proxy for a service
 */
export function createLazyProxy<T>(
    serviceInterface: ServiceInterface<T>,
    container: any
): T {
    return new LazyProxy(serviceInterface, container) as any;
}
