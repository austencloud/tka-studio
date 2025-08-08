/**
 * 🏭 TKA APPLICATION FACTORY
 *
 * Enterprise-grade application factory that creates different "flavors" of the application:
 * - Production: Full web UI with persistent storage
 * - Test: Mock services with in-memory storage
 * - Headless: Real logic without UI components
 * - Development: Enhanced debugging and hot-reload support
 *
 * Matches the sophistication of the desktop ApplicationFactory.
 */

import { ServiceContainer } from "./core/ServiceContainer.js";
import {
  ContainerConfiguration,
  ApplicationFactoryConfiguration,
} from "./core/types.js";
import { ServiceRegistrationManager } from "./ServiceRegistrationManager.js";
import { createServiceInterface } from "./core/types.js";
import { registerPictographServices } from "../pictograph/di/PictographServiceRegistration.js";

// ============================================================================
// SERVICE INTERFACES - Cross-Platform Compatibility
// ============================================================================

// Core Services
export const ISequenceDataService = createServiceInterface(
  "ISequenceDataService",
  class {}
);
export const ISettingsService = createServiceInterface(
  "ISettingsService",
  class {}
);
export const IValidationService = createServiceInterface(
  "IValidationService",
  class {}
);
export const ILayoutService = createServiceInterface(
  "ILayoutService",
  class {}
);

// Management Services
export const ISequenceManager = createServiceInterface(
  "ISequenceManager",
  class {}
);
export const IPictographManagementService = createServiceInterface(
  "IPictographManagementService",
  class {}
);
export const IUIStateManagementService = createServiceInterface(
  "IUIStateManagementService",
  class {}
);
export const IArrowManagementService = createServiceInterface(
  "IArrowManagementService",
  class {}
);

// Infrastructure Services
export const IFileSystemService = createServiceInterface(
  "IFileSystemService",
  class {}
);
export const ISessionStateService = createServiceInterface(
  "ISessionStateService",
  class {}
);
export const ILoggingService = createServiceInterface(
  "ILoggingService",
  class {}
);
export const IErrorHandlingService = createServiceInterface(
  "IErrorHandlingService",
  class {}
);

// Web-Specific Services
export const IStorageService = createServiceInterface(
  "IStorageService",
  class {}
);
export const INavigationService = createServiceInterface(
  "INavigationService",
  class {}
);
export const IThemeService = createServiceInterface("IThemeService", class {});
export const INotificationService = createServiceInterface(
  "INotificationService",
  class {}
);

/**
 * Main application factory for creating configured service containers
 */
export class ApplicationFactory {
  private static _logger?: any;

  // ============================================================================
  // PRODUCTION APPLICATION - Full Web UI with Persistence
  // ============================================================================

  /**
   * Create production application with full web UI and browser storage
   */
  static createProductionApp(): ServiceContainer {
    const container = new ServiceContainer("production");

    try {
      // Configure for production environment
      const config: ContainerConfiguration = {
        enableValidation: true,
        enableDebugging: false,
        enableMetrics: true,
        maxResolutionDepth: 50,
        defaultScope: "singleton" as any,
        autoDisposeScopes: true,
        strictMode: true,
        environment: "production",
      };

      // Register storage services (browser-based)
      this._registerStorageServices(container);

      // Register core business services
      this._registerCoreServices(container);

      // Register UI services
      this._registerUIServices(container);

      // Register web-specific services
      this._registerWebServices(container);

      // Register extracted services
      const registrationManager = new ServiceRegistrationManager();
      registrationManager.registerAllServices(container);

      // Register pictograph services
      registerPictographServices(container);

      this._log("info", "Created production application container");
      return container;
    } catch (error) {
      this._log("error", "Failed to create production application", error);
      throw error;
    }
  }

  // ============================================================================
  // TEST APPLICATION - Mock Services with In-Memory Storage
  // ============================================================================

  /**
   * Create test application with mock services and in-memory storage.
   * Perfect for automated testing - no UI, no persistence, fast execution.
   */
  static createTestApp(): ServiceContainer {
    const container = new ServiceContainer("test");

    try {
      // Configure for testing environment
      const config: ContainerConfiguration = {
        enableValidation: true,
        enableDebugging: true,
        enableMetrics: true,
        maxResolutionDepth: 25,
        defaultScope: "singleton" as any,
        autoDisposeScopes: true,
        strictMode: false,
        environment: "test",
      };

      // Register mock services
      this._registerMockServices(container);

      // Register test utilities
      this._registerTestUtilities(container);

      // Register pictograph services
      registerPictographServices(container);

      this._log("info", "Created test application container");
      return container;
    } catch (error) {
      this._log("error", "Failed to create test application", error);
      throw error;
    }
  }

  // ============================================================================
  // HEADLESS APPLICATION - Real Logic without UI
  // ============================================================================

  /**
   * Create headless application with real business logic but no UI.
   * Useful for server-side processing, API endpoints, or CI/CD environments.
   */
  static createHeadlessApp(): ServiceContainer {
    const container = new ServiceContainer("headless");

    try {
      // Configure for headless environment
      const config: ContainerConfiguration = {
        enableValidation: true,
        enableDebugging: false,
        enableMetrics: true,
        maxResolutionDepth: 50,
        defaultScope: "singleton" as any,
        autoDisposeScopes: true,
        strictMode: true,
        environment: "production",
      };

      // Register storage services (same as production)
      this._registerStorageServices(container);

      // Register real business logic services
      this._registerCoreServices(container);

      // Register headless UI services (no actual UI)
      this._registerHeadlessServices(container);

      // Register pictograph services
      registerPictographServices(container);

      this._log("info", "Created headless application container");
      return container;
    } catch (error) {
      this._log("error", "Failed to create headless application", error);
      throw error;
    }
  }

