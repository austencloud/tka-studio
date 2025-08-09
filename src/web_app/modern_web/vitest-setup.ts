/**
 * Vitest Setup File
 *
 * Configures the testing environment for modern pictograph tests
 */

import { vi } from 'vitest';
import '@testing-library/jest-dom';

// Mock browser APIs that might not be available in test environment
Object.defineProperty(window, 'matchMedia', {
	writable: true,
	value: vi.fn().mockImplementation((query) => ({
		matches: false,
		media: query,
		onchange: null,
		addListener: vi.fn(), // deprecated
		removeListener: vi.fn(), // deprecated
		addEventListener: vi.fn(),
		removeEventListener: vi.fn(),
		dispatchEvent: vi.fn(),
	})),
});

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
	observe: vi.fn(),
	unobserve: vi.fn(),
	disconnect: vi.fn(),
}));

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
	observe: vi.fn(),
	unobserve: vi.fn(),
	disconnect: vi.fn(),
}));

// Mock crypto.randomUUID for ID generation
Object.defineProperty(global, 'crypto', {
	value: {
		randomUUID: vi.fn(() => 'test-uuid-' + Math.random().toString(36).slice(2)),
	},
});

// Mock fetch for testing
global.fetch = vi.fn();

// Mock URL constructor
global.URL = vi.fn().mockImplementation((url) => ({
	href: url,
	pathname: new URL(url, 'http://localhost').pathname,
	search: new URL(url, 'http://localhost').search,
	hash: new URL(url, 'http://localhost').hash,
}));

// Suppress console warnings in tests unless debugging
const originalWarn = console.warn;
console.warn = (...args) => {
	// Only show warnings that are not from expected test behavior
	const message = args[0];
	if (typeof message === 'string') {
		// Suppress known testing warnings
		if (
			message.includes('deprecation') ||
			message.includes('test environment') ||
			message.includes('jsdom')
		) {
			return;
		}
	}
	originalWarn(...args);
};

// Set up test environment globals
global.__TEST_ENV__ = true;
