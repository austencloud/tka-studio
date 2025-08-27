/**
 * Application Bootstrap - TKA V2 Modern (InversifyJS)
 *
 * This module exports the InversifyJS container and resolve function.
 * The old custom DI system has been replaced with InversifyJS.
 */

// Re-export everything from the inversify container
export { container, resolve, TYPES } from "./inversify/container";

// Legacy functions for backward compatibility
export async function createWebApplication() {
  const { container } = await import("./inversify/container");
  return container;
}

export function getContainer() {
  const { container } = require("./inversify/container");
  return container;
}

export function setGlobalContainer() {
  // No-op - InversifyJS handles this internally
}

export function legacyResolve() {
  throw new Error(
    "🚨 LEGACY DI SYSTEM DISABLED! Use resolve(TYPES.ServiceName) instead."
  );
}
