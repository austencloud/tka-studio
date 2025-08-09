/**
 * Pictograph Rendering Service - Complete Rendering Engine
 *
 * This service handles the actual SVG rendering of pictographs.
 * Integrates with the sophisticated ArrowPositioningService for accurate positioning.
 */

import type { BeatData } from '@tka/schemas';
import type {
	IPictographRenderingService,
	PictographData,
	IArrowPositioningService,
	IPropRenderingService,
	ArrowPosition,
	GridData,
} from '../interfaces';
import { createGridData, type GridData as RawGridData } from '../../data/gridCoordinates.js';

export class PictographRenderingService implements IPictographRenderingService {
	private readonly SVG_SIZE = 950;
	private readonly CENTER_X = 475;
	private readonly CENTER_Y = 475;

	constructor(
		private arrowPositioning: IArrowPositioningService,
		private propRendering: IPropRenderingService
	) {
		console.log(
			'🎨 PictographRenderingService initialized with sophisticated positioning and prop rendering'
		);
	}

	/**
	 * Render a pictograph from pictograph data
	 */
	async renderPictograph(data: PictographData): Promise<SVGElement> {
		try {
			console.log('🎨 Rendering pictograph with sophisticated positioning:', data.id);
			const svg = this.createBaseSVG();

			// 1. Render grid first
			await this.renderGrid(svg, data.gridData?.mode || 'diamond');

			// 2. Calculate arrow positions using sophisticated positioning service
			const gridMode = data.gridData?.mode || 'diamond';
			const rawGridData = createGridData(gridMode);
			const gridDataWithMode = this.adaptGridData(rawGridData, gridMode);
			console.log('📊 Using real grid data:', gridDataWithMode);

			const arrowPositions = await this.arrowPositioning.calculateAllArrowPositions(
				data,
				gridDataWithMode
			);
			console.log(
				`🏹 Calculated ${arrowPositions.size} arrow positions:`,
				Object.fromEntries(arrowPositions)
			);

			// 3. Render arrows with sophisticated calculated positions
			for (const [color, position] of arrowPositions.entries()) {
				console.log(`🎯 Rendering ${color} arrow at sophisticated position:`, position);
				const motionData = data.motions?.[color as 'blue' | 'red'];
				await this.renderArrowAtPosition(
					svg,
					color as 'blue' | 'red',
					position,
					motionData
				);
			}

			// 4. Render props
			await this.renderProps(svg, data);

			// 5. Render glyph overlays (letter, VTG, elemental) if assets are present
			await this.renderOverlays(svg, data);

			// 6. Add metadata
			this.renderIdLabel(svg, data);
			this.renderDebugInfo(svg, data, arrowPositions);

			console.log('✅ Pictograph rendering complete with sophisticated positioning');
			return svg;
		} catch (error) {
			console.error('❌ Error rendering pictograph:', error);
			const errorMessage = error instanceof Error ? error.message : 'Unknown error';
			return this.createErrorSVG(errorMessage);
		}
	}

	/** Render glyph overlays (letters now; VTG/elemental when data is available) */
	private async renderOverlays(svg: SVGElement, data: PictographData): Promise<void> {
		try {
			if (data.letter) {
				await this.renderLetterGlyph(svg, data.letter);
			}
		} catch (e) {
			console.warn('Overlay rendering skipped:', e);
		}
	}

	private async renderLetterGlyph(svg: SVGElement, letter: string): Promise<void> {
		// Map common Greek letters to Type6 assets
		const map: Record<string, string> = {
			α: '/images/letters_trimmed/Type6/Alpha.svg',
			β: '/images/letters_trimmed/Type6/Beta.svg',
			γ: '/images/letters_trimmed/Type6/Gamma.svg',
		};
		const path = map[letter];
		if (!path) return; // only render supported letters for now

		const res = await fetch(path);
		if (!res.ok) return;
		const content = await res.text();
		const parser = new DOMParser();
		const doc = parser.parseFromString(content, 'image/svg+xml');
		const el = doc.documentElement as unknown as SVGElement;

		// Create a group and insert first to measure natural size, then position bottom-left
		const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		group.setAttribute('class', 'tka-letter');
		group.setAttribute('opacity', '0'); // hide during measurement
		const imported = document.importNode(el, true);
		group.appendChild(imported);
		svg.appendChild(group);

		// Measure bounding box after insertion
		let bbox: DOMRect;
		try {
			bbox = group.getBBox();
		} catch {
			// Fallback if getBBox fails
			bbox = new DOMRect(0, 0, 120, 80);
		}
		const letterHeight = bbox.height || 80;
		const x = Math.round(letterHeight / 1.5);
		const y = Math.round(this.SVG_SIZE - letterHeight * 1.7);
		group.setAttribute('transform', `translate(${x}, ${y})`);
		group.removeAttribute('opacity');
	}

