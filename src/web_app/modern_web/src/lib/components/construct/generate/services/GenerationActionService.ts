/**
 * GenerationActionService - Handles sequence generation and auto-completion actions
 * 
 * Extracted from GeneratePanel.svelte to provide reusable generation logic.
 * Manages generation state, progress tracking, and result handling.
 */

import type { GenerationConfiguration } from './GenerationConfigurationService';

// ===== Types =====
export interface GenerationResult {
	success: boolean;
	sequence?: any[]; // Replace with actual sequence type
	error?: string;
	metadata?: {
		generationTime: number;
		configurationUsed: GenerationConfiguration;
		generationId: string;
	};
}

export interface GenerationProgress {
	stage: 'preparing' | 'generating' | 'validating' | 'complete' | 'error';
	progress: number; // 0-100
	message: string;
	estimatedTimeRemaining?: number;
}

export interface GenerationOptions {
	showProgress?: boolean;
	timeout?: number;
	abortOnError?: boolean;
	validateResult?: boolean;
}

export type GenerationEventType = 'started' | 'progress' | 'completed' | 'error' | 'cancelled';

export interface GenerationEvent {
	type: GenerationEventType;
	timestamp: number;
	data?: GenerationResult | GenerationProgress | Error;
}

// ===== Main Service Class =====
export class GenerationActionService {
	private isGenerating = false;
	private currentGenerationId: string | null = null;
	private currentAbortController: AbortController | null = null;
	private eventListeners: Array<(event: GenerationEvent) => void> = [];
	private progressListeners: Array<(progress: GenerationProgress) => void> = [];

	/**
	 * Generates a new sequence based on configuration
	 */
	async generateSequence(
		config: GenerationConfiguration,
		options: GenerationOptions = {}
	): Promise<GenerationResult> {
		if (this.isGenerating) {
			throw new Error('Generation already in progress');
		}

		const generationId = this.createGenerationId();
		const startTime = Date.now();

		try {
			this.startGeneration(generationId, config, options);

			// Simulate generation process
			const result = await this.performGeneration(config, options);

			const metadata = {
				generationTime: Date.now() - startTime,
				configurationUsed: { ...config },
				generationId,
			};

			const finalResult: GenerationResult = {
				...result,
				metadata,
			};

			this.completeGeneration(finalResult);
			return finalResult;

		} catch (error) {
			const errorResult: GenerationResult = {
				success: false,
				error: error instanceof Error ? error.message : 'Unknown generation error',
				metadata: {
					generationTime: Date.now() - startTime,
					configurationUsed: { ...config },
					generationId,
				},
			};

			this.errorGeneration(error as Error, errorResult);
			return errorResult;

		} finally {
			this.cleanupGeneration();
		}
	}

	/**
	 * Auto-completes the current sequence
	 */
	async autoCompleteSequence(
		currentSequence: any[], // Replace with actual sequence type
		config: Partial<GenerationConfiguration>,
		options: GenerationOptions = {}
	): Promise<GenerationResult> {
		if (this.isGenerating) {
			throw new Error('Generation already in progress');
		}

		const generationId = this.createGenerationId();
		const startTime = Date.now();

		try {
			this.startGeneration(generationId, config as GenerationConfiguration, options, 'auto-complete');

			// Simulate auto-completion process
			const result = await this.performAutoCompletion(currentSequence, config, options);

			const metadata = {
				generationTime: Date.now() - startTime,
				configurationUsed: { ...config } as GenerationConfiguration,
				generationId,
			};

			const finalResult: GenerationResult = {
				...result,
				metadata,
			};

			this.completeGeneration(finalResult);
			return finalResult;

		} catch (error) {
			const errorResult: GenerationResult = {
				success: false,
				error: error instanceof Error ? error.message : 'Unknown auto-completion error',
				metadata: {
					generationTime: Date.now() - startTime,
					configurationUsed: { ...config } as GenerationConfiguration,
					generationId,
				},
			};

			this.errorGeneration(error as Error, errorResult);
			return errorResult;

		} finally {
			this.cleanupGeneration();
		}
	}

	/**
	 * Cancels the current generation
	 */
	cancelGeneration(): boolean {
		if (!this.isGenerating || !this.currentAbortController) {
			return false;
		}

		this.currentAbortController.abort();
		this.emitEvent({
			type: 'cancelled',
			timestamp: Date.now(),
		});

		this.cleanupGeneration();
		return true;
	}

	/**
	 * Gets current generation state
	 */
	getGenerationState(): {
		isGenerating: boolean;
		currentGenerationId: string | null;
		canCancel: boolean;
	} {
		return {
			isGenerating: this.isGenerating,
			currentGenerationId: this.currentGenerationId,
			canCancel: this.isGenerating && this.currentAbortController !== null,
		};
	}

