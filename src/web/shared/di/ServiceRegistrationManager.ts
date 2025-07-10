/**
 * 🔧 TKA SERVICE REGISTRATION MANAGER
 *
 * Sophisticated service registration orchestrator that manages the registration
 * of all application services in the correct dependency order.
 */

import { ServiceContainer } from "./core/ServiceContainer.js";
import { createServiceInterface } from "./core/types.js";

export class ServiceRegistrationManager {
  private _progressCallback?: (message: string) => void;

  constructor(progressCallback?: (message: string) => void) {
    this._progressCallback = progressCallback;
  }

  /**
   * Register all application services in the DI container
   */
  registerAllServices(container: ServiceContainer): void {
    this._updateProgress("Configuring services...");

    try {
      // Register services in dependency order
      this.registerCoreServices(container);
      this.registerDataServices(container);
      this.registerBusinessServices(container);
      this.registerUIServices(container);
      this.registerWebServices(container);
      this.registerUtilityServices(container);

      this._updateProgress("Services configured successfully");
    } catch (error) {
      this._updateProgress(`Service configuration failed: ${error}`);
      throw error;
    }
  }

  /**
   * Register core foundational services
   */
  registerCoreServices(container: ServiceContainer): void {
    this._updateProgress("Registering core services...");

    // Logging service (foundational)
    const ILoggingService = createServiceInterface(
      "ILoggingService",
      class {
        log(level: string, message: string, ...args: any[]): void {}
        debug(message: string, ...args: any[]): void {}
        info(message: string, ...args: any[]): void {}
        warn(message: string, ...args: any[]): void {}
        error(message: string, ...args: any[]): void {}
      }
    );

    container.registerSingleton(
      ILoggingService,
      class ConsoleLoggingService {
        log(level: string, message: string, ...args: any[]): void {
          console.log(`[${level.toUpperCase()}] ${message}`, ...args);
        }
        debug(message: string, ...args: any[]): void {
          console.debug(message, ...args);
        }
        info(message: string, ...args: any[]): void {
          console.info(message, ...args);
        }
        warn(message: string, ...args: any[]): void {
          console.warn(message, ...args);
        }
        error(message: string, ...args: any[]): void {
          console.error(message, ...args);
        }
      }
    );

    // Error handling service
    const IErrorHandlingService = createServiceInterface(
      "IErrorHandlingService",
      class {
        handleError(error: Error, context?: any): void {}
        reportError(error: Error, context?: any): void {}
      }
    );

    container.registerSingleton(
      IErrorHandlingService,
      class ErrorHandlingService {
        handleError(error: Error, context?: any): void {
          console.error("Application error:", error, context);
          // In production, this would send to error reporting service
        }
        reportError(error: Error, context?: any): void {
          this.handleError(error, context);
        }
      }
    );

    // Configuration service
    const IConfigurationService = createServiceInterface(
      "IConfigurationService",
      class {
        get(key: string): any {}
        set(key: string, value: any): void {}
        getEnvironment(): string {}
      }
    );

    container.registerSingleton(
      IConfigurationService,
      class ConfigurationService {
        private _config = new Map<string, any>();

        constructor() {
          // Load default configuration
          this._config.set("environment", this._detectEnvironment());
          this._config.set("debug", this._isDebugMode());
          this._config.set("apiBaseUrl", this._getApiBaseUrl());
        }

        get(key: string): any {
          return this._config.get(key);
        }

        set(key: string, value: any): void {
          this._config.set(key, value);
        }

        getEnvironment(): string {
          return this._config.get("environment") || "production";
        }

        private _detectEnvironment(): string {
          if (typeof window !== "undefined") {
            if (
              window.location.hostname === "localhost" ||
              window.location.hostname === "127.0.0.1"
            ) {
              return "development";
            }
          }
          return "production";
        }

        private _isDebugMode(): boolean {
          return this._detectEnvironment() === "development";
        }

        private _getApiBaseUrl(): string {
          const env = this._detectEnvironment();
          return env === "development" ? "http://localhost:8000" : "/api";
        }
      }
    );
  }

