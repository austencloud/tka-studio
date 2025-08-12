/**
 * 🚀 TKA ENTERPRISE DEPENDENCY INJECTION SYSTEM
 *
 * Next-generation dependency injection for web applications that matches
 * and exceeds the sophistication of enterprise desktop systems.
 *
 * Features:
 * ✅ Type-safe interface-based registration
 * ✅ Advanced lifecycle management (Singleton, Transient, Scoped, Lazy, Factory)
 * ✅ Sophisticated resolution chain with fallback strategies
 * ✅ Comprehensive validation and error handling
 * ✅ Enterprise-grade debugging and monitoring
 * ✅ Performance metrics and telemetry
 * ✅ Application factory pattern for different environments
 * ✅ Cross-platform compatibility with desktop DI system
 */

// ============================================================================
// CORE EXPORTS - Main DI System Components
// ============================================================================

export { ServiceContainer } from "./core/ServiceContainer.js";
export { ApplicationFactory } from "./ApplicationFactory.js";
export { ServiceRegistrationManager } from "./ServiceRegistrationManager.js";

// ============================================================================
// TYPE SYSTEM EXPORTS - Comprehensive Type Safety
// ============================================================================

export {
  // Core types
  ServiceInterface,
  ServiceScope,
  ServiceDescriptor,
  ResolutionContext,
  ResolutionResult,

  // Validation types
  ValidationResult,
  ValidationError,
  ValidationWarning,

  // Metrics types
  ServiceMetrics,
  ContainerMetrics,

  // Debug types
  DebugInfo,
  RegistrationEvent,
  ResolutionEvent,
  ScopeEvent,
  ErrorEvent,

  // Factory types
  ServiceFactory,
  AsyncServiceFactory,
  ConditionalServiceFactory,
  MultiImplementationFactory,

  // Lifecycle types
  ServiceLifecycleHooks,
  IDisposable,
  IInitializable,

  // Configuration types
  ContainerConfiguration,
  ApplicationFactoryConfiguration,
  ServiceRegistrationConfig,

  // Utility types
  Constructor,
  AbstractConstructor,
  Mixin,
  ServiceProvider,
  ServiceType,

  // Factory functions
  createServiceInterface,
} from "./core/types.js";

// ============================================================================
// ADVANCED COMPONENTS EXPORTS - Enterprise Features
// ============================================================================

export { ServiceRegistry } from "./core/ServiceRegistry.js";
export { ResolverChain, IServiceResolver } from "./core/ResolverChain.js";
export { LifecycleManager } from "./core/LifecycleManager.js";
export { ValidationEngine } from "./core/ValidationEngine.js";
export { DebuggingTools } from "./core/DebuggingTools.js";
export { ServiceMetrics as ServiceMetricsCollector } from "./core/ServiceMetrics.js";
export { LazyProxy, createLazyProxy } from "./core/LazyProxy.js";

// ============================================================================
// CONVENIENCE EXPORTS - Common Service Interfaces
// ============================================================================

export {
  // Core service interfaces
  ISequenceDataService,
  ISettingsService,
  IValidationService,
  ILayoutService,

  // Management service interfaces
  ISequenceManager,
  IPictographManagementService,
  IUIStateManagementService,
  IArrowManagementService,

  // Infrastructure service interfaces
  IFileSystemService,
  ISessionStateService,
  ILoggingService,
  IErrorHandlingService,

  // Web-specific service interfaces
  IStorageService,
  INavigationService,
  IThemeService,
  INotificationService,
} from "./ApplicationFactory.js";

// ============================================================================
// UTILITY FUNCTIONS - Developer Experience Helpers
// ============================================================================

/**
 * Create a production-ready service container with all services registered
 */
export function createProductionContainer(): ServiceContainer {
  return ApplicationFactory.createProductionApp();
}

/**
 * Create a test container with mock services for automated testing
 */
export function createTestContainer(): ServiceContainer {
  return ApplicationFactory.createTestApp();
}

/**
 * Create a headless container for server-side processing
 */
export function createHeadlessContainer(): ServiceContainer {
  return ApplicationFactory.createHeadlessApp();
}

/**
 * Create a development container with enhanced debugging
 */
export function createDevelopmentContainer(): ServiceContainer {
  return ApplicationFactory.createDevelopmentApp();
}

