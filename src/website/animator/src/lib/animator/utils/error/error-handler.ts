/**
 * Standardized error handling utilities for the animator
 */

export interface AnimatorError {
	code: string;
	message: string;
	details?: string;
	timestamp: Date;
}

export class AnimatorErrorHandler {
	/**
	 * Create a standardized error object
	 */
	static createError(
		code: string,
		message: string,
		details?: string,
		originalError?: Error
	): AnimatorError {
		return {
			code,
			message,
			details: details || (originalError ? originalError.message : undefined),
			timestamp: new Date()
		};
	}

	/**
	 * Format error for user display
	 */
	static formatForUser(error: AnimatorError): string {
		return `${error.message}${error.details ? ` (${error.details})` : ''}`;
	}

	/**
	 * Format error for logging/debugging
	 */
	static formatForLogging(error: AnimatorError): string {
		return `[${error.code}] ${error.message} - ${error.details || 'No details'} (${error.timestamp.toISOString()})`;
	}

	/**
	 * Handle file loading errors
	 */
	static handleFileError(originalError: Error): AnimatorError {
		if (originalError.message.includes('metadata')) {
			return this.createError(
				'FILE_NO_METADATA',
				'File does not contain sequence metadata',
				'Please ensure the file was exported from the animator with embedded sequence data',
				originalError
			);
		}

		if (originalError.message.includes('format')) {
			return this.createError(
				'FILE_INVALID_FORMAT',
				'Invalid file format',
				'Please upload a PNG file with embedded sequence data',
				originalError
			);
		}

		return this.createError('FILE_LOAD_ERROR', 'Failed to load file', undefined, originalError);
	}

	/**
	 * Handle sequence validation errors
	 */
	static handleSequenceError(originalError: Error): AnimatorError {
		if (originalError.message.includes('steps')) {
			return this.createError(
				'SEQUENCE_NO_STEPS',
				'Sequence contains no animation steps',
				'Please ensure the sequence has at least one animation step',
				originalError
			);
		}

		if (originalError.message.includes('metadata')) {
			return this.createError(
				'SEQUENCE_INVALID_METADATA',
				'Invalid sequence metadata',
				'Please check the sequence format and try again',
				originalError
			);
		}

		return this.createError(
			'SEQUENCE_VALIDATION_ERROR',
			'Sequence validation failed',
			undefined,
			originalError
		);
	}

	/**
	 * Handle animation engine errors
	 */
	static handleEngineError(originalError: Error): AnimatorError {
		if (originalError.message.includes('initialize')) {
			return this.createError(
				'ENGINE_INIT_ERROR',
				'Failed to initialize animation engine',
				'Please check the sequence data and try again',
				originalError
			);
		}

		return this.createError('ENGINE_ERROR', 'Animation engine error', undefined, originalError);
	}

	/**
	 * Handle canvas/rendering errors
	 */
	static handleRenderError(originalError: Error): AnimatorError {
		return this.createError(
			'RENDER_ERROR',
			'Failed to render animation',
			'Please try refreshing the page or check your browser compatibility',
			originalError
		);
	}
}

/**
 * Error codes for common animator errors
 */
export const ERROR_CODES = {
	FILE_NO_METADATA: 'FILE_NO_METADATA',
	FILE_INVALID_FORMAT: 'FILE_INVALID_FORMAT',
	FILE_LOAD_ERROR: 'FILE_LOAD_ERROR',
	SEQUENCE_NO_STEPS: 'SEQUENCE_NO_STEPS',
	SEQUENCE_INVALID_METADATA: 'SEQUENCE_INVALID_METADATA',
	SEQUENCE_VALIDATION_ERROR: 'SEQUENCE_VALIDATION_ERROR',
	ENGINE_INIT_ERROR: 'ENGINE_INIT_ERROR',
	ENGINE_ERROR: 'ENGINE_ERROR',
	RENDER_ERROR: 'RENDER_ERROR'
} as const;

export type ErrorCode = (typeof ERROR_CODES)[keyof typeof ERROR_CODES];