	/**
	 * Adds event listener for generation events
	 */
	addEventListener(listener: (event: GenerationEvent) => void): () => void {
		this.eventListeners.push(listener);
		
		return () => {
			const index = this.eventListeners.indexOf(listener);
			if (index > -1) {
				this.eventListeners.splice(index, 1);
			}
		};
	}

	/**
	 * Adds progress listener for generation progress updates
	 */
	addProgressListener(listener: (progress: GenerationProgress) => void): () => void {
		this.progressListeners.push(listener);
		
		return () => {
			const index = this.progressListeners.indexOf(listener);
			if (index > -1) {
				this.progressListeners.splice(index, 1);
			}
		};
	}

	/**
	 * Validates if generation can be started with given configuration
	 */
	canStartGeneration(config: GenerationConfiguration): { canStart: boolean; reason?: string } {
		if (this.isGenerating) {
			return { canStart: false, reason: 'Generation already in progress' };
		}

		// Add configuration validation
		if (!config) {
			return { canStart: false, reason: 'Configuration is required' };
		}

		if (config.length <= 0) {
			return { canStart: false, reason: 'Sequence length must be positive' };
		}

		if (config.letterTypes.size === 0) {
			return { canStart: false, reason: 'At least one letter type must be selected' };
		}

		return { canStart: true };
	}

	// ===== Private Methods =====

