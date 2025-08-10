/**
 * Beat Frame Service (Runes-based)
 *
 * Manages beat frame layout and interactions for the Workbench.
 * Now supports a dedicated Start Position tile at [0,0] and responsive columns.
 */

import type { BeatData } from '../domain';
import { GridMode } from '../domain';

interface BeatFrameConfig {
	/** Number of columns allocated for BEATS (excludes the Start tile column) */
	columns: number;
	beatSize: number;
	gap: number;
	gridMode: GridMode;
	/** Whether to reserve the first column for the Start Position tile */
	hasStartTile: boolean;
}

class BeatFrameService {
	// Configuration state
	#config = $state<BeatFrameConfig>({
		columns: 4, // columns for beats only
		beatSize: 120,
		gap: 0, // Desktop parity: zero spacing between cells
		gridMode: GridMode.DIAMOND,
		hasStartTile: true,
	});

	// Interaction state
	#hoveredBeatIndex = $state<number>(-1);
	#draggedBeatIndex = $state<number>(-1);

	// Derived state
	readonly config = $derived(this.#config);
	readonly hoveredBeatIndex = $derived(this.#hoveredBeatIndex);
	readonly draggedBeatIndex = $derived(this.#draggedBeatIndex);

	// Actions
	setConfig(updates: Partial<BeatFrameConfig>): void {
		this.#config = { ...this.#config, ...updates };
	}

	setHoveredBeat(index: number): void {
		this.#hoveredBeatIndex = index;
	}

	clearHoveredBeat(): void {
		this.#hoveredBeatIndex = -1;
	}

	setDraggedBeat(index: number): void {
		this.#draggedBeatIndex = index;
	}

	clearDraggedBeat(): void {
		this.#draggedBeatIndex = -1;
	}

	// Layout calculations
	private totalColumns(): number {
		return this.#config.columns + (this.#config.hasStartTile ? 1 : 0);
	}

	calculateBeatPosition(index: number): { x: number; y: number } {
		const columnsForBeats = Math.max(1, this.#config.columns);
		const row = Math.floor(index / columnsForBeats);
		const col = (index % columnsForBeats) + (this.#config.hasStartTile ? 1 : 0);

		const step = this.#config.beatSize + this.#config.gap;
		return { x: col * step, y: row * step };
	}

	calculateFrameDimensions(beatCount: number): { width: number; height: number } {
		const step = this.#config.beatSize + this.#config.gap;

		// If no beats, size to just the Start tile (desktop shows START only)
		if (beatCount <= 0) {
			const width = this.#config.hasStartTile ? this.#config.beatSize : 0;
			const height = this.#config.beatSize;
			return { width, height };
		}

		const columnsForBeats = Math.max(1, this.#config.columns);
		const rows = Math.ceil(beatCount / columnsForBeats) || 1;
		const totalCols = this.totalColumns();

		return {
			width: totalCols * step - this.#config.gap,
			height: rows * step - this.#config.gap,
		};
	}

	// Beat interaction helpers
	getBeatAtPosition(x: number, y: number, beatCount: number): number {
		const step = this.#config.beatSize + this.#config.gap;
		const colRaw = Math.floor(x / step);
		const row = Math.floor(y / step);

		// Ignore clicks on the Start tile column
		const startOffset = this.#config.hasStartTile ? 1 : 0;
		if (colRaw < startOffset) return -1;

		const col = colRaw - startOffset;
		const index = row * Math.max(1, this.#config.columns) + col;
		return index >= 0 && index < beatCount ? index : -1;
	}

	isBeatVisible(beat: BeatData): boolean {
		return !beat.is_blank || beat.pictograph_data != null;
	}

	getBeatDisplayText(beat: BeatData): string {
		if (beat.is_blank && !beat.pictograph_data) {
			// fallback: show beat number if available on metadata or domain type
			return (
				beat.beat_number ??
				(beat.metadata as Record<string, unknown>)?.beat_number ??
				''
			).toString();
		}
		const metadataLetter = (beat.metadata as Record<string, unknown>)?.letter;
		return (
			beat.pictograph_data?.letter ??
			(typeof metadataLetter === 'string' ? metadataLetter : '') ??
			''
		);
	}
}

// Singleton instance
export const beatFrameService = new BeatFrameService();
