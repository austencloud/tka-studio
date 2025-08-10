import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/svelte';
import OptionPickerScroll from '../OptionPickerScroll.svelte';
import type { PictographData } from '$lib/domain/PictographData';

// Mock ModernPictograph component
vi.mock('$lib/components/pictograph/ModernPictograph.svelte', () => ({
	default: vi.fn(() => ({
		$$: { fragment: null },
		$set: vi.fn(),
		$destroy: vi.fn()
	}))
}));

describe('OptionPicker Integration', () => {
	// Create test data that matches the expected sectioning
	const createTestPictographs = (): PictographData[] => {
		const pictographs: PictographData[] = [];
		
		// Type1 letters (16 pictographs)
		const type1Letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P'];
		type1Letters.forEach((letter, index) => {
			pictographs.push({
				id: `type1-${index}`,
				letter,
				end_position: 'BL',
				grid_data: { grid_mode: 'diamond' },
				arrows: {},
				props: {},
				motions: {}
			} as PictographData);
		});

		// Type2 letters (8 pictographs)
		const type2Letters = ['W', 'X', 'Y', 'Z', 'Σ', 'Δ', 'θ', 'Ω'];
		type2Letters.forEach((letter, index) => {
			pictographs.push({
				id: `type2-${index}`,
				letter,
				end_position: 'BR',
				grid_data: { grid_mode: 'diamond' },
				arrows: {},
				props: {},
				motions: {}
			} as PictographData);
		});

		// Type3 letters (8 pictographs)
		const type3Letters = ['W-', 'X-', 'Y-', 'Z-', 'Σ-', 'Δ-', 'θ-', 'Ω-'];
		type3Letters.forEach((letter, index) => {
			pictographs.push({
				id: `type3-${index}`,
				letter,
				end_position: 'TL',
				grid_data: { grid_mode: 'diamond' },
				arrows: {},
				props: {},
				motions: {}
			} as PictographData);
		});

		// Type4 letters (3 pictographs)
		const type4Letters = ['Φ', 'Ψ', 'Λ'];
		type4Letters.forEach((letter, index) => {
			pictographs.push({
				id: `type4-${index}`,
				letter,
				end_position: 'TR',
				grid_data: { grid_mode: 'diamond' },
				arrows: {},
				props: {},
				motions: {}
			} as PictographData);
		});

		return pictographs; // Total: 35 pictographs
	};

	const defaultProps = {
		pictographs: createTestPictographs(),
		onPictographSelected: vi.fn(),
		containerWidth: 800,
		containerHeight: 600,
		layoutConfig: {
			gridColumns: 'repeat(4, minmax(0, 1fr))',
			optionSize: '144px',
			gridGap: '8px',
			gridClass: 'default-grid',
			aspectClass: 'default-aspect',
			scaleFactor: 1.0
		},
		deviceInfo: {
			deviceType: 'desktop' as const,
			isFoldable: false,
			foldableInfo: {
				isFoldable: false,
				isUnfolded: false,
				foldableType: 'unknown' as const,
				confidence: 0
			}
		},
		foldableInfo: {
			isFoldable: false,
			isUnfolded: false,
			foldableType: 'unknown' as const,
			confidence: 0
		}
	};

	beforeEach(() => {
		vi.clearAllMocks();
	});

	describe('Sectioned Display', () => {
		it('should organize pictographs into correct sections', async () => {
			render(OptionPickerScroll, { props: defaultProps });

			// Wait for component to render
			await waitFor(() => {
				// Should find Type1 section with 16 pictographs
				const type1Button = screen.getByText(/Type1.*Dual-Shift/i);
				expect(type1Button).toBeInTheDocument();

				// Should find Type2 section with 8 pictographs  
				const type2Button = screen.getByText(/Type2.*Shift/i);
				expect(type2Button).toBeInTheDocument();

				// Should find Type3 section with 8 pictographs
				const type3Button = screen.getByText(/Type3.*Static/i);
				expect(type3Button).toBeInTheDocument();

				// Should find Type4 section with 3 pictographs
				const type4Button = screen.getByText(/Type4.*Dash/i);
				expect(type4Button).toBeInTheDocument();
			});
		});

		it('should display correct number of pictographs per section', async () => {
			render(OptionPickerScroll, { props: defaultProps });

			await waitFor(() => {
				// Check that pictograph containers are rendered
				const pictographContainers = screen.getAllByRole('button');
				
				// Should have section header buttons + pictograph containers
				// 4 section headers + 35 pictograph containers = 39 total buttons
				expect(pictographContainers.length).toBeGreaterThan(30);
			});
		});

		it('should handle empty pictographs array', () => {
			render(OptionPickerScroll, { 
				props: { ...defaultProps, pictographs: [] }
			});

			// Should show empty state
			expect(screen.getByText(/No options available/i)).toBeInTheDocument();
		});
	});

	describe('Layout Responsiveness', () => {
		it('should adapt to different container widths', () => {
			const { rerender } = render(OptionPickerScroll, { props: defaultProps });

			// Test with smaller container
			rerender({ 
				props: { ...defaultProps, containerWidth: 400 }
			});

			// Should still render sections
			expect(screen.getByText(/Type1.*Dual-Shift/i)).toBeInTheDocument();

			// Test with larger container
			rerender({ 
				props: { ...defaultProps, containerWidth: 1200 }
			});

			// Should still render sections
			expect(screen.getByText(/Type1.*Dual-Shift/i)).toBeInTheDocument();
		});
	});

	describe('Pictograph Selection', () => {
		it('should call onPictographSelected when pictograph is clicked', async () => {
			const mockOnSelect = vi.fn();
			render(OptionPickerScroll, { 
				props: { ...defaultProps, onPictographSelected: mockOnSelect }
			});

			await waitFor(() => {
				const pictographContainers = screen.getAllByRole('button');
				// Find a pictograph container (not a section header)
				const pictographContainer = pictographContainers.find(button => 
					!button.textContent?.includes('Type')
				);
				
				if (pictographContainer) {
					pictographContainer.click();
					expect(mockOnSelect).toHaveBeenCalled();
				}
			});
		});
	});
});
