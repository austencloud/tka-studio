/**
 * 🎯 TKA ENTERPRISE DI TYPE SYSTEM
 *
 * Sophisticated type definitions that provide compile-time safety
 * and runtime validation for the dependency injection system.
 */

// ============================================================================
// CORE SERVICE TYPES - Type-Safe Interface System
// ============================================================================

/**
 * Service interface marker with runtime type information
 */
export interface ServiceInterface<T = any> {
    readonly name: string;
    readonly symbol: symbol;
    readonly type: new (...args: any[]) => T;
    readonly metadata?: ServiceMetadata;
}

/**
 * Create a type-safe service interface
 */
export function createServiceInterface<T>(
    name: string,
    type: new (...args: any[]) => T,
    metadata?: ServiceMetadata
): ServiceInterface<T> {
    return {
        name,
        symbol: Symbol(name),
        type,
        metadata
    };
}

/**
 * Service metadata for enhanced debugging and validation
 */
export interface ServiceMetadata {
    description?: string;
    version?: string;
    dependencies?: string[];
    tags?: string[];
    deprecated?: boolean;
    deprecationMessage?: string;
}

// ============================================================================
// SERVICE LIFECYCLE - Advanced Scoping System
// ============================================================================

/**
 * Service lifecycle scopes
 */
export enum ServiceScope {
    /** One instance per container */
    Singleton = 'singleton',

    /** New instance per resolution */
    Transient = 'transient',

    /** One instance per scope */
    Scoped = 'scoped',

    /** Deferred instantiation */
    Lazy = 'lazy',

    /** Custom factory function */
    Factory = 'factory',

    /** Specific instance */
    Instance = 'instance',

    /** One instance per request (web-specific) */
    Request = 'request',

    /** One instance per session (web-specific) */
    Session = 'session',

    /** One instance per component tree (Svelte-specific) */
    Component = 'component'
}

/**
 * Service descriptor containing registration information
 */
export interface ServiceDescriptor<T = any> {
    readonly serviceInterface: ServiceInterface<T>;
    readonly implementation?: new (...args: any[]) => T;
    readonly factory?: () => T;
    readonly instance?: T;
    readonly scope: ServiceScope;
    readonly registeredAt: Date;
    readonly metadata?: ServiceMetadata;
}

// ============================================================================
// RESOLUTION CONTEXT - Enterprise Debugging Support
// ============================================================================

/**
 * Context information for service resolution
 */
export interface ResolutionContext {
    readonly serviceInterface: ServiceInterface;
    readonly containerId: string;
    readonly resolutionStack: string[];
    readonly resolutionDepth: number;
    readonly timestamp: Date;
    readonly scopeId?: string;
    readonly requestId?: string;
    readonly sessionId?: string;
    readonly componentId?: string;
}

/**
 * Resolution result with detailed information
 */
export interface ResolutionResult<T = any> {
    readonly instance: T;
    readonly context: ResolutionContext;
    readonly resolutionTime: number;
    readonly fromCache: boolean;
    readonly resolverUsed: string;
}

// ============================================================================
// VALIDATION TYPES - Comprehensive Error Handling
// ============================================================================

/**
 * Validation result for service registration
 */
export interface ValidationResult {
    readonly isValid: boolean;
    readonly errors: ValidationError[];
    readonly warnings: ValidationWarning[];
}

/**
 * Validation error details
 */
export interface ValidationError {
    readonly code: string;
    readonly message: string;
    readonly severity: 'error' | 'warning' | 'info';
    readonly context?: any;
}

/**
 * Validation warning details
 */
export interface ValidationWarning {
    readonly code: string;
    readonly message: string;
    readonly suggestion?: string;
    readonly context?: any;
}

// ============================================================================
// METRICS AND MONITORING - Performance Tracking
// ============================================================================

/**
 * Service resolution metrics
 */
export interface ServiceMetrics {
    readonly serviceName: string;
    readonly totalResolutions: number;
    readonly successfulResolutions: number;
    readonly failedResolutions: number;
    readonly averageResolutionTime: number;
    readonly minResolutionTime: number;
    readonly maxResolutionTime: number;
    readonly lastResolutionTime: Date | null;
    readonly cacheHitRate: number;
}

/**
 * Container-wide metrics
 */
export interface ContainerMetrics {
    readonly containerId: string;
    readonly totalServices: number;
    readonly totalResolutions: number;
    readonly averageResolutionTime: number;
    readonly serviceMetrics: Map<string, ServiceMetrics>;
    readonly createdAt: Date;
    readonly lastActivity: Date | null;
}

// ============================================================================
// DEBUGGING TYPES - Advanced Observability
// ============================================================================

/**
 * Debug information for troubleshooting
 */
export interface DebugInfo {
    readonly containerId: string;
    readonly registrationHistory: RegistrationEvent[];
    readonly resolutionHistory: ResolutionEvent[];
    readonly scopeHistory: ScopeEvent[];
    readonly errorHistory: ErrorEvent[];
}

/**
 * Service registration event
 */
export interface RegistrationEvent {
    readonly timestamp: Date;
    readonly serviceName: string;
    readonly scope: ServiceScope;
    readonly implementationName?: string;
    readonly metadata?: any;
}

