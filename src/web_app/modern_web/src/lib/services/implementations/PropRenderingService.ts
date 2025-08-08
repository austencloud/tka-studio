/**
 * Prop Rendering Service - Web Implementation
 * 
 * This service handles prop rendering for the web app, including:
 * - Loading and caching prop SVG assets
 * - Applying color transformations
 * - Calculating prop positions based on motion data
 * - Rendering props as SVG elements
 */

import type {
	IPropRenderingService,
	PropPosition,
	MotionData,
	GridMode,
	Location
} from '../interfaces';
import { createGridData, type GridData } from '../../data/gridCoordinates.js';

export class PropRenderingService implements IPropRenderingService {
	private svgCache = new Map<string, string>();
	private readonly SUPPORTED_PROPS = ['staff', 'hand', 'fan'];
	
	// Color transformation constants (matching desktop)
	private readonly COLOR_TRANSFORMATIONS = {
		blue: '#2E3192',
		red: '#ED1C24'
	};

	constructor() {
		console.log('🎭 PropRenderingService initialized');
	}

	/**
	 * Render a prop as an SVG element
	 */
	async renderProp(
		propType: string,
		color: 'blue' | 'red',
		motionData: MotionData,
		gridMode: GridMode = 'diamond'
	): Promise<SVGElement> {
		try {
			console.log(`🎭 Rendering ${color} ${propType} prop`);

			// Load and color the SVG
			const svgContent = await this.loadPropSVG(propType, color);
			
			// Calculate position
			const position = await this.calculatePropPosition(motionData, color, gridMode);
			
			// Create SVG element
			const propElement = this.createPropElement(svgContent, position, propType, color);
			
			console.log(`✅ ${color} ${propType} prop rendered at position:`, position);
			return propElement;

		} catch (error) {
			console.error(`❌ Error rendering ${color} ${propType} prop:`, error);
			return this.createErrorProp(propType, color);
		}
	}

	/**
	 * Calculate prop position based on motion data using real grid coordinates
	 */
	async calculatePropPosition(
		motionData: MotionData,
		color: 'blue' | 'red',
		gridMode: GridMode = 'diamond'
	): Promise<PropPosition> {
		try {
			// Use end location for prop positioning
			const location = (motionData?.endLoc as any) || 's';
			const gridData = createGridData(gridMode);
			const basePosition = this.getLocationCoordinates(location, gridMode, gridData);

			// Calculate rotation based on motion orientation
			const rotation = this.calculatePropRotation(motionData);

			// Apply small offset for color separation
			const offset = this.getColorOffset(color);

			return {
				x: basePosition.x + offset.x,
				y: basePosition.y + offset.y,
				rotation
			};

		} catch (error) {
			console.error('❌ Error calculating prop position:', error);
			// Return center position as fallback (950x950 scene)
			return { x: 475, y: 475, rotation: 0 };
		}
	}

	/**
	 * Load prop SVG with color transformation
	 */
	async loadPropSVG(propType: string, color: 'blue' | 'red'): Promise<string> {
		const cacheKey = `${propType}_${color}`;
		
		if (this.svgCache.has(cacheKey)) {
			return this.svgCache.get(cacheKey)!;
		}

		try {
			// Load base SVG
			const response = await fetch(`/images/props/${propType}.svg`);
			if (!response.ok) {
				throw new Error(`Failed to load ${propType}.svg: ${response.status}`);
			}
			
			let svgContent = await response.text();
			
			// Apply color transformation
			svgContent = this.applyColorTransformation(svgContent, color);
			
			// Cache the result
			this.svgCache.set(cacheKey, svgContent);
			
			console.log(`📦 Loaded and cached ${propType} SVG for ${color}`);
			return svgContent;

		} catch (error) {
			console.error(`❌ Error loading ${propType} SVG:`, error);
			// Return fallback SVG
			return this.createFallbackSVG(propType, color);
		}
	}

	/**
	 * Get supported prop types
	 */
	getSupportedPropTypes(): string[] {
		return [...this.SUPPORTED_PROPS];
	}

