/**
 * Logging System Index
 *
 * Main entry point for the structured logging system.
 */

// Export types
export {
  LogLevel,
  LogDomain,
  type LogEntry,
  type LogEntryParams,
  type Logger,
  type LoggerConfig,
  type LoggerContext,
  type LogTransport,
  type PerformanceLogger,
  type MachineLoggerOptions,
  type ComponentLoggerOptions
} from './types.js';

// Export constants
export {
  DEFAULT_LOG_LEVEL,
  DEFAULT_LOGGER_CONFIG,
  LOG_URL_PARAM,
  MAX_MEMORY_LOGS,
  MAX_STORAGE_LOGS,
  STORAGE_KEY,
  CORRELATION_ID_PREFIX,
  SESSION_ID,
  CONSOLE_COLORS,
  CONSOLE_SYMBOLS,
  DOMAIN_COLORS,
  PERFORMANCE_THRESHOLDS
} from './constants.js';

// Export core logger
export { logger, LoggerImpl } from './logger.js';

// Export context utilities
export {
  setGlobalContext,
  getGlobalContext,
  addGlobalContextData,
  clearGlobalContext,
  createDomainContext,
  createPictographContext,
  createSequenceContext,
  createSvgContext,
  createStateContext,
  createComponentContext,
  gatherAutomaticContext,
  initializeGlobalContext
} from './context.js';

// Export configuration utilities
export {
  parseLogConfig,
  createDefaultTransports,
  createDevTransports,
  createProdTransports,
  createLoggerConfig
} from './config.js';

// Export machine logger
export {
  createMachineInspector,
  withLogging,
  createLoggedActor
} from './machine-logger.js';

// Export error logger
export {
  ErrorSeverity,
  ErrorCategory,
  type AppError,
  errorLogger
} from './error-logger.js';

// Export transports
export * from './transports.js';