/**
 * Quick service interface creation helper
 */
export function defineService<T>(
  name: string,
  type: new (...args: any[]) => T
) {
  return createServiceInterface(name, type);
}

/**
 * Container builder for custom configurations
 */
export class ContainerBuilder {
  private _container: ServiceContainer;
  private _registrationManager: ServiceRegistrationManager;

  constructor(containerId?: string) {
    this._container = new ServiceContainer(containerId);
    this._registrationManager = new ServiceRegistrationManager();
  }

  /**
   * Register a singleton service
   */
  singleton<T>(
    serviceInterface: ServiceInterface<T>,
    implementation: new (...args: any[]) => T
  ): this {
    this._container.registerSingleton(serviceInterface, implementation);
    return this;
  }

  /**
   * Register a transient service
   */
  transient<T>(
    serviceInterface: ServiceInterface<T>,
    implementation: new (...args: any[]) => T
  ): this {
    this._container.registerTransient(serviceInterface, implementation);
    return this;
  }

  /**
   * Register a factory service
   */
  factory<T>(serviceInterface: ServiceInterface<T>, factory: () => T): this {
    this._container.registerFactory(serviceInterface, factory);
    return this;
  }

  /**
   * Register an instance
   */
  instance<T>(serviceInterface: ServiceInterface<T>, instance: T): this {
    this._container.registerInstance(serviceInterface, instance);
    return this;
  }

  /**
   * Register all standard services
   */
  withStandardServices(): this {
    this._registrationManager.registerAllServices(this._container);
    return this;
  }

  /**
   * Enable debug mode
   */
  withDebugMode(): this {
    this._container.setDebugMode(true);
    return this;
  }

  /**
   * Build the configured container
   */
  build(): ServiceContainer {
    return this._container;
  }
}

/**
 * Create a container builder for custom configurations
 */
export function createContainerBuilder(containerId?: string): ContainerBuilder {
  return new ContainerBuilder(containerId);
}

// ============================================================================
// GLOBAL CONTAINER MANAGEMENT - Singleton Pattern
// ============================================================================

let _globalContainer: ServiceContainer | null = null;

/**
 * Get or create the global application container
 */
export function getGlobalContainer(): ServiceContainer {
  if (!_globalContainer) {
    _globalContainer = ApplicationFactory.createProductionApp();
  }
  return _globalContainer;
}

/**
 * Set the global container (useful for testing)
 */
export function setGlobalContainer(container: ServiceContainer): void {
  _globalContainer = container;
}

/**
 * Reset the global container
 */
export function resetGlobalContainer(): void {
  if (_globalContainer) {
    _globalContainer.dispose();
    _globalContainer = null;
  }
}

/**
 * Resolve a service from the global container
 */
export function resolve<T>(serviceInterface: ServiceInterface<T>): T {
  return getGlobalContainer().resolve(serviceInterface);
}

/**
 * Try to resolve a service from the global container
 */
export function tryResolve<T>(serviceInterface: ServiceInterface<T>): T | null {
  return getGlobalContainer().tryResolve(serviceInterface);
}

// ============================================================================
// VERSION AND METADATA
// ============================================================================

export const VERSION = "1.0.0";
export const BUILD_DATE = new Date().toISOString();

export const SYSTEM_INFO = {
  name: "TKA Enterprise DI System",
  version: VERSION,
  buildDate: BUILD_DATE,
  features: [
    "Type-safe interface-based registration",
    "Advanced lifecycle management",
    "Sophisticated resolution chain",
    "Comprehensive validation",
    "Enterprise debugging tools",
    "Performance metrics",
    "Application factory pattern",
    "Cross-platform compatibility",
  ],
  compatibility: {
    desktop: "Full parity with Python DI system",
    web: "Native TypeScript implementation",
    mobile: "Compatible with React Native",
    server: "Node.js and Deno support",
  },
};

/**
 * Get system information and diagnostics
 */
export function getSystemInfo() {
  return {
    ...SYSTEM_INFO,
    runtime: {
      platform: typeof window !== "undefined" ? "browser" : "node",
      userAgent: typeof navigator !== "undefined" ? navigator.userAgent : "N/A",
      timestamp: new Date().toISOString(),
    },
  };
}