	/**
	 * Apply color transformation to SVG content
	 */
	private applyColorTransformation(svgContent: string, color: 'blue' | 'red'): string {
		const targetColor = this.COLOR_TRANSFORMATIONS[color];
		
		// Replace common fill patterns
		svgContent = svgContent.replace(/fill="[^"]*"/g, `fill="${targetColor}"`);
		svgContent = svgContent.replace(/fill:[^;]*/g, `fill:${targetColor}`);
		
		// Replace stroke patterns for outlines
		svgContent = svgContent.replace(/stroke="[^"]*"/g, `stroke="${targetColor}"`);
		svgContent = svgContent.replace(/stroke:[^;]*/g, `stroke:${targetColor}`);
		
		return svgContent;
	}

	/**
	 * Get coordinates for a location on the grid using real grid data
	 */
	private getLocationCoordinates(location: Location, gridMode: GridMode, gridData: GridData): { x: number; y: number } {
		// Props are positioned at hand points based on their end location
		const pointName = `${location}_${gridMode}_hand_point`;
		const point = gridData.allHandPointsNormal?.[pointName];

		if (point?.coordinates) {
			return point.coordinates;
		}

		// Fallback to center if point not found
		console.warn(`Hand point '${pointName}' not found, using center`);
		return gridData.centerPoint?.coordinates || { x: 475, y: 475 };
	}

	/**
	 * Calculate prop rotation based on motion data
	 */
	private calculatePropRotation(motionData: MotionData): number {
		// Basic rotation based on end orientation
		const orientationRotations = {
			'in': 0,
			'out': 180,
			'clock': 90,
			'counter': 270
		};

		const baseRotation = orientationRotations[motionData.endOri || 'in'];
		
		// Add motion type adjustments
		let adjustment = 0;
		if (motionData.motionType === 'anti') {
			adjustment += 180;
		}

		return (baseRotation + adjustment) % 360;
	}

	/**
	 * Get small offset for color separation
	 */
	private getColorOffset(color: 'blue' | 'red'): { x: number; y: number } {
		// Small offset to prevent props from overlapping
		return color === 'blue' ? { x: -8, y: -8 } : { x: 8, y: 8 };
	}

	/**
	 * Create prop SVG element with positioning
	 */
	private createPropElement(
		svgContent: string,
		position: PropPosition,
		propType: string,
		color: 'blue' | 'red'
	): SVGElement {
		// Parse SVG content
		const parser = new DOMParser();
		const svgDoc = parser.parseFromString(svgContent, 'image/svg+xml');
		const svgElement = svgDoc.documentElement;

		// Create wrapper group
		const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		group.setAttribute('class', `prop-${color} prop-${propType}`);
		group.setAttribute('data-prop-type', propType);
		group.setAttribute('data-color', color);
		
		// Apply transform for positioning and rotation
		const transform = `translate(${position.x}, ${position.y}) rotate(${position.rotation}) scale(0.3)`;
		group.setAttribute('transform', transform);

		// Copy SVG content to group
		while (svgElement.firstChild) {
			group.appendChild(svgElement.firstChild);
		}

		return group;
	}

	/**
	 * Create fallback SVG for missing props
	 */
	private createFallbackSVG(propType: string, color: 'blue' | 'red'): string {
		const fillColor = this.COLOR_TRANSFORMATIONS[color];
		return `
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
				<rect x="10" y="10" width="80" height="80" fill="${fillColor}" opacity="0.5"/>
				<text x="50" y="55" text-anchor="middle" font-size="12" fill="white">${propType}</text>
			</svg>
		`;
	}

	/**
	 * Create error prop element
	 */
	private createErrorProp(propType: string, color: 'blue' | 'red'): SVGElement {
		const group = document.createElementNS('http://www.w3.org/2000/svg', 'g');
		group.setAttribute('class', `prop-error prop-${color}`);
		
		const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
		circle.setAttribute('cx', '150');
		circle.setAttribute('cy', '150');
		circle.setAttribute('r', '10');
		circle.setAttribute('fill', '#dc2626');
		circle.setAttribute('opacity', '0.7');
		
		group.appendChild(circle);
		return group;
	}
}
