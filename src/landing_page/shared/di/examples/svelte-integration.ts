/**
 * 🎭 TKA DI SVELTE INTEGRATION EXAMPLE
 *
 * Demonstrates how to integrate the TKA Enterprise DI system with Svelte
 * applications, including context providers, reactive services, and component injection.
 */

import { writable, derived, readable } from 'svelte/store';
import { getContext, setContext } from 'svelte';
import {
    ServiceContainer,
    ApplicationFactory,
    createServiceInterface,
    defineService,
    ServiceScope
} from '../index.js';

// ============================================================================
// SVELTE CONTEXT INTEGRATION
// ============================================================================

const DI_CONTAINER_KEY = Symbol('DI_CONTAINER');

/**
 * Set the DI container in Svelte context
 */
export function setDIContainer(container: ServiceContainer): void {
    setContext(DI_CONTAINER_KEY, container);
}

/**
 * Get the DI container from Svelte context
 */
export function getDIContainer(): ServiceContainer {
    const container = getContext(DI_CONTAINER_KEY);
    if (!container) {
        throw new Error('DI Container not found in context. Make sure to call setDIContainer in a parent component.');
    }
    return container;
}

/**
 * Resolve a service from the DI container in Svelte context
 */
export function inject<T>(serviceInterface: any): T {
    const container = getDIContainer();
    return container.resolve(serviceInterface);
}

/**
 * Try to resolve a service, returning null if not found
 */
export function tryInject<T>(serviceInterface: any): T | null {
    try {
        const container = getDIContainer();
        return container.tryResolve(serviceInterface);
    } catch {
        return null;
    }
}

// ============================================================================
// REACTIVE SERVICE STORES
// ============================================================================

/**
 * Create a reactive Svelte store for a service
 */
export function createServiceStore<T>(serviceInterface: any) {
    const container = getDIContainer();
    const service = container.resolve(serviceInterface);

    // Create a writable store with the service
    const store = writable(service);

    return {
        subscribe: store.subscribe,
        get: () => service,
        update: (updater: (service: T) => T) => {
            const newService = updater(service);
            store.set(newService);
            return newService;
        }
    };
}

/**
 * Create a reactive store that automatically updates when service state changes
 */
export function createReactiveServiceStore<T, R>(
    serviceInterface: any,
    selector: (service: T) => R,
    interval = 1000
) {
    const container = getDIContainer();
    const service = container.resolve(serviceInterface);

    return readable(selector(service), (set) => {
        const intervalId = setInterval(() => {
            set(selector(service));
        }, interval);

        return () => clearInterval(intervalId);
    });
}

// ============================================================================
// COMPONENT SCOPED SERVICES
// ============================================================================

/**
 * Create a component-scoped service that's unique per component instance
 */
export function createComponentScopedService<T>(
    serviceInterface: any,
    componentId?: string
): T {
    const container = getDIContainer();
    const scopeId = componentId || `component_${Math.random().toString(36).substr(2, 9)}`;

    // Create component scope if it doesn't exist
    if (!container.isRegistered(serviceInterface)) {
        throw new Error(`Service ${serviceInterface.name} is not registered`);
    }

    container.createScope(scopeId);
    container.setCurrentScope(scopeId);

    return container.resolve(serviceInterface);
}

// ============================================================================
// EXAMPLE SERVICES FOR SVELTE INTEGRATION
// ============================================================================

// Define reactive services
const ICounterService = defineService('ICounterService', class {
    count = 0;
    increment(): void {}
    decrement(): void {}
    reset(): void {}
    subscribe(callback: (count: number) => void): () => void { return () => {}; }
});

const IThemeService = defineService('IThemeService', class {
    currentTheme = 'light';
    setTheme(theme: string): void {}
    getAvailableThemes(): string[] { return []; }
    subscribe(callback: (theme: string) => void): () => void { return () => {}; }
});

const INotificationService = defineService('INotificationService', class {
    notifications: any[] = [];
    addNotification(message: string, type: string): void {}
    removeNotification(id: string): void {}
    subscribe(callback: (notifications: any[]) => void): () => void { return () => {}; }
});

// Implement reactive services
class ReactiveCounterService {
    private _count = 0;
    private _subscribers = new Set<(count: number) => void>();

    get count(): number {
        return this._count;
    }

    increment(): void {
        this._count++;
        this._notify();
    }

    decrement(): void {
        this._count--;
        this._notify();
    }

    reset(): void {
        this._count = 0;
        this._notify();
    }

    subscribe(callback: (count: number) => void): () => void {
        this._subscribers.add(callback);
        callback(this._count); // Initial call

        return () => {
            this._subscribers.delete(callback);
        };
    }

    private _notify(): void {
        this._subscribers.forEach(callback => callback(this._count));
    }
}

class ReactiveThemeService {
    private _currentTheme = 'light';
    private _subscribers = new Set<(theme: string) => void>();
    private _availableThemes = ['light', 'dark', 'blue', 'green'];

    get currentTheme(): string {
        return this._currentTheme;
    }

    setTheme(theme: string): void {
        if (this._availableThemes.includes(theme)) {
            this._currentTheme = theme;
            this._notify();

            // Apply theme to document
            if (typeof document !== 'undefined') {
                document.documentElement.setAttribute('data-theme', theme);
            }
        }
    }

    getAvailableThemes(): string[] {
        return [...this._availableThemes];
    }

