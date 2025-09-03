import { LogLevel } from './types';
import { logger } from './Logger';

export const debug = (source: string, message: string, data?: unknown): void => {
	logger.log({ level: LogLevel.DEBUG, source, message, data });
};

export const info = (source: string, message: string, data?: unknown): void => {
	logger.log({ level: LogLevel.INFO, source, message, data });
};

export const warn = (source: string, message: string, data?: unknown): void => {
	logger.log({ level: LogLevel.WARN, source, message, data });
};

export const error = (source: string, message: string, data?: unknown): void => {
	logger.log({ level: LogLevel.ERROR, source, message, data });
};
