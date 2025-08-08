/**
 * Pictograph Service - High-level pictograph operations
 * 
 * Coordinates pictograph rendering and manipulation operations.
 */

import type { IPictographService, PictographData, IPictographRenderingService } from '../interfaces';

export class PictographService implements IPictographService {
	constructor(
		private renderingService: IPictographRenderingService
	) {}

	/**
	 * Render a pictograph to SVG
	 */
	async renderPictograph(data: PictographData): Promise<SVGElement> {
		try {
			return await this.renderingService.renderPictograph(data);
		} catch (error) {
			console.error('Failed to render pictograph:', error);
			// Return fallback SVG
			return this.createFallbackSVG();
		}
	}

	/**
	 * Update arrow data in a pictograph
	 */
	async updateArrow(pictographId: string, arrowData: any): Promise<PictographData> {
		// TODO: Implement pictograph data management
		throw new Error('updateArrow not yet implemented');
	}

	/**
	 * Create a fallback SVG when rendering fails
	 */
	private createFallbackSVG(): SVGElement {
		const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
		svg.setAttribute('width', '300');
		svg.setAttribute('height', '300');
		svg.setAttribute('viewBox', '0 0 300 300');
		
		// Add error indicator
		const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
		rect.setAttribute('x', '10');
		rect.setAttribute('y', '10');
		rect.setAttribute('width', '280');
		rect.setAttribute('height', '280');
		rect.setAttribute('fill', '#f3f4f6');
		rect.setAttribute('stroke', '#e5e7eb');
		rect.setAttribute('stroke-width', '2');
		
		const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		text.setAttribute('x', '150');
		text.setAttribute('y', '150');
		text.setAttribute('text-anchor', 'middle');
		text.setAttribute('fill', '#6b7280');
		text.textContent = 'Render Error';
		
		svg.appendChild(rect);
		svg.appendChild(text);
		
		return svg;
	}
}
