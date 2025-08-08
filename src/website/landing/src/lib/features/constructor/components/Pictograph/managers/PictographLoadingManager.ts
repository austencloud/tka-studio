// src/lib/constructor/components/Pictograph/managers/PictographLoadingManager.ts
import type { PictographStateData } from '../pictographState.js';
import type { PictographStateManager } from './PictographStateManager.js';

export class PictographLoadingManager {
	constructor(
		private state: PictographStateData,
		private stateManager: PictographStateManager
	) {}

	async startLoading() {
		this.stateManager.updateState('initializing', 'Starting pictograph loading');

		try {
			await this.loadGrid();
			await this.loadProps();
			await this.loadArrows();

			this.stateManager.updateState('complete', 'All components loaded successfully');
		} catch (error) {
			this.stateManager.setError(
				error instanceof Error ? error.message : 'Unknown loading error',
				'LoadingManager'
			);
		}
	}

	private async loadGrid(): Promise<void> {
		this.stateManager.updateState('grid_loading', 'Loading grid component');

		// Simulate grid loading
		await this.delay(100);

		this.stateManager.markComponentLoaded('grid');
	}

	private async loadProps(): Promise<void> {
		this.stateManager.updateState('props_loading', 'Loading prop components');

		// Simulate prop loading
		await this.delay(100);

		this.stateManager.markComponentLoaded('redProp');
		this.stateManager.markComponentLoaded('blueProp');
	}

	private async loadArrows(): Promise<void> {
		this.stateManager.updateState('arrows_loading', 'Loading arrow components');

		// Simulate arrow loading
		await this.delay(100);

		this.stateManager.markComponentLoaded('redArrow');
		this.stateManager.markComponentLoaded('blueArrow');
	}

	private delay(ms: number): Promise<void> {
		return new Promise(resolve => setTimeout(resolve, ms));
	}

	reset() {
		// Reset any loading state
		this.stateManager.reset();
	}
}
