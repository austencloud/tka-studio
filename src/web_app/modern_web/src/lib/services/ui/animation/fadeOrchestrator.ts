/**
 * Fade Orchestrator Service - Web App Implementation
 * Ported from desktop app fade manager architecture
 */

import { cubicOut } from 'svelte/easing';
import type {
	FadeConfig,
	FadeOperation,
	FadeOrchestratorState,
	FadeEvent,
	FadeEventType,
	TabTransitionState,
	MainTabId,
	ConstructSubTabId,
	TabFadeConfig,
} from './fadeTypes';

/**
 * Main fade orchestrator class that manages all fade operations
 * Mimics the desktop app's FadeManager behavior
 */
export class FadeOrchestrator {
	private state: FadeOrchestratorState;
	private eventListeners: Map<FadeEventType, ((event: FadeEvent) => void)[]>;
	private operationCounter: number = 0;

	constructor(initialConfig: Partial<FadeConfig> = {}) {
		this.state = {
			isEnabled: true,
			activeOperations: new Map(),
			tabTransition: {
				isTransitioning: false,
				currentTab: '',
				targetTab: null,
				transitionId: null,
			},
			globalDuration: initialConfig.duration || 300,
			globalEasing: initialConfig.easing || cubicOut,
		};

		this.eventListeners = new Map();
	}

	/**
	 * Check if fades are enabled (like desktop app)
	 */
	public fadesEnabled(): boolean {
		return this.state.isEnabled;
	}

	/**
	 * Enable or disable fade animations globally
	 */
	public setFadesEnabled(enabled: boolean): void {
		this.state.isEnabled = enabled;

		if (!enabled) {
			// Cancel all active operations when disabling
			this.cancelAllOperations();
		}
	}

	/**
	 * Get current transition state
	 */
	public getTabTransitionState(): TabTransitionState {
		return { ...this.state.tabTransition };
	}

	/**
	 * Check if currently transitioning between tabs
	 */
	public isTransitioning(): boolean {
		return this.state.tabTransition.isTransitioning;
	}

	/**
	 * Start a main tab transition (Construct, Browse, etc.)
	 */
	public async startMainTabTransition(
		fromTab: MainTabId,
		toTab: MainTabId,
		config: Partial<TabFadeConfig> = {}
	): Promise<string> {
		if (this.state.tabTransition.isTransitioning) {
			console.warn(
				`FadeOrchestrator: Already transitioning from ${this.state.tabTransition.currentTab} to ${this.state.tabTransition.targetTab}`
			);
			return this.state.tabTransition.transitionId!;
		}

		const transitionId = this.generateOperationId('main_tab_transition');

		this.state.tabTransition = {
			isTransitioning: true,
			currentTab: fromTab,
			targetTab: toTab,
			transitionId,
		};

		const mergedConfig: TabFadeConfig = {
			tabType: 'main',
			fromTab,
			toTab,
			duration: config.duration || this.state.globalDuration,
			easing: config.easing || this.state.globalEasing,
			...config,
		};

		this.emitEvent('transition_start', transitionId, {
			type: 'main_tab',
			fromTab,
			toTab,
			config: mergedConfig,
		});

		return transitionId;
	}

	/**
	 * Complete a main tab transition
	 */
	public completeMainTabTransition(transitionId: string): void {
		if (this.state.tabTransition.transitionId !== transitionId) {
			console.warn(
				`FadeOrchestrator: Transition ID mismatch. Expected ${this.state.tabTransition.transitionId}, got ${transitionId}`
			);
			return;
		}

		const fromTab = this.state.tabTransition.currentTab;
		const toTab = this.state.tabTransition.targetTab;

		this.state.tabTransition = {
			isTransitioning: false,
			currentTab: toTab || fromTab,
			targetTab: null,
			transitionId: null,
		};

		this.emitEvent('transition_complete', transitionId, {
			type: 'main_tab',
			fromTab,
			toTab,
		});
	}

	/**
	 * Start a sub-tab transition (Build, Generate, etc.)
	 */
	public async startSubTabTransition(
		fromTab: ConstructSubTabId,
		toTab: ConstructSubTabId,
		config: Partial<TabFadeConfig> = {}
	): Promise<string> {
		const transitionId = this.generateOperationId('sub_tab_transition');

		const mergedConfig: TabFadeConfig = {
			tabType: 'sub',
			fromTab,
			toTab,
			duration: config.duration || this.state.globalDuration,
			easing: config.easing || this.state.globalEasing,
			...config,
		};

		this.emitEvent('transition_start', transitionId, {
			type: 'sub_tab',
			fromTab,
			toTab,
			config: mergedConfig,
		});

		return transitionId;
	}

	/**
	 * Complete a sub-tab transition
	 */
	public completeSubTabTransition(transitionId: string, fromTab: string, toTab: string): void {
		this.emitEvent('transition_complete', transitionId, {
			type: 'sub_tab',
			fromTab,
			toTab,
		});
	}