	/** Render overlays from glyphData on BeatData (VTG and elemental) */
	private async renderOverlaysFromGlyphData(svg: SVGElement, glyphData?: any): Promise<void> {
		if (!glyphData) return;
		try {
			// VTG glyphs
			const vtg = glyphData.vtg_mode as string | undefined;
			if (vtg) {
				const vtgMap: Record<string, string> = {
					SS: '/images/vtg_glyphs/SS.svg',
					SO: '/images/vtg_glyphs/SO.svg',
					TS: '/images/vtg_glyphs/TS.svg',
					TO: '/images/vtg_glyphs/TO.svg',
					QS: '/images/vtg_glyphs/QS.svg',
					QO: '/images/vtg_glyphs/QO.svg',
				};
				const path = vtgMap[vtg];
				if (path) await this.renderVtgGlyph(svg, path);
			}

			// Elemental glyphs
			const elemental = glyphData.elemental_type as string | undefined;
			if (elemental) {
				const elemMap: Record<string, string> = {
					water: '/images/elements/water.svg',
					fire: '/images/elements/fire.svg',
					earth: '/images/elements/earth.svg',
					air: '/images/elements/air.svg',
					sun: '/images/elements/sun.svg',
					moon: '/images/elements/moon.svg',
				};
				const path = elemMap[elemental];
				if (path) await this.renderElementalGlyph(svg, path);
			}
		} catch (e) {
			console.warn('Glyph overlay rendering failed:', e);
		}
	}

	private async renderVtgGlyph(svg: SVGElement, path: string): Promise<void> {
		// Legacy: bottom-right, 4% offset, ~0.7 scale
		const offsetPct = 0.04;
		const scale = 0.7;
		const res = await fetch(path);
		if (!res.ok) return;
		const content = await res.text();
		const parser = new DOMParser();
		const doc = parser.parseFromString(content, 'image/svg+xml');
		const el = doc.documentElement as unknown as SVGElement;
		const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		g.setAttribute('class', 'vtg-glyph');
		g.setAttribute('opacity', '0');
		g.appendChild(document.importNode(el, true));
		svg.appendChild(g);
		let bbox: DOMRect;
		try {
			bbox = g.getBBox();
		} catch {
			bbox = new DOMRect(0, 0, 100, 100);
		}
		const ox = this.SVG_SIZE * offsetPct;
		const oy = this.SVG_SIZE * offsetPct;
		const x = this.SVG_SIZE - bbox.width * scale - ox;
		const y = this.SVG_SIZE - bbox.height * scale - oy;
		g.setAttribute('transform', `translate(${x}, ${y}) scale(${scale})`);
		g.removeAttribute('opacity');
	}

	private async renderElementalGlyph(svg: SVGElement, path: string): Promise<void> {
		// Legacy: top-right, 4% offset
		const offsetPct = 0.04;
		const res = await fetch(path);
		if (!res.ok) return;
		const content = await res.text();
		const parser = new DOMParser();
		const doc = parser.parseFromString(content, 'image/svg+xml');
		const el = doc.documentElement as unknown as SVGElement;
		const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		g.setAttribute('class', 'elemental-glyph');
		g.setAttribute('opacity', '0');
		g.appendChild(document.importNode(el, true));
		svg.appendChild(g);
		let bbox: DOMRect;
		try {
			bbox = g.getBBox();
		} catch {
			bbox = new DOMRect(0, 0, 100, 100);
		}
		const ox = this.SVG_SIZE * offsetPct;
		const oy = this.SVG_SIZE * offsetPct;
		const x = this.SVG_SIZE - bbox.width - ox;
		const y = oy;
		g.setAttribute('transform', `translate(${x}, ${y})`);
		g.removeAttribute('opacity');
	}

	/**
	 * Render a beat as a pictograph
	 */
	async renderBeat(beat: BeatData): Promise<SVGElement> {
		// Convert beat data to pictograph data
		const pictographData = this.beatToPictographData(beat);
		const svg = await this.renderPictograph(pictographData);
		// Render VTG/elemental overlays if glyphData is provided
		await this.renderOverlaysFromGlyphData(svg, beat.glyphData as any);
		return svg;
	}

