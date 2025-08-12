/**
 * SVG Generator for creating prop staff images and grid
 * Based on the exact implementation from standalone_animator.html
 */

export class SVGGenerator {
	/**
	 * Generate grid SVG exactly as in standalone_animator.html
	 */
	static generateGridSvg(): string {
		return `<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 950 950" style="enable-background:new 0 0 950 950; background-color: #ffffff;" xml:space="preserve"><g id="outer_points"><circle fill="#000000" cx="475" cy="175" r="25"/><circle fill="#000000" cx="775" cy="475" r="25"/><circle fill="#000000" cx="475" cy="775" r="25"/><circle fill="#000000" cx="175" cy="475" r="25"/></g><g id="halfway_points"><circle fill="#000000" cx="475" cy="323.5" r="8"/><circle fill="#000000" cx="626.5" cy="475" r="8"/><circle fill="#000000" cx="475" cy="626.5" r="8"/><circle fill="#000000" cx="323.5" cy="475" r="8"/></g><g id="center_group"><circle fill="#000000" cx="475" cy="475" r="12"/></g></svg>`;
	}

	/**
	 * Generate blue staff SVG exactly as in standalone_animator.html
	 */
	static generateBlueStaffSvg(): string {
		return `<svg version="1.1" id="staff" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 252.8 77.8" style="enable-background:new 0 0 252.8 77.8;" xml:space="preserve"><path fill="#2E3192" stroke="#555555" stroke-width="1" stroke-miterlimit="10" d="M251.4,67.7V10.1c0-4.8-4.1-8.7-9.1-8.7s-9.1,3.9-9.1,8.7v19.2H10.3c-4.9,0-8.9,3.8-8.9,8.5V41 c0,4.6,4,8.5,8.9,8.5h222.9v18.2c0,4.8,4.1,8.7,9.1,8.7S251.4,72.5,251.4,67.7z"/><circle id="centerPoint" fill="#FF0000" cx="126.4" cy="38.9" r="5" /></svg>`;
	}

	/**
	 * Generate red staff SVG exactly as in standalone_animator.html
	 */
	static generateRedStaffSvg(): string {
		return `<svg version="1.1" id="staff" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 252.8 77.8" style="enable-background:new 0 0 252.8 77.8;" xml:space="preserve"><path fill="#ED1C24" stroke="#555555" stroke-width="1" stroke-miterlimit="10" d="M251.4,67.7V10.1c0-4.8-4.1-8.7-9.1-8.7s-9.1,3.9-9.1,8.7v19.2H10.3c-4.9,0-8.9,3.8-8.9,8.5V41 c0,4.6,4,8.5,8.9,8.5h222.9v18.2c0,4.8,4.1,8.7,9.1,8.7S251.4,72.5,251.4,67.7z"/><circle id="centerPoint" fill="#FF0000" cx="126.4" cy="38.9" r="5" /></svg>`;
	}
}
