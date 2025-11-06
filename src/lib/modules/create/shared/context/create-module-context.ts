/**
 * Create Module Context
 *
 * Provides shared state and services to all descendant components via Svelte's context API.
 * This eliminates prop drilling and makes the component tree more maintainable.
 *
 * Usage:
 * - In CreateModule: setCreateModuleContext({ ... })
 * - In child components: const ctx = getCreateModuleContext()
 *
 * Domain: Create module - Context management
 */

import { getContext, setContext } from "svelte";
import type { createCreateModuleState as CreateModuleStateType } from "../state/create-module-state.svelte";
import type { createConstructTabState as ConstructTabStateType } from "../state/construct-tab-state.svelte";
import type { PanelCoordinationState } from "../state/panel-coordination-state.svelte";
import type { CreateModuleServices } from "../services/ServiceInitializer";

type CreateModuleState = ReturnType<typeof CreateModuleStateType>;
type ConstructTabState = ReturnType<typeof ConstructTabStateType>;

/**
 * Context interface for Create Module
 * Provides all shared state and services to descendant components
 */
export interface CreateModuleContext {
  // Core state
  CreateModuleState: CreateModuleState;
  constructTabState: ConstructTabState;
  panelState: PanelCoordinationState;

  // Services
  services: CreateModuleServices;

  // Layout state
  layout: {
    shouldUseSideBySideLayout: boolean;
    isMobilePortrait: () => boolean;
  };

  // Common handlers
  handlers: {
    onError: (error: string) => void;
  };
}

const CONTEXT_KEY = "createModule";

/**
 * Set the Create Module context
 * Call this in CreateModule component to provide context to descendants
 */
export function setCreateModuleContext(context: CreateModuleContext): void {
  setContext(CONTEXT_KEY, context);
}

/**
 * Get the Create Module context
 * Call this in child components to access shared state and services
 */
export function getCreateModuleContext(): CreateModuleContext {
  const context = getContext<CreateModuleContext>(CONTEXT_KEY);
  
  if (!context) {
    throw new Error(
      "CreateModuleContext not found. Make sure you're calling getCreateModuleContext() " +
      "within a component that is a descendant of CreateModule."
    );
  }
  
  return context;
}

/**
 * Optional: Get the Create Module context if it exists
 * Returns undefined if context is not available
 */
export function tryGetCreateModuleContext(): CreateModuleContext | undefined {
  return getContext<CreateModuleContext>(CONTEXT_KEY);
}

