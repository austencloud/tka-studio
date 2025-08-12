import { render, screen } from '@testing-library/svelte';
import { describe, it, expect, beforeEach, vi } from 'vitest';
import GeneratePanel from '../generate/GeneratePanel.svelte';

// Mock the device detection service
vi.mock('$lib/services/ServiceRegistry', () => ({
	resolve: vi.fn(() => ({
		getCapabilities: () => ({ hasTouch: false, hasMouse: true }),
		getResponsiveSettings: () => ({
			minTouchTarget: 44,
			elementSpacing: 16,
			allowScrolling: true,
			layoutDensity: 'comfortable',
			fontScaling: 1.0,
		}),
		onCapabilitiesChanged: () => () => {},
	})),
}));

// Mock the selector components
vi.mock('../tabs/generate/selectors/LevelSelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/LengthSelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/TurnIntensitySelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/GridModeSelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/GenerationModeToggle.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/PropContinuityToggle.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/LetterTypeSelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/SliceSizeSelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));
vi.mock('../tabs/generate/selectors/CAPTypeSelector.svelte', () => ({
	default: vi.fn(() => ({ $$: { on_mount: [], on_destroy: [] } })),
}));

describe('GeneratePanel Layout Tests', () => {
	beforeEach(() => {
		vi.clearAllMocks();
	});

	it('should render with proper grid layout structure', () => {
		render(GeneratePanel);

		// Check that the main container exists
		const panel = screen.getByText('Customize Your Sequence').closest('.generate-panel');
		expect(panel).toBeInTheDocument();

		// Check that settings container uses grid layout
		const settingsContainer = panel?.querySelector('.settings-container');
		expect(settingsContainer).toBeInTheDocument();
	});

	it('should have consistent section structure', () => {
		render(GeneratePanel);

		const panel = screen.getByText('Customize Your Sequence').closest('.generate-panel');
		const sections = panel?.querySelectorAll('.settings-section');

		// Should have 3 sections: Sequence Settings, Mode & Layout, and Mode-specific
		expect(sections).toHaveLength(3);

		// Each section should have a title and settings-grid
		sections?.forEach((section) => {
			expect(section.querySelector('.section-title')).toBeInTheDocument();
			expect(section.querySelector('.settings-grid')).toBeInTheDocument();
		});
	});

	it('should apply correct CSS classes for layout stability', () => {
		render(GeneratePanel);

		const panel = screen.getByText('Customize Your Sequence').closest('.generate-panel');
		const settingsContainer = panel?.querySelector('.settings-container');

		// Check that the container has proper CSS classes
		expect(settingsContainer).toHaveClass('settings-container');

		// Check that mode-specific section has the special class
		const modeSpecificSection = panel?.querySelector('.mode-specific-section');
		expect(modeSpecificSection).toBeInTheDocument();
		expect(modeSpecificSection).toHaveClass('settings-section', 'mode-specific-section');
	});

	it('should have proper responsive attributes', () => {
		render(GeneratePanel);

		const panel = screen.getByText('Customize Your Sequence').closest('.generate-panel');

		// Check data attributes for responsive behavior
		expect(panel).toHaveAttribute('data-layout');
		expect(panel).toHaveAttribute('data-allow-scroll');

		// Check CSS custom properties
		const style = panel?.getAttribute('style');
		expect(style).toBeTruthy();
		expect(style).toContain('--min-touch-target');
		expect(style).toContain('--element-spacing');
	});

	it('should maintain action section at bottom', () => {
		render(GeneratePanel);

		const panel = screen.getByText('Customize Your Sequence').closest('.generate-panel');
		const actionSection = panel?.querySelector('.action-section');

		expect(actionSection).toBeInTheDocument();

		// Action section should contain buttons
		const buttons = actionSection?.querySelectorAll('.action-button');
		expect(buttons?.length).toBeGreaterThan(0);
	});
});
