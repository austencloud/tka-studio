/**
 * Logging System Types
 *
 * Core type definitions for the structured logging system.
 */

/**
 * Log levels with numeric values for comparison
 */
export enum LogLevel {
	TRACE = 0,
	DEBUG = 1,
	INFO = 2,
	WARN = 3,
	ERROR = 4,
	FATAL = 5,
	NONE = 100 // Special level to disable logging
}

/**
 * String representation of log levels
 */
export type LogLevelString = 'trace' | 'debug' | 'info' | 'warn' | 'error' | 'fatal' | 'none';

/**
 * Mapping between string and enum log levels
 */
export const LOG_LEVEL_MAP: Record<LogLevelString, LogLevel> = {
	trace: LogLevel.TRACE,
	debug: LogLevel.DEBUG,
	info: LogLevel.INFO,
	warn: LogLevel.WARN,
	error: LogLevel.ERROR,
	fatal: LogLevel.FATAL,
	none: LogLevel.NONE
};

/**
 * Mapping between enum and string log levels
 */
export const LOG_LEVEL_NAMES: Record<LogLevel, LogLevelString> = {
	[LogLevel.TRACE]: 'trace',
	[LogLevel.DEBUG]: 'debug',
	[LogLevel.INFO]: 'info',
	[LogLevel.WARN]: 'warn',
	[LogLevel.ERROR]: 'error',
	[LogLevel.FATAL]: 'fatal',
	[LogLevel.NONE]: 'none'
};

/**
 * TKA-specific logging domains
 */
export enum LogDomain {
	APP = 'app',
	PICTOGRAPH = 'pictograph',
	SEQUENCE = 'sequence',
	MOTION = 'motion',
	SVG = 'svg',
	STATE = 'state',
	COMPONENT = 'component',
	SYSTEM = 'system'
}

/**
 * Base log entry interface
 */
export interface LogEntry {
	// Standard fields
	id: string;
	timestamp: number;
	level: LogLevel;
	levelName: LogLevelString;
	message: string;
	source: string;
	domain?: LogDomain;

	// Context information
	correlationId?: string;
	parentCorrelationId?: string;
	sessionId?: string;
	userId?: string;

	// Error information
	error?: {
		name?: string;
		message: string;
		stack?: string;
		cause?: unknown;
	};

	// Performance information
	duration?: number;
	startTime?: number;
	endTime?: number;

	// TKA-specific fields
	letterContext?: string;
	gridMode?: string;
	motionData?: unknown;
	componentState?: string;
	renderMetrics?: {
		renderTime?: number;
		frameRate?: number;
		componentsLoaded?: number;
		totalComponents?: number;
	};

	// Additional data
	data?: Record<string, unknown>;
}

/**
 * Log entry creation parameters (subset of fields that are required when creating a log)
 */
export type LogEntryParams = Pick<LogEntry, 'message' | 'source'> &
	Partial<Omit<LogEntry, 'id' | 'timestamp' | 'level' | 'levelName' | 'message' | 'source'>>;

/**
 * Logger context information
 */
export interface LoggerContext {
	source: string;
	domain?: LogDomain;
	correlationId?: string;
	parentCorrelationId?: string;
	data?: Record<string, unknown>;
}

/**
 * Logger configuration
 */
export interface LoggerConfig {
	minLevel: LogLevel;
	enabledSources?: string[];
	enabledDomains?: LogDomain[];
	disabledSources?: string[];
	disabledDomains?: LogDomain[];
	transports: LogTransport[];
	includeTimestamps?: boolean;
	includeCorrelationIds?: boolean;
	prettyPrint?: boolean;
	sampling?: {
		rate: number;
		minLevel: LogLevel;
	};
	startTime?: number; // Added startTime property to track when logger was initialized
}

/**
 * Transport interface for log output destinations
 */
export interface LogTransport {
	name: string;
	log(entry: LogEntry): void;
	flush?(): Promise<void>;
	clear?(): void;
	getEntries?(): LogEntry[];
}

/**
 * Core logger interface
 */
export interface Logger {
	// Basic logging methods
	trace(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;
	debug(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;
	info(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;
	warn(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;
	error(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;
	fatal(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;

	// Log with explicit level
	log(level: LogLevel, message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void;

	// Context management
	withContext(context: Partial<LoggerContext>): Logger;

	// Performance tracking
	startTimer(operation: string): PerformanceLogger;

	// TKA-specific logging methods
	pictograph(
		message: string,
		params: {
			letter?: string;
			gridMode?: string;
			componentState?: string;
			renderMetrics?: LogEntry['renderMetrics'];
			error?: Error;
			data?: Record<string, unknown>;
		}
	): void;

	svgError(
		message: string,
		params: {
			path?: string;
			component?: string;
			fallbackApplied?: boolean;
			error?: Error;
			data?: Record<string, unknown>;
		}
	): void;

	transition(params: {
		machine: string;
		from: string;
		to: string;
		event: string;
		duration?: number;
		data?: Record<string, unknown>;
	}): void;

	// Configuration
	setConfig(config: Partial<LoggerConfig>): void;
	getConfig(): LoggerConfig;

	// Utility methods
	isEnabled(level: LogLevel): boolean;
	createChildLogger(source: string, context?: Partial<Omit<LoggerContext, 'source'>>): Logger;
}

/**
 * Performance logger interface for timing operations
 */
export interface PerformanceLogger {
	start(): void;
	end(data?: Record<string, unknown>): void;
	checkpoint(name: string, data?: Record<string, unknown>): void;
	cancel(): void;
}

/**
 * Machine logger configuration
 */
export interface MachineLoggerOptions {
  name: string;
  level?: LogLevel;
  includedEvents?: string[];
  excludedEvents?: string[];
  contextFields?: string[];
  includeSnapshots?: boolean;
  logTransitions?: boolean;
  performanceTracking?: {
    enabled: boolean;  // This was the issue - it was requiring this to be defined
    transitionThreshold?: number;
  };
}

/**
 * Component logger options
 */
export interface ComponentLoggerOptions {
	enableTiming?: boolean;
	domainType?: LogDomain;
	trackLifecycle?: boolean;
	trackRenders?: boolean;
	trackErrors?: boolean;
	context?: Record<string, unknown>;
}