	/**
	 * Create base SVG element
	 */
	private createBaseSVG(): SVGElement {
		const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
		svg.setAttribute('width', this.SVG_SIZE.toString());
		svg.setAttribute('height', this.SVG_SIZE.toString());
		svg.setAttribute('viewBox', `0 0 ${this.SVG_SIZE} ${this.SVG_SIZE}`);
		svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');

		// Add background
		const background = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
		background.setAttribute('width', '100%');
		background.setAttribute('height', '100%');
		background.setAttribute('fill', '#ffffff');
		svg.appendChild(background);

		return svg;
	}

	/**
	 * Adapt raw grid data to match the interface requirements
	 */
	private adaptGridData(rawGridData: RawGridData, mode: 'diamond' | 'box'): GridData {
		// Filter out null coordinates and adapt to interface
		const adaptPoints = (
			points: Record<string, { coordinates: { x: number; y: number } | null }>
		) => {
			const adapted: Record<string, { coordinates: { x: number; y: number } }> = {};
			for (const [key, point] of Object.entries(points)) {
				if (point.coordinates) {
					adapted[key] = { coordinates: point.coordinates };
				}
			}
			return adapted;
		};

		return {
			mode,
			allLayer2PointsNormal: adaptPoints(rawGridData.allLayer2PointsNormal || {}),
			allHandPointsNormal: adaptPoints(rawGridData.allHandPointsNormal || {}),
		};
	}

	/**
	 * Render arrow at sophisticated calculated position using real SVG assets
	 */
	private async renderArrowAtPosition(
		svg: SVGElement,
		color: 'blue' | 'red',
		position: ArrowPosition,
		motionData: any
	): Promise<void> {
		console.log(`🎨 Rendering ${color} arrow with sophisticated positioning:`, position);

		try {
			// Get the correct arrow SVG path
			const arrowSvgPath = this.getArrowSvgPath(motionData);
			console.log(`🏹 Loading arrow SVG: ${arrowSvgPath}`);

			// Load the arrow SVG
			const response = await fetch(arrowSvgPath);
			if (!response.ok) {
				throw new Error(`Failed to load arrow SVG: ${response.status}`);
			}

			const svgContent = await response.text();

			// Create arrow group with metadata
			const arrowGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
			arrowGroup.setAttribute('class', `arrow-${color} sophisticated-positioning`);
			arrowGroup.setAttribute('data-color', color);
			arrowGroup.setAttribute('data-position', `${position.x},${position.y}`);
			arrowGroup.setAttribute('data-rotation', position.rotation.toString());

			// Apply sophisticated position and rotation transform
			const transform = `translate(${position.x}, ${position.y}) rotate(${position.rotation})`;
			arrowGroup.setAttribute('transform', transform);

			// Parse and insert the SVG content
			const parser = new DOMParser();
			const svgDoc = parser.parseFromString(svgContent, 'image/svg+xml');
			const svgElement = svgDoc.documentElement as unknown as SVGElement;

			// Apply color transformation
			this.applyArrowColorTransformation(svgElement, color);

			// Import the SVG content into the arrow group
			const importedSvg = document.importNode(svgElement, true);
			arrowGroup.appendChild(importedSvg);

			svg.appendChild(arrowGroup);
			console.log(`✅ ${color} arrow rendered with real SVG asset`);
		} catch (error) {
			console.error(`❌ Error loading arrow SVG for ${color}:`, error);
			// Fallback to simple arrow
			this.renderFallbackArrow(svg, color, position);
		}
	}

	/**
	 * Get the correct arrow SVG path based on motion data (like ArrowSvgManager)
	 */
	private getArrowSvgPath(motionData: any): string {
		if (!motionData) {
			return '/images/arrows/static/from_radial/static_0.svg'; // Default fallback
		}

		const motionType = motionData.motionType || 'static';
		const turns = motionData.turns || 0;
		const startOri = motionData.startOrientation || 'in';

		// Handle float arrows (special case)
		if (motionType === 'float') {
			return '/images/arrows/float.svg';
		}

		// Determine radial path based on start orientation
		const radialPath = startOri === 'in' ? 'from_radial' : 'from_nonradial';

		// Format turns to match filename (e.g., 0 -> "0.0", 1 -> "1.0", 0.5 -> "0.5")
		const turnsStr = turns % 1 === 0 ? `${turns}.0` : turns.toString();

		// Construct path: /images/arrows/{motionType}/{radialPath}/{motionType}_{turns}.svg
		return `/images/arrows/${motionType}/${radialPath}/${motionType}_${turnsStr}.svg`;
	}

