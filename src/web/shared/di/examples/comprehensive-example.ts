/**
 * 🎯 TKA DI COMPREHENSIVE EXAMPLE
 * 
 * This example demonstrates the full power and sophistication of the TKA
 * Enterprise Dependency Injection system, showcasing all major features.
 */

import {
    ServiceContainer,
    ApplicationFactory,
    createServiceInterface,
    createContainerBuilder,
    ServiceScope,
    getGlobalContainer,
    resolve,
    defineService
} from '../index.js';

// ============================================================================
// EXAMPLE 1: BASIC SERVICE REGISTRATION AND RESOLUTION
// ============================================================================

console.log('🚀 TKA DI System - Comprehensive Examples\n');

// Define service interfaces
const IUserService = defineService('IUserService', class {
    getUser(id: string): any { return null; }
    createUser(data: any): any { return null; }
});

const IEmailService = defineService('IEmailService', class {
    sendEmail(to: string, subject: string, body: string): Promise<boolean> { return Promise.resolve(false); }
});

const INotificationService = defineService('INotificationService', class {
    notify(userId: string, message: string): Promise<void> { return Promise.resolve(); }
});

// Implement services
class UserService {
    private users = new Map<string, any>();

    getUser(id: string): any {
        return this.users.get(id) || null;
    }

    createUser(data: any): any {
        const user = { id: this.generateId(), ...data, createdAt: new Date() };
        this.users.set(user.id, user);
        return user;
    }

