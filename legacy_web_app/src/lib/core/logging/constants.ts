/**
 * Logging System Constants
 *
 * Shared constants for the structured logging system.
 */

import { LogLevel, type LoggerConfig } from './types';
import { browser } from '$app/environment';
import { loggingConfig } from '$lib/config/logging';

/**
 * Default log level based on environment
 */
export const DEFAULT_LOG_LEVEL = loggingConfig.defaultLogLevel;

/**
 * Default configuration for the logger
 */
export const DEFAULT_LOGGER_CONFIG: LoggerConfig = {
	minLevel: DEFAULT_LOG_LEVEL,
	transports: [],
	includeTimestamps: true,
	includeCorrelationIds: true,
	prettyPrint: import.meta.env.DEV,
	sampling: {
		rate: 1.0, // Log everything by default
		minLevel: LogLevel.TRACE
	}
};

/**
 * URL parameter name for log configuration
 */
export const LOG_URL_PARAM = 'log';

/**
 * Maximum number of logs to keep in memory buffer
 */
export const MAX_MEMORY_LOGS = 1000;

/**
 * Maximum number of logs to keep in localStorage
 */
export const MAX_STORAGE_LOGS = 500;

/**
 * LocalStorage key for logs
 */
export const STORAGE_KEY = 'tka_logs';

/**
 * Default correlation ID prefix
 */
export const CORRELATION_ID_PREFIX = 'corr';

/**
 * Default session ID
 */
export const SESSION_ID = browser ? `session_${Date.now().toString(36)}` : 'server';

/**
 * Console colors for different log levels (for pretty printing)
 */
export const CONSOLE_COLORS: Record<LogLevel, string> = {
	[LogLevel.TRACE]: '#6c757d', // Gray
	[LogLevel.DEBUG]: '#17a2b8', // Cyan
	[LogLevel.INFO]: '#0d6efd', // Blue
	[LogLevel.WARN]: '#ffc107', // Yellow
	[LogLevel.ERROR]: '#dc3545', // Red
	[LogLevel.FATAL]: '#7c0101', // Dark red
	[LogLevel.NONE]: '#000000' // Black
};

/**
 * Console symbols for different log levels (for pretty printing)
 */
export const CONSOLE_SYMBOLS = {
	[LogLevel.TRACE]: '🔍',
	[LogLevel.DEBUG]: '🐞',
	[LogLevel.INFO]: 'ℹ️',
	[LogLevel.WARN]: '⚠️',
	[LogLevel.ERROR]: '❌',
	[LogLevel.FATAL]: '💀',
	[LogLevel.NONE]: ''
};

/**
 * Domain colors for visualization
 */
export const DOMAIN_COLORS = {
	app: '#4285F4', // Google Blue
	pictograph: '#EA4335', // Google Red
	sequence: '#FBBC05', // Google Yellow
	motion: '#34A853', // Google Green
	svg: '#8F00FF', // Violet
	state: '#FF6D01', // Orange
	component: '#00BCD4', // Cyan
	system: '#757575' // Gray
};

/**
 * Performance thresholds in milliseconds
 */
export const PERFORMANCE_THRESHOLDS = {
	GOOD: 50, // Under 50ms is good
	WARNING: 100, // 50-100ms is a warning
	POOR: 200 // Over 200ms is poor
};
