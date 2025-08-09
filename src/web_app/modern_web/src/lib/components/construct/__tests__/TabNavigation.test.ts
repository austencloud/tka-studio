/**
 * TabNavigation Component Tests
 *
 * Tests for the TabNavigation component extracted from ConstructTab
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/svelte';
import '@testing-library/jest-dom';
import TabNavigation from '../TabNavigation.svelte';

// Mock the stores and services
vi.mock('$stores/constructTabState.svelte', () => {
	const mockConstructTabState = {
		activeRightPanel: 'build',
	};
	return {
		constructTabState: mockConstructTabState,
	};
});

vi.mock('$services/implementations/ConstructTabTransitionService', () => {
	const mockTransitionService = {
		handleMainTabTransition: vi.fn(),
	};
	return {
		constructTabTransitionService: mockTransitionService,
	};
});

describe('TabNavigation', () => {
	beforeEach(async () => {
		vi.clearAllMocks();
		const { constructTabState } = await import('$stores/constructTabState.svelte');
		constructTabState.activeRightPanel = 'build';
	});

	describe('Basic Rendering', () => {
		it('should render all four tab buttons', () => {
			render(TabNavigation);

			const navigation = screen.getByTestId('tab-navigation');
			expect(navigation).toBeInTheDocument();

			const buildButton = screen.getByText('🔨 Build');
			const generateButton = screen.getByText('🤖 Generate');
			const editButton = screen.getByText('🔧 Edit');
			const exportButton = screen.getByText('🔤 Export');

			expect(buildButton).toBeInTheDocument();
			expect(generateButton).toBeInTheDocument();
			expect(editButton).toBeInTheDocument();
			expect(exportButton).toBeInTheDocument();
		});

		it('should have correct CSS classes', () => {
			const { container } = render(TabNavigation);

			const navigation = container.querySelector('.main-tab-navigation');
			expect(navigation).toBeInTheDocument();
			expect(navigation).toHaveClass('main-tab-navigation');

			const buttons = container.querySelectorAll('.main-tab-btn');
			expect(buttons).toHaveLength(4);
			buttons.forEach((button) => {
				expect(button).toHaveClass('main-tab-btn');
			});
		});
	});

	describe('Active State Management', () => {
		it('should mark build tab as active by default', async () => {
			const { constructTabState } = await import('$stores/constructTabState.svelte');
			constructTabState.activeRightPanel = 'build';
			render(TabNavigation);

			const buildButton = screen.getByText('🔨 Build');
			expect(buildButton).toHaveClass('active');

			const generateButton = screen.getByText('🤖 Generate');
			expect(generateButton).not.toHaveClass('active');
		});

		it('should mark generate tab as active when selected', async () => {
			const { constructTabState } = await import('$stores/constructTabState.svelte');
			constructTabState.activeRightPanel = 'generate';
			render(TabNavigation);

			const generateButton = screen.getByText('🤖 Generate');
			expect(generateButton).toHaveClass('active');

			const buildButton = screen.getByText('🔨 Build');
			expect(buildButton).not.toHaveClass('active');
		});

		it('should mark edit tab as active when selected', async () => {
			const { constructTabState } = await import('$stores/constructTabState.svelte');
			constructTabState.activeRightPanel = 'edit';
			render(TabNavigation);

			const editButton = screen.getByText('🔧 Edit');
			expect(editButton).toHaveClass('active');

			const buildButton = screen.getByText('🔨 Build');
			expect(buildButton).not.toHaveClass('active');
		});

		it('should mark export tab as active when selected', async () => {
			const { constructTabState } = await import('$stores/constructTabState.svelte');
			constructTabState.activeRightPanel = 'export';
			render(TabNavigation);

			const exportButton = screen.getByText('🔤 Export');
			expect(exportButton).toHaveClass('active');

			const buildButton = screen.getByText('🔨 Build');
			expect(buildButton).not.toHaveClass('active');
		});
	});

	describe('Tab Click Handling', () => {
		it('should call transition service when build tab is clicked', async () => {
			render(TabNavigation);

			const buildButton = screen.getByText('🔨 Build');
			await fireEvent.click(buildButton);

			const { constructTabTransitionService } = await import(
				'$services/implementations/ConstructTabTransitionService'
			);
			expect(constructTabTransitionService.handleMainTabTransition).toHaveBeenCalledWith(
				'build'
			);
		});

		it('should call transition service when generate tab is clicked', async () => {
			render(TabNavigation);

			const generateButton = screen.getByText('🤖 Generate');
			await fireEvent.click(generateButton);

			const { constructTabTransitionService } = await import(
				'$services/implementations/ConstructTabTransitionService'
			);
			expect(constructTabTransitionService.handleMainTabTransition).toHaveBeenCalledWith(
				'generate'
			);
		});

		it('should call transition service when edit tab is clicked', async () => {
			render(TabNavigation);

			const editButton = screen.getByText('🔧 Edit');
			await fireEvent.click(editButton);

			const { constructTabTransitionService } = await import(
				'$services/implementations/ConstructTabTransitionService'
			);
			expect(constructTabTransitionService.handleMainTabTransition).toHaveBeenCalledWith(
				'edit'
			);
		});

		it('should call transition service when export tab is clicked', async () => {
			render(TabNavigation);

			const exportButton = screen.getByText('🔤 Export');
			await fireEvent.click(exportButton);

			const { constructTabTransitionService } = await import(
				'$services/implementations/ConstructTabTransitionService'
			);
			expect(constructTabTransitionService.handleMainTabTransition).toHaveBeenCalledWith(
				'export'
			);
		});
	});

	describe('Keyboard Accessibility', () => {
		it('should handle keyboard navigation', async () => {
			render(TabNavigation);

			const buildButton = screen.getByText('🔨 Build');
			buildButton.focus();

			await fireEvent.keyDown(buildButton, { key: 'Enter' });
			const { constructTabTransitionService } = await import(
				'$services/implementations/ConstructTabTransitionService'
			);
			expect(constructTabTransitionService.handleMainTabTransition).toHaveBeenCalledWith(
				'build'
			);
		});

		it('should be focusable', () => {
			render(TabNavigation);

			const buttons = screen.getAllByRole('button');
			buttons.forEach((button) => {
				button.focus();
				expect(button).toHaveFocus();
			});
		});
	});

	describe('Accessibility', () => {
		it('should have proper test id', () => {
			render(TabNavigation);

			const navigation = screen.getByTestId('tab-navigation');
			expect(navigation).toHaveAttribute('data-testid', 'tab-navigation');
		});

		it('should have proper button roles', () => {
			render(TabNavigation);

			const buttons = screen.getAllByRole('button');
			expect(buttons).toHaveLength(4);

			buttons.forEach((button) => {
				expect(button).toHaveAttribute('type', 'button');
			});
		});
	});
});
