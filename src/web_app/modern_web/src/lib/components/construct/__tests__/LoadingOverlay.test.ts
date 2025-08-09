/**
 * LoadingOverlay Component Tests
 *
 * Tests for the LoadingOverlay component extracted from ConstructTab
 */

import { describe, it, expect, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/svelte';
import '@testing-library/jest-dom';
import LoadingOverlay from '../LoadingOverlay.svelte';

describe('LoadingOverlay', () => {
	beforeEach(() => {
		// Clear any previous renders
	});

	describe('Basic Rendering', () => {
		it('should render with default message', () => {
			render(LoadingOverlay);

			const overlay = screen.getByTestId('loading-overlay');
			expect(overlay).toBeInTheDocument();

			const defaultMessage = screen.getByText('Processing...');
			expect(defaultMessage).toBeInTheDocument();

			const spinner = overlay.querySelector('.loading-spinner');
			expect(spinner).toBeInTheDocument();
		});

		it('should render with custom message', () => {
			render(LoadingOverlay, {
				props: {
					message: 'Custom loading message',
				},
			});

			const overlay = screen.getByTestId('loading-overlay');
			expect(overlay).toBeInTheDocument();

			const customMessage = screen.getByText('Custom loading message');
			expect(customMessage).toBeInTheDocument();
		});

		it('should have correct CSS classes', () => {
			const { container } = render(LoadingOverlay, {
				props: {
					message: 'Test message',
				},
			});

			const overlay = container.querySelector('.loading-overlay');
			expect(overlay).toBeInTheDocument();
			expect(overlay).toHaveClass('loading-overlay');

			const spinner = container.querySelector('.loading-spinner');
			expect(spinner).toBeInTheDocument();
			expect(spinner).toHaveClass('loading-spinner');
		});
	});

	describe('Message Display', () => {
		it('should handle empty message', () => {
			render(LoadingOverlay, {
				props: {
					message: '',
				},
			});

			const overlay = screen.getByTestId('loading-overlay');
			expect(overlay).toBeInTheDocument();

			// Should still render the paragraph element, just empty
			const messageElement = overlay.querySelector('p');
			expect(messageElement).toBeInTheDocument();
			expect(messageElement).toHaveTextContent('');
		});

		it('should handle long messages', () => {
			const longMessage =
				'This is a very long loading message that should still be displayed correctly';

			render(LoadingOverlay, {
				props: {
					message: longMessage,
				},
			});

			const messageText = screen.getByText(longMessage);
			expect(messageText).toBeInTheDocument();
		});

		it('should handle special characters in message', () => {
			const specialMessage = 'Loading with special chars: <>&"\'';

			render(LoadingOverlay, {
				props: {
					message: specialMessage,
				},
			});

			const messageText = screen.getByText(specialMessage);
			expect(messageText).toBeInTheDocument();
		});
	});

	describe('Spinner Animation', () => {
		it('should have spinner element with correct class', () => {
			const { container } = render(LoadingOverlay);

			const spinner = container.querySelector('.loading-spinner');
			expect(spinner).toBeInTheDocument();
			expect(spinner).toHaveClass('loading-spinner');
		});
	});

	describe('Overlay Structure', () => {
		it('should have correct CSS classes for styling', () => {
			const { container } = render(LoadingOverlay);

			const overlay = container.querySelector('.loading-overlay');
			expect(overlay).toBeInTheDocument();
			expect(overlay).toHaveClass('loading-overlay');
		});
	});

	describe('Accessibility', () => {
		it('should have proper test id', () => {
			render(LoadingOverlay, {
				props: {
					message: 'Accessible loading',
				},
			});

			const overlay = screen.getByTestId('loading-overlay');
			expect(overlay).toHaveAttribute('data-testid', 'loading-overlay');
		});

		it('should be properly structured for screen readers', () => {
			render(LoadingOverlay, {
				props: {
					message: 'Screen reader test',
				},
			});

			const overlay = screen.getByTestId('loading-overlay');
			const messageElement = screen.getByText('Screen reader test');

			expect(overlay).toContainElement(messageElement);
		});
	});
});
