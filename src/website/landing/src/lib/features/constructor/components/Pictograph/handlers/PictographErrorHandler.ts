// src/lib/constructor/components/Pictograph/handlers/PictographErrorHandler.ts
import type { PictographStateData } from '../pictographState.js';
import type { PictographStateManager } from '../managers/PictographStateManager.js';

export class PictographErrorHandler {
	constructor(
		private state: PictographStateData,
		private stateManager: PictographStateManager
	) {}

	handleError(error: any, component?: string) {
		console.error('Pictograph error:', error);

		const errorMessage = this.extractErrorMessage(error);
		this.stateManager.setError(errorMessage, component);
	}

	private extractErrorMessage(error: any): string {
		if (typeof error === 'string') {
			return error;
		}

		if (error instanceof Error) {
			return error.message;
		}

		if (error && typeof error === 'object') {
			if (error.message) {
				return error.message;
			}
			if (error.detail) {
				return error.detail;
			}
		}

		return 'An unknown error occurred';
	}

	clearError() {
		this.stateManager.clearError();
	}

	hasError(): boolean {
		return this.state.error !== null;
	}

	getErrorMessage(): string | null {
		return this.state.error?.message || null;
	}
}