	/**
	 * Apply color transformation to arrow SVG
	 */
	private applyArrowColorTransformation(svgElement: SVGElement, color: 'blue' | 'red'): void {
		// Find all path elements and apply color
		const paths = svgElement.querySelectorAll('path');
		const fillColor = color === 'blue' ? '#3b82f6' : '#ef4444';
		const strokeColor = color === 'blue' ? '#1d4ed8' : '#dc2626';

		paths.forEach((path) => {
			path.setAttribute('fill', fillColor);
			path.setAttribute('stroke', strokeColor);
			path.setAttribute('stroke-width', '1');
		});
	}

	/**
	 * Render fallback arrow if SVG loading fails
	 */
	private renderFallbackArrow(
		svg: SVGElement,
		color: 'blue' | 'red',
		position: ArrowPosition
	): void {
		console.log(`🔄 Rendering fallback arrow for ${color}`);

		// Create arrow group
		const arrowGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		arrowGroup.setAttribute('class', `arrow-${color} fallback`);
		arrowGroup.setAttribute(
			'transform',
			`translate(${position.x}, ${position.y}) rotate(${position.rotation})`
		);

		// Create simple arrow path
		const arrowPath = this.createEnhancedArrowPath(color);
		arrowGroup.appendChild(arrowPath);

		svg.appendChild(arrowGroup);
	}

	/**
	 * Create enhanced arrow SVG path with sophisticated styling
	 */
	private createEnhancedArrowPath(color: 'blue' | 'red'): SVGElement {
		const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');

		// More sophisticated arrow shape
		path.setAttribute('d', 'M 0,-25 L 15,0 L 0,25 L -8,15 L -8,-15 Z');
		path.setAttribute('fill', color);
		path.setAttribute('stroke', '#000000');
		path.setAttribute('stroke-width', '2');
		path.setAttribute('opacity', '0.9');

		// Add sophisticated styling
		path.setAttribute('filter', 'drop-shadow(1px 1px 2px rgba(0,0,0,0.3))');
		path.setAttribute('class', 'sophisticated-arrow');

		return path;
	}

	/**
	 * Create position indicator for debugging
	 */
	private createPositionIndicator(color: 'blue' | 'red'): SVGElement {
		const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
		circle.setAttribute('cx', '0');
		circle.setAttribute('cy', '0');
		circle.setAttribute('r', '3');
		circle.setAttribute('fill', color === 'blue' ? '#0066ff' : '#ff0066');
		circle.setAttribute('opacity', '0.7');
		circle.setAttribute('class', 'position-indicator');
		return circle;
	}

	/**
	 * Render ID label with enhanced metadata
	 */
	private renderIdLabel(svg: SVGElement, data: PictographData): void {
		const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		text.setAttribute('x', this.CENTER_X.toString());
		text.setAttribute('y', (this.CENTER_Y + 130).toString());
		text.setAttribute('text-anchor', 'middle');
		text.setAttribute('font-family', 'monospace');
		text.setAttribute('font-size', '11');
		text.setAttribute('fill', '#4b5563');
		text.textContent = `${data.id.slice(-8)} • Sophisticated Positioning`;
		svg.appendChild(text);
	}

	/**
	 * Render debug information about positioning
	 */
	private renderDebugInfo(
		svg: SVGElement,
		data: PictographData,
		positions: Map<string, ArrowPosition>
	): void {
		let yOffset = 15;

		for (const [color, position] of positions.entries()) {
			const debugText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			debugText.setAttribute('x', '10');
			debugText.setAttribute('y', yOffset.toString());
			debugText.setAttribute('font-family', 'monospace');
			debugText.setAttribute('font-size', '10');
			debugText.setAttribute('fill', '#6b7280');
			debugText.textContent = `${color}: [${position.x.toFixed(1)}, ${position.y.toFixed(1)}] ∠${position.rotation.toFixed(0)}°`;
			svg.appendChild(debugText);
			yOffset += 12;
		}

		// Add letter info if present
		if (data.letter) {
			const letterText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			letterText.setAttribute('x', '10');
			letterText.setAttribute('y', yOffset.toString());
			letterText.setAttribute('font-family', 'monospace');
			letterText.setAttribute('font-size', '10');
			letterText.setAttribute('fill', '#059669');
			letterText.setAttribute('font-weight', 'bold');
			letterText.textContent = `Letter: ${data.letter}`;

			svg.appendChild(letterText);
		}
	}

	/**
	 * Render props for both colors
	 * DISABLED: Props are now rendered by Prop.svelte components to avoid duplicates
	 */
	private async renderProps(svg: SVGElement, data: PictographData): Promise<void> {
		// Props are now handled by ModernPictograph.svelte -> Prop.svelte components
		// This service-level rendering is disabled to prevent duplicate CIRCLE_PROP elements
		console.log('🎭 Props rendering delegated to Prop.svelte components');
		return;
	}

