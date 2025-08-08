import { PROP_COLORS } from '../../constants/colors.js';
// import { ANIMATION_CONSTANTS } from '../../constants/animation.js'; // Not used currently

/**
 * Utility class for generating SVG strings for canvas rendering
 */
export class SVGGenerator {
	/**
	 * Generate theme-aware grid SVG
	 */
	static generateGridSvg(showLayer2: boolean, isDarkMode: boolean): string {
		const gridColor = isDarkMode ? '#ffffff' : '#000000';
		const layer2Color = showLayer2 ? gridColor : 'none';

		return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 950">
			<g>
				<circle fill="${gridColor}" cx="475" cy="175" r="25"/>
				<circle fill="${gridColor}" cx="775" cy="475" r="25"/>
				<circle fill="${gridColor}" cx="475" cy="775" r="25"/>
				<circle fill="${gridColor}" cx="175" cy="475" r="25"/>
			</g>


			<g>
				<circle fill="${layer2Color}" cx="625" cy="325" r="8.8"/>
				<circle fill="${layer2Color}" cx="625" cy="625" r="8.8"/>
				<circle fill="${layer2Color}" cx="325" cy="625" r="8.8"/>
				<circle fill="${layer2Color}" cx="325" cy="325" r="8.8"/>
			</g>
			<g>
				<circle fill="${layer2Color}" cx="475" cy="325" r="4.7"/>
				<circle fill="${layer2Color}" cx="625" cy="475" r="4.7"/>
				<circle fill="${layer2Color}" cx="475" cy="625" r="4.7"/>
				<circle fill="${layer2Color}" cx="325" cy="475" r="4.7"/>
			</g>
			<circle fill="${gridColor}" cx="475" cy="475" r="12"/>
		</svg>`;
	}

	/**
	 * Generate blue staff SVG using exact design from specification
	 */
	static generateBlueStaffSvg(): string {
		return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 252.8 77.8" style="enable-background:new 0 0 252.8 77.8;">
			<style type="text/css">
				.staff-body { fill: ${PROP_COLORS.BLUE}; stroke: #FFFFFF; stroke-width: 2.75; stroke-miterlimit: 10; }
				.center-point { fill: #0000FF; }
			</style>
			<path class="staff-body" d="M251.4,67.7V10.1c0-4.8-4.1-8.7-9.1-8.7s-9.1,3.9-9.1,8.7v19.2H10.3c-4.9,0-8.9,3.8-8.9,8.5V41
				c0,4.6,4,8.5,8.9,8.5h222.9v18.2c0,4.8,4.1,8.7,9.1,8.7S251.4,72.5,251.4,67.7z"/>
			<circle class="center-point" cx="126.4" cy="38.9" r="2"/>
		</svg>`;
	}

	/**
	 * Generate red staff SVG using exact design from specification
	 */
	static generateRedStaffSvg(): string {
		return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 252.8 77.8" style="enable-background:new 0 0 252.8 77.8;">
			<style type="text/css">
				.staff-body { fill: ${PROP_COLORS.RED}; stroke: #FFFFFF; stroke-width: 2.75; stroke-miterlimit: 10; }
				.center-point { fill: #0000FF; }
			</style>
			<path class="staff-body" d="M251.4,67.7V10.1c0-4.8-4.1-8.7-9.1-8.7s-9.1,3.9-9.1,8.7v19.2H10.3c-4.9,0-8.9,3.8-8.9,8.5V41
				c0,4.6,4,8.5,8.9,8.5h222.9v18.2c0,4.8,4.1,8.7,9.1,8.7S251.4,72.5,251.4,67.7z"/>
			<circle class="center-point" cx="126.4" cy="38.9" r="2"/>
		</svg>`;
	}
}
