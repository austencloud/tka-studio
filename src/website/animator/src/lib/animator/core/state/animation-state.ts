/**
 * Centralized state management for the animation system
 */

import type { SequenceData, PropState } from '../../types/core.js';

export interface AnimationState {
	// Sequence data
	sequenceData: SequenceData | null;
	totalBeats: number;
	sequenceWord: string;
	sequenceAuthor: string;

	// Animation state
	isPlaying: boolean;
	currentBeat: number;
	speed: number;
	isLooping: boolean;
	canLoop: boolean;

	// Prop states
	blueProp: PropState;
	redProp: PropState;

	// UI state
	errorMessage: string;
	successMessage: string;
	isLoading: boolean;

	// Canvas settings
	canvasWidth: number;
	canvasHeight: number;
	gridVisible: boolean;
}

export interface AnimationStateActions {
	// Sequence actions
	loadSequence: (_data: SequenceData) => void;
	clearSequence: () => void;

	// Animation controls
	play: () => void;
	pause: () => void;
	reset: () => void;
	setSpeed: (_speed: number) => void;
	setBeat: (_beat: number) => void;
	toggleLoop: () => void;

	// Prop state updates
	updatePropStates: (_blue: PropState, _red: PropState) => void;

	// Message actions
	setError: (_message: string) => void;
	setSuccess: (_message: string) => void;
	clearMessages: () => void;

	// UI actions
	setLoading: (_loading: boolean) => void;
	setCanvasSize: (_width: number, _height: number) => void;
	toggleGrid: () => void;
}

/**
 * Create initial animation state
 */
export function createInitialState(): AnimationState {
	return {
		// Sequence data
		sequenceData: null,
		totalBeats: 0,
		sequenceWord: '',
		sequenceAuthor: '',

		// Animation state
		isPlaying: false,
		currentBeat: 0,
		speed: 1.0,
		isLooping: false,
		canLoop: false,

		// Prop states
		blueProp: { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 },
		redProp: { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 },

		// UI state
		errorMessage: '',
		successMessage: '',
		isLoading: false,

		// Canvas settings
		canvasWidth: 500,
		canvasHeight: 500,
		gridVisible: true
	};
}

/**
 * State management class for animation state
 * Note: This class manages state that will be consumed by Svelte components
 */
export class AnimationStateManager {
	private state: AnimationState = createInitialState();

	// Getters for reactive access
	get current(): AnimationState {
		return this.state;
	}

	// Sequence actions
	loadSequence(data: SequenceData): void {
		const metadata = data[0] || {};
		this.state.sequenceData = data;
		this.state.sequenceWord = metadata.word || '';
		this.state.sequenceAuthor = metadata.author || '';
		this.state.totalBeats = data.length - 2; // Subtract metadata and start position
		this.state.canLoop = this.state.totalBeats > 0;
		this.state.currentBeat = 0;
		this.state.isPlaying = false;
		this.clearMessages();
	}

	clearSequence(): void {
		this.state.sequenceData = null;
		this.state.totalBeats = 0;
		this.state.sequenceWord = '';
		this.state.sequenceAuthor = '';
		this.state.canLoop = false;
		this.reset();
	}

	// Animation controls
	play(): void {
		if (this.state.sequenceData) {
			this.state.isPlaying = true;
		}
	}

	pause(): void {
		this.state.isPlaying = false;
	}

	reset(): void {
		this.state.isPlaying = false;
		this.state.currentBeat = 0;
		this.state.blueProp = { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 };
		this.state.redProp = { centerPathAngle: 0, staffRotationAngle: 0, x: 0, y: 0 };
	}

	setSpeed(speed: number): void {
		this.state.speed = Math.max(0.1, Math.min(3.0, speed));
	}

	setBeat(beat: number): void {
		this.state.currentBeat = Math.max(0, Math.min(this.state.totalBeats, beat));
	}

	toggleLoop(): void {
		if (this.state.canLoop) {
			this.state.isLooping = !this.state.isLooping;
		}
	}

	// Prop state updates
	updatePropStates(blue: PropState, red: PropState): void {
		this.state.blueProp = { ...blue };
		this.state.redProp = { ...red };
	}

	// Message actions
	setError(message: string): void {
		this.state.errorMessage = message;
		this.state.successMessage = '';
	}

	setSuccess(message: string): void {
		this.state.successMessage = message;
		this.state.errorMessage = '';
	}

	clearMessages(): void {
		this.state.errorMessage = '';
		this.state.successMessage = '';
	}

	// UI actions
	setLoading(loading: boolean): void {
		this.state.isLoading = loading;
	}

	setCanvasSize(width: number, height: number): void {
		this.state.canvasWidth = width;
		this.state.canvasHeight = height;
	}

	toggleGrid(): void {
		this.state.gridVisible = !this.state.gridVisible;
	}

	// Computed properties
	get metadata() {
		return {
			word: this.state.sequenceWord,
			author: this.state.sequenceAuthor,
			totalBeats: this.state.totalBeats
		};
	}

	get animationStatus() {
		return {
			isPlaying: this.state.isPlaying,
			currentBeat: this.state.currentBeat,
			speed: this.state.speed,
			isLooping: this.state.isLooping,
			canLoop: this.state.canLoop
		};
	}

	get propStates() {
		return {
			blue: this.state.blueProp,
			red: this.state.redProp
		};
	}

	get messages() {
		return {
			error: this.state.errorMessage,
			success: this.state.successMessage
		};
	}

	get canvasSettings() {
		return {
			width: this.state.canvasWidth,
			height: this.state.canvasHeight,
			gridVisible: this.state.gridVisible
		};
	}
}
