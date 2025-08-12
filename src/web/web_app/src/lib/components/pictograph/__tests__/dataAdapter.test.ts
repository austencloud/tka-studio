/**
 * Data Adapter Tests
 *
 * Tests for the legacy/modern data structure conversion functions
 */

import { createBeatData, createPictographData } from '$lib/domain';
import { ArrowType, GridMode } from '$lib/domain/enums';
import { describe, expect, it } from 'vitest';
import {
	beatDataToPictographData,
	ensureModernPictographData,
	extractLegacyArrowData,
	extractLegacyPropData,
	legacyToModernArrowData,
	legacyToModernPictographData,
	legacyToModernPropData,
	modernToLegacyPictographData,
} from '../dataAdapter';

describe('Data Adapter', () => {
	describe('legacyToModernPictographData', () => {
		it('should convert basic legacy data to modern format', () => {
			const legacy: any = {
				id: 'test-id',
				grid_data: { mode: 'diamond' },
				arrows: {
					blue: {
						id: 'blue-1',
						arrow_type: 'blue',
						color: 'blue',
						motion_type: 'pro',
						turns: 0,
						is_mirrored: false,
						start_orientation: 'in',
						end_orientation: 'in',
						rotation_direction: 'clockwise',
						position_x: 0,
						position_y: 0,
						rotation_angle: 0,
						is_visible: true,
						is_selected: false,
					},
					red: {
						id: 'red-1',
						arrow_type: 'red',
						color: 'red',
						motion_type: 'anti',
						turns: 0,
						is_mirrored: false,
						start_orientation: 'in',
						end_orientation: 'in',
						rotation_direction: 'clockwise',
						position_x: 0,
						position_y: 0,
						rotation_angle: 0,
						is_visible: true,
						is_selected: false,
					},
				},
				props: {
					blue: {
						id: 'blue-prop-1',
						prop_type: 'staff',
						color: 'blue',
						orientation: 'in',
						rotation_direction: 'no_rot',
						position_x: 0,
						position_y: 0,
						rotation_angle: 0,
						is_visible: true,
						is_selected: false,
					},
					red: {
						id: 'red-prop-1',
						prop_type: 'staff',
						color: 'red',
						orientation: 'in',
						rotation_direction: 'no_rot',
						position_x: 0,
						position_y: 0,
						rotation_angle: 0,
						is_visible: true,
						is_selected: false,
					},
				},
				motions: {
					blue: { motion_type: 'pro' },
					red: { motion_type: 'anti' },
				},
				letter: 'A',
			};

			const modern = legacyToModernPictographData(legacy);

			expect(modern.id).toBe('test-id');
			expect(modern.letter).toBe('A');
			expect(modern.arrows.blue).toEqual(legacy.arrows.blue);
			expect(modern.arrows.red).toEqual(legacy.arrows.red);
			expect(modern.props.blue).toEqual(legacy.props.blue);
			expect(modern.props.red).toEqual(legacy.props.red);
			expect(modern.motions.blue).toEqual(legacy.motions.blue);
			expect(modern.motions.red).toEqual(legacy.motions.red);
		});

		it('should handle missing arrows and props gracefully', () => {
			const legacy: any = {
				id: 'test-id-2',
				letter: 'B',
			};

			const modern = legacyToModernPictographData(legacy);

			expect(modern.id).toBe('test-id-2');
			expect(modern.letter).toBe('B');
			expect(modern.arrows.blue).toBeDefined();
			expect(modern.arrows.red).toBeDefined();
			expect(modern.props.blue).toBeDefined();
			expect(modern.props.red).toBeDefined();
		});
	});

	describe('modernToLegacyPictographData', () => {
		it('should convert modern data back to legacy format', () => {
			const modern = createPictographData({
				id: 'modern-test',
				letter: 'C',
				arrows: {
					blue: {
						id: 'blue-arrow',
						arrow_type: ArrowType.BLUE,
						color: 'blue',
						motion_type: 'pro',
						turns: 0,
						is_mirrored: false,
						start_orientation: 'in',
						end_orientation: 'in',
						rotation_direction: 'clockwise',
						position_x: 0,
						position_y: 0,
						rotation_angle: 0,
						is_visible: true,
						is_selected: false,
					},
					red: {
						id: 'red-arrow',
						arrow_type: ArrowType.RED,
						color: 'red',
						motion_type: 'anti',
						turns: 0,
						is_mirrored: false,
						start_orientation: 'in',
						end_orientation: 'in',
						rotation_direction: 'clockwise',
						position_x: 0,
						position_y: 0,
						rotation_angle: 0,
						is_visible: true,
						is_selected: false,
					},
				},
			});

			const legacy = modernToLegacyPictographData(modern);

			expect(legacy.id).toBe('modern-test');
			expect(legacy.letter).toBe('C');
			expect(legacy.arrows!.blue!.id).toBe('blue-arrow');
			expect(legacy.arrows!.red!.id).toBe('red-arrow');
		});
	});

	describe('beatDataToPictographData', () => {
		it('should extract pictograph data from beat', () => {
			const pictographData = createPictographData({
				letter: 'D',
				id: 'beat-pictograph',
			});

			const beat = createBeatData({
				beat_number: 1,
				pictograph_data: pictographData,
			});

			const result = beatDataToPictographData(beat);

			expect(result).toEqual(pictographData);
			expect(result?.letter).toBe('D');
			expect(result?.id).toBe('beat-pictograph');
		});

		it('should return null for beat without pictograph data', () => {
			const beat = createBeatData({
				beat_number: 1,
				is_blank: true,
			});

			const result = beatDataToPictographData(beat);

			expect(result).toBeNull();
		});
	});

	describe('extractLegacyArrowData', () => {
		it('should extract arrow data from legacy direct properties', () => {
			const legacy = {
				blueArrowData: {
					id: 'blue-legacy',
					motionType: 'pro',
					loc: 'n',
					turns: 1.5,
				},
				redArrowData: {
					id: 'red-legacy',
					motionType: 'anti',
					loc: 's',
					turns: 0.5,
				},
			};

			const result = extractLegacyArrowData(legacy);

			expect(result.blue).toBeDefined();
			expect(result.red).toBeDefined();
			expect(result.blue?.motion_type).toBe('pro');
			expect(result.blue?.location).toBe('n');
			expect(result.blue?.turns).toBe(1.5);
			expect(result.red?.motion_type).toBe('anti');
			expect(result.red?.location).toBe('s');
			expect(result.red?.turns).toBe(0.5);
		});

		it('should handle missing arrow data', () => {
			const legacy = {
				blueArrowData: {
					id: 'blue-only',
					motionType: 'float',
				},
			};

			const result = extractLegacyArrowData(legacy);

			expect(result.blue).toBeDefined();
			expect(result.red).toBeNull();
			expect(result.blue?.motion_type).toBe('float');
		});
	});

	describe('extractLegacyPropData', () => {
		it('should extract prop data from legacy direct properties', () => {
			const legacy = {
				bluePropData: {
					id: 'blue-prop-legacy',
					propType: 'staff',
					loc: 'ne',
					rotAngle: 45,
				},
				redPropData: {
					id: 'red-prop-legacy',
					propType: 'fan',
					loc: 'sw',
					rotAngle: 225,
				},
			};

			const result = extractLegacyPropData(legacy);

			expect(result.blue).toBeDefined();
			expect(result.red).toBeDefined();
			expect(result.blue?.prop_type).toBe('staff');
			expect(result.blue?.location).toBe('ne');
			expect(result.blue?.rotation_angle).toBe(45);
			expect(result.red?.prop_type).toBe('fan');
			expect(result.red?.location).toBe('sw');
			expect(result.red?.rotation_angle).toBe(225);
		});
	});

	describe('ensureModernPictographData', () => {
		it('should detect and convert legacy data with direct properties', () => {
			const legacy = {
				id: 'ensure-test',
				gridMode: 'box',
				letter: 'E',
				redArrowData: {
					motionType: 'dash',
					loc: 'w',
					turns: 2,
				},
				bluePropData: {
					propType: 'poi',
					loc: 'e',
					rotAngle: 90,
				},
			};

			const modern = ensureModernPictographData(legacy);

			expect(modern).toBeDefined();
			expect(modern?.id).toBe('ensure-test');
			expect(modern?.letter).toBe('E');
			expect(modern?.grid_data.grid_mode).toBe(GridMode.BOX);
			expect(modern?.arrows.red?.motion_type).toBe('dash');
			expect(modern?.arrows.red?.location).toBe('w');
			expect(modern?.props.blue?.prop_type).toBe('poi');
			expect(modern?.props.blue?.location).toBe('e');
		});

		it('should pass through already modern data', () => {
			const modern = createPictographData({
				letter: 'F',
				grid_data: {
					grid_mode: GridMode.DIAMOND,
					center_x: 0,
					center_y: 0,
					radius: 100,
					grid_points: {},
				},
			});

			const result = ensureModernPictographData(modern as unknown as Record<string, unknown>);

			expect(result).toEqual(modern);
		});

		it('should return null for invalid data', () => {
			const invalid = null;
			const result = ensureModernPictographData(
				invalid as unknown as Record<string, unknown>
			);
			expect(result).toBeNull();
		});

		it('should return null for empty object', () => {
			const empty = {};
			const result = ensureModernPictographData(empty);
			expect(result).toBeNull();
		});
	});

	describe('legacyToModernArrowData', () => {
		it('should convert legacy arrow with all properties', () => {
			const legacy = {
				id: 'arrow-test',
				motionType: 'pro',
				loc: 'n',
				startOri: 'in',
				endOri: 'out',
				propRotDir: 'clockwise',
				turns: 1.5,
				svgMirrored: true,
				coords: { x: 100, y: 200 },
				rotAngle: 45,
			};

			const modern = legacyToModernArrowData(legacy, 'blue');

			expect(modern.id).toBe('arrow-test');
			expect(modern.color).toBe('blue');
			expect(modern.motion_type).toBe('pro');
			expect(modern.location).toBe('n');
			expect(modern.start_orientation).toBe('in');
			expect(modern.end_orientation).toBe('out');
			expect(modern.rotation_direction).toBe('clockwise');
			expect(modern.turns).toBe(1.5);
			expect(modern.is_mirrored).toBe(true);
			expect(modern.coordinates).toEqual({ x: 100, y: 200 });
			expect(modern.rotation_angle).toBe(45);
		});

		it('should handle missing properties with defaults', () => {
			const legacy = {
				motionType: 'float',
			};

			const modern = legacyToModernArrowData(legacy, 'red');

			expect(modern.id).toBeDefined(); // Should generate UUID
			expect(modern.color).toBe('red');
			expect(modern.motion_type).toBe('float');
			expect(modern.location).toBe('center'); // Default
			expect(modern.turns).toBe(0); // Default
			expect(modern.is_mirrored).toBe(false); // Default
		});
	});

	describe('legacyToModernPropData', () => {
		it('should convert legacy prop with all properties', () => {
			const legacy = {
				id: 'prop-test',
				propType: 'fan',
				loc: 'se',
				coords: { x: 300, y: 400 },
				rotAngle: 135,
				svgCenter: { x: 50, y: 50 },
			};

			const modern = legacyToModernPropData(legacy, 'red');

			expect(modern.id).toBe('prop-test');
			expect(modern.color).toBe('red');
			expect(modern.prop_type).toBe('fan');
			expect(modern.location).toBe('se');
			expect(modern.coordinates).toEqual({ x: 300, y: 400 });
			expect(modern.rotation_angle).toBe(135);
			expect(modern.svg_center).toEqual({ x: 50, y: 50 });
		});

		it('should handle missing properties with defaults', () => {
			const legacy = {};

			const modern = legacyToModernPropData(legacy, 'blue');

			expect(modern.id).toBeDefined(); // Should generate UUID
			expect(modern.color).toBe('blue');
			expect(modern.prop_type).toBe('staff'); // Default
			expect(modern.location).toBe('center'); // Default
			expect(modern.rotation_angle).toBe(0); // Default
		});
	});
});
