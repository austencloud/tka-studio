import { GridMode } from "$domain";

/**
 * SVG Generator for creating prop staff images and grid
 * Based on the exact implementation from standalone_animator.html
 */

export class SVGGenerator {
  /**
   * Generate grid SVG exactly as in standalone_animator.html
   * @param gridMode - Type of grid to generate (GridMode.DIAMOND or GridMode.BOX)
   */
  static generateGridSvg(gridMode: GridMode = GridMode.DIAMOND): string {
    if (gridMode === GridMode.BOX) {
      return `<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 950 950" style="enable-background:new 0 0 950 950;" xml:space="preserve">
<style type="text/css">
	.st0{stroke:#000000;stroke-width:7;stroke-miterlimit:10;}
	.st1{fill:none;}
</style>
<circle id="center_point" cx="475" cy="475" r="11.2"/>
<path id="ne_box_outer_point" class="st0" d="M262.9,247.9c4,0,7.8,1.6,10.6,4.4c5.8,5.8,5.8,15.4,0,21.2c-2.8,2.8-6.6,4.4-10.6,4.4
	s-7.8-1.6-10.6-4.4c-5.8-5.8-5.8-15.4,0-21.2C255.1,249.4,258.9,247.9,262.9,247.9 M262.9,237.9c-6.4,0-12.8,2.4-17.7,7.3
	c-9.8,9.8-9.8,25.6,0,35.4c4.9,4.9,11.3,7.3,17.7,7.3s12.8-2.4,17.7-7.3c9.8-9.8,9.8-25.6,0-35.4
	C275.7,240.3,269.3,237.9,262.9,237.9L262.9,237.9z"/>
<path id="se_box_outer_point" class="st0" d="M687.1,247.9c4,0,7.8,1.6,10.6,4.4c5.8,5.8,5.8,15.4,0,21.2c-2.8,2.8-6.6,4.4-10.6,4.4
	s-7.8-1.6-10.6-4.4c-5.8-5.8-5.8-15.4,0-21.2C679.4,249.4,683.1,247.9,687.1,247.9 M687.1,237.9c-6.4,0-12.8,2.4-17.7,7.3
	c-9.8,9.8-9.8,25.6,0,35.4c4.9,4.9,11.3,7.3,17.7,7.3s12.8-2.4,17.7-7.3c9.8-9.8,9.8-25.6,0-35.4
	C699.9,240.3,693.5,237.9,687.1,237.9L687.1,237.9z"/>
<path id="sw_box_outer_point" class="st0" d="M687.1,672.1c4,0,7.8,1.6,10.6,4.4c5.8,5.8,5.8,15.4,0,21.2c-2.8,2.8-6.6,4.4-10.6,4.4
	s-7.8-1.6-10.6-4.4c-5.8-5.8-5.8-15.4,0-21.2C679.4,673.7,683.1,672.1,687.1,672.1 M687.1,662.1c-6.4,0-12.8,2.4-17.7,7.3
	c-9.8,9.8-9.8,25.6,0,35.4c4.9,4.9,11.3,7.3,17.7,7.3s12.8-2.4,17.7-7.3c9.8-9.8,9.8-25.6,0-35.4
	C699.9,664.6,693.5,662.1,687.1,662.1L687.1,662.1z"/>
<path id="nw_box_outer_point" class="st0" d="M262.9,672.1c4,0,7.8,1.6,10.6,4.4c5.8,5.8,5.8,15.4,0,21.2c-2.8,2.8-6.6,4.4-10.6,4.4
	s-7.8-1.6-10.6-4.4c-5.8-5.8-5.8-15.4,0-21.2C255.1,673.7,258.9,672.1,262.9,672.1 M262.9,662.1c-6.4,0-12.8,2.4-17.7,7.3
	c-9.8,9.8-9.8,25.6,0,35.4c4.9,4.9,11.3,7.3,17.7,7.3s12.8-2.4,17.7-7.3c9.8-9.8,9.8-25.6,0-35.4
	C275.7,664.6,269.3,662.1,262.9,662.1L262.9,662.1z"/>
<g>
	<circle id="nw_box_hand_point" cx="373.8" cy="373.8" r="8"/>
	<circle id="ne_box_hand_point" cx="576.2" cy="373.8" r="8"/>
	<circle id="se_box_hand_point" cx="576.2" cy="576.2" r="8"/>
	<circle id="sw_box_hand_point" cx="373.8" cy="576.2" r="8"/>
</g>
</svg>`;
    } else {
      // Diamond grid (default)
      return `<?xml version="1.0" encoding="utf-8"?>
<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px"
	 viewBox="0 0 950 950" style="enable-background:new 0 0 950 950;" xml:space="preserve">
<style type="text/css">
	.st0{fill:none;}
</style>
<g>
	<circle id="n_diamond_outer_point" cx="475" cy="175" r="25"/>
	<circle id="e_diamond_outer_point" cx="775" cy="475" r="25"/>
	<circle id="s_diamond_outer_point" cx="475" cy="775" r="25"/>
	<circle id="w_diamond_outer_point" cx="175" cy="475" r="25"/>
</g>
<g>
	<circle id="n_diamond_hand_point" cx="475" cy="331.9" r="8"/>
	<circle id="e_diamond_hand_point" cx="618.1" cy="475" r="8"/>
	<circle id="s_diamond_hand_point" cx="475" cy="618.1" r="8"/>
	<circle id="w_diamond_hand_point" cx="331.9" cy="475" r="8"/>
</g>
<circle id="center_point" cx="475" cy="475" r="12"/>
</svg>`;
    }
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
