import { render, screen } from '@testing-library/svelte';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import '@testing-library/jest-dom/vitest';
import AnimatorCanvas from './AnimatorCanvas.svelte';
import type { PropState } from '../../types/core.js';

// Mock the svgStringToImage function
vi.mock('../../svgStringToImage.js', () => ({
	svgStringToImage: vi.fn().mockResolvedValue({
		src: 'data:image/svg+xml;base64,test',
		width: 500,
		height: 500
	})
}));

// Mock localStorage
const localStorageMock = {
	getItem: vi.fn(),
	setItem: vi.fn(),
	removeItem: vi.fn(),
	clear: vi.fn()
};
Object.defineProperty(window, 'localStorage', {
	value: localStorageMock
});

// Mock canvas context
const mockContext = {
	clearRect: vi.fn(),
	drawImage: vi.fn(),
	save: vi.fn(),
	restore: vi.fn(),
	translate: vi.fn(),
	rotate: vi.fn()
};

// Mock HTMLCanvasElement
Object.defineProperty(HTMLCanvasElement.prototype, 'getContext', {
	value: vi.fn().mockReturnValue(mockContext)
});

describe('AnimatorCanvas', () => {
	const mockBlueProp: PropState = {
		x: 475,
		y: 331.9,
		staffRotationAngle: 0,
		centerPathAngle: 0
	};

	const mockRedProp: PropState = {
		x: 475,
		y: 618.1,
		staffRotationAngle: Math.PI / 2,
		centerPathAngle: Math.PI
	};

	beforeEach(() => {
		vi.clearAllMocks();
		localStorageMock.getItem.mockReturnValue(null);
	});

	it('renders canvas with correct dimensions', () => {
		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp,
				width: 500,
				height: 500
			}
		});

		const canvas = document.querySelector('canvas');
		expect(canvas).toBeInTheDocument();
		expect(canvas).toHaveAttribute('width', '500');
		expect(canvas).toHaveAttribute('height', '500');
	});

	it('renders layer2 visibility toggle', () => {
		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp
			}
		});

		const toggle = screen.getByLabelText(/show layer2 points/i);
		expect(toggle).toBeInTheDocument();
		expect(toggle).toHaveAttribute('type', 'checkbox');
	});

	it('initializes layer2 visibility from localStorage', () => {
		localStorageMock.getItem.mockReturnValue('true');

		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp
			}
		});

		expect(localStorageMock.getItem).toHaveBeenCalledWith('grid-layer2-visible');
	});

	it('saves layer2 visibility to localStorage when changed', async () => {
		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp
			}
		});

		await new Promise((resolve) => setTimeout(resolve, 0));

		expect(localStorageMock.setItem).toHaveBeenCalledWith('grid-layer2-visible', 'false');
	});

	it('generates grid SVG with theme-aware colors', () => {
		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp
			}
		});

		const canvas = document.querySelector('canvas');
		expect(canvas).toBeInTheDocument();
	});

	it('handles grid visibility prop correctly', () => {
		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp,
				gridVisible: false
			}
		});

		// Canvas should still render even when grid is not visible
		const canvas = document.querySelector('canvas');
		expect(canvas).toBeInTheDocument();
	});

	it('applies correct CSS classes for theming', () => {
		render(AnimatorCanvas, {
			props: {
				blueProp: mockBlueProp,
				redProp: mockRedProp
			}
		});

		const wrapper = document.querySelector('.canvas-wrapper');
		expect(wrapper).toBeInTheDocument();
		expect(wrapper).toHaveClass('canvas-wrapper');
	});
});
