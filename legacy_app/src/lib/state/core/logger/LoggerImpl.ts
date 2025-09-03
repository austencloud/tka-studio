import { LogLevel, type LogEntry, type Logger, type LoggerConfig } from './types';

export class LoggerImpl implements Logger {
	private config: LoggerConfig = {
		minLevel: LogLevel.INFO,
		enabledSources: undefined,
		format: (entry) =>
			`[${entry.level.toUpperCase()}] ${entry.source}: ${entry.message}${
				entry.data ? ` ${JSON.stringify(entry.data)}` : ''
			}`
	};

	log(entry: Omit<LogEntry, 'timestamp'>): void {
		if (!this.isEnabled(entry.source, entry.level)) return;

		const fullEntry: LogEntry = {
			...entry,
			timestamp: Date.now()
		};

		const formatted = this.config.format!(fullEntry);
		const method = this.getConsoleMethod(entry.level);

		// eslint-disable-next-line no-console
		console[method](formatted);
	}

	isEnabled(source: string, level: LogLevel): boolean {
		if (this.config.enabledSources && !this.config.enabledSources.includes(source)) {
			return false;
		}

		const levels = Object.values(LogLevel);
		const minLevelIndex = levels.indexOf(this.config.minLevel ?? LogLevel.INFO);
		const currentLevelIndex = levels.indexOf(level);

		return currentLevelIndex >= minLevelIndex;
	}

	setConfig(config: Partial<LoggerConfig>): void {
		this.config = {
			...this.config,
			...config
		};
	}

	private getConsoleMethod(level: LogLevel): 'debug' | 'info' | 'warn' | 'error' {
		switch (level) {
			case LogLevel.DEBUG:
				return 'debug';
			case LogLevel.INFO:
				return 'info';
			case LogLevel.WARN:
				return 'warn';
			case LogLevel.ERROR:
				return 'error';
		}
	}
}
