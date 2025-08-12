/**
 * 🧪 CIRCULAR DEPENDENCY DETECTION TESTS
 * 
 * Critical tests for circular dependency detection and prevention,
 * ensuring the DI system handles complex dependency scenarios gracefully.
 */

import { describe, test, expect, beforeEach } from 'vitest';
import {
    ServiceContainer,
    createServiceInterface,
    ServiceScope
} from '../../index.js';

describe('Circular Dependency Detection', () => {
    let container: ServiceContainer;

    beforeEach(() => {
        container = new ServiceContainer('circular-test');
    });

    afterEach(() => {
        container.dispose();
    });

    describe('Direct Circular Dependencies', () => {
        test('should detect simple A -> B -> A circular dependency', () => {
            const IServiceA = createServiceInterface('IServiceA', class {
                getValue(): string { return ''; }
            });
            
            const IServiceB = createServiceInterface('IServiceB', class {
                getValue(): string { return ''; }
            });

            // Create circular dependency through factory registration
            container.registerFactory(IServiceA, () => {
                const serviceB = container.resolve(IServiceB);
                return {
                    getValue: () => `A depends on ${serviceB.getValue()}`
                };
            });

            container.registerFactory(IServiceB, () => {
                const serviceA = container.resolve(IServiceA); // This creates the cycle
                return {
                    getValue: () => `B depends on ${serviceA.getValue()}`
                };
            });

            expect(() => {
                container.resolve(IServiceA);
            }).toThrow(/Circular dependency detected/);
        });

        test('should detect self-referencing circular dependency', () => {
            const ISelfReferencing = createServiceInterface('ISelfReferencing', class {
                getValue(): string { return ''; }
            });

            container.registerFactory(ISelfReferencing, () => {
                const self = container.resolve(ISelfReferencing); // Self-reference
                return {
                    getValue: () => `Self: ${self.getValue()}`
                };
            });

            expect(() => {
                container.resolve(ISelfReferencing);
            }).toThrow(/Circular dependency detected/);
        });
    });

    describe('Complex Circular Dependencies', () => {
        test('should detect A -> B -> C -> A circular dependency', () => {
            const IServiceA = createServiceInterface('IServiceA', class {});
            const IServiceB = createServiceInterface('IServiceB', class {});
            const IServiceC = createServiceInterface('IServiceC', class {});

            container.registerFactory(IServiceA, () => {
                const serviceB = container.resolve(IServiceB);
                return { dependency: serviceB };
            });

            container.registerFactory(IServiceB, () => {
                const serviceC = container.resolve(IServiceC);
                return { dependency: serviceC };
            });

            container.registerFactory(IServiceC, () => {
                const serviceA = container.resolve(IServiceA); // Completes the cycle
                return { dependency: serviceA };
            });

            expect(() => {
                container.resolve(IServiceA);
            }).toThrow(/Circular dependency detected/);
        });

        test('should detect deep circular dependency chain', () => {
            const services = [];
            const interfaces = [];

            // Create a chain of 5 services: A -> B -> C -> D -> E -> A
            for (let i = 0; i < 5; i++) {
                const serviceName = `IService${String.fromCharCode(65 + i)}`; // A, B, C, D, E
                interfaces.push(createServiceInterface(serviceName, class {}));
            }

            // Register services with dependencies
            for (let i = 0; i < 5; i++) {
                const currentInterface = interfaces[i];
                const nextInterface = interfaces[(i + 1) % 5]; // Wrap around to create cycle

                container.registerFactory(currentInterface, () => {
                    const dependency = container.resolve(nextInterface);
                    return { dependency };
                });
            }

            expect(() => {
                container.resolve(interfaces[0]);
            }).toThrow(/Circular dependency detected/);
        });
    });

    describe('Valid Complex Dependencies', () => {
        test('should allow valid diamond dependency pattern', () => {
            // Diamond pattern: A depends on B and C, both B and C depend on D
            const IServiceA = createServiceInterface('IServiceA', class {});
            const IServiceB = createServiceInterface('IServiceB', class {});
            const IServiceC = createServiceInterface('IServiceC', class {});
            const IServiceD = createServiceInterface('IServiceD', class {
                getValue(): string { return ''; }
            });

            // D has no dependencies
            container.registerSingleton(IServiceD, class ServiceD {
                getValue(): string { return 'D'; }
            });

            // B depends on D
            container.registerFactory(IServiceB, () => {
                const serviceD = container.resolve(IServiceD);
                return { 
                    getValue: () => `B->${serviceD.getValue()}`
                };
            });

            // C depends on D
            container.registerFactory(IServiceC, () => {
                const serviceD = container.resolve(IServiceD);
                return { 
                    getValue: () => `C->${serviceD.getValue()}`
                };
            });

            // A depends on both B and C
            container.registerFactory(IServiceA, () => {
                const serviceB = container.resolve(IServiceB);
                const serviceC = container.resolve(IServiceC);
                return { 
                    getValue: () => `A->${serviceB.getValue()},${serviceC.getValue()}`
                };
            });

            expect(() => {
                const serviceA = container.resolve(IServiceA);
                expect(serviceA).toBeDefined();
            }).not.toThrow();
        });

        test('should allow deep linear dependency chain', () => {
            const interfaces = [];
            
            // Create a linear chain: A -> B -> C -> D -> E
            for (let i = 0; i < 5; i++) {
                const serviceName = `ILinearService${String.fromCharCode(65 + i)}`;
                interfaces.push(createServiceInterface(serviceName, class {
                    getValue(): string { return ''; }
                }));
            }

            // Register the last service (E) with no dependencies
            container.registerSingleton(interfaces[4], class ServiceE {
                getValue(): string { return 'E'; }
            });

            // Register the chain backwards (D -> C -> B -> A)
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

            expect(() => {
                const serviceA = container.resolve(interfaces[0]);
                expect(serviceA.getValue()).toBe('A->B->C->D->E');
            }).not.toThrow();
        });
    });

    describe('Resolution Stack Tracking', () => {
        test('should track resolution stack depth', () => {
            const IDeepService = createServiceInterface('IDeepService', class {});
            
            let resolutionDepth = 0;
            container.registerFactory(IDeepService, () => {
                resolutionDepth++;
                if (resolutionDepth > 50) { // Simulate max depth
                    throw new Error('Maximum resolution depth exceeded');
                }
                return { depth: resolutionDepth };
            });

            expect(() => {
                container.resolve(IDeepService);
            }).not.toThrow();
            
            expect(resolutionDepth).toBe(1);
        });

        test('should provide detailed circular dependency error message', () => {
            const IServiceA = createServiceInterface('IServiceA', class {});
            const IServiceB = createServiceInterface('IServiceB', class {});
            const IServiceC = createServiceInterface('IServiceC', class {});

            container.registerFactory(IServiceA, () => {
                const serviceB = container.resolve(IServiceB);
                return { dependency: serviceB };
            });

            container.registerFactory(IServiceB, () => {
                const serviceC = container.resolve(IServiceC);
                return { dependency: serviceC };
            });

            container.registerFactory(IServiceC, () => {
                const serviceA = container.resolve(IServiceA);
                return { dependency: serviceA };
            });

            try {
                container.resolve(IServiceA);
                expect.fail('Should have thrown circular dependency error');
            } catch (error) {
                const errorMessage = error.message;
                expect(errorMessage).toContain('Circular dependency detected');
                expect(errorMessage).toContain('IServiceA');
                expect(errorMessage).toContain('IServiceB');
                expect(errorMessage).toContain('IServiceC');
            }
        });
    });

    describe('Scoped Circular Dependencies', () => {
        test('should detect circular dependencies within scopes', () => {
            const IScopedA = createServiceInterface('IScopedA', class {});
            const IScopedB = createServiceInterface('IScopedB', class {});

            container.registerScoped(IScopedA, class ScopedA {}, ServiceScope.Scoped);
            container.registerScoped(IScopedB, class ScopedB {}, ServiceScope.Scoped);

            // Override with factories that create circular dependency
            container.registerFactory(IScopedA, () => {
                const scopedB = container.resolve(IScopedB);
                return { dependency: scopedB };
            });

            container.registerFactory(IScopedB, () => {
                const scopedA = container.resolve(IScopedA);
                return { dependency: scopedA };
            });

            container.createScope('test-scope');
            container.setCurrentScope('test-scope');

            expect(() => {
                container.resolve(IScopedA);
            }).toThrow(/Circular dependency detected/);

            container.disposeScope('test-scope');
        });
    });

    describe('Lazy Loading and Circular Dependencies', () => {
        test('should handle lazy services in circular dependency detection', () => {
            const ILazyA = createServiceInterface('ILazyA', class {});
            const ILazyB = createServiceInterface('ILazyB', class {});

            // Register lazy services
            container.registerLazy(ILazyA, class LazyA {});
            container.registerLazy(ILazyB, class LazyB {});

            // Override with factories that would create circular dependency
            container.registerFactory(ILazyA, () => {
                const lazyB = container.resolve(ILazyB);
                return { dependency: lazyB };
            });

            container.registerFactory(ILazyB, () => {
                const lazyA = container.resolve(ILazyA);
                return { dependency: lazyA };
            });

            expect(() => {
                container.resolve(ILazyA);
            }).toThrow(/Circular dependency detected/);
        });

        test('should allow lazy proxies to break potential circular dependencies', () => {
            const ILazyBreaker = createServiceInterface('ILazyBreaker', class {
                getValue(): string { return ''; }
            });
            
            const IRegularService = createServiceInterface('IRegularService', class {
                getValue(): string { return ''; }
            });

            // Register regular service that uses lazy proxy
            container.registerFactory(IRegularService, () => {
                const lazyBreaker = container.resolveLazy(ILazyBreaker);
                return {
                    getValue: () => `Regular service with lazy: ${lazyBreaker.getValue()}`
                };
            });

            // Register lazy service
            container.registerLazy(ILazyBreaker, class LazyBreaker {
                getValue(): string { return 'lazy-value'; }
            });

            expect(() => {
                const service = container.resolve(IRegularService);
                expect(service.getValue()).toContain('lazy-value');
            }).not.toThrow();
        });
    });
});
