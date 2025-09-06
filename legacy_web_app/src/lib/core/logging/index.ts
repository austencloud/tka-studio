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
} from './types';

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
} from './constants';

// Export core logger
export { logger, LoggerImpl } from './logger';

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
} from './context';

// Export configuration utilities
export {
  parseLogConfig,
  createDefaultTransports,
  createDevTransports,
  createProdTransports,
  createLoggerConfig
} from './config';

// Export machine logger
export {
  createMachineInspector,
  withLogging,
  createLoggedActor
} from './machine-logger';

// Export error logger
export {
  ErrorSeverity,
  ErrorCategory,
  type AppError,
  errorLogger
} from './error-logger';

// Export transports
export * from './transports';
