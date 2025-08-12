# 🚀 TKA Enterprise Dependency Injection System

**Next-generation dependency injection for web applications that matches and exceeds the sophistication of enterprise desktop systems.**

## ✨ Features

- ✅ **Type-safe interface-based registration** - Full TypeScript support with runtime validation
- ✅ **Advanced lifecycle management** - Singleton, Transient, Scoped, Lazy, Factory patterns
- ✅ **Sophisticated resolution chain** - Multiple resolvers with fallback strategies
- ✅ **Comprehensive validation** - Registration validation with detailed error reporting
- ✅ **Enterprise debugging tools** - Performance monitoring, metrics, and diagnostics
- ✅ **Application factory pattern** - Production, Test, Headless, Development configurations
- ✅ **Cross-platform compatibility** - Full parity with desktop Python DI system
- ✅ **Svelte integration** - Native reactive store integration and context providers

## 🏗️ Architecture

```
TKA Enterprise DI System
├── Core Components
│   ├── ServiceContainer      # Main DI container with enterprise features
│   ├── ServiceRegistry       # Advanced service registration and metadata
│   ├── ResolverChain        # Sophisticated resolution with multiple strategies
│   ├── LifecycleManager     # Advanced lifecycle and scope management
│   ├── ValidationEngine     # Comprehensive validation and error handling
│   ├── DebuggingTools       # Enterprise debugging and monitoring
│   └── ServiceMetrics       # Performance tracking and telemetry
├── Application Factory
│   ├── Production App       # Full web UI with persistent storage
│   ├── Test App            # Mock services with in-memory storage
│   ├── Headless App        # Real logic without UI components
│   └── Development App     # Enhanced debugging and hot-reload
├── Advanced Features
│   ├── LazyProxy           # Transparent lazy loading with proxies
│   ├── ServiceDecorators   # Attribute-based service registration
│   ├── Cross-Platform Types # Shared type system with desktop
│   └── Reactive Integration # Svelte store integration
└── Testing Infrastructure
    ├── TestHelper          # Comprehensive testing utilities
    ├── Mock Services       # Test doubles and headless services
    └── Integration Tests   # Cross-platform compatibility tests
```

## 🚀 Quick Start

### Basic Usage

```typescript
import {
    createProductionContainer,
    defineService,
    resolve
} from '@tka/di';

// Define service interface
const IUserService = defineService('IUserService', class {
    getUser(id: string): User | null { return null; }
    createUser(data: UserData): User { return null as any; }
});

// Get container and resolve service
const container = createProductionContainer();
const userService = container.resolve(IUserService);

// Or use global container
const globalUserService = resolve(IUserService);
```

### Container Builder Pattern

```typescript
import { createContainerBuilder } from '@tka/di';

const container = createContainerBuilder('my-app')
    .singleton(IUserService, UserService)
    .transient(IEmailService, EmailService)
    .factory(INotificationService, () => new NotificationService())
    .withStandardServices()
    .withDebugMode()
    .build();
```

### Application Factory

```typescript
import { ApplicationFactory } from '@tka/di';

// Different application configurations
const prodApp = ApplicationFactory.createProductionApp();
const testApp = ApplicationFactory.createTestApp();
const headlessApp = ApplicationFactory.createHeadlessApp();
const devApp = ApplicationFactory.createDevelopmentApp();
```

## 🎭 Svelte Integration

### Setup in App.svelte

```typescript
import { setupSvelteDI } from '@tka/di/svelte';

const { container, stores, setDIContainer } = setupSvelteDI();

// Set DI container in context
setDIContainer();

// Use reactive stores
$: count = $stores.count;
$: theme = $stores.theme;
```

### Component Injection

```typescript
import { inject, serviceToStore } from '@tka/di/svelte';

// Direct injection
const userService = inject(IUserService);

// Reactive store
const userStore = serviceToStore(userService, s => s.currentUser);
```

## 🧪 Testing

### Comprehensive Test Suite

```typescript
import { TKAWebTestHelper } from '@tka/di/testing';

const testHelper = new TKAWebTestHelper(true);

// Run full test suite
const results = await testHelper.runComprehensiveTestSuite();
console.log(`Tests: ${results.passedTests}/${results.totalTests} passed`);

// Test specific functionality
const sequenceResult = await testHelper.createSequence('Test', 8);
const beatResult = await testHelper.createBeatWithMotions(1, 'A');
const workflowResult = await testHelper.testCompleteUserWorkflow();
```

### Custom Testing

```typescript
// Test dependency injection
const diResult = await testHelper.testServiceDependencyInjection();

// Test container isolation
const isolationResult = await testHelper.testContainerIsolation();
```

