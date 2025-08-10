/**
 * Error Handling Service for Legacy Web Application
 * 
 * Provides centralized error handling, logging, and reporting functionality.
 */

export enum ErrorSeverity {
	CRITICAL = 'CRITICAL',
	ERROR = 'ERROR',
	WARNING = 'WARNING',
	INFO = 'INFO'
}

export interface ErrorReport {
	message: string;
	severity: ErrorSeverity;
	source: string;
	timestamp?: Date;
	context?: Record<string, any>;
	stack?: string;
}

export interface ErrorHandlingOptions {
	logToConsole?: boolean;
	reportToService?: boolean;
	showUserNotification?: boolean;
}

/**
 * Centralized error handling service
 */
class ErrorHandlingService {
	private errorReports: ErrorReport[] = [];
	private maxReports = 100; // Keep last 100 error reports
	private options: ErrorHandlingOptions = {
		logToConsole: true,
		reportToService: false,
		showUserNotification: false
	};

	/**
	 * Configure error handling options
	 */
	configure(options: Partial<ErrorHandlingOptions>): void {
		this.options = { ...this.options, ...options };
	}

	/**
	 * Report an error
	 */
	reportError(report: Omit<ErrorReport, 'timestamp'>): void {
		const fullReport: ErrorReport = {
			...report,
			timestamp: new Date()
		};

		// Add to internal storage
		this.addToReports(fullReport);

		// Log to console if enabled
		if (this.options.logToConsole) {
			this.logToConsole(fullReport);
		}

		// Report to external service if enabled
		if (this.options.reportToService) {
			this.reportToExternalService(fullReport);
		}

		// Show user notification if enabled
		if (this.options.showUserNotification) {
			this.showUserNotification(fullReport);
		}
	}

	/**
	 * Handle an error with automatic severity detection
	 */
	handleError(error: Error | string, source: string, context?: Record<string, any>): void {
		const message = error instanceof Error ? error.message : error;
		const stack = error instanceof Error ? error.stack : undefined;
		
		this.reportError({
			message,
			severity: this.detectSeverity(message),
			source,
			context,
			stack
		});
	}

	/**
	 * Get recent error reports
	 */
	getRecentErrors(count: number = 10): ErrorReport[] {
		return this.errorReports.slice(-count);
	}

	/**
	 * Clear error reports
	 */
	clearReports(): void {
		this.errorReports = [];
	}

	/**
	 * Get error count by severity
	 */
	getErrorCountBySeverity(): Record<ErrorSeverity, number> {
		const counts = {
			[ErrorSeverity.CRITICAL]: 0,
			[ErrorSeverity.ERROR]: 0,
			[ErrorSeverity.WARNING]: 0,
			[ErrorSeverity.INFO]: 0
		};

		this.errorReports.forEach(report => {
			counts[report.severity]++;
		});

		return counts;
	}

	private addToReports(report: ErrorReport): void {
		this.errorReports.push(report);
		
		// Keep only the most recent reports
		if (this.errorReports.length > this.maxReports) {
			this.errorReports = this.errorReports.slice(-this.maxReports);
		}
	}

	private logToConsole(report: ErrorReport): void {
		const timestamp = report.timestamp?.toISOString() || 'Unknown';
		const prefix = `[${timestamp}] [${report.severity}] [${report.source}]`;
		
		switch (report.severity) {
			case ErrorSeverity.CRITICAL:
			case ErrorSeverity.ERROR:
				console.error(`${prefix} ${report.message}`, report.context || '');
				if (report.stack) {
					console.error('Stack trace:', report.stack);
				}
				break;
			case ErrorSeverity.WARNING:
				console.warn(`${prefix} ${report.message}`, report.context || '');
				break;
			case ErrorSeverity.INFO:
				console.info(`${prefix} ${report.message}`, report.context || '');
				break;
		}
	}

	private reportToExternalService(report: ErrorReport): void {
		// In a real application, this would send to an error reporting service
		// like Sentry, LogRocket, or a custom endpoint
		console.debug('Would report to external service:', report);
	}

	private showUserNotification(report: ErrorReport): void {
		// In a real application, this would show a toast notification or modal
		// For now, we'll just log it
		if (report.severity === ErrorSeverity.CRITICAL || report.severity === ErrorSeverity.ERROR) {
			console.debug('Would show user notification:', report.message);
		}
	}

	private detectSeverity(message: string): ErrorSeverity {
		const lowerMessage = message.toLowerCase();
		
		if (lowerMessage.includes('critical') || lowerMessage.includes('fatal')) {
			return ErrorSeverity.CRITICAL;
		}
		
		if (lowerMessage.includes('error') || lowerMessage.includes('failed') || lowerMessage.includes('exception')) {
			return ErrorSeverity.ERROR;
		}
		
		if (lowerMessage.includes('warning') || lowerMessage.includes('warn')) {
			return ErrorSeverity.WARNING;
		}
		
		return ErrorSeverity.ERROR; // Default to ERROR for unknown cases
	}
}

// Export singleton instance
export const errorService = new ErrorHandlingService();

// Export the class for testing or custom instances
export { ErrorHandlingService };