	/**
	 * Render grid using real SVG assets
	 */
	private async renderGrid(
		svg: SVGElement,
		gridMode: 'diamond' | 'box' = 'diamond'
	): Promise<void> {
		try {
			// Load the appropriate grid SVG
			const gridPath = `/images/grid/${gridMode}_grid.svg`;
			console.log(`🔲 Loading grid SVG: ${gridPath}`);

			// Create image element for the grid
			const gridImage = document.createElementNS('http://www.w3.org/2000/svg', 'image');
			gridImage.setAttribute('href', gridPath);
			gridImage.setAttribute('x', '0');
			gridImage.setAttribute('y', '0');
			gridImage.setAttribute('width', this.SVG_SIZE.toString());
			gridImage.setAttribute('height', this.SVG_SIZE.toString());
			gridImage.setAttribute('preserveAspectRatio', 'none');

			svg.appendChild(gridImage);
			console.log(`✅ Grid rendered: ${gridMode} mode`);
		} catch (error) {
			console.error(`❌ Error loading grid SVG for ${gridMode} mode:`, error);
			// Fallback: render a simple grid outline
			this.renderFallbackGrid(svg, gridMode);
		}
	}

	/**
	 * Fallback grid rendering if SVG loading fails
	 */
	private renderFallbackGrid(svg: SVGElement, gridMode: 'diamond' | 'box'): void {
		const gridGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		gridGroup.setAttribute('class', `fallback-grid-${gridMode}`);

		if (gridMode === 'diamond') {
			// Create diamond outline
			const diamond = document.createElementNS('http://www.w3.org/2000/svg', 'polygon');
			const size = 143; // Approximate size based on real coordinates
			const points = [
				`${this.CENTER_X},${this.CENTER_Y - size}`, // top
				`${this.CENTER_X + size},${this.CENTER_Y}`, // right
				`${this.CENTER_X},${this.CENTER_Y + size}`, // bottom
				`${this.CENTER_X - size},${this.CENTER_Y}`, // left
			].join(' ');

			diamond.setAttribute('points', points);
			diamond.setAttribute('fill', 'none');
			diamond.setAttribute('stroke', '#e5e7eb');
			diamond.setAttribute('stroke-width', '2');
			gridGroup.appendChild(diamond);
		} else {
			// Create box outline
			const box = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
			const size = 202; // Approximate size based on real coordinates
			box.setAttribute('x', (this.CENTER_X - size / 2).toString());
			box.setAttribute('y', (this.CENTER_Y - size / 2).toString());
			box.setAttribute('width', size.toString());
			box.setAttribute('height', size.toString());
			box.setAttribute('fill', 'none');
			box.setAttribute('stroke', '#e5e7eb');
			box.setAttribute('stroke-width', '2');
			gridGroup.appendChild(box);
		}

		svg.appendChild(gridGroup);
	}

	/**
	 * Convert beat data to pictograph data
	 */
	private beatToPictographData(beat: BeatData): PictographData {
		return {
			id: `beat-${beat.beatNumber}`,
			gridData: { mode: 'diamond' },
			arrows: { blue: {}, red: {} },
			props: { blue: {}, red: {} },
			motions: {
				blue: beat.blueMotion,
				red: beat.redMotion,
			},
			letter: beat.letter,
		};
	}

	/**
	 * Create error SVG with detailed error information
	 */
	private createErrorSVG(errorMessage?: string): SVGElement {
		const svg = this.createBaseSVG();

		const errorText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		errorText.setAttribute('x', this.CENTER_X.toString());
		errorText.setAttribute('y', this.CENTER_Y.toString());
		errorText.setAttribute('text-anchor', 'middle');
		errorText.setAttribute('fill', '#dc2626');
		errorText.setAttribute('font-weight', 'bold');
		errorText.textContent = 'Rendering Error';

		if (errorMessage) {
			const detailText = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			detailText.setAttribute('x', this.CENTER_X.toString());
			detailText.setAttribute('y', (this.CENTER_Y + 20).toString());
			detailText.setAttribute('text-anchor', 'middle');
			detailText.setAttribute('fill', '#dc2626');
			detailText.setAttribute('font-size', '12');
			detailText.textContent =
				errorMessage.substring(0, 50) + (errorMessage.length > 50 ? '...' : '');
			svg.appendChild(detailText);
		}

		svg.appendChild(errorText);
		return svg;
	}
}