  /**
   * Register data access services
   */
  registerDataServices(container: ServiceContainer): void {
    this._updateProgress("Registering data services...");

    // Storage service
    const IStorageService = createServiceInterface(
      "IStorageService",
      class {
        getItem(key: string): string | null {
          return null;
        }
        setItem(key: string, value: string): void {}
        removeItem(key: string): void {}
        clear(): void {}
      }
    );

    container.registerSingleton(
      IStorageService,
      class BrowserStorageService {
        getItem(key: string): string | null {
          try {
            return localStorage.getItem(key);
          } catch {
            return null;
          }
        }

        setItem(key: string, value: string): void {
          try {
            localStorage.setItem(key, value);
          } catch (error) {
            console.warn("Failed to save to localStorage:", error);
          }
        }

        removeItem(key: string): void {
          try {
            localStorage.removeItem(key);
          } catch (error) {
            console.warn("Failed to remove from localStorage:", error);
          }
        }

        clear(): void {
          try {
            localStorage.clear();
          } catch (error) {
            console.warn("Failed to clear localStorage:", error);
          }
        }
      }
    );

    // Sequence data service
    const ISequenceDataService = createServiceInterface(
      "ISequenceDataService",
      class {
        async getSequence(id: string): Promise<any> {
          return null;
        }
        async saveSequence(sequence: any): Promise<any> {
          return sequence;
        }
        async deleteSequence(id: string): Promise<boolean> {
          return false;
        }
        async listSequences(): Promise<any[]> {
          return [];
        }
      }
    );

    container.registerSingleton(
      ISequenceDataService,
      class BrowserSequenceDataService {
        constructor(private storageService: any) {}

        async getSequence(id: string): Promise<any> {
          const data = this.storageService.getItem(`sequence_${id}`);
          return data ? JSON.parse(data) : null;
        }

        async saveSequence(sequence: any): Promise<any> {
          this.storageService.setItem(
            `sequence_${sequence.id}`,
            JSON.stringify(sequence)
          );
          return sequence;
        }

        async deleteSequence(id: string): Promise<boolean> {
          this.storageService.removeItem(`sequence_${id}`);
          return true;
        }

        async listSequences(): Promise<any[]> {
          // In a real implementation, this would scan localStorage for sequence keys
          return [];
        }
      }
    );
  }

