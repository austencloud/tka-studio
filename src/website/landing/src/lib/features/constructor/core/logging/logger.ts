/**
 * Core Logger Implementation
 *
 * The main logger implementation that handles log processing, context management,
 * and dispatching to transports.
 */

import { browser } from '$app/environment';
import {
  LogLevel,
  LOG_LEVEL_NAMES,
  type LogEntry,
  type LogEntryParams,
  type Logger,
  type LoggerConfig,
  type LoggerContext,
  type LogTransport,
  type PerformanceLogger,
  LogDomain
} from './types.js';
import {
  DEFAULT_LOGGER_CONFIG,
  CORRELATION_ID_PREFIX,
  SESSION_ID
} from './constants.js';
import { parseLogConfig } from './config.js';

/**
 * Implementation of the PerformanceLogger interface
 */
class PerformanceLoggerImpl implements PerformanceLogger {
  private logger: LoggerImpl;
  private operation: string;
  private startTime: number = 0;
  private checkpoints: Array<{ name: string; time: number; data?: Record<string, unknown> }> = [];
  private active: boolean = false;

  constructor(logger: LoggerImpl, operation: string) {
    this.logger = logger;
    this.operation = operation;
  }

  start(): void {
    this.startTime = performance.now();
    this.active = true;
    this.checkpoints = [];
  }

  checkpoint(name: string, data?: Record<string, unknown>): void {
    if (!this.active) return;

    const time = performance.now();
    this.checkpoints.push({
      name,
      time,
      data
    });

    // Log the checkpoint
    this.logger.debug(`Checkpoint: ${name}`, {
      data: {
        ...data,
        operation: this.operation,
        elapsedSinceStart: time - this.startTime,
        elapsedSincePrevious: this.checkpoints.length > 1
          ? time - this.checkpoints[this.checkpoints.length - 2].time
          : time - this.startTime
      }
    });
  }

  end(data?: Record<string, unknown>): void {
    if (!this.active) return;

    const endTime = performance.now();
    const duration = endTime - this.startTime;

    this.logger.info(`Completed: ${this.operation}`, {
      duration,
      startTime: this.startTime,
      endTime,
      data: {
        ...data,
        checkpoints: this.checkpoints.map(cp => ({
          name: cp.name,
          elapsedSinceStart: cp.time - this.startTime,
          ...cp.data
        }))
      }
    });

    this.active = false;
  }

  cancel(): void {
    this.active = false;
  }
}

/**
 * Main logger implementation
 */
export class LoggerImpl implements Logger {
  private config: LoggerConfig;
  private context: LoggerContext;
  private transports: LogTransport[] = [];

  constructor(source: string, config?: Partial<LoggerConfig>, context?: Partial<LoggerContext>) {
    // Initialize with default config
    this.config = { ...DEFAULT_LOGGER_CONFIG };

    // Apply provided config
    if (config) {
      this.setConfig(config);
    }

    // Initialize context
    this.context = {
      source,
      ...context
    };

    // Apply URL configuration if in browser
    if (browser) {
      const urlConfig = parseLogConfig();
      if (urlConfig) {
        this.setConfig(urlConfig);
      }
    }
  }

  /**
   * Set logger configuration
   */
  setConfig(config: Partial<LoggerConfig>): void {
    this.config = {
      ...this.config,
      ...config,
      // Merge arrays instead of replacing
      transports: [...(this.config.transports || []), ...(config.transports || [])]
    };
  }

  /**
   * Get current logger configuration
   */
  getConfig(): LoggerConfig {
    return { ...this.config };
  }

  /**
   * Check if a log level is enabled
   */
  isEnabled(level: LogLevel): boolean {
    return level >= this.config.minLevel;
  }

  /**
   * Create a child logger with inherited context
   */
  createChildLogger(source: string, context?: Partial<Omit<LoggerContext, 'source'>>): Logger {
    return new LoggerImpl(
      source,
      this.config,
      {
        ...this.context,
        source,
        // If parent has a correlationId, set it as parentCorrelationId in child
        ...(this.context.correlationId
          ? { parentCorrelationId: this.context.correlationId }
          : {}),
        ...context
      }
    );
  }

  /**
   * Create a new logger with additional context
   */
  withContext(context: Partial<LoggerContext>): Logger {
    return new LoggerImpl(
      context.source || this.context.source,
      this.config,
      {
        ...this.context,
        ...context
      }
    );
  }

  /**
   * Start a performance timer
   */
  startTimer(operation: string): PerformanceLogger {
    const timer = new PerformanceLoggerImpl(this, operation);
    timer.start();
    return timer;
  }

  /**
   * Log a trace message
   */
  trace(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    this.log(LogLevel.TRACE, message, params);
  }

  /**
   * Log a debug message
   */
  debug(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    this.log(LogLevel.DEBUG, message, params);
  }

