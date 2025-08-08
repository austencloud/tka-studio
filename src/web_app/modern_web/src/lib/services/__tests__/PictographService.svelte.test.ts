/**
 * PictographService Svelte 5 Runes Tests
 * 
 * Tests for the rune-based pictograph service
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { createPictographService, createBeatPictographService } from '../PictographService.svelte';
import { createBeatData, createPictographData } from '$lib/domain';

describe('PictographService (Runes)', () => {
	let service: ReturnType<typeof createPictographService>;

	beforeEach(() => {
		service = createPictographService({
			debugMode: false,
			loadingTimeout: 1000
		});
	});

	describe('Initial State', () => {
		it('should start with clean initial state', () => {
			expect(service.currentData).toBeNull();
			expect(service.isLoading).toBe(false);
			expect(service.errorMessage).toBeNull();
			expect(service.loadingProgress).toBe(0);
			expect(service.hasValidData).toBe(false);
		});
	});

	describe('setPictographData', () => {
		it('should set pictograph data and start loading', () => {
			const pictographData = createPictographData({
				letter: 'A',
				grid_data: { mode: 'diamond' },
				arrows: {
					blue: {
						id: 'blue-arrow',
						arrow_type: 'blue',
						color: 'blue',
						motion_type: 'pro',
						location: 'n',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'clockwise',
						turns: 1,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 0,
						svg_center: null,
						svg_mirrored: false,
						metadata: {}
					},
					red: {
						id: 'red-arrow',
						arrow_type: 'red',
						color: 'red',
						motion_type: 'anti',
						location: 's',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'counter_clockwise',
						turns: 1,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 180,
						svg_center: null,
						svg_mirrored: false,
						metadata: {}
					}
				}
			});

			service.setPictographData(pictographData);

			expect(service.currentData).toEqual(pictographData);
			expect(service.hasValidData).toBe(true);
			expect(service.isLoading).toBe(true);
			expect(service.errorMessage).toBeNull();
		});

		it('should handle invalid data gracefully', () => {
			const invalidData = null;

			service.setPictographData(invalidData);

			expect(service.currentData).toBeNull();
			expect(service.hasValidData).toBe(false);
			expect(service.isLoading).toBe(false);
			expect(service.errorMessage).toBe('Invalid pictograph data provided');
		});

		it('should convert legacy data format', () => {
			const legacyData = {
				id: 'legacy-test',
				gridMode: 'box',
				letter: 'B',
				redArrowData: {
					motionType: 'pro',
					loc: 'e',
					turns: 1.5
				}
			};

			service.setPictographData(legacyData);

			expect(service.currentData).toBeDefined();
			expect(service.currentData?.letter).toBe('B');
			expect(service.currentData?.grid_data.mode).toBe('box');
			expect(service.currentData?.arrows.red?.motion_type).toBe('pro');
			expect(service.currentData?.arrows.red?.location).toBe('e');
			expect(service.hasValidData).toBe(true);
		});
	});

	describe('setBeatData', () => {
		it('should set data from beat with pictograph', () => {
			const pictographData = createPictographData({
				letter: 'C',
				grid_data: { mode: 'diamond' }
			});

			const beatData = createBeatData({
				beat_number: 1,
				pictograph_data: pictographData
			});

			service.setBeatData(beatData);

			expect(service.currentData).toEqual(pictographData);
			expect(service.hasValidData).toBe(true);
			expect(service.isLoading).toBe(true);
		});

		it('should clear data for beat without pictograph', () => {
			// First set some data
			const pictographData = createPictographData({ letter: 'D' });
			service.setPictographData(pictographData);
			expect(service.hasValidData).toBe(true);

			// Then set blank beat
			const blankBeat = createBeatData({
				beat_number: 2,
				is_blank: true
			});

			service.setBeatData(blankBeat);

			expect(service.currentData).toBeNull();
			expect(service.hasValidData).toBe(false);
			expect(service.isLoading).toBe(false);
		});
	});

	describe('Component Loading Tracking', () => {
		beforeEach(() => {
			const pictographData = createPictographData({
				letter: 'E',
				arrows: {
					blue: {
						id: 'blue',
						arrow_type: 'blue',
						color: 'blue',
						motion_type: 'pro',
						location: 'n',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'clockwise',
						turns: 1,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 0,
						svg_center: null,
						svg_mirrored: false,
						metadata: {}
					},
					red: {
						id: 'red',
						arrow_type: 'red',
						color: 'red',
						motion_type: 'anti',
						location: 's',
						start_orientation: 'in',
						end_orientation: 'out',
						rotation_direction: 'counter_clockwise',
						turns: 1,
						is_mirrored: false,
						coordinates: null,
						rotation_angle: 180,
						svg_center: null,
						svg_mirrored: false,
						metadata: {}
					}
				},
				props: {
					blue: {
						id: 'blue-prop',
						prop_type: 'staff',
						color: 'blue',
						location: 'n',
						coordinates: null,
						rotation_angle: 0,
						svg_center: null,
						metadata: {}
					},
					red: {
						id: 'red-prop',
						prop_type: 'staff',
						color: 'red',
						location: 's',
						coordinates: null,
						rotation_angle: 180,
						svg_center: null,
						metadata: {}
					}
				}
			});

			service.setPictographData(pictographData);
		});

		it('should track component loading progress', () => {
			expect(service.isLoading).toBe(true);
			expect(service.loadingProgress).toBe(0); // 0 of 5 components loaded

			service.markComponentLoaded('grid');
			expect(service.loadingProgress).toBe(20); // 1 of 5 components loaded

			service.markComponentLoaded('blue-arrow');
			expect(service.loadingProgress).toBe(40); // 2 of 5 components loaded

			service.markComponentLoaded('red-arrow');
			expect(service.loadingProgress).toBe(60); // 3 of 5 components loaded

			service.markComponentLoaded('blue-prop');
			expect(service.loadingProgress).toBe(80); // 4 of 5 components loaded

			service.markComponentLoaded('red-prop');
			expect(service.loadingProgress).toBe(100); // 5 of 5 components loaded
			expect(service.isLoading).toBe(false); // Should auto-complete
		});

		it('should handle component errors gracefully', () => {
			service.markComponentError('grid', 'Failed to load grid SVG');

			expect(service.errorMessage).toBe('grid: Failed to load grid SVG');
			expect(service.loadingProgress).toBe(20); // Still marks as loaded to prevent blocking
		});

		it('should complete loading even with errors', () => {
			service.markComponentLoaded('grid');
			service.markComponentError('blue-arrow', 'Network error');
			service.markComponentLoaded('red-arrow');
			service.markComponentLoaded('blue-prop');
			service.markComponentLoaded('red-prop');

			expect(service.isLoading).toBe(false);
			expect(service.loadingProgress).toBe(100);
			expect(service.errorMessage).toBe('blue-arrow: Network error');
		});
	});

	describe('Service Configuration', () => {
		it('should create service with custom config', () => {
			const customService = createPictographService({
				debugMode: true,
				defaultGridMode: 'box',
				loadingTimeout: 2000
			});

			const config = customService.getConfig();
			expect(config.debugMode).toBe(true);
			expect(config.defaultGridMode).toBe('box');
			expect(config.loadingTimeout).toBe(2000);
		});

		it('should allow toggling debug mode', () => {
			const config = service.getConfig();
			expect(config.debugMode).toBe(false);

			service.setDebugMode(true);
			const updatedConfig = service.getConfig();
			expect(updatedConfig.debugMode).toBe(true);
		});
	});

	describe('reset', () => {
		it('should reset service to initial state', () => {
			// Set up some state
			const pictographData = createPictographData({ letter: 'F' });
			service.setPictographData(pictographData);
			service.markComponentLoaded('grid');
			service.markComponentError('arrow', 'Some error');

			// Reset
			service.reset();

			expect(service.currentData).toBeNull();
			expect(service.isLoading).toBe(false);
			expect(service.errorMessage).toBeNull();
			expect(service.loadingProgress).toBe(0);
			expect(service.hasValidData).toBe(false);
		});
	});
});

describe('createBeatPictographService', () => {
	it('should create service bound to specific beat', () => {
		const pictographData = createPictographData({
			letter: 'G'
		});

		const beatData = createBeatData({
			beat_number: 3,
			pictograph_data: pictographData
		});

		const beatService = createBeatPictographService(beatData, {
			debugMode: true
		});

		expect(beatService.currentData).toEqual(pictographData);
		expect(beatService.hasValidData).toBe(true);
		expect(beatService.getConfig().debugMode).toBe(true);
	});

	it('should handle blank beat', () => {
		const blankBeat = createBeatData({
			beat_number: 4,
			is_blank: true
		});

		const beatService = createBeatPictographService(blankBeat);

		expect(beatService.currentData).toBeNull();
		expect(beatService.hasValidData).toBe(false);
	});
});
