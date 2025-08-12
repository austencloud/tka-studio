/**
 * ModernPictograph Component Tests
 *
 * Tests for the main pictograph orchestrator component
 */

import { createBeatData, createPictographData } from '$lib/domain';
import { GridMode } from '$lib/domain/enums';
import '@testing-library/jest-dom';
import { render, screen } from '@testing-library/svelte';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import ModernPictograph from '../Pictograph.svelte';

// Mock the child components
vi.mock('../Grid.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [], props: {} } })),
}));

vi.mock('../Prop.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [], props: {} } })),
}));

vi.mock('../Arrow.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [], props: {} } })),
}));

vi.mock('../TKAGlyph.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [], props: {} } })),
}));

describe('ModernPictograph', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	describe('Basic Rendering', () => {
		it('should render with pictograph data', () => {
			const pictographData = createPictographData({
				letter: 'A',
				// Provide full grid_data shape matching domain (tests previously used legacy 'mode')
				grid_data: {
					grid_mode: GridMode.DIAMOND,
					center_x: 0,
					center_y: 0,
					radius: 100,
					grid_points: {},
				},
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toBeInTheDocument();
			expect(svg).toHaveAttribute('width', '300');
			expect(svg).toHaveAttribute('height', '300');
		});

		it('should render with beat data', () => {
			const pictographData = createPictographData({
				letter: 'B',
				grid_data: {
					grid_mode: GridMode.BOX,
					center_x: 0,
					center_y: 0,
					radius: 100,
					grid_points: {},
				},
			});

			const beatData = createBeatData({
				beat_number: 1,
				pictograph_data: pictographData,
			});

			render(ModernPictograph, {
				props: {
					beatData,
					width: 200,
					height: 200,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toBeInTheDocument();
			expect(svg).toHaveAttribute('viewBox', '0 0 950 950');
		});

		it('should render empty state when no data provided', () => {
			render(ModernPictograph, {
				props: {
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toBeInTheDocument();

			// Should show empty state
			const emptyText = screen.getByText('Empty');
			expect(emptyText).toBeInTheDocument();
		});
	});

	describe('Clickable Behavior', () => {
		it('should render as button when onClick provided', () => {
			const handleClick = vi.fn();
			const pictographData = createPictographData({
				letter: 'C',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					onClick: handleClick,
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('button');
			expect(svg).toBeInTheDocument();
			expect(svg).toHaveAttribute('tabindex', '0');
		});

		it('should render as img when no onClick provided', () => {
			const pictographData = createPictographData({
				letter: 'D',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toBeInTheDocument();
			expect(svg).toHaveAttribute('tabindex', '-1');
		});
	});

	describe('Beat Number Display', () => {
		it('should show beat number when provided', () => {
			const pictographData = createPictographData({
				letter: 'E',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					beatNumber: 5,
					width: 300,
					height: 300,
				},
			});

			const beatNumberText = screen.getByText('5');
			expect(beatNumberText).toBeInTheDocument();
		});

		it('should show START label for start position', () => {
			const pictographData = createPictographData({
				letter: 'F',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					isStartPosition: true,
					width: 300,
					height: 300,
				},
			});

			const startText = screen.getByText('START');
			expect(startText).toBeInTheDocument();
		});

		it('should not show beat number for start position', () => {
			const pictographData = createPictographData({
				letter: 'G',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					beatNumber: 1,
					isStartPosition: true,
					width: 300,
					height: 300,
				},
			});

			const startText = screen.getByText('START');
			expect(startText).toBeInTheDocument();

			const beatNumberText = screen.queryByText('1');
			expect(beatNumberText).not.toBeInTheDocument();
		});
	});

	describe('Debug Mode', () => {
		it('should show debug info when debug enabled', () => {
			const pictographData = createPictographData({
				id: 'debug-test-id',
				letter: 'H',
				grid_data: {
					grid_mode: GridMode.DIAMOND,
					center_x: 0,
					center_y: 0,
					radius: 100,
					grid_points: {},
				},
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					debug: true,
					width: 300,
					height: 300,
				},
			});

			// Should show abbreviated ID
			const debugId = screen.getByText(/debug-test-id/);
			expect(debugId).toBeInTheDocument();

			// Should show grid mode
			const gridMode = screen.getByText(/Grid: diamond/);
			expect(gridMode).toBeInTheDocument();

			// Should show letter
			const letter = screen.getByText(/Letter: H/);
			expect(letter).toBeInTheDocument();
		});

		it('should not show debug info when debug disabled', () => {
			const pictographData = createPictographData({
				id: 'no-debug-test-id',
				letter: 'I',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					debug: false,
					width: 300,
					height: 300,
				},
			});

			const debugId = screen.queryByText(/no-debug-test-id/);
			expect(debugId).not.toBeInTheDocument();
		});
	});

	describe('Letter Display', () => {
		it('should show letter from pictograph data', () => {
			const pictographData = createPictographData({
				letter: 'J',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					width: 300,
					height: 300,
				},
			});

			// Letter should be rendered by TKAGlyph component
			// Since we mocked TKAGlyph, we'll verify the props would be passed correctly
			const svg = screen.getByRole('img');
			expect(svg).toBeInTheDocument();
		});

		it('should show beat number for beat without letter', () => {
			const beatData = createBeatData({
				beat_number: 7,
				is_blank: false,
			});

			render(ModernPictograph, {
				props: {
					beatData,
					width: 300,
					height: 300,
				},
			});

			const beatNumber = screen.getByText('7');
			expect(beatNumber).toBeInTheDocument();
		});
	});

	describe('Component State Classes', () => {
		it('should have loading class during initial state', () => {
			const pictographData = createPictographData({
				letter: 'K',
			});

			const { container } = render(ModernPictograph, {
				props: {
					pictographData,
					width: 300,
					height: 300,
				},
			});

			const pictographContainer = container.querySelector('.modern-pictograph');
			expect(pictographContainer).toHaveClass('loading');
		});

		it('should have clickable class when onClick provided', () => {
			const handleClick = vi.fn();
			const pictographData = createPictographData({
				letter: 'L',
			});

			const { container } = render(ModernPictograph, {
				props: {
					pictographData,
					onClick: handleClick,
					width: 300,
					height: 300,
				},
			});

			const pictographContainer = container.querySelector('.modern-pictograph');
			expect(pictographContainer).toHaveClass('clickable');
		});

		it('should have debug-mode class when debug enabled', () => {
			const pictographData = createPictographData({
				letter: 'M',
			});

			const { container } = render(ModernPictograph, {
				props: {
					pictographData,
					debug: true,
					width: 300,
					height: 300,
				},
			});

			const pictographContainer = container.querySelector('.modern-pictograph');
			expect(pictographContainer).toHaveClass('debug-mode');
		});
	});

	describe('Accessibility', () => {
		it('should have proper aria-label for regular pictograph', () => {
			const pictographData = createPictographData({
				letter: 'N',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					beatNumber: 3,
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toHaveAttribute('aria-label', 'Beat 3 Pictograph');
		});

		it('should have proper aria-label for start position', () => {
			const pictographData = createPictographData({
				letter: 'O',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
					isStartPosition: true,
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toHaveAttribute('aria-label', 'Start Position');
		});
	});

	describe('Props Validation', () => {
		it('should handle missing width/height with defaults', () => {
			const pictographData = createPictographData({
				letter: 'P',
			});

			render(ModernPictograph, {
				props: {
					pictographData,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toHaveAttribute('width', '300'); // Default
			expect(svg).toHaveAttribute('height', '300'); // Default
		});

		it('should handle both pictographData and beatData being null', () => {
			render(ModernPictograph, {
				props: {
					pictographData: null,
					beatData: null,
					width: 300,
					height: 300,
				},
			});

			const svg = screen.getByRole('img');
			expect(svg).toBeInTheDocument();

			// Should show empty state
			const emptyText = screen.getByText('Empty');
			expect(emptyText).toBeInTheDocument();
		});
	});
});