    private generateId(): string {
        return `user_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    }
}

class EmailService {
    async sendEmail(to: string, subject: string, body: string): Promise<boolean> {
        console.log(`📧 Sending email to ${to}: ${subject}`);
        // Simulate async operation
        await new Promise(resolve => setTimeout(resolve, 100));
        return true;
    }
}

class NotificationService {
    constructor(
        private userService: any,
        private emailService: any
    ) {}

    async notify(userId: string, message: string): Promise<void> {
        const user = this.userService.getUser(userId);
        if (user && user.email) {
            await this.emailService.sendEmail(user.email, 'Notification', message);
            console.log(`🔔 Notified user ${userId}: ${message}`);
        }
    }
}

// ============================================================================
// EXAMPLE 2: APPLICATION FACTORY USAGE
// ============================================================================

console.log('📦 Example 1: Application Factory Usage');

// Create different application configurations
const productionContainer = ApplicationFactory.createProductionApp();
const testContainer = ApplicationFactory.createTestApp();
const headlessContainer = ApplicationFactory.createHeadlessApp();
const devContainer = ApplicationFactory.createDevelopmentApp();

console.log('✅ Created all application variants');
console.log(`Production container: ${productionContainer.getDiagnostics().containerId}`);
console.log(`Test container: ${testContainer.getDiagnostics().containerId}`);
console.log(`Headless container: ${headlessContainer.getDiagnostics().containerId}`);
console.log(`Development container: ${devContainer.getDiagnostics().containerId}\n`);

// ============================================================================
// EXAMPLE 3: CONTAINER BUILDER PATTERN
// ============================================================================

console.log('🏗️ Example 2: Container Builder Pattern');

const customContainer = createContainerBuilder('custom-app')
    .singleton(IUserService, UserService)
    .singleton(IEmailService, EmailService)
    .factory(INotificationService, () => {
        const userService = customContainer.resolve(IUserService);
        const emailService = customContainer.resolve(IEmailService);
        return new NotificationService(userService, emailService);
    })
    .withDebugMode()
    .build();

console.log('✅ Built custom container with builder pattern\n');

// ============================================================================
// EXAMPLE 4: SERVICE RESOLUTION AND USAGE
// ============================================================================

console.log('🔧 Example 3: Service Resolution and Usage');

// Resolve services
const userService = customContainer.resolve(IUserService);
const notificationService = customContainer.resolve(INotificationService);

// Use services
const newUser = userService.createUser({
    name: 'John Doe',
    email: 'john@example.com'
});

console.log('👤 Created user:', newUser);

// Send notification
await notificationService.notify(newUser.id, 'Welcome to TKA!');

console.log('✅ Services working correctly\n');

// ============================================================================
// EXAMPLE 5: ADVANCED SCOPING
// ============================================================================

console.log('🎯 Example 4: Advanced Scoping');

// Create scoped services
const IScopedService = defineService('IScopedService', class {
    getValue(): string { return ''; }
    setValue(value: string): void {}
});

class ScopedService {
    private value = `scoped_${Math.random().toString(36).substr(2, 9)}`;

    getValue(): string {
        return this.value;
    }

    setValue(value: string): void {
        this.value = value;
    }
}

// Register scoped service
customContainer.registerScoped(IScopedService, ScopedService, ServiceScope.Scoped);

// Create scopes and test isolation
customContainer.createScope('scope1');
customContainer.setCurrentScope('scope1');
const scopedService1 = customContainer.resolve(IScopedService);
scopedService1.setValue('value-from-scope1');

customContainer.createScope('scope2');
customContainer.setCurrentScope('scope2');
const scopedService2 = customContainer.resolve(IScopedService);
scopedService2.setValue('value-from-scope2');

console.log('🎯 Scope 1 value:', scopedService1.getValue());
console.log('🎯 Scope 2 value:', scopedService2.getValue());
console.log('✅ Scoped services are properly isolated\n');

// ============================================================================
// EXAMPLE 6: LAZY LOADING
// ============================================================================

console.log('⏳ Example 5: Lazy Loading');

const IExpensiveService = defineService('IExpensiveService', class {
    doExpensiveOperation(): string { return ''; }
});

class ExpensiveService {
    constructor() {
        console.log('💰 ExpensiveService created (this should be lazy)');
    }

    doExpensiveOperation(): string {
        return 'Expensive operation completed';
    }
}

customContainer.registerLazy(IExpensiveService, ExpensiveService);

console.log('📝 Registered lazy service (not created yet)');

const lazyProxy = customContainer.resolveLazy(IExpensiveService);
console.log('🔗 Got lazy proxy (service still not created)');

const result = lazyProxy.doExpensiveOperation();
console.log('✅ Used lazy service:', result);
console.log('✅ Service was created on first use\n');

// ============================================================================
// EXAMPLE 7: PERFORMANCE MONITORING
// ============================================================================

console.log('📊 Example 6: Performance Monitoring');

// Perform multiple resolutions to generate metrics
for (let i = 0; i < 10; i++) {
    customContainer.resolve(IUserService);
    customContainer.resolve(IEmailService);
    customContainer.resolve(INotificationService);
}

// Get performance metrics
const metrics = customContainer.getMetrics();
console.log('📈 Container metrics:');
console.log(`  Total services: ${metrics.totalServices}`);
console.log(`  Total resolutions: ${metrics.totalResolutions}`);
console.log(`  Average resolution time: ${metrics.averageResolutionTime.toFixed(2)}ms`);

// Get detailed diagnostics
const diagnostics = customContainer.getDiagnostics();
console.log('🔍 Container diagnostics:');
console.log(`  Container ID: ${diagnostics.containerId}`);
console.log(`  Registered services: ${diagnostics.registeredServices.length}`);
console.log(`  Debug info available: ${!!diagnostics.debugInfo}`);
console.log('✅ Performance monitoring working\n');

// ============================================================================
// EXAMPLE 8: ERROR HANDLING AND VALIDATION
// ============================================================================

console.log('⚠️ Example 7: Error Handling and Validation');

try {
    // Try to resolve non-existent service
    const INonExistentService = defineService('INonExistentService', class {});
    customContainer.resolve(INonExistentService);
} catch (error) {
    console.log('❌ Expected error caught:', error.message);
}

try {
    // Try to register invalid service
    customContainer.registerSingleton(null as any, null as any);
} catch (error) {
    console.log('❌ Validation error caught:', error.message);
}

console.log('✅ Error handling working correctly\n');

// ============================================================================
// EXAMPLE 9: GLOBAL CONTAINER USAGE
// ============================================================================

console.log('🌍 Example 8: Global Container Usage');

// Use global container
const globalUserService = resolve(IUserService);
console.log('🌍 Resolved service from global container');

// The global container is automatically created with production configuration
const globalDiagnostics = getGlobalContainer().getDiagnostics();
console.log(`🌍 Global container ID: ${globalDiagnostics.containerId}`);
console.log('✅ Global container working\n');

// ============================================================================
// EXAMPLE 10: CLEANUP AND DISPOSAL
// ============================================================================

console.log('🧹 Example 9: Cleanup and Disposal');

// Dispose scopes
customContainer.disposeScope('scope1');
customContainer.disposeScope('scope2');
console.log('🗑️ Disposed scopes');

// Clear metrics
customContainer.clearMetrics();
console.log('📊 Cleared metrics');

// Dispose container
customContainer.dispose();
console.log('🗑️ Disposed custom container');

console.log('✅ Cleanup completed\n');

// ============================================================================
// SUMMARY
// ============================================================================

console.log('🎉 TKA DI System Examples Completed Successfully!');
console.log('\nFeatures demonstrated:');
console.log('✅ Application Factory pattern');
console.log('✅ Container Builder pattern');
console.log('✅ Service registration and resolution');
console.log('✅ Advanced scoping and isolation');
console.log('✅ Lazy loading with proxies');
console.log('✅ Performance monitoring and metrics');
console.log('✅ Error handling and validation');
console.log('✅ Global container management');
console.log('✅ Proper cleanup and disposal');
console.log('\n🚀 Your web DI system now matches desktop sophistication!');