  /**
   * Log an info message
   */
  info(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    this.log(LogLevel.INFO, message, params);
  }

  /**
   * Log a warning message
   */
  warn(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    this.log(LogLevel.WARN, message, params);
  }

  /**
   * Log an error message
   */
  error(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    this.log(LogLevel.ERROR, message, params);
  }

  /**
   * Log a fatal message
   */
  fatal(message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    this.log(LogLevel.FATAL, message, params);
  }

  /**
   * Log a pictograph-specific message
   */
  pictograph(message: string, params: {
    letter?: string;
    gridMode?: string;
    componentState?: string;
    renderMetrics?: LogEntry['renderMetrics'];
    error?: Error;
    data?: Record<string, unknown>;
  }): void {
    const { letter, gridMode, componentState, renderMetrics, error, data } = params;

    const level = error ? LogLevel.ERROR : LogLevel.INFO;

    this.log(level, message, {
      domain: LogDomain.PICTOGRAPH,
      letterContext: letter,
      gridMode,
      componentState,
      renderMetrics,
      error: error ? {
        message: error.message,
        name: error.name,
        stack: error.stack
      } : undefined,
      data
    });
  }

  /**
   * Log an SVG-specific error
   */
  svgError(message: string, params: {
    path?: string;
    component?: string;
    fallbackApplied?: boolean;
    error?: Error;
    data?: Record<string, unknown>;
  }): void {
    const { path, component, fallbackApplied, error, data } = params;

    this.error(message, {
      domain: LogDomain.SVG,
      error: error ? {
        message: error.message,
        name: error.name,
        stack: error.stack
      } : undefined,
      data: {
        ...data,
        path,
        component,
        fallbackApplied
      }
    });
  }

  /**
   * Log a state machine transition
   */
  transition(params: {
    machine: string;
    from: string;
    to: string;
    event: string;
    duration?: number;
    data?: Record<string, unknown>;
  }): void {
    const { machine, from, to, event, duration, data } = params;

    this.info(`Transition: ${from} → ${to} (${event})`, {
      domain: LogDomain.STATE,
      duration,
      data: {
        ...data,
        machine,
        from,
        to,
        event
      }
    });
  }

  /**
   * Core logging method
   */
  log(level: LogLevel, message: string, params?: Omit<LogEntryParams, 'message' | 'source'>): void {
    // Skip if level is below minimum
    if (!this.isEnabled(level)) return;

    // Skip if sampling is enabled and this log should be sampled out
    if (this.shouldSample(level)) return;

    // Create the log entry
    const entry = this.createLogEntry(level, message, params);

    // Send to all transports
    this.dispatchToTransports(entry);
  }

  /**
   * Create a log entry with all required fields
   */
  private createLogEntry(
    level: LogLevel,
    message: string,
    params?: Omit<LogEntryParams, 'message' | 'source'>
  ): LogEntry {
    const timestamp = Date.now();
    const correlationId = params?.correlationId || this.context.correlationId || this.generateCorrelationId();

    return {
      id: this.generateId(),
      timestamp,
      level,
      levelName: LOG_LEVEL_NAMES[level],
      message,
      source: this.context.source,
      domain: params?.domain || this.context.domain,
      correlationId,
      parentCorrelationId: params?.parentCorrelationId || this.context.parentCorrelationId,
      sessionId: SESSION_ID,
      // Include all other params
      ...params,
      // Merge data objects
      data: {
        ...(this.context.data || {}),
        ...(params?.data || {})
      }
    };
  }

  /**
   * Dispatch a log entry to all transports
   */
  private dispatchToTransports(entry: LogEntry): void {
    for (const transport of this.config.transports) {
      try {
        transport.log(entry);
      } catch (error) {
        // Don't use this.error here to avoid potential infinite loops
        console.error(`Error in transport ${transport.name}:`, error);
      }
    }
  }

  /**
   * Generate a unique ID for a log entry
   */
  private generateId(): string {
    return browser
      ? crypto.randomUUID()
      : `log_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
  }

  /**
   * Generate a correlation ID
   */
  private generateCorrelationId(): string {
    return `${CORRELATION_ID_PREFIX}_${Date.now().toString(36)}_${Math.random().toString(36).substring(2, 5)}`;
  }

  /**
   * Determine if a log should be sampled out based on sampling configuration
   */
  private shouldSample(level: LogLevel): boolean {
    const { sampling } = this.config;

    // If sampling is not configured or rate is 1.0, don't sample
    if (!sampling || sampling.rate >= 1.0) return false;

    // Never sample logs above the minimum sampling level
    if (level >= sampling.minLevel) return false;

    // Sample based on rate
    return Math.random() > sampling.rate;
  }
}

// Create the singleton logger instance
const rootLogger = new LoggerImpl('app');

// Export the singleton
export const logger = rootLogger;