    subscribe(callback: (theme: string) => void): () => void {
        this._subscribers.add(callback);
        callback(this._currentTheme); // Initial call

        return () => {
            this._subscribers.delete(callback);
        };
    }

    private _notify(): void {
        this._subscribers.forEach(callback => callback(this._currentTheme));
    }
}

class ReactiveNotificationService {
    private _notifications: any[] = [];
    private _subscribers = new Set<(notifications: any[]) => void>();

    get notifications(): any[] {
        return [...this._notifications];
    }

    addNotification(message: string, type: string = 'info'): void {
        const notification = {
            id: `notif_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
            message,
            type,
            timestamp: new Date()
        };

        this._notifications.push(notification);
        this._notify();

        // Auto-remove after 5 seconds
        setTimeout(() => {
            this.removeNotification(notification.id);
        }, 5000);
    }

    removeNotification(id: string): void {
        const index = this._notifications.findIndex(n => n.id === id);
        if (index >= 0) {
            this._notifications.splice(index, 1);
            this._notify();
        }
    }

    subscribe(callback: (notifications: any[]) => void): () => void {
        this._subscribers.add(callback);
        callback(this._notifications); // Initial call

        return () => {
            this._subscribers.delete(callback);
        };
    }

    private _notify(): void {
        this._subscribers.forEach(callback => callback([...this._notifications]));
    }
}

// ============================================================================
// SVELTE STORE INTEGRATION
// ============================================================================

/**
 * Convert a reactive service to a Svelte store
 */
export function serviceToStore<T>(service: any, selector: (service: any) => T) {
    return readable(selector(service), (set) => {
        if (typeof service.subscribe === 'function') {
            return service.subscribe(() => {
                set(selector(service));
            });
        }

        // Fallback for non-reactive services
        set(selector(service));
        return () => {};
    });
}

/**
 * Create Svelte stores from services
 */
export function createServiceStores(container: ServiceContainer) {
    const counterService = container.resolve(ICounterService);
    const themeService = container.resolve(IThemeService);
    const notificationService = container.resolve(INotificationService);

    return {
        // Counter store
        count: serviceToStore(counterService, s => s.count),

        // Theme store
        theme: serviceToStore(themeService, s => s.currentTheme),

        // Notifications store
        notifications: serviceToStore(notificationService, s => s.notifications),

        // Service actions
        actions: {
            counter: {
                increment: () => counterService.increment(),
                decrement: () => counterService.decrement(),
                reset: () => counterService.reset()
            },
            theme: {
                setTheme: (theme: string) => themeService.setTheme(theme),
                getAvailableThemes: () => themeService.getAvailableThemes()
            },
            notifications: {
                add: (message: string, type?: string) => notificationService.addNotification(message, type),
                remove: (id: string) => notificationService.removeNotification(id)
            }
        }
    };
}

// ============================================================================
// SETUP FUNCTION FOR SVELTE APPS
// ============================================================================

/**
 * Setup DI container for Svelte application
 */
export function setupSvelteDI() {
    // Create container with reactive services
    const container = ApplicationFactory.createDevelopmentApp();

    // Register reactive services
    container.registerSingleton(ICounterService, ReactiveCounterService);
    container.registerSingleton(IThemeService, ReactiveThemeService);
    container.registerSingleton(INotificationService, ReactiveNotificationService);

    // Create stores
    const stores = createServiceStores(container);

    return {
        container,
        stores,
        setDIContainer: () => setDIContainer(container),
        inject,
        tryInject,
        createServiceStore,
        createReactiveServiceStore,
        createComponentScopedService
    };
}

// ============================================================================
// EXAMPLE USAGE IN SVELTE COMPONENTS
// ============================================================================

export const SVELTE_COMPONENT_EXAMPLES = `
<!-- App.svelte -->
<script>
  import { setupSvelteDI } from './di/examples/svelte-integration.js';

  const { container, stores, setDIContainer } = setupSvelteDI();

  // Set DI container in context for child components
  setDIContainer();

  // Use reactive stores
  $: count = $stores.count;
  $: theme = $stores.theme;
  $: notifications = $stores.notifications;
</script>

<!-- Counter.svelte -->
<script>
  import { inject } from './di/examples/svelte-integration.js';
  import { ICounterService } from './di/examples/svelte-integration.js';

  // Inject service directly
  const counterService = inject(ICounterService);

  // Create reactive store
  const countStore = serviceToStore(counterService, s => s.count);
</script>

<div>
  <h2>Counter: {$countStore}</h2>
  <button on:click={() => counterService.increment()}>+</button>
  <button on:click={() => counterService.decrement()}>-</button>
  <button on:click={() => counterService.reset()}>Reset</button>
</div>

<!-- ThemeSelector.svelte -->
<script>
  import { inject } from './di/examples/svelte-integration.js';
  import { IThemeService } from './di/examples/svelte-integration.js';

  const themeService = inject(IThemeService);
  const themeStore = serviceToStore(themeService, s => s.currentTheme);
  const availableThemes = themeService.getAvailableThemes();
</script>

<select bind:value={$themeStore} on:change={(e) => themeService.setTheme(e.target.value)}>
  {#each availableThemes as theme}
    <option value={theme}>{theme}</option>
  {/each}
</select>
`;

console.log('🎭 Svelte DI Integration Examples Ready!');
console.log('📝 Component examples available in SVELTE_COMPONENT_EXAMPLES');
console.log('✅ Full reactive service integration with Svelte stores');
