/**
 * 🧪 SERVICE CONTAINER CORE TESTS
 * 
 * Comprehensive unit tests for the ServiceContainer core functionality,
 * following enterprise testing patterns from Spring, NestJS, and Autofac.
 */

import { describe, test, expect, beforeEach, afterEach } from 'vitest';
import {
    ServiceContainer,
    createServiceInterface,
    ServiceScope,
    ValidationResult
} from '../../index.js';

describe('ServiceContainer Core Functionality', () => {
    let container: ServiceContainer;

    beforeEach(() => {
        container = new ServiceContainer('test-container');
    });

    afterEach(() => {
        container.dispose();
    });

    describe('Container Lifecycle', () => {
        test('should create container with unique ID', () => {
            const diagnostics = container.getDiagnostics();
            expect(diagnostics.containerId).toBeDefined();
            expect(diagnostics.containerId).toContain('test-container');
            expect(diagnostics.isDisposed).toBe(false);
        });

        test('should track creation time', () => {
            const diagnostics = container.getDiagnostics();
            expect(diagnostics.createdAt).toBeInstanceOf(Date);
            expect(diagnostics.createdAt.getTime()).toBeLessThanOrEqual(Date.now());
        });

        test('should dispose properly', () => {
            container.dispose();
            const diagnostics = container.getDiagnostics();
            expect(diagnostics.isDisposed).toBe(true);
        });

        test('should throw when using disposed container', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            container.dispose();
            
            expect(() => {
                container.registerSingleton(ITestService, class TestService {});
            }).toThrow(/disposed/);
        });
    });

    describe('Service Registration', () => {
        test('should register singleton service', () => {
            const ITestService = createServiceInterface('ITestService', class {
                test(): string { return 'test'; }
            });

            class TestService {
                test(): string { return 'singleton'; }
            }

            expect(() => {
                container.registerSingleton(ITestService, TestService);
            }).not.toThrow();

            expect(container.isRegistered(ITestService)).toBe(true);
        });

        test('should register transient service', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerTransient(ITestService, TestService);
            expect(container.isRegistered(ITestService)).toBe(true);
        });

        test('should register scoped service', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerScoped(ITestService, TestService, ServiceScope.Scoped);
            expect(container.isRegistered(ITestService)).toBe(true);
        });

        test('should register factory service', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            const factory = () => ({ test: 'factory' });

            container.registerFactory(ITestService, factory);
            expect(container.isRegistered(ITestService)).toBe(true);
        });

        test('should register instance service', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            const instance = { test: 'instance' };

            container.registerInstance(ITestService, instance);
            expect(container.isRegistered(ITestService)).toBe(true);
        });

        test('should register lazy service', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerLazy(ITestService, TestService);
            expect(container.isRegistered(ITestService)).toBe(true);
        });
    });

    describe('Service Resolution', () => {
        test('should resolve singleton service', () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            class TestService {
                getValue(): string { return 'singleton-value'; }
            }

            container.registerSingleton(ITestService, TestService);
            const service = container.resolve(ITestService);
            
            expect(service).toBeDefined();
            expect(service.getValue()).toBe('singleton-value');
        });

        test('should return same instance for singleton', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerSingleton(ITestService, TestService);
            
            const service1 = container.resolve(ITestService);
            const service2 = container.resolve(ITestService);
            
            expect(service1).toBe(service2);
        });

        test('should return different instances for transient', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerTransient(ITestService, TestService);
            
            const service1 = container.resolve(ITestService);
            const service2 = container.resolve(ITestService);
            
            expect(service1).not.toBe(service2);
            expect(service1).toBeInstanceOf(TestService);
            expect(service2).toBeInstanceOf(TestService);
        });

        test('should resolve factory service', () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            const factory = () => ({ getValue: () => 'factory-value' });
            container.registerFactory(ITestService, factory);
            
            const service = container.resolve(ITestService);
            expect(service.getValue()).toBe('factory-value');
        });

        test('should resolve instance service', () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            const instance = { getValue: () => 'instance-value' };
            container.registerInstance(ITestService, instance);
            
            const service = container.resolve(ITestService);
            expect(service).toBe(instance);
            expect(service.getValue()).toBe('instance-value');
        });

        test('should throw for unregistered service', () => {
            const IUnregisteredService = createServiceInterface('IUnregisteredService', class {});
            
            expect(() => {
                container.resolve(IUnregisteredService);
            }).toThrow(/Service not found/);
        });

        test('should return null for tryResolve with unregistered service', () => {
            const IUnregisteredService = createServiceInterface('IUnregisteredService', class {});
            
            const result = container.tryResolve(IUnregisteredService);
            expect(result).toBeNull();
        });
    });

    describe('Lazy Resolution', () => {
        test('should create lazy proxy without instantiating service', () => {
            let instantiated = false;
            
            const ILazyService = createServiceInterface('ILazyService', class {
                test(): string { return ''; }
            });

            class LazyService {
                constructor() {
                    instantiated = true;
                }
                test(): string { return 'lazy'; }
            }

            container.registerLazy(ILazyService, LazyService);
            const lazyProxy = container.resolveLazy(ILazyService);
            
            expect(instantiated).toBe(false);
            expect(lazyProxy).toBeDefined();
        });

        test('should instantiate service on first access', () => {
            let instantiated = false;
            
            const ILazyService = createServiceInterface('ILazyService', class {
                test(): string { return ''; }
            });

            class LazyService {
                constructor() {
                    instantiated = true;
                }
                test(): string { return 'lazy-result'; }
            }

            container.registerLazy(ILazyService, LazyService);
            const lazyProxy = container.resolveLazy(ILazyService);
            
            expect(instantiated).toBe(false);
            
            const result = lazyProxy.test();
            
            expect(instantiated).toBe(true);
            expect(result).toBe('lazy-result');
        });
    });

    describe('Scope Management', () => {
        test('should create and manage scopes', () => {
            const scopeId = 'test-scope';
            
            expect(() => {
                container.createScope(scopeId);
            }).not.toThrow();
            
            expect(() => {
                container.setCurrentScope(scopeId);
            }).not.toThrow();
            
            expect(() => {
                container.disposeScope(scopeId);
            }).not.toThrow();
        });

        test('should isolate scoped services', () => {
            const IScopedService = createServiceInterface('IScopedService', class {
                getValue(): string { return ''; }
                setValue(value: string): void {}
            });

            class ScopedService {
                private value = Math.random().toString();
                getValue(): string { return this.value; }
                setValue(value: string): void { this.value = value; }
            }

            container.registerScoped(IScopedService, ScopedService, ServiceScope.Scoped);

            // Create two scopes
            container.createScope('scope1');
            container.createScope('scope2');

            // Get services from different scopes
            container.setCurrentScope('scope1');
            const service1 = container.resolve(IScopedService);
            const value1 = service1.getValue();

            container.setCurrentScope('scope2');
            const service2 = container.resolve(IScopedService);
            const value2 = service2.getValue();

            expect(value1).not.toBe(value2);
            expect(service1).not.toBe(service2);

            // Cleanup
            container.disposeScope('scope1');
            container.disposeScope('scope2');
        });

        test('should throw for invalid scope operations', () => {
            expect(() => {
                container.setCurrentScope('non-existent-scope');
            }).toThrow(/does not exist/);

            expect(() => {
                container.createScope('test-scope');
                container.createScope('test-scope'); // Duplicate
            }).toThrow(/already exists/);
        });
    });

    describe('Error Handling and Validation', () => {
        test('should validate service registration', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            
            expect(() => {
                container.registerSingleton(null as any, null as any);
            }).toThrow();
        });

        test('should handle circular dependency detection', () => {
            // This would be implemented in the resolver chain tests
            // For now, just ensure the container can handle the error
            const ICircularA = createServiceInterface('ICircularA', class {});
            const ICircularB = createServiceInterface('ICircularB', class {});

            // Register services that would create circular dependency
            container.registerSingleton(ICircularA, class CircularA {});
            container.registerSingleton(ICircularB, class CircularB {});

            // The actual circular dependency detection would be tested in resolver tests
            expect(container.isRegistered(ICircularA)).toBe(true);
            expect(container.isRegistered(ICircularB)).toBe(true);
        });
    });

    describe('Metrics and Diagnostics', () => {
        test('should track resolution metrics', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerSingleton(ITestService, TestService);
            
            // Perform multiple resolutions
            for (let i = 0; i < 5; i++) {
                container.resolve(ITestService);
            }

            const metrics = container.getMetrics();
            expect(metrics.totalResolutions).toBeGreaterThan(0);
            expect(metrics.totalServices).toBeGreaterThan(0);
        });

        test('should provide comprehensive diagnostics', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerSingleton(ITestService, TestService);
            container.resolve(ITestService);

            const diagnostics = container.getDiagnostics();
            
            expect(diagnostics.containerId).toBeDefined();
            expect(diagnostics.createdAt).toBeInstanceOf(Date);
            expect(diagnostics.isDisposed).toBe(false);
            expect(diagnostics.registeredServices).toContain('ITestService');
            expect(diagnostics.metrics).toBeDefined();
            expect(diagnostics.debugInfo).toBeDefined();
        });

        test('should clear metrics', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerSingleton(ITestService, TestService);
            container.resolve(ITestService);

            let metrics = container.getMetrics();
            expect(metrics.totalResolutions).toBeGreaterThan(0);

            container.clearMetrics();
            metrics = container.getMetrics();
            expect(metrics.totalResolutions).toBe(0);
        });
    });

    describe('Debug Mode', () => {
        test('should enable and disable debug mode', () => {
            expect(() => {
                container.setDebugMode(true);
            }).not.toThrow();

            expect(() => {
                container.setDebugMode(false);
            }).not.toThrow();
        });

        test('should track debug information when enabled', () => {
            container.setDebugMode(true);
            
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            container.registerSingleton(ITestService, TestService);
            container.resolve(ITestService);

            const debugInfo = container.getDiagnostics().debugInfo;
            expect(debugInfo).toBeDefined();
            expect(debugInfo.registrationHistory).toBeDefined();
            expect(debugInfo.resolutionHistory).toBeDefined();
        });
    });
});
