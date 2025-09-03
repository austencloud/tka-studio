/**
 * Error Logger
 *
 * Enhanced error logging with categorization, grouping, and recovery suggestions.
 */

import { browser } from '$app/environment';
import { logger } from './logger';
import { LogDomain, LogLevel } from './types';

/**
 * Error severity levels
 */
export enum ErrorSeverity {
	INFO = 'info',
	WARNING = 'warning',
	ERROR = 'error',
	CRITICAL = 'critical'
}

/**
 * Error categories for domain-specific errors
 */
export enum ErrorCategory {
	// General categories
	NETWORK = 'network',
	VALIDATION = 'validation',
	AUTHORIZATION = 'authorization',
	RESOURCE = 'resource',
	TIMEOUT = 'timeout',
	UNEXPECTED = 'unexpected',

	// TKA-specific categories
	PICTOGRAPH_RENDERING = 'pictograph_rendering',
	SVG_LOADING = 'svg_loading',
	SEQUENCE_VALIDATION = 'sequence_validation',
	MOTION_DATA = 'motion_data',
	STATE_TRANSITION = 'state_transition',
	COMPONENT_INITIALIZATION = 'component_initialization'
}

/**
 * Application error interface
 */
export interface AppError {
	id: string;
	source: string;
	message: string;
	timestamp: number;
	stack?: string;
	severity: ErrorSeverity;
	category?: ErrorCategory;
	context?: Record<string, any>;
	recoverable?: boolean;
	recoverySuggestion?: string;
	errorCode?: string;
}

/**
 * Error logger implementation
 */
export class ErrorLogger {
	private errors: AppError[] = [];
	private maxErrorCount: number;
	private isProduction: boolean;

	constructor(maxErrorCount: number = 100) {
		this.maxErrorCount = maxErrorCount;
		this.isProduction = import.meta.env.PROD;

		// Set up global error handlers if in browser
		if (browser) {
			this.setupGlobalErrorHandlers();
		}
	}

	/**
	 * Log an error with comprehensive details
	 */
	log(error: Omit<AppError, 'id' | 'timestamp'>): void {
		const newError: AppError = {
			id: browser ? crypto.randomUUID() : `error-${Date.now()}`,
			timestamp: Date.now(),
			...error
		};

		// Trim error list if it exceeds max count
		if (this.errors.length >= this.maxErrorCount) {
			this.errors.shift();
		}

		this.errors.push(newError);

		// Log to the unified logger
		this.logToUnifiedLogger(newError);
	}

	/**
	 * Get all current errors
	 */
	getErrors(): AppError[] {
		return [...this.errors];
	}

	/**
	 * Clear all stored errors
	 */
	clearErrors(): void {
		this.errors = [];
	}

	/**
	 * Create an error from an unknown error object
	 */
	createError(
		source: string,
		error: unknown,
		severity: ErrorSeverity = ErrorSeverity.ERROR,
		category?: ErrorCategory
	): AppError {
		if (error instanceof Error) {
			return {
				id: browser ? crypto.randomUUID() : `error-${Date.now()}`,
				source,
				message: error.message,
				stack: error.stack,
				timestamp: Date.now(),
				severity,
				category,
				context: (error as any).context
			};
		}

		return {
			id: browser ? crypto.randomUUID() : `error-${Date.now()}`,
			source,
			message: String(error),
			timestamp: Date.now(),
			severity,
			category
		};
	}

	/**
	 * Log an error to the unified logger
	 */
	private logToUnifiedLogger(error: AppError): void {
		// Map severity to log level
		const level = this.mapSeverityToLogLevel(error.severity);

		// Determine domain based on source or category
		const domain = this.determineDomain(error);

		const srcLogger = logger.createChildLogger(error.source);

		srcLogger.log(level, error.message, {
			domain,
			error: {
				message: error.message,
				stack: error.stack,
				name: error.category || 'Error'
			},
			data: {
				...error.context,
				severity: error.severity,
				category: error.category,
				recoverable: error.recoverable,
				recoverySuggestion: error.recoverySuggestion,
				errorCode: error.errorCode
			}
		});

		// For critical errors in production, we might want to report to an external service
		if (this.isProduction && error.severity === ErrorSeverity.CRITICAL) {
			this.reportCriticalError(error);
		}
	}

	/**
	 * Map error severity to log level
	 */
	private mapSeverityToLogLevel(severity: ErrorSeverity): LogLevel {
		switch (severity) {
			case ErrorSeverity.INFO:
				return LogLevel.INFO;
			case ErrorSeverity.WARNING:
				return LogLevel.WARN;
			case ErrorSeverity.ERROR:
				return LogLevel.ERROR;
			case ErrorSeverity.CRITICAL:
				return LogLevel.FATAL;
			default:
				return LogLevel.ERROR;
		}
	}

	/**
	 * Determine the appropriate log domain based on error details
	 */
	private determineDomain(error: AppError): LogDomain | undefined {
		// Check category first
		if (error.category) {
			switch (error.category) {
				case ErrorCategory.PICTOGRAPH_RENDERING:
					return LogDomain.PICTOGRAPH;
				case ErrorCategory.SVG_LOADING:
					return LogDomain.SVG;
				case ErrorCategory.SEQUENCE_VALIDATION:
				case ErrorCategory.MOTION_DATA:
					return LogDomain.SEQUENCE;
				case ErrorCategory.STATE_TRANSITION:
					return LogDomain.STATE;
				case ErrorCategory.COMPONENT_INITIALIZATION:
					return LogDomain.COMPONENT;
			}
		}

		// Check source if category doesn't map to a domain
		const source = error.source.toLowerCase();
		if (source.includes('pictograph')) {
			return LogDomain.PICTOGRAPH;
		} else if (source.includes('svg')) {
			return LogDomain.SVG;
		} else if (source.includes('sequence')) {
			return LogDomain.SEQUENCE;
		} else if (source.includes('machine') || source.includes('state')) {
			return LogDomain.STATE;
		} else if (source.includes('component')) {
			return LogDomain.COMPONENT;
		}

		// Default to system domain
		return LogDomain.SYSTEM;
	}

	/**
	 * Report critical errors to external service
	 */
	private reportCriticalError(error: AppError): void {
		// Placeholder for external error reporting (e.g., Sentry, LogRocket)
		console.warn('Critical Error Reported:', error);

		// In a real implementation, you would send this to your error tracking service
		// Example: Sentry.captureException(error);
	}

	/**
	 * Set up global error handlers
	 */
	private setupGlobalErrorHandlers(): void {
		// Handle uncaught exceptions
		window.addEventListener('error', (event) => {
			this.log({
				source: 'window.onerror',
				message: event.message || 'Uncaught exception',
				stack: event.error?.stack,
				severity: ErrorSeverity.ERROR,
				category: ErrorCategory.UNEXPECTED,
				context: {
					filename: event.filename,
					lineno: event.lineno,
					colno: event.colno
				}
			});
		});

		// Handle unhandled promise rejections
		window.addEventListener('unhandledrejection', (event) => {
			const error = event.reason instanceof Error ? event.reason : new Error(String(event.reason));

			this.log({
				source: 'unhandledrejection',
				message: error.message || 'Unhandled promise rejection',
				stack: error.stack,
				severity: ErrorSeverity.ERROR,
				category: ErrorCategory.UNEXPECTED,
				context: {
					reason: event.reason
				}
			});
		});
	}
}

// Create singleton instance
export const errorLogger = new ErrorLogger();
