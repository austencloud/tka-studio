// Constants and default data for the pictograph animator

export const CANVAS_SIZE = 600;
export const PI = Math.PI;
export const TWO_PI = 2 * PI;
export const HALF_PI = PI / 2;
export const GRID_VIEWBOX_SIZE = 950;
export const GRID_CENTER = GRID_VIEWBOX_SIZE / 2;
export const GRID_HALFWAY_POINT_OFFSET = 151.5;
export const STAFF_VIEWBOX_WIDTH = 252.8;
export const STAFF_VIEWBOX_HEIGHT = 77.8;
export const STAFF_CENTER_X = 126.4;
export const STAFF_CENTER_Y = 38.9;

export const gridScaleFactor = CANVAS_SIZE / GRID_VIEWBOX_SIZE;
export const scaledHalfwayRadius = GRID_HALFWAY_POINT_OFFSET * gridScaleFactor;

// Location angles mapping
export const locationAngles = { e: 0, s: HALF_PI, w: PI, n: -HALF_PI };

// SVG strings for images
export const gridSvgString = `<svg version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 950 950" style="enable-background:new 0 0 950 950; background-color: #ffffff;" xml:space="preserve"><g id="outer_points"><circle fill="#000000" cx="475" cy="175" r="25"/><circle fill="#000000" cx="775" cy="475" r="25"/><circle fill="#000000" cx="475" cy="775" r="25"/><circle fill="#000000" cx="175" cy="475" r="25"/></g><g id="halfway_points"><circle fill="#000000" cx="475" cy="323.5" r="8"/><circle fill="#000000" cx="626.5" cy="475" r="8"/><circle fill="#000000" cx="475" cy="626.5" r="8"/><circle fill="#000000" cx="323.5" cy="475" r="8"/></g><g id="center_group"><circle fill="#000000" cx="475" cy="475" r="12"/></g></svg>`;

export const staffBaseSvgString = (fillColor: string) =>
  `<svg version="1.1" id="staff" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" x="0px" y="0px" viewBox="0 0 252.8 77.8" style="enable-background:new 0 0 252.8 77.8;" xml:space="preserve"><path fill="${fillColor}" stroke="#555555" stroke-width="1" stroke-miterlimit="10" d="M251.4,67.7V10.1c0-4.8-4.1-8.7-9.1-8.7s-9.1,3.9-9.1,8.7v19.2H10.3c-4.9,0-8.9,3.8-8.9,8.5V41 c0,4.6,4,8.5,8.9,8.5h222.9v18.2c0,4.8,4.1,8.7,9.1,8.7S251.4,72.5,251.4,67.7z"/><circle id="centerPoint" fill="#FF0000" cx="126.4" cy="38.9" r="5" /></svg>`;

// Default sequence data
export const defaultSequence = [
  {
    word: "ALFBBLFA",
    author: "Austen Cloud",
    level: 0,
    prop_type: "staff",
    grid_mode: "diamond",
    is_circular: false,
    can_be_CAP: false,
    is_strict_rotated_CAP: false,
    is_strict_mirrored_CAP: false,
    is_strict_swapped_CAP: false,
    is_mirrored_swapped_CAP: false,
    is_rotated_swapped_CAP: false,
  },
  {
    beat: 0,
    sequence_start_position: "alpha",
    letter: "α",
    end_pos: "alpha1",
    timing: "none",
    direction: "none",
    blue_attributes: {
      start_loc: "s",
      end_loc: "s",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    },
    red_attributes: {
      start_loc: "n",
      end_loc: "n",
      start_ori: "in",
      end_ori: "in",
      prop_rot_dir: "no_rot",
      turns: 0,
      motion_type: "static",
    },
  },
  {
    beat: 1,
    letter: "A",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha1",
    end_pos: "alpha3",
    timing: "split",
    direction: "same",
    blue_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "s",
      end_loc: "w",
      turns: 0,
      end_ori: "in",
    },
    red_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "n",
      end_loc: "e",
      turns: 0,
      end_ori: "in",
    },
  },
  {
    beat: 2,
    letter: "L",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha3",
    end_pos: "beta1",
    timing: "tog",
    direction: "opp",
    blue_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "w",
      end_loc: "n",
      turns: 0,
      end_ori: "in",
    },
    red_attributes: {
      motion_type: "anti",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "e",
      end_loc: "n",
      turns: 0,
      end_ori: "out",
    },
  },
  {
    beat: 3,
    letter: "F",
    letter_type: "Type1",
    duration: 1,
    start_pos: "beta1",
    end_pos: "alpha7",
    timing: "tog",
    direction: "opp",
    blue_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "n",
      end_loc: "e",
      turns: 0,
      end_ori: "in",
    },
    red_attributes: {
      motion_type: "anti",
      start_ori: "out",
      prop_rot_dir: "cw",
      start_loc: "n",
      end_loc: "w",
      turns: 0,
      end_ori: "in",
    },
  },
  {
    beat: 4,
    letter: "B",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha7",
    end_pos: "alpha5",
    timing: "split",
    direction: "same",
    blue_attributes: {
      motion_type: "anti",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "e",
      end_loc: "n",
      turns: 0,
      end_ori: "out",
    },
    red_attributes: {
      motion_type: "anti",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "w",
      end_loc: "s",
      turns: 0,
      end_ori: "out",
    },
  },
  {
    beat: 5,
    letter: "B",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha5",
    end_pos: "alpha3",
    timing: "split",
    direction: "same",
    blue_attributes: {
      motion_type: "anti",
      start_ori: "out",
      prop_rot_dir: "cw",
      start_loc: "n",
      end_loc: "w",
      turns: 0,
      end_ori: "in",
    },
    red_attributes: {
      motion_type: "anti",
      start_ori: "out",
      prop_rot_dir: "cw",
      start_loc: "s",
      end_loc: "e",
      turns: 0,
      end_ori: "in",
    },
  },
  {
    beat: 6,
    letter: "L",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha3",
    end_pos: "beta5",
    timing: "tog",
    direction: "opp",
    blue_attributes: {
      motion_type: "anti",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "w",
      end_loc: "s",
      turns: 0,
      end_ori: "out",
    },
    red_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "e",
      end_loc: "s",
      turns: 0,
      end_ori: "in",
    },
  },
  {
    beat: 7,
    letter: "F",
    letter_type: "Type1",
    duration: 1,
    start_pos: "beta5",
    end_pos: "alpha7",
    timing: "tog",
    direction: "opp",
    blue_attributes: {
      motion_type: "anti",
      start_ori: "out",
      prop_rot_dir: "cw",
      start_loc: "s",
      end_loc: "e",
      turns: 0,
      end_ori: "in",
    },
    red_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "s",
      end_loc: "w",
      turns: 0,
      end_ori: "in",
    },
  },
  {
    beat: 8,
    letter: "A",
    letter_type: "Type1",
    duration: 1,
    start_pos: "alpha7",
    end_pos: "alpha1",
    timing: "split",
    direction: "same",
    blue_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "e",
      end_loc: "s",
      turns: 0,
      end_ori: "in",
    },
    red_attributes: {
      motion_type: "pro",
      start_ori: "in",
      prop_rot_dir: "cw",
      start_loc: "w",
      end_loc: "n",
      turns: 0,
      end_ori: "in",
    },
  },
];

// Metadata for SEO and accessibility
export const title = "Pictograph Animator - Interactive Flow Art Visualization";
export const description =
  "Visualize and animate flow art patterns with this interactive tool for props like poi, staff, and hoops.";
