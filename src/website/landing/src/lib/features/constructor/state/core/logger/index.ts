import { LogLevel } from './types.js';
import { logger } from './Logger.js';
export { LogLevel } from './types.js';
export type { Logger, LogEntry, LoggerConfig } from './types.js';
export { logger } from './Logger.js';

// Export convenience methods
export const debug = (source: string, message: string, data?: unknown): void =>
	logger.log({ level: LogLevel.DEBUG, source, message, data });

export const info = (source: string, message: string, data?: unknown): void =>
	logger.log({ level: LogLevel.INFO, source, message, data });

export const warn = (source: string, message: string, data?: unknown): void =>
	logger.log({ level: LogLevel.WARN, source, message, data });

export const error = (source: string, message: string, data?: unknown): void =>
	logger.log({ level: LogLevel.ERROR, source, message, data });
