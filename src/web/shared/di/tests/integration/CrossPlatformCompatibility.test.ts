/**
 * 🧪 CROSS-PLATFORM COMPATIBILITY TESTS
 * 
 * Ensures the web DI system maintains full parity with the desktop
 * Python DI system, validating equivalent functionality and behavior.
 */

import { describe, test, expect, beforeEach, afterEach } from 'vitest';
import {
    ServiceContainer,
    ApplicationFactory,
    createServiceInterface,
    ServiceScope,
    TKAWebTestHelper
} from '../../index.js';

describe('Cross-Platform Compatibility', () => {
    let testHelper: TKAWebTestHelper;

    beforeEach(() => {
        testHelper = new TKAWebTestHelper(true);
    });

    afterEach(() => {
        testHelper.dispose();
    });

    describe('Desktop DI System Parity', () => {
        test('should provide equivalent ApplicationFactory patterns', () => {
            // Test all factory methods exist and work
            const productionApp = ApplicationFactory.createProductionApp();
            const testApp = ApplicationFactory.createTestApp();
            const headlessApp = ApplicationFactory.createHeadlessApp();
            const devApp = ApplicationFactory.createDevelopmentApp();

            expect(productionApp).toBeInstanceOf(ServiceContainer);
            expect(testApp).toBeInstanceOf(ServiceContainer);
            expect(headlessApp).toBeInstanceOf(ServiceContainer);
            expect(devApp).toBeInstanceOf(ServiceContainer);

            // Verify different configurations
            const prodDiagnostics = productionApp.getDiagnostics();
            const testDiagnostics = testApp.getDiagnostics();

            expect(prodDiagnostics.containerId).toContain('production');
            expect(testDiagnostics.containerId).toContain('test');

            // Cleanup
            productionApp.dispose();
            testApp.dispose();
            headlessApp.dispose();
            devApp.dispose();
        });

        test('should support equivalent service registration patterns', () => {
            const container = testHelper.getContainer();

            const ITestService = createServiceInterface('ITestService', class {
                getValue(): string { return ''; }
            });

            // Test all registration patterns that exist in desktop system
            expect(() => {
                container.registerSingleton(ITestService, class TestService {
                    getValue(): string { return 'singleton'; }
                });
            }).not.toThrow();

            expect(() => {
                container.registerTransient(ITestService, class TestService {
                    getValue(): string { return 'transient'; }
                });
            }).not.toThrow();

            expect(() => {
                container.registerScoped(ITestService, class TestService {
                    getValue(): string { return 'scoped'; }
                }, ServiceScope.Scoped);
            }).not.toThrow();

            expect(() => {
                container.registerFactory(ITestService, () => ({
                    getValue: () => 'factory'
                }));
            }).not.toThrow();

            expect(() => {
                container.registerInstance(ITestService, {
                    getValue: () => 'instance'
                });
            }).not.toThrow();

            expect(() => {
                container.registerLazy(ITestService, class TestService {
                    getValue(): string { return 'lazy'; }
                });
            }).not.toThrow();
        });

        test('should provide equivalent lifecycle management', () => {
            const container = testHelper.getContainer();

            // Test scope management (equivalent to desktop)
            expect(() => {
                container.createScope('test-scope');
                container.setCurrentScope('test-scope');
                container.disposeScope('test-scope');
            }).not.toThrow();

            // Test disposal patterns
            let disposed = false;
            const IDisposableService = createServiceInterface('IDisposableService', class {});
            
            container.registerSingleton(IDisposableService, class DisposableService {
                dispose(): void { disposed = true; }
            });

            const service = container.resolve(IDisposableService);
            container.dispose();

            // Service should be disposed when container is disposed
            expect(disposed).toBe(true);
        });

        test('should provide equivalent debugging and diagnostics', () => {
            const container = testHelper.getContainer();

            // Test debug mode
            expect(() => {
                container.setDebugMode(true);
                container.setDebugMode(false);
            }).not.toThrow();

            // Test diagnostics
            const diagnostics = container.getDiagnostics();
            expect(diagnostics).toHaveProperty('containerId');
            expect(diagnostics).toHaveProperty('createdAt');
            expect(diagnostics).toHaveProperty('isDisposed');
            expect(diagnostics).toHaveProperty('registeredServices');
            expect(diagnostics).toHaveProperty('metrics');
            expect(diagnostics).toHaveProperty('debugInfo');

            // Test metrics
            const metrics = container.getMetrics();
            expect(metrics).toHaveProperty('containerId');
            expect(metrics).toHaveProperty('totalServices');
            expect(metrics).toHaveProperty('totalResolutions');
            expect(metrics).toHaveProperty('averageResolutionTime');
        });
    });

    describe('TKAAITestHelper Equivalent Functionality', () => {
        test('should provide comprehensive test suite equivalent', async () => {
            const results = await testHelper.runComprehensiveTestSuite();

            expect(results).toHaveProperty('success');
            expect(results).toHaveProperty('totalTests');
            expect(results).toHaveProperty('passedTests');
            expect(results).toHaveProperty('failedTests');
            expect(results).toHaveProperty('duration');
            expect(results).toHaveProperty('results');

            // Should have multiple test categories like desktop version
            expect(results.totalTests).toBeGreaterThanOrEqual(8);
            
            // Should pass all tests
            expect(results.success).toBe(true);
            expect(results.failedTests).toBe(0);
        });

        test('should provide sequence creation equivalent', async () => {
            const result = await testHelper.createSequence('Test Sequence', 8);

            expect(result).toHaveProperty('success');
            expect(result).toHaveProperty('message');
            expect(result).toHaveProperty('duration');

            if (result.success) {
                expect(result.details).toHaveProperty('id');
                expect(result.details).toHaveProperty('name');
                expect(result.details).toHaveProperty('length');
                expect(result.details.name).toBe('Test Sequence');
                expect(result.details.length).toBe(8);
            }
        });

        test('should provide beat creation equivalent', async () => {
            const result = await testHelper.createBeatWithMotions(1, 'A');

            expect(result).toHaveProperty('success');
            expect(result).toHaveProperty('message');
            expect(result).toHaveProperty('duration');

            if (result.success) {
                expect(result.details).toHaveProperty('beatNumber');
                expect(result.details).toHaveProperty('letter');
                expect(result.details).toHaveProperty('motions');
                expect(result.details.beatNumber).toBe(1);
                expect(result.details.letter).toBe('A');
            }
        });

        test('should provide complete workflow testing', async () => {
            const result = await testHelper.testCompleteUserWorkflow();

            expect(result).toHaveProperty('success');
            expect(result).toHaveProperty('message');
            expect(result).toHaveProperty('duration');

            if (result.success) {
                expect(result.details).toHaveProperty('steps');
                expect(result.details).toHaveProperty('executedSteps');
                expect(result.details.executedSteps).toBeGreaterThan(0);
            }
        });
    });

    describe('Service Interface Compatibility', () => {
        test('should support equivalent service interface patterns', () => {
            // Test interface creation patterns
            const ICompatService = createServiceInterface('ICompatService', class {
                process(data: any): any { return data; }
            }, {
                description: 'Compatibility test service',
                version: '1.0.0',
                tags: ['test', 'compatibility']
            });

            expect(ICompatService).toHaveProperty('name');
            expect(ICompatService).toHaveProperty('symbol');
            expect(ICompatService).toHaveProperty('type');
            expect(ICompatService).toHaveProperty('metadata');

            expect(ICompatService.name).toBe('ICompatService');
            expect(ICompatService.metadata?.description).toBe('Compatibility test service');
            expect(ICompatService.metadata?.tags).toContain('test');
        });

        test('should support equivalent dependency injection patterns', async () => {
            const container = testHelper.getContainer();

            // Test dependency injection equivalent to desktop patterns
            const IRepository = createServiceInterface('IRepository', class {
                save(data: any): any { return data; }
            });

            const IService = createServiceInterface('IService', class {
                process(data: any): any { return data; }
            });

            const IController = createServiceInterface('IController', class {
                handle(request: any): any { return request; }
            });

            // Register with dependency chain
            container.registerSingleton(IRepository, class Repository {
                save(data: any): any {
                    return { ...data, saved: true, timestamp: new Date() };
                }
            });

            container.registerFactory(IService, () => {
                const repo = container.resolve(IRepository);
                return new (class Service {
                    process(data: any): any {
                        const processed = { ...data, processed: true };
                        return repo.save(processed);
                    }
                })();
            });

            container.registerFactory(IController, () => {
                const service = container.resolve(IService);
                return new (class Controller {
                    handle(request: any): any {
                        return service.process(request);
                    }
                })();
            });

            // Test the full chain
            const controller = container.resolve(IController);
            const result = controller.handle({ test: 'data' });

            expect(result.test).toBe('data');
            expect(result.processed).toBe(true);
            expect(result.saved).toBe(true);
            expect(result.timestamp).toBeInstanceOf(Date);
        });
    });

    describe('Error Handling Compatibility', () => {
        test('should provide equivalent error handling patterns', () => {
            const container = testHelper.getContainer();

            // Test unregistered service error
            const IUnregistered = createServiceInterface('IUnregistered', class {});
            
            expect(() => {
                container.resolve(IUnregistered);
            }).toThrow(/Service not found/);

            // Test circular dependency error
            const ICircularA = createServiceInterface('ICircularA', class {});
            const ICircularB = createServiceInterface('ICircularB', class {});

            container.registerFactory(ICircularA, () => {
                const b = container.resolve(ICircularB);
                return { dependency: b };
            });

            container.registerFactory(ICircularB, () => {
                const a = container.resolve(ICircularA);
                return { dependency: a };
            });

            expect(() => {
                container.resolve(ICircularA);
            }).toThrow(/Circular dependency detected/);
        });

        test('should provide equivalent validation patterns', () => {
            const container = testHelper.getContainer();

            // Test invalid registration
            expect(() => {
                container.registerSingleton(null as any, null as any);
            }).toThrow();

            // Test disposed container
            container.dispose();
            
            const ITestService = createServiceInterface('ITestService', class {});
            
            expect(() => {
                container.registerSingleton(ITestService, class TestService {});
            }).toThrow(/disposed/);
        });
    });

    describe('Performance Compatibility', () => {
        test('should provide equivalent performance characteristics', async () => {
            const container = testHelper.getContainer();

            const IPerformanceService = createServiceInterface('IPerformanceService', class {
                getValue(): string { return ''; }
            });

            container.registerSingleton(IPerformanceService, class PerformanceService {
                getValue(): string { return 'performance-test'; }
            });

            // Test resolution performance
            const iterations = 1000;
            const startTime = performance.now();

            for (let i = 0; i < iterations; i++) {
                const service = container.resolve(IPerformanceService);
                expect(service.getValue()).toBe('performance-test');
            }

            const endTime = performance.now();
            const averageTime = (endTime - startTime) / iterations;

            console.log(`Web DI resolution performance: ${averageTime.toFixed(4)}ms average`);

            // Should be reasonably fast (equivalent to desktop performance expectations)
            expect(averageTime).toBeLessThan(1); // Less than 1ms per resolution
        });

        test('should provide equivalent metrics collection', () => {
            const container = testHelper.getContainer();

            const IMetricsService = createServiceInterface('IMetricsService', class {});
            container.registerSingleton(IMetricsService, class MetricsService {});

            // Generate some metrics
            for (let i = 0; i < 10; i++) {
                container.resolve(IMetricsService);
            }

            const metrics = container.getMetrics();

            // Should track equivalent metrics to desktop system
            expect(metrics.totalResolutions).toBeGreaterThan(0);
            expect(metrics.averageResolutionTime).toBeGreaterThan(0);
            expect(metrics.serviceMetrics.size).toBeGreaterThan(0);

            // Should have service-specific metrics
            const serviceMetrics = metrics.serviceMetrics.get('IMetricsService');
            expect(serviceMetrics).toBeDefined();
            expect(serviceMetrics?.totalResolutions).toBe(10);
        });
    });

    describe('Feature Completeness', () => {
        test('should provide all desktop DI system features', () => {
            const container = testHelper.getContainer();

            // Verify all major features are available
            const features = [
                'registerSingleton',
                'registerTransient', 
                'registerScoped',
                'registerFactory',
                'registerInstance',
                'registerLazy',
                'resolve',
                'tryResolve',
                'resolveLazy',
                'createScope',
                'setCurrentScope',
                'disposeScope',
                'isRegistered',
                'getDiagnostics',
                'getMetrics',
                'clearMetrics',
                'setDebugMode',
                'dispose'
            ];

            for (const feature of features) {
                expect(typeof (container as any)[feature]).toBe('function');
            }
        });

        test('should provide equivalent testing infrastructure', () => {
            // Verify TKAWebTestHelper has equivalent methods to desktop TKAAITestHelper
            const testMethods = [
                'runComprehensiveTestSuite',
                'createSequence',
                'createBeatWithMotions',
                'testCompleteUserWorkflow',
                'testServiceDependencyInjection',
                'testContainerIsolation',
                'getContainer',
                'dispose'
            ];

            for (const method of testMethods) {
                expect(typeof (testHelper as any)[method]).toBe('function');
            }
        });
    });
});