## 📊 Performance Monitoring

### Metrics and Diagnostics

```typescript
// Get container metrics
const metrics = container.getMetrics();
console.log(`Total resolutions: ${metrics.totalResolutions}`);
console.log(`Average time: ${metrics.averageResolutionTime}ms`);

// Get detailed diagnostics
const diagnostics = container.getDiagnostics();
console.log('Container ID:', diagnostics.containerId);
console.log('Registered services:', diagnostics.registeredServices);

// Performance summary
const summary = container.getPerformanceSummary();
console.log('Slow services:', summary.slowServices);
console.log('Error-prone services:', summary.errorProneServices);
```

### Debug Mode

```typescript
// Enable debugging
container.setDebugMode(true);

// Export debug data
const debugData = container.exportDebugData();
console.log('Debug export:', debugData);
```

## 🔧 Advanced Features

### Lazy Loading

```typescript
// Register lazy service
container.registerLazy(IExpensiveService, ExpensiveService);

// Get lazy proxy (service not created yet)
const lazyService = container.resolveLazy(IExpensiveService);

// Service created on first use
const result = lazyService.doExpensiveOperation();
```

### Scoped Services

```typescript
// Register scoped service
container.registerScoped(IScopedService, ScopedService, ServiceScope.Request);

// Create and use scopes
container.createScope('request-123');
container.setCurrentScope('request-123');
const scopedService = container.resolve(IScopedService);

// Cleanup scope
container.disposeScope('request-123');
```

### Factory Patterns

```typescript
// Simple factory
container.registerFactory(IService, () => new Service());

// Container-aware factory
container.registerFactory(IComplexService, (container) => {
    const dependency = container.resolve(IDependency);
    return new ComplexService(dependency);
});
```

## 🌐 Cross-Platform Compatibility

This web DI system provides **full parity** with the desktop Python DI system:

| Feature | Desktop (Python) | Web (TypeScript) | Status |
|---------|------------------|------------------|---------|
| Service Registration | ✅ | ✅ | ✅ Full Parity |
| Lifecycle Management | ✅ | ✅ | ✅ Full Parity |
| Scoping & Isolation | ✅ | ✅ | ✅ Full Parity |
| Lazy Loading | ✅ | ✅ | ✅ Full Parity |
| Validation Engine | ✅ | ✅ | ✅ Full Parity |
| Debugging Tools | ✅ | ✅ | ✅ Full Parity |
| Performance Metrics | ✅ | ✅ | ✅ Full Parity |
| Application Factory | ✅ | ✅ | ✅ Full Parity |
| Testing Infrastructure | ✅ | ✅ | ✅ Full Parity |

## 📚 API Reference

### Core Classes

- **ServiceContainer** - Main DI container with enterprise features
- **ApplicationFactory** - Factory for creating configured applications
- **ServiceRegistrationManager** - Orchestrates service registration
- **TKAWebTestHelper** - Comprehensive testing utilities

### Type System

- **ServiceInterface<T>** - Type-safe service interface marker
- **ServiceScope** - Lifecycle scope enumeration
- **ServiceDescriptor** - Service registration metadata
- **ResolutionContext** - Service resolution context information

### Utility Functions

- **defineService()** - Quick service interface creation
- **createProductionContainer()** - Production-ready container
- **createTestContainer()** - Test container with mocks
- **resolve()** - Global service resolution
- **inject()** - Svelte component injection

## 🎯 Best Practices

1. **Use Interface-Based Registration** - Always define service interfaces
2. **Leverage Application Factory** - Use appropriate factory for your environment
3. **Implement Proper Scoping** - Choose correct lifecycle for your services
4. **Enable Debug Mode in Development** - Use debugging tools during development
5. **Write Comprehensive Tests** - Use TKAWebTestHelper for testing
6. **Monitor Performance** - Track metrics and optimize slow services
7. **Handle Errors Gracefully** - Use validation and error handling features

## 🔄 Migration from Basic DI

If you're migrating from a basic DI system:

1. Replace string tokens with typed interfaces using `defineService()`
2. Use `ApplicationFactory` instead of manual container creation
3. Leverage advanced scoping instead of simple singleton/transient
4. Add comprehensive testing with `TKAWebTestHelper`
5. Enable performance monitoring and debugging

## 🤝 Contributing

This DI system is part of the TKA project. See the main TKA documentation for contribution guidelines.

## 📄 License

Part of the TKA project. See main project license.

---

**🚀 Your web applications now have enterprise-grade dependency injection that matches desktop sophistication!**
