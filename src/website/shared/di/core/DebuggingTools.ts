/**
 * 🔍 TKA DEBUGGING TOOLS
 *
 * Enterprise-grade debugging and monitoring tools for the dependency injection system.
 * Provides comprehensive logging, performance tracking, and diagnostic capabilities.
 */

import {
    DebugInfo,
    RegistrationEvent,
    ResolutionEvent,
    ScopeEvent,
    ErrorEvent,
    ResolutionContext
} from './types.js';

export class DebuggingTools {
    private readonly _containerId: string;
    private readonly _registrationHistory: RegistrationEvent[] = [];
    private readonly _resolutionHistory: ResolutionEvent[] = [];
    private readonly _scopeHistory: ScopeEvent[] = [];
    private readonly _errorHistory: ErrorEvent[] = [];

    private _debugMode = false;
    private _maxHistorySize = 1000;
    private _performanceThreshold = 10; // ms

    constructor(containerId: string) {
        this._containerId = containerId;
        this._debugMode = this._isDebugEnvironment();
    }

    // ============================================================================
    // REGISTRATION LOGGING
    // ============================================================================

    /**
     * Log service registration
     */
    logRegistration(serviceName: string, scope: string, implementationName?: string): void {
        const event: RegistrationEvent = {
            timestamp: new Date(),
            serviceName,
            scope: scope as any,
            implementationName,
            metadata: { containerId: this._containerId }
        };

        this._registrationHistory.push(event);
        this._trimHistory(this._registrationHistory);

        if (this._debugMode) {
            console.debug(`[DI:${this._containerId}] Registered ${serviceName} as ${scope}${implementationName ? ` -> ${implementationName}` : ''}`);
        }
    }

    /**
     * Log factory registration
     */
    logFactoryRegistration(serviceName: string, scope: string): void {
        this.logRegistration(serviceName, scope, 'Factory');
    }

    /**
     * Log instance registration
     */
    logInstanceRegistration(serviceName: string, instance: any): void {
        const instanceType = instance?.constructor?.name || 'Unknown';
        this.logRegistration(serviceName, 'instance', instanceType);
    }

    // ============================================================================
    // RESOLUTION LOGGING
    // ============================================================================

    /**
     * Record service resolution
     */
    recordResolution(serviceName: string, resolutionTime: number, success: boolean, error?: any): void {
        const event: ResolutionEvent = {
            timestamp: new Date(),
            serviceName,
            resolutionTime,
            success,
            fromCache: false, // Would be determined by resolver
            resolverUsed: 'Unknown', // Would be set by resolver
            context: this._createBasicContext(serviceName),
            error
        };

        this._resolutionHistory.push(event);
        this._trimHistory(this._resolutionHistory);

        // Log performance warnings
        if (resolutionTime > this._performanceThreshold) {
            console.warn(`[DI:${this._containerId}] Slow resolution: ${serviceName} took ${resolutionTime.toFixed(2)}ms`);
        }

        if (this._debugMode) {
            const status = success ? '✅' : '❌';
            console.debug(`[DI:${this._containerId}] ${status} Resolved ${serviceName} in ${resolutionTime.toFixed(2)}ms`);
        }

        if (error) {
            this._recordError(error, this._createBasicContext(serviceName));
        }
    }

    // ============================================================================
    // SCOPE LOGGING
    // ============================================================================

    /**
     * Log scope creation
     */
    logScopeCreation(scopeId: string): void {
        const event: ScopeEvent = {
            timestamp: new Date(),
            scopeId,
            action: 'created'
        };

        this._scopeHistory.push(event);
        this._trimHistory(this._scopeHistory);

        if (this._debugMode) {
            console.debug(`[DI:${this._containerId}] Created scope: ${scopeId}`);
        }
    }

    /**
     * Log scope disposal
     */
    logScopeDisposal(scopeId: string): void {
        const event: ScopeEvent = {
            timestamp: new Date(),
            scopeId,
            action: 'disposed'
        };

        this._scopeHistory.push(event);
        this._trimHistory(this._scopeHistory);

        if (this._debugMode) {
            console.debug(`[DI:${this._containerId}] Disposed scope: ${scopeId}`);
        }
    }

    // ============================================================================
    // CONTAINER LIFECYCLE LOGGING
    // ============================================================================

    /**
     * Log container creation
     */
    logContainerCreation(containerId: string, createdAt: Date): void {
        if (this._debugMode) {
            console.info(`[DI:${containerId}] Container created at ${createdAt.toISOString()}`);
        }
    }

    /**
     * Log container disposal
     */
    logContainerDisposal(containerId: string): void {
        if (this._debugMode) {
            console.info(`[DI:${containerId}] Container disposed`);
        }
    }

    // ============================================================================
    // DEBUGGING AND DIAGNOSTICS
    // ============================================================================

    /**
     * Get comprehensive debug information
     */
    getDebugInfo(): DebugInfo {
        return {
            containerId: this._containerId,
            registrationHistory: [...this._registrationHistory],
            resolutionHistory: [...this._resolutionHistory],
            scopeHistory: [...this._scopeHistory],
            errorHistory: [...this._errorHistory]
        };
    }

