// src/lib/constructor/components/Pictograph/handlers/PictographEventHandler.ts
import type { PictographStateData } from '../pictographState.js';
import type { PictographStateManager } from '../managers/PictographStateManager.js';

export class PictographEventHandler {
	constructor(
		private state: PictographStateData,
		private stateManager: PictographStateManager
	) {}

	handleClick(event?: MouseEvent) {
		// Handle pictograph click events
		console.log('Pictograph clicked', this.state.data);
	}

	handleKeydown(event: KeyboardEvent) {
		if (event.key === 'Enter' || event.key === ' ') {
			event.preventDefault();
			this.handleClick();
		}
	}

	handleStateChange(status: PictographStateData['status'], reason?: string) {
		this.stateManager.updateState(status, reason);
	}
}
