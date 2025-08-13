/**
 * Simple Dependency Injection Container
 * Local implementation to replace missing @tka/shared/di/core modules
 */

export interface ServiceInterface<T = unknown> {
  token: string;
  implementation: new (...args: unknown[]) => T;
}

export function createServiceInterface<T>(
  token: string,
  implementation: new (...args: unknown[]) => T,
): ServiceInterface<T> {
  return { token, implementation };
}

export type Factory<T> = () => T;

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
    factory: Factory<T>,
  ): void {
    this.factories.set(serviceInterface.token, factory);
  }

  registerSingleton<T>(
    serviceInterface: ServiceInterface<T>,
    instance: T,
  ): void {
    this.singletons.set(serviceInterface.token, instance);
  }

  registerSingletonClass<T>(serviceInterface: ServiceInterface<T>): void {
    const instance = new serviceInterface.implementation();
    this.singletons.set(serviceInterface.token, instance);
  }

  resolve<T>(serviceInterface: ServiceInterface<T>): T {
    const token = serviceInterface.token;

    // Check if it's a singleton
    if (this.singletons.has(token)) {
      return this.singletons.get(token) as T;
    }

    // Check if it's a factory
    if (this.factories.has(token)) {
      const factory = this.factories.get(token);
      if (!factory) {
        throw new Error(`Factory for ${token} is unexpectedly undefined`);
      }
      return factory() as T;
    }

    // Check if it's a registered service
    const serviceConfig = this.services.get(token);
    if (serviceConfig) {
      const { implementation, dependencies } = serviceConfig;
      const resolvedDependencies = dependencies.map((depToken: string) => {
        const depServiceConfig = this.services.get(depToken);
        if (!depServiceConfig) {
          throw new Error(`Dependency ${depToken} not found`);
        }
        return this.resolve({
          token: depToken,
          implementation: depServiceConfig.implementation,
        });
      });

      return new implementation(...resolvedDependencies) as T;
    }

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
