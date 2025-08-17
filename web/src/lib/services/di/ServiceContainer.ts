/**
 * Simple Dependency Injection Container
 * Local implementation to replace missing @tka/shared/di/core modules
 */

import type { ServiceInterface, Factory } from "./types";

interface ServiceConfig {
  implementation: new (...args: unknown[]) => unknown;
  dependencies: string[];
}

export class ServiceContainer {
  private services = new Map<string, ServiceConfig>();
  private factories = new Map<string, Factory<unknown>>();
  private singletons = new Map<string, unknown>();

  constructor(public readonly name: string) {}

  register<T>(
    serviceInterface: ServiceInterface<T>,
    ...dependencies: ServiceInterface[]
  ): void {
    this.services.set(serviceInterface.token, {
      implementation: serviceInterface.implementation as new (
        ...args: unknown[]
      ) => unknown,
      dependencies: dependencies.map((dep) => dep.token),
    });
  }

  registerFactory<T>(
    serviceInterface: ServiceInterface<T>,
    factory: Factory<T>
  ): void {
    this.factories.set(serviceInterface.token, factory);
  }

  registerSingleton<T>(
    serviceInterface: ServiceInterface<T>,
    instance: T
  ): void {
    this.singletons.set(serviceInterface.token, instance);
  }

  registerSingletonClass<T>(serviceInterface: ServiceInterface<T>): void {
    console.log(`🔧 Registering singleton class: ${serviceInterface.token}`);
    const instance = new serviceInterface.implementation();
    this.singletons.set(serviceInterface.token, instance);
    console.log(`✅ Singleton registered: ${serviceInterface.token}`);
  }

  /**
   * Get debug information about registered services
   */
  getDebugInfo(): {
    singletons: string[];
    factories: string[];
    services: string[];
  } {
    return {
      singletons: Array.from(this.singletons.keys()),
      factories: Array.from(this.factories.keys()),
      services: Array.from(this.services.keys()),
    };
  }

  resolve<T>(serviceInterface: ServiceInterface<T>): T {
    const token = serviceInterface.token;
    console.log(`🔍 Resolving: ${token}`);

    // Check if it's a singleton
    if (this.singletons.has(token)) {
      console.log(`✅ Found singleton: ${token}`);
      return this.singletons.get(token) as T;
    }

    // Check if it's a factory
    if (this.factories.has(token)) {
      console.log(`🏭 Creating from factory: ${token}`);
      const factory = this.factories.get(token);
      if (!factory) {
        throw new Error(`Factory for ${token} is unexpectedly undefined`);
      }
      return factory() as T;
    }

    // Check if it's a registered service
    const serviceConfig = this.services.get(token);
    if (serviceConfig) {
      console.log(`🔨 Creating service: ${token}`);
      const { implementation, dependencies } = serviceConfig;
      console.log(`📦 Dependencies for ${token}:`, dependencies);

      const resolvedDependencies = dependencies.map((depToken: string) => {
        console.log(`🔗 Resolving dependency: ${depToken} for ${token}`);

        // Check singletons first
        if (this.singletons.has(depToken)) {
          console.log(`✅ Found singleton dependency: ${depToken}`);
          return this.singletons.get(depToken);
        }

        // Check factories
        if (this.factories.has(depToken)) {
          console.log(`🏭 Creating from factory dependency: ${depToken}`);
          const factory = this.factories.get(depToken);
          if (!factory) {
            throw new Error(
              `Factory for dependency ${depToken} is unexpectedly undefined`
            );
          }
          return factory();
        }

        // Check services
        const depServiceConfig = this.services.get(depToken);
        if (depServiceConfig) {
          console.log(`🔨 Creating service dependency: ${depToken}`);
          return this.resolve({
            token: depToken,
            implementation: depServiceConfig.implementation,
          });
        }

        // Dependency not found
        console.error(
          `❌ Available singletons:`,
          Array.from(this.singletons.keys())
        );
        console.error(
          `❌ Available factories:`,
          Array.from(this.factories.keys())
        );
        console.error(
          `❌ Available services:`,
          Array.from(this.services.keys())
        );
        throw new Error(`Dependency ${depToken} not found`);
      });

      return new implementation(...resolvedDependencies) as T;
    }

    console.error(`❌ Service not found: ${token}`);
    console.error(
      `❌ Available singletons:`,
      Array.from(this.singletons.keys())
    );
    console.error(`❌ Available factories:`, Array.from(this.factories.keys()));
    console.error(`❌ Available services:`, Array.from(this.services.keys()));
    throw new Error(`Service ${token} not registered`);
  }

  has(serviceInterface: ServiceInterface): boolean {
    return (
      this.services.has(serviceInterface.token) ||
      this.factories.has(serviceInterface.token) ||
      this.singletons.has(serviceInterface.token)
    );
  }

  clear(): void {
    this.services.clear();
    this.factories.clear();
    this.singletons.clear();
  }
}
