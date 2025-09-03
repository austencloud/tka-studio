/**
 * Helper functions for mocking localStorage in tests
 */
import { vi } from 'vitest';

/**
 * Creates a mock storage object that can be used to replace localStorage
 * @returns A mock storage object with spied methods
 */
export function createMockStorage() {
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
		length: 0,
		key: vi.fn((index: number) => Object.keys(store)[index] || null),
		_store: store // For direct access in tests
	};
}

/**
 * Sets up localStorage mock for tests
 * @returns The mock storage object
 */
export function setupLocalStorageMock() {
	const mockStorage = createMockStorage();

	// Save the original localStorage
	const originalLocalStorage = global.localStorage;

	// Use Object.defineProperty to avoid "Cannot assign to read only property" error
	Object.defineProperty(window, 'localStorage', {
		value: mockStorage,
		writable: true
	});

	// Also mock global.localStorage for environments where window.localStorage isn't used
	const originalGlobalStorage = global.localStorage;
	global.localStorage = mockStorage;

	// Return both the mock and a cleanup function
	return {
		mockStorage,
		cleanup: () => {
			// Restore the original localStorage
			Object.defineProperty(window, 'localStorage', {
				value: originalLocalStorage,
				writable: true
			});
			global.localStorage = originalGlobalStorage;
		}
	};
}

/**
 * Configures a mock storage to throw quota exceeded error on setItem
 * @param mockStorage The mock storage to configure
 */
export function setupQuotaExceededError(mockStorage: ReturnType<typeof createMockStorage>) {
	const quotaError = new DOMException('Quota exceeded', 'QuotaExceededError');
	vi.spyOn(mockStorage, 'setItem').mockImplementation(() => {
		throw quotaError;
	});
	return quotaError;
}

/**
 * Configures a mock storage to return specific data for a key
 * @param mockStorage The mock storage to configure
 * @param key The key to mock
 * @param value The value to return for the key
 */
export function setupMockStorageData(
	mockStorage: ReturnType<typeof createMockStorage>,
	key: string,
	value: string
) {
	vi.spyOn(mockStorage, 'getItem').mockImplementation((k) => {
		if (k === key) {
			return value;
		}
		return null;
	});
}
