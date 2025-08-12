/**
 * 📊 TKA SERVICE METRICS
 *
 * Advanced performance monitoring and metrics collection for the dependency injection system.
 */

import { ServiceMetrics as IServiceMetrics, ContainerMetrics } from './types.js';

export class ServiceMetrics {
    private readonly _serviceMetrics = new Map<string, ServiceMetricsData>();
    private readonly _containerId: string;
    private readonly _createdAt = new Date();
    private _lastActivity: Date | null = null;

    constructor(containerId?: string) {
        this._containerId = containerId || 'unknown';
    }

    /**
     * Record a service resolution
     */
    recordResolution(serviceName: string, resolutionTime: number, success: boolean): void {
        let metrics = this._serviceMetrics.get(serviceName);
        if (!metrics) {
            metrics = new ServiceMetricsData(serviceName);
            this._serviceMetrics.set(serviceName, metrics);
        }

        metrics.recordResolution(resolutionTime, success);
        this._lastActivity = new Date();
    }

    /**
     * Record a cache hit
     */
    recordCacheHit(serviceName: string): void {
        const metrics = this._serviceMetrics.get(serviceName);
        if (metrics) {
            metrics.recordCacheHit();
        }
    }

    /**
     * Get metrics for a specific service
     */
    getServiceMetrics(serviceName: string): IServiceMetrics | null {
        const metrics = this._serviceMetrics.get(serviceName);
        return metrics ? metrics.toInterface() : null;
    }

    /**
     * Get all service metrics
     */
    getAllServiceMetrics(): Map<string, IServiceMetrics> {
        const result = new Map<string, IServiceMetrics>();
        for (const [name, metrics] of this._serviceMetrics) {
            result.set(name, metrics.toInterface());
        }
        return result;
    }

    /**
     * Get container-wide metrics
     */
    getMetrics(): ContainerMetrics {
        const serviceMetrics = new Map<string, IServiceMetrics>();
        let totalResolutions = 0;
        let totalResolutionTime = 0;

        for (const [name, metrics] of this._serviceMetrics) {
            const serviceMetric = metrics.toInterface();
            serviceMetrics.set(name, serviceMetric);
            totalResolutions += serviceMetric.totalResolutions;
            totalResolutionTime += serviceMetric.averageResolutionTime * serviceMetric.totalResolutions;
        }

        const averageResolutionTime = totalResolutions > 0 ? totalResolutionTime / totalResolutions : 0;

        return {
            containerId: this._containerId,
            totalServices: this._serviceMetrics.size,
            totalResolutions,
            averageResolutionTime,
            serviceMetrics,
            createdAt: this._createdAt,
            lastActivity: this._lastActivity
        };
    }

    /**
     * Get performance summary
     */
    getPerformanceSummary() {
        const metrics = this.getMetrics();
        const services = Array.from(metrics.serviceMetrics.values());

        const slowServices = services
            .filter(s => s.averageResolutionTime > 10)
            .sort((a, b) => b.averageResolutionTime - a.averageResolutionTime);

        const errorProneServices = services
            .filter(s => s.failedResolutions > 0)
            .sort((a, b) => (b.failedResolutions / b.totalResolutions) - (a.failedResolutions / a.totalResolutions));

        const mostUsedServices = services
            .sort((a, b) => b.totalResolutions - a.totalResolutions)
            .slice(0, 10);

        return {
            totalServices: metrics.totalServices,
            totalResolutions: metrics.totalResolutions,
            averageResolutionTime: metrics.averageResolutionTime,
            slowServices: slowServices.slice(0, 5),
            errorProneServices: errorProneServices.slice(0, 5),
            mostUsedServices,
            overallSuccessRate: this._calculateOverallSuccessRate(services)
        };
    }

    /**
     * Clear all metrics
     */
    clear(): void {
        this._serviceMetrics.clear();
        this._lastActivity = null;
    }

    /**
     * Export metrics data
     */
    export() {
        return {
            containerId: this._containerId,
            createdAt: this._createdAt,
            lastActivity: this._lastActivity,
            exportedAt: new Date(),
            metrics: this.getMetrics(),
            summary: this.getPerformanceSummary()
        };
    }

    private _calculateOverallSuccessRate(services: IServiceMetrics[]): number {
        const totalResolutions = services.reduce((sum, s) => sum + s.totalResolutions, 0);
        const totalSuccessful = services.reduce((sum, s) => sum + s.successfulResolutions, 0);
        return totalResolutions > 0 ? (totalSuccessful / totalResolutions) * 100 : 100;
    }
}

/**
 * Internal metrics data for a single service
 */
class ServiceMetricsData {
    private readonly _serviceName: string;
    private _totalResolutions = 0;
    private _successfulResolutions = 0;
    private _failedResolutions = 0;
    private _totalResolutionTime = 0;
    private _minResolutionTime = Number.MAX_VALUE;
    private _maxResolutionTime = 0;
    private _lastResolutionTime: Date | null = null;
    private _cacheHits = 0;

    constructor(serviceName: string) {
        this._serviceName = serviceName;
    }

    recordResolution(resolutionTime: number, success: boolean): void {
        this._totalResolutions++;
        this._totalResolutionTime += resolutionTime;
        this._lastResolutionTime = new Date();

        if (success) {
            this._successfulResolutions++;
        } else {
            this._failedResolutions++;
        }

        // Update min/max times only for successful resolutions
        if (success) {
            this._minResolutionTime = Math.min(this._minResolutionTime, resolutionTime);
            this._maxResolutionTime = Math.max(this._maxResolutionTime, resolutionTime);
        }
    }

    recordCacheHit(): void {
        this._cacheHits++;
    }

    toInterface(): IServiceMetrics {
        const averageResolutionTime = this._successfulResolutions > 0
            ? this._totalResolutionTime / this._successfulResolutions
            : 0;

        const cacheHitRate = (this._totalResolutions + this._cacheHits) > 0
            ? (this._cacheHits / (this._totalResolutions + this._cacheHits)) * 100
            : 0;

        return {
            serviceName: this._serviceName,
            totalResolutions: this._totalResolutions,
            successfulResolutions: this._successfulResolutions,
            failedResolutions: this._failedResolutions,
            averageResolutionTime,
            minResolutionTime: this._minResolutionTime === Number.MAX_VALUE ? 0 : this._minResolutionTime,
            maxResolutionTime: this._maxResolutionTime,
            lastResolutionTime: this._lastResolutionTime,
            cacheHitRate
        };
    }
}
