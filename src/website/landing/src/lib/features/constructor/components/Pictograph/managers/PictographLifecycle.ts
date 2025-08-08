// src/lib/constructor/components/Pictograph/managers/PictographLifecycle.ts
import type { PictographData } from '$lib/constructor/types/PictographData.js';
import type { PictographStateData } from '../pictographState.js';
import type { PictographStateManager } from './PictographStateManager.js';
import type { PictographLoadingManager } from './PictographLoadingManager.js';
import type { PictographErrorHandler } from '../handlers/PictographErrorHandler.js';
import type { PictographEventHandler } from '../handlers/PictographEventHandler.js';

export class PictographLifecycle {
	constructor(
		private state: PictographStateData,
		private stateManager: PictographStateManager,
		private loadingManager: PictographLoadingManager,
		private errorHandler: PictographErrorHandler,
		private eventHandler: PictographEventHandler
	) {}

	async initialize(pictographData: PictographData) {
		try {
			this.state.data = pictographData;
			await this.loadingManager.startLoading();
		} catch (error) {
			this.errorHandler.handleError(error);
		}
	}

	async updatePictographData(pictographData: PictographData) {
		if (this.state.data === pictographData) {
			return; // No change
		}

		try {
			this.state.data = pictographData;
			this.stateManager.clearError();
			await this.loadingManager.startLoading();
		} catch (error) {
			this.errorHandler.handleError(error);
		}
	}

	async refresh(pictographData: PictographData) {
		try {
			this.stateManager.reset();
			this.state.data = pictographData;
			await this.loadingManager.startLoading();
		} catch (error) {
			this.errorHandler.handleError(error);
		}
	}

	cleanup() {
		this.stateManager.reset();
		this.state.data = null;
	}
}
