/**
 * Sequence Generation Service - Generate complete sequences
 * 
 * Orchestrates the generation of complete sequences by coordinating
 * motion generation and applying sequence-level constraints.
 */

import type { SequenceData, BeatData } from '@tka/schemas';
import type {
	ISequenceGenerationService,
	IMotionGenerationService,
	ISequenceDomainService,
	GenerationOptions
} from '../interfaces';

export class SequenceGenerationService implements ISequenceGenerationService {
	constructor(
		private motionGenerationService: IMotionGenerationService,
		private sequenceDomainService: ISequenceDomainService
	) {}

	/**
	 * Generate a complete sequence
	 */
	async generateSequence(options: GenerationOptions): Promise<SequenceData> {
		try {
			console.log('Generating sequence with options:', options);

			// Validate options
			this.validateGenerationOptions(options);

			// Generate beats
			const beats: BeatData[] = [];
			
			for (let i = 1; i <= options.length; i++) {
				const beat = await this.generateBeat(i, options, beats);
				beats.push(beat);
			}

			// Create sequence using domain service
			const sequence = this.sequenceDomainService.createSequence({
				name: this.generateSequenceName(options),
				length: options.length,
				gridMode: options.gridMode,
				propType: options.propType
			});

			// Replace the empty beats with generated beats
			const generatedSequence: SequenceData = {
				...sequence,
				beats,
				createdAt: new Date().toISOString(),
				updatedAt: new Date().toISOString()
			};

			console.log('Sequence generation complete:', generatedSequence.id);
			return generatedSequence;
		} catch (error) {
			console.error('Failed to generate sequence:', error);
			throw new Error(`Sequence generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	/**
	 * Generate a single beat
	 */
	private async generateBeat(
		beatNumber: number,
		options: GenerationOptions,
		previousBeats: BeatData[]
	): Promise<BeatData> {
		try {
			console.log(`Generating beat ${beatNumber}/${options.length}`);

			// Generate motions for both colors
			const blueMotion = await this.motionGenerationService.generateMotion(
				'blue',
				options,
				previousBeats
			);

			const redMotion = await this.motionGenerationService.generateMotion(
				'red',
				options,
				previousBeats
			);

			// Create beat
			const beat: BeatData = {
				beatNumber,
				letter: null, // Will be calculated later
				duration: 1.0,
				blueMotion,
				redMotion,
				blueReversal: false,
				redReversal: false,
				filled: true,
				tags: [],
				metadata: {
					generated: true,
					generatedAt: new Date().toISOString(),
					difficulty: options.difficulty
				}
			};

			return beat;
		} catch (error) {
			console.error(`Failed to generate beat ${beatNumber}:`, error);
			throw new Error(`Beat generation failed: ${error instanceof Error ? error.message : 'Unknown error'}`);
		}
	}

	/**
	 * Validate generation options
	 */
	private validateGenerationOptions(options: GenerationOptions): void {
		if (!options.length || options.length < 1 || options.length > 64) {
			throw new Error('Sequence length must be between 1 and 64');
		}

		if (!['diamond', 'box'].includes(options.gridMode)) {
			throw new Error('Grid mode must be either "diamond" or "box"');
		}

		if (!['beginner', 'intermediate', 'advanced'].includes(options.difficulty)) {
			throw new Error('Difficulty must be "beginner", "intermediate", or "advanced"');
		}
	}

	/**
	 * Generate a sequence name based on options
	 */
	private generateSequenceName(options: GenerationOptions): string {
		const timestamp = new Date().toLocaleString('en-US', {
			month: 'short',
			day: 'numeric',
			hour: 'numeric',
			minute: '2-digit'
		});

		const difficulty = options.difficulty.charAt(0).toUpperCase() + options.difficulty.slice(1);
		
		return `${difficulty} ${options.length}-Beat (${timestamp})`;
	}

	/**
	 * Generate sequence with specific patterns
	 */
	async generatePatternSequence(
		pattern: 'circular' | 'linear' | 'random',
		options: GenerationOptions
	): Promise<SequenceData> {
		// TODO: Implement pattern-specific generation
		console.log(`Generating ${pattern} pattern sequence`);
		
		// For now, use basic generation
		return this.generateSequence(options);
	}

	/**
	 * Generate sequence variations
	 */
	async generateVariations(
		baseSequence: SequenceData,
		variationType: 'timing' | 'direction' | 'complexity',
		count: number = 3
	): Promise<SequenceData[]> {
		// TODO: Implement sequence variations
		console.log(`Generating ${count} ${variationType} variations`);
		
		const variations: SequenceData[] = [];
		
		for (let i = 0; i < count; i++) {
			// For now, generate new sequences
			// Eventually this will modify the base sequence
			const options: GenerationOptions = {
				length: baseSequence.length || 8,
				gridMode: 'diamond',
				propType: 'fan',
				difficulty: 'intermediate'
			};
			
			const variation = await this.generateSequence(options);
			variation.name = `${baseSequence.name} - Variation ${i + 1}`;
			variations.push(variation);
		}
		
		return variations;
	}

	/**
	 * Get generation statistics
	 */
	getGenerationStats(): {
		totalGenerated: number;
		averageGenerationTime: number;
		lastGenerated: string | null;
	} {
		// TODO: Implement statistics tracking
		return {
			totalGenerated: 0,
			averageGenerationTime: 0,
			lastGenerated: null
		};
	}
}