/**
 * Service resolution event
 */
export interface ResolutionEvent {
    readonly timestamp: Date;
    readonly serviceName: string;
    readonly resolutionTime: number;
    readonly success: boolean;
    readonly fromCache: boolean;
    readonly resolverUsed: string;
    readonly context: ResolutionContext;
    readonly error?: Error;
}

/**
 * Scope lifecycle event
 */
export interface ScopeEvent {
    readonly timestamp: Date;
    readonly scopeId: string;
    readonly action: 'created' | 'disposed' | 'activated';
    readonly serviceCount?: number;
}

/**
 * Error event for debugging
 */
export interface ErrorEvent {
    readonly timestamp: Date;
    readonly error: Error;
    readonly context: ResolutionContext;
    readonly stackTrace: string;
}

// ============================================================================
// FACTORY TYPES - Advanced Instantiation Patterns
// ============================================================================

/**
 * Service factory function
 */
export type ServiceFactory<T> = (container: any) => T;

/**
 * Async service factory for complex initialization
 */
export type AsyncServiceFactory<T> = (container: any) => Promise<T>;

/**
 * Conditional service factory based on environment
 */
export type ConditionalServiceFactory<T> = {
    condition: (container: any) => boolean;
    factory: ServiceFactory<T>;
};

/**
 * Multi-implementation factory for strategy pattern
 */
export type MultiImplementationFactory<T> = {
    implementations: Map<string, ServiceFactory<T>>;
    selector: (container: any) => string;
};

// ============================================================================
// LIFECYCLE HOOKS - Advanced Service Management
// ============================================================================

/**
 * Service lifecycle hooks
 */
export interface ServiceLifecycleHooks<T = any> {
    onCreating?: (context: ResolutionContext) => void;
    onCreated?: (instance: T, context: ResolutionContext) => void;
    onResolving?: (context: ResolutionContext) => void;
    onResolved?: (instance: T, context: ResolutionContext) => void;
    onDisposing?: (instance: T) => void;
    onDisposed?: (instance: T) => void;
}

/**
 * Disposable service interface
 */
export interface IDisposable {
    dispose(): void | Promise<void>;
}

/**
 * Initializable service interface
 */
export interface IInitializable {
    initialize(): void | Promise<void>;
}

// ============================================================================
// CONFIGURATION TYPES - Environment-Specific Setup
// ============================================================================

/**
 * Container configuration options
 */
export interface ContainerConfiguration {
    readonly enableValidation: boolean;
    readonly enableDebugging: boolean;
    readonly enableMetrics: boolean;
    readonly maxResolutionDepth: number;
    readonly defaultScope: ServiceScope;
    readonly autoDisposeScopes: boolean;
    readonly strictMode: boolean;
    readonly environment: 'development' | 'test' | 'production';
}

/**
 * Application factory configuration
 */
export interface ApplicationFactoryConfiguration {
    readonly containerConfig: ContainerConfiguration;
    readonly serviceRegistrations: ServiceRegistrationConfig[];
    readonly middlewareConfig?: MiddlewareConfiguration;
    readonly loggingConfig?: LoggingConfiguration;
}

/**
 * Service registration configuration
 */
export interface ServiceRegistrationConfig {
    readonly serviceInterface: ServiceInterface;
    readonly implementation?: new (...args: any[]) => any;
    readonly factory?: ServiceFactory<any>;
    readonly instance?: any;
    readonly scope: ServiceScope;
    readonly condition?: (container: any) => boolean;
    readonly metadata?: ServiceMetadata;
}

/**
 * Middleware configuration for request/response processing
 */
export interface MiddlewareConfiguration {
    readonly enableRequestScoping: boolean;
    readonly enableSessionScoping: boolean;
    readonly enableComponentScoping: boolean;
    readonly requestTimeout: number;
    readonly sessionTimeout: number;
}

/**
 * Logging configuration for debugging
 */
export interface LoggingConfiguration {
    readonly level: 'debug' | 'info' | 'warn' | 'error';
    readonly enableConsoleLogging: boolean;
    readonly enableFileLogging: boolean;
    readonly enableRemoteLogging: boolean;
    readonly logFilePath?: string;
    readonly remoteEndpoint?: string;
}

// ============================================================================
// UTILITY TYPES - Advanced TypeScript Patterns
// ============================================================================

/**
 * Extract service type from interface
 */
export type ServiceType<T> = T extends ServiceInterface<infer U> ? U : never;

/**
 * Constructor type for service implementations
 */
export type Constructor<T = {}> = new (...args: any[]) => T;

/**
 * Abstract constructor type for base classes
 */
export type AbstractConstructor<T = {}> = abstract new (...args: any[]) => T;

/**
 * Mixin type for service composition
 */
export type Mixin<T extends Constructor> = (base: T) => T;

/**
 * Service provider type for dependency injection
 */
export type ServiceProvider<T> = {
    provide: ServiceInterface<T>;
    useClass?: Constructor<T>;
    useFactory?: ServiceFactory<T>;
    useValue?: T;
    scope?: ServiceScope;
};