	private createGenerationId(): string {
		return `gen_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
	}

	private startGeneration(
		generationId: string,
		config: GenerationConfiguration,
		options: GenerationOptions,
		type: 'generate' | 'auto-complete' = 'generate'
	): void {
		this.isGenerating = true;
		this.currentGenerationId = generationId;
		this.currentAbortController = new AbortController();

		this.emitEvent({
			type: 'started',
			timestamp: Date.now(),
			data: { type, config, options } as any,
		});

		if (options.showProgress) {
			this.emitProgress({
				stage: 'preparing',
				progress: 0,
				message: `Starting ${type}...`,
			});
		}
	}

	private async performGeneration(
		config: GenerationConfiguration,
		options: GenerationOptions
	): Promise<GenerationResult> {
		const steps = [
			{ stage: 'preparing' as const, message: 'Preparing generation...', duration: 200 },
			{ stage: 'generating' as const, message: 'Generating sequence...', duration: 1500 },
			{ stage: 'validating' as const, message: 'Validating result...', duration: 300 },
		];

		let totalProgress = 0;
		const progressPerStep = 100 / steps.length;

		for (let i = 0; i < steps.length; i++) {
			const step = steps[i];
			
			if (options.showProgress) {
				this.emitProgress({
					stage: step.stage,
					progress: totalProgress,
					message: step.message,
					estimatedTimeRemaining: this.calculateRemainingTime(i, steps.length, step.duration),
				});
			}

			// Simulate step execution
			await this.simulateAsync(step.duration, options.timeout);

			// Check for abort
			if (this.currentAbortController?.signal.aborted) {
				throw new Error('Generation cancelled');
			}

			totalProgress += progressPerStep;
		}

		// Complete progress
		if (options.showProgress) {
			this.emitProgress({
				stage: 'complete',
				progress: 100,
				message: 'Generation complete!',
			});
		}

		// Simulate successful result
		return {
			success: true,
			sequence: this.createMockSequence(config),
		};
	}

	private async performAutoCompletion(
		currentSequence: any[],
		config: Partial<GenerationConfiguration>,
		options: GenerationOptions
	): Promise<GenerationResult> {
		const steps = [
			{ stage: 'preparing' as const, message: 'Analyzing current sequence...', duration: 300 },
			{ stage: 'generating' as const, message: 'Generating completion...', duration: 1000 },
			{ stage: 'validating' as const, message: 'Validating completion...', duration: 200 },
		];

		let totalProgress = 0;
		const progressPerStep = 100 / steps.length;

		for (let i = 0; i < steps.length; i++) {
			const step = steps[i];
			
			if (options.showProgress) {
				this.emitProgress({
					stage: step.stage,
					progress: totalProgress,
					message: step.message,
					estimatedTimeRemaining: this.calculateRemainingTime(i, steps.length, step.duration),
				});
			}

			// Simulate step execution
			await this.simulateAsync(step.duration, options.timeout);

			// Check for abort
			if (this.currentAbortController?.signal.aborted) {
				throw new Error('Auto-completion cancelled');
			}

			totalProgress += progressPerStep;
		}

		// Complete progress
		if (options.showProgress) {
			this.emitProgress({
				stage: 'complete',
				progress: 100,
				message: 'Auto-completion complete!',
			});
		}

		// Simulate successful result
		return {
			success: true,
			sequence: [...currentSequence, ...this.createMockCompletion(currentSequence, config)],
		};
	}

	private async simulateAsync(duration: number, timeout?: number): Promise<void> {
		const effectiveDuration = Math.min(duration, timeout || Infinity);
		
		return new Promise((resolve, reject) => {
			const timer = setTimeout(resolve, effectiveDuration);
			
			if (this.currentAbortController) {
				this.currentAbortController.signal.addEventListener('abort', () => {
					clearTimeout(timer);
					reject(new Error('Operation aborted'));
				});
			}
		});
	}

	private calculateRemainingTime(currentStep: number, totalSteps: number, currentStepDuration: number): number {
		const remainingSteps = totalSteps - currentStep - 1;
		const averageStepDuration = 500; // Rough estimate
		return currentStepDuration + (remainingSteps * averageStepDuration);
	}

	private createMockSequence(config: GenerationConfiguration): any[] {
		// This is a placeholder - replace with actual sequence generation logic
		return Array.from({ length: config.length }, (_, i) => ({
			id: `beat_${i}`,
			index: i,
			type: Array.from(config.letterTypes)[i % config.letterTypes.size],
			data: `mock_data_${i}`,
		}));
	}

	private createMockCompletion(currentSequence: any[], config: Partial<GenerationConfiguration>): any[] {
		// This is a placeholder - replace with actual completion logic
		const completionLength = Math.max(1, (config.length || 16) - currentSequence.length);
		return Array.from({ length: completionLength }, (_, i) => ({
			id: `completion_${i}`,
			index: currentSequence.length + i,
			type: 'TYPE1', // Simplified
			data: `completion_data_${i}`,
		}));
	}

	private completeGeneration(result: GenerationResult): void {
		this.emitEvent({
			type: 'completed',
			timestamp: Date.now(),
			data: result,
		});
	}

	private errorGeneration(error: Error, result: GenerationResult): void {
		this.emitEvent({
			type: 'error',
			timestamp: Date.now(),
			data: result,
		});

		console.error('Generation error:', error);
	}

	private cleanupGeneration(): void {
		this.isGenerating = false;
		this.currentGenerationId = null;
		this.currentAbortController = null;
	}

	private emitEvent(event: GenerationEvent): void {
		this.eventListeners.forEach(listener => {
			try {
				listener(event);
			} catch (error) {
				console.error('Error in generation event listener:', error);
			}
		});
	}

	private emitProgress(progress: GenerationProgress): void {
		this.progressListeners.forEach(listener => {
			try {
				listener(progress);
			} catch (error) {
				console.error('Error in generation progress listener:', error);
			}
		});
	}
}

// ===== Factory Functions =====

/**
 * Creates a new GenerationActionService instance
 */
export function createGenerationActionService(): GenerationActionService {
	return new GenerationActionService();
}

/**
 * Creates a generation action service with preset options for different use cases
 */
export function createGenerationActionServiceWithPresets(
	preset: 'development' | 'production' | 'testing'
): GenerationActionService {
	const service = createGenerationActionService();

	if (preset === 'development') {
		// Add development-specific listeners
		service.addEventListener((event) => {
			console.log('🎯 Generation Event:', event);
		});
		
		service.addProgressListener((progress) => {
			console.log('📊 Generation Progress:', progress);
		});
	}

	return service;
}

// ===== Utility Functions =====

/**
 * Estimates generation time based on configuration
 */
export function estimateGenerationTime(config: GenerationConfiguration): number {
	// Base time + length factor + complexity factor
	const baseTime = 500; // ms
	const lengthFactor = config.length * 50; // ms per beat
	const complexityFactor = config.level * 200; // ms per level
	const modeFactor = config.mode === 'CIRCULAR' ? 300 : 0; // Additional time for circular mode
	
	return baseTime + lengthFactor + complexityFactor + modeFactor;
}

/**
 * Checks if generation can be performed with current system resources
 */
export function checkGenerationCapabilities(): {
	canGenerate: boolean;
	maxLength: number;
	warnings: string[];
} {
	const warnings: string[] = [];
	let maxLength = 64;

	// Check memory (rough estimate)
	if (typeof performance !== 'undefined' && 'memory' in performance) {
		const memory = (performance as any).memory;
		if (memory.usedJSHeapSize > memory.jsHeapSizeLimit * 0.8) {
			warnings.push('High memory usage detected');
			maxLength = 32;
		}
	}

	// Check if we're in a web worker or main thread
	const isMainThread = typeof window !== 'undefined';
	if (!isMainThread) {
		maxLength = 128; // Web workers can handle larger sequences
	}

	return {
		canGenerate: true,
		maxLength,
		warnings,
	};
}
