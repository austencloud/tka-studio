export enum LogLevel {
	DEBUG = 'debug',
	INFO = 'info',
	WARN = 'warn',
	ERROR = 'error'
}

export interface LogEntry {
	level: LogLevel;
	source: string;
	message: string;
	data?: unknown;
	timestamp: number;
}

export interface LoggerConfig {
	minLevel?: LogLevel;
	enabledSources?: string[];
	format?: (entry: LogEntry) => string;
}

export interface Logger {
	log(entry: Omit<LogEntry, 'timestamp'>): void;
	isEnabled(source: string, level: LogLevel): boolean;
	setConfig(config: Partial<LoggerConfig>): void;
}
