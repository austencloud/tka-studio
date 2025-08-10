import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import OptionPickerSection from '../OptionPickerSection.svelte';
import type { PictographData } from '$lib/domain/PictographData';

// Mock ModernPictograph component
vi.mock('$lib/components/pictograph/ModernPictograph.svelte', () => ({
	default: vi.fn(() => ({
		$$: { fragment: null },
		$set: vi.fn(),
		$destroy: vi.fn()
	}))
}));

describe('OptionPickerSection', () => {
	const mockPictographs: PictographData[] = [
		{
			id: 'test-1',
			letter: 'A',
			end_position: 'BL',
			grid_data: { grid_mode: 'diamond' },
			arrows: {},
			props: {},
			motions: {}
		} as PictographData,
		{
			id: 'test-2', 
			letter: 'B',
			end_position: 'BR',
			grid_data: { grid_mode: 'diamond' },
			arrows: {},
			props: {},
			motions: {}
		} as PictographData
	];

	const defaultProps = {
		letterType: 'Type1',
		pictographs: mockPictographs,
		onPictographSelected: vi.fn(),
		containerWidth: 800,
		isExpanded: true
	};

	beforeEach(() => {
		vi.clearAllMocks();
	});

	describe('Basic Rendering', () => {
		it('should render section with correct letter type', () => {
			render(OptionPickerSection, { props: defaultProps });
			
			// Should render the section
			const section = screen.getByRole('region', { name: /Type1/i });
			expect(section).toBeInTheDocument();
		});

		it('should render pictographs when expanded', () => {
			render(OptionPickerSection, { props: defaultProps });
			
			// Should render pictograph containers
			const pictographContainers = screen.getAllByRole('button');
			expect(pictographContainers).toHaveLength(2);
		});

		it('should not render pictographs when collapsed', () => {
			render(OptionPickerSection, { 
				props: { ...defaultProps, isExpanded: false }
			});
			
			// Should not render pictograph containers when collapsed
			const pictographContainers = screen.queryAllByRole('button');
			expect(pictographContainers).toHaveLength(0);
		});
	});

	describe('Layout Configuration', () => {
		it('should calculate layout based on container width', () => {
			const { component } = render(OptionPickerSection, { 
				props: { ...defaultProps, containerWidth: 400 }
			});
			
			// Should render with appropriate grid layout
			const section = screen.getByRole('region');
			expect(section).toBeInTheDocument();
		});

		it('should handle different container sizes', () => {
			const { component } = render(OptionPickerSection, { 
				props: { ...defaultProps, containerWidth: 1200 }
			});
			
			// Should render with appropriate grid layout for larger container
			const section = screen.getByRole('region');
			expect(section).toBeInTheDocument();
		});
	});

	describe('Pictograph Selection', () => {
		it('should call onPictographSelected when pictograph is clicked', async () => {
			const mockOnSelect = vi.fn();
			render(OptionPickerSection, { 
				props: { ...defaultProps, onPictographSelected: mockOnSelect }
			});
			
			const pictographButtons = screen.getAllByRole('button');
			await pictographButtons[0].click();
			
			expect(mockOnSelect).toHaveBeenCalledWith(mockPictographs[0]);
		});

		it('should handle keyboard selection', async () => {
			const mockOnSelect = vi.fn();
			render(OptionPickerSection, { 
				props: { ...defaultProps, onPictographSelected: mockOnSelect }
			});
			
			const pictographButtons = screen.getAllByRole('button');
			pictographButtons[0].focus();
			await pictographButtons[0].dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter' }));
			
			expect(mockOnSelect).toHaveBeenCalledWith(mockPictographs[0]);
		});
	});

	describe('Empty State', () => {
		it('should show empty message when no pictographs provided', () => {
			render(OptionPickerSection, { 
				props: { ...defaultProps, pictographs: [] }
			});
			
			expect(screen.getByText(/No options available for this type/i)).toBeInTheDocument();
		});
	});

	describe('Accessibility', () => {
		it('should have proper ARIA attributes', () => {
			render(OptionPickerSection, { props: defaultProps });
			
			const pictographButtons = screen.getAllByRole('button');
			pictographButtons.forEach(button => {
				expect(button).toHaveAttribute('tabindex', '0');
			});
		});
	});
});