  // ============================================================================
  // DEVELOPMENT APPLICATION - Enhanced Debugging and Hot-Reload
  // ============================================================================

  /**
   * Create development application with enhanced debugging and development tools
   */
  static createDevelopmentApp(): ServiceContainer {
    const container = new ServiceContainer("development");

    try {
      // Configure for development environment
      const config: ContainerConfiguration = {
        enableValidation: true,
        enableDebugging: true,
        enableMetrics: true,
        maxResolutionDepth: 50,
        defaultScope: "singleton" as any,
        autoDisposeScopes: false, // Keep scopes for debugging
        strictMode: false,
        environment: "development",
      };

      // Register development storage services
      this._registerStorageServices(container);

      // Register core services with development enhancements
      this._registerCoreServices(container);

      // Register UI services with hot-reload support
      this._registerUIServices(container);

      // Register development tools
      this._registerDevelopmentTools(container);

      // Register pictograph services
      registerPictographServices(container);

      this._log("info", "Created development application container");
      return container;
    } catch (error) {
      this._log("error", "Failed to create development application", error);
      throw error;
    }
  }

  // ============================================================================
  // SERVICE REGISTRATION METHODS
  // ============================================================================

  private static _registerStorageServices(container: ServiceContainer): void {
    // Browser storage services
    container.registerSingleton(
      IStorageService,
      class BrowserStorageService {
        getItem(key: string): string | null {
          return localStorage.getItem(key);
        }
        setItem(key: string, value: string): void {
          localStorage.setItem(key, value);
        }
        removeItem(key: string): void {
          localStorage.removeItem(key);
        }
      }
    );

    container.registerSingleton(
      ISequenceDataService,
      class BrowserSequenceDataService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      ISettingsService,
      class BrowserSettingsService {
        // Implementation would go here
      }
    );
  }

  private static _registerCoreServices(container: ServiceContainer): void {
    container.registerSingleton(
      ISequenceManager,
      class SequenceManager {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      IPictographManagementService,
      class PictographManagementService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      IValidationService,
      class ValidationService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      IArrowManagementService,
      class ArrowManagementService {
        // Implementation would go here
      }
    );
  }

  private static _registerUIServices(container: ServiceContainer): void {
    container.registerSingleton(
      ILayoutService,
      class WebLayoutService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      IUIStateManagementService,
      class WebUIStateManagementService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      IThemeService,
      class ThemeService {
        // Implementation would go here
      }
    );
  }

  private static _registerWebServices(container: ServiceContainer): void {
    container.registerSingleton(
      INavigationService,
      class SvelteNavigationService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      INotificationService,
      class WebNotificationService {
        // Implementation would go here
      }
    );

    container.registerSingleton(
      ISessionStateService,
      class WebSessionStateService {
        // Implementation would go here
      }
    );
  }

  private static _registerMockServices(container: ServiceContainer): void {
    // Mock implementations for testing
    container.registerSingleton(
      ISequenceDataService,
      class MockSequenceDataService {
        private _sequences = new Map();

        async getSequence(id: string) {
          return this._sequences.get(id) || null;
        }

        async saveSequence(sequence: any) {
          this._sequences.set(sequence.id, sequence);
          return sequence;
        }
      }
    );

    container.registerSingleton(
      ISettingsService,
      class MockSettingsService {
        private _settings = new Map();

        getSetting(key: string) {
          return this._settings.get(key);
        }

        setSetting(key: string, value: any) {
          this._settings.set(key, value);
        }
      }
    );

    // Add more mock services as needed
  }

  private static _registerHeadlessServices(container: ServiceContainer): void {
    container.registerSingleton(
      ILayoutService,
      class HeadlessLayoutService {
        getMainWindowSize() {
          return { width: 1920, height: 1080 };
        }

        getWorkbenchSize() {
          return { width: 1440, height: 1080 };
        }
      }
    );

    container.registerSingleton(
      IUIStateManagementService,
      class HeadlessUIStateManagementService {
        // Headless implementation
      }
    );
  }

  private static _registerTestUtilities(container: ServiceContainer): void {
    container.registerSingleton(
      createServiceInterface("ITestHelper", class {}),
      class TestHelper {
        // Test utility methods
      }
    );
  }

  private static _registerDevelopmentTools(container: ServiceContainer): void {
    container.registerSingleton(
      createServiceInterface("IHotReloadService", class {}),
      class HotReloadService {
        // Hot reload functionality
      }
    );

    container.registerSingleton(
      createServiceInterface("IDevToolsService", class {}),
      class DevToolsService {
        // Development tools
      }
    );
  }

  // ============================================================================
  // UTILITIES
  // ============================================================================

  private static _log(level: string, message: string, error?: any): void {
    if (typeof console !== "undefined") {
      const timestamp = new Date().toISOString();
      const logMessage = `[${timestamp}] [ApplicationFactory] ${message}`;

      switch (level) {
        case "info":
          console.info(logMessage);
          break;
        case "warn":
          console.warn(logMessage);
          break;
        case "error":
          console.error(logMessage, error);
          break;
        default:
          console.log(logMessage);
      }
    }
  }
}
