/**
 * 🧪 RESOLVER CHAIN TESTS
 *
 * Comprehensive tests for the ResolverChain and individual resolvers,
 * ensuring robust service resolution with proper fallback strategies.
 */

import { describe, test, expect, beforeEach } from 'vitest';
import {
    ResolverChain,
    SingletonResolver,
    TransientResolver,
    ScopedResolver,
    FactoryResolver,
    InstanceResolver,
    FallbackResolver,
    ServiceRegistry,
    createServiceInterface,
    ServiceScope
} from '../../index.js';

describe('ResolverChain', () => {
    let resolverChain: ResolverChain;
    let registry: ServiceRegistry;

    beforeEach(() => {
        resolverChain = new ResolverChain();
        registry = new ServiceRegistry();
    });

    describe('Resolver Chain Management', () => {
        test('should have default resolvers in correct priority order', () => {
            const resolvers = resolverChain.getResolvers();

            expect(resolvers).toHaveLength(7);

            // Check priority order (highest first)
            const priorities = resolvers.map(r => r.priority);
            for (let i = 1; i < priorities.length; i++) {
                expect(priorities[i]).toBeLessThanOrEqual(priorities[i - 1]);
            }
        });

        test('should add custom resolver', () => {
            const customResolver = {
                name: 'CustomResolver',
                priority: 200,
                canResolve: () => false,
                resolve: () => null
            };

            resolverChain.addResolver(customResolver);
            const resolvers = resolverChain.getResolvers();

            expect(resolvers).toContain(customResolver);
            expect(resolvers[0]).toBe(customResolver); // Should be first due to highest priority
        });

        test('should remove resolver by name', () => {
            const initialCount = resolverChain.getResolvers().length;

            const removed = resolverChain.removeResolver('SingletonResolver');
            expect(removed).toBe(true);

            const resolvers = resolverChain.getResolvers();
            expect(resolvers).toHaveLength(initialCount - 1);
            expect(resolvers.find(r => r.name === 'SingletonResolver')).toBeUndefined();
        });

        test('should return false when removing non-existent resolver', () => {
            const removed = resolverChain.removeResolver('NonExistentResolver');
            expect(removed).toBe(false);
        });

        test('should get resolver by name', () => {
            const resolver = resolverChain.getResolver('SingletonResolver');
            expect(resolver).toBeDefined();
            expect(resolver?.name).toBe('SingletonResolver');
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

            registry.registerSingleton(ITestService, TestService);

            const context = createMockContext(ITestService);
            const mockContainer = createMockContainer(registry, resolverChain);

            const result = resolverChain.resolve(ITestService, registry, mockContainer, context);

            expect(result).toBeDefined();
            expect(result?.getValue()).toBe('singleton-value');
        });

        test('should resolve transient service', () => {
            const ITestService = createServiceInterface('ITestService', class {});
            class TestService {}

            registry.registerTransient(ITestService, TestService);

            const context = createMockContext(ITestService);
            const mockContainer = createMockContainer(registry, resolverChain);

            const result1 = resolverChain.resolve(ITestService, registry, mockContainer, context);
            const result2 = resolverChain.resolve(ITestService, registry, mockContainer, context);

            expect(result1).toBeDefined();
            expect(result2).toBeDefined();
            expect(result1).not.toBe(result2); // Different instances
        });

        test('should resolve factory service', () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            const factory = () => ({ getValue: () => 'factory-value' });
            registry.registerFactory(ITestService, factory, ServiceScope.Factory);

            const context = createMockContext(ITestService);
            const mockContainer = createMockContainer(registry, resolverChain);

            const result = resolverChain.resolve(ITestService, registry, mockContainer, context);

            expect(result).toBeDefined();
            expect(result?.getValue()).toBe('factory-value');
        });

        test('should resolve instance service', () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            const instance = { getValue: () => 'instance-value' };
            registry.registerInstance(ITestService, instance);

            const context = createMockContext(ITestService);
            const mockContainer = createMockContainer(registry, resolverChain);

            const result = resolverChain.resolve(ITestService, registry, mockContainer, context);

            expect(result).toBe(instance);
        });

        test('should return null for unregistered service', () => {
            const IUnregisteredService = createServiceInterface('IUnregisteredService', class {});

            const context = createMockContext(IUnregisteredService);
            const mockContainer = createMockContainer(registry, resolverChain);

            const result = resolverChain.resolve(IUnregisteredService, registry, mockContainer, context);

            expect(result).toBeNull();
        });
    });

    describe('Individual Resolvers', () => {
        describe('SingletonResolver', () => {
            let resolver: SingletonResolver;

            beforeEach(() => {
                resolver = new SingletonResolver();
            });

            test('should identify singleton services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                registry.registerSingleton(ITestService, class TestService {});

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should not identify non-singleton services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                registry.registerTransient(ITestService, class TestService {});

                expect(resolver.canResolve(ITestService, registry)).toBe(false);
            });

            test('should resolve singleton service', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                class TestService {}

                registry.registerSingleton(ITestService, TestService);

                const context = createMockContext(ITestService);
                const mockContainer = createMockContainer(registry, resolverChain);

                const result = resolver.resolve(ITestService, registry, mockContainer, context);

                expect(result).toBeInstanceOf(TestService);
            });

            test('should return cached singleton instance', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                class TestService {}

                registry.registerSingleton(ITestService, TestService);

                const context = createMockContext(ITestService);
                const mockContainer = createMockContainer(registry, resolverChain);

                const result1 = resolver.resolve(ITestService, registry, mockContainer, context);
                const result2 = resolver.resolve(ITestService, registry, mockContainer, context);

                expect(result1).toBe(result2);
            });
        });

        describe('TransientResolver', () => {
            let resolver: TransientResolver;

            beforeEach(() => {
                resolver = new TransientResolver();
            });

            test('should identify transient services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                registry.registerTransient(ITestService, class TestService {});

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should create new instances each time', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                class TestService {}

                registry.registerTransient(ITestService, TestService);

                const context = createMockContext(ITestService);
                const mockContainer = createMockContainer(registry, resolverChain);

                const result1 = resolver.resolve(ITestService, registry, mockContainer, context);
                const result2 = resolver.resolve(ITestService, registry, mockContainer, context);

                expect(result1).toBeInstanceOf(TestService);
                expect(result2).toBeInstanceOf(TestService);
                expect(result1).not.toBe(result2);
            });
        });

        describe('ScopedResolver', () => {
            let resolver: ScopedResolver;

            beforeEach(() => {
                resolver = new ScopedResolver();
            });

            test('should identify scoped services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                registry.registerScoped(ITestService, class TestService {}, ServiceScope.Scoped);

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should identify request scoped services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                registry.registerScoped(ITestService, class TestService {}, ServiceScope.Request);

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should resolve scoped service', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                class TestService {}

                registry.registerScoped(ITestService, TestService, ServiceScope.Scoped);

                const context = createMockContext(ITestService, 'test-scope');
                const mockContainer = createMockContainer(registry, resolverChain);

                const result = resolver.resolve(ITestService, registry, mockContainer, context);

                expect(result).toBeInstanceOf(TestService);
            });
        });

        describe('FactoryResolver', () => {
            let resolver: FactoryResolver;

            beforeEach(() => {
                resolver = new FactoryResolver();
            });

            test('should identify factory services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                const factory = () => ({ test: 'factory' });
                registry.registerFactory(ITestService, factory, ServiceScope.Factory);

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should resolve factory service', () => {
                const ITestService = createServiceInterface('ITestService', class {
                    getValue(): string { return ''; }
                });

                const factory = () => ({ getValue: () => 'factory-result' });
                registry.registerFactory(ITestService, factory, ServiceScope.Factory);

                const context = createMockContext(ITestService);
                const mockContainer = createMockContainer(registry, resolverChain);

                const result = resolver.resolve(ITestService, registry, mockContainer, context);

                expect(result?.getValue()).toBe('factory-result');
            });
        });

        describe('InstanceResolver', () => {
            let resolver: InstanceResolver;

            beforeEach(() => {
                resolver = new InstanceResolver();
            });

            test('should identify instance services', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                const instance = { test: 'instance' };
                registry.registerInstance(ITestService, instance);

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should resolve instance service', () => {
                const ITestService = createServiceInterface('ITestService', class {});
                const instance = { test: 'instance' };
                registry.registerInstance(ITestService, instance);

                const context = createMockContext(ITestService);
                const mockContainer = createMockContainer(registry, resolverChain);

                const result = resolver.resolve(ITestService, registry, mockContainer, context);

                expect(result).toBe(instance);
            });
        });

        describe('FallbackResolver', () => {
            let resolver: FallbackResolver;

            beforeEach(() => {
                resolver = new FallbackResolver();
            });

            test('should always claim it can resolve', () => {
                const ITestService = createServiceInterface('ITestService', class {});

                expect(resolver.canResolve(ITestService, registry)).toBe(true);
            });

            test('should attempt to create instance from interface type', () => {
                const ITestService = createServiceInterface('ITestService', class TestService {
                    getValue(): string { return 'fallback'; }
                });

                const context = createMockContext(ITestService);
                const mockContainer = createMockContainer(registry, resolverChain);

                const result = resolver.resolve(ITestService, registry, mockContainer, context);

                // Fallback resolver should attempt to create instance
                expect(result).toBeDefined();
            });
        });
    });
});

// Helper functions for creating mock objects
function createMockContext(serviceInterface: any, scopeId?: string) {
    return {
        serviceInterface,
        containerId: 'test-container',
        resolutionStack: [],
        resolutionDepth: 0,
        timestamp: new Date(),
        scopeId
    };
}

function createMockContainer(registry: ServiceRegistry, resolverChain: ResolverChain) {
    return {
        resolve: (serviceInterface: any) => {
            const context = createMockContext(serviceInterface);
            return resolverChain.resolve(serviceInterface, registry, this, context);
        }
    };
}