  /**
   * Register business logic services
   */
  registerBusinessServices(container: ServiceContainer): void {
    this._updateProgress("Registering business services...");

    // Sequence management service
    const ISequenceManager = createServiceInterface(
      "ISequenceManager",
      class {
        async createSequence(name: string, length: number): Promise<any> {
          return null;
        }
        async updateSequence(id: string, data: any): Promise<any> {
          return null;
        }
        async deleteSequence(id: string): Promise<boolean> {
          return false;
        }
      }
    );

    container.registerSingleton(
      ISequenceManager,
      class SequenceManager {
        constructor(private dataService: any) {}

        async createSequence(name: string, length: number): Promise<any> {
          const sequence = {
            id: this._generateId(),
            name,
            length,
            beats: [],
            createdAt: new Date(),
            updatedAt: new Date(),
          };
          return await this.dataService.saveSequence(sequence);
        }

        async updateSequence(id: string, data: any): Promise<any> {
          const existing = await this.dataService.getSequence(id);
          if (!existing) throw new Error(`Sequence ${id} not found`);

          const updated = { ...existing, ...data, updatedAt: new Date() };
          return await this.dataService.saveSequence(updated);
        }

        async deleteSequence(id: string): Promise<boolean> {
          return await this.dataService.deleteSequence(id);
        }

        private _generateId(): string {
          return `seq_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        }
      }
    );

    // Validation service
    const IValidationService = createServiceInterface(
      "IValidationService",
      class {
        validateSequence(sequence: any): {
          isValid: boolean;
          errors: string[];
        } {
          return { isValid: true, errors: [] };
        }
      }
    );

    container.registerSingleton(
      IValidationService,
      class ValidationService {
        validateSequence(sequence: any): {
          isValid: boolean;
          errors: string[];
        } {
          const errors: string[] = [];

          if (!sequence.name || sequence.name.trim() === "") {
            errors.push("Sequence name is required");
          }

          if (!sequence.length || sequence.length < 1) {
            errors.push("Sequence must have at least 1 beat");
          }

          return { isValid: errors.length === 0, errors };
        }
      }
    );
  }

  /**
   * Register UI services
   */
  registerUIServices(container: ServiceContainer): void {
    this._updateProgress("Registering UI services...");

    // Theme service
    const IThemeService = createServiceInterface(
      "IThemeService",
      class {
        getCurrentTheme(): string {
          return "default";
        }
        setTheme(theme: string): void {}
        getAvailableThemes(): string[] {
          return [];
        }
      }
    );

    container.registerSingleton(
      IThemeService,
      class ThemeService {
        private _currentTheme = "default";

        getCurrentTheme(): string {
          return this._currentTheme;
        }

        setTheme(theme: string): void {
          this._currentTheme = theme;
          document.documentElement.setAttribute("data-theme", theme);
        }

        getAvailableThemes(): string[] {
          return ["default", "dark", "light", "blue", "green"];
        }
      }
    );

    // Notification service
    const INotificationService = createServiceInterface(
      "INotificationService",
      class {
        showSuccess(message: string): void {}
        showError(message: string): void {}
        showWarning(message: string): void {}
        showInfo(message: string): void {}
      }
    );

    container.registerSingleton(
      INotificationService,
      class NotificationService {
        showSuccess(message: string): void {
          this._showNotification(message, "success");
        }

        showError(message: string): void {
          this._showNotification(message, "error");
        }

        showWarning(message: string): void {
          this._showNotification(message, "warning");
        }

        showInfo(message: string): void {
          this._showNotification(message, "info");
        }

        private _showNotification(message: string, type: string): void {
          // In a real implementation, this would integrate with a toast/notification system
          console.log(`[${type.toUpperCase()}] ${message}`);
        }
      }
    );
  }

  /**
   * Register web-specific services
   */
  registerWebServices(container: ServiceContainer): void {
    this._updateProgress("Registering web services...");

    // Navigation service
    const INavigationService = createServiceInterface(
      "INavigationService",
      class {
        navigate(path: string): void {}
        goBack(): void {}
        getCurrentPath(): string {
          return "/";
        }
      }
    );

    container.registerSingleton(
      INavigationService,
      class SvelteNavigationService {
        navigate(path: string): void {
          if (typeof window !== "undefined") {
            window.history.pushState({}, "", path);
          }
        }

        goBack(): void {
          if (typeof window !== "undefined") {
            window.history.back();
          }
        }

        getCurrentPath(): string {
          if (typeof window !== "undefined") {
            return window.location.pathname;
          }
          return "/";
        }
      }
    );
  }

  /**
   * Register utility services
   */
  registerUtilityServices(container: ServiceContainer): void {
    this._updateProgress("Registering utility services...");

    // ID generator service
    const IIdGeneratorService = createServiceInterface(
      "IIdGeneratorService",
      class {
        generateId(): string {
          return "";
        }
        generateUuid(): string {
          return "";
        }
      }
    );

    container.registerTransient(
      IIdGeneratorService,
      class IdGeneratorService {
        generateId(): string {
          return `id_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
        }

        generateUuid(): string {
          if (typeof crypto !== "undefined" && crypto.randomUUID) {
            return crypto.randomUUID();
          }
          // Fallback UUID generation
          return "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx".replace(
            /[xy]/g,
            (c) => {
              const r = (Math.random() * 16) | 0;
              const v = c === "x" ? r : (r & 0x3) | 0x8;
              return v.toString(16);
            }
          );
        }
      }
    );
  }

  private _updateProgress(message: string): void {
    if (this._progressCallback) {
      this._progressCallback(message);
    }
  }
}
