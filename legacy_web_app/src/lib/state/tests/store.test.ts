import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { get } from 'svelte/store';
import { stateRegistry } from '../core/registry';
import { createStore, createSelector, combineStores, createPersistentStore } from '../core/store';

// Helper to mock localStorage for persistence tests
const mockLocalStorage = () => {
	let store: Record<string, string> = {};
	return {
		getItem: vi.fn((key: string) => store[key] || null),
		setItem: vi.fn((key: string, value: string) => {
			store[key] = value.toString();
		}),
		removeItem: vi.fn((key: string) => {
			delete store[key];
		}),
		clear: vi.fn(() => {
			store = {};
		}),
		throwQuotaExceededError: () => {
			vi.mocked(localStorage.setItem).mockImplementationOnce(() => {
				throw new DOMException('Quota exceeded', 'QuotaExceededError');
			});
		},
		_store: store
	};
};

describe('Store Factory', () => {
	beforeEach(() => {
		vi.resetAllMocks();
		vi.useFakeTimers();
		localStorage.clear();
		stateRegistry.clear();
	});

	afterEach(() => {
		stateRegistry.clear();
		vi.useRealTimers();
	});

	describe('createStore', () => {
		it('creates a store with initial state', () => {
			const store = createStore('testStore', { count: 0 }, () => ({}));
			expect(get(store)).toEqual({ count: 0 });
		});

		it('creates a store with actions that can update state', () => {
			const store = createStore('counterStore', { count: 0 }, (set, update, get) => ({
				increment: () => update((state) => ({ count: state.count + 1 })),
				decrement: () => update((state) => ({ count: state.count - 1 })),
				setValue: (value: number) => set({ count: value }),
				getCount: () => get().count
			}));

			// Test actions
			store.increment();
			expect(get(store).count).toBe(1);

			store.decrement();
			expect(get(store).count).toBe(0);

			store.setValue(42);
			expect(get(store).count).toBe(42);

			// Test getter
			expect(store.getCount()).toBe(42);
		});

		it('provides a reset action automatically', () => {
			const store = createStore('resetStore', { count: 10 }, () => ({
				increment: () => {}
			}));

			// Update the state
			store.subscribe((value) => {}); // establish a subscription
			store.increment();

			// Reset should restore the initial state
			store.reset();
			expect(get(store)).toEqual({ count: 10 });
		});

		it('registers the store with the state registry', () => {
			const registrySpy = vi.spyOn(stateRegistry, 'registerStore');

			createStore('registryTest', { value: 'test' }, () => ({}), {
				description: 'Test description'
			});

			expect(registrySpy).toHaveBeenCalledWith(
				'registryTest',
				expect.anything(),
				expect.objectContaining({
					description: 'Test description'
				})
			);
		});

		it('tracks subscriptions for cleanup', () => {
			const trackSubscriptionSpy = vi.spyOn(stateRegistry, 'trackSubscription');

			const store = createStore('subscriptionStore', { value: 'test' }, () => ({}));

			// Subscribe to the store
			const unsubscribe = store.subscribe(() => {});

			expect(trackSubscriptionSpy).toHaveBeenCalledWith('subscriptionStore', expect.any(Function));

			// Clean up
			unsubscribe();
		});
	});

	describe('createSelector', () => {
		it('creates a derived store from a parent store', () => {
			// Create a parent store with explicit type definitions
			interface UserState {
				user: {
					name: string;
					age: number;
				};
			}

			const parentStore = createStore<
				UserState,
				{
					updateName: (name: string) => void;
				}
			>('parentStore', { user: { name: 'John', age: 30 } }, (set) => ({
				updateName: (name: string) => set({ user: { name, age: 30 } })
			}));

			// Create a derived store selecting the name
			const nameSelector = createSelector(
				{
					subscribe: (callback) => {
						return parentStore.subscribe((state) => callback(state.user.name));
					}
				},
				{
					id: 'nameSelector',
					description: 'Selects user name'
				}
			);

			// Check initial value
			expect(get(nameSelector)).toBe('John');

			// Update the parent store
			parentStore.updateName('Jane');

			// The selector should reflect the updated value
			expect(get(nameSelector)).toBe('Jane');
		});

		it('registers selectors with the state registry when ID provided', () => {
			const registrySpy = vi.spyOn(stateRegistry, 'registerStore');

			const parentStore = createStore('parentStore', { count: 0 }, () => ({}));

			createSelector(
				{
					subscribe: (callback) => {
						return parentStore.subscribe((state) => callback(state.count));
					}
				},
				{
					id: 'countSelector',
					description: 'Selects count'
				}
			);

			expect(registrySpy).toHaveBeenCalledWith(
				'countSelector',
				expect.anything(),
				expect.objectContaining({
					persist: false,
					description: 'Selects count'
				})
			);
		});

		it('tracks subscriptions for cleanup when ID provided', () => {
			const trackSubscriptionSpy = vi.spyOn(stateRegistry, 'trackSubscription');

			const parentStore = createStore('parentStore', { count: 0 }, () => ({}));

			const countSelector = createSelector(
				{
					subscribe: (callback) => {
						return parentStore.subscribe((state) => callback(state.count));
					}
				},
				{ id: 'countSelector' }
			);

			// Subscribe to the selector
			const unsubscribe = countSelector.subscribe(() => {});

			expect(trackSubscriptionSpy).toHaveBeenCalledWith('countSelector', expect.any(Function));

			// Clean up
			unsubscribe();
		});
	});

	describe('combineStores', () => {
		it('combines multiple stores into a single derived store', () => {
			interface UserStore {
				name: string;
			}
			interface ScoreStore {
				value: number;
			}

			const userStore = createStore<UserStore, {}>('userStore', { name: 'John' }, () => ({}));
			const scoreStore = createStore<
				ScoreStore,
				{
					setValue: (value: number) => void;
				}
			>('scoreStore', { value: 100 }, (set) => ({
				setValue: (value: number) => set({ value })
			}));

			const combinedStore = combineStores(
				{
					user: userStore,
					score: scoreStore
				},
				{
					id: 'combinedStore',
					description: 'Combined user and score'
				}
			);

			// Check combined value
			expect(get(combinedStore)).toEqual({
				user: { name: 'John' },
				score: { value: 100 }
			});

			// Update one of the stores
			scoreStore.setValue(200);

			// Combined store should reflect the update
			expect(get(combinedStore)).toEqual({
				user: { name: 'John' },
				score: { value: 200 }
			});
		});

		it('registers combined store with registry when ID provided', () => {
			const registrySpy = vi.spyOn(stateRegistry, 'registerStore');

			const store1 = createStore('store1', { a: 1 }, () => ({}));
			const store2 = createStore('store2', { b: 2 }, () => ({}));

			combineStores(
				{ store1, store2 },
				{
					id: 'combinedStores',
					description: 'Combined stores'
				}
			);

			expect(registrySpy).toHaveBeenCalledWith(
				'combinedStores',
				expect.anything(),
				expect.objectContaining({
					persist: false,
					description: 'Combined stores'
				})
			);
		});

		it('tracks subscriptions for cleanup when ID provided', () => {
			const trackSubscriptionSpy = vi.spyOn(stateRegistry, 'trackSubscription');

			const store1 = createStore('store1', { a: 1 }, () => ({}));
			const store2 = createStore('store2', { b: 2 }, () => ({}));

			const combined = combineStores({ store1, store2 }, { id: 'combinedStores' });

			// Subscribe to the combined store
			const unsubscribe = combined.subscribe(() => {});

			expect(trackSubscriptionSpy).toHaveBeenCalledWith('combinedStores', expect.any(Function));

			// Clean up
			unsubscribe();
		});
	});

	describe('createPersistentStore', () => {
		beforeEach(() => {
			// Set up localStorage mock for each test
			Object.defineProperty(window, 'localStorage', {
				value: mockLocalStorage(),
				writable: true
			});
		});

		it('creates a store that persists to localStorage', () => {
			const persistentStore = createPersistentStore('persistentStore', { count: 0 });

			// Update the store
			persistentStore.update((state) => ({ count: 42 }));

			// Fast-forward timers to trigger debounced persistence
			vi.runAllTimers();

			// Verify localStorage was called with the right data
			expect(localStorage.setItem).toHaveBeenCalledWith(
				'persistentStore',
				JSON.stringify({ count: 42 })
			);
		});

		it('restores state from localStorage on initialization', () => {
			// Set up pre-existing data in localStorage
			localStorage.setItem('existingStore', JSON.stringify({ value: 'restored' }));

			// Create store with the same ID
			const store = createPersistentStore('existingStore', { value: 'initial' });

			// Should restore the persisted state
			expect(get(store)).toEqual({ value: 'restored' });
		});

		it('supports selective field persistence', () => {
			const store = createPersistentStore(
				'selectiveStore',
				{
					persist: 'yes',
					doNotPersist: 'no'
				},
				{
					persistFields: ['persist']
				}
			);

			// Update store
			store.update((state) => ({
				...state,
				persist: 'updated',
				doNotPersist: 'updated too'
			}));

			// Fast-forward timers
			vi.runAllTimers();

			// Check what was persisted
			expect(localStorage.setItem).toHaveBeenCalledWith(
				'selectiveStore',
				JSON.stringify({ persist: 'updated' }) // Only the 'persist' field should be saved
			);

			// Create a new store to verify what gets restored
			localStorage.clear();
			localStorage.setItem('selectiveStore', JSON.stringify({ persist: 'restored' }));

			const newStore = createPersistentStore(
				'selectiveStore',
				{
					persist: 'initial',
					doNotPersist: 'initial'
				},
				{
					persistFields: ['persist']
				}
			);

			// The persisted field should be restored, but the non-persisted field should use initial value
			expect(get(newStore)).toEqual({
				persist: 'restored', // From localStorage
				doNotPersist: 'initial' // From initial state
			});
		});

		it('debounces persistence operations', () => {
			const store = createPersistentStore('debouncedStore', { count: 0 }, { debounceTime: 500 });

			// Make multiple rapid updates
			store.update((state) => ({ count: 1 }));
			store.update((state) => ({ count: 2 }));
			store.update((state) => ({ count: 3 }));

			// No localStorage calls should have happened yet
			expect(localStorage.setItem).not.toHaveBeenCalled();

			// Advance time but not enough to trigger persistence
			vi.advanceTimersByTime(300);
			expect(localStorage.setItem).not.toHaveBeenCalled();

			// Advance time to trigger persistence
			vi.advanceTimersByTime(200);
			expect(localStorage.setItem).toHaveBeenCalledTimes(1);
			expect(localStorage.setItem).toHaveBeenCalledWith(
				'debouncedStore',
				JSON.stringify({ count: 3 })
			);
		});

		it('handles localStorage quota errors', () => {
			// Mock console methods
			const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});
			const consoleWarnSpy = vi.spyOn(console, 'warn').mockImplementation(() => {});

			// Create our own localStorage mock with a throwing setItem
			const mockLS = {
				getItem: vi.fn(),
				setItem: vi.fn().mockImplementation(() => {
					throw new DOMException('Quota exceeded', 'QuotaExceededError');
				}),
				removeItem: vi.fn(),
				clear: vi.fn(),
				length: 0,
				key: vi.fn()
			};

			// Replace the global localStorage
			Object.defineProperty(window, 'localStorage', { value: mockLS, writable: true });

			// Create store
			const store = createPersistentStore('quotaStore', { data: 'large' });

			// Update store to trigger persistence
			store.update((state) => ({ data: 'even larger' }));

			// Fast-forward timers
			vi.runAllTimers();

			// Verify error was logged
			expect(consoleErrorSpy).toHaveBeenCalledWith(
				expect.stringContaining('Error persisting state'),
				expect.anything()
			);
		});

		it('detects changes and only persists when necessary', () => {
			const store = createPersistentStore('efficientStore', { count: 0 });

			// Update with a new value
			store.update((state) => ({ count: 1 }));
			vi.runAllTimers();

			// Should persist
			expect(localStorage.setItem).toHaveBeenCalledTimes(1);
			vi.clearAllMocks();

			// Update with the same value
			store.update((state) => ({ count: 1 })); // Same value
			vi.runAllTimers();

			// Should not persist again (no change)
			expect(localStorage.setItem).not.toHaveBeenCalled();
		});
	});
});