	/**
	 * Create a fade operation (like desktop app's fade_and_update)
	 */
	public async fadeAndUpdate(
		updateCallback: () => void | Promise<void>,
		config: Partial<FadeConfig> = {}
	): Promise<string> {
		if (!this.state.isEnabled) {
			// If fades disabled, just execute the callback immediately
			await updateCallback();
			return 'disabled';
		}

		const operationId = this.generateOperationId('fade_and_update');

		const operation: FadeOperation = {
			id: operationId,
			targets: [], // Will be set by the calling component
			type: 'fade_and_update',
			config: {
				duration: config.duration || this.state.globalDuration,
				easing: config.easing || this.state.globalEasing,
				...config,
			},
			callback: typeof updateCallback === 'function' ? updateCallback : undefined,
			status: 'pending',
		};

		this.state.activeOperations.set(operationId, operation);
		this.emitEvent('fade_start', operationId, { operation });

		// Execute the update callback
		try {
			operation.status = 'running';
			await updateCallback();
			operation.status = 'completed';
			this.emitEvent('fade_complete', operationId, { operation });
		} catch (error) {
			operation.status = 'cancelled';
			this.emitEvent('fade_error', operationId, { operation, error });
		} finally {
			this.state.activeOperations.delete(operationId);
		}

		return operationId;
	}

	/**
	 * Cancel all active operations
	 */
	public cancelAllOperations(): void {
		for (const [id, operation] of this.state.activeOperations) {
			operation.status = 'cancelled';
			this.emitEvent('fade_error', id, { operation, reason: 'cancelled_by_user' });
		}
		this.state.activeOperations.clear();
	}

	/**
	 * Get the current fade configuration for a specific operation type
	 */
	public getFadeConfig(type: 'main_tab' | 'sub_tab' | 'general' = 'general'): FadeConfig {
		// Different configs for different transition types
		const configs = {
			main_tab: {
				duration: 350,
				easing: this.state.globalEasing,
				delay: 0,
			},
			sub_tab: {
				duration: 250,
				easing: this.state.globalEasing,
				delay: 0,
			},
			general: {
				duration: this.state.globalDuration,
				easing: this.state.globalEasing,
				delay: 0,
			},
		};

		return configs[type];
	}

	/**
	 * Register an event listener
	 */
	public addEventListener(type: FadeEventType, listener: (event: FadeEvent) => void): void {
		if (!this.eventListeners.has(type)) {
			this.eventListeners.set(type, []);
		}
		this.eventListeners.get(type)!.push(listener);
	}

	/**
	 * Remove an event listener
	 */
	public removeEventListener(type: FadeEventType, listener: (event: FadeEvent) => void): void {
		const listeners = this.eventListeners.get(type);
		if (listeners) {
			const index = listeners.indexOf(listener);
			if (index > -1) {
				listeners.splice(index, 1);
			}
		}
	}

	/**
	 * Emit an event to all listeners
	 */
	private emitEvent(type: FadeEventType, operationId: string, details?: any): void {
		const event: FadeEvent = {
			type,
			operationId,
			timestamp: Date.now(),
			details,
		};

		const listeners = this.eventListeners.get(type);
		if (listeners) {
			listeners.forEach((listener) => {
				try {
					listener(event);
				} catch (error) {
					console.error(`FadeOrchestrator: Error in event listener for ${type}:`, error);
				}
			});
		}
	}

	/**
	 * Generate a unique operation ID
	 */
	private generateOperationId(type: string): string {
		return `${type}_${this.operationCounter++}_${Date.now()}`;
	}

	/**
	 * Get debug information about the current state
	 */
	public getDebugInfo() {
		return {
			isEnabled: this.state.isEnabled,
			activeOperationsCount: this.state.activeOperations.size,
			tabTransition: this.state.tabTransition,
			globalConfig: {
				duration: this.state.globalDuration,
				easing: this.state.globalEasing.name || 'custom',
			},
		};
	}
}

// Singleton instance for global use
let globalFadeOrchestrator: FadeOrchestrator | null = null;

/**
 * Get the global fade orchestrator instance
 */
export function getFadeOrchestrator(): FadeOrchestrator {
	if (!globalFadeOrchestrator) {
		globalFadeOrchestrator = new FadeOrchestrator();
	}
	return globalFadeOrchestrator;
}

/**
 * Initialize fade orchestrator with custom config
 */
export function initializeFadeOrchestrator(config: Partial<FadeConfig> = {}): FadeOrchestrator {
	globalFadeOrchestrator = new FadeOrchestrator(config);
	return globalFadeOrchestrator;
}

/**
 * Reset the global fade orchestrator
 */
export function resetFadeOrchestrator(): void {
	if (globalFadeOrchestrator) {
		globalFadeOrchestrator.cancelAllOperations();
	}
	globalFadeOrchestrator = null;
}
