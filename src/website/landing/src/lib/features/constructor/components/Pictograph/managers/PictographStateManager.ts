// src/lib/constructor/components/Pictograph/managers/PictographStateManager.ts
import type { PictographStateData } from '../pictographState.js';

export class PictographStateManager {
	constructor(private state: PictographStateData) {}

	updateState(status: PictographStateData['status'], reason?: string) {
		const previousStatus = this.state.status;

		this.state.stateHistory.push({
			from: previousStatus,
			to: status,
			reason,
			timestamp: Date.now()
		});

		this.state.status = status;

		// Update load progress based on status
		this.updateLoadProgress();
	}

	private updateLoadProgress() {
		switch (this.state.status) {
			case 'idle':
				this.state.loadProgress = 0;
				break;
			case 'initializing':
				this.state.loadProgress = 10;
				break;
			case 'grid_loading':
				this.state.loadProgress = 30;
				break;
			case 'props_loading':
				this.state.loadProgress = 60;
				break;
			case 'arrows_loading':
				this.state.loadProgress = 80;
				break;
			case 'complete':
				this.state.loadProgress = 100;
				break;
			case 'error':
				// Keep current progress on error
				break;
		}
	}

	setError(message: string, component?: string) {
		this.state.error = {
			message,
			component,
			timestamp: Date.now()
		};
		this.updateState('error', `Error in ${component || 'unknown component'}: ${message}`);
	}

	clearError() {
		this.state.error = null;
	}

	markComponentLoaded(component: keyof PictographStateData['components']) {
		this.state.components[component] = true;
	}

	areAllComponentsLoaded(): boolean {
		return Object.values(this.state.components).every(loaded => loaded);
	}

	reset() {
		this.state.status = 'idle';
		this.state.error = null;
		this.state.loadProgress = 0;
		this.state.components = {
			grid: false,
			redProp: false,
			blueProp: false,
			redArrow: false,
			blueArrow: false
		};
		this.state.stateHistory = [];
	}
}