    /**
     * Get performance statistics
     */
    getPerformanceStats() {
        const resolutions = this._resolutionHistory;
        const successful = resolutions.filter(r => r.success);
        const failed = resolutions.filter(r => !r.success);

        const times = successful.map(r => r.resolutionTime);
        const avgTime = times.length > 0 ? times.reduce((a, b) => a + b, 0) / times.length : 0;
        const minTime = times.length > 0 ? Math.min(...times) : 0;
        const maxTime = times.length > 0 ? Math.max(...times) : 0;

        return {
            totalResolutions: resolutions.length,
            successfulResolutions: successful.length,
            failedResolutions: failed.length,
            successRate: resolutions.length > 0 ? (successful.length / resolutions.length) * 100 : 0,
            averageResolutionTime: avgTime,
            minResolutionTime: minTime,
            maxResolutionTime: maxTime,
            slowResolutions: successful.filter(r => r.resolutionTime > this._performanceThreshold).length
        };
    }

    /**
     * Get service usage statistics
     */
    getServiceUsageStats() {
        const usage = new Map<string, { count: number; totalTime: number; errors: number }>();

        for (const resolution of this._resolutionHistory) {
            const stats = usage.get(resolution.serviceName) || { count: 0, totalTime: 0, errors: 0 };
            stats.count++;
            stats.totalTime += resolution.resolutionTime;
            if (!resolution.success) stats.errors++;
            usage.set(resolution.serviceName, stats);
        }

        return Object.fromEntries(
            Array.from(usage.entries()).map(([service, stats]) => [
                service,
                {
                    ...stats,
                    averageTime: stats.totalTime / stats.count,
                    errorRate: (stats.errors / stats.count) * 100
                }
            ])
        );
    }

    /**
     * Export debug data for analysis
     */
    exportDebugData() {
        return {
            containerId: this._containerId,
            exportedAt: new Date().toISOString(),
            debugInfo: this.getDebugInfo(),
            performanceStats: this.getPerformanceStats(),
            serviceUsageStats: this.getServiceUsageStats(),
            configuration: {
                debugMode: this._debugMode,
                maxHistorySize: this._maxHistorySize,
                performanceThreshold: this._performanceThreshold
            }
        };
    }

    // ============================================================================
    // CONFIGURATION
    // ============================================================================

    /**
     * Enable or disable debug mode
     */
    setDebugMode(enabled: boolean): void {
        this._debugMode = enabled;
        console.info(`[DI:${this._containerId}] Debug mode ${enabled ? 'enabled' : 'disabled'}`);
    }

    /**
     * Set maximum history size
     */
    setMaxHistorySize(size: number): void {
        this._maxHistorySize = Math.max(100, size);
        this._trimAllHistories();
    }

    /**
     * Set performance threshold for warnings
     */
    setPerformanceThreshold(threshold: number): void {
        this._performanceThreshold = Math.max(1, threshold);
    }

    // ============================================================================
    // CLEANUP
    // ============================================================================

    /**
     * Clear all debug history
     */
    clearHistory(): void {
        this._registrationHistory.length = 0;
        this._resolutionHistory.length = 0;
        this._scopeHistory.length = 0;
        this._errorHistory.length = 0;
    }

    /**
     * Dispose debugging tools
     */
    dispose(): void {
        this.clearHistory();
        if (this._debugMode) {
            console.info(`[DI:${this._containerId}] Debugging tools disposed`);
        }
    }

    // ============================================================================
    // PRIVATE UTILITIES
    // ============================================================================

    private _recordError(error: any, context: ResolutionContext): void {
        const errorEvent: ErrorEvent = {
            timestamp: new Date(),
            error: error instanceof Error ? error : new Error(String(error)),
            context,
            stackTrace: error?.stack || new Error().stack || 'No stack trace available'
        };

        this._errorHistory.push(errorEvent);
        this._trimHistory(this._errorHistory);
    }

    private _createBasicContext(serviceName: string): ResolutionContext {
        return {
            serviceInterface: { name: serviceName, symbol: Symbol(serviceName), type: class {} },
            containerId: this._containerId,
            resolutionStack: [],
            resolutionDepth: 0,
            timestamp: new Date()
        };
    }

    private _trimHistory<T>(history: T[]): void {
        if (history.length > this._maxHistorySize) {
            history.splice(0, history.length - this._maxHistorySize);
        }
    }

    private _trimAllHistories(): void {
        this._trimHistory(this._registrationHistory);
        this._trimHistory(this._resolutionHistory);
        this._trimHistory(this._scopeHistory);
        this._trimHistory(this._errorHistory);
    }

    private _isDebugEnvironment(): boolean {
        // Check various debug indicators
        if (typeof window !== 'undefined') {
            return !!(window as any).__TKA_DEBUG__ ||
                   location.hostname === 'localhost' ||
                   location.hostname === '127.0.0.1';
        }

        if (typeof process !== 'undefined') {
            return process.env.NODE_ENV === 'development' ||
                   process.env.TKA_DEBUG === 'true';
        }

        return false;
    }
}
