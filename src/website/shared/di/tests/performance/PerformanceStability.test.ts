/**
 * 🧪 PERFORMANCE AND STABILITY TESTS
 *
 * Comprehensive performance benchmarks and stability tests to ensure
 * the DI system performs well under various load conditions.
 */

import { describe, test, expect, beforeEach, afterEach } from 'vitest';
import {
    ServiceContainer,
    ApplicationFactory,
    createServiceInterface,
    ServiceScope
} from '../../index.js';

describe('Performance and Stability Tests', () => {
    let container: ServiceContainer;

    beforeEach(() => {
        container = new ServiceContainer('performance-test');
    });

    afterEach(() => {
        container.dispose();
    });

    describe('Resolution Performance', () => {
        test('should resolve singleton services quickly', async () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            class TestService {
                getValue(): string { return 'test-value'; }
            }

            container.registerSingleton(ITestService, TestService);

            const iterations = 1000;
            const startTime = performance.now();

            for (let i = 0; i < iterations; i++) {
                const service = container.resolve(ITestService);
                expect(service.getValue()).toBe('test-value');
            }

            const endTime = performance.now();
            const totalTime = endTime - startTime;
            const averageTime = totalTime / iterations;

            console.log(`Singleton resolution: ${averageTime.toFixed(3)}ms average over ${iterations} iterations`);

            // Should resolve in less than 1ms on average
            expect(averageTime).toBeLessThan(1);
        });

        test('should resolve transient services efficiently', async () => {
            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            class TestService {
                getValue(): string { return 'transient-value'; }
            }

            container.registerTransient(ITestService, TestService);

            const iterations = 1000;
            const startTime = performance.now();

            for (let i = 0; i < iterations; i++) {
                const service = container.resolve(ITestService);
                expect(service.getValue()).toBe('transient-value');
            }

            const endTime = performance.now();
            const totalTime = endTime - startTime;
            const averageTime = totalTime / iterations;

            console.log(`Transient resolution: ${averageTime.toFixed(3)}ms average over ${iterations} iterations`);

            // Transient should be reasonably fast (less than 2ms on average)
            expect(averageTime).toBeLessThan(2);
        });

        test('should handle complex dependency chains efficiently', async () => {
            // Create a chain of dependencies: A -> B -> C -> D -> E
            const interfaces = [];
            for (let i = 0; i < 5; i++) {
                const serviceName = `IChainService${String.fromCharCode(65 + i)}`;
                interfaces.push(createServiceInterface(serviceName, class {
                    getValue(): string { return ''; }
                }));
            }

            // Register the leaf service (E)
            container.registerSingleton(interfaces[4], class ChainServiceE {
                getValue(): string { return 'E'; }
            });

            // Register the chain
            for (let i = 3; i >= 0; i--) {
                const currentInterface = interfaces[i];
                const nextInterface = interfaces[i + 1];
                const serviceName = String.fromCharCode(65 + i);

                container.registerFactory(currentInterface, () => {
                    const dependency = container.resolve(nextInterface);
                    return {
                        getValue: () => `${serviceName}->${dependency.getValue()}`
                    };
                });
            }

            const iterations = 100;
            const startTime = performance.now();

            for (let i = 0; i < iterations; i++) {
                const service = container.resolve(interfaces[0]);
                expect(service.getValue()).toBe('A->B->C->D->E');
            }

            const endTime = performance.now();
            const totalTime = endTime - startTime;
            const averageTime = totalTime / iterations;

            console.log(`Complex chain resolution: ${averageTime.toFixed(3)}ms average over ${iterations} iterations`);

            // Complex chains should still be reasonably fast
            expect(averageTime).toBeLessThan(5);
        });
    });

    describe('Memory Management', () => {
        test('should not leak memory with transient services', async () => {
            const ITransientService = createServiceInterface('ITransientService', class {
                getValue(): string { return ''; }
            });

            class TransientService {
                private data = new Array(1000).fill('memory-test'); // Some memory usage
                getValue(): string { return 'transient'; }
            }

            container.registerTransient(ITransientService, TransientService);

            const initialMemory = (performance as any).memory?.usedJSHeapSize || 0;

            // Create many transient instances
            for (let i = 0; i < 1000; i++) {
                const service = container.resolve(ITransientService);
                expect(service.getValue()).toBe('transient');
            }

            // Force garbage collection if available
            if (global.gc) {
                global.gc();
            }

            const finalMemory = (performance as any).memory?.usedJSHeapSize || 0;

            // Memory should not grow excessively (allowing for some variance)
            if (initialMemory > 0 && finalMemory > 0) {
                const memoryGrowth = finalMemory - initialMemory;
                console.log(`Memory growth: ${(memoryGrowth / 1024 / 1024).toFixed(2)}MB`);

                // Should not grow more than 50MB
                expect(memoryGrowth).toBeLessThan(50 * 1024 * 1024);
            }
        });

        test('should properly dispose scoped services', async () => {
            let disposedCount = 0;

            const IScopedService = createServiceInterface('IScopedService', class {
                getValue(): string { return ''; }
            });

            class ScopedService {
                getValue(): string { return 'scoped'; }
                dispose(): void { disposedCount++; }
            }

            container.registerScoped(IScopedService, ScopedService, ServiceScope.Scoped);

            // Create multiple scopes and services
            for (let i = 0; i < 10; i++) {
                const scopeId = `scope-${i}`;
                container.createScope(scopeId);
                container.setCurrentScope(scopeId);

                const service = container.resolve(IScopedService);
                expect(service.getValue()).toBe('scoped');

                container.disposeScope(scopeId);
            }

            // All services should have been disposed
            expect(disposedCount).toBe(10);
        });
    });

    describe('Concurrent Access', () => {
        test('should handle concurrent singleton resolution', async () => {
            let constructorCallCount = 0;

            const ISingletonService = createServiceInterface('ISingletonService', class {
                getValue(): string { return ''; }
            });

            class SingletonService {
                constructor() {
                    constructorCallCount++;
                }
                getValue(): string { return 'singleton'; }
            }

            container.registerSingleton(ISingletonService, SingletonService);

            // Simulate concurrent access
            const promises = [];
            for (let i = 0; i < 100; i++) {
                promises.push(Promise.resolve().then(() => {
                    const service = container.resolve(ISingletonService);
                    return service.getValue();
                }));
            }

            const results = await Promise.all(promises);

            // All should return the same value
            expect(results.every(r => r === 'singleton')).toBe(true);

            // Constructor should only be called once
            expect(constructorCallCount).toBe(1);
        });

        test('should handle concurrent transient resolution', async () => {
            let constructorCallCount = 0;

            const ITransientService = createServiceInterface('ITransientService', class {
                getId(): number { return 0; }
            });

            class TransientService {
                private id: number;

                constructor() {
                    this.id = ++constructorCallCount;
                }

                getId(): number { return this.id; }
            }

            container.registerTransient(ITransientService, TransientService);

            // Simulate concurrent access
            const promises = [];
            for (let i = 0; i < 100; i++) {
                promises.push(Promise.resolve().then(() => {
                    const service = container.resolve(ITransientService);
                    return service.getId();
                }));
            }

            const results = await Promise.all(promises);

            // All should have unique IDs
            const uniqueIds = new Set(results);
            expect(uniqueIds.size).toBe(100);

            // Constructor should be called 100 times
            expect(constructorCallCount).toBe(100);
        });
    });

    describe('Stress Testing', () => {
        test('should handle high-volume service registration', async () => {
            const serviceCount = 1000;
            const interfaces = [];

            const startTime = performance.now();

            // Register many services
            for (let i = 0; i < serviceCount; i++) {
                const serviceName = `IStressService${i}`;
                const serviceInterface = createServiceInterface(serviceName, class {
                    getValue(): string { return ''; }
                });

                interfaces.push(serviceInterface);

                container.registerSingleton(serviceInterface, class {
                    getValue(): string { return `service-${i}`; }
                });
            }

            const registrationTime = performance.now() - startTime;
            console.log(`Registered ${serviceCount} services in ${registrationTime.toFixed(2)}ms`);

            // Verify all services are registered
            expect(interfaces.every(i => container.isRegistered(i))).toBe(true);

            // Registration should be reasonably fast
            expect(registrationTime).toBeLessThan(1000); // Less than 1 second
        });

        test('should handle high-volume service resolution', async () => {
            const IStressService = createServiceInterface('IStressService', class {
                getValue(): string { return ''; }
            });

            container.registerSingleton(IStressService, class StressService {
                getValue(): string { return 'stress-test'; }
            });

            const resolutionCount = 10000;
            const startTime = performance.now();

            for (let i = 0; i < resolutionCount; i++) {
                const service = container.resolve(IStressService);
                expect(service.getValue()).toBe('stress-test');
            }

            const resolutionTime = performance.now() - startTime;
            const averageTime = resolutionTime / resolutionCount;

            console.log(`Resolved ${resolutionCount} services in ${resolutionTime.toFixed(2)}ms (${averageTime.toFixed(4)}ms average)`);

            // Should handle high volume efficiently
            expect(averageTime).toBeLessThan(0.1); // Less than 0.1ms per resolution
        });

        test('should handle complex mixed workload', async () => {
            // Create a mix of service types
            const ISingleton = createServiceInterface('ISingleton', class {});
            const ITransient = createServiceInterface('ITransient', class {});
            const IFactory = createServiceInterface('IFactory', class {});
            const IScoped = createServiceInterface('IScoped', class {});

            container.registerSingleton(ISingleton, class Singleton {});
            container.registerTransient(ITransient, class Transient {});
            container.registerFactory(IFactory, () => ({ type: 'factory' }));
            container.registerScoped(IScoped, class Scoped {}, ServiceScope.Scoped);

            container.createScope('stress-scope');
            container.setCurrentScope('stress-scope');

            const iterations = 1000;
            const startTime = performance.now();

            for (let i = 0; i < iterations; i++) {
                // Mix of different resolution types
                container.resolve(ISingleton);
                container.resolve(ITransient);
                container.resolve(IFactory);
                container.resolve(IScoped);
            }

            const totalTime = performance.now() - startTime;
            const averageTime = totalTime / (iterations * 4);

            console.log(`Mixed workload: ${averageTime.toFixed(4)}ms average per resolution`);

            container.disposeScope('stress-scope');

            // Should handle mixed workload efficiently
            expect(averageTime).toBeLessThan(1);
        });
    });

    describe('Long-Running Stability', () => {
        test('should maintain performance over extended usage', async () => {
            const ILongRunningService = createServiceInterface('ILongRunningService', class {
                getValue(): string { return ''; }
            });

            container.registerSingleton(ILongRunningService, class LongRunningService {
                getValue(): string { return 'long-running'; }
            });

            const measurements = [];
            const batchSize = 1000;
            const batches = 10;

            for (let batch = 0; batch < batches; batch++) {
                const batchStart = performance.now();

                for (let i = 0; i < batchSize; i++) {
                    const service = container.resolve(ILongRunningService);
                    expect(service.getValue()).toBe('long-running');
                }

                const batchTime = performance.now() - batchStart;
                const batchAverage = batchTime / batchSize;
                measurements.push(batchAverage);

                console.log(`Batch ${batch + 1}: ${batchAverage.toFixed(4)}ms average`);
            }

            // Performance should remain stable (no significant degradation)
            const firstBatch = measurements[0];
            const lastBatch = measurements[measurements.length - 1];
            const degradation = (lastBatch - firstBatch) / firstBatch;

            console.log(`Performance degradation: ${(degradation * 100).toFixed(2)}%`);

            // Should not degrade more than 50%
            expect(degradation).toBeLessThan(0.5);
        });

        test('should handle metrics collection without performance impact', async () => {
            const IMetricsService = createServiceInterface('IMetricsService', class {});
            container.registerSingleton(IMetricsService, class MetricsService {});

            // Test with metrics enabled
            const iterations = 1000;

            const startWithMetrics = performance.now();
            for (let i = 0; i < iterations; i++) {
                container.resolve(IMetricsService);
            }
            const timeWithMetrics = performance.now() - startWithMetrics;

            // Clear metrics and test again
            container.clearMetrics();

            const startWithoutMetrics = performance.now();
            for (let i = 0; i < iterations; i++) {
                container.resolve(IMetricsService);
            }
            const timeWithoutMetrics = performance.now() - startWithoutMetrics;

            const overhead = (timeWithMetrics - timeWithoutMetrics) / timeWithoutMetrics;
            console.log(`Metrics overhead: ${(overhead * 100).toFixed(2)}%`);

            // Metrics should not add significant overhead (less than 100%)
            expect(overhead).toBeLessThan(1.0);
        });
    });
});
