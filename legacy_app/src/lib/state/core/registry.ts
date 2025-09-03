/**
 * State Registry
 *
 * A central registry for all state machines and stores in the application.
 * This helps with:
 * - Tracking all state containers
 * - Providing debugging capabilities
 * - Enabling persistence
 * - Facilitating testing
 *
 * This file is now a re-export from the modular registry implementation.
 */

// Re-export everything from the modular registry
export * from './registry/index';
