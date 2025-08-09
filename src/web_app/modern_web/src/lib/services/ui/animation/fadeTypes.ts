/**
 * Fade Animation Types for TKA Web App
 * Ported from desktop app fade manager architecture
 */

export interface FadeConfig {
	duration?: number;
	delay?: number;
	easing?: (t: number) => number;
	opacity?: {
		start?: number;
		end?: number;
	};
}

export interface TransitionConfig extends FadeConfig {
	direction?: 'in' | 'out' | 'both';
	fallback?: boolean;
}

export interface CrossfadeConfig extends FadeConfig {
	key: string;
	fallback?: (node: Element, params: any) => any;
}

export type FadeTarget = Element | HTMLElement | null;

export interface FadeOperation {
	id: string;
	targets: FadeTarget[];
	type: 'fade_in' | 'fade_out' | 'crossfade' | 'fade_and_update';
	config: FadeConfig;
	callback?: () => void;
	status: 'pending' | 'running' | 'completed' | 'cancelled';
}

export interface TabTransitionState {
	isTransitioning: boolean;
	currentTab: string;
	targetTab: string | null;
	transitionId: string | null;
}

export interface FadeOrchestratorState {
	isEnabled: boolean;
	activeOperations: Map<string, FadeOperation>;
	tabTransition: TabTransitionState;
	globalDuration: number;
	globalEasing: (t: number) => number;
}

export type FadeEventType =
	| 'fade_start'
	| 'fade_complete'
	| 'fade_error'
	| 'transition_start'
	| 'transition_complete';

export interface FadeEvent {
	type: FadeEventType;
	operationId: string;
	timestamp: number;
	details?: any;
}

// Tab-specific types
export type MainTabId = 'construct' | 'browse' | 'sequence_card' | 'write' | 'learn';
export type ConstructSubTabId = 'build' | 'generate' | 'edit' | 'export';

export interface TabFadeConfig extends FadeConfig {
	tabType: 'main' | 'sub';
	fromTab: string;
	toTab: string;
}
